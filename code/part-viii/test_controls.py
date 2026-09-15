# SPDX-License-Identifier: Apache-2.0
"""Independent behavior checks for KA-5–KA-8, using only fictional data."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/knowledge-assistant'))
from contracts import load
from workflow import run
from source_skill import verify, load_trace, PACKAGE
from reliable_runtime import Principal, Store, action, retry_schedule
from security_controls import dispatch, attack_case, verify_inventory, governed_input, delete_subject, expire_records, verify_model_digest

EXPECTED=load('../part-viii/expected-v1.json')


class Controls(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.path=Path(self.directory.name)/'state.sqlite'
        self.now=1000.0
        self.store=Store(self.path,clock=lambda:self.now)
        self.user=Principal('north','mira',scopes=('orders:read:own','orders:cancel:own'))
        self.reviewer=Principal('north','reviewer','approver',scopes=('orders:approve',))

    def tearDown(self):self.store.close();self.directory.cleanup()

    def approved(self,decision='approved',expires=1100):
        return self.store.approve(self.reviewer,self.user,action(),decision=decision,expires=expires)

    def test_workflow_guards_and_two_locales(self):
        for locale in ['en','zh-hans']:
            question=load('ka5-content-v1.json')['locales'][locale]['question']
            for name,choice in [('valid','use_evidence'),('decline','abstain'),('invalid','cancel_order')]:
                actual=run(question,locale=locale,choose=lambda _:choice)
                self.assertEqual([e['state'] for e in actual['events']],EXPECTED['workflow'][name])
                self.assertEqual(actual['model_calls'],1)
                if name=='valid':self.assertEqual(actual['answer']['amount_yuan'],750)
            empty=run(question,locale=locale,documents=[],choose=lambda _:self.fail('must not call model'))
            self.assertEqual([e['state'] for e in empty['events']],EXPECTED['workflow']['empty'])

    def test_model_call_limit_and_timeout(self):
        result=run('Beijing lodging',max_transitions=2,choose=lambda _:self.fail('budget must stop first'))
        self.assertEqual(result['state'],'STOPPED');self.assertEqual(result['model_calls'],0)
        def timeout(_):raise TimeoutError()
        self.assertEqual(run('Beijing lodging',choose=timeout)['answer']['reason_code'],'decision_timeout')

    def test_source_skill_rejects_old_and_tampered_evidence(self):
        result=run('Beijing lodging',choose=lambda _: 'use_evidence')
        context=result['retrieval']['context'];answer=result['answer']
        self.assertTrue(verify(context,answer)['supported'])
        wrong=deepcopy(answer);wrong['amount_yuan']=600
        self.assertFalse(verify(context,wrong)['supported'])
        self.assertFalse(verify(context,answer,on_date='2025-09-14')['supported'])
        docs=deepcopy(load('ka4-documents-v1.json')['documents']);docs[1]['authority']='unreviewed'
        self.assertFalse(verify(context,answer,documents=docs)['supported'])
        trace=load_trace(dict(context=context,answer=answer))
        self.assertTrue(trace[-1]['report']['supported'])
        self.assertEqual([e['stage'] for e in trace],['discover','activate','reference','execute','report'])

    def test_timeout_after_commit_recovery_and_replay(self):
        approval=self.approved();self.store.start(self.user,'r',action(),approval,'key')
        first=self.store.advance(self.user,'r',fault='after_commit')
        self.assertEqual(first['state'],'UNCERTAIN')
        self.assertEqual(self.store.read(self.user,'A-104')['effects'],1)
        before=self.store.db.total_changes;self.store.replay(self.user,'r')
        self.assertEqual(self.store.db.total_changes,before)
        self.store.close();self.store=Store(self.path,clock=lambda:self.now)
        second=self.store.advance(self.user,'r')
        self.assertTrue(second['result']['receipt_reused'])
        self.assertEqual(second['remaining'],1)
        self.assertEqual(self.store.read(self.user,'A-104')['effects'],1)
        self.assertEqual(self.store.compensate(self.user,'r')['business_writes'],0)

    def test_failure_before_commit_has_no_receipt_and_is_retried(self):
        approval=self.approved();self.store.start(self.user,'r',action(),approval,'key')
        self.store.advance(self.user,'r',fault='before_commit')
        self.assertEqual(self.store.read(self.user,'A-104')['effects'],0)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM receipts').fetchone()[0],0)
        self.assertEqual(self.store.advance(self.user,'r')['state'],'DONE')
        self.assertEqual(self.store.read(self.user,'A-104')['effects'],1)

    def test_approval_denial_expiry_mismatch_and_reviewer(self):
        self.approved(decision='denied')
        with self.assertRaisesRegex(PermissionError,'approval_denied'):self.store.cancel(self.user,action(),'approval-1','key')
        with self.assertRaises(PermissionError):self.store.approve(self.user,self.user,action(),'invalid')
        self.assertEqual(self.store.read(self.user,'A-104')['effects'],0)
        self.store.approve(self.reviewer,self.user,action(),'expired',expires=999)
        with self.assertRaisesRegex(PermissionError,'approval_expired'):self.store.cancel(self.user,action(),'expired','key')
        with self.assertRaisesRegex(PermissionError,'mismatch'):self.store.cancel(self.user,action('A-105'),'approval-1','key')

    def test_duplicate_keys_cannot_change_arguments(self):
        approval=self.approved();self.store.cancel(self.user,action(),approval,'key')
        with self.assertRaisesRegex(ValueError,'idempotency_conflict'):self.store.cancel(self.user,action('A-105'),approval,'key')
        with self.assertRaisesRegex(ValueError,'version_conflict'):self.store.cancel(self.user,action(),approval,'fresh-key')

    def test_persisted_budget_deadline_and_attempt_limit(self):
        approval=self.approved()
        for run_id,budget,deadline,reason in [('zero',0,1001,'call_budget'),('late',3,999,'deadline')]:
            self.store.start(self.user,run_id,action(),approval,run_id,budget,deadline)
            self.assertEqual(self.store.advance(self.user,run_id)['result']['reason'],reason)
        self.store.start(self.user,'two',action(),approval,'two')
        self.store.advance(self.user,'two',fault='before_commit');self.store.advance(self.user,'two',fault='before_commit')
        self.assertEqual(self.store.advance(self.user,'two')['result']['reason'],'attempt_limit')
        self.assertEqual(self.store.read(self.user,'A-104')['effects'],0)
        schedule=retry_schedule()
        self.assertEqual(schedule['remaining'],1);self.assertEqual(schedule['elapsed_seconds'],0.35)
        self.assertEqual(len(retry_schedule(deadline=0.21)['events']),1)

    def test_tenant_scope_and_credentials(self):
        self.assertEqual(self.store.read(self.user,'A-104')['status'],'processing')
        south=Principal('south','leo')
        self.assertEqual(self.store.read(south,'A-104')['status'],'shipped')
        for principal in [replace(self.user,user='leo'),replace(self.user,tenant='south'),replace(self.user,audience='another-service'),replace(self.user,expires_at=999),replace(self.user,scopes=())]:
            with self.assertRaises(PermissionError):self.store.read(principal,'A-104')
        self.assertFalse(dispatch({'name':'get_order','arguments':{'order_id':'A-104','tenant':'south'}},self.store,self.user)['allowed'])
        self.assertFalse(dispatch({'name':'send_http','arguments':{}},self.store,self.user)['allowed'])

    def test_identical_attack_fixtures_before_after(self):
        for case in load('../part-viii/attacks-v1.json')['cases']:
            unsafe=Store(Path(self.directory.name)/(case['id']+'-unsafe.sqlite'),clock=lambda:self.now)
            self.assertTrue(attack_case(case,unsafe,self.user,False)['compromised']);unsafe.close()
            guarded=attack_case(case,self.store,self.user,True)
            self.assertFalse(guarded['compromised']);self.assertEqual(guarded['control'],case['expected_control'])
        self.assertEqual(self.store.read(self.user,'A-104')['effects'],0)

    def test_integrity_catches_bytes_and_symlink(self):
        root=Path(self.directory.name);file=root/'helper.py';file.write_text('pass\n')
        inventory=[dict(path='helper.py',sha256=hashlib.sha256(file.read_bytes()).hexdigest())]
        self.assertTrue(verify_inventory(root,inventory)['accepted'])
        file.write_text('raise RuntimeError()\n');self.assertFalse(verify_inventory(root,inventory)['accepted'])
        file.unlink();file.symlink_to(ROOT/'code/knowledge-assistant/workflow.py')
        self.assertFalse(verify_inventory(root,inventory)['accepted'])

    def test_minimization_deletion_and_group_invariance(self):
        for group in ['amber','violet']:
            record=governed_input(dict(question='Beijing lodging',on_date='2026-09-14',topic='travel',locale='en',group=group,credential='DEMO-SECRET-ORCHID',hotel_address='fictional'))
            self.assertNotIn('credential',record);self.assertNotIn('group',record)
            self.assertEqual(run(**record,choose=lambda _: 'use_evidence')['answer']['amount_yuan'],750)
        stores={name:[dict(subject='mira',content='fictional'),dict(subject='leo',content='fictional')] for name in ['logs','memory','cache','feedback']}
        receipt=delete_subject(stores,'mira')
        self.assertEqual(receipt['after'],dict(logs=1,memory=1,cache=1,feedback=1))
        self.assertNotIn('mira',json.dumps(stores))

    def test_retention_and_model_digest_boundaries(self):
        records=[dict(id='a',created_day=3,retention_days=7)]
        self.assertEqual(expire_records(records,9)['after'],1)
        self.assertEqual(expire_records(records,10)['after'],0)
        expected='458ce03a21878025d072b8740d0e0e3b34abec3585fdadb0b5ab92d1e85dfb61'
        self.assertTrue(verify_model_digest(expected,expected))
        for offered in ['0'*64,expected.upper(),expected[:-1],None]:self.assertFalse(verify_model_digest(offered,expected))

    def test_permission_matrix_retains_legitimate_use(self):
        from permission_records import run as matrix
        rows=matrix()['rows']
        self.assertEqual([row['case'] for row in rows if row['allowed']],['own_read','south_own_read','approved_cancel'])
        for row in rows:self.assertEqual(row['north_effects'],1 if row['case']=='approved_cancel' else 0)

if __name__=='__main__':unittest.main()
