# Part III validation and editorial record

As of / last verified: 2026-09-12. Required manuscript, practice, editorial, build, and browser acceptance are complete. All new chapter content remains in draft; no publication is implied.

## Audit, dependency boundary, and preservation

The workspace contains separate book and main-site repositories. No applicable AGENTS.md was found. Existing uncommitted Part II chapters, primer, numerical code, figures, checks, and site fixes were preserved. Part I has eight published language pages dated 2026-09-10. Chapters 11–14 were placeholders; the Python primer and required Chapters 5–7 and 10 were complete, with real CPU project code. Chapter 15 remains a future chapter. No blocking prerequisite gap or additional primer was found.

The current master-plan sections 2–10, relevant contracts in the private counterpart, contributing guide, implementation plan, book configuration, all eight Part I bodies, Part I author/release records and assets, required bilingual prerequisites, current Part III placeholders, and adjacent Chapter 15 scope were read. Historical Part I/II results were treated as history rather than current passes.

A pre-edit hash snapshot outside the repository covered 255 existing source and supporting files. The final comparison found changes only in the eight requested chapter bodies, package.json, README.md, docs/implementation-plan.md, and code/part-ii/run_notebooks.py. The other 243 checked files retained their bytes, including accepted Part I content/assets, existing Part II numerical data and notebooks, the knowledge-assistant collection, and book configuration. The main-site Git worktree remained clean after its local build and composition.

All eight new bodies retain `draft: true` without publication dates. Current configured titles, IDs, order, and permanent routes are preserved. Existing heading numbering, KaTeX, static figures, responsive containers, and publication filtering are reused. The shared notebook runner gained an optional part selector; its default remains Part II. No renderer or CSS change was needed. No learning controls, code-copy buttons, PDF, EPUB, website redesign, commit, push, publishing, or deployment is part of this work.

## Delivered learning evidence

Chapters 11–14 have complete English technical baselines and Chinese semantic counterparts, seven original bilingual static diagrams with licensing, and 21 exercises with independent visible answers per language (5, 6, 5, and 5 by chapter). The Part checkpoint is in Chapter 14. The fixed fixture, independent expected values, actual CPU output, and two executed notebooks form one connected sequence-practice package. They reuse Part II arithmetic and the exact Chapter 10 long-input pair rather than replacing the previous project or creating another knowledge assistant.

Independent fraction expectations were frozen before implementation. The nine numerical/behavior tests cover three-step states, sequence resets and parameter immutability, identical window inputs versus unequal attenuated RNN states, the exact tie boundary and changed retention, BPTT against a closed-form polynomial and central finite differences at four weights, distance products, gate arithmetic, the computed encoder collision, teacher/generated prefix divergence, EOS versus a step cap, both attention queries, frozen-state versus re-encoded-input deletion, equal-score normalization, common-score-shift invariance, and invalid/empty memory.

The validator also compares the actual bilingual numerical tables to the fixed inputs and expectations, checks all inline/display mathematics and heading-depth parity, numbered examples/tables and exercise/answer alignment, reference and diagram parity, draft authorization, absence of teaching controls, source hashes, notebook code/dependency hashes, and non-error sequential cell outputs. A figure-specific regression ensures that a computed gradient is a numerical result, while the updated weight is the parameter node.

## Actual CPU and notebook execution

The new isolated environment used Python 3.12.10 on macOS 26.5.2 arm64, with NumPy 2.0.2, nbformat 5.10.4, nbclient 0.10.2, and ipykernel 6.29.5. `data/part-iii/environment.txt` contains the actual full package freeze. The core also passed under system Python 3.9.6. There is no GPU dependency, random sampling, downloaded model, or paid service.

Commands were run from the book root; `/tmp` resolves to `/private/tmp` on this machine:

| Executed command | Observed result |
| --- | --- |
| `python3 -m unittest discover -s code/part-iii -p test_core.py -v` | Nine independent tests passed. |
| `BOOK_PYTHON=/private/tmp/llm-book-part-iii-venv/bin/python pnpm test:part-iii:cpu` | The same nine tests passed in the fresh CPU environment. |
| `/private/tmp/llm-book-part-iii-venv/bin/python code/part-iii/run.py --record` | Complete state, failure, gradient, target, and attention records saved with actual versions and hashes. |
| `BOOK_PYTHON=/private/tmp/llm-book-part-iii-venv/bin/python pnpm notebooks:part-iii` | Both notebooks executed from fresh kernels, with six code cells each and no allowed errors; the optional NumPy cell was executed. |
| `BOOK_PYTHON=/private/tmp/llm-book-part-ii-venv/bin/python pnpm test:cpu` | Seven existing CPU training/model-reload tests passed. Existing Part II notebooks were not rerun or rewritten. |

The actual notebook record is timestamped 2026-09-12T05:30:42.548718+00:00. Notebook 01 took 1.0425 seconds and Notebook 02 took 1.2429 seconds in this execution. These are local execution times for tiny diagnostics, not RNN training or hardware benchmarks. Code and imported dependency hashes are in `data/part-iii/notebook-execution.json`; outputs remain in the notebooks. The actual core reproduction is in `data/part-iii/run.json`.

