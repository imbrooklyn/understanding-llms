# Part VII evidence records

Original fictional data and educational records: CC BY-SA 4.0. No third-party dataset or user account is included. The continuing inputs live in `data/knowledge-assistant/`; this directory contains derived execution evidence and independent expected values.

- `inherited-freeze-v1.json`: hashes of retained KA-0, learned NNLM, KA-1 and format-adaptation artifacts. No unfavorable case is removed.
- `expected-v1.json`: independently derived arithmetic and finite-case expectations. Decimal and binomial calculations in the tests use another path from the general implementation.
- `context-run.json`, `schema-run.json`: actual KA-2 serialization and validation, with authored fault inputs identified.
- `tool-run.json`, `http-run.json`, `mcp-run.json`: actual local execution paths. The direct timeout is injected; HTTP timeout is exercised against a delayed loopback server. The MCP record is actual subprocess stdio. None is a model decision experiment.
- `retrieval-run.json`: complete unchanged-card comparisons, full score orders, positive returned lists, gold labels and metric denominators. Float64 calculation, scores rounded to 12 decimals for stable A–E ties, six decimals for chapter display; no random retrieval seed is needed.
- `rag-traces.json`: canonical bilingual source → chunk/card → metadata/index → retrieval → context → local extractive composition → citation/abstention traces.
- `eval-run.json`: 12 semantic development cases × 2 languages × 3 repeats × 2 conditions = 144 actual deterministic executions. Only preselection eligibility filtering changes. Both conditions retain identical sibling-conflict expansion and support gates. Expected safe abstentions are distinguished from unanswered answerable tasks.
- `ablations-run.json`: separate rewrite, parent expansion and exact-line compression probes. The irrelevant filing-note variant never replaces the frozen corpus. These results are not combined into the primary comparison.
- `run-manifest.json`, `notebook-execution.json`: actual dates, interpreter/platform, source/output hashes and fresh-kernel execution evidence. Duration is local wall-clock evidence, not a model benchmark.
- `browser-validation.json`: completed local build/browser outcomes, final page/renderer/workflow hashes, log hashes and manual visual-review scope. The full suite, final Part VII rerun and production-only run are distinct checks; no hosted workflow or deployment is implied.

The bootstrap unit is a semantic case; translations and repeated deterministic runs are clustered. Exact convolution over the observed paired differences yields the percentile interval. This conditional development-set resampling does not establish deployment confidence. Source support is checked only for the declared exact-source claim format, not arbitrary natural-language entailment.
