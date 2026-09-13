# SPDX-License-Identifier: Apache-2.0
"""Actual CPU training, gradient, shape and representation checks."""
import contextlib
import io
import json
import math
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
import torch
from torch import nn
import classifier
import nnlm

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class CPUTests(unittest.TestCase):
    def test_numpy_axes_padding_and_independent_torch_loss(self):
        fixture = read("data/part-ii/arithmetic.json")["shape"]
        x = np.array(fixture["input"], dtype=np.float64)
        w = np.array(fixture["weight"], dtype=np.float64)
        np.testing.assert_array_equal(x @ w, fixture["expected_output"])
        self.assertEqual(x.shape, x.transpose(1, 0, 2).shape)
        self.assertFalse(np.array_equal(x, x.transpose(1, 0, 2)))
        np.testing.assert_array_equal(np.array([[2, 2], [0, 0]])[:1].mean(0), [2, 2])
        logits = torch.tensor([[math.log(2), 0, 0]] * 2, dtype=torch.float64)
        losses = nn.functional.cross_entropy(logits, torch.tensor([0, 1]), reduction="none")
        torch.testing.assert_close(losses, torch.tensor([math.log(2), math.log(4)], dtype=torch.float64), atol=1e-12, rtol=0)

    def test_all_gradient_routes_and_opposite_target(self):
        result = classifier.one_step()
        self.assertEqual(result["gradients"], {"w": [-0.5, -1], "bias": -0.5})
        self.assertAlmostEqual(result["new_loss"], math.log1p(math.exp(-0.3)), places=12)
        for target in [0.0, 1.0]:
            parameter = torch.zeros(3, dtype=torch.float64, requires_grad=True)
            inputs = torch.tensor([1.0, 2.0, 1.0], dtype=torch.float64)
            loss = nn.functional.binary_cross_entropy_with_logits(parameter @ inputs, torch.tensor(target, dtype=torch.float64))
            loss.backward()
            expected = [(0.5-target)*x for x in [1, 2, 1]]
            self.assertEqual(parameter.grad.tolist(), expected)
            for axis in range(3):
                plus, minus = parameter.detach().clone(), parameter.detach().clone()
                plus[axis], minus[axis] = 1e-5, -1e-5
                def scalar(p):
                    z = float(p @ inputs)
                    return math.log1p(math.exp(z)) - target*z
                self.assertAlmostEqual((scalar(plus)-scalar(minus))/2e-5, expected[axis], places=9)

    def test_frozen_split_roles_and_measured_overfit(self):
        data = read("data/part-ii/classifier-data.json")
        all_rows = [row for rows in data["splits"].values() for row in rows]
        self.assertEqual(len({tuple(row["x"]) for row in all_rows}), 120)
        self.assertEqual(len({row["id"] for row in all_rows}), 120)
        self.assertEqual([len(data["splits"][key]) for key in ["train", "validation", "test"]], [24, 48, 48])
        for split, rows in data["splits"].items():
            self.assertEqual(sum(row["label_flipped"] for row in rows), 4 if split == "train" else 0)
            for row in rows:
                clean = int(row["x"][0] * row["x"][1] > 0)
                self.assertEqual(row["label"], 1-clean if row["label_flipped"] else clean)
        calls, original = [], classifier.tensors
        def trace(rows):
            calls.append(rows[0]["id"].split("-")[0])
            return original(rows)
        with contextlib.redirect_stdout(io.StringIO()), patch.object(classifier, "tensors", side_effect=trace):
            result = classifier.run(write=False)
        self.assertEqual(calls, ["train", "validation", "test"])
        self.assertEqual(result["selected_step"], min(result["curve"], key=lambda row: row["validation"]["loss"])["step"])
        self.assertEqual(result["selected_step"], 5)
        self.assertEqual(result["curve"][-1]["train"]["correct"], 24)
        self.assertGreater(result["curve"][-1]["validation"]["loss"], 8)
        self.assertEqual(result["test_once_after_selection"]["correct"], 38)
        reference = read("data/part-ii/classifier-run.json")
        for measured, recorded in zip(result["curve"], reference["curve"]):
            for split in ["train", "validation"]:
                self.assertAlmostEqual(measured[split]["loss"], recorded[split]["loss"], delta=1e-9)

    def test_saved_classifier_parameters_reproduce_selected_result(self):
        snapshot = read("data/part-ii/classifier-model.json")
        model = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 2)).double()
        model.load_state_dict({key: torch.tensor(value, dtype=torch.float64) for key, value in snapshot["state_dict"].items()})
        self.assertEqual(sum(p.numel() for p in model.parameters()), 1218)
        result = classifier.evaluate(model, classifier.tensors(read("data/part-ii/classifier-data.json")["splits"]["test"]))
        self.assertAlmostEqual(result["loss"], read("data/part-ii/classifier-run.json")["test_once_after_selection"]["loss"], delta=1e-9)

    def test_nnlm_paper_order_and_fixed_window_collision(self):
        self.assertAlmostEqual(nnlm.paper_trace()["loss"], math.log(2), places=12)
        paper = read("data/part-ii/nnlm-paper.json")
        embedding = np.array(paper["embedding"])
        hidden = embedding[paper["reversed_context"]].reshape(1, 4) @ np.array(paper["hidden_weight"])
        np.testing.assert_array_equal(hidden, [[0, 0]])
        collision = read("data/part-ii/nnlm-data.json")["window_collision"]
        windows = [prefix[-collision["window"]:] for prefix in collision["prefix_ids"]]
        self.assertEqual(windows, collision["expected_contexts"])
        self.assertNotEqual(collision["prefix_ids"][0], collision["prefix_ids"][1])
        model = nnlm.WindowLM(5, 5).double().eval()
        logits = model(torch.tensor(windows, dtype=torch.long))
        self.assertTrue(torch.equal(logits[0], logits[1]))

    def test_count_lm_fractions_and_actual_nnlm_training(self):
        fixture = read("data/part-ii/nnlm-data.json")
        train = nnlm.events(fixture["train"], fixture)
        test = nnlm.events(fixture["test"], fixture)
        self.assertEqual((len(train), len(test)), (20, 8))
        self.assertEqual(sum(row["context"] == ["BOS", "BOS"] for row in train), 5)
        expected = [2/7, 1/4, 2/11, 1/10, 1/5, 2/7, 1/12, 1/5]
        self.assertEqual(nnlm.count_measure(train, test, fixture)["target_probabilities"], expected)
        with contextlib.redirect_stdout(io.StringIO()):
            result = nnlm.run(write=False)
        self.assertEqual(result["selected_step"], 10)
        self.assertEqual(result["selected_step"], min(result["curve"], key=lambda row: row["validation_loss"])["step"])
        count, neural = [result["test_once_after_selection"][key] for key in ["count_lm", "nnlm"]]
        self.assertLess(neural["mean_loss"], count["mean_loss"])
        self.assertLess(neural["correct"], count["correct"])
        self.assertAlmostEqual(neural["mean_loss"], read("data/part-ii/nnlm-run.json")["test_once_after_selection"]["nnlm"]["mean_loss"], delta=1e-9)
        for method, successes in [("authored_static", 4), ("nnlm_input_mean", 7)]:
            for locale in ["en", "zh-hans"]:
                self.assertEqual(result["retrieval"][method][locale]["success_count"], successes)
                self.assertEqual(result["retrieval"][method][locale]["query_count"], 9)

    def test_saved_nnlm_and_static_collision_are_distinct_evidence(self):
        fixture = read("data/part-ii/nnlm-data.json")
        model = nnlm.WindowLM(10, 9).double()
        snapshot = read("data/part-ii/nnlm-model.json")
        model.load_state_dict({key: torch.tensor(value, dtype=torch.float64) for key, value in snapshot["state_dict"].items()})
        self.assertEqual(sum(p.numel() for p in model.parameters()), 193)
        inputs = nnlm.tensors(nnlm.events(fixture["test"], fixture), fixture)
        measured = nnlm.measure(model, inputs)
        self.assertAlmostEqual(measured["mean_loss"], 1.4244286318524, delta=1e-9)
        static = read("data/knowledge-assistant/ka-static-v1.json")
        self.assertEqual(nnlm.mean_vectors(["order", "processing"], static["vectors"], 3), nnlm.mean_vectors(["order", "approval"], static["vectors"], 3))
        self.assertEqual(nnlm.mean_vectors(["unseen"], static["vectors"], 3), [0, 0, 0])


if __name__ == "__main__":
    torch.set_num_threads(1)
    unittest.main(verbosity=2)
