# SPDX-License-Identifier: Apache-2.0
"""Execute a selected part's notebooks in fresh CPU kernels using this interpreter."""
import hashlib
import argparse
import json
from pathlib import Path
import sys
import tempfile
import time
from datetime import datetime, timezone
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[2]


def run(only=None, part="part-ii"):
    if part not in {"part-ii", "part-iii", "part-iv", "part-v"}:
        raise ValueError("unsupported notebook collection")
    paths = sorted((ROOT / "notebooks" / part).glob("*.ipynb"))
    if not paths or (only is not None and only not in {path.name for path in paths}):
        raise ValueError("requested notebook collection or file is missing")
    records = []
    with tempfile.TemporaryDirectory(prefix="book-notebooks-") as temporary:
        kernel_root = Path(temporary) / "kernels"
        kernel = kernel_root / part
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Book CPU", "language": "python",
            "env": {"IPYTHONDIR": str(Path(temporary) / "ipython"), "MPLBACKEND": "Agg"}}))
        specifications = KernelSpecManager(kernel_dirs=[str(kernel_root)])
        for path in paths:
            if only is not None and path.name != only:
                continue
            notebook = nbformat.read(path, as_version=4)
            source = "\n".join(cell.source for cell in notebook.cells if cell.cell_type == "code")
            manager = KernelManager(kernel_name=part, kernel_spec_manager=specifications)
            started = time.perf_counter()
            client = NotebookClient(notebook, km=manager, timeout=180, allow_errors=False,
                                    resources={"metadata": {"path": str(ROOT)}})
            try:
                client.execute()
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
            nbformat.write(notebook, path)
            record = {"notebook": str(path.relative_to(ROOT)), "code_sha256": hashlib.sha256(source.encode()).hexdigest(),
                      "code_cells": sum(c.cell_type == "code" for c in notebook.cells),
                      "elapsed_seconds": round(time.perf_counter() - started, 4), "status": "passed"}
            records.append(record)
            print(json.dumps(record), flush=True)
    result = {"as_of": datetime.now(timezone.utc).isoformat(), "python": sys.version.split()[0],
              "condition": "fresh kernel per notebook, CPU, no allowed errors", "executions": records}
    if part == "part-iii":
        dependencies = ["code/part-iii/core.py", "code/part-ii/numerical.py",
                        "data/part-iii/sequence-v1.json", "data/part-iii/expected.json",
                        "data/part-ii/nnlm-data.json", "code/part-iii/requirements.txt"]
        result["inputs_sha256"] = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                   for name in dependencies}
    if part == "part-iv":
        dependencies = sorted(str(path.relative_to(ROOT)) for directory in ["code/part-iv", "code/mini-gpt"]
                              for path in (ROOT / directory).glob("*.py"))
        dependencies += ["code/part-iv/requirements.txt", "code/part-iv/requirements-tested.txt",
                         "data/part-iv/attention.json", "data/part-iv/tokenizer-cases.json",
                         "data/mini-gpt/corpus.json", "data/mini-gpt/config.json", "data/mini-gpt/tokenizer.json",
                         "data/mini-gpt/generation-probes.json", "data/mini-gpt/training-run.json",
                         "code/part-ii/run_notebooks.py"]
        result["inputs_sha256"] = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                   for name in dependencies}
    if part == "part-v":
        dependencies = sorted(str(path.relative_to(ROOT)) for directory in ["code/part-v", "code/mini-gpt"]
                              for path in (ROOT / directory).glob("*.py"))
        dependencies += ["code/knowledge-assistant/ka1.py", "code/knowledge-assistant/baselines.py",
                         "code/part-ii/text_processing.py", "code/part-ii/numerical.py", "code/part-ii/run_notebooks.py",
                         "code/part-v/requirements.txt", "code/part-iv/requirements-tested.txt"]
        for directory in ["data/part-v", "data/knowledge-assistant", "data/mini-gpt"]:
            dependencies += sorted(str(path.relative_to(ROOT)) for path in (ROOT / directory).glob("*.json")
                                   if path.name not in {"notebook-execution.json", "validation-manifest.json"})
        dependencies += ["data/mini-gpt/weights-selected.pt", "data/mini-gpt/weights-final.pt"]
        result["inputs_sha256"] = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                   for name in dependencies}
    if only is None:
        destination = ROOT / "data" / part / "notebook-execution.json"
        destination.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--part", choices=["part-ii", "part-iii", "part-iv", "part-v"], default="part-ii")
    parser.add_argument("--only",
                        help="Execute one practice notebook without replacing the full-suite evidence record")
    arguments = parser.parse_args()
    run(arguments.only, arguments.part)
