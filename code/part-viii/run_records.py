# SPDX-License-Identifier: Apache-2.0
"""Execute fixed Part VIII cases and retain actual observations, not expected output."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/knowledge-assistant'))
from contracts import load
from workflow import run as workflow
from source_skill import load_trace, PACKAGE
from reliable_runtime import Principal, Store, action, retry_schedule
from security_controls import attack_case, delete_subject, governed_input, verify_inventory, expire_records, verify_model_digest
from system_eval import evaluate, judge_report


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def recovery_case(path,fault=None,decision='approved',budget=3,deadline=1001,expiry=1100):
    user=Principal('north','mira',scopes=('orders:read:own','orders:cancel:own'))
    reviewer=Principal('north','reviewer','approver',scopes=('orders:approve',))
    store=Store(path,clock=lambda:1000.0)
    approval=store.approve(reviewer,user,action(),decision=decision,expires=expiry)
    store.start(user,'request-1',action(),approval,'north-intent-1',budget,deadline)
    first=store.advance(user,'request-1',fault=fault)
    effect_first=store.read(user,'A-104')['effects']
    before=store.db.total_changes;replayed=store.replay(user,'request-1');delta=store.db.total_changes-before
    store.close();store=Store(path,clock=lambda:1000.0)
    last=store.advance(user,'request-1') if first['state']=='UNCERTAIN' else store.run_record(user,'request-1')
    result=dict(first=first,after_reopen=last,first_effects=effect_first,final_order=store.read(user,'A-104'),
                replay_mutations=delta,replay=replayed,trace=store.replay(user,'request-1'))
    result['compensation']=store.compensate(user,'request-1');store.close();return result


def run():
    start=time.perf_counter();out=ROOT/'data/part-viii';records={}
    fixed={}
    for locale in ['en','zh-hans']:
        question=load('ka5-content-v1.json')['locales'][locale]['question']
        fixed[locale]={name:workflow(question,locale=locale,choose=lambda _,choice=choice:choice) for name,choice in [('valid','use_evidence'),('decline','abstain'),('invalid','cancel_order')]}
        fixed[locale]['empty']=workflow(question,locale=locale,documents=[],choose=lambda _:'use_evidence')
        fixed[locale]['exhausted']=workflow(question,locale=locale,max_transitions=2,choose=lambda _:'use_evidence')
    records['workflow-run.json']=dict(provenance='Actual host execution with explicitly authored decision adapters; real model runs stored separately.',locales=fixed)
    valid=fixed['en']['valid']
    reviewed=load('../part-viii/reviewed-inventory-v1.json')
    integrity=verify_inventory(ROOT,reviewed['files'])
    if not integrity['accepted']:raise ValueError('reviewed_inventory_mismatch')
    prefix=str(PACKAGE.relative_to(ROOT))+'/'
    expected_hashes={row['path'][len(prefix):]:row['sha256'] for row in reviewed['files'] if row['path'].startswith(prefix)}
    records['skill-run.json']=dict(provenance='Actual local reads and helper subprocess after matching the separately captured package inventory.',
                                  package_version='1.0.0',package_sha256=expected_hashes,
                                  trace=load_trace(dict(context=valid['retrieval']['context'],answer=valid['answer']),expected_hashes))
    with tempfile.TemporaryDirectory(prefix='book-viii-records-') as directory:
        temporary=Path(directory)
        cases={'success':{},'before_commit':dict(fault='before_commit'),'after_commit':dict(fault='after_commit'),
               'denied':dict(decision='denied'),'expired':dict(expiry=999),'budget':dict(budget=0),'deadline':dict(deadline=999)}
        recoveries={name:recovery_case(temporary/(name+'.sqlite'),**kwargs) for name,kwargs in cases.items()}
        unsafe=Store(temporary/'unsafe.sqlite',clock=lambda:1000.0)
        for _ in range(2):
            with unsafe.db:unsafe.db.execute('UPDATE orders SET status=?,effects=effects+1 WHERE tenant=? AND id=?',('cancelled','north','A-104'))
        unsafe_effects=unsafe.read(Principal('north','mira'),'A-104')['effects'];unsafe.close()
        records['recovery-run.json']=dict(provenance='Actual SQLite execution/reopen; fault exceptions deliberately placed; event time 1000 is a fixed logical clock, not measured latency.',cases=recoveries,unsafe_duplicate_effects=unsafe_effects,logical_schedule=retry_schedule(),short_deadline_schedule=retry_schedule(deadline=0.21))
        attacks=[]
        for case in load('../part-viii/attacks-v1.json')['cases']:
            observations={}
            for protected in [False,True]:
                store=Store(temporary/(case['id']+str(protected)+'.sqlite'),clock=lambda:1000.0)
                user=Principal('north','mira',scopes=('orders:read:own','orders:cancel:own'))
                observations['guarded' if protected else 'unsafe']=attack_case(case,store,user,protected)
                store.close()
            attacks.append(dict(case=case,**observations))
        records['attack-run.json']=dict(provenance='Actual local sinks with authored adversarial proposals; isolated fresh database per before/after case; zero external requests.',cases=attacks)
        tamper=[]
        for name,path in [('skill',PACKAGE/'SKILL.md'),('helper',PACKAGE/'scripts/verify.py'),('mcp',ROOT/'code/knowledge-assistant/mcp_readonly.py')]:
            local=temporary/(name+'.txt');local.write_bytes(path.read_bytes())
            inventory=[dict(path=local.name,sha256=digest(local))]
            before=verify_inventory(temporary,inventory)
            local.write_bytes(local.read_bytes()+b'\nUNREVIEWED CHANGE\n')
            after=verify_inventory(temporary,inventory)
            tamper.append(dict(component=name,before=before['accepted'],after=after['accepted'],executed_changed_bytes=False))
        records['supply-chain-run.json']=dict(provenance='Actual hash verification of copied files; changed bytes never executed.',cases=tamper,model_digest_case=dict(expected='458ce03a21878025d072b8740d0e0e3b34abec3585fdadb0b5ab92d1e85dfb61',offered='0'*64,accepted=verify_model_digest('0'*64,'458ce03a21878025d072b8740d0e0e3b34abec3585fdadb0b5ab92d1e85dfb61'),provenance='Authored mismatched manifest digest; no weight corruption performed.'))
    records['system-eval-run.json']=evaluate()
    model=load('../part-viii/model-run.json');human=load('../part-viii/human-judge-run.json');human_cases=load('../part-viii/human-calibration-v1.json')
    records['judge-calibration.json']=judge_report(model,human,human_cases)
    stores={name:[dict(subject='mira',content='fictional'),dict(subject='leo',content='fictional')] for name in ['logs','memory','cache','feedback']}
    records['governance-run.json']=dict(provenance='Actual local projection and deletion over synthetic copies; no real user records.',
        minimized=governed_input(dict(question='Beijing lodging',topic='travel',locale='en',on_date='2026-09-14',credential='DEMO-SECRET-ORCHID',hotel_address='fictional')),
        deletion=delete_subject(stores,'mira'),expiry=expire_records([dict(id='content',created_day=0,retention_days=7),dict(id='audit',created_day=0,retention_days=30)],7),unsafe_group_pairs=[dict(group='amber',amount_yuan=750),dict(group='violet',amount_yuan=600)],group_pairs=[dict(group=group,amount_yuan=workflow(**governed_input(dict(question='Beijing lodging',locale='en',group=group)),choose=lambda _:'use_evidence')['answer']['amount_yuan']) for group in ['amber','violet']],
        correction=dict(current=workflow('Beijing lodging',choose=lambda _:'use_evidence')['answer']['amount_yuan'],historical=workflow('Beijing lodging',on_date='2025-09-14',choose=lambda _:'use_evidence')['answer']['amount_yuan']))
    for name,value in records.items():(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    inputs=sorted([p for p in (ROOT/'code/knowledge-assistant').rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.suffix in {'.py','.md','.json'}]+list((ROOT/'code/part-viii').glob('*.py'))+list((ROOT/'data/knowledge-assistant').glob('ka[456]*.json')))
    inputs += [out/name for name in ['failure-attribution-v1.json','permission-run.json','sandbox-run.json','model-provenance.json','dependency-inventory.json','expected-v1.json','judge-cases-v1.json','attacks-v1.json','human-calibration-v1.json','travel-human-labels-v1.json','reviewed-inventory-v1.json','model-run.json','human-judge-run.json']]
    inputs += list((ROOT/'data/knowledge-assistant').glob('*card-v*.json'))+[ROOT/'data/knowledge-assistant/governance-v1.json',ROOT/'data/knowledge-assistant/risk-register-v3.json']
    manifest=dict(recorded_at=datetime.now(timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),elapsed_seconds=round(time.perf_counter()-start,6),
                  conditions='Fresh Python 3.12 CPU venv with inherited pinned requirements; no network needed by this runner; subprocess source helper; synthetic SQLite only.',
                  inputs_sha256={str(p.relative_to(ROOT)):digest(p) for p in inputs},outputs_sha256={name:digest(out/name) for name in records})
    (out/'run-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(records=len(records),matrix=records['system-eval-run.json']['summaries'],judge=records['judge-calibration.json']['human_calibration']),indent=2))
    return manifest

if __name__=='__main__':run()
