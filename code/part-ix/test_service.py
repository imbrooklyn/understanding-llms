# SPDX-License-Identifier: Apache-2.0
"""Observable service contracts; independent fixtures precede these tests."""
from copy import deepcopy
import json
import math
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/knowledge-assistant'))
from service import server, Application
from service_ops import ResponseCache,TokenBucket,CircuitBreaker,Feedback,manifest,Releases,sli
from reliable_runtime import Principal
from baselines import run_locale,load_fixture
from service_worker import compute

from support import EXPECTED, QUERY, http, submit, release_gate




class NumericPolicies(unittest.TestCase):
    def test_deadline_and_semantic_false_match(self):
        e=EXPECTED['deadline']
        self.assertEqual(e['budget_ms']-sum(e[k] for k in ['queue_ms','retrieval_ms','attempt_ms','backoff_ms']),e['remaining_ms'])
        # Independent geometry: projecting [0.99,0.01] on [1,0].
        similarity=.99/math.sqrt(.99**2+.01**2)
        self.assertGreater(similarity,EXPECTED['semantic']['threshold'])
        self.assertNotEqual(600,750)

    def test_cache_expiry_scope_version_and_copy(self):
        now=[10.0];cache=ResponseCache(capacity=2,clock=lambda:now[0]);p=Principal('north','mira')
        a=manifest();key=cache.key(p,QUERY,a);cache.put(key,{'amount':750},30,('north','mira'))
        for t,hit in zip(EXPECTED['cache']['lookup_times'],EXPECTED['cache']['hits']):
            now[0]=t;self.assertEqual(cache.get(key) is not None,hit)
        keys=[key,cache.key(Principal('south','leo'),QUERY,a),cache.key(p,{**QUERY,'on_date':'2025-09-14'},a),cache.key(p,QUERY,manifest('rc-b',ttl=10))]
        self.assertEqual(len(set(keys)),4)
        cache.put(key,{'amount':750},30,('north','mira'));cache.get(key)['amount']=600
        self.assertEqual(cache.get(key)['amount'],750)
        cache.delete_subject(('north','mira'));self.assertIsNone(cache.get(key))

    def test_bucket_and_breaker_boundary_and_single_probe(self):
        now=[0];bucket=TokenBucket(2,1,lambda:now[0]);actual=[]
        for t in EXPECTED['bucket']['times']:
            now[0]=t;actual.append(bucket.take('north')[0])
        self.assertEqual(actual,EXPECTED['bucket']['allowed'])
        now[0]=0;breaker=CircuitBreaker(2,5,lambda:now[0]);allowed=[];states=[]
        for t,result in zip(EXPECTED['breaker']['times'],EXPECTED['breaker']['results']):
            now[0]=t;ok=breaker.allow();allowed.append(ok)
            if ok:
                if breaker.state=='half_open':self.assertFalse(breaker.allow())
                breaker.finish(result)
            states.append(breaker.state)
        self.assertEqual(allowed,EXPECTED['breaker']['allowed']);self.assertEqual(states,EXPECTED['breaker']['states'])

    def test_slo_eligibility_window_and_empty(self):
        rows=[dict(arrival=i,outcome='answered' if i<18 else 'error',eligible=True,duration=.2) for i in range(20)]
        rows += [dict(arrival=20,outcome='cancelled',eligible=True,duration=.1),dict(arrival=21,outcome='unauthenticated',eligible=False,duration=0),dict(arrival=60,outcome='error',eligible=True,duration=0)]
        report=sli(rows,0,60)
        for key in ['total','good','bad','sli','budget','burn']:self.assertAlmostEqual(report[key],EXPECTED['slo'][key])
        self.assertEqual(report['cancelled'],1);self.assertEqual(report['excluded'],1)
        self.assertIsNone(sli([],0,60)['sli'])

    def test_feedback_requires_review_and_expires_without_training(self):
        now=[0];feedback=Feedback(lambda:now[0]);row=feedback.submit(('north','mira'),'r','missing_answer')
        case=dict(id='reviewed-1',request=QUERY,expected=750,source='travel-v2:1-3',rationale='Checked the fictional source interval.')
        with self.assertRaises(PermissionError):feedback.review(row['id'],'user',case)
        self.assertEqual(feedback.regressions,[])
        feedback.review(row['id'],'maintainer',case)
        self.assertEqual(len(feedback.regressions),1)
        feedback.delete_subject(('north','mira'));self.assertEqual(feedback.rows,[])
        other=feedback.submit(('south','leo'),'s','hard_to_use');self.assertNotEqual(row['id'],other['id'])
        now[0]=7*86400;feedback._expire();self.assertEqual(feedback.rows,[])
        with self.assertRaises(ValueError):feedback.submit(('north','mira'),'r','arbitrary free text')

    def test_release_gate_and_inflight_snapshot(self):
        a,b,bad=manifest(),manifest('rc-b',ttl=10),manifest('rc-stale',historical_bug=True)
        gates=[release_gate(r) for r in [a,b,bad]]
        self.assertEqual([g['passed_cases'] for g in gates],[10,10,4])
        releases=Releases(a);before=releases.snapshot(0)
        with self.assertRaises(ValueError):releases.switch(bad,gates[2])
        releases.switch(b,gates[1],canary=True)
        self.assertEqual(sum(releases.snapshot(i)['name']=='rc-b' for i in range(10)),1)
        releases.switch(b,gates[1]);self.assertEqual(before['name'],'rc-a')
        self.assertEqual(releases.snapshot(1)['name'],'rc-b')
        with self.assertRaises(ValueError):releases.switch(b,gates[0])

    def test_retained_lexical_baseline_same_set(self):
        fixture=load_fixture()
        for locale in ['en','zh-hans']:
            self.assertEqual(run_locale(fixture,locale)['success_counts'],EXPECTED['inherited_lexical_counts'])


