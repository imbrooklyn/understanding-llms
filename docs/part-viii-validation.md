# Part VIII validation and editorial record

As of / last verified: 2026-09-14. This is an execution record, not a publication authorization. Chapters 47–53 remain draft in both languages, with no new publication dates. No commit, push, publication or deployment was performed.

## Starting point and preservation audit

The workspace root contains separate book and main-site repositories plus a private Chinese master plan. Applicable ancestor/repository instruction files were checked; no AGENTS.md applied. The actual public master-plan sections 2–10, corresponding private-plan scope, CONTRIBUTING, implementation plan, configuration, all eight current Part I chapter bodies, Part I blueprint/research/validation/release record and shared assets were read before drafting. Required prior Chapter 11/23/32/40–46, Chapter 54 scope, Python/HTTP Primers and KA project code/data were inspected in both languages where applicable. Historical release/test records were not used as substitutes for current execution.

The actual workspace already contained substantive, uncommitted KA-2–KA-4/Part VII work and an implemented HTTP Primer. The original Mini GPT rejection and the three lexical baselines were retained. No missing prerequisite required a new Primer or rewriting the preceding part. Chapters 47–53 began as placeholders. Existing title numbering, KaTeX, static figures, draft filtering and responsive styles were reused. The Chinese draft titles for Chapters 47 and 52 were synchronized with `book.mjs`; published titles were untouched.

A pre-edit digest snapshot of 336 existing chapter, figure, data and code files was kept outside the repository. Comparison after drafting found changes only in the fourteen targeted chapter bodies; all other 322 sampled files were unchanged, including published Part I and the inherited implementation/data. The snapshot does not cover every maintenance document; authorized append-only maintenance updates and configuration/package changes are listed by Git. Pre-existing dirty work, including CI and renderer changes, was preserved.

## Actual execution environment and commands

Observed environment: macOS 26.5.2 arm64, Python 3.12.10, Node v23.10.0, pnpm 11.24.0, installed Astro 7.3.1 and Playwright 1.63.0. Package manifest ranges are not substituted for observed installed versions. The clean CPU venv is `/tmp/llm-book-part-viii-venv`, installed from the inherited exact requirements through the configured package mirror. Distribution metadata is in `data/part-viii/dependency-inventory.json`; optional author-only PyArrow/PyYAML are separate from that core environment.

Commands actually run from the book repository:

```sh
/tmp/llm-book-part-viii-venv/bin/python code/part-viii/test_controls.py
/tmp/llm-book-part-viii-venv/bin/python code/part-viii/permission_records.py
/tmp/llm-book-part-viii-venv/bin/python code/part-viii/run_records.py
BOOK_PYTHON=/tmp/llm-book-part-viii-venv/bin/python pnpm test:part-viii:cpu
BOOK_PYTHON=/tmp/llm-book-part-viii-venv/bin/python pnpm notebooks:part-viii
BOOK_PYTHON=/tmp/llm-book-part-viii-venv/bin/python pnpm ci:build
```

The behavior suite currently has 14 tests, including a separately enumerated 20-row permission matrix. Both notebooks executed every cell, in order, in separate fresh kernels: five code cells each, no accepted errors. The executed notebooks and input/source/artifact hashes are retained. `run-manifest.json` records actual deterministic runs and separately pins the saved model, human, OS, permission and provenance evidence. Logical times and synthetic faults are explicitly distinguished from measured wall time.

The optional initial model probe made 18 actual CPU calls; the public-human/self-comparison probe made 20. Their saved raw responses include incorrect answers and ties. `/api/ps` observations reported zero VRAM for each run. The installed model manifest and five referenced blobs were independently hashed; no model was downloaded for the task, and no weights are redistributed. Core notebooks analyze those saved outputs without rerunning a model.

The optional macOS sandbox probe actually ran both unconfined and confined subprocesses against temporary fake data and a loopback listener. The public fixture remained readable; designated secret-file reading and network connection changed from success to PermissionError errno 1. General runtime reads remain possible; write restrictions are declared by the profile, while the measured attempts concern reads and network. The initial overly restrictive profile prevented Python startup (an observed -6 exit is retained); that is not counted as a successful functional sandbox.

The installed Skill creator's structural validator initially rejected the current official specification's optional top-level `compatibility` field. The field was moved into package metadata, which also preserves the runtime note, and the actual package then passed `quick_validate.py`. The full body size changed from 1509 to 1511 UTF-8 bytes; both textbook tables, reviewed inventory and real load trace were updated. Name/description serialization remains 225 bytes and the reference 1127 bytes. This does not imply the live specification forbids top-level compatibility.

