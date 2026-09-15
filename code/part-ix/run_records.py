# SPDX-License-Identifier: Apache-2.0
"""Actual local service experiments; never publish/deploy or modify inherited runs."""
from datetime import datetime,timezone
from importlib import util
from importlib.metadata import distributions
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
from support import ROOT,EXPECTED,QUERY,http,submit,release_gate
from service import server
from service_ops import manifest,file_digest,TokenBucket,CircuitBreaker,ResponseCache,Feedback,sli
from reliable_runtime import Principal,Store
from security_controls import attack_case,verify_inventory
from contracts import load
from baselines import load_fixture,run_locale
from mcp_readonly import demo as mcp_demo
from system_eval import evaluate

OUT=ROOT/'data/part-ix'


def imported(name,path):
    spec=util.spec_from_file_location(name,path)
    module=util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def run():
    started=time.perf_counter();OUT.mkdir(exist_ok=True)
    integrity=verify_inventory(ROOT,load('../part-viii/reviewed-inventory-v1.json')['files'])
    if not integrity['accepted']:raise ValueError('inherited_integrity')
    records={}
    with server(rate=100,burst=100) as (app,base):
        traces=[];exchanges=[]
        for label,query in [('current',QUERY),('current_zh',{**QUERY,'locale':'zh-hans','question':EXPECTED['release_cases'][0]['question']['zh-hans']}),
                            ('historical',{**QUERY,'on_date':'2025-12-31'}),('absent',{**QUERY,'question':'volcano'}),
                            ('synonym',{**QUERY,'question':'overnight accommodation ceiling'}),('own_order',{**QUERY,'topic':'order','question':'A-104'}),
                            ('forbidden_order',{**QUERY,'topic':'order','question':'B-205'}),('cached',QUERY)]:
            job=submit(app,base,query)
            traces.append(dict(label=label,trace=job.trace()))
            exchanges.append(dict(label=label,method='POST',path='/api/requests',request=query,accepted_status=202,
                                  result=http(base,f'/api/requests/{job.id}')))
        job=submit(app,base,{**QUERY,'question':'Beijing lodging policy'},wait=False)
        limit=time.monotonic()+2
        while not any(e['stage']=='attempt' for e in job.events) and time.monotonic()<limit:time.sleep(.001)
        cancel=http(base,f'/api/requests/{job.id}/cancel',{})
        if not job.done.wait(3):raise AssertionError('cancel_not_acknowledged')
        traces.append(dict(label='cancelled',trace=job.trace()))
        exchanges.append(dict(label='cancelled',method='POST',path=f'/api/requests/{job.id}/cancel',response=cancel))
        status,stream=http(base,f'/api/requests/{traces[0]["trace"]["trace_id"]}/events')
        exchanges += [dict(label='stream',status=status,body=stream),dict(label='invalid_credential',response=http(base,'/api/requests',QUERY,key='invalid-placeholder')),
                      dict(label='cross_tenant_request',response=http(base,f'/api/requests/{job.id}',key='demo-south'))]
        records['service-run.json']=dict(transport='actual loopback HTTP; OS-assigned port',base_url=base,
            assigned_work_delay_seconds=.05,traces=traces,exchanges=exchanges,monitor=app.monitor())
    a,b,bad=manifest(),manifest('rc-b',ttl=10),manifest('rc-stale',historical_bug=True)
    gates={r['name']:release_gate(r) for r in [a,b,bad]}
    with server(rate=100,burst=100) as (app,base):
        rejection=None
        try:app.release.switch(bad,gates['rc-stale'])
        except ValueError as error:rejection=str(error)
        app.release.switch(b,gates['rc-b'],canary=True)
        cohort=[]
        for i in range(10):
            job=submit(app,base);cohort.append(dict(number=i,release=job.release['name'],state=job.state,amount=job.result['answer']['amount_yuan']))
        app.release.switch(b,gates['rc-b'])
        # Force a bad configuration only inside this explicitly labeled local drill.
        app.release.switch(bad,gates['rc-stale'],drill=True)
        failed=submit(app,base)
        app.fault={'delay':.15};inflight=submit(app,base,wait=False)
        app.release.switch(a,gates['rc-a'])
        app.fault={};recovered=submit(app,base)
        if not inflight.done.wait(3):raise AssertionError('inflight_not_finished')
        before=failed.trace();replayed=failed.trace()
        recomputed=submit(app,base)
        records['release-run.json']=dict(gates=gates,rejected_candidate_reason=rejection,cohort=cohort,
            failed=failed.trace(),rollback=recovered.trace(),inflight=inflight.trace(),journal=app.release.journal,
            replay=dict(kind='read stored record',same=before==replayed,new_model_calls=0,new_order_effects=0),
            recomputation=dict(kind='new read-only request under restored version',trace=recomputed.trace()),
            release_scope='configuration-only local rollout; unchanged executable code; no public deployment')
    with server(rate=100,burst=100) as (app,base):
        faults=[]
        app.fault={'fail_first':True};job=submit(app,base);faults.append(dict(label='retry_recovers',trace=job.trace()))
        app.cache.rows.clear();app.fault={'unavailable':True}
        for label in ['failure_one','failure_two','open_reject']:
            job=submit(app,base);faults.append(dict(label=label,trace=job.trace(),breaker=app.breaker.state))
        app.fault={};time.sleep(.26)
        job=submit(app,base);faults.append(dict(label='probe_recovers',trace=job.trace(),breaker=app.breaker.state))
        monitor=app.monitor()
        records['resilience-run.json']=dict(provenance='Actual HTTP jobs; dependency exceptions and 0.05-second backoff explicitly injected; actual monotonic timestamps.',traces=faults,monitor=monitor)
    with server(deadline=.1) as (app,base):
        app.fault={'delay':.2};job=submit(app,base)
        records['resilience-run.json']['deadline']=job.trace()
    with server(concurrency=1,rate=100,burst=100) as (app,base):
        app.fault={'delay':.2};job=submit(app,base,wait=False)
        records['resilience-run.json']['overload']=http(base,'/api/requests',QUERY)
        job.done.wait(3)
    with server(burst=1,rate=.001) as (app,base):
        submit(app,base);records['resilience-run.json']['rate_limit']=http(base,'/api/requests',QUERY)
    now=[0.0];bucket=TokenBucket(2,1,lambda:now[0]);buckets=[]
    for t in EXPECTED['bucket']['times']:
        now[0]=t;allowed,retry=bucket.take('north');buckets.append(dict(time=t,allowed=allowed,remaining=bucket.rows['north'][0],retry_after=retry))
    breaker=CircuitBreaker(2,5,lambda:now[0]);breakers=[]
    for t,result in zip(EXPECTED['breaker']['times'],EXPECTED['breaker']['results']):
        now[0]=t;allowed=breaker.allow()
        if allowed:breaker.finish(result)
        breakers.append(dict(time=t,allowed=allowed,result=result,state=breaker.state))
    rows=[dict(arrival=i,outcome='answered' if i<18 else 'error',eligible=True,duration=.2) for i in range(20)]
    rows += [dict(arrival=20,outcome='cancelled',eligible=True,duration=.1),dict(arrival=21,outcome='unauthenticated',eligible=False,duration=0)]
    records['policy-run.json']=dict(provenance='Actual calculation on authored logical clocks and outcomes; not measured traffic or model accuracy.',
        bucket=buckets,breaker=breakers,slo_rows=rows,slo=sli(rows,0,60),
        semantic_similarity=.99/math.sqrt(.99**2+.01**2),semantic_cache_enabled=False)
    feedback=Feedback(lambda:1000);report=feedback.submit(('north','mira'),'synthetic-request','missing_answer')
    before=list(feedback.regressions)
    case=dict(id='reviewed-current-boundary',request={**QUERY,'on_date':'2026-01-01'},expected=750,source='travel-v2:1-3',rationale='Author reviewed the inclusive start date; feedback category alone supplies no label.')
    reviewed=feedback.review(report['id'],'maintainer',case)
    after=list(feedback.regressions);feedback.delete_subject(('north','mira'))
    records['feedback-run.json']=dict(provenance='Actual local quarantine, explicit author review, synthetic regression proposal and subject deletion; no training or automatic release.',
        submitted=report,regressions_before=before,reviewed=reviewed,regressions_after=after,retained_reports_after_deletion=feedback.rows,
        regression_result=compute_for_feedback(case,a))
    prior=imported('part_viii_records',ROOT/'code/part-viii/run_records.py')
    permission=imported('part_viii_permissions',ROOT/'code/part-viii/permission_records.py')
    with tempfile.TemporaryDirectory(prefix='ka-capstone-') as directory:
        attacks=[]
        for case in load('../part-viii/attacks-v1.json')['cases']:
            result={}
            for protected in [False,True]:
                store=Store(Path(directory)/(case['id']+str(protected)+'.sqlite'),clock=lambda:1000)
                result['guarded' if protected else 'unsafe']=attack_case(case,store,Principal('north','mira',scopes=('orders:read:own','orders:cancel:own')),protected);store.close()
            attacks.append(dict(case=case,**result))
        records['capstone-run.json']=dict(provenance='Fresh deterministic CPU component runs alongside actual service records; inherited neural-model evidence is referenced, not rerun.',
            lexical={locale:run_locale(load_fixture(),locale) for locale in ['en','zh-hans']},mcp=mcp_demo(),permissions=permission.run(),
            recovery=prior.recovery_case(Path(directory)/'recovery.sqlite',fault='after_commit'),attacks=attacks,layers=evaluate(),
            historical_model_evidence={p:file_digest(p) for p in ['data/knowledge-assistant/ka1-run-v1.json','data/knowledge-assistant/ka1-format-run-v1.json','data/part-viii/model-run.json','data/part-viii/judge-calibration.json']})
    for release in [a,b,bad]:records[release['name']+'.json']=release
    for name,value in records.items():
        (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    inputs={p:file_digest(p) for p in a['files']}
    for path in sorted((ROOT/'code/part-ix').glob('*.py')):inputs[str(path.relative_to(ROOT))]=file_digest(str(path.relative_to(ROOT)))
    inputs['data/part-ix/expected-v1.json']=file_digest('data/part-ix/expected-v1.json')
    evidence=dict(recorded_at=datetime.now(timezone.utc).isoformat(),command='python code/part-ix/run_records.py',python=sys.version,
                 platform=platform.platform(),cpu_only=True,elapsed_seconds=time.perf_counter()-started,inputs_sha256=inputs,
                 outputs_sha256={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in records})
    (OUT/'run-manifest.json').write_text(json.dumps(evidence,indent=2)+'\n')
    dependencies=sorted([dict(name=d.metadata['Name'],version=d.version,license=d.metadata.get('License-Expression') or d.metadata.get('License','unspecified')) for d in distributions()],key=lambda r:r['name'].lower())
    (OUT/'dependency-inventory.json').write_text(json.dumps(dict(python=sys.version,platform=platform.platform(),packages=dependencies),indent=2)+'\n')
    print(json.dumps(dict(outputs=len(records),gates={k:v['passed_cases'] for k,v in gates.items()},service=[(r['label'],r['trace']['state']) for r in records['service-run.json']['traces']],seconds=round(time.perf_counter()-started,3)),indent=2))


def compute_for_feedback(case,release):
    from service_worker import compute
    actual=compute(case['request'],release)['answer']['amount_yuan']
    return dict(actual=actual,expected=case['expected'],passed=actual==case['expected'])


if __name__=='__main__':run()
