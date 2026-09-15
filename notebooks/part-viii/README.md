# Part VIII CPU notebooks

Run `BOOK_PYTHON=/path/to/python pnpm notebooks:part-viii` from the repository root after installing the shared requirements. The runner supplies a fresh kernel per notebook and records complete execution in `data/part-viii/notebook-execution.json`.

1. `01-workflow-recovery.ipynb`: finite workflow, source Skill loading/helper, real SQLite close/reopen recovery, read-only replay and approval matrix.
2. `02-evaluation-governance-security.ipynb`: equal-score attribution, raw Judge/human comparison, independent confusion arithmetic, local adverse proposals, minimization/deletion/expiry, copied-byte integrity and saved OS evidence.

All key results and reference answers are also visible in Chapters 47–53 without running these notebooks. Implementation prose is English. Bilingual textbook strings live in the shared content resources. Original prose is CC BY-SA 4.0; code is Apache-2.0. The attributed human-reference source text is CC BY 4.0, as documented in `data/part-viii/README.md`.
