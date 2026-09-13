# SPDX-License-Identifier: Apache-2.0
"""Small, explicit arithmetic; no third-party dependencies."""
import math


def dot(left, right):
    if len(left) != len(right):
        raise ValueError("coordinate lengths differ")
    return math.fsum(a * b for a, b in zip(left, right))


def matmul(left, right):
    if not left or not right or not right[0]:
        raise ValueError("nonempty matrices required")
    width = len(left[0])
    if any(len(row) != width for row in left) or any(len(row) != len(right[0]) for row in right):
        raise ValueError("ragged matrix")
    if width != len(right):
        raise ValueError("contracted dimensions differ")
    return [[dot(row, column) for column in zip(*right)] for row in left]


def cosine(left, right):
    numerator = dot(left, right)
    denominator = math.sqrt(dot(left, left) * dot(right, right))
    return None if denominator == 0 else numerator / denominator


def softmax(logits):
    if not logits or not all(math.isfinite(value) for value in logits):
        raise ValueError("finite nonempty logits required")
    shift = max(logits)
    weights = [math.exp(value - shift) for value in logits]
    total = math.fsum(weights)
    return [value / total for value in weights]


def target_loss(logits, target):
    if not 0 <= target < len(logits):
        raise ValueError("target outside candidate order")
    softmax(logits)  # Validate input without taking log of an underflowed probability.
    shift = max(logits)
    return shift - logits[target] + math.log(math.fsum(math.exp(x - shift) for x in logits))


def distribution(values):
    if not values or any(not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("nonnegative finite probabilities required")
    if not math.isclose(math.fsum(values), 1, abs_tol=1e-12):
        raise ValueError("probabilities must sum to one")


def kl(reference, proposal):
    distribution(reference)
    distribution(proposal)
    if len(reference) != len(proposal):
        raise ValueError("candidate lengths differ")
    terms = []
    for q, p in zip(reference, proposal):
        if q == 0:
            continue
        if p == 0:
            return math.inf
        terms.append(q * math.log(q / p))
    return math.fsum(terms)
