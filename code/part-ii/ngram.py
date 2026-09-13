# SPDX-License-Identifier: Apache-2.0
"""Parameterized character N-gram bridge; reads the unchanged Part I data."""
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fit(texts, vocabulary, n=2, alpha=0):
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    if not math.isfinite(alpha) or alpha < 0:
        raise ValueError("alpha must be finite and nonnegative")
    if len(set(vocabulary)) != len(vocabulary) or "EOS" not in vocabulary or "BOS" in vocabulary:
        raise ValueError("invalid candidate vocabulary")
    rows = defaultdict(Counter)
    for text in texts:
        if not isinstance(text, str) or any(c not in vocabulary for c in text):
            raise ValueError("text contains unsupported characters")
        history = ["BOS"] * (n - 1)
        for token in [*text, "EOS"]:
            context = tuple(history[-(n - 1):]) if n > 1 else ()
            rows[context][token] += 1
            history.append(token)
    return {"n": n, "alpha": alpha, "vocabulary": list(vocabulary), "rows": dict(rows)}


def probabilities(model, context):
    counts = model["rows"].get(tuple(context), {})
    denominator = sum(counts.values()) + model["alpha"] * len(model["vocabulary"])
    if denominator == 0:
        return None
    return [(counts.get(token, 0) + model["alpha"]) / denominator for token in model["vocabulary"]]


def sequence_probability(model, text):
    if any(c not in model["vocabulary"] for c in text):
        raise ValueError("text contains unsupported characters")
    history = ["BOS"] * (model["n"] - 1)
    result = 1.0
    for token in [*text, "EOS"]:
        context = history[-(model["n"] - 1):] if model["n"] > 1 else []
        row = probabilities(model, context)
        if row is None:
            return None
        result *= row[model["vocabulary"].index(token)]
        if result == 0:
            return 0.0  # A zero-probability prefix cannot recover later.
        history.append(token)
    return result


def generate(model, seed=42, max_draws=12):
    state = seed % (2 ** 32)
    history = ["BOS"] * (model["n"] - 1)
    tokens, draws = [], []
    for _ in range(max_draws):
        context = history[-(model["n"] - 1):] if model["n"] > 1 else []
        row = probabilities(model, context)
        if row is None:
            return {"tokens": tokens, "draws": draws, "stop": "undefined"}
        state = (1664525 * state + 1013904223) % (2 ** 32)
        draw = state / (2 ** 32)
        cumulative = 0.0
        selected = model["vocabulary"][-1]
        for candidate, probability in zip(model["vocabulary"], row):
            cumulative += probability
            if draw < cumulative:
                selected = candidate
                break
        tokens.append(selected)
        draws.append(draw)
        history.append(selected)
        if selected == "EOS":
            return {"tokens": tokens, "draws": draws, "stop": "eos"}
    return {"tokens": tokens, "draws": draws, "stop": "limit"}


def run():
    fixture = json.loads((ROOT / "data/part-i/ngram.json").read_text())
    expected = json.loads((ROOT / "data/part-i/expected.json").read_text())
    results = []
    for case in expected["held_out"]:
        model = fit(fixture["train"], fixture["vocabulary"], case["n"], case["alpha"])
        result = {"n": case["n"], "alpha": case["alpha"]}
        for text in fixture["held_out"]:
            result[text] = sequence_probability(model, text)
            assert math.isclose(result[text], case[text], abs_tol=1e-12)
        results.append(result)
    baseline = fit(fixture["train"], fixture["vocabulary"])
    assert {context[0]: [row.get(t, 0) for t in fixture["vocabulary"]]
            for context, row in baseline["rows"].items()} == expected["bigram_rows"]
    sample = generate(baseline, fixture["seed"], fixture["max_draws"])
    assert sample["tokens"] == expected["generation"]["tokens"]
    assert sample["draws"] == expected["generation"]["draws"]
    output = {"held_out": results, "generation": sample}
    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    run()
