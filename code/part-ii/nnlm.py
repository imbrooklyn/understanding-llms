# SPDX-License-Identifier: Apache-2.0
"""A fixed-window neural LM; likelihood and retrieval remain separate tasks."""
from collections import Counter, defaultdict
import copy
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code/knowledge-assistant"))
from baselines import load_fixture, tokens, evaluate_vectors


class WindowLM(nn.Module):
    def __init__(self, input_size, output_size, window=2, dimension=4, hidden=8):
        super().__init__()
        self.embedding = nn.Embedding(input_size, dimension)
        self.hidden = nn.Linear(window * dimension, hidden)
        self.output = nn.Linear(hidden, output_size)

    def forward(self, ids):
        embedded = self.embedding(ids)
        combined = embedded.flatten(start_dim=1)
        hidden = torch.relu(self.hidden(combined))
        return self.output(hidden)


def events(sequences, fixture):
    result = []
    window = fixture["window"]
    for sequence_index, sequence in enumerate(sequences):
        history = ["BOS"] * window
        for position, target in enumerate(sequence + ["EOS"]):
            result.append({"sequence": sequence_index, "position": position,
                           "context": history[-window:], "target": target})
            history.append(target)
    return result


def tensors(event_rows, fixture):
    input_ids = {word: i for i, word in enumerate(fixture["input_vocabulary"])}
    output_ids = {word: i for i, word in enumerate(fixture["output_vocabulary"])}
    return (torch.tensor([[input_ids[word] for word in row["context"]] for row in event_rows], dtype=torch.long),
            torch.tensor([output_ids[row["target"]] for row in event_rows], dtype=torch.long))


def measure(model, inputs):
    model.eval()
    with torch.no_grad():
        logits = model(inputs[0])
        losses = nn.functional.cross_entropy(logits, inputs[1], reduction="none")
        correct = int((logits.argmax(1) == inputs[1]).sum().item())
    return {"mean_loss": losses.mean().item(), "perplexity": math.exp(losses.mean().item()),
            "correct": correct, "events": len(losses), "target_losses": losses.tolist(),
            "predicted_ids": logits.argmax(1).tolist(), "target_probabilities": (-losses).exp().tolist()}


def count_measure(train_events, test_events, fixture):
    counts = defaultdict(Counter)
    for row in train_events:
        counts[tuple(row["context"])][row["target"]] += 1
    probabilities, predictions = [], []
    for row in test_events:
        context = counts[tuple(row["context"])]
        weights = [context[word] + 1 for word in fixture["output_vocabulary"]]
        probabilities.append((context[row["target"]] + 1) / sum(weights))
        predictions.append(fixture["output_vocabulary"][weights.index(max(weights))])
    loss = sum(-math.log(p) for p in probabilities) / len(probabilities)
    return {"target_probabilities": probabilities, "predictions": predictions, "mean_loss": loss,
            "perplexity": math.exp(loss), "events": len(probabilities),
            "correct": sum(prediction == row["target"] for prediction, row in zip(predictions, test_events))}


def paper_trace():
    fixture = json.loads((ROOT / "data/part-ii/nnlm-paper.json").read_text())
    embedding = torch.tensor(fixture["embedding"], dtype=torch.float64)
    hidden_weight = torch.tensor(fixture["hidden_weight"], dtype=torch.float64)
    output_weight = torch.tensor([[0, 0, math.log(3), 0], [0, 0, 0, 0]], dtype=torch.float64)
    embedded = embedding[torch.tensor(fixture["context_ids"])]
    combined = embedded.flatten(start_dim=1)
    hidden = torch.relu(combined @ hidden_weight)
    logits = hidden @ output_weight
    probabilities = logits.softmax(-1)
    loss = nn.functional.cross_entropy(logits, torch.tensor(fixture["target"])).item()
    assert combined.tolist() == fixture["expected_concat"]
    assert hidden.tolist() == fixture["expected_hidden"]
    assert torch.allclose(probabilities, torch.tensor(fixture["expected_probabilities"], dtype=torch.float64), atol=1e-12)
    assert math.isclose(loss, math.log(2), abs_tol=1e-12)
    return {"ids_shape": [1, 2], "embedded_shape": list(embedded.shape), "combined": combined.tolist(),
            "hidden": hidden.tolist(), "logits": logits.tolist(), "probabilities": probabilities.tolist(), "loss": loss}


def mean_vectors(pieces, mapping, dimension):
    if not pieces:
        return [0.0] * dimension
    return [sum(mapping.get(word, [0.0] * dimension)[axis] for word in pieces) / len(pieces)
            for axis in range(dimension)]


