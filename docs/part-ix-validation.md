# Part IX validation and editorial record

Status: complete for the declared local CPU demonstration and static textbook scope. `as_of: 2026-09-15`; primary-source verification was performed on 2026-09-14. Measurements retain actual UTC timestamps, which can fall on the preceding date in Asia/Shanghai. No commit, push, publication or deployment was performed.

## Scope and starting state

Repository boundaries, applicable instructions, Git status and existing work were audited first. No applicable `AGENTS.md` was found. The required public plan sections, contribution and implementation documents, configuration, eight accepted Part I chapters, Part I author/release records and shared assets were fully read. Both language versions of the prerequisite chapters, the HTTP Primer, KA-0 through KA-8 implementations and their evidence were inspected. The private planning document was consulted but not copied into the public repository. The adjacent multimodal extension remains outside this task.

The actual tree already contained completed Part VII/VIII work and published Chapters 1–39 plus the Python Primer, superseding the older September 10 publication snapshot. The HTTP Primer was already substantive and draft. Chapter 54 adds the necessary bridge from its methods, status, timeout and stream foundations to background jobs, ownership checks and cancellation. Existing lexical retrieval, structured contracts, read-only MCP, Skill checks, permission state, approval receipts and attack regressions were executable. No missing prerequisite project was concealed behind a placeholder or replaced with a second assistant.

The delivery includes eight draft Chapter 54–57 pages, four shared bilingual figure sources, the KA-9/KA-10 increment in `code/knowledge-assistant/`, two executed notebooks, fixed and measured evidence in `data/part-ix/`, and the English blueprint, research, online implementation notes, runbook and capstone dossier. Data/System Cards, license and dependency inventories and an owned risk register supplement inherited versions. Chapter IDs, routes, order and published Part I material are preserved. Four Chinese draft titles were edited together with configuration and frontmatter.

A private starting snapshot contained hashes of 623 tracked and untracked files. Final comparison found no missing starting file and exactly 12 changed starting files: the eight target chapters, `src/config/book.mjs`, `package.json`, `CONTRIBUTING.md` and `docs/implementation-plan.md`. All other starting bytes, including inherited Part VII/VIII changes, frozen shared READMEs and Part I prose, code, data and figures, matched. New Part IX files are additional to this comparison. The private prompt and snapshot were not added to the repository.

## Environment and executed checks

A clean `/tmp/llm-book-part-ix-venv` used Python 3.12.10 with `include-system-site-packages = false` on macOS 26.5.2 arm64. The existing pinned Part VII dependencies supplied JSON Schema and notebook tools. The installed 39-distribution inventory and exact freeze are retained. Acceptance did not use the system Python 3.9 interpreter, neural model calls, GPU, paid API or model account.

Actual website versions were Node 23.10.0, pnpm 11.24.0, Astro 7.3.1, Starlight 0.42.0 and KaTeX 0.16.47. Playwright 1.63.0 drove installed Chrome 153.0.8010.36. No website dependency or renderer was replaced. The browser manifest binds final source bytes, screenshots, versions and results.

The commands below ran from the book root unless stated otherwise. `BOOK_PYTHON` was explicitly `/tmp/llm-book-part-ix-venv/bin/python`; repeatable environment setup is in [the CPU README](../code/part-ix/README.md).

| Actual command or operation | Observed result |
| --- | --- |
| `BOOK_PYTHON=/tmp/llm-book-part-ix-venv/bin/python pnpm records:part-ix` | Completed loopback service, candidate, fault, feedback and inherited capstone runs; nine output hashes and relevant source/input hashes retained |
| `BOOK_PYTHON=/tmp/llm-book-part-ix-venv/bin/python pnpm notebooks:part-ix` | Both notebooks executed every code cell in order in fresh kernels, with no allowed errors |
| Both Python blocks from `docs/part-ix-runbook.md`, executed in order | Passed; one B request and nine A requests in the actual cohort; output and source hash retained in `runbook-run.json` |
| `BOOK_PYTHON=/tmp/llm-book-part-ix-venv/bin/python pnpm ci:build` | Passed all content/language/Part I–IX validators, applicable CPU suites, Node tests, Astro checks, production build and release filtering |
| `pnpm ci:build` in `../imbrooklyn.github.io` | Passed; seven main-site pages; zero Astro errors, warnings or hints |
| `pnpm compose:site` in the main-site repository | Passed; 306 book files matched the combined copy byte for byte; all eight Part IX routes absent |
| `git diff --check` | Passed after final Markdown cleanup |

