# SPDX-License-Identifier: Apache-2.0
"""Loopback KA-9/10 service. POSIX process cancellation; no order-write endpoint."""
import argparse
from html import escape
from contextlib import contextmanager
from copy import deepcopy
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
from urllib.parse import urlsplit, parse_qs
import uuid
from contracts import encode, no_duplicates, reject_constant
from reliable_runtime import Principal, Store
from service_ops import ROOT, manifest, verify_manifest, Releases, ResponseCache, TokenBucket, CircuitBreaker, Feedback, sli

TERMINAL = {'answered','abstained','refused','cancelled','error'}
UI = Path(__file__).parent / 'service-ui'


class Job:
    def __init__(self, principal, request, release, fault, deadline):
        self.id = uuid.uuid4().hex
        self.principal, self.request, self.release, self.fault = principal, request, release, fault
        self.arrival = time.monotonic()
        self.deadline = self.arrival + deadline
        self.state, self.result = 'accepted', None
        self.events, self.spans = [], []
        self.stop, self.done = threading.Event(), threading.Event()
        self.lock = threading.RLock()
        self.root_span = uuid.uuid4().hex[:16]
        self.event('accepted')

    def event(self, stage, **fields):
        with self.lock:
            self.events.append(dict(id=len(self.events)+1, stage=stage,
                                    elapsed_ms=round((time.monotonic()-self.arrival)*1000,3), **fields))

    def public(self):
        with self.lock:
            return dict(request_id=self.id, state=self.state, result=deepcopy(self.result))

    def trace(self):
        with self.lock:
            return dict(trace_id=self.id, manifest=self.release['digest'], release_name=self.release['name'],
                        request=deepcopy(self.request), state=self.state, result=deepcopy(self.result),
                        events=deepcopy(self.events), spans=deepcopy(self.spans),
                        model_calls=0, backend='extractive', fault=deepcopy(self.fault))