class HTTPBehavior(unittest.TestCase):
    def test_real_success_stream_resume_and_ownership(self):
        with server(rate=100,burst=50) as (app,base):
            job=submit(app,base)
            self.assertEqual(job.state,'answered');self.assertEqual(job.result['answer']['amount_yuan'],750)
            status,stream=http(base,f'/api/requests/{job.id}/events')
            self.assertEqual(status,200);self.assertIn('"stage":"answered"',stream)
            status,resumed=http(base,f'/api/requests/{job.id}/events',extra={'Last-Event-ID':'4'})
            self.assertNotIn('id: 1\n',resumed);self.assertIn('id: 5\n',resumed)
            self.assertEqual(http(base,f'/api/requests/{job.id}',key='demo-south')[0],404)
            self.assertEqual(http(base,'/api/requests',QUERY,key='bad')[0],401)
            self.assertEqual(http(base,'/api/requests',{**QUERY,'tenant':'south'})[0],400)
            self.assertEqual(http(base,'/api/requests',QUERY,extra={'Origin':'https://untrusted.example'})[0],403)
            self.assertEqual(http(base,f'/api/requests/{job.id}/cancel',{})[0],409)
            again=submit(app,base);self.assertIn('cache_hit',[e['stage'] for e in again.events])

    def test_cancel_running_process_no_late_answer_or_cache(self):
        with server(rate=100,burst=50) as (app,base):
            job=submit(app,base,wait=False)
            # Cancel after the subprocess starts, then inspect the stable terminal result.
            deadline=time.monotonic()+2
            while not any(e['stage']=='attempt' for e in job.events) and time.monotonic()<deadline:time.sleep(.001)
            self.assertEqual(http(base,f'/api/requests/{job.id}/cancel',{})[0],202)
            self.assertTrue(job.done.wait(3));self.assertEqual(job.state,'cancelled')
            time.sleep(.05);self.assertEqual(job.state,'cancelled');self.assertEqual(len(app.cache.rows),0)
            self.assertNotIn('answered',[e['stage'] for e in job.events])
            self.assertIn('worker_stopped',[e['stage'] for e in job.events])
            self.assertNotIn('dependency_failure',[e['stage'] for e in job.events])

    def test_deadline_retry_breaker_fallback_and_recovery(self):
        with server(rate=100,burst=50) as (app,base):
            app.fault={'fail_first':True};first=submit(app,base)
            self.assertEqual(first.state,'answered');self.assertEqual(sum(e['stage']=='attempt' for e in first.events),2)
            app.cache.rows.clear();app.fault={'unavailable':True}
            one,two=submit(app,base),submit(app,base)
            self.assertEqual([one.state,two.state],['error','error']);self.assertEqual(app.breaker.state,'open')
            blocked=submit(app,base);self.assertIn('circuit_open',[e['stage'] for e in blocked.events])
            self.assertFalse(any(e['stage']=='attempt' for e in blocked.events))
            app.fault={};time.sleep(.26)
            recovered=submit(app,base);self.assertEqual(recovered.state,'answered');self.assertEqual(app.breaker.state,'closed')
        with server(deadline=.1) as (app,base):
            app.fault={'delay':.2};job=submit(app,base)
            self.assertEqual(job.state,'error');self.assertEqual(job.result['reason'],'deadline')

    def test_concurrency_admission_rate_limit_and_order_isolation(self):
        with server(concurrency=1,rate=100,burst=50) as (app,base):
            app.fault={'delay':.3};job=submit(app,base,wait=False)
            self.assertEqual(http(base,'/api/requests',QUERY)[0],503)
            self.assertTrue(job.done.wait(3));app.fault={}
            north=submit(app,base,{**QUERY,'topic':'order','question':'A-104'})
            south=submit(app,base,{**QUERY,'topic':'order','question':'A-104'},key='demo-south')
            self.assertEqual(north.result['order']['status'],'processing');self.assertEqual(south.result['order']['status'],'shipped')
            self.assertEqual(north.result['order']['order_id'],'A-104')
            denied=submit(app,base,{**QUERY,'topic':'order','question':'A-105'},key='demo-south')
            self.assertEqual(denied.state,'refused')
            self.assertEqual(http(base,'/api/orders/A-104/cancel',{})[0],404)
        with server(burst=1,rate=.001) as (app,base):
            submit(app,base);self.assertEqual(http(base,'/api/requests',QUERY)[0],429)

    def test_feedback_route_minimization_and_static_ui_labels(self):
        with tempfile.TemporaryDirectory() as directory,server(directory,rate=100,burst=50) as (app,base):
            job=submit(app,base)
            self.assertEqual(http(base,f'/api/requests/{job.id}/feedback',{'category':'wrong_source'})[0],202)
            self.assertEqual(http(base,f'/api/requests/{job.id}/feedback',{'category':'wrong_source','text':'secret'})[0],400)
            log=(Path(directory)/'diagnostics.jsonl').read_text()
            self.assertNotIn('demo-north',log);self.assertNotIn('Beijing lodging',log)
            self.assertNotIn('question',app.feedback.rows[0])
            for lang in ['en','zh-hans']:
                status,page=http(base,'/?lang='+lang)
                self.assertEqual(status,200);self.assertNotIn('{{',page);self.assertIn('role="status"',page)


if __name__=='__main__':unittest.main()
