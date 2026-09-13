# Web book implementation plan

## Target state

Authors maintain the book text, examples, diagrams, and accompanying practice assets. Repository infrastructure owns routing, bilingual mapping, navigation, search, validation, integration with the main site, and the publication pipeline.

## Repositories and responsibilities

- `imbrooklyn/understanding-llms` is the public, authoritative book source repository. It does not deploy independently.
- `imbrooklyn/imbrooklyn.github.io` owns the site shell and is the sole GitHub Pages publisher.
- The main site's manually triggered deployment checks out the book source, builds Starlight, and merges the result into one Pages artifact.
- No PAT, repository dispatch, or cross-repository secret is required.

## Permanent routes

```text
/books/understanding-llms/
/books/understanding-llms/en/
/books/understanding-llms/en/ch-01/
/books/understanding-llms/zh-hans/
/books/understanding-llms/zh-hans/ch-01/
```

The book root redirects to English. English is the technical baseline. Chapters, glossary, errata, and changelog retain locale prefixes. Other books use their own `/books/<book-slug>/` namespace and source repository.

## Content form and current scope

Write a self-contained static textbook. Do not embed learning-content selectors, inputs, buttons, or collapsed answers. Compile figures, numbered examples, complete experiment comparisons, and solutions with the prose; do not require browser JavaScript to read them. Preserve site navigation, search, and language selection.

The September 10, 2026 release covers bilingual CH-01–CH-04 following explicit publication authorization. It produces no PDF and makes no PDF-layout investment. The September 13, 2026 authorization additionally releases all completed CH-05–CH-39 and Primer-PY language pairs. CH-40–CH-57, Primer-HTTP and the online extension remain placeholders and are excluded. Future releases require their own review and authorization. Public documentation and code comments are English; the book and its associated localized content remain bilingual. See CONTRIBUTING.md for the editorial contract.

The following increment descriptions record the earlier draft authoring stages; their original validation records remain historical evidence. Current publication scope is recorded in `docs/releases/2026-09-13-parts-ii-vi.md`.

The September 12 Part II work adds complete draft CH-05–CH-10 and Primer-PY bodies, original static figures, fixed CPU evidence and five notebooks. The continuing knowledge-assistant project starts at `code/knowledge-assistant` and `data/knowledge-assistant`; later parts retain its three lexical baselines. The training curve is compiled from recorded data into a static SVG through the existing figure mechanism. No new learning controls or publishing routes are introduced. See `docs/part-ii-blueprint.md`, `docs/part-ii-research.md` and `docs/part-ii-validation.md` for the scope and evidence.

Part III adds complete bilingual draft CH-11–CH-14, seven diagrams using the existing static renderer, fixed sequence diagnostics, and two CPU notebooks. Its code reuses Part II numerical operations; the shared notebook runner has an optional part selector with its previous default preserved. No renderer, route, or page-design extension is required. Author scope, sources, and execution evidence are in `docs/part-iii-blueprint.md`, `docs/part-iii-research.md`, and `docs/part-iii-validation.md`.

Part IV adds complete bilingual draft CH-15–CH-21, ten shared static figures, independent attention/mask/block/tokenizer evidence, and three executed CPU notebooks. The continuing Mini GPT lives in `code/mini-gpt/` and `data/mini-gpt/`, with an actual forward/loss trace (MG-1) and bounded training, save/restore, fresh-process repeat and generation evidence (MG-2). The existing curve renderer receives one narrowly scoped static-series branch; heading numbering, math, page design and draft filtering are reused. Primer-PY is already complete and remains unchanged. Scope, sources and actual acceptance records are in `docs/part-iv-blueprint.md`, `docs/part-iv-research.md` and `docs/part-iv-validation.md`.

## Content lifecycle

1. Create matching locale files with stable frontmatter and `draft: true`.
2. Complete both bodies and review technical equivalence.
3. Only when publication is authorized, remove both draft flags and give both files the same `published: YYYY-MM-DD` date.
4. Validate filenames, bilingual pairs, publishing state, numerical assets, and the independent book build.
5. The author manually runs the main site's Pages workflow to publish the combined source.

## Part V draft increment

Chapters 22–33 add twelve complete bilingual draft pairs, twelve shared static figures, data cards beside the existing project data, resource/trace worksheets, generation-policy records and KA-1. The existing Mini GPT checkpoints and KA-0 documents/baselines remain unchanged. KA-1 freezes the contract before comparing two actual CPU parameter configurations and preserves all 144 attempts, including failures; both candidates are rejected for assistant use. `docs/ka1-selection-report.md` records the decision and optional external-candidate documentation separately.

