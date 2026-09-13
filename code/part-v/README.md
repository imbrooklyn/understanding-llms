# Part V CPU practice

Read Primer-PY and the relevant chapters first; MG-2 and KA-0 are implemented prerequisites. Core reading requires no programming, GPU, paid service or model account. This directory adds small mechanisms and generation-policy comparisons; KA-1 itself extends `code/knowledge-assistant/ka1.py` and imports the existing Mini GPT. It does not create a second assistant project.

Original code and comments: Apache-2.0. Text: CC BY-SA 4.0. Prompts, bilingual labels and examples are in versioned data resources. No executable here calls an external model service or performs an order operation.

Run from the book repository root. A clean CPU environment was tested with Python 3.12.10, PyTorch 2.7.0 and NumPy 2.0.2 on arm64 macOS. `requirements.txt` reuses the exact tested Part IV dependency set, including notebook packages.

```sh
python3.12 -m venv /tmp/llm-book-part-v
/tmp/llm-book-part-v/bin/python -m pip install -r code/part-v/requirements.txt
BOOK_PYTHON=/tmp/llm-book-part-v/bin/python pnpm test:part-v:cpu
BOOK_PYTHON=/tmp/llm-book-part-v/bin/python pnpm notebooks:part-v
pnpm validate:part-v
```

Jupyter needs local loopback sockets to connect each fresh kernel. The notebook runner closes its kernels and uses a temporary kernel specification. A restricted environment must permit that local operation. Dependency installation needs package-network access once; subsequent core runs use retained local files.

`mechanisms.py` contains scalar calculations. `run.py` reads assigned inputs and derives counts, distributions, quantization errors, intervention margins and trace metrics. No GPU speed is inferred from this script's runtime.

```sh
/tmp/llm-book-part-v/bin/python code/part-v/run.py
/tmp/llm-book-part-v/bin/python code/part-v/generation_matrix.py
/tmp/llm-book-part-v/bin/python code/knowledge-assistant/ka1.py
```

These commands do not overwrite retained results. `run.py --write` refreshes derived teaching evidence. The generation and KA-1 `--write` options are intended only for explicitly versioned authoring runs: raw timing is a historical measurement, and changing it invalidates review and notebook provenance. Tests compare observable token IDs, complete bytes, stops and UTF-8 failures, not elapsed-time identity. Floating-point/cross-stack reproducibility is not guaranteed.

`test_mechanisms.py` checks independent fractions and changed conditions: sampler boundary/tie behavior, zero denominators, invalid dimensions, offset-sensitive normalization, signed gates, unequal microbatch weights, control patches, beam joint probability, cache growth, one-output latency, quantizer clipping/ties, finite-workload versus fixed-window throughput, speculative residual correction and pipeline mutations. `test_ka1.py` executes the entire paired CPU comparison again and verifies source identity, complete row coverage, retained failures and inherited retrieval behavior. The import harness uses explicit file paths to disambiguate the several project `run.py` modules.

See [the evidence inventory](../../data/part-v/README.md), [notebook guide](../../notebooks/part-v/README.md) and [KA-1 report](../../docs/ka1-selection-report.md). Actual commands, outcomes and remaining limits belong in [Part V validation](../../docs/part-v-validation.md).