The latest core run is recorded at `2026-09-14T16:37:20.213682+00:00`, with 8.494362 seconds of elapsed core work. This is a small-suite observation, not a capacity estimate. Final CI passed 13 Part II, 9 Part III, 18 Part VII, 14 Part VIII and 12 Part IX Python tests, plus 25 existing Node tests. Part IX took 7.453 seconds in that run. Astro checked 68 files with zero errors, warnings and hints. Production built 93 pages, including the root redirect, in 1.71 seconds. The release checker verified 40 excluded language-specific draft routes and all 92 public language pages, search indexing, sitemap, both feeds and roadmaps. Counts describe this actual tree, not a fixed Part I assumption.

Notebook execution was recorded at `2026-09-14T16:37:24.785760+00:00`. `01-service.ipynb` ran three code cells in 2.308924 seconds; `02-operations.ipynb` ran four in 1.818096 seconds. The first makes real HTTP requests and cancels a running worker. The second executes gates and policy calculations, and explicitly reads the saved rollback record without pretending that reading caused a rollback. Input hashes are checked before and after execution, including the consumed release record. Executed artifact hashes are in [notebook-execution.json](../data/part-ix/notebook-execution.json).

Restricted execution initially prevented loopback sockets or the main site's `tsx` IPC pipe. Commands were rerun with the required local process/socket permission and passed. No automatic approval review rejection occurred. These were environment conditions, not silently skipped checks.

## Independent expectations and actual behavior

`expected-v1.json` was authored before implementation verification. Its source intervals, expected amounts and statuses come from fixed source lines. Small calculations were independently worked through, then rechecked by the JavaScript validator and Python suite. The function being judged does not manufacture its own expected answer.

| Claim or boundary | Independent check and retained result |
| --- | --- |
| Waiting budget | 1,000 ms minus 120, 80, 300 and 100 ms leaves 400 ms; a 550 ms next attempt does not fit |
| Span interpretation | Overlapping children use interval union, not a sum that assumes sequential work |
| Cache validity | TTL is invalid at equality; principal, request date and component identity separate entries; knowledge updates cannot rely on an unexpired stale entry becoming correct |
| Semantic false hit | Assigned vectors give cosine approximately 0.999949 while dated answers differ, 600 versus 750; semantic response reuse remains disabled |
| Limiter and breaker | Fractional refill, rejected permits, capacity, consecutive failed requests, open rejection and a single recovery probe are checked at boundaries |
| SLO denominator | The authored 22 observations give 20 eligible outcomes, 18 timely successes, 90% SLI, one allowed bad outcome and burn multiple 2; the strict greater-than-two alert does not fire |
| Changed denominator | The exercise's 48/50 is 96%; including three cancellations changes the declared metric to 48/53, approximately 90.566%, with burn approximately 4.717 |
| Actual fault sequence | Five completed eligible requests give two good outcomes and three failures: 40% SLI, burn multiple 12 and the declared alert firing |
| Source and authority | Actual requests return current 750, historical 600, abstention for absent evidence and the retained supported synonym miss; ownership and tenant denials remain visible |
| Release and rollback | A and B each pass 10/10 presentations; stale candidate 4/10 is refused normally. The forced local drill returns 600; rollback restores 750; an already admitted stale job retains 600 |
| Cancellation and recovery | A running worker is stopped with one cancelled terminal result and no later answer/cache write. Inherited approved-write recovery reconciles one receipt and one effect; reading a trace adds no effect |
| Feedback governance | A report enters quarantine, trusted review creates a separately specified synthetic regression case, and the original subject report is deleted; feedback does not automatically train or relabel the fixture |

Current capstone runs preserve Keyword 5/9, BoW Count 6/9 and TF-IDF 7/9 on the same original query set in each language. They also execute the inherited read-only MCP subprocess, 20 permission rows, six fixed attack proposals and the small layered comparison. Denominators remain separate. The ten-presentation bilingual gate is five cases in two languages, not ten independent demonstrations of generalization. The synonym miss remains outside the small release fixture and is not removed to improve a score.

