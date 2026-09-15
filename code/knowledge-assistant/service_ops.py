# SPDX-License-Identifier: Apache-2.0
"""Small explicit policies for the loopback KA service; no network dependencies."""
from collections import OrderedDict
from copy import deepcopy
import hashlib
import json
import math
import sys
from importlib.metadata import version
from pathlib import Path
import threading
import time

ROOT = Path(__file__).resolve().parents[2]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def manifest(name='rc-a', historical_bug=False, ttl=30):
    paths = sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'code/knowledge-assistant').rglob('*')
                   if p.is_file() and (p.suffix in {'.py', '.js', '.html', '.css'} or 'skills/' in str(p)) and '__pycache__' not in str(p))
    paths += ['code/part-ii/text_processing.py', 'code/part-ii/numerical.py']
    paths += sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'data/knowledge-assistant').glob('*.json'))
    paths += ['data/part-viii/reviewed-inventory-v1.json']
    files = {p: file_digest(p) for p in paths}
    value = dict(name=name, format='ka-release-v1', files=files,
                 runtime=dict(python=sys.version.split()[0],jsonschema=version('jsonschema')),
                 config=dict(on_date_override='2025-09-14' if historical_bug else None, cache_ttl_seconds=ttl),
                 model=dict(kind='extractive', weights=None, neural_tokenizer=None, seed=None, precision='not applicable; lexical ranking uses binary64'),
                 components=dict(code='code/knowledge-assistant/service.py', tokenizer='code/knowledge-assistant/baselines.py',
                                 prompt='data/knowledge-assistant/ka2-content-v1.json', context='data/knowledge-assistant/ka2-context-contract-v1.json',
                                 data='data/knowledge-assistant/ka4-documents-v1.json', index='code/knowledge-assistant/retrieval.py',
                                 schema='data/knowledge-assistant/ka2-answer-schema-v1.json', tool='code/knowledge-assistant/reliable_runtime.py',
                                 mcp='code/knowledge-assistant/mcp_readonly.py', skill='code/knowledge-assistant/skills/source-verification/SKILL.md'),
                 index_recipe=dict(method='BM25', k1=1.2, b=.75, candidate_order=['A','B','C','D','E'], tie_round_digits=12))
    value['digest'] = digest(value)
    return value


def verify_manifest(value):
    body = {k:v for k,v in value.items() if k != 'digest'}
    return value['digest'] == digest(body) and all(file_digest(p) == h for p,h in value['files'].items())


class Releases:
    def __init__(self, initial):
        self.lock = threading.RLock()
        self.active = deepcopy(initial)
        self.canary = None
        self.journal = []

    def snapshot(self, cohort):
        with self.lock:
            value = self.canary if self.canary and cohort % 10 == 0 else self.active
            return deepcopy(value)

    def switch(self, value, gate, canary=False, drill=False):
        if not verify_manifest(value):
            raise ValueError('release_integrity')
        if not drill and (gate.get('manifest') != value['digest'] or not gate.get('passed')):
            raise ValueError('release_gate')
        with self.lock:
            before = self.active['digest']
            if canary:
                self.canary = deepcopy(value)
            else:
                self.active, self.canary = deepcopy(value), None
            self.journal.append(dict(at=time.time(), before=before, after=value['digest'],
                                     action='canary' if canary else 'switch', forced_local_fault_drill=drill))


class ResponseCache:
    def __init__(self, capacity=64, clock=time.monotonic):
        self.rows, self.capacity, self.clock = OrderedDict(), capacity, clock
        self.lock = threading.Lock()

    @staticmethod
    def key(principal, request, release):
        return digest([principal.tenant, principal.user, principal.scopes, request, release['digest']])

    def get(self, key):
        with self.lock:
            row = self.rows.get(key)
            if row is None:
                return None
            if self.clock() >= row['expires']:
                del self.rows[key]
                return None
            self.rows.move_to_end(key)
            return deepcopy(row['value'])

    def put(self, key, value, ttl, subject):
        with self.lock:
            self.rows[key] = dict(value=deepcopy(value), expires=self.clock()+ttl, subject=subject)
            self.rows.move_to_end(key)
            while len(self.rows) > self.capacity:
                self.rows.popitem(last=False)

    def delete_subject(self, subject):
        with self.lock:
            self.rows = OrderedDict((k,v) for k,v in self.rows.items() if v['subject'] != subject)

    def expire(self):
        with self.lock:
            self.rows = OrderedDict((k,v) for k,v in self.rows.items() if self.clock() < v['expires'])