## KA acceptance evidence and failure attribution

| Milestone / diagnostic | Actual observation | Decision and remaining boundary |
| --- | --- | --- |
| KA-5 | Both local model decisions select use_evidence; host reaches 750; authored invalid/empty/exhausted cases stop with finite calls | Accept the narrow integration and guard behavior; no general evidence-judging claim |
| KA-6 | Real helper trace; denied/expired approvals produce zero effects; before-commit fault starts at zero; lost-reply recovery after reopening retains one effect; replay mutates zero rows | Accept local single-database recovery; remote services/concurrent workers require other contracts |
| KA-7 R/G | Both 3/4; R's current request first fails retrieval, G's historical request first fails generation | Retain faulted variants; repair owners and rerun targets are in `failure-attribution-v1.json` |
| KA-7 domain human | One real reader supplied pass/fail/pass/fail with explicit anonymous-use consent after model outputs were fixed; four meanings match in each language | Narrow domain evidence, eight model decisions but four human cases; no second annotator |
| KA-7 public human | Conservative reference agreement 0/4; order consistency 3/4 | Reject this configuration for automatic release; no unfavorable sample replacement |
| Bias probes | Correct 750 and short answer each preferred across their particular swaps; identical-answer attribution probe selects position A; own-generated text wins both orders in 2/4 pairs | The new self pairs lack independent human quality labels; no causal self-bias conclusion |
| KA-8 governance | Four projected fields; each store decreases 2→1; content expires on day 7 while audit remains; equal group values; corrected current 750/historical 600 | Local field projection and in-memory lifecycle simulation, not production retention/deletion or societal fairness certification |
| KA-8 attacks | Six authored adverse proposals accepted by deliberately unsafe local sinks and blocked at their intended host controls; actual model still answers 600 with/without source labels | Distinguish model failure from host enforcement; no universal injection/jailbreak claim |
| KA-8 permissions/provenance | Own reads and approved write succeed; 17 other permission rows deny; changed Skill/helper/MCP bytes and mismatched model digest reject; bounded OS probe measured | Host identity, publisher/build trust, real services and sandbox escapes remain outside the proof |

The nine-query Keyword/BoW Count/TF-IDF baseline remains 5/9, 6/9 and 7/9 in each language. The independent handwritten confusion example remains separate from observed model results: TP 3, FP 1, TN 4, FN 2 imply accuracy 7/10, precision 3/4 and recall 3/5. The logical retry calculation is 0.20 + 0.05 + 0.10 = 0.35 seconds, with two of three call units spent. Deadline, empty-evidence, changed-argument, expired-credential and retained-negative-case checks cover boundaries rather than only happy-path snapshots.

## Editorial passes and visual findings

The first pass checked the mechanism chain, assumptions, arithmetic, prerequisites, source support and chapter responsibilities against the English baseline. The second pass read Chinese independently for subjects, references and causal continuity, then checked semantic equivalence. The two editions retain identical heading-level sequences, display math, source URLs, exercise IDs and answer mappings. Each chapter has explained examples, visible results, a counterexample/boundary, summary, exercises, answers and references. Chapter 53 adds six transfer checkpoints with visible answers.

Specific revisions included separating model/host measurements, adding the actual consented labels without erasing adverse public-human calibration, explaining the four-case/eight-decision denominator, preserving historical 600 during correction, naming HTML output context, spelling out the single-database atomicity boundary, and distinguishing real approval from prose. Chinese terminology was normalized for credentials, principal and audience. The load-trace table received its own number and Figure 49.1 an explicit explanatory reference. A code-block comment that the inherited heading validator interpreted as an H1 was moved to a separate visible output block without changing the renderer.

Actual diagram inspection found that metadata, identity and receipt nodes had used the inherited embedding-row-ID role. Their sources were corrected to application-record nodes; no shared renderer or styling was changed for this task. The historical generation-failure label was corrected to 750, matching the actual faulty proposal. Figure labels, captions, alternatives and licensing are bilingual. All code/documentation intended for the public repository is English; private author prompts were not copied.

## Browser and production integration status

The complete browser command uses an owned preview at `http://127.0.0.1:4326`:

```sh
ASTRO_DEV_BACKGROUND=1 pnpm dev --host 127.0.0.1 --port 4326 --ignore-lock
BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser
```

Ports 4321–4325 were already in use and were not stopped. Installed Astro's inspected CLI automatically backgrounds agent sessions; the foreground environment flag and documented ignore-lock option allowed this owned preview without changing another service's lock.

