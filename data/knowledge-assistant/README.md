# Knowledge assistant: frozen KA-0 collection

as_of: 2026-09-12  
last_verified: 2026-09-12

`ka0-v1.json` is the first immutable query/document/relevance contract for the continuing knowledge-assistant project. Later parts should add explicitly versioned fields or successor datasets here, retain v1 and all three lexical results, and explain any version mapping. Do not create separate assistants for each part. All text is original fictional textbook content, CC BY-SA 4.0; English and Chinese strings are centralized bilingual resources, not translated inside implementation code.

## Document and query contract

The five candidate IDs, in tie-breaking order, are `travel-v1`, `travel-v2`, `rail-faq-v1`, `status-faq-v1`, `approval-faq-v1`. The chapters abbreviate them A–E. The old travel policy is archived at 600 yuan per room-night; the current version is 750, effective 2026-01-01. Order A-104 is fictional. Reading an FAQ does not query or cancel a real order.

Each document retains its full `body`, version/effective-status metadata and a deliberately short authored `index_text`. Only `index_text` is scored. Repeated terms represent title/summary/tag duplication in the diagnostic. The full body is not secretly re-tokenized for a different method. The exact first-seen eight-term vocabulary is frozen. English ASCII letter/digit runs and a small longest-match Chinese lexicon produce parallel canonical terms; unknowns remain outside the lexical columns. This rule is a declared small-dataset tokenizer, not a general Chinese segmenter or machine translation system.

The nine query intents and relevance sets are fixed before baseline execution. Current lodging requires B; the synonym query asks for a policy source in any version and accepts A or B. The stale-premise query requires checking the current rule, so returning A fails even though it shares the number 600. The out-of-scope query has an empty relevance set and succeeds only on abstention. The fixture freezes `failure_taxonomy` with the data. Every retained query, including unfavorable cases, appears in the static chapter comparison.

## Scoring and outputs

All methods use the same documents, queries, normalization, vocabulary, candidate order and labels:

- Keyword counts distinct query terms also present in a document.
- BoW Count represents raw occurrence counts and ranks by cosine.
- TF-IDF uses raw TF and `idf = ln((N+1)/(df+1)) + 1`, then cosine; `df` counts containing documents. Query counts use the same IDF fitted to the document corpus. Zero TF remains zero and out-of-vocabulary terms add no column.

Scores are sorted descending after rounding to twelve decimals for ties, then by original candidate order. A maximum score at or below zero yields `null` (abstention). An all-zero diagnostic ranking is retained for inspection but must not be interpreted as a predicted source. Cosine's undefined zero-vector case is mapped to application score zero; the general numerical function itself returns `None`.

Success is a top-one relevant document, or abstention for an empty relevant set. Denominator: all nine queries. The actual lexical run has 5, 6 and 7 successes respectively in both locales. These are diagnostic collection results, not representative product accuracy. `ka0-expected.json` supplies separately enumerated counts, predictions and scalar score derivations; `ka0-lexical-run.json` supplies actual complete matrices/scores/rankings and source/input hashes.

`ka-static-v1.json` is a hand-authored three-coordinate map. It intentionally adds synonym sharing while collapsing policy numbers and order-status/approval distinctions. It is not trained Word2Vec. Chapter 10 records its 4/9 retrieval result and the 7/9 result from averaged four-dimensional NNLM input embeddings in `data/part-ii/nnlm-run.json`. NNLM training never uses KA-0 relevance labels. Its language prediction evaluation is separate from retrieval.

All fixture content, original expectations, output tables and parameter arrays are CC BY-SA 4.0. There are no third-party datasets or downloaded model weights. See [the implementation](../../code/knowledge-assistant/README.md) and [Part II validation](../../docs/part-ii-validation.md).

## KA-2 through KA-4 extension

The `ka2-*` files define one bilingual context template, a versioned Draft 2020-12 answer schema and localized content. The local counter is Unicode code points, explicitly not model tokens. `ka3-orders-v1.json` is a new original fictional read snapshot: A-104 belongs to mira; B-205 belongs to leo. It does not replace KA-1's distinct A104 assignment.

`ka4-documents-v1.json` adds exact bilingual source lines, validity intervals, authority/license and authored support spans while preserving KA-0 card meanings. The search card is an authored child summary, not a quotable source; its parent supplies original lines. `ka4-retrieval-rules-v1.json` freezes BM25, dense pooling, RRF, positive-score return, ties and a narrow rule reranker. `ka4-eval-v1.json` is a separate RAG development contract with explicit topic/date inputs. In particular, its current synonym question does not overwrite KA-0's version-neutral synonym relevance.

New original content uses CC BY-SA 4.0. [Part VII records](../part-vii/README.md) state producer, parameters, source hashes, complete rankings, failure injections, confidence assumptions and limitations. Neither the authored three-axis map nor the local extractive answer composer is reported as a new learned model experiment.

## Part VIII additions

`ka5-content-v1.json` centralizes bilingual decision and answer strings; `ka5-workflow-v1.json` fixes candidates, transitions and limits. `ka6-orders-v1.json` adds two fictional tenants with intentionally repeated order IDs without replacing KA-3 data. `data-card-v3.json`, `system-card-v1.json`, `risk-register-v3.json` and `governance-v1.json` document intended use, responsibilities, retention/deletion and refusal policy. Previous corpus versions and baseline outcomes remain unchanged. Actual KA-5–KA-8 observations and their separate human-reference licensing are in `../part-viii/README.md`.