`pnpm validate:part-v` joins `ci:build` with bilingual structure/math, rendered-source, direct table-to-evidence and provenance checks. `BOOK_PYTHON=<tested-python> pnpm test:part-v:cpu` executes changed-condition tests and full paired replay; `pnpm notebooks:part-v` runs three fresh CPU kernels through the minimally extended existing notebook runner. Browser coverage includes all 24 pages on both viewports, both figure themes, same-chapter language navigation, local overflow and no-JavaScript evidence. No renderer or page redesign is required. Scope, primary sources, editorial findings and actual outcomes are maintained in the three Part V author records. All new content stays draft-only; no release operation accompanies this increment.

## Build and integration

Starlight uses site `https://imbrooklyn.dev` and base `/books/understanding-llms`. The book builds into its own `dist/`. The main site builds its shell and copies the book output to `dist/books/understanding-llms/`. Only one final Pages artifact is uploaded, avoiding competing deployments to the same domain.

The book provides localized navigation, Pagefind search, canonical URLs, sitemap, alternate-language links, edit links, and RSS. Production filtering removes unpublished chapters and their links. Development mode shows drafts for review.

## Visual experience

Custom CSS reuses the main site's IBM Plex Mono, accent color, light/dark variables, borders, spacing, and focus treatment. The book retains a readable content width, chapter sidebar, page outline, and links to the main site and source repository. Local figures use meaningful labels and descriptions rather than color alone. Wide mathematical expressions and tables stay within their own scroll containers on narrow screens.

## Verification and completion

- Both locale routes build and switch to the same chapter in the other language.
- Unpublished chapters stay out of production routes, links, and search output.
- Public repository documentation and code comments use English.
- Chapter contents remain complete without JavaScript and contain no learning controls.
- Standalone book and main-site composition builds succeed.
- Local desktop/mobile previews check figures, formulas, navigation, and content availability.
- Part II bilingual and dependency-free behavioral checks run inside `pnpm ci:build`. `BOOK_PYTHON=<CPU-environment-python> pnpm test:cpu` additionally executes the training and model-reload checks; the notebook runner independently executes fresh kernels and records outputs.
- Part III content, independent sequence behavior, numerical tables, figure semantics, and recorded notebook hashes are checked by `pnpm validate:part-iii` inside `ci:build`. `pnpm test:part-iii:cpu` and `pnpm notebooks:part-iii` use `BOOK_PYTHON` when supplied. The shared browser entry includes all eight Part III pages in both viewport projects and with JavaScript disabled.
- Part IV bilingual equations/anchors/visible answers, independent scalar evidence, model/checkpoint identities and executed-notebook hashes run in `pnpm validate:part-iv` within `ci:build`. `BOOK_PYTHON=<CPU-environment-python> pnpm test:part-iv:cpu` executes 23 behavior tests; `pnpm notebooks:part-iv` uses the same interpreter in three fresh kernels. The shared browser suite covers all fourteen Part IV pages at both viewport sizes, both themes and without JavaScript.
- An authorized release includes the main-site deployment and live-site verification of the published routes, navigation, search, and feedback links.

## Part VI draft increment

CH-34–CH-39 separate data/objectives, update mechanisms, inputs/external capabilities and runtime computation. Existing prerequisites and Primer-PY are complete; no upstream rewrite or new primer is required. Six bilingual static figures reuse lanes, formulas, numbering and draft filtering. A bounded static SVG branch plots the fixed call-budget curve; it adds no client interaction or page redesign.

The project increment extends the same Mini GPT/KA-1 implementation with an immutable runtime-format experiment and a decision report. It retains all original cases/checkpoints/policies/seeds and lexical baselines. Two CPU notebooks execute actual generation replay and independent mechanism calculations. Optional SFT/RL/PEFT training is explicitly unmeasured.

`pnpm validate:part-vi` verifies bilingual equations/anchors, visible answers, table-to-evidence bindings, budget/stop failures, matrix arithmetic and provenance inside `ci:build`. `BOOK_PYTHON=<tested-python> pnpm test:part-vi:cpu` runs behavioral tests and exact paired output reproduction; `pnpm notebooks:part-vi` uses fresh CPU kernels. The shared browser suite covers every language page, desktop/mobile, both figure themes, same-chapter switching, local overflow and no-JavaScript access. Actual outcomes and editorial findings belong in `docs/part-vi-validation.md`.
