# SPDX-License-Identifier: Apache-2.0
"""KA-6/8 local simulator: durable budgets, approvals, receipts and tenant binding.

Only the host constructs Principal. This is an in-process trust contract, not an
identity provider or a secure execution environment for arbitrary Python.
"""
from dataclasses import dataclass
import hashlib
import json
import sqlite3
import time
from contracts import load, encode


@dataclass(frozen=True)
class Principal:
    tenant: str
    user: str
    role: str = 'reader'
    audience: str = 'orders-local'
    scopes: tuple = ('orders:read:own',)
    expires_at: float = 2000.0


def action(order_id='A-104', version=1):
    return dict(name='cancel_order', arguments=dict(order_id=order_id, expected_version=version))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


class Store:
    def __init__(self, path, clock=time.time):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.clock = clock
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS orders(tenant TEXT, id TEXT, owner TEXT, status TEXT, version INTEGER,
          effects INTEGER DEFAULT 0, PRIMARY KEY(tenant,id));
        CREATE TABLE IF NOT EXISTS approvals(id TEXT PRIMARY KEY, tenant TEXT, user TEXT, action_hash TEXT,
          decision TEXT, expires REAL, reviewer TEXT);
        CREATE TABLE IF NOT EXISTS receipts(tenant TEXT, key TEXT, user TEXT, action_hash TEXT, result TEXT,
          PRIMARY KEY(tenant,key));
        CREATE TABLE IF NOT EXISTS runs(tenant TEXT, id TEXT, user TEXT, action TEXT, approval TEXT, key TEXT,
          state TEXT, remaining INTEGER, attempts INTEGER, deadline REAL, result TEXT, PRIMARY KEY(tenant,id));
        CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY AUTOINCREMENT, tenant TEXT, run_id TEXT,
          at REAL, state TEXT, detail TEXT);
        ''')
        with self.db:
            for row in load('ka6-orders-v1.json')['orders']:
                self.db.execute('INSERT OR IGNORE INTO orders(tenant,id,owner,status,version) VALUES(?,?,?,?,?)',
                                (row['tenant'],row['order_id'],row['owner'],row['status'],row['version']))

    def close(self): self.db.close()

    def authenticate(self, principal, scope):
        if principal.audience != 'orders-local' or principal.expires_at <= self.clock():
            raise PermissionError('credential_invalid')
        if scope not in principal.scopes: raise PermissionError('scope_denied')

    def read(self, principal, order_id):
        self.authenticate(principal, 'orders:read:own')
        row = self.db.execute('SELECT * FROM orders WHERE tenant=? AND id=? AND owner=?',
                              (principal.tenant,order_id,principal.user)).fetchone()
        if not row: raise PermissionError('not_found_or_forbidden')
        return dict(row)

    def approve(self, reviewer, subject, proposal, approval_id='approval-1', decision='approved', expires=1100.0):
        self.authenticate(reviewer, 'orders:approve')
        if reviewer.role != 'approver' or reviewer.tenant != subject.tenant: raise PermissionError('reviewer_denied')
        if decision not in {'approved','denied'}: raise ValueError('invalid_approval')
        self.validate_action(proposal)
        with self.db:
            self.db.execute('INSERT INTO approvals VALUES(?,?,?,?,?,?,?)',
                            (approval_id,subject.tenant,subject.user,fingerprint(proposal),decision,expires,reviewer.user))
        return approval_id

    @staticmethod
    def validate_action(proposal):
        if not isinstance(proposal,dict) or set(proposal) != {'name','arguments'} or proposal['name'] != 'cancel_order':
            raise ValueError('action_allowlist')
        arguments = proposal['arguments']
        if not isinstance(arguments,dict) or set(arguments) != {'order_id','expected_version'}:
            raise ValueError('argument_schema')
        if not isinstance(arguments['order_id'],str) or type(arguments['expected_version']) is not int or arguments['expected_version'] < 1:
            raise ValueError('argument_schema')

    def start(self, principal, run_id, proposal, approval_id, key, budget=3, deadline=1001.0):
        self.authenticate(principal, 'orders:read:own')
        self.validate_action(proposal)
        if not isinstance(key,str) or not key or type(budget) is not int or budget < 0: raise ValueError('invalid_run')
        with self.db:
            self.db.execute('INSERT INTO runs VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                            (principal.tenant,run_id,principal.user,encode(proposal),approval_id,key,'PENDING',budget,0,deadline,None))
            self.event(principal.tenant,run_id,'PENDING',dict(action_hash=fingerprint(proposal),budget=budget))

    def event(self, tenant, run_id, state, detail):
        self.db.execute('INSERT INTO events(tenant,run_id,at,state,detail) VALUES(?,?,?,?,?)',
                        (tenant,run_id,self.clock(),state,encode(detail)))

    def replay(self, principal, run_id):
        self.authenticate(principal,'orders:read:own')
        run = self.db.execute('SELECT user FROM runs WHERE tenant=? AND id=?',(principal.tenant,run_id)).fetchone()
        if not run or run['user'] != principal.user: raise PermissionError('run_forbidden')
        return [dict(sequence=row['sequence'],at=row['at'],state=row['state'],detail=json.loads(row['detail']))
                for row in self.db.execute('SELECT * FROM events WHERE tenant=? AND run_id=? ORDER BY sequence',(principal.tenant,run_id))]

    def cancel(self, principal, proposal, approval_id, key, fault=None):
        self.authenticate(principal, 'orders:read:own')
        self.validate_action(proposal)
        hashed = fingerprint(proposal)
        # Receipt reads need current read permission, but neither a new approval nor a write.
        receipt = self.db.execute('SELECT * FROM receipts WHERE tenant=? AND key=?',(principal.tenant,key)).fetchone()
        if receipt:
            if receipt['user'] != principal.user or receipt['action_hash'] != hashed: raise ValueError('idempotency_conflict')
            return dict(json.loads(receipt['result']), receipt_reused=True)
        self.authenticate(principal, 'orders:cancel:own')
        approval = self.db.execute('SELECT * FROM approvals WHERE id=?',(approval_id,)).fetchone()
        if not approval or approval['tenant'] != principal.tenant or approval['user'] != principal.user or approval['action_hash'] != hashed:
            raise PermissionError('approval_missing_or_mismatch')
        if approval['decision'] != 'approved': raise PermissionError('approval_denied')
        if approval['expires'] <= self.clock(): raise PermissionError('approval_expired')
        order = self.read(principal,proposal['arguments']['order_id'])
        if order['version'] != proposal['arguments']['expected_version']: raise ValueError('version_conflict')
        if order['status'] != 'processing': raise ValueError('not_cancellable')
        if fault == 'before_commit': raise TimeoutError('before_commit')
        result = dict(status='cancelled',order_id=order['id'],version=order['version']+1,receipt_reused=False)
        # This atomic boundary is valid only because both effect and receipt share this database.
        with self.db:
            changed = self.db.execute('UPDATE orders SET status=?,version=version+1,effects=effects+1 WHERE tenant=? AND id=? AND owner=? AND version=? AND status=?',
                                     ('cancelled',principal.tenant,order['id'],principal.user,order['version'],'processing')).rowcount
            if changed != 1: raise ValueError('concurrent_change')
            self.db.execute('INSERT INTO receipts VALUES(?,?,?,?,?)',(principal.tenant,key,principal.user,hashed,encode(result)))
        if fault == 'after_commit': raise TimeoutError('response_lost_after_commit')
        return result

    def advance(self, principal, run_id, fault=None):
        self.authenticate(principal,'orders:read:own')
        row = self.db.execute('SELECT * FROM runs WHERE tenant=? AND id=?',(principal.tenant,run_id)).fetchone()
        if not row or row['user'] != principal.user: raise PermissionError('run_forbidden')
        if row['state'] in {'DONE','DENIED','STOPPED','MANUAL_REVIEW'}: return dict(row)
        reason = 'deadline' if self.clock() >= row['deadline'] else 'call_budget' if row['remaining'] <= 0 else 'attempt_limit' if row['attempts'] >= 2 else None
        if reason:
            with self.db:
                self.db.execute('UPDATE runs SET state=?,result=? WHERE tenant=? AND id=?',('STOPPED',encode(dict(reason=reason)),principal.tenant,run_id))
                self.event(principal.tenant,run_id,'STOPPED',dict(reason=reason))
            return self.run_record(principal,run_id)
        with self.db:
            self.db.execute('UPDATE runs SET remaining=remaining-1,attempts=attempts+1,state=? WHERE tenant=? AND id=?',('CALLING',principal.tenant,run_id))
            self.event(principal.tenant,run_id,'CALLING',dict(attempt=row['attempts']+1,remaining=row['remaining']-1))
        try:
            result = self.cancel(principal,json.loads(row['action']),row['approval'],row['key'],fault)
            state = 'DONE'
        except TimeoutError as error:
            state,result = 'UNCERTAIN',dict(reason=str(error))
        except PermissionError as error:
            state,result = 'DENIED',dict(reason=str(error))
        except ValueError as error:
            state,result = 'MANUAL_REVIEW',dict(reason=str(error))
        with self.db:
            self.db.execute('UPDATE runs SET state=?,result=? WHERE tenant=? AND id=?',(state,encode(result),principal.tenant,run_id))
            self.event(principal.tenant,run_id,state,result)
        return self.run_record(principal,run_id)

    def run_record(self, principal, run_id):
        self.replay(principal,run_id)
        row = dict(self.db.execute('SELECT * FROM runs WHERE tenant=? AND id=?',(principal.tenant,run_id)).fetchone())
        row['result'] = json.loads(row['result']) if row['result'] else None
        return row

    def compensate(self, principal, run_id):
        record = self.run_record(principal,run_id)
        # A cancellation cannot safely be inverted into a fresh booking.
        with self.db:
            self.event(principal.tenant,run_id,'COMPENSATION_REVIEW',dict(reason='no_automatic_inverse',prior_state=record['state']))
        return dict(status='manual_review',business_writes=0,reason='no_automatic_inverse')


def retry_schedule(durations=(0.2,0.1), timeout=0.2, backoff=0.05, deadline=1.0, budget=3):
    """A logical-clock experiment, not measured latency or a thread-cancellation API."""
    elapsed = 0.0
    events = []
    for index,duration in enumerate(durations[:2]):
        if budget <= 0 or elapsed >= deadline: break
        if index:
            if elapsed+backoff >= deadline: break
            elapsed += backoff
        budget -= 1
        allowance = min(timeout,deadline-elapsed)
        elapsed += min(duration,allowance)
        success = duration < allowance
        events.append(dict(attempt=index+1,budget=budget,elapsed_seconds=round(elapsed,6),status='ok' if success else 'timeout'))
        if success: break
    return dict(events=events,remaining=budget,elapsed_seconds=round(elapsed,6))
