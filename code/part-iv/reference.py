# SPDX-License-Identifier: Apache-2.0
"""Independent scalar arithmetic; never imports the vectorized implementation."""
import math


def matmul(left, right):
    return [[sum(row[k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for row in left]


def norm(row, epsilon=1e-5):
    mean = sum(row) / len(row)
    variance = sum((v - mean) ** 2 for v in row) / len(row)
    return [(v - mean) / math.sqrt(variance + epsilon) for v in row]


def attention(q, k, v, visible):
    out = []
    for i, query in enumerate(q):
        allowed = [j for j, yes in enumerate(visible[i]) if yes]
        if not allowed:
            raise ValueError("empty query")
        scores = [sum(a * b for a, b in zip(query, k[j])) / math.sqrt(len(query)) for j in allowed]
        maximum = max(scores)
        numerators = [math.exp(s - maximum) for s in scores]
        denominator = sum(numerators)
        out.append([sum(n * v[j][c] for n, j in zip(numerators, allowed)) / denominator for c in range(len(v[0]))])
    return out


def block(x):
    n1 = [norm(row) for row in x]
    visible = [[j <= i for j in range(len(x))] for i in range(len(x))]
    h = []
    for c in range(2):
        values = [[row[c]] for row in n1]
        h.append(attention(values, values, values, visible))
    joined = [[h[0][i][0], h[1][i][0]] for i in range(len(x))]
    change = matmul(joined, [[1, 1], [1, -1]])
    r = [[a + b for a, b in zip(old, add)] for old, add in zip(x, change)]
    n2 = [norm(row) for row in r]
    hidden = [[max(v, 0) for v in row] for row in matmul(n2, [[1, -1, 0], [0, 1, 1]])]
    ffn = matmul(hidden, [[1, 0], [0, 1], [1, -1]])
    return [[a + b for a, b in zip(old, add)] for old, add in zip(r, ffn)]
