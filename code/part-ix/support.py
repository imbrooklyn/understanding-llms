# SPDX-License-Identifier: Apache-2.0
"""Shared experiment clients and an independently specified local release gate."""
import json
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code/knowledge-assistant'))
from service_worker import compute

EXPECTED = json.loads((ROOT / 'data/part-ix/expected-v1.json').read_text())
QUERY = dict(question='Beijing lodging', on_date='2026-09-14', topic='travel', locale='en')


def http(base,path,body=None,key='demo-north',extra=None):
    headers={'Authorization':'Bearer '+key,'Content-Type':'application/json',**(extra or {})}
    data=None if body is None else json.dumps(body).encode()
    try: response=urlopen(Request(base+path,data=data,headers=headers),timeout=5)
    except HTTPError as error: response=error
    with response:
        raw=response.read().decode()
        value=raw if response.headers.get_content_type()=='text/event-stream' or response.headers.get_content_type()=='text/html' else json.loads(raw)
        return response.status,value


def submit(app,base,query=None,key='demo-north',wait=True):
    status,value=http(base,'/api/requests',query or QUERY,key)
    if status!=202: raise AssertionError((status,value))
    job=app.jobs[value['request_id']]
    if wait and not job.done.wait(5): raise AssertionError('request_did_not_stop')
    return job


def release_gate(release):
    rows=[]
    for locale in ['en','zh-hans']:
        for case in EXPECTED['release_cases']:
            request=dict(question=case['question'][locale],locale=locale,on_date=case['on_date'],topic=case['topic'])
            result=compute(request,release)['answer']
            actual=dict(status=result['status'],amount_yuan=result['amount_yuan'],source=result['citations'][0]['source_id'] if result['citations'] else None)
            rows.append(dict(case=case['id'],locale=locale,request=request,expected=case['expected'],actual=actual,passed=actual==case['expected']))
    return dict(manifest=release['digest'],passed=all(r['passed'] for r in rows),passed_cases=sum(r['passed'] for r in rows),total=len(rows),rows=rows)

