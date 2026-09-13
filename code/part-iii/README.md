# Part III CPU sequence practice

As of / last verified: 2026-09-12. Code: Apache-2.0. Chapter and notebook prose, figures, and original fixed data: CC BY-SA 4.0. Prerequisite: the completed Python primer, then Chapters 11–14 in order. Core reading does not require running code.

`core.py` reuses Part II's `numerical.py` matrix, dot-product, distribution, and stable Softmax primitives. It implements a state-by-state RNN log, the same-task two-token baseline, scalar BPTT, gate arithmetic, a complete supplied conditional translation trace, and cross-attention with two explicitly different deletion procedures. `test_core.py` uses frozen fractions, a closed-form polynomial and finite differences, state collision and tie behavior, stopping, normalization invariants, and intervention differences. No model is fitted and no outside action is performed.

Run the dependency-free core from the book root:

```bash
python3 code/part-iii/run.py
python3 -m unittest discover -s code/part-iii -p test_core.py -v
```

Use `--record` with `run.py` only when intentionally refreshing the saved evidence; its output records versions and hashes. The nine-token color task is imported from the existing Chapter 10 data, with a hash check that requires review when the source changes. Output candidate order is fixed and ties select the first candidate. Every independent sequence starts from its declared initial state.

## Fresh CPU notebook environment

The core uses Python's standard library only. The notebooks were executed with Python 3.12.10; the optional matrix cross-check uses NumPy 2.0.2. These are reproducibility pins, not claims about the latest releases. No GPU library, model account, tokenizer download, or paid API is required. The initial dependency installation requires network access unless wheels are already cached.

```bash
python3.12 -m venv /tmp/llm-book-part-iii-venv
/tmp/llm-book-part-iii-venv/bin/python -m pip install -r code/part-iii/requirements.txt
BOOK_PYTHON=/tmp/llm-book-part-iii-venv/bin/python pnpm test:part-iii:cpu
BOOK_PYTHON=/tmp/llm-book-part-iii-venv/bin/python pnpm notebooks:part-iii
```

The notebook runner is the existing `code/part-ii/run_notebooks.py`, extended with `--part part-iii`; its default remains Part II. It creates a fresh CPU kernel for each notebook, allows no cell errors, preserves outputs, and writes evidence only after the complete collection succeeds. It needs local kernel sockets. Opening the file alone is not an execution check.

`01-state-and-gradient.ipynb` contains the complete RNN failure, shared-weight gradient, distance table, and gate examples. `02-seq2seq-attention.ipynb` contains both target timelines, both queries, both deletion procedures, an optional NumPy recomputation, and the empty-memory boundary. Each includes a transfer check and a visible explanation. The tested environment's full package list is in `data/part-iii/environment.txt`.

## What the results establish

A calculated state is not a supplied gate activation; a supplied conditional decoder table is not a trained decoder. The saved CPU output establishes that this implementation reproduces the declared fixtures. It does not establish translation quality, measured RNN/GRU/LSTM performance, ELMo training, or arbitrary-distance retention. The fixed queries do not imply a learned decoder state trajectory. Chapter 14's readout is a scalar diagnostic, not a word probability.

Official implementation references checked on 2026-09-12: [NumPy 2.0 matrix multiplication](https://numpy.org/doc/2.0/reference/generated/numpy.matmul.html) for the optional matrix path, and [NBClient execution](https://nbclient.readthedocs.io/en/latest/client.html) for fresh-kernel execution, errors, and output persistence. Core mechanism sources and their limits are in `docs/part-iii-research.md`.