Earlier Mini GPT selection/adaptation and optional Qwen/Ollama judge results are referenced by immutable hashes and described as historical. They were not rerun or converted into current neural service measurements. The default service records an extractive answer producer and zero neural calls.

## Failures retained and repairs verified

The first cancellation run classified `InterruptedError` under `OSError` as a dependency failure before cancellation. Its trace and old source hash remain in `initial-cancellation-observation.json` and `initial-service-run.json`. Exception ordering was corrected. Regression checks require worker termination, one cancelled terminal event and no dependency-failure, late answer or cache write after cancellation.

The first UI browser run failed four service cases because the store's `id` was not mapped to public `order_id`. The original failure record and screenshot remain. The adapter now maps the field at the boundary; both languages and viewports display A-104 and its correct fictional status. A separate UI race could let a late cancellation acknowledgement overwrite an already received terminal event. The handler now checks job identity and request epoch. Its browser test delays the acknowledgement by 150 ms and verifies that cancellation remains visible afterward.

An early build reported deprecation hints because a helper named `status` collided with legacy `window.status`. Renaming it to `setStatus` removed the hints. Notebook replay input was added to the execution inventory, with hashes checked before and after running.

Visual review found that the capstone diagram used the record shape for an external source and verification work. Source and operation kinds were corrected. Cancellation labels now match lowercase state fields, and the Chinese version-relationship title was clarified. Corrected figures were rebuilt and previewed after stopping only the owned preview and clearing its generated Astro content store.

A subsequent CI run caught navigation text appended by this task to two shared READMEs included in the inherited Part VIII frozen manifest. Only those new additions were removed, restoring their exact starting bytes. Navigation to the new material remains in Part IX documents and the contribution guide. The old manifest was not regenerated or weakened; the final complete CI passed.

## Browser and visual acceptance

An owned development preview used inspected free loopback port 4326. Its final launch was `ASTRO_DEV_BACKGROUND=1 pnpm dev --host 127.0.0.1 --port 4326 --ignore-lock`. Existing services on other ports were not stopped. A separate owned Python static server exposed the local combined production directory on 4327. Application tests start and close their own loopback instances.

| Actual browser invocation | Result |
| --- | --- |
| `BOOK_PYTHON=/tmp/llm-book-part-ix-venv/bin/python BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser` | 278 passed, 8 production-only cases skipped, zero failures; reported duration 9.9 minutes |
| `BOOK_PYTHON=/tmp/llm-book-part-ix-venv/bin/python BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser tests/part-ix.browser.ts tests/part-ix-service.browser.ts --output test-results/part-ix-final --reporter=list` | 26 passed, no skips or failures, 51.3 seconds; after final corrections and fresh preview content store |
| `BOOK_RELEASE_CHECK=1 BOOK_PREVIEW_URL=http://127.0.0.1:4327 pnpm test:browser tests/release.browser.ts --output test-results/part-ix-production --reporter=list` | 8 passed, no skips or failures, 8.1 seconds |

The full development suite preceded final Part IX figure labels/roles and a clarification that the service has no order-cancellation endpoint. The final 26-case run covers all affected pages and service behavior. The production suite separately resolves eight intentional development skips. These are overlapping scopes, not 312 unique tests.

All eight pages were visited at 1440×1000 and 390×844. Checks cover complete content, natural chapter numbering, matching bilingual structure, same-chapter language switching, links and anchors, KaTeX without errors, localized figure labels/roles/alternative text/captions/license, visible answers and absence of teaching controls. Both themes were captured. JavaScript-disabled contexts visited all eight chapters at both sizes and verified static figures, formulas, results and answers. No whole-page horizontal overflow was found; wide material is constrained locally.

Rendered figures were visually inspected, not accepted from source or DOM checks alone: all four chapters in English and Chinese, light and dark, desktop and mobile. Page-top and reference-answer captures were reviewed, including Chinese mobile SLO calculations without JavaScript. Service citations, order read, clear/undo, unsent handoff, feedback and cancellation were exercised. Visible focus, labels and live-status attributes form the accessibility evidence; service theme/viewport screenshots were inspected.

