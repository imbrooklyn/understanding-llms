# KA-1 selection report

`as_of: 2026-09-13`  
`last_verified: 2026-09-13`  
Decision: reject both measured configurations for the specified bilingual Knowledge Assistant. Retain the validation-selected checkpoint for its existing educational use. This is a completed configuration-selection decision, with no product release or external-model recommendation.

## Contract and provenance

The frozen `data/knowledge-assistant/ka1-contract-v1.json` defines six compact evidence-conditioned answer cases in each language: current lodging amount, stale-premise correction, historical amount, fictional order status, approval boundary and unknown policy. It inherits all five documents, nine queries and Keyword/BoW Count/TF-IDF baselines from KA-0 without deleting difficult queries. Answer and retrieval metrics remain separate. The companion `ka1-provenance-note-v1.json` corrects an overbroad source-attribution sentence in the frozen metadata: D defines a possible status, while KA-1 assigns processing to a new fictional short label A104; no-granted-approval is also an added condition. Document links are conceptual provenance, not live status evidence. The original frozen bytes, prompts, rubric and results are unchanged. Cases, rubric, candidates, adaptation, seeds and source identities were frozen at 2026-09-13T04:35:44.060022+00:00, before the measured run at 2026-09-13T04:38:23.958253+00:00.

| Identity | Value |
| --- | --- |
| A | MG-2 validation-selected step 50, `weights-selected.pt` |
| A SHA-256 | `02abe42d897c83cc39a2bfb720642a6de8caef4200b3f421a7840fe0429fadfc` |
| B | MG-2 final step 600, `weights-final.pt` |
| B SHA-256 | `a8ffef09fc809cf06330972037169738ebc26730f5a62e22802d073e47b13271` |
| Tokenizer semantic SHA-256 | `9bb146ce375bda3aa518a48a60d9f69611b8d0afde9df9a8298eae9dfa9dd354` |
| Structure | Same 13,875 parameters, one causal block, 64-position context and byte-BPE tokenizer |
| Runtime | Python 3.12.10; PyTorch 2.7.0; CPU float64; one thread; arm64 macOS 26.5.2 |
| Primary policy | Greedy; fixed token-ID tie order; seeds 7, 42, 31415; maximum 24 new tokens |
| Stress policy | Temperature 0.7, top-k 5; same seeds and budget |
| Timing | Complete warm generation call including full trace collection and byte decoding; two warmups per candidate; loading excluded; no KV cache or network |

The pre-run freeze, raw run and review each retain hashes to their actual inputs. Model tensors occupy 111,000 bytes per candidate; this is not process peak memory. The shared code/dataset licenses are recorded per asset: original implementation Apache-2.0; original corpus, snapshots, reports and records CC BY-SA 4.0. Dependencies retain their own licenses.

## Same-contract observations

A robust case must satisfy the semantic rubric on all three primary repeats. The gate requires all six cases in **each** language; current-policy and approval failures are disqualifying. The 1,000 ms p95 complete-call limit is only a diagnostic latency gate. Passing it would not establish a service SLO. Eighteen repeats do not become eighteen independent scenarios.

| Primary group | Strict passes / 18 | Semantic passes / 18 | Robust cases / 6 | Median ms | Nearest-rank p95 ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| A English | 0 | 6 | 2 | 0.718167 | 0.983209 |
| A Chinese | 0 | 0 | 0 | 1.376146 | 2.230083 |
| B English | 0 | 0 | 0 | 1.5149585 | 5.475667 |
| B Chinese | 0 | 0 | 0 | 1.023396 | 5.160334 |

The semantic review is disclosed AI-assisted author inspection of all 62 unique case/locale/completion/UTF-8 combinations, propagated to their identical attempts. It is neither an independent human panel nor a calibrated model-judge experiment. Reasons and failure tags are visible in `ka1-adjudication-v1.json`; Chapters 32–33 print the rubric, calibration counterexamples and all distinct primary responses in both languages. A's `750.` is correct on two English current-amount cases despite strict punctuation mismatch, but wrong on historical 600. B's numeric prefixes occur in unintelligible complete responses. No favorable substring is substituted for the whole answer.

All 144 attempts remain recorded. There are no runner exceptions. One B English stress response contains invalid UTF-8; bytes and replacement display are preserved. The stress policy yields A only one semantic English pass in 18 attempts and no robust case; other stress groups have none. EOS, token-budget and context-limit stops are separately retained, including approval failures. The code performs no cancellation or other order action.

All nine inherited retrieval queries ran in both languages: Keyword 5/9, BoW Count 6/9, TF-IDF 7/9. These document-selection results are unchanged and are not pooled with generated-answer metrics.

## Tradeoffs and decision

| Dimension | Evidence | Consequence |
| --- | --- | --- |
| Ability and languages | Complete paired run, strict detector, disclosed rubric review | Both fail the bilingual quality gates; A's relative advantage cannot qualify it |
| Latency | Actual warm complete calls above | Tiny outputs and trace collection differ from production streaming; no measured TTFT/TPOT or concurrency |
| Cost | No paid API requests; tensor byte count | Hardware, electricity, idle capacity and labor remain unmeasured |
| Privacy | Local runner reads local synthetic fixtures/weights; no service calls | No external prompt path in this run; no deployed logging/access-control audit |
| Licensing | Original per-asset licenses, retained provenance | Code license does not automatically relicense data or snapshots |
| Availability | Successful local replay from retained files | No uptime, failover, load or regional-service eligibility claim |
| Maintenance | Small shared implementation, fixed dependencies, tests and hashes | Dependency updates, monitoring, recovery and data ownership remain operational obligations |

Hard gates precede weighted preferences. Both candidates are rejected for the assistant use. The report's assigned cost illustration assumes *other, already-qualified* hypothetical candidates: USD 0.004/request for an API versus USD 20/month plus 0.001/request locally. Its 6,667-request whole-number crossover is arithmetic under assumptions, not a measured local price or a reason to override quality failure.

## Separate dated documentary layer

`data/part-v/external-candidates-2026-09-13.json` records official Claude Haiku 4.5 and Qwen2.5-0.5B-Instruct model/config/license/price/terms observations, full source links and unresolved conditions. Neither candidate was downloaded or executed. Claude's listed base rates imply USD 0.002 for the assigned 1,000-input/200-output request before other charges; no invoice or access test exists. The inspected API availability list does not include mainland China. Qwen's inspected per-file change hashes do not pin the complete current weight/tokenizer repository. Open weights and an OSI Open Source AI compliance determination are separate questions. See the actual source sections and boundaries in `docs/part-v-research.md` and the dated section of Chapter 33.

## Reproduction and reconsideration

From the repository root, follow `code/part-v/README.md` to install the pinned CPU environment, then run:

```sh
BOOK_PYTHON=/path/to/tested/python pnpm test:part-v:cpu
BOOK_PYTHON=/path/to/tested/python pnpm notebooks:part-v
pnpm validate:part-v
```

The tests/notebooks execute the full paired comparison without replacing historical raw timing or review files. Token IDs, outputs, bytes, stops, UTF-8 status and retrieval behavior are compared; elapsed times are allowed to vary. All data/model/tokenizer/code identities needed for replay are retained in the JSON evidence. The chapters are fully static and do not require execution to understand the rejection.

Reconsideration requires an appropriate candidate and a newly frozen run under unchanged or explicitly versioned criteria. Production acceptance would additionally require realistic document lengths/citations, unused representative bilingual cases, independent human review, sustained load/tail latency, privacy controls and operational recovery evidence. No paid API/GPU run, external candidate benchmark, human-panel trial or deployment is claimed.
