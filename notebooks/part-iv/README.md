# Part IV CPU notebooks

Read Primer-PY, then execute in order:

1. `01-attention-and-block.ipynb`: independent hand expectations, visible-key normalization and scalar block comparison for Chapters 15–17.
2. `02-tokenizer-boundaries.ipynb`: all BPE merge decisions, supplied WordPiece, exact byte round trips, invalid UTF-8 and the colon-space prefix failure for Chapter 19.
3. `03-mini-gpt.ipynb`: actual MG-1 forward and bounded MG-2 training, continuation, fresh-process repeat and all qualitative generation probes for Chapters 20–21.

Use the clean setup in `code/mini-gpt/README.md`, then run `BOOK_PYTHON=/tmp/llm-book-part-iv-venv/bin/python pnpm notebooks:part-iv` from the book root. The shared runner executes every cell in a fresh kernel for each notebook, rejects errors, and records code/input hashes and measured execution times in `data/part-iv/notebook-execution.json`. Notebook 3 creates temporary model files and leaves reference training evidence intact. A complete successful execution is required; opening the notebook is insufficient.

All implementation explanations and code comments are English. Example strings are loaded from explicit shared content/data resources. Original code: Apache-2.0; original prose, examples and measured outputs: CC BY-SA 4.0. No third-party notebook, corpus or weight is copied. The chapter figures, calculations and answers remain readable without running these notebooks.
