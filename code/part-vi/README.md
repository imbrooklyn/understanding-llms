# Part VI CPU practice

Code: Apache-2.0. As of / last verified: 2026-09-13. No core exercise needs a GPU, API key or model account. Primer-PY is the programming prerequisite; the complete mechanisms/results/answers are also static in both language pages.

From the book root:

```sh
python3.12 -m venv /tmp/llm-book-part-vi-venv
/tmp/llm-book-part-vi-venv/bin/python -m pip install -r code/part-vi/requirements.txt
BOOK_PYTHON=/tmp/llm-book-part-vi-venv/bin/python pnpm test:part-vi:cpu
BOOK_PYTHON=/tmp/llm-book-part-vi-venv/bin/python pnpm notebooks:part-vi
/tmp/llm-book-part-vi-venv/bin/python code/part-vi/run.py
/tmp/llm-book-part-vi-venv/bin/python code/knowledge-assistant/format_adaptation.py
```

`core.py` uses the standard library. It serializes a narrow teaching chat template, computes masked losses and preference quantities, checks the declared amount grammar, replays budgeted selectors and multiplies low-rank matrices. The preference audit operates on explicit structured scope/amount metadata; it is not an automated natural-language rubric judge. Step candidates use the exact grammar `digits + digits = digits`; the selector extracts the final amount from text and the verifier recomputes the required amount from the task. It does not read the stored gold label to choose a candidate.

`run.py` checks independent expectations before optionally writing a mechanism record with `--write`. Normal use verifies a fresh replay without replacing evidence. The KA-1 runner similarly replays its immutable freeze and refuses to overwrite an existing run. It uses the shared Mini GPT, tokenizer, checkpoint and lexical baselines; no duplicate assistant implementation is created.

`run_notebooks.py` gives each notebook a fresh kernel using the selected interpreter. It fails on cell errors and writes executed outputs plus a provenance record only after execution. The older parts' notebook runners and measured source hashes remain untouched. The pinned tested stack is inherited from Part IV: Python 3.12.10 was used here with PyTorch 2.7.0, NumPy 2.0.2, nbclient 0.10.2, nbformat 5.10.4 and ipykernel 6.29.5. Model comparison is one-thread CPU float64; arithmetic replay uses Python integers and binary64.

## Optional parameter training

Installed distribution license metadata and exact license-file hashes are recorded in `data/part-vi/dependency-licenses.json`. PyTorch and the notebook packages declare BSD licenses; NumPy's recorded wheel license also contains bundled-component terms. These dependencies are not vendored by this increment and retain their own licenses.

No parameter training is needed for this delivery and no PEFT training result is reported. The matrix exercise is an executed arithmetic demonstration with assigned factors. A future external-model experiment must separately record the base repository and exact revision, model/tokenizer/template versions, license text and redistribution terms, data origin/license, adaptation objective, trainable parameter names, quantization settings, seeds, resource budget and held-out/retention outcomes. A code library license does not determine a checkpoint or dataset license; an adapter does not remove the base model's conditions.

Do not treat a uniform scalar quantization exercise as QLoRA, or the seven assigned numbers as learned weights. Full updates, LoRA and QLoRA must be compared under the same declared data/objective and evaluation contract, with tuning and runtime costs disclosed.
