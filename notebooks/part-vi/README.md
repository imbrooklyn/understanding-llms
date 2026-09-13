# Part VI executed notebooks

Both notebooks use shared data and code. Implementation prose is English; textbook explanations, captions and answers have dedicated English and Chinese pages. Notebook narrative and original outputs: CC BY-SA 4.0; code cells: Apache-2.0.

1. `01-objectives-and-checkers.ipynb` reproduces serialization, masked loss, preference audit, verifier failures and all fixed budget comparisons. Its timer measures controller replay.
2. `02-ka1-and-low-rank.ipynb` re-generates the 144 actual paired KA-1 attempts, checks retained outputs and unchanged parameters, then calculates assigned low-rank and quantization examples. It does not train an adapter.

Install the pinned environment in `code/part-vi/README.md` and run `BOOK_PYTHON=/path/to/python pnpm notebooks:part-vi` from the book root. Each notebook starts in a fresh kernel, executes every code cell in order and stops on any error. Saved outputs and `data/part-vi/notebook-execution.json` are execution evidence; opening the notebook alone is not verification. No paid service or GPU is used.

