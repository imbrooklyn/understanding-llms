# SPDX-License-Identifier: Apache-2.0
"""One hand-derived SGD step and a fixed nonlinear CPU classification run."""
import copy
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[2]


def one_step():
    x = torch.tensor([1.0, 2.0], dtype=torch.float64)
    w = torch.zeros(2, dtype=torch.float64, requires_grad=True)
    bias = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    optimizer = torch.optim.SGD([w, bias], lr=0.1)
    optimizer.zero_grad()
    z = x @ w + bias
    loss = nn.functional.binary_cross_entropy_with_logits(z, torch.tensor(1.0, dtype=torch.float64))
    loss.backward()
    gradients = {"w": w.grad.tolist(), "bias": bias.grad.item()}
    optimizer.step()
    with torch.no_grad():
        new_z = (x @ w + bias).item()
    assert gradients == {"w": [-0.5, -1.0], "bias": -0.5}
    assert torch.allclose(w, torch.tensor([0.05, 0.1], dtype=torch.float64), atol=1e-12)
    return {"initial_loss": loss.item(), "gradients": gradients, "new_w": w.tolist(), "new_bias": bias.item(),
            "new_z": new_z, "new_probability": 1 / (1 + math.exp(-new_z)), "new_loss": math.log1p(math.exp(-new_z)),
            "perturb_w0_minus_0_01_loss": math.log1p(math.exp(0.01)),
            "perturb_w0_plus_0_01_loss": math.log1p(math.exp(-0.01))}


def tensors(rows):
    return (torch.tensor([row["x"] for row in rows], dtype=torch.float64, device="cpu"),
            torch.tensor([row["label"] for row in rows], dtype=torch.long, device="cpu"))


def evaluate(model, inputs):
    x, target = inputs
    model.eval()
    with torch.no_grad():
        logits = model(x)
        loss = nn.functional.cross_entropy(logits, target).item()
        correct = int((logits.argmax(dim=1) == target).sum().item())
    return {"loss": loss, "correct": correct, "count": len(target), "accuracy": correct / len(target)}


def run(write=False):
    started = time.perf_counter()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(17)
    data_path = ROOT / "data/part-ii/classifier-data.json"
    fixture = json.loads(data_path.read_text())
    train = tensors(fixture["splits"]["train"])
    validation = tensors(fixture["splits"]["validation"])
    model = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 2)).double()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    curve, best = [], None
    for step in range(601):
        train_metrics, validation_metrics = evaluate(model, train), evaluate(model, validation)
        curve.append({"step": step, "train": train_metrics, "validation": validation_metrics})
        if best is None or validation_metrics["loss"] < best["validation"]["loss"]:
            best = {"step": step, "train": train_metrics, "validation": validation_metrics,
                    "state": copy.deepcopy(model.state_dict())}
        if step == 600:
            break
        model.train()
        optimizer.zero_grad()
        logits = model(train[0])
        loss = nn.functional.cross_entropy(logits, train[1])
        loss.backward()
        optimizer.step()
    model.load_state_dict(best["state"])
    test_metrics = evaluate(model, tensors(fixture["splits"]["test"]))
    result = {"version": "classifier-run-v1", "as_of": "2026-09-11", "status": "measured CPU run",
              "dataset_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "environment": {"python": platform.python_version(), "torch": torch.__version__, "system": platform.system(), "machine": platform.machine(), "device": "cpu", "dtype": "float64", "threads": 1},
              "configuration": {"seed": 17, "layers": [2, 32, 32, 2], "activation": "ReLU", "optimizer": "Adam", "learning_rate": 0.03, "steps": 600, "batch": "all 24 training rows", "selection": "minimum validation loss, first step wins exact ties"},
              "one_step": one_step(), "curve": curve, "selected_step": best["step"],
              "selected_train": best["train"], "selected_validation": best["validation"], "test_once_after_selection": test_metrics,
              "elapsed_seconds": time.perf_counter() - started}
    if write:
        (ROOT / "data/part-ii/classifier-run.json").write_text(json.dumps(result, indent=2) + "\n")
        snapshot = {"version": "classifier-selected-v1", "license": "CC-BY-SA-4.0", "step": best["step"],
                    "dataset_sha256": result["dataset_sha256"], "state_dict": {key: value.tolist() for key, value in best["state"].items()}}
        (ROOT / "data/part-ii/classifier-model.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    summary = {key: result[key] for key in ["environment", "selected_step", "selected_train", "selected_validation", "test_once_after_selection", "elapsed_seconds", "one_step"]}
    summary["curve_samples"] = [curve[i] for i in [0, 20, 100, 300, 600]]
    print(json.dumps(summary, indent=2))
    return result


if __name__ == "__main__":
    run(write=True)