class Application:
    def __init__(self, directory, concurrency=2, deadline=3, rate=2, burst=4, work_delay=.05):
        if os.name != 'posix':
            raise RuntimeError('posix_process_groups_required')
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.database = self.directory/'orders.sqlite'
        store = Store(self.database)
        store.close()
        self.release = Releases(manifest())
        self.cache = ResponseCache()
        self.bucket = TokenBucket(burst, rate)
        self.breaker = CircuitBreaker()
        self.feedback = Feedback()
        self.slots = threading.BoundedSemaphore(concurrency)
        self.deadline, self.work_delay = deadline, work_delay
        self.jobs, self.metrics, self.threads = {}, [], []
        self.lock = threading.RLock()
        self.fault, self.cohort, self.dropped_metrics = {}, 0, 0
        self.started = time.monotonic()
        self.tokens = {'demo-north':('north','mira'), 'demo-south':('south','leo')}
        self.closing = threading.Event()

    def authenticate(self, authorization):
        identity = self.tokens.get(authorization.removeprefix('Bearer ')) if authorization.startswith('Bearer ') else None
        if identity is None:
            raise PermissionError('unauthenticated')
        return Principal(*identity, expires_at=time.time()+60)

    @staticmethod
    def validate(value):
        if not isinstance(value, dict) or set(value) != {'question','on_date','topic','locale'}:
            raise ValueError('request_shape')
        if not all(isinstance(v,str) for v in value.values()):
            raise ValueError('request_types')
        if not 1 <= len(value['question']) <= 500 or value['locale'] not in {'en','zh-hans'} or value['topic'] not in {'travel','approval','order'}:
            raise ValueError('request_values')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value['on_date']):
            raise ValueError('request_date')
        date.fromisoformat(value['on_date'])
        if value['topic'] == 'order' and not re.fullmatch(r'[AB]-\d{3}',value['question']):
            raise ValueError('order_id')

    def metric(self, arrival, outcome, eligible, duration=0):
        with self.lock:
            self.metrics.append(dict(arrival=arrival, outcome=outcome, eligible=eligible, duration=duration))
            if len(self.metrics) > 1000:
                self.metrics.pop(0)
                self.dropped_metrics += 1

    def submit(self, principal, request):
        self.validate(request)
        subject = (principal.tenant, principal.user)
        allowed, retry = self.bucket.take(subject)
        if not allowed:
            self.metric(time.monotonic(),'rate_limited',True)
            return 429, dict(error='rate_limited', retry_after=retry)
        if not self.slots.acquire(blocking=False):
            self.metric(time.monotonic(),'overloaded',True)
            return 503, dict(error='overloaded', retry_after=1)
        with self.lock:
            # Retain at most 100 completed/pending jobs; never evict running work.
            while len(self.jobs) >= 100:
                old = next((k for k,v in self.jobs.items() if v.done.is_set()),None)
                if old is None:
                    self.slots.release()
                    return 503, dict(error='overloaded',retry_after=1)
                del self.jobs[old]
            selected = self.release.snapshot(self.cohort)
            self.cohort += 1
            job = Job(principal, deepcopy(request), selected, deepcopy(self.fault), self.deadline)
            self.jobs[job.id] = job
            thread = threading.Thread(target=self.run, args=(job,), daemon=True)
            self.threads = [t for t in self.threads if t.is_alive()] + [thread]
            thread.start()
        return 202, dict(request_id=job.id, state='accepted')

    def owned(self, principal, request_id):
        with self.lock:
            job = self.jobs.get(request_id)
        if job is None or (job.principal.tenant,job.principal.user) != (principal.tenant,principal.user):
            raise PermissionError('not_found_or_forbidden')
        return job

    def cancel(self, principal, request_id):
        job = self.owned(principal, request_id)
        with job.lock:
            if job.state in TERMINAL:
                return 409, job.public()
            job.stop.set()
            job.event('cancel_requested')
            # The worker acknowledges only after child cleanup; do not claim it stopped yet.
            job.state = 'cancelling'
            return 202, job.public()

    def check(self, job):
        if job.stop.is_set():
            raise InterruptedError('cancelled')
        if time.monotonic() >= job.deadline:
            raise TimeoutError('deadline')

    def pause(self, job, seconds):
        end = time.monotonic()+seconds
        while time.monotonic() < end:
            self.check(job)
            job.stop.wait(min(.01,max(0,end-time.monotonic())))
        self.check(job)

    def finish(self, job, state, result):
        with job.lock:
            if job.state in TERMINAL:
                return
            if job.stop.is_set():
                state, result = 'cancelled', dict(reason='cancelled')
            job.state, job.result = state, result
            ended = time.monotonic()
            job.event(state)
            job.spans.append(dict(trace_id=job.id, span_id=job.root_span, parent_span_id=None,
                                  name='request', start_ms=0, end_ms=round((ended-job.arrival)*1000,3), status=state))
            self.metric(job.arrival,state,True,ended-job.arrival)

    def compute(self, job):
        process = subprocess.Popen([sys.executable,str(Path(__file__).with_name('service_worker.py'))],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, start_new_session=True)
        first = True
        try:
            while True:
                self.check(job)
                try:
                    output, error = process.communicate(input=encode(dict(request=job.request,release=job.release)) if first else None,
                                                        timeout=.02)
                    break
                except subprocess.TimeoutExpired:
                    first = False
            if process.returncode:
                raise RuntimeError('worker_failed')
            self.check(job)
            return json.loads(output)
        finally:
            if process.poll() is None:
                os.killpg(process.pid,signal.SIGTERM)
                try:
                    process.communicate(timeout=.2)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid,signal.SIGKILL)
                    process.communicate()
                job.event('worker_stopped')

    def run(self, job):
        breaker_held = False
        try:
            self.check(job)
            if not verify_manifest(job.release):
                raise RuntimeError('release_integrity')
            job.event('running')
            self.pause(job,self.work_delay + job.fault.get('delay',0))
            principal = job.principal
            with StoreContext(self.database) as store:
                store.authenticate(principal,'orders:read:own')
                if job.request['topic'] == 'order':
                    value = store.read(principal,job.request['question'])
                    self.finish(job,'answered',dict(kind='order',order=dict(order_id=value['id'],status=value['status'],
                                                                          version=value['version'],source='ka6-orders-v1')))
                    return
            key = self.cache.key(principal,job.request,job.release)
            cached = self.cache.get(key)
            if cached is not None:
                job.event('cache_hit')
                self.finish(job,cached['answer']['status'],cached)
                return
            job.event('cache_miss')
            if not self.breaker.allow():
                job.event('circuit_open')
                self.finish(job,'error',dict(reason='temporarily_unavailable',handoff=True))
                return
            breaker_held = True
            for attempt in range(1,3):
                self.check(job)
                job.event('attempt',number=attempt)
                try:
                    if job.fault.get('unavailable') or (job.fault.get('fail_first') and attempt == 1):
                        raise OSError('injected_dependency_unavailable')
                    value = self.compute(job)
                    break
                except (InterruptedError,TimeoutError):
                    raise
                except OSError:
                    job.event('dependency_failure',attempt=attempt)
                    if attempt == 2:
                        raise RuntimeError('dependency_unavailable')
                    self.pause(job,.05)
            for span in value.pop('stages'):
                job.spans.append(dict(trace_id=job.id,span_id=uuid.uuid4().hex[:16],parent_span_id=job.root_span,
                                      name=span['name'],start_ms=round((span['start']-job.arrival)*1000,3),
                                      end_ms=round((span['end']-job.arrival)*1000,3),status='ok'))
            job.event('source_checked',supported=value['answer']['status']=='answered')
            self.check(job)
            self.breaker.finish(True)
            breaker_held = False
            # Cache and final visibility share the cancellation guard.
            with job.lock:
                self.check(job)
                if value['answer']['status']=='answered':
                    self.cache.put(key,value,job.release['config']['cache_ttl_seconds'],(principal.tenant,principal.user))
                self.finish(job,value['answer']['status'],value)
        except InterruptedError:
            self.finish(job,'cancelled',dict(reason='cancelled'))
        except PermissionError:
            self.finish(job,'refused',dict(reason='not_found_or_forbidden'))
        except TimeoutError:
            self.finish(job,'error',dict(reason='deadline',handoff=True))
        except Exception as error:
            reason = str(error) if str(error) in {'release_integrity','worker_failed','dependency_unavailable'} else 'internal_error'
            self.finish(job,'error',dict(reason=reason,handoff=True))
        finally:
            if breaker_held:
                self.breaker.finish(None if job.state=='cancelled' else False)
            # Diagnostics deliberately omit question, token, result and principal.
            with self.lock:
                diagnostic = self.directory/'diagnostics.jsonl'
                if diagnostic.exists() and diagnostic.stat().st_size > 1_000_000:
                    diagnostic.replace(self.directory/'diagnostics.previous.jsonl')
                with (self.directory/'diagnostics.jsonl').open('a') as stream:
                    stream.write(encode(dict(request_id=job.id,manifest=job.release['digest'],state=job.state,events=job.events,spans=job.spans))+'\n')
            job.done.set()
            self.slots.release()

    def monitor(self):
        with self.lock:
            result = sli(self.metrics,self.started,time.monotonic(),latency_limit=self.deadline)
            result.update(dropped_records=self.dropped_metrics,complete_window=self.dropped_metrics==0,
                          boundary='server-observed terminal status; not browser delivery or factual accuracy')
            return result

    def close(self):
        self.closing.set()
        for job in list(self.jobs.values()):
            if not job.done.is_set():
                job.stop.set()
        for thread in self.threads:
            thread.join(timeout=4)

    def housekeeping(self):
        while not self.closing.wait(1):
            self.cache.expire()
            self.feedback.expire()


