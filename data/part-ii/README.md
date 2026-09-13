# Part II evidence card

as_of: 2026-09-12  
last_verified: 2026-09-12

These small original fixtures are public teaching material, licensed CC BY-SA 4.0. They contain no real user records, credentials or externally executed actions. Bilingual example strings in `text-contract.json` are an explicit textbook content resource. Implementation notes and metadata are English.

| Asset | Provenance and interpretation |
| --- | --- |
| `arithmetic.json` | Author-supplied rows and weights; independent cell arithmetic, exact fractions and symbolic logarithmic expectations. Token IDs/rows retain the Part I toy-longest-v1 meanings. |
| `classifier-data.json` | Frozen `quadrants-v1`: 24 training, 48 validation and 48 test coordinate pairs; seed 1729, four decimals, four predetermined training label flips. IDs and coordinates are disjoint across splits. |
| `classifier-run.json` | Actual initial CPU run, seed 17, 600 Adam updates, all 601 train/validation observations. First minimum validation loss selects step 5; test is evaluated after selection. Runtime is a local measurement, not a benchmark. |
| `classifier-model.json` | Selected step-5 parameter arrays, original architecture and dataset hash; no optimizer-resume claim. The full training loop is reproducible from its fixed seed. |
| `text-contract.json` | Thirteen authored normalization cases, four code-point/UTF-8 traces and explicit negation/compatibility/offset losses. `search-key-v1` is for case-insensitive lexical lookup, not identity, signatures or raw-span indexing. |
| `nnlm-paper.json` | Completely supplied four-word network state, independent concatenation/probability results and reversed-context counterexample. It is not a trained model result. |
| `nnlm-data.json` | `ka-window-lm-v1`: five KA-0 canonical index-card sequences for training (20 scored events), separate validation/test variants (8 each), window 2, BOS inputs, EOS targets, nine output candidates. The eight count-LM target probabilities are independently enumerated integer fractions. A separate red/blue alphabet demonstrates identical visible windows. |
| `nnlm-run.json` | Actual seed-23 CPU training, 201 train/validation observations, selected step 10, test target probabilities and predictions. Also records every KA-0 retrieval score and ranking for authored static vectors and averaged learned input rows. |
| `nnlm-model.json` | Selected NNLM parameter arrays. Embeddings have four coordinates; this is the book's tiny NNLM, not Word2Vec or GloVe. |
| `environment.json` | Observed interpreter, platform, Unicode database, computation settings and installed versions. |
| `notebook-execution.json` | Actual fresh-kernel execution evidence for all five notebooks: UTC time, code hashes, counts, elapsed seconds and status. |

The corresponding measured scripts record hashes of their sources and principal input files. The code checks those hashes to reject stale evidence. Notebook code hashes cover all code cells in order. A software change must be followed by an actual rerun and an explicit assessment of changed results; editing expected values to match an implementation is not independent validation.

Training uses float64, CPU, one thread and deterministic PyTorch algorithms. Paper arithmetic uses absolute tolerance 1e-12. Reproduction of fixed training loss uses 1e-9 in the verified environment; cross-platform bit identity is not promised. Candidate ties take the first declared candidate (lexical ranking uses scores rounded to twelve decimals for tie comparison). Display rounding is six decimals unless a table explicitly supplies exact fractions or longer traces.

The classifier is a constructed noise/overfit diagnostic. Its clean validation/test labels intentionally differ from four corrupted training labels. The NNLM split contains recombinations of the same small vocabulary and related policy cards; it is not a document-disjoint real-world generalization study. Retrieval uses the unchanged KA-0 relevance task and denominator 9. Language prediction uses the same eight test events for both count LM and NNLM, including EOS. These metrics cannot be mixed. Repeated reproduction supplies no new test observations.

See [the continuing KA-0 data card](../knowledge-assistant/README.md), [practice instructions](../../code/part-ii/README.md), [primary-source ledger](../../docs/part-ii-research.md) and [validation record](../../docs/part-ii-validation.md).
