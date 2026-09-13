# Part V validation and editorial record

`as_of: 2026-09-13`  
`last_verified: 2026-09-13`  
Status: complete for the draft-only Chapter 22–33 and KA-1 contracts. No required item remains blocked.

## Scope and preserved starting work

All twenty-four Chapter 22–33 manuscripts contain the complete argument, worked examples, shared static figures, counterexamples, boundaries, summaries, transfer exercises, directly visible answers and annotated references. Twelve figure sources provide both languages, captions, alternative text and original-source licenses. All new pages remain `draft: true`, without added publication dates. IDs, order and routes are unchanged. Previously unwritten Chinese configuration titles were polished with matching frontmatter; published Part I titles were retained.

The audit read master-plan sections 2–10 and the corresponding private plan, CONTRIBUTING, implementation plan/configuration, all eight accepted Part I bodies and their records/assets, the full target range, specified prerequisites, both primers and Chapter 34's boundary. MG-2, its tokenizer and two CPU checkpoints are implemented. KA-0 provides five bilingual documents, nine queries and three lexical baselines. Primer-PY supplies the practice prerequisite. Primer-HTTP remains a later engineering dependency; no new primer is required here. No blocking project prerequisite was missing.

The starting inventory recorded 333 existing files and Git status outside the public repository. The comparison found no missing inventoried file. Changes within that inventory are limited to the twenty-four target manuscripts, scoped configuration/package/implementation-plan updates, the shared notebook runner extension, and regenerated Part IV notebook outputs/execution provenance. Part IV code-cell hashes are unchanged. All inventoried Part I text, data, code and figure assets are byte-identical to their starting state. Existing Parts II–IV prose, fixtures, Mini GPT code/corpus/tokenizer/checkpoints and KA-0 inputs are preserved. The root README received Part V links. Unrelated dirty rendering/style/lockfile work was not reset or rewritten. The main repository has no source changes.

The task reuses heading numbering, KaTeX, static figures, navigation and publication filtering. No renderer, design, interactive lesson, hidden solution or copy button was added. Mechanisms live in `code/part-v/`; KA-1 extends `code/knowledge-assistant/ka1.py`, importing the existing Mini GPT and lexical baselines. Public author documents, code comments and notebook explanations are English; localized examples and labels are explicit content resources.

## Frozen evidence and actual CPU work

The English blueprint preceded primary-source research and candidate evaluation. Independent hand calculations in `data/part-v/expected.json` preceded the scalar implementation. The research ledger records actual supporting sections, official URLs, dates/versions and limits. Historical paper measurements remain distinct from this book's runs.

KA-1 froze its cases, rubric, gates, policies, candidates, seeds and input hashes at `2026-09-13T04:35:44.060022+00:00`, before the paired run recorded at `2026-09-13T04:38:23.958253+00:00`. All 144 attempts retain complete IDs, probabilities, bytes, displayed text, stop reasons, UTF-8 status and warm complete-call times. Chapter 29 separately retains 36 actual continuations. Neither run was replaced to obtain favorable results.

The two measured configurations are the existing validation-selected step-50 and final step-600 MG-2 checkpoints, with identical architecture, tokenizer, task and criteria. Both fail the bilingual quality gates and are rejected for assistant use; the selected checkpoint remains useful for education. This completes a configuration-selection decision without claiming a deployable assistant. All nine KA-0 queries and Keyword/BoW Count/TF-IDF results remain a separate retrieval comparison. Complete primary responses and the unsuccessful/invalid-UTF-8 stress evidence are retained.

Semantic scoring is disclosed AI-assisted author inspection of all 62 unique case/locale/completion/UTF-8 combinations, mapped to identical attempts. It is not an independent human panel or calibrated LLM-judge trial. Six assigned calibration examples expose substring false positives and strict-match false negatives. The post-run `ka1-provenance-note-v1.json` corrects overly broad attribution in the frozen metadata: KA-0 explains a possible status, while KA-1 assigns processing to a new fictional short label and adds no-granted-approval. No prompt, rubric, document, frozen byte, run or decision changes. Both languages and the report explain the increment.

A clean temporary environment installed the exact reused dependency set: Python 3.12.10, PyTorch 2.7.0, NumPy 2.0.2, nbformat 5.10.4 and nbclient 0.10.2 on arm64 macOS 26.5.2. Generation uses CPU float64 and one thread. Package installation required network access once; core runs then used local retained files, without a model service.

Actual commands ran from the book root with `BOOK_PYTHON=/private/tmp/llm-book-part-v-venv/bin/python`, unless another root is specified:

