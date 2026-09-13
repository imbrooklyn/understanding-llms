# Part IV mechanism practice

Original code: Apache-2.0. Fixture data and diagrams: CC BY-SA 4.0. No model downloads, credentials, GPU, or paid service are needed. Read Primer-PY before running the practice; all central values and answers are already visible in the textbook.

Run from the book repository root with Python 3.12. A fresh environment avoids mixing an existing project's packages:

```sh
python3.12 -m venv /tmp/llm-book-part-iv-venv
/tmp/llm-book-part-iv-venv/bin/python -m pip install -r code/part-iv/requirements.txt
/tmp/llm-book-part-iv-venv/bin/python code/part-iv/run.py
```

`--write` deliberately replaces only `data/part-iv/numpy-run.json`, never the independent expectations. `mechanisms.py` exposes projections, row Softmax, a mask with explicit visible=True semantics, two-head concatenation/output projection, coordinate LayerNorm and a pre-norm block. It is small verification code, not an optimized library. Float64 absolute comparison tolerance is 1e-12; displayed chapter values are rounded to six decimals.

The continuing language-model project is in `code/mini-gpt/`; its tokenizer/corpus/model configuration remains the same between MG-1 and MG-2. The installation and measured environment are documented in `docs/part-iv-validation.md`. `requirements.txt` declares the requested direct versions; the actual complete environment is recorded after clean installation. Installation requires network access once; computations use local data thereafter.