An element screenshot of the tall Chinese mobile version diagram cuts off part of the caption at its screenshot boundary. A separate caption viewport capture shows the complete caption and license in the page. The document does not clip or overflow. Both captures remain so that this screenshot limitation is not mistaken for a page defect.

The archive contains 104 final Part IX screenshots and 12 production screenshots. [browser-manifest.json](../data/part-ix/browser-manifest.json) records their hashes and 325 final source hashes. Six logs under `data/part-ix/logs/` preserve command results. ANSI control sequences were removed and the private absolute workspace prefix replaced by `$WORKSPACE`; result lines were retained. The original UI failure screenshot remains separate.

After archiving, `pnpm validate:content`, `pnpm validate:language`, `pnpm validate:part-ix` and `git diff --check` passed again. All 447 archived source/screenshot/log hashes matched; the 623-file preservation comparison still had exactly the 12 intended changes. No delivery file checked under the new project/evidence/notebook/document directories was ignored by Git.

Production verification used the composed output: 306 book files were byte-identical to the combined copy. Drafts did not enter routes, navigable links, search, feeds or sitemap. Existing search worked in both languages and viewports, including Chapter 39. No public page gained an unavailable draft link. These commands build and serve local files, without triggering hosting.

## Two editorial passes

The first pass checked chapter responsibility, primary-source support, assumptions, arithmetic, provenance, prerequisites and bilingual equivalence. Each English technical baseline preceded its Chinese counterpart. One continuing dated policy request connects service responsibility and cancellation, evidence-bound candidates, bounded reuse and failure handling, and final acceptance with distinct denominators and human owners. The HTTP bridge precedes practice. No multimodal, multi-agent or industrial-deployment prerequisite was added.

Clarifications were added in both languages where needed: stopping a worker differs from hiding an answer; overlapping spans cannot simply be added; metadata cannot restore executable/database bytes; admitted jobs keep their version; semantic similarity does not establish time-valid equivalence; a live SLO window can contain unfinished requests; capped metrics must flag incomplete coverage; logical expiry differs from periodic physical sweeping; job cancellation differs from order cancellation. The MCP fixture and service order store are identified as different inherited snapshots, not one live merchant system.

The second pass read each complete Chinese chapter independently, then returned to the English facts and qualifications. Long noun chains and unclear actors were restructured. Account and tenant references were made consistent. Titles, tables, figure text, captions, exercises, answers and reference annotations were checked separately. Model execution and problem-solving reasoning retain distinct wording; protocol fields and errors remain literal. Both languages include the same numbered evidence, calculations, counterexamples, transfer exercises and visible explained answers with matching anchors. Required explanatory additions were not confined to one language.

These passes are editorial judgments, not claims that tests prove good prose. Principal numbers are connected to their inputs and denominators. The final chapter includes answered transfer problems and a cross-chapter checkpoint rather than substituting a feature list for acceptance evidence.

## Limits and responsibility

No required local textbook, service, notebook or browser acceptance item remains blocked. The claim is narrow: a reproducible, evaluable fictional assistant on one macOS CPU environment with a fixed small corpus and controlled faults.

Linux and Windows were not tested; worker process-group cancellation assumes POSIX. Production identity/revocation, encryption, durable queues, multiple instances, sustained load, real availability, complete erasure, executable/database rollback and external MCP client interoperability were not validated. Python's demonstration HTTP server is not presented as a production server. Theme/focus/status inspection and DOM checks do not establish full WCAG conformance or assistive-technology usability. No new neural benchmark, training run, independent security audit or adaptive attack study was performed.

Known lexical misses, stale-source risks, biased feedback, small denominators and historical-judge limits remain in prose, cards and the owned risk register. Policy owners validate source intervals; maintainers review feedback and release evidence; operators inspect compatibility and recovery; users review cited evidence. Monitoring changes do not establish causes, a manifest does not prove quality and replay does not reverse effects.

All eight target pages and the unchanged HTTP Primer remain `draft: true`, without new publication dates. The working tree is the delivery; passing checks does not imply release authorization.