| Command | Observed result |
| --- | --- |
| `python3.12 -m venv /private/tmp/llm-book-part-v-venv`; environment's `python -m pip install -r code/part-v/requirements.txt` | Clean CPU environment created and pinned dependencies installed |
| `BOOK_PYTHON=... pnpm test:part-v:cpu` | 24 tests passed, including full paired replay, retained failures and inherited retrieval |
| `BOOK_PYTHON=... pnpm notebooks:part-v` | Three fresh-kernel notebooks passed: 4, 2 and 3 code cells; no allowed errors |
| `BOOK_PYTHON=... pnpm notebooks:part-iv` | Three existing notebooks reran successfully: 3 code cells each, after the shared runner extension |
| `pnpm ci:build` | All language/content/Parts I–V validators, 14 Node tests, Astro checks, production build and draft inspection passed |
| Main repository: `pnpm ci:build` | Content validation, Astro diagnostics and production build passed |
| Main repository: `pnpm compose:site` | Book output copied into the generated main site; independent SHA-256 tree comparison found 143 identical files and no extras |
| `BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser` | All 156 cases passed in 5.6 minutes, including 52 Part V cases |
| `BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser tests/part-v.browser.ts` | All 52 Part V cases passed in 1.9 minutes after screenshot-only corrections |

Final Part V notebook execution times were 0.7409, 1.2202 and 1.2140 seconds. These are notebook times, not serving benchmarks. Execution records include code-cell and input hashes. Replays compare complete outputs, IDs, bytes, stops and UTF-8 validity, without expecting identical elapsed times or replacing historical measurements. The Part IV regression trains only in a temporary destination and leaves the saved MG-2 bundle intact.

JavaScript independently checks integer products, exact/symbolic expectations, timestamps and reported results. Python tests perturb inputs instead of accepting implementation-generated gold values. Boundaries include sampling ties/cumulative mass, invalid draws/dimensions, zero denominators, RMS offsets, signed gates, unequal valid-target microbatches, inert patch controls, beam joint probability, cache concurrency, undefined one-output TPOT, quantizer ties/clipping, observation windows, speculative rejection correction and erroneous filters. Content checks bind both languages' actual table cells to the fixtures and complete measured primary responses. Full commands and logs are retained in [the acceptance evidence](../data/part-v/verification/README.md).

## Browser, visual and production checks

The inspected stack is Node 23.10.0, pnpm 11.24.0, Astro 7.3.1, Starlight 0.42.0, KaTeX 0.16.47, Playwright 1.63.0 and Chrome 153.0.8010.36. A free port was confirmed before starting the task-owned draft preview:

```sh
ASTRO_DEV_BACKGROUND=1 pnpm dev --host 127.0.0.1 --port 4326 --ignore-lock
BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser
```

The explicit settings keep this preview separate from the existing Astro service on port 4325. Only the task's identified process was stopped during cache recovery; other services remained running.

The final complete suite passed all 156 cases after the Markdown/cache repairs and figure-classification corrections. Budget declarations and a recovery-file bundle are external objects; a generated completion is text. The suite checks each rendered node's class against its declared source kind as well as its visible text. A subsequent screenshot-only adjustment masks navigation without reflow, aligns a nearly viewport-height figure before capture and allows the page-top paint to settle. All 52 Part V cases passed again with this adjustment and added caption-bounds checks; no site content, renderer or CSS changed during that final capture adjustment.

The Part V suite visits all twelve chapters in both languages at 1440×1000 and 390×844. It checks chapter/section numbering, same-chapter language switching, local links/anchors, mathematics, all visible answers and key evidence, absence of teaching controls, local scrolling for wide material and no whole-page overflow. Every localized figure label, flow, caption, alternative text and credit is compared with the rendered figure in light/dark themes; parameter borders remain neutral and double. Separate JavaScript-disabled contexts visit every chapter, language and viewport. Screenshots cover figures, openings, equations, answers, wide-table right edges and the KA-1 summary.

Actual screenshot inspection covered all twelve figures in both languages, themes and viewports, and the page openings for all twenty-four pages in both viewports. Labels, calculations, flows, neutral parameter borders and full credits are legible; mobile figures stack their steps. The corrected classifications were inspected again in the final rendered figures. Additional inspection covered the RoPE, sampling and TTFT/TPOT formulas, the wide gated-FFN matrix, both language versions of the KA-1 result tables and complete reference answers, and both edges of the English mobile summary table. Wide material scrolls locally and the whole page stays within its viewport. All JavaScript-disabled page visits and static-evidence/answer checks passed. These image reviews supplement the two full manuscript-reading passes; they do not stand in for those readings.

