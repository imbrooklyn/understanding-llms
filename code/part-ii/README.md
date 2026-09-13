# Part II CPU practice

as_of: 2026-09-12  
last_verified: 2026-09-12

Read Chapter 5 core, then the bilingual Python primer. Run the character N-gram bridge before the NumPy shapes exercise, and complete Chapter 6 before the training practice. All core explanations, calculations, comparisons and answers are static in the chapters. No GPU, model account, API key or external order system is used.

## Reproduce the environment

From the book repository root, use Python 3.12 and a new virtual environment:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r code/part-ii/requirements.txt
BOOK_PYTHON=.venv/bin/python pnpm test:cpu
.venv/bin/python code/part-ii/run_notebooks.py
pnpm ci:build
```

The recorded run used a newly created environment in a temporary directory, Python 3.12.10, NumPy 2.0.2, PyTorch 2.7.0, float64, one PyTorch CPU thread, macOS arm64. The direct pins are in `requirements.txt`; `requirements-tested.txt` and `data/part-ii/environment.json` record the complete observed package set. The latter is an environment record, not a claim of a universal cross-platform lock. A Linux PyTorch installation can select the CPU wheel from the official PyTorch CPU package index; no GPU computation is required. Windows, Linux, hosted notebooks and GPU execution were not used for this revision's measured results.

The notebook runner creates a temporary kernel specification using its own interpreter and starts a fresh kernel for each notebook. It allows no error outputs, shuts down each kernel, writes executed notebooks and records their code hashes, cell counts and actual elapsed times in `data/part-ii/notebook-execution.json`. Jupyter uses local loopback sockets; a restricted process sandbox may need permission for that local IPC. A notebook that only opens is not a completed run.

Readers can add `--only 01-primer-and-ngram.ipynb` to run the first notebook after the primer, and choose later filenames after their chapters. A single-notebook run saves that notebook but does not replace the aggregate full-suite evidence. Omitting `--only` executes all five for author verification.

## Programs and evidence

| Program | Input and observable result |
| --- | --- |
| `ngram.py` | Reads unchanged `data/part-i/ngram.json` and independent `expected.json`; changes order 1–3 and smoothing 0/1, checks all six diagnostics, sequence boundaries and exact LCG32 draws. MG-0 remains a project milestone. |
| `numerical.py`, `shape_practice.py` | Explicit dot/MatMul/cosine and NumPy batch arithmetic; detects shape-compatible axis changes; padding means have different denominators. |
| `probability_practice.py` | Fixed logits, shift invariance, target loss, perplexity, directional KL, mathematical support zeros and numerical underflow. |
| `text_processing.py` | Pure `search_key(raw)` with NFC, casefold, NFC and whitespace collapse; returns a string or raises a documented type error. Bilingual strings are read from the content fixture. |
| `classifier.py` | Hand-derived SGD update plus seeded 2→32→32→2 classifier. Fits training data, selects by validation loss, then scores test data. Saves curve and selected state when invoked as a script. |
| `nnlm.py` | Supplied paper trace; seeded window-2, 4-dimensional NNLM; count-LM target fractions; separate retrieval reuse of input embeddings. Saves actual run and selected state when invoked as a script. |

To reproduce saved result files, run `classifier.py`, `../knowledge-assistant/baselines.py` and `nnlm.py` by their repository-relative paths. Their Python `run(write=False)` entry points perform the same work without replacing the recorded experiment. Reproduction can change elapsed time and software metadata. Numerical expectations use unrounded values; the paper arithmetic tolerance is 1e-12 and the fixed CPU-training comparison tolerance is 1e-9. Displayed tables generally round to six decimals. Do not tune on the retained test results or replace unfavorable examples.

`make_classifier_data.py` documents the original generator. Ordinary reproduction reads the frozen fixture; generating a new dataset version is a separate authoring change. `data/knowledge-assistant/ka0-v1.json` belongs to one continuing cross-part knowledge-assistant project.

## Checks and licenses

`pnpm validate:part-ii`, included in `pnpm ci:build`, checks bilingual structures, formulas, citations, static assets, completed notebook evidence and the dependency-free `test_core.py` behaviors. It can use `BOOK_PYTHON` or system `python3`. `BOOK_PYTHON=.venv/bin/python pnpm test:cpu` runs `test_cpu.py`, including real classifier and NNLM training, independent finite differences, model reloads and information-loss counterexamples. Notebook execution is a separate explicit command because it writes outputs and needs a kernel environment. Browser coverage is in `tests/part-ii.browser.ts` and the standard `pnpm test:browser` entry.

Original Python code is Apache-2.0. Original chapter prose, fixture values, diagrams, derived tables and saved model parameters are CC BY-SA 4.0. Notebook code is Apache-2.0; original explanatory Markdown is CC BY-SA 4.0. No third-party corpus, pretrained weights or paper figure is redistributed. NumPy, PyTorch and the Jupyter packages retain their own licenses; their installed metadata was inspected (BSD-family licenses, with additional wheel notices where applicable). Installing a dependency does not relicense it under the book's license.
