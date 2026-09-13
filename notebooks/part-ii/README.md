# Part II notebooks

as_of: 2026-09-12  
last_verified: 2026-09-12

Read Chapter 5 core and Primer-PY first. Follow this order:

1. `01-primer-and-ngram.ipynb`: Python values, loops, functions/errors and the deferred Chapter 4 order/smoothing comparison against unchanged Part I expectations.
2. `02-shapes-and-loss.ipynb`: NumPy axes and padding; after Chapter 6, stable probability/loss arithmetic and a separate PyTorch cross-entropy calculation.
3. `03-training.ipynb`: one complete SGD step, then actual seeded classifier fitting, validation selection and test evaluation.
4. `04-text-and-ka0.ipynb`: bilingual normalization contract, offset failure and all three lexical baselines; a corpus-change exercise does not overwrite v1.
5. `05-representations-and-nnlm.ipynb`: supplied paper trace, actual NNLM training, same-collection retrieval, separate continuation metrics and identical-window failure.

Each notebook includes visible outputs and reference checks. The code reads shared implementation and fixtures instead of duplicating them. English Markdown describes implementation; bilingual strings are imported from clearly identified content resources. Core textbook mechanisms and solutions remain directly readable on the static pages.

Use the [CPU setup instructions](../../code/part-ii/README.md), then run `python code/part-ii/run_notebooks.py` with that environment's interpreter. It executes every code cell from a fresh kernel with no allowed errors, saves outputs and writes `data/part-ii/notebook-execution.json`. The notebook validator checks source hashes and consecutive execution counts. Opening a notebook or reusing an old kernel does not satisfy this verification.

Code cells are Apache-2.0. Original explanatory Markdown and original teaching inputs/outputs are CC BY-SA 4.0. Imported libraries retain their own licenses. These notebooks use CPU only and perform no live account or order actions. A cloud notebook environment has not been verified for this revision.
