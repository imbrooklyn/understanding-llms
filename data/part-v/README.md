# Part V evidence

`as_of: 2026-09-13`

All original fixtures, annotations and recorded outputs in this directory are CC BY-SA 4.0. No third-party model weights, corpus or figures are redistributed here. Source metadata link to third-party materials under their own terms. Code is separately Apache-2.0. Localized textbook strings and prompts live in the JSON content resources, not implementation comments.

| File | Evidence class and purpose |
| --- | --- |
| `lifecycle-card.json` | Author-assigned, vendor-neutral lifecycle claims; no measured model release |
| `pipeline-input.json` | Eight original HTML records and explicit filtering/redaction/deduplication rules; all addresses and accounts fictional |
| `mechanisms.json` | Assigned budgets, component matrices, resource dimensions, intervention states, generation rules and single/multiple-request timestamps |
| `expected.json` | Independent integer products, exact fractions and symbolic expectations established before the scalar implementation |
| `derived-run.json` | Actual CPU recomputation of the assigned fixtures, with code/input hashes; these are **derived teaching results**, not hardware or model-quality measurements |
| `modern-config.json` | Book-owned explanatory schema; it is not a promise that a particular engine accepts these field names |
| `generation-tasks.json` | Frozen bilingual tasks, checkpoint, candidate policies, seeds and stopping budget |
| `generation-run.json` | All 36 actual final-checkpoint continuations and complete step traces, including IDs, probabilities, byte representation, stops and UTF-8 status |
| `external-candidates-2026-09-13.json` | Official-source documentary inspection with dates and unresolved conditions; neither external candidate was run |
| `content-contract.json` | Explicit bilingual headings/captions and key evidence markers for content/browser validation |
| `notebook-execution.json` | Actual fresh-kernel execution records, code-cell and input hashes; generated only after execution |
| `verification/` | Actual acceptance logs, source-preservation and composed-output checks; separate from model measurements |

The shared projects remain in `data/mini-gpt/` and `data/knowledge-assistant/`. Their `data-card-v2.json` files add provenance without changing the original corpus or KA-0 fixture. KA-1 inherits all nine queries and all three lexical baselines. Its contract, pre-run freeze, 144 attempts, review reasons, calibration and dated source-attribution correction (`ka1-provenance-note-v1.json`) stay beside KA-0. See [the selection report](../../docs/ka1-selection-report.md).

Generation uses candidate token-ID order, CPU float64, one thread, and the existing MG-2 implementation. Assigned scalar sampling uses Paris, Lyon, red, EOS in that order; sorted ties retain original order, top-p keeps the smallest prefix with cumulative mass at least p, and draws use left-closed/right-open intervals. Quantization uses nearest-even ties and clipping. JSON keeps full Python numeric representations; chapter displays round explicitly. Decimal byte units and binary MiB are distinguished in the chapters.

To reproduce without replacing historical model measurements, run the CPU tests or notebooks in [the practice instructions](../../code/part-v/README.md). `--write` is an explicit authoring operation: changing a historical run also invalidates downstream reviews and hashes. Create a new version for a new task or candidate rather than silently replacing an unfavorable result.
