# SPDX-License-Identifier: Apache-2.0
"""Regenerate the original frozen synthetic split; never fit a model here."""
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[2]


def dataset():
    generator = random.Random(1729)
    splits = {}
    seen = set()
    for split, count in [("train", 24), ("validation", 48), ("test", 48)]:
        rows = []
        for index in range(count):
            point = [round(generator.uniform(-1, 1), 4) for _ in range(2)]
            assert tuple(point) not in seen
            seen.add(tuple(point))
            clean = int(point[0] * point[1] > 0)
            corrupted = split == "train" and index in [2, 7, 13, 19]
            rows.append({"id": f"{split}-{index:02}", "x": point, "label": 1 - clean if corrupted else clean,
                         "rule_label": clean, "label_flipped": corrupted})
        splits[split] = rows
    return {"version": "quadrants-v1", "license": "CC-BY-SA-4.0", "provenance": "Original authored synthetic diagnostic, not real people or a representative benchmark",
            "generator": "Python random.Random(1729), uniform(-1,1), round to 4 decimal places, train then validation then test",
            "axes": ["dimensionless horizontal coordinate", "dimensionless vertical coordinate"],
            "rule": "class 1 iff x0*x1 > 0; four predetermined train labels flipped",
            "split_policy": "frozen disjoint rows before fitting; validation selects a snapshot; test scored only after selection",
            "splits": splits}


if __name__ == "__main__":
    (ROOT / "data/part-ii/classifier-data.json").write_text(json.dumps(dataset(), indent=2) + "\n")
