# SPDX-License-Identifier: Apache-2.0
"""Record executed deterministic mechanisms; authored fixtures remain unchanged."""
import argparse
import copy
import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from core import (ROOT, audit_pair, audit_serialized, dpo, fixture, kl, low_rank,
                  masked_loss, replay_budget, serialize, verify_amount, verify_process)


def run():
    sft = fixture('sft-v1.json')
    serialized = serialize(sft['messages'], sft['vocabulary'])
    audits = []
    for case in sft['invalid_cases']:
        messages = copy.deepcopy(sft['messages'])
        ids, mask = serialized['ids'][:], serialized['mask'][:]
        operation = case['operation']
        if operation == 'replace_user_role':
            messages[1]['role'] = case['value']
        elif operation == 'empty_assistant':
            messages[2]['content'] = []
        elif operation == 'truncate_last':
            ids.pop()
        elif operation == 'shift_mask_right':
            mask = [0] + mask[:-1]
        elif operation == 'insert_control_in_content':
            messages[1]['content'].append('<assistant>')
        else:
            raise ValueError('unknown audit operation')
        try:
            audit_serialized(messages, sft['vocabulary'], ids, mask)
            error = None
        except ValueError as exc:
            error = str(exc)
        if error != case['error']:
            raise AssertionError((case['id'], error))
        audits.append(dict(id=case['id'], error=error))
    prefs = fixture('preferences-v1.json')
    example = prefs['probability_example']
    policy, reference = example['policy'], example['reference']
    preference = dict(audits=[audit_pair(pair) for pair in prefs['pairs']],
                      kl=kl(policy, reference), reverse_kl=kl(reference, policy),
                      dpo=dpo(*policy, *reference))
    reasoning = fixture('reasoning-v1.json')
    judgements = []
    for candidate in reasoning['candidates']:
        response = candidate['response']
        judgements.append(dict(id=candidate['id'], substring='1430' in response,
            exact=response.strip() == '1430',
            rule=verify_amount(reasoning['costs'], reasoning['cap'], response),
            process=verify_process(reasoning['costs'], reasoning['cap'], candidate)))
    matrices = fixture('low-rank-v1.json')
    adapter = low_rank(matrices['W0'], matrices['A'], matrices['B'], matrices['x'], matrices['alpha'])
    quant = matrices['quantization']
    quantized = round(quant['weight'] / quant['grid']) * quant['grid']
    quantization = dict(original=quant['weight'] * quant['input'],
        quantized=quantized * quant['input'],
        original_with_delta=(quant['weight'] + quant['delta']) * quant['input'],
        quantized_with_delta=(quantized + quant['delta']) * quant['input'])
    paths = [*sorted((ROOT / 'data/part-vi').glob('*-v1.json')),
             ROOT / 'data/part-vi/expected.json', Path(__file__), Path(__file__).with_name('core.py')]
    paths = [path for path in paths if path.name != 'mechanism-run-v1.json']
    return dict(version='mechanism-run-v1', recorded_at=datetime.now(timezone.utc).isoformat(),
        evidence_kind='executed CPU controller and arithmetic replay, no model generation or training',
        environment=dict(python=sys.version.split()[0], platform=platform.platform(),
                         processor=platform.machine(), device='cpu', random_seed=None,
                         precision='Python binary64 float; exact integer arithmetic before scale'),
        source_sha256={str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
        sft=dict(**serialized, loss=masked_loss(sft['target_probabilities'], serialized['mask']), audits=audits),
        preference=preference, verifier=judgements, budget=replay_budget(), low_rank=adapter,
        quantization=quantization)


def verify(result):
    expected = fixture('expected.json')
    for field in ('ids', 'inputs', 'targets', 'mask'):
        assert result['sft'][field] == expected['sft'][field]
    assert math.isclose(result['sft']['loss'], expected['sft']['loss'], abs_tol=1e-12)
    assert math.isclose(result['preference']['kl'], expected['preference']['kl'], abs_tol=1e-12)
    assert math.isclose(result['preference']['dpo']['loss'], expected['preference']['dpo_loss'], abs_tol=1e-12)
    budget = fixture('budget-v1.json')
    for method, scores in budget['independent_expected']['primary_correct'].items():
        rows = [row for row in result['budget'] if row['order'] == ['A', 'B', 'C'] and row['method'] == method]
        assert [row['correct'] for row in rows] == scores
        at_four = next(row for row in rows if row['maximum'] == 4)
        for field, value in budget['independent_expected']['budget4'][method].items():
            assert at_four[field] == value
    for field in ('delta', 'base_output', 'adapter_output', 'combined_output'):
        assert result['low_rank'][field] == expected['lora'][field]
    assert result['low_rank']['merged_output'] == result['low_rank']['combined_output']
    for rule, values in fixture('reasoning-v1.json')['expected_acceptance'].items():
        assert [(row[rule]['accepted'] if rule == 'rule' else row[rule]) for row in result['verifier']] == values
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='Replace the mechanism record after deliberate fixture/code changes.')
    args = parser.parse_args()
    result = verify(run())
    if args.write:
        path = ROOT / 'data/part-vi/mechanism-run-v1.json'
        path.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(verified=True, budget_rows=len(result['budget']),
                         invalid_formats=len(result['sft']['audits']), trained_model=False)))

