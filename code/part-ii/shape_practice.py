# SPDX-License-Identifier: Apache-2.0
"""Reproduce Chapter 5 from its shared fixture on CPU."""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def run():
    fixture = json.loads((ROOT / "data/part-ii/arithmetic.json").read_text())
    x = np.array(fixture["shape"]["input"], dtype=np.float64)
    w = np.array(fixture["shape"]["weight"], dtype=np.float64)
    actual = x @ w
    np.testing.assert_array_equal(actual, fixture["shape"]["expected_output"])
    swapped = x.transpose(1, 0, 2)
    assert swapped.shape == x.shape
    assert not np.array_equal(swapped, x)
    result = {"input_shape": list(x.shape), "weight_shape": list(w.shape),
              "output_shape": list(actual.shape), "output": actual.tolist(),
              "same_shape_different_axes": not np.array_equal(swapped, x)}
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run()