The book build generated 21 pages with zero Astro errors/warnings. Its production checker verified all 112 current draft chapter/support routes and their links absent from HTML/XML, client JS/JSON/maps, RSS and sitemap. It decoded 20 Pagefind fragments containing only built pages, including all eight published Part I chapters. These are observed repository totals, not fixed Part V assumptions. The composed tree has no Chapter 22–33 routes or links and retains the main homepage. The main build retains existing empty `drafts` collection notices in its log; its diagnostic check reported zero errors/warnings. No deployment command ran.

## Two editorial passes

The first pass read each complete English baseline, then checked Chinese against the same facts, formulas, examples, conditions, references and answers. The second read every Chinese manuscript independently for natural order, clear referents and causal transitions, then reread the complete English range for technical parity. These are agent-assisted author reviews, not an external native-speaker panel. Automated parity checks support this reading but do not prove prose quality.

| Chapter | Particular review and repair |
| --- | --- |
| 22 | Independent lifecycle axes; base checkpoint has completed pretraining; MG-2 failures remain visible |
| 23 | Every pipeline count and mixture denominator; false deletion; distinct permission and crawler-policy evidence |
| 24 | FLOP units/omissions; assigned curve versus fit/extrapolation; separate lifetime cost |
| 25 | Distant-key opening; explain each input/output before naming the mechanism; epsilon/gain and offset conditions |
| 26 | Define each recurrence symbol; distinguish resident/active parameters, KV heads and attention pairs |
| 27 | Both optimizer accumulators and all five categories; valid-target weighting; allocated gradient storage versus reset values |
| 28 | Decodability versus association/effect; matched inert-site control; undefined recovery denominator |
| 29 | All filters, renormalization and draw boundaries; full short beam paths; different structured/creative criteria |
| 30 | Positions actually processed into cache; invalidate from the changed position; TTFT versus complete time and interval count |
| 31 | Same arrivals and both observation windows; exact speculative correction; no universal speedup |
| 32 | Added fictional conditions disclosed without rewriting the freeze; case-level uncertainty; explicit review method |
| 33 | All primary outputs and rounded metrics bound to raw data; unchanged quality gates; dated documentation separated from unperformed measurements |

Chinese consistently distinguishes model running (`inference`) from problem-solving reasoning (`reasoning`). Long translated noun phrases and unclear pronouns were reorganized, including headings, figure text and answers. Technical explanatory repairs were made in both languages. The final checkpoint and transfer answers connect data, training, generation, running, serving and evaluation, leaving instruction training to Chapter 34.

## Failures and corrections

Initial CPU integration exposed a tokenizer loader argument mismatch and ambiguous import of another project's `run.py`. The loader now follows the existing API and the test harness imports an explicit module path. Full CPU and notebook replays subsequently passed.

The first restricted notebook attempt could not bind Jupyter loopback sockets. The same fresh-kernel workflow succeeded with local socket permission; saved output was not substituted for execution.

The first full browser run produced 143 passes and 13 failures: Chinese emphasis delimiters adjacent to punctuation rendered literally. The manuscripts were corrected without changing the renderer, and focused checks passed. A later run detected stale figure labels in Astro's generated content cache and was interrupted. Only the task's preview was stopped and `.astro/data-store.json` removed. A clean build/restart produced current figures, and a focused Chapter 27 check passed on both viewports before the 156-case pass. The subsequent figure-classification polish receives the same fresh-cache treatment. Failed/interrupted runs are not counted as acceptance passes.

Visual inspection also found a screenshot artifact in the Chinese mobile Chapter 24 figure: its 840.64 px height was placed at y=65.34 in an 844 px viewport, leaving the caption below the captured viewport edge. Direct geometry inspection and a separate caption image established that the caption was complete and inside its figure in the page. Aligning the figure at y=0.34 captured the full caption and license. The final browser harness retains this capture correction and checks caption bounds. The website layout was not changed to accommodate the screenshot tool.

## Remaining limits and publication boundary

No paid API, GPU, external-model download/run, production serving/load test, independent human panel, deployed privacy audit or real order operation was performed. These are optional or outside the chapter contracts. External model/config/license/price observations are dated official-document checks, with unresolved pinning and access conditions disclosed. Constructed interventions, resource budgets and serving traces prove their assigned arithmetic, not industrial performance or modern-model accuracy. Public diagnostics are not a blind generalization benchmark.

Original text, figures, data and records use documented CC BY-SA 4.0 licenses; code uses Apache-2.0, with dependencies/external sources retaining their own terms. The private Chinese task/plan was not copied into the public repository. No commit, push, publication, deployment, PDF or EPUB was produced. Changes remain in the workspace as drafts.
