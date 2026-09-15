# SPDX-License-Identifier: Apache-2.0
"""Isolated read-only answer work; parent owns cancellation and final visibility."""
import json
import sys
import time
from contracts import load
from rag import run
from source_skill import load_trace


def compute(request, release):
    on_date = release['config']['on_date_override'] or request['on_date']
    started = time.monotonic()
    trace = run(request['question'], on_date=on_date, topic=request['topic'], locale=request['locale'])
    retrieved = time.monotonic()
    skill = []
    if trace['answer']['status'] == 'answered':
        prefix = 'code/knowledge-assistant/skills/source-verification/'
        inventory = load('../part-viii/reviewed-inventory-v1.json')['files']
        expected = {r['path'][len(prefix):]:r['sha256'] for r in inventory if r['path'].startswith(prefix)}
        skill = load_trace(dict(context=trace['context'], answer=trace['answer'], locale=request['locale'],
                                on_date=on_date, topic=request['topic']), expected_hashes=expected)
        if not skill[-1]['report']['supported']:
            raise ValueError('source_check_failed')
    ended = time.monotonic()
    return dict(answer=trace['answer'], retrieval=trace, skill=skill, effective_date=on_date,
                stages=[dict(name='retrieval_and_composition', start=started, end=retrieved),
                        dict(name='source_skill', start=retrieved, end=ended)])


if __name__ == '__main__':
    payload = json.load(sys.stdin)
    print(json.dumps(compute(payload['request'], payload['release']), ensure_ascii=False))
