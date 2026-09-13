# Part IV fixture card

Version: `part-iv-v1`. Author: Understanding LLMs contributors. Original synthetic teaching data and computed numerical traces: CC BY-SA 4.0. No third-party dataset, private information, real order, external action, or pretrained weight is included.

- `attention.json`: author-chosen X and three W matrices; explicit position order; hand-expanded integer products; independently evaluated symbolic row ratios; full-precision expected values. These are not trained embeddings or measured language competence.
- `numpy-run.json`: actual float64 NumPy execution, with runtime versions, full intermediate matrices, absolute deviations from the independent attention expectations, causal masks, two-head and single-block traces. Regenerate using `python code/part-iv/run.py --write`. A trace alone is not an independent expected value; independent behavior tests accompany it.

Rows mean receiving queries, columns mean contributing keys. Scores are dimensionless, probabilities sum over visible keys, and displayed values are rounded to six decimal places. A valid all-masked row is an error. A padded query is explicitly excluded and receives a zero mixture. Identifiers in these files support auditing; reader tables use natural example/figure/table numbers.

The continuing Mini GPT dataset and tokenizer live in `data/mini-gpt/`, not in a separate copy for each chapter. Its card records the split, text boundaries, byte alphabet, special IDs, normalization, versions, seeds, loss units, and measured-run provenance.

- `mask-cases.json`: explicit causal/padding visibility, an author-constructed future-copy oracle with independent 0.995 versus 0.5 target probabilities, and the two-head concatenation/output-projection expectations. These are constructed evidence under stated rules, not trained accuracy.
- `architectures.json`: original whole-word teaching inputs, targets and all allowed position relations for BERT/GPT/T5 comparisons. Boundary simplifications are declared; the matrices are not library tokenizer outputs or a benchmark.
- `tokenizer-cases.json`: complete hand-BPE corpus/rules and independent expected merges, supplied WordPiece vocabulary and whole-word unknown examples, exact round-trip strings and a normalization counterexample.
- `tokenizer-run.json`: all pair counts at every hand merge, actual Mini GPT tokenizer IDs and UTF-8/code-point/token lengths for the same strings, WordPiece results and explicit lossy-normalization evidence.
- `content-contract.json`: bilingual validation labels and key static-evidence requirements. These are content resources, not model inputs.
- `notebook-execution.json`: actual fresh-kernel execution counts, durations, code hashes and imported input/source hashes. It is generated only after complete successful execution, not inferred from a notebook opening.

Source and artifact hashes in `validation-manifest.json` bind the mechanism/tokenizer evidence to its inputs and implementation. They detect stale records, while independent math and behavior checks establish the intended operations. The core implementation, normalized scalar-loop reference and unit tests are separately readable under `code/part-iv/`.
