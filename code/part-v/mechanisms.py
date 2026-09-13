# SPDX-License-Identifier: Apache-2.0
"""Small scalar mechanisms; inputs and localized text live in shared resources."""
import math


def distribution(logits, temperature=1, top_k=None, top_p=None):
    if not logits or not all(math.isfinite(x) for x in logits):
        raise ValueError('finite nonempty logits required')
    if not math.isfinite(temperature) or temperature < 0:
        raise ValueError('temperature must be finite and nonnegative')
    if top_k is not None and (type(top_k) is not int or not 1 <= top_k <= len(logits)):
        raise ValueError('top_k outside candidate range')
    if top_p is not None and not 0 < top_p <= 1:
        raise ValueError('top_p must be in (0,1]')
    order = sorted(range(len(logits)), key=lambda i: (-logits[i], i))
    if temperature == 0:
        return [float(i == order[0]) for i in range(len(logits))]
    scaled = [(x - max(logits)) / temperature for x in logits]
    masses = [math.exp(x) for x in scaled]
    eligible = order[:top_k] if top_k is not None else order
    denominator = sum(masses[i] for i in eligible)
    if top_p is not None:
        retained, cumulative = [], 0.0
        for i in eligible:
            retained.append(i)
            cumulative += masses[i] / denominator
            if cumulative >= top_p:
                break
        eligible = retained
        denominator = sum(masses[i] for i in eligible)
    return [masses[i] / denominator if i in eligible else 0.0 for i in range(len(logits))]


def draw_index(probabilities, draw):
    if not 0 <= draw < 1 or not probabilities or not all(math.isfinite(p) and p >= 0 for p in probabilities) or not math.isclose(sum(probabilities), 1, abs_tol=1e-12):
        raise ValueError('invalid distribution or draw')
    cumulative = 0.0
    for i, probability in enumerate(probabilities):
        cumulative += probability
        if draw < cumulative:
            return i
    return max(i for i, p in enumerate(probabilities) if p > 0)


def rotate_quarter(vector, turns):
    if len(vector) != 2 or type(turns) is not int:
        raise ValueError('two coordinates and integer quarter turns required')
    x, y = vector
    for _ in range(turns % 4):
        x, y = -y, x
    return [x, y]


def rmsnorm(values, epsilon=1e-6):
    if not values or not math.isfinite(epsilon) or epsilon < 0 or not all(math.isfinite(x) for x in values):
        raise ValueError('invalid RMS inputs')
    denominator = math.sqrt(sum(x*x for x in values) / len(values) + epsilon)
    if denominator == 0:
        raise ValueError('zero RMS denominator')
    return [x / denominator for x in values]


def row_matmul(row, matrix):
    if not matrix or len(row) != len(matrix) or not matrix[0] or any(len(r) != len(matrix[0]) for r in matrix):
        raise ValueError('matrix shape mismatch')
    return [sum(x*r[j] for x, r in zip(row, matrix)) for j in range(len(matrix[0]))]


def swiglu(row, gate, up, down):
    g, u = row_matmul(row, gate), row_matmul(row, up)
    if len(g) != len(u):
        raise ValueError('gate and value widths differ')
    silu = [x / (1 + math.exp(-x)) for x in g]
    product = [x*y for x, y in zip(silu, u)]
    return dict(gate=g, up=u, silu=silu, product=product, output=row_matmul(product, down))


def kv_bytes(layers, tokens, kv_heads, head_width, bytes_per_value, sequences=1):
    values = [layers, tokens, kv_heads, head_width, bytes_per_value, sequences]
    if any(type(x) is not int or x < 0 for x in values) or min(layers, kv_heads, head_width, bytes_per_value, sequences) == 0:
        raise ValueError('invalid KV dimensions')
    return 2 * math.prod(values)


def latency(arrival, emissions):
    if not emissions or not all(math.isfinite(x) for x in [arrival, *emissions]):
        raise ValueError('at least one finite emission required')
    if emissions[0] < arrival or any(b < a for a, b in zip(emissions, emissions[1:])):
        raise ValueError('timestamps out of order')
    gaps = [b-a for a, b in zip(emissions, emissions[1:])]
    return dict(ttft_ms=emissions[0]-arrival, gaps_ms=gaps,
                tpot_ms=sum(gaps)/len(gaps) if gaps else None,
                end_to_end_ms=emissions[-1]-arrival)


def quantize(values, scale, qmin=-7, qmax=7):
    if not math.isfinite(scale) or scale <= 0 or qmin >= qmax or not all(math.isfinite(x) for x in values):
        raise ValueError('invalid quantizer inputs')
    integers = [max(qmin, min(qmax, round(x/scale))) for x in values]
    decoded = [x*scale for x in integers]
    return dict(integers=integers, decoded=decoded, errors=[q-x for q, x in zip(decoded, values)])


def weighted_gradient(means, counts):
    if len(means) != len(counts) or not counts or not all(math.isfinite(g) for g in means) or any(type(n) is not int or n <= 0 for n in counts):
        raise ValueError('positive aligned event counts required')
    return sum(g*n for g, n in zip(means, counts)) / sum(counts)


def speculative_correction(target, proposal):
    if len(target) != len(proposal) or not target or any(x < 0 for x in target+proposal) or not all(math.isclose(sum(x), 1, abs_tol=1e-12) for x in (target, proposal)):
        raise ValueError('two aligned distributions required')
    accept = [min(1, p/q) if q else 1 for p, q in zip(target, proposal)]
    residual = [max(0, p-q) for p, q in zip(target, proposal)]
    total = sum(residual)
    return dict(accept=accept, residual=[x/total for x in residual] if total else None)


def linear_prefix(keys, values):
    if len(keys) != len(values) or not keys or any(k < 0 for k in keys):
        raise ValueError('aligned nonnegative keys required')
    numerator, denominator, rows = 0, 0, []
    for key, value in zip(keys, values):
        numerator += key * value
        denominator += key
        rows.append(dict(numerator=numerator, denominator=denominator,
                         output=numerator/denominator if denominator else None))
    return rows


def rescue(clean, corrupt, patched):
    return (patched-corrupt)/(clean-corrupt) if clean != corrupt else None


def two_step_beam(first, after, width):
    if type(width) is not int or width < 1:
        raise ValueError('positive integer beam width required')
    parents = sorted(first.items(), key=lambda x:-x[1])[:width]
    paths = [dict(tokens=[parent,child], probability=parent_mass*child_mass, complete=child=='EOS')
             for parent,parent_mass in parents for child,child_mass in after[parent].items()]
    return sorted(paths,key=lambda x:-x['probability'])[:width]


def confusion(predicted, actual):
    if len(predicted)!=len(actual) or not predicted:
        raise ValueError('aligned nonempty labels required')
    return {key:sum(p==want_p and a==want_a for p,a in zip(predicted,actual))
            for key,want_p,want_a in [('tp',True,True),('fp',True,False),('tn',False,False),('fn',False,True)]}
