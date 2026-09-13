# SPDX-License-Identifier: Apache-2.0
"""Print and optionally save actual NumPy traces without replacing expected values."""
import argparse
import json
from pathlib import Path
import platform
import numpy as np
from mechanisms import projected_attention, masked_softmax, two_heads, small_block

ROOT = Path(__file__).resolve().parents[2]


def serialize(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {k: serialize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serialize(v) for v in value]
    return value


def run():
    fixture = json.loads((ROOT / "data/part-iv/attention.json").read_text())
    a = projected_attention(*(fixture[k] for k in ("X", "WQ", "WK", "WV")))
    errors = {}
    for key, expected in fixture["expected"].items():
        errors[key] = float(np.max(np.abs(a[key] - expected)))
        np.testing.assert_allclose(a[key], expected, atol=fixture["tolerance"], rtol=0)
    causal = masked_softmax(a["scores"], np.tril(np.ones((3, 3), dtype=bool)))
    position = np.array([[0., 0.], [0., 1.], [1., 0.]])
    return serialize(dict(python=platform.python_version(), numpy=np.__version__,
        dtype="float64", device="cpu", attention=a, max_abs_errors=errors,
        causal_weights=causal, causal_output=causal @ a["V"],
        multihead=two_heads(fixture["X"]), position=position,
        block=small_block(np.asarray(fixture["X"]) + position)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.write:
        (ROOT / "data/part-iv/numpy-run.json").write_text(payload)
    print(payload)
