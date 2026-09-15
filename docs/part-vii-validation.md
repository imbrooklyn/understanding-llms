# Part VII validation record

Started: 2026-09-14. Scope: CH-40–46 and Primer-HTTP in both languages, continuing KA-2–4 assets and part-specific verification. All target pages remain drafts. No release action is authorized.

## Initial audit

Both repositories were clean. CH-01–39 and Primer-PY are published in the current source. Target bodies and HTTP primer were placeholders. KA-0, KA-1 and Part VI adaptation are implemented; no accepted bilingual generator exists. Existing static rendering, numbering, math and draft exclusion are reusable. No site redesign or upstream rewrite is needed.

## Implemented scope

CH-40–46 and Primer-HTTP now contain complete bilingual draft manuscripts, static worked examples and failure comparisons, visible exercises and reasoned answers, and primary references. Eight original shared figures use the existing renderer. The only renderer extension enables its figure transform for Primer-HTTP while preserving unnumbered primer headings. No published manuscript, inherited dataset, checkpoint or acceptance decision was rewritten.

KA-2 adds versioned context serialization, budgets, JSON Schema Draft 2020-12, typed records and explicit parse/schema/application/provider failure branches. KA-3 adds one ownership-checked read operation reused by direct Tool, local HTTP and a revision-pinned MCP stdio adapter. KA-4 retains all lexical and dense baselines, adds BM25/fusion/reranking, and connects source parsing, addressed chunks/cards, metadata, retrieval, exact context, extractive answers, source support, abstention and layered evaluation. Two fresh-kernel notebooks use the same implementation.

## Actual CPU execution

Host: macOS 26.5.2 arm64; Python 3.12.10 in a newly created `/tmp/llm-book-part-vii-venv`; no GPU or external model calls. Direct dependencies are pinned in `code/part-vii/requirements.txt`; the actual complete environment is `requirements-tested.txt`. Runtime records use UTC, while this editorial date uses Asia/Shanghai. The recorded UTC date 2026-09-13 therefore corresponds to local 2026-09-14.

Executed from the book root:

```sh
python3.12 -m venv /tmp/llm-book-part-vii-venv
/tmp/llm-book-part-vii-venv/bin/python -m pip install -r code/part-vii/requirements.txt
/tmp/llm-book-part-vii-venv/bin/python code/part-vii/run_records.py
/tmp/llm-book-part-vii-venv/bin/python code/part-vii/run_notebooks.py
BOOK_PYTHON=/tmp/llm-book-part-vii-venv/bin/python pnpm ci:build
```

Installation and loopback tests initially encountered sandbox network/socket restrictions; rerunning those local tasks with sandbox permission succeeded. No failed attempt is recorded as a completed experiment. Final records were regenerated after strengthening malformed-generator handling and lossless conversion of JSON Schema mathematical integers into Python integer fields.

The 18 Part VII behavior tests passed. They include independent Decimal BM25 arithmetic, finite graded rankings, an independent binomial bootstrap calculation, exact budget boundaries, storage-order invariance, strict JSON/parser branches, schema-valid false facts, foreign-order backend-call counts, actual HTTP status/stream/timeout/no-write checks, actual MCP subprocess correlation and protocol errors, source offsets, conflicts, broken citations, malformed generator output and immutable inherited hashes. A JSON `750.0` is accepted as a mathematical integer; a string or Boolean is not coerced into an amount.

The record runner produced nine evidence files and 144 primary evaluation traces. Both notebooks executed all six code cells in order in separate fresh kernels with no allowed errors. Final notebook elapsed times were 1.337109 s and 0.813906 s; these are local execution observations, not model speed benchmarks. Input, implementation, output and notebook hashes are retained in `run-manifest.json` and `notebook-execution.json`.

A second fresh environment, `/tmp/llm-book-part-vii-ci-venv`, installed only `requirements-ci.txt`; all 18 behavior tests and the complete `ci:build` passed there too. The book CI and the main site's book-build workflow now select Python 3.12.10 and install that subset. Both workflow files were parsed as YAML and checked for installation before book validation. GitHub-hosted Linux execution was not triggered or tested.

## Checked results and limits

The independent BM25 example yields B = 1.5749061904610961, A = 1.414465238086587 and C = 0.7905282010746079. The graded C,A,B example yields Recall@2 = 1/2, reciprocal rank = 1/2 and nDCG@2 = 0.17376534287144002 (displayed to six decimals). The original Keyword/Count/TF-IDF success counts remain 5/9, 6/9 and 7/9 in both languages. New BM25/authored-dense/learned-NNLM/hybrid/rule-rerank counts are 7/9, 4/9, 7/9, 4/9 and 8/9. No losing method or inconvenient original query was removed.

The paired RAG development comparison changes only preselection scope filtering: 7/12 to 8/12 task successes. Retrieval coverage is 8/10 to 9/10, usable context 6/10 to 7/10 and proposed status/amount correctness 8/12 to 9/12. Citation precision means use different nonempty-citation denominators, 3/5 and 4/6; they are not evidence that the unchanged citation checker improved. Four expected abstentions pass in both conditions. Twelve semantic pairs, with translations/repeats clustered, give mean improvement 1/12 and an exact conditional percentile interval [0, 0.25]. These authored development cases do not support a deployment-accuracy or generalization claim.

## Editorial review

