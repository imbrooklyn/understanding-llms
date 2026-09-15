# SPDX-License-Identifier: Apache-2.0
"""Loopback-only fictional HTTP fixture; never a production server."""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from read_tools import lookup

PLACEHOLDER = 'demo-placeholder-key'


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, status, value, **headers):
        payload = json.dumps(value, separators=(',', ':')).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        for key, val in headers.items():
            self.send_header(key.replace('_', '-'), val)
        self.end_headers()
        try:
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        if self.headers.get('Authorization') != 'Bearer ' + PLACEHOLDER:
            return self.reply(401, {'error': 'unauthenticated'}, WWW_Authenticate='Bearer')
        if self.path == '/rate-limit':
            return self.reply(429, {'error': 'rate_limited'}, Retry_After='1')
        if self.path == '/slow':
            time.sleep(0.15)
            return self.reply(200, {'status': 'completed_after_delay'})
        if self.path == '/stream':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.end_headers()
            for part in [{'order_id': 'A-104'}, {'status': 'processing'}, {'complete': True}]:
                self.wfile.write(('data: ' + json.dumps(part) + '\n\n').encode())
                self.wfile.flush()
            return
        if not self.path.startswith('/orders/'):
            return self.reply(404, {'error': 'not_found'})
        result = lookup(self.path.removeprefix('/orders/'), 'mira')
        status = {'forbidden': 403, 'not_found': 404}.get(result.get('error'), 200)
        self.reply(status, result)

    def do_POST(self):
        self.reply(405, {'error': 'method_not_allowed'}, Allow='GET')


@contextmanager
def server():
    service = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=service.serve_forever, daemon=True)
    thread.start()
    try:
        yield 'http://127.0.0.1:' + str(service.server_address[1])
    finally:
        service.shutdown()
        service.server_close()
        thread.join()


def get(base, path, key=PLACEHOLDER, timeout=0.2):
    req = Request(base + path, headers={'Authorization': 'Bearer ' + key})
    try:
        response = urlopen(req, timeout=timeout)
    except HTTPError as error:
        response = error
    with response:
        body = response.read().decode('utf-8')
        content = body if response.headers.get_content_type() == 'text/event-stream' else json.loads(body)
        return response.status, content, response.headers.get('Retry-After')


def demo():
    rows = []
    with server() as base:
        for path, key in [('/orders/A-104', PLACEHOLDER), ('/orders/A-104', 'invalid-placeholder'), ('/orders/B-205', PLACEHOLDER), ('/orders/A-999', PLACEHOLDER), ('/rate-limit', PLACEHOLDER), ('/stream', PLACEHOLDER)]:
            status, body, retry_after = get(base, path, key)
            rows.append(dict(path=path, credential='redacted', status=status, body=body, retry_after=retry_after))
        try:
            urlopen(Request(base + '/orders/A-104', method='POST'), timeout=0.2)
        except HTTPError as error:
            with error:
                rows.append(dict(path='/orders/A-104', method='POST', status=error.code, body=json.loads(error.read())))
        try:
            get(base, '/slow', timeout=0.02)
        except TimeoutError:
            rows.append(dict(path='/slow', status='client_timeout', timeout_seconds=0.02, server_delay_seconds=0.15, completion='not_proven_by_timeout'))
    return dict(transport='actual loopback HTTP on OS-assigned port', records=rows)


if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