def retrieval(mapping, dimension, fixture):
    result = {}
    for locale in ["en", "zh-hans"]:
        documents = [mean_vectors(tokens(d["index_text"][locale], locale, fixture), mapping, dimension) for d in fixture["documents"]]
        queries = [mean_vectors(tokens(q["text"][locale], locale, fixture), mapping, dimension) for q in fixture["queries"]]
        rows = evaluate_vectors(documents, queries, fixture)
        result[locale] = {"dimension": dimension, "document_matrix": documents, "query_matrix": queries,
                          "results": rows, "success_count": sum(row["success"] for row in rows), "query_count": len(rows)}
    return result


def run(write=False):
    started = time.perf_counter()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(23)
    path = ROOT / "data/part-ii/nnlm-data.json"
    fixture = json.loads(path.read_text())
    train_events = events(fixture["train"], fixture)
    validation_events = events(fixture["validation"], fixture)
    train, validation = tensors(train_events, fixture), tensors(validation_events, fixture)
    model = WindowLM(len(fixture["input_vocabulary"]), len(fixture["output_vocabulary"])).double()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    curve, best = [], None
    for step in range(201):
        train_score, validation_score = measure(model, train), measure(model, validation)
        curve.append({"step": step, "train_loss": train_score["mean_loss"], "validation_loss": validation_score["mean_loss"]})
        if best is None or validation_score["mean_loss"] < best["validation"]["mean_loss"]:
            best = {"step": step, "train": train_score, "validation": validation_score, "state": copy.deepcopy(model.state_dict())}
        if step == 200:
            break
        model.train()
        optimizer.zero_grad()
        loss = nn.functional.cross_entropy(model(train[0]), train[1])
        loss.backward()
        optimizer.step()
    model.load_state_dict(best["state"])
    test_events = events(fixture["test"], fixture)
    neural_test = measure(model, tensors(test_events, fixture))
    count_test = count_measure(train_events, test_events, fixture)
    assert all(math.isclose(actual, numerator / denominator, abs_tol=1e-12)
               for actual, (numerator, denominator) in zip(count_test["target_probabilities"], fixture["test_count_target_fractions"]))
    ka = load_fixture()
    static = json.loads((ROOT / "data/knowledge-assistant/ka-static-v1.json").read_text())
    learned = {word: model.embedding.weight[index].detach().tolist() for index, word in enumerate(fixture["input_vocabulary"]) if word not in ["BOS", "EOS"]}
    result = {"version": "nnlm-run-v1", "as_of": "2026-09-12", "status": "measured CPU training and deterministic retrieval", "dataset_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "ka_dataset_sha256": hashlib.sha256((ROOT / "data/knowledge-assistant/ka0-v1.json").read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "environment": {"python": platform.python_version(), "torch": torch.__version__, "device": "cpu", "dtype": "float64", "threads": 1, "system": platform.system(), "machine": platform.machine()},
              "configuration": {"seed": 23, "window": 2, "embedding_dimension": 4, "hidden": 8, "steps": 200, "optimizer": "Adam", "lr": 0.03, "batch": len(train_events), "selection": "first minimum validation mean loss"},
              "train_events": train_events, "validation_events": validation_events, "test_events": test_events,
              "curve": curve, "selected_step": best["step"], "selected_train": best["train"], "selected_validation": best["validation"],
              "test_once_after_selection": {"count_lm": count_test, "nnlm": neural_test},
              "paper_trace": paper_trace(), "learned_vectors": learned,
              "retrieval": {"authored_static": retrieval(static["vectors"], static["dimension"], ka), "nnlm_input_mean": retrieval(learned, 4, ka)},
              "elapsed_seconds": time.perf_counter() - started}
    if write:
        (ROOT / "data/part-ii/nnlm-run.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        (ROOT / "data/part-ii/nnlm-model.json").write_text(json.dumps({"version":"nnlm-selected-v1", "license":"CC-BY-SA-4.0", "step":best["step"], "state_dict":{key:value.tolist() for key,value in best["state"].items()}},indent=2)+'\n')
    print(json.dumps({"selected_step": result["selected_step"], "train_loss": best["train"]["mean_loss"], "validation_loss": best["validation"]["mean_loss"],
                      "test": result["test_once_after_selection"], "retrieval": {key:{"success_count":value["en"]["success_count"],"predictions":[row["prediction"] for row in value["en"]["results"]]} for key,value in result["retrieval"].items()},
                      "elapsed_seconds":result["elapsed_seconds"], "paper_trace":result["paper_trace"]},indent=2))
    return result


if __name__ == "__main__":
    run(write=True)