The first sandboxed dependency installation could not reach the configured proxy; a reviewed network retry installed the pinned requirements from PyPI. A sandboxed notebook attempt failed when a local kernel socket was denied; the approved retry completed both fresh kernels. The failed runner was identified and stopped. These unsuccessful attempts are not counted as successful notebook execution.

## Builds and browser acceptance

Node 23.10.0, pnpm 11.24.0, book Astro 7.3.1, KaTeX 0.16.47, and Playwright 1.63.0 were the installed versions inspected. They are reproducibility observations, not latest-version recommendations.

| Command | Observed result |
| --- | --- |
| `pnpm ci:build` in the book repository | Passed after the final bilingual ELMo clarification. Includes bilingual/language checks; Part I, II, and III validation; 13 Part II and nine Part III Python checks; 12 Node tests; Astro/TypeScript checks; production build and draft-output verification. |
| `pnpm ci:build` in the main-site repository | Passed. The sandboxed initial attempt could not create tsx's local IPC socket; the approved retry succeeded. |
| `pnpm compose:site` in the main-site repository | Built book output copied into the combined local artifact. No deployment was triggered. |
| `node scripts/check-draft-output.mjs ../imbrooklyn.github.io/dist/books/understanding-llms` | Passed on the combined artifact. The 112 current draft routes and their links were absent from generated HTML/XML and client JS/JSON/maps; 20 decoded Pagefind fragments referenced only built pages, including every published Part I page. |
| `git diff --check` | Passed. |
| `pnpm exec astro check` after the final browser-test additions | Passed: 29 files, zero errors, warnings, or hints. |

The task-owned development preview used `http://127.0.0.1:4325/books/understanding-llms/`, selected after inspecting occupied ports. Existing services on other ports were left alone. The browser command was `BOOK_PREVIEW_URL=http://127.0.0.1:4325 pnpm test:browser`, with 1440×1000 and 390×844 viewport projects. The full suite contains 72 cases, including 20 Part III cases. Earlier runs passed all 72, but visual inspection found that Astro had retained old diagram markup after a source edit. Those earlier passes do not establish that the corrected diagram was rendered.

Only the task-owned preview was stopped. After the final build, the generated `.astro/data-store.json` was removed and the preview restarted. Browser coverage was strengthened to compare every rendered bilingual diagram label and flow with its current source, in addition to checking numbered titles/anchors, same-chapter language switching, local links, complete numerical evidence and visible answers, no page errors, local scrolling of wide formulas/tables, no whole-page overflow, and readable light/dark diagrams. JavaScript-disabled cases visit every Part III page and verify formulas, figures, evidence, and answers without operating learning controls. The final refreshed-preview run passed all 72 cases in 2.5 minutes, including all 20 Part III cases. No tests were skipped.

Browser captures are generated in ignored `test-results/`, including page tops, equations, diagram/theme combinations, deletion and generation tables, reference answers, JavaScript-disabled answers, and the right ends of wide evidence blocks. They are acceptance artifacts rather than new textbook assets. Actual rendered images were inspected directly and in contact sheets across both languages, both viewports, and both figure themes. The corrected Chapter 12 diagrams and red-source label in Chapter 13 were re-inspected after the refreshed run. Wide equations exposed their rightmost terms through local scrolling, and the inspected JavaScript-disabled answer captures contained the full explanations. There was no whole-page horizontal overflow or unreadable diagram label requiring a site-style change.

## Two editorial reviews

The technical review checked the argument against the primary-source ledger and independent calculations, not just headings. It separated missing window input, weak forward retention, backward gradient transport, prefix mismatch, and source-summary collision. It verified the loss divisor, summing shared-weight contributions, the later forget-gate LSTM form, Cho's retain-old-state GRU convention, ELMo's frozen task recipe and character-based bottom representation, the deliberately supplied decoder table and queries, unscaled dot-product scoring, controlled deletions, and residual recursive scheduling. No industrial measurement or trained decoder trajectory was inferred from an authored value.

The reading review independently read all four Chinese bodies from beginning to end, then compared them with the English technical baselines. It checked clear actors and referents, transitions and first-use explanations, terminology, formula/table meaning, captions, exercises, limitations, and citations. Edits included a more precise “source representation” boundary, an approximation sign for rounded probabilities, natural descriptions of the matched window baseline, and an explanation of stacked recurrent layers and ELMo's token representation in both languages. Diagram review separated the gradient from the parameter it updates, replaced direction wording that was unsuitable when mobile lanes stack vertically, and clarified that the encoder diagram depicts the red source.

## Limits and completion boundary

The required practice uses supplied sequence diagnostics, as allowed by the chapter contracts. It does not fit a translator, train ELMo, benchmark LSTM against GRU, measure industrial long-context quality, or test GPU performance. Gate activations and query probes are supplied; source/RNN states and all derived reads are computed. Both deletion procedures hold the query and diagnostic readout fixed; neither is an unconstrained-generation causal experiment. Logical storage counts exclude process/container overhead. These limitations are explicit in both languages and are not silently substituted for a promised training experiment.

No required Part III acceptance item remains blocked or unverified. The final combined artifact passed draft-output checking, and the English author documentation and Part III content/evidence checks passed. Part I stays published, all new bodies stay in draft, and pre-existing work remains preserved. No publication is authorized or performed.
