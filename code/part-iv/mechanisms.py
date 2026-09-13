# SPDX-License-Identifier: Apache-2.0
"""Explicit NumPy mechanisms; dimensions are batch, heads, positions, coordinates."""
import numpy as np


def softmax(scores):
    scores = np.asarray(scores, dtype=np.float64)
    if not np.isfinite(scores).all():
        raise ValueError("softmax requires finite unmasked scores")
    shifted = scores - scores.max(axis=-1, keepdims=True)
    weights = np.exp(shifted)
    return weights / weights.sum(axis=-1, keepdims=True)


def projected_attention(x, wq, wk, wv):
    x, wq, wk, wv = (np.asarray(a, dtype=np.float64) for a in (x, wq, wk, wv))
    q, k, v = x @ wq, x @ wk, x @ wv
    dots = q @ k.swapaxes(-1, -2)
    scores = dots / np.sqrt(q.shape[-1])
    weights = softmax(scores)
    return dict(Q=q, K=k, V=v, dots=dots, scores=scores, weights=weights, output=weights @ v)


def masked_softmax(scores, visible, query_valid=None):
    """True means allowed. Invalid queries return zero; empty valid rows fail."""
    scores = np.asarray(scores, dtype=np.float64)
    visible = np.broadcast_to(np.asarray(visible, dtype=bool), scores.shape)
    valid = np.ones(scores.shape[:-1], dtype=bool) if query_valid is None else np.broadcast_to(query_valid, scores.shape[:-1])
    if not np.isfinite(scores).all():
        raise ValueError("input scores must be finite")
    if np.any(valid & ~visible.any(axis=-1)):
        raise ValueError("a valid query has no visible key")
    masked = np.where(visible & valid[..., None], scores, -np.inf)
    # Avoid evaluating an undefined all-minus-infinity row, even transiently.
    safe = np.where(valid[..., None], masked, 0.0)
    shifted = safe - safe.max(axis=-1, keepdims=True)
    exp = np.exp(shifted)
    weights = exp / exp.sum(axis=-1, keepdims=True)
    return np.where(valid[..., None], weights, 0.0)


def two_heads(x):
    """Two one-coordinate causal heads; head order is first, second coordinate."""
    x = np.asarray(x, dtype=np.float64)
    visible = np.tril(np.ones((len(x), len(x)), dtype=bool))
    heads, weights = [], []
    for coordinate in (0, 1):
        q = x[:, coordinate:coordinate + 1]
        a = masked_softmax(q @ q.T, visible)
        heads.append(a @ q)
        weights.append(a)
    joined = np.concatenate(heads, axis=-1)
    wo = np.array([[1., 1.], [1., -1.]])
    return dict(weights=weights, heads=heads, joined=joined, output=joined @ wo)


def layer_norm(x, gamma=None, beta=None, epsilon=1e-5):
    x = np.asarray(x, dtype=np.float64)
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    mean = x.mean(axis=-1, keepdims=True)
    variance = ((x - mean) ** 2).mean(axis=-1, keepdims=True)
    gamma = np.ones(x.shape[-1]) if gamma is None else np.asarray(gamma)
    beta = np.zeros(x.shape[-1]) if beta is None else np.asarray(beta)
    if gamma.shape != (x.shape[-1],) or beta.shape != gamma.shape:
        raise ValueError("normalization parameters must match coordinates")
    return (x - mean) / np.sqrt(variance + epsilon) * gamma + beta


def residual(x, change):
    if x.shape != change.shape:
        raise ValueError("residual shapes must match exactly")
    return x + change


def small_block(x):
    """One pre-norm block: a causal two-head read and a shared 2->3->2 FFN."""
    x = np.asarray(x, dtype=np.float64)
    assert x.ndim == 2 and x.shape[-1] == 2
    norm1 = layer_norm(x)
    attention = two_heads(norm1)
    r = residual(x, attention["output"])
    norm2 = layer_norm(r)
    w1 = np.array([[1., -1., 0.], [0., 1., 1.]])
    w2 = np.array([[1., 0.], [0., 1.], [1., -1.]])
    hidden = np.maximum(norm2 @ w1, 0)
    ffn = hidden @ w2
    out = residual(r, ffn)
    assert out.shape == x.shape
    return dict(input=x, norm1=norm1, attention=attention["output"], residual1=r,
                norm2=norm2, hidden=hidden, ffn=ffn, output=out)
