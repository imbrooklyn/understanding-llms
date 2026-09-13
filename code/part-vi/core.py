# SPDX-License-Identifier: Apache-2.0
"""Small, inspectable mechanisms; no language model is trained by this module."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fixture(name):
    return json.loads((ROOT / 'data/part-vi' / name).read_text(encoding='utf-8'))


def serialize(messages, vocabulary):
    if [message['role'] for message in messages] != ['system', 'user', 'assistant']:
        raise ValueError('unsupported role sequence')
    ids = [vocabulary.index('<bos>')]
    scored = [0]
    controls = {token for token in vocabulary if token.startswith('<')}
    for message in messages:
        content = message['content']
        if not content:
            raise ValueError('empty message')
        if any(token in controls for token in content):
            raise ValueError('control token in content')
        ids.append(vocabulary.index('<' + message['role'] + '>'))
        scored.append(0)
        ids.extend(vocabulary.index(token) for token in content)
        ids.append(vocabulary.index('<eot>'))
        scored.extend([int(message['role'] == 'assistant')] * (len(content) + 1))
    return dict(ids=ids, inputs=ids[:-1], targets=ids[1:], mask=scored[1:])


def audit_serialized(messages, vocabulary, ids, mask):
    expected = serialize(messages, vocabulary)
    if ids != expected['ids']:
        raise ValueError('serialized sequence mismatch')
    if mask != expected['mask']:
        raise ValueError('shifted target mask mismatch')
    return len(ids), len(mask), sum(mask)


def masked_loss(probabilities, mask):
    if len(probabilities) != len(mask) or any(bit not in (0, 1) for bit in mask):
        raise ValueError('invalid loss mask')
    selected = [probability for probability, bit in zip(probabilities, mask) if bit]
    if not selected:
        raise ValueError('no scored targets')
    if any(p is None or not math.isfinite(p) or not 0 < p <= 1 for p in selected):
        raise ValueError('invalid target probability')
    return math.fsum(-math.log(p) for p in selected) / len(selected)


def distribution(values):
    if not values or any(not math.isfinite(p) or p < 0 for p in values) or not math.isclose(sum(values), 1, abs_tol=1e-12):
        raise ValueError('invalid distribution')


def kl(policy, reference):
    distribution(policy)
    distribution(reference)
    if len(policy) != len(reference):
        raise ValueError('different supports')
    if any(p > 0 and q == 0 for p, q in zip(policy, reference)):
        return math.inf
    return math.fsum(p * math.log(p / q) for p, q in zip(policy, reference) if p > 0)


def dpo(chosen, rejected, reference_chosen, reference_rejected, beta=1):
    if not math.isfinite(beta) or beta <= 0:
        raise ValueError('beta must be positive')
    if any(not math.isfinite(p) or not 0 < p <= 1 for p in (chosen, rejected, reference_chosen, reference_rejected)):
        raise ValueError('positive response probabilities required')
    margin = beta * (math.log(chosen / reference_chosen) - math.log(rejected / reference_rejected))
    loss = max(0, -margin) + math.log1p(math.exp(-abs(margin)))
    return dict(margin=margin, probability=math.exp(-loss), loss=loss)


def audit_pair(pair):
    target = pair['evidence'].get(pair['scope'])
    if target is None:
        return 'quarantine'
    chosen = pair['chosen']['amount'] == target
    rejected = pair['rejected']['amount'] == target
    if chosen and rejected:
        return 'tie'
    if chosen:
        return 'keep'
    if rejected:
        return 'reverse'
    return 'quarantine'


def reimburse(costs, cap):
    if not costs or not isinstance(cap, int) or isinstance(cap, bool) or cap < 0:
        raise ValueError('invalid reimbursement input')
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in costs):
        raise ValueError('invalid cost')
    return sum(min(value, cap) for value in costs)


def parse_amount(response):
    import re
    value = response.strip()
    if not re.fullmatch(r'(?:0|[1-9][0-9]*|[1-9][0-9]{0,2}(?:,[0-9]{3})+)', value):
        return None
    return int(value.replace(',', ''))


def verify_amount(costs, cap, response):
    expected = reimburse(costs, cap)
    parsed = parse_amount(response)
    return dict(accepted=parsed == expected, parsed=parsed,
                reason='malformed amount' if parsed is None else 'correct amount' if parsed == expected else 'wrong amount')


def verify_process(costs, cap, candidate):
    return (verify_amount(costs, cap, candidate['response'])['accepted']
            and candidate['allowances'] == [min(value, cap) for value in costs]
            and candidate['total'] == sum(candidate['allowances']))


def audit_tokens(text):
    import re
    return len(re.findall(r'[A-Za-z_]+|[0-9]+|[^\s]', text))


def parse_step_answer(text):
    import re
    match = re.fullmatch(r'([0-9]+) \+ ([0-9]+) = ([0-9]+)', text)
    if not match:
        raise ValueError('malformed step expression')
    return int(match.group(3))


def replay_case(case, method, maximum, order):
    from collections import Counter
    if not isinstance(maximum, int) or maximum < 0 or method not in {'direct', 'steps', 'vote', 'search'}:
        raise ValueError('invalid replay policy')
    if sorted(order) != sorted(candidate['id'] for candidate in case['candidates']):
        raise ValueError('invalid candidate order')
    prompt = 'sum per night minimum costs ' + ' '.join(map(str, case['costs'])) + ' cap ' + str(case['cap'])
    calls, selected, seen = [], None, []
    candidates = {candidate['id']: candidate for candidate in case['candidates']}
    for index, candidate_id in enumerate(order):
        needed = 2 if method == 'search' else 1
        if len(calls) + needed > maximum:
            break
        candidate = candidates[candidate_id]
        response = case['direct'] if method == 'direct' else candidate['text']
        total = parse_amount(response) if method == 'direct' else parse_step_answer(response)
        calls.append(dict(kind='generate', candidate='direct' if method == 'direct' else candidate_id,
                          input_tokens=audit_tokens(prompt), output_tokens=audit_tokens(response), response=response))
        seen.append(total)
        if method in {'direct', 'steps'}:
            selected = total
            break
        if method == 'search':
            accepted = verify_amount(case['costs'], case['cap'], str(total))['accepted']
            calls.append(dict(kind='verify', candidate=candidate_id,
                              input_tokens=audit_tokens(prompt) + audit_tokens(response), output_tokens=1,
                              response='accept' if accepted else 'reject'))
            if accepted:
                selected = total
                break
        if method == 'vote':
            counts = Counter(seen)
            selected = max(seen, key=lambda answer: counts[answer])
    return dict(case=case['id'], method=method, maximum=maximum, order=order, selected=selected,
                correct=selected == case['answer'], calls=calls, call_count=len(calls),
                tokens=sum(call['input_tokens'] + call['output_tokens'] for call in calls))


def replay_budget():
    import time
    data = fixture('budget-v1.json')
    rows = []
    for order in data['orders']:
        for maximum in data['budget']['maxima']:
            for method in ('direct', 'steps', 'vote', 'search'):
                started = time.perf_counter_ns()
                cases = [replay_case(case, method, maximum, order) for case in data['cases']]
                elapsed = (time.perf_counter_ns() - started) / 1_000_000
                rows.append(dict(order=order, maximum=maximum, method=method, cases=cases,
                                 correct=sum(case['correct'] for case in cases), total=len(cases),
                                 calls=sum(case['call_count'] for case in cases),
                                 tokens=sum(case['tokens'] for case in cases), replay_elapsed_ms=elapsed))
    return rows

def matrix_shape(matrix):
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError('invalid rectangular matrix')
    return len(matrix), len(matrix[0])


def matmul(left, right):
    rows, inner = matrix_shape(left)
    other_inner, columns = matrix_shape(right)
    if inner != other_inner:
        raise ValueError('matrix dimensions do not match')
    return [[sum(left[i][k] * right[k][j] for k in range(inner))
             for j in range(columns)] for i in range(rows)]


def matvec(matrix, vector):
    return [row[0] for row in matmul(matrix, [[value] for value in vector])]


def low_rank(base, a, b, vector, alpha=1):
    rows, columns = matrix_shape(base)
    rank, input_columns = matrix_shape(a)
    output_rows, other_rank = matrix_shape(b)
    if (input_columns, output_rows, other_rank) != (columns, rows, rank):
        raise ValueError('incompatible adapter dimensions')
    scale = alpha / rank
    delta = [[scale * value for value in row] for row in matmul(b, a)]
    base_output = matvec(base, vector)
    adapter_output = [scale * value for value in matvec(b, matvec(a, vector))]
    combined = [left + right for left, right in zip(base_output, adapter_output)]
    merged = [[left + right for left, right in zip(row, increment)]
              for row, increment in zip(base, delta)]
    return dict(delta=delta, base_output=base_output, adapter_output=adapter_output,
                combined_output=combined, merged_output=matvec(merged, vector),
                base_parameters=rows * columns, trainable_parameters=rank * (rows + columns))