class StoreContext:
    def __init__(self,path): self.path=path
    def __enter__(self): self.store=Store(self.path); return self.store
    def __exit__(self,*args): self.store.close()


class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self,*args): pass

    def reply(self,status,value,content_type='application/json',retry=None):
        body = value if isinstance(value,bytes) else encode(value).encode()
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        if retry: self.send_header('Retry-After',str(retry))
        if status==401: self.send_header('WWW-Authenticate','Bearer')
        self.end_headers()
        try: self.wfile.write(body)
        except (BrokenPipeError,ConnectionResetError): pass

    def handle_request(self,method):
        app = self.server.app
        origin = 'http://127.0.0.1:'+str(self.server.server_port)
        if self.headers.get('Host') != origin.removeprefix('http://') or self.headers.get('Origin',origin) != origin:
            return self.reply(403,dict(error='origin_denied'))
        path = urlsplit(self.path).path
        assets = {'/':('index.html','text/html; charset=utf-8'), '/app.js':('app.js','text/javascript; charset=utf-8'),
                  '/style.css':('style.css','text/css; charset=utf-8')}
        if method=='GET' and path in assets:
            name,mime=assets[path]
            body=(UI/name).read_bytes()
            if name=='index.html':
                locale='zh-hans' if parse_qs(urlsplit(self.path).query).get('lang')==['zh-hans'] else 'en'
                content=json.loads((ROOT/'data/knowledge-assistant/service-content-v1.json').read_text())[locale]
                content['locale']=locale
                body=re.sub(r'\{\{([a-z_]+)\}\}',lambda m:escape(content[m[1]]),body.decode()).encode()
            return self.reply(200,body,mime)
        if method=='GET' and path=='/content.json':
            return self.reply(200,(ROOT/'data/knowledge-assistant/service-content-v1.json').read_bytes())
        try:
            principal = app.authenticate(self.headers.get('Authorization',''))
        except PermissionError:
            app.metric(time.monotonic(),'unauthenticated',False)
            return self.reply(401,dict(error='unauthenticated'))
        try:
            value = {}
            if method=='POST':
                if self.headers.get('Transfer-Encoding') or self.headers.get_content_type() != 'application/json':
                    return self.reply(415,dict(error='json_required'))
                length = int(self.headers.get('Content-Length','0'))
                if not 0 < length <= 4096:
                    return self.reply(413,dict(error='body_limit'))
                value = json.loads(self.rfile.read(length),object_pairs_hook=no_duplicates,parse_constant=reject_constant)
            if path=='/api/requests' and method=='POST':
                status,result = app.submit(principal,value)
                return self.reply(status,result,retry=result.get('retry_after'))
            match = re.fullmatch(r'/api/requests/([0-9a-f]{32})(/cancel|/events|/feedback)?',path)
            if match:
                job = app.owned(principal,match[1])
                suffix=match[2]
                if suffix=='/cancel' and method=='POST':
                    if value != {}: raise ValueError('cancel_shape')
                    status,result=app.cancel(principal,job.id)
                    return self.reply(status,result)
                if suffix=='/feedback' and method=='POST':
                    if not isinstance(value,dict) or set(value)!={'category'} or not job.done.is_set():
                        raise ValueError('feedback_shape')
                    row=app.feedback.submit((principal.tenant,principal.user),job.id,value['category'])
                    return self.reply(202,dict(state=row['state']))
                if method=='GET' and suffix=='/events':
                    return self.stream(job)
                if method=='GET' and suffix is None:
                    return self.reply(200,job.public())
            return self.reply(404,dict(error='not_found'))
        except PermissionError:
            return self.reply(404,dict(error='not_found_or_forbidden'))
        except (ValueError,UnicodeDecodeError,TypeError):
            app.metric(time.monotonic(),'invalid_request',False)
            return self.reply(400,dict(error='invalid_request'))

    def stream(self,job):
        try:
            after=int(self.headers.get('Last-Event-ID','0'))
            if after<0: raise ValueError()
        except ValueError:
            return self.reply(400,dict(error='event_id'))
        self.send_response(200)
        self.send_header('Content-Type','text/event-stream; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        try:
            while True:
                with job.lock:
                    events=[dict(e) for e in job.events if e['id']>after]
                    terminal=job.state in TERMINAL
                for event in events:
                    self.wfile.write(f'id: {event["id"]}\ndata: {encode(event)}\n\n'.encode())
                    self.wfile.flush()
                    after=event['id']
                if terminal: return
                job.done.wait(.02)
        except (BrokenPipeError,ConnectionResetError,TimeoutError):
            # A disconnected reader does not cancel work or repeat a request.
            return

    def do_GET(self): self.handle_request('GET')
    def do_POST(self): self.handle_request('POST')


@contextmanager
def server(directory=None,port=0,**options):
    with tempfile.TemporaryDirectory(prefix='ka-service-') as temporary:
        app=Application(directory or temporary,**options)
        httpd=ThreadingHTTPServer(('127.0.0.1',port),Handler)
        httpd.daemon_threads=True
        httpd.app=app
        thread=threading.Thread(target=httpd.serve_forever,daemon=True)
        thread.start()
        maintenance=threading.Thread(target=app.housekeeping,daemon=True)
        maintenance.start()
        try:
            yield app,'http://127.0.0.1:'+str(httpd.server_port)
        finally:
            app.close()
            httpd.shutdown()
            httpd.server_close()
            thread.join()
            maintenance.join()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=0)
    parser.add_argument('--state-dir',default=None)
    args=parser.parse_args()
    with server(args.state_dir,args.port) as (app,url):
        print(json.dumps(dict(url=url,mode='local fictional extractive service',state_dir=str(app.directory))),flush=True)
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt: pass