Round one checked each chapter's responsibility, prerequisite bridges, source support, units, numerical substitutions, full candidate orders, empty-gold conventions and failure boundaries. English technical baselines preceded Chinese drafting. Review corrected the distinction between character accounting and model tokens, mathematical JSON integers and Python storage, and the annotated support span versus the entire extended parent document. Both languages explain these distinctions. The BM25 parameters now have an explicit bound and length-adjustment explanation.

The input/output budget boundary is also explicit. The local packer uses an illustrative 200-code-point reserve to test input selection; it does not constrain the extractive composer's output. Canonical final JSON lengths are actually 502 English and 346 Chinese code points, checked independently by JavaScript serialization of saved Python-produced records. CH-40 and CH-45 state that this cannot establish a working model output limit. A future model adapter needs actual tokenizer accounting, a sufficient output allowance and truncation handling.

Round two read all eight Chinese manuscripts independently, then compared them with the English versions for actors, causal transitions, limitations, terminology, figures, sources, exercise numbering and reasoning in the answers. Model running and problem-solving reasoning are not conflated. The local composer is explicitly distinguished from LLM generation throughout. Source citations carry date/unit/scope; authored failures and actual execution are named separately. The final checkpoint remains within the single-request scope handed to CH-47.

The initial full browser pass exposed literal Markdown emphasis delimiters beside parenthesized Chinese terms. Emphasis was moved onto the term before the parentheses; no shared Markdown parser rewrite was needed. An initial Primer preview also exposed the missing figure transform. The existing transformer now handles this primer; two new renderer regression tests preserve both that behavior and chapter numbering. Browser checks require a figure to exist, avoiding a vacuous label check.

Manual mobile screenshots then exposed overwrapped ranking/evaluation columns despite no whole-page overflow. CH-44's complete ranking table and CH-46's case/count tables now reuse the existing `book-case-comparison` scroll container in both languages. Follow-up checks caught missing blank lines after the HTML wrappers and an assertion that needed to position the table vertically before testing its horizontal ends; both were corrected. No global CSS redesign was needed. Actual scrolled screenshots show readable column groups and the final reference captions.

## Site checks

Node 23.10.0 and pnpm 11.24.0 were used. The final `pnpm ci:build` passed all Part I–VII content/behavior/provenance checks, 23 Node tests, Astro checking, production build and draft-output audit. Astro reported zero diagnostics. The production artifact contains 93 HTML pages; all 92 public language pages remain built, indexed and in the sitemap. All 40 draft routes, including the sixteen target pages, are excluded from public links, search, RSS, sitemap and roadmaps.

The main site's `pnpm ci:build` passed with zero Astro diagnostics; its existing empty-draft-collection notices remain. `pnpm compose:site` then copied the book artifact locally. The book's `check-draft-output.mjs` also passed against `../imbrooklyn.github.io/dist/books/understanding-llms`. No deployment command was run.

The full browser suite passed 220 tests, with eight production-only cases intentionally skipped on the draft preview. Those eight cases passed separately against the final composed production artifact in 7.6 seconds. The final Part VII page rerun, including the wide-table fixes and budget clarification, passed all 36 cases in 1.2 minutes. `data/part-vii/browser-validation.json` retains the outcomes, actual viewport/browser details, log hashes and final source hashes. No required local content, practice, preview or build acceptance item remains incomplete.

The owned preview used `http://127.0.0.1:4337`; the composed artifact used a separate loopback server at port 4338. The observed browser was Chrome 153.0.8010.36. Desktop was 1440×1000, mobile 390×844. Tests cover every target page, natural chapter labels, structural anchors, same-chapter language selection, internal links, visible results and answers, both figure themes, local overflow, and all sixteen pages with JavaScript disabled.

```sh
ASTRO_DEV_BACKGROUND=1 pnpm dev --host 127.0.0.1 --port 4337 --ignore-lock
BOOK_PREVIEW_URL=http://127.0.0.1:4337 pnpm test:browser
BOOK_PREVIEW_URL=http://127.0.0.1:4337 pnpm test:browser tests/part-vii.browser.ts --output=/tmp/part-vii-final-page-results --reporter=line
BOOK_PREVIEW_URL=http://127.0.0.1:4338 BOOK_RELEASE_CHECK=1 pnpm test:browser tests/release.browser.ts --output=/tmp/part-vii-release-results --reporter=line
```

The environment flag keeps the explicitly owned Astro preview in the foreground rather than reusing another agent's background server. Only our port-4337 process was stopped for cache refresh; other preview services remained running. The final production build was completed before restarting the final draft preview, so build-time content filtering could not race that page check.

Manual visual review inspected all 32 page/viewport combinations and all 64 localized light/dark figure captures, plus separately scrolled mobile captions, both ends of the wide ranking/evaluation tables and the long probability formula. Some tall element screenshots cropped their off-viewport caption; direct caption captures confirmed complete readable content, rather than treating screenshot clipping as a page defect. Page headings, paragraph rhythm, source labels, numerical contrasts and non-color shape/border distinctions remain legible. Local visual artifacts are in `/tmp/part-vii-visual/`; browser artifacts are in the paths above and ignored `test-results/`. They are QA evidence, not new website assets.

## Unmeasured scope

No new LLM generation, constrained-decoding accuracy, neural reranker, pretrained dense model, production authentication, remote OAuth, full MCP conformance, write operation or live business experiment was performed. The runnable answer stage is a deterministic exact-source composer; arbitrary paraphrase entailment remains outside its checker. Prior KA-1 rejections persist, so the increment does not claim an accepted general-purpose model. Core local practice is implemented and executed; these optional model/production experiments are not substituted with replayed or invented measurements.
