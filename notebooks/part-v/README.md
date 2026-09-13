# Part V notebooks

Text and outputs: CC BY-SA 4.0. Code cells: Apache-2.0. Implementation explanations are English; displayed bilingual examples are loaded from shared content resources.

| Notebook | Prerequisites | Executed work |
| --- | --- | --- |
| `01-resources-and-mechanisms.ipynb` | Primer-PY, Chapters 23–31 | Recompute pipeline counts, budgets, block components, intervention controls, sampling, KV memory, quantization and serving metrics; test changed conditions |
| `02-generation-matrix.ipynb` | Primer-PY, MG-2, Chapter 29 | Execute all 36 fixed CPU continuations and compare their full traces against the retained evidence |
| `03-ka1-comparison.ipynb` | Primer-PY, KA-0, MG-2, Chapters 32–33 | Execute all 144 paired attempts and inherited retrieval baselines; inspect calibration/review and reproduce the rejection decision |

Use `BOOK_PYTHON=/path/to/tested/python pnpm notebooks:part-v` from the repository root after following `code/part-v/README.md`. Each notebook receives a fresh CPU kernel with no allowed errors. The runner saves executed outputs and `data/part-v/notebook-execution.json` with exact source/input identities. Opening a notebook is not counted as executing it. The historical generation/KA-1 files and model snapshots are never rewritten by these notebooks.

The chapters show the complete mechanisms and decision evidence statically. Running notebooks provides an additional reproducibility path, not access to hidden answers. No live API, GPU, external model download or action execution is needed.
