# Continuing knowledge-assistant project

Original code, Apache-2.0. `baselines.py` is KA-0: dependency-free Keyword, BoW Count and TF-IDF retrieval over the same versioned bilingual collection. Shared text processing lives in `code/part-ii/text_processing.py`; localized strings live in `data/knowledge-assistant/ka0-v1.json`. No external service is contacted.

From the book repository root:

```sh
python3 code/knowledge-assistant/baselines.py
pnpm validate:part-ii
```

The script writes complete deterministic results to `data/knowledge-assistant/ka0-lexical-run.json`. Call `run(write=False)` to inspect a reproduction without replacing that record. `run_locale`, `count_vector`, `rank` and `evaluate_vectors` expose the same contract to the later static/NNLM comparison. Future parts should extend this project while retaining the frozen collection and three lexical baselines.

For the precise indexing scope, relevance labels, candidate order, TF/IDF definition, abstention rule, versioning and failure taxonomy, read [the data card](../../data/knowledge-assistant/README.md). For pinned training dependencies and the later representation comparison, read [Part II practice](../part-ii/README.md). The retrieval output is a ranked source and optional top-one prediction, not a generated answer, live order status or authorization to act.

## Part VI runtime-format increment

`format_adaptation.py` reuses the frozen KA-1 inputs, the same Mini GPT/checkpoints and the same lexical baselines. It compares each actual generation with a terminal-period-only amount normalization, without changing parameters or the judge. The original contract and unfavorable responses remain intact.

Run `python code/knowledge-assistant/format_adaptation.py` from the book root in the [Part VI CPU environment](../part-vi/README.md). Normal replay checks input hashes and exact raw output reproduction; it does not overwrite the retained freeze/run. The complete comparison is in `data/knowledge-assistant/ka1-format-run-v1.json` and [the adaptation decision](../../docs/ka1-adaptation-report.md). Formatting improves a narrow strict score, while semantic gates still reject both checkpoints. No RAG interface, live tool, cancellation or parameter training is implemented by this increment.