class TokenBucket:
    def __init__(self, capacity=4, rate=2, clock=time.monotonic):
        self.capacity, self.rate, self.clock = capacity, rate, clock
        self.rows, self.lock = {}, threading.Lock()

    def take(self, subject):
        with self.lock:
            now = self.clock()
            amount, then = self.rows.get(subject, (self.capacity, now))
            amount = min(self.capacity, amount + (now-then)*self.rate)
            accepted = amount >= 1
            self.rows[subject] = (amount-1 if accepted else amount, now)
            return accepted, 0 if accepted else math.ceil((1-amount)/self.rate)


class CircuitBreaker:
    """Consecutive failed requests; retry attempts are not separate failures."""
    def __init__(self, threshold=2, cooldown=.25, clock=time.monotonic):
        self.threshold, self.cooldown, self.clock = threshold, cooldown, clock
        self.failures, self.state, self.opened, self.probe = 0, 'closed', 0, False
        self.lock = threading.Lock()

    def allow(self):
        with self.lock:
            if self.state == 'open' and self.clock()-self.opened >= self.cooldown:
                self.state = 'half_open'
            if self.state == 'open' or (self.state == 'half_open' and self.probe):
                return False
            if self.state == 'half_open':
                self.probe = True
            return True

    def finish(self, success):
        with self.lock:
            self.probe = False
            if success is None:
                return
            if success:
                self.failures, self.state = 0, 'closed'
            else:
                self.failures += 1
                if self.state == 'half_open' or self.failures >= self.threshold:
                    self.state, self.opened = 'open', self.clock()


def sli(rows, start, end, target=.95, latency_limit=3):
    selected = [r for r in rows if start <= r['arrival'] < end]
    eligible = [r for r in selected if r['eligible'] and r['outcome'] != 'cancelled']
    good = sum(r['outcome'] in {'answered','abstained','refused'} and r['duration'] <= latency_limit for r in eligible)
    total = len(eligible)
    bad = total-good
    return dict(window=[start,end], total=total, good=good, bad=bad,
                sli=good/total if total else None, target=target, budget=total*(1-target),
                burn=(bad/total)/(1-target) if total else None,
                cancelled=sum(r['outcome']=='cancelled' for r in selected),
                excluded=sum(not r['eligible'] for r in selected),
                alert=total >= 5 and bad/total > 2*(1-target) if total else False)


class Feedback:
    def __init__(self, clock=time.time):
        self.clock, self.rows, self.regressions = clock, [], []
        self.lock = threading.Lock()
        self.serial = 0

    def submit(self, subject, request_id, category):
        if category not in {'wrong_source','missing_answer','hard_to_use'}:
            raise ValueError('feedback_category')
        with self.lock:
            self._expire()
            if len(self.rows) >= 100:
                raise ValueError('feedback_capacity')
            self.serial += 1
            row = dict(id=self.serial, subject=subject, request_id=request_id,
                       category=category, state='quarantined', created=self.clock())
            self.rows.append(row)
            return deepcopy(row)

    def review(self, number, reviewer, case):
        if reviewer != 'maintainer':
            raise PermissionError('reviewer_required')
        if set(case) != {'id','request','expected','source','rationale'} or not case['rationale']:
            raise ValueError('review_contract')
        with self.lock:
            self._expire()
            row = next(r for r in self.rows if r['id'] == number)
            if row['state'] != 'quarantined':
                raise ValueError('already_reviewed')
            row['state'] = 'reviewed'
            self.regressions.append(deepcopy(case))
            return deepcopy(case)

    def _expire(self):
        self.rows[:] = [r for r in self.rows if self.clock() < r['created']+7*86400]

    def expire(self):
        with self.lock:
            self._expire()

    def delete_subject(self, subject):
        with self.lock:
            self.rows[:] = [r for r in self.rows if r['subject'] != subject]