The final full book CI build passed all inherited/new validators and CPU checks, including 18 Part VII and 14 Part VIII behavior tests, 25 Node tests, Astro check with zero errors/warnings/hints, and a 93-page static build. The draft-output checker confirmed 40 excluded language draft routes, 92 public language pages, and correct search/sitemap/feed/roadmap filtering. One restricted-shell invocation failed at the inherited HTTP test's loopback socket bind with PermissionError. The complete command then passed with local socket access; no test was skipped or weakened to bypass that environmental restriction.

The main-site `pnpm ci:build` passed with seven pages, and `pnpm compose:site` copied the final book build into the local combined artifact. All 306 book files were compared byte for byte with their combined copies and matched. All fourteen Chapter 47–53 language routes were absent from the combined artifact. No deployment command was run.

### Final browser results and visual review

The initial complete browser run exercised 260 configured cases: 246 passed, six failed, and eight production-only cases were conditionally skipped. All six failures were the new Chinese Chapter 51–53 pages at both viewport sizes: punctuation next to bold delimiters exposed literal `**`. The manuscripts were corrected without modifying shared Markdown behavior. All inherited development-preview cases passed in that complete run.

The new Part VIII suite subsequently passed all 32 cases. Manual screenshot review then found stale node roles after figure-source edits. Only the owned preview was stopped; generated `.astro/data-store.json` was removed before restarting it. The suite now compares rendered node roles with the actual source as well as checking localized node text, alternative text, captions and licenses. It also captures captions in the viewport: a clipped element screenshot is not accepted as evidence that the page itself clips the caption. After final manuscript whitespace cleanup and a fresh content cache, the complete strengthened 32-case suite passed again in 1.1 minutes:

```sh
BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser tests/part-viii.browser.ts --output test-results/part-viii-accepted --reporter=list
```

Coverage includes all fourteen language pages at 1440×1000 and 390×844, light and dark figure rendering, same-chapter language switching, natural chapter and section numbering, internal links and anchors, visible answers, math rendering, local overflow for wide tables/formulas, no whole-page horizontal overflow, and no interactive textbook controls. Four no-JavaScript cases each traverse all seven chapters in one language/viewport combination; the content, figures, results and answers remain readable. Actual desktop and mobile screenshots were reviewed for every chapter in both languages, including final application-record roles, the historical 750 failure label and Chinese credential wording. The final screenshot directory is generated and Git-ignored; it is not a new publication artifact.

The eight production-only cases were run separately against the locally served combined artifact, including real Pagefind searches in both languages and excluded draft routes. All eight passed in 8.2 seconds:

```sh
BOOK_RELEASE_CHECK=1 BOOK_PREVIEW_URL=http://127.0.0.1:4327 pnpm test:browser tests/release.browser.ts --output test-results/part-viii-production --reporter=list
```

This is a complete initial browser run followed by successful focused repair checks and production checks, not a claim that the first 260-case run was clean. Across those runs, the 220 inherited development cases, 32 new development cases and eight production cases all have passing evidence.

### Acceptance closure

All fourteen manuscripts, seven shared bilingual figures, visible exercises and answers, the two fully executed notebooks, KA-5–KA-8 local increments, fixed positive and negative records, provenance inventory, governance Cards and author records are present. The final pre-edit digest comparison again found only the fourteen targeted bodies changed among the 336 sampled prior files. `git diff --check` passed after removing extra trailing blank lines. No prerequisite or local core exercise remains unfinished. The deliberately rejected Judge configuration and the explicit limits below remain part of the delivered result.

Execution transcripts for this session are local files under `/tmp`: `part-viii-ci-final.log`, `part-viii-browser.log`, `part-viii-browser-accepted.log`, `part-viii-production-browser.log`, `part-viii-main-build.log`, `part-viii-compose-final.log` and `part-viii-notebooks-final.log`. Durable machine-readable experiment outputs, input hashes, actual runtime versions and notebook execution records are retained under `data/part-viii/`; the commands above are the repeatable check entry points.

After verification, only the two owned preview processes on ports 4326 and 4327 were stopped. Other workspace services and pre-existing modifications were left in place.

## Explicit limits

No Linux execution, GPU benchmark, external paid API, real order/payment, real user credential, production authentication, real retention scheduler/backup erasure, deployment, legal compliance certification or complete security proof was performed. The model conversion has no independently verified build attestation. Dependencies have exact observed versions but no signed builder proof or downloaded wheel-hash lock. The local cabinet-code fixture is a behavioral-boundary surrogate, not a real harmful-content jailbreak benchmark. Automatic Judge release remains rejected. These limits are stated in the relevant chapters and Cards and do not hide a missing local core exercise.
