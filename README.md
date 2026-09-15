# Understanding Large Language Models from the Ground Up

The source repository for a web-first bilingual open textbook published at [imbrooklyn.dev/books/understanding-llms/](https://imbrooklyn.dev/books/understanding-llms/).

The [September 13 release record](docs/releases/2026-09-13-parts-ii-vi.md) documents the publication of all completed draft chapters and the Python primer. Earlier author validation records describe the draft state at the time they were written; this release record supersedes their publication-status statements.

## Authoring

Book pages live in matching locale directories:

```text
src/content/docs/
├── en/
└── zh-hans/
```

Planned chapters begin with a stable route, title, description, sidebar metadata, and `draft: true`. To publish a chapter:

1. Replace the placeholder body in both locale files.
2. Remove `draft: true` and add `published: YYYY-MM-DD` to both files.
3. Run `pnpm ci:build`.
4. Commit and push this repository.
5. Manually run the `Deploy to GitHub Pages` workflow in `imbrooklyn/imbrooklyn.github.io`.

No deployment workflow or cross-repository credential is required here. The website workflow checks out this public repository and publishes the combined static artifact.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the chapter contract and [docs/implementation-plan.md](docs/implementation-plan.md) for the publishing architecture.

## Local development

```sh
pnpm install
pnpm dev
```

The production path is `/books/understanding-llms/`; the Astro development server applies the same base path locally. Open the local URL printed by Astro because it selects the next available port when `4321` is already in use.

## Commands

- `pnpm dev` starts the local Starlight site, including draft pages.
- `pnpm validate:content` checks bilingual pairs, frontmatter, filenames, and draft parity.
- `pnpm check` runs Astro and TypeScript checks.
- `pnpm build` creates the production site in `dist/` and excludes drafts.
- `pnpm ci:build` runs the complete validation and build pipeline.

## License

Original prose is CC BY-SA 4.0. Code is Apache-2.0. See [LICENSE.md](LICENSE.md).

## Part I: first public edition

Chapters 1–4 form the first public edition, dated September 10, 2026, with numbered worked examples, complete static data comparisons, six shared figures, summaries, and 35 exercises with visible solutions per language. Read the [English edition](https://imbrooklyn.dev/books/understanding-llms/en/ch-01/) or [Chinese edition](https://imbrooklyn.dev/books/understanding-llms/zh-hans/ch-01/). Chapters 5–39 and Primer-PY were subsequently released on September 13, 2026. Chapters 54–57 were released on September 15, 2026. Chapters 40–53, Primer-HTTP and the online extension remain web drafts. The prerequisite project sources are included; the companion service runs locally. See the [Part IX publication record](docs/releases/2026-09-15-part-ix.md).

For a passage that needs a clearer explanation, submit [reader feedback](https://github.com/imbrooklyn/understanding-llms/issues/new?template=reader-feedback.yml). Use the separate erratum template for specific corrections.

The [blueprint](docs/part-i-blueprint.md), [primary-source ledger](docs/part-i-research.md), [fixture card](data/part-i/README.md), and [validation record](docs/part-i-validation.md) document scope and evidence. All fixtures are original teaching constructions. Numerical code and independent expected values support author verification; the reader does not need to operate controls or run code.

Run `pnpm test` for numerical checks, `pnpm validate:part-i` for bilingual contracts, and `pnpm validate:language` for public documentation and comments. With the development server running, use `BOOK_PREVIEW_URL=http://127.0.0.1:<actual-port> pnpm test:browser` for desktop/mobile verification, including JavaScript-disabled reading. Complete `ci:build` before starting the final preview. If Astro serves old rendered content after a renderer change, stop your own preview, remove the generated `.astro/data-store.json`, and restart it.

Public documentation and code comments are English. The textbook and its localized figures, examples, and navigation remain bilingual. This edition is web-only; it does not include a PDF.

## Part II: foundations and CPU practice

Chapters 5–10 and Primer-PY now contain complete bilingual manuscripts, shared numerical/text fixtures, static figures, visible exercises and answers. They are included in the September 13, 2026 release. Start with Chapter 5 core, then the Python primer, the Chapter 4 character N-gram notebook, NumPy shapes and the training practice.

The [practice guide](code/part-ii/README.md) covers the five executed notebooks and CPU environment. The [continuing KA-0 project](code/knowledge-assistant/README.md) retains Keyword, BoW Count and TF-IDF on one frozen collection; Chapter 10 adds separate static/NNLM comparisons. Review the [blueprint](docs/part-ii-blueprint.md), [research ledger](docs/part-ii-research.md) and [validation record](docs/part-ii-validation.md). `pnpm validate:part-ii` is included in `ci:build`; `BOOK_PYTHON=<environment-python> pnpm test:cpu` runs actual CPU training checks.

## Part III: recurrent sequences and attention

Chapters 11–14 continue from fixed windows through recurrent states, BPTT and gates, Seq2Seq timelines, and a complete cross-attention calculation. Both languages include seven shared static diagrams, fixed failure comparisons, and 21 transfer exercises with visible answers per language. These pages are included in the September 13, 2026 release.

The [practice guide](code/part-iii/README.md) reproduces the supplied sequence diagnostics and explains the two executed CPU notebooks. The code reuses Part II arithmetic and the existing notebook runner; the Chapter 10 comparison inputs and continuing knowledge-assistant baselines are preserved. See the [blueprint](docs/part-iii-blueprint.md), [primary-source ledger](docs/part-iii-research.md), [fixed data](data/part-iii/README.md), and [validation record](docs/part-iii-validation.md) for assumptions and actual evidence.

`pnpm validate:part-iii` runs inside `ci:build`. Use `BOOK_PYTHON=<environment-python> pnpm test:part-iii:cpu` for the sequence behavior checks and `BOOK_PYTHON=<environment-python> pnpm notebooks:part-iii` for fresh notebook execution. The existing `pnpm test:browser` entry now also covers every Part III language page at both viewport sizes, including static reading without JavaScript.

## Part IV: Transformer mechanisms and Mini GPT

Chapters 15–21 contain complete English/Chinese manuscripts with ten shared static figures, explicit Q/K/V and mask calculations, a complete block, architecture/target comparisons, tokenizer merge and round-trip evidence, and visible transfer exercises and answers. All fourteen pages are included in the September 13, 2026 release.

The [mechanism guide](code/part-iv/README.md) and [Mini GPT guide](code/mini-gpt/README.md) run locally on CPU. MG-1 connects raw text to logits/loss; MG-2 supplies actual training/validation curves, small locally trained checkpoints, verified continuation/fresh-process repeats, and original favorable and unfavorable generation traces. Three [executed notebooks](notebooks/part-iv/README.md) use the shared runner. The existing knowledge-assistant and NNLM baselines are preserved.

Read the [blueprint](docs/part-iv-blueprint.md), [primary-source ledger](docs/part-iv-research.md), [fixture card](data/part-iv/README.md), [Mini GPT data card](data/mini-gpt/README.md) and [validation record](docs/part-iv-validation.md). `pnpm validate:part-iv` runs in `ci:build`; `BOOK_PYTHON=<environment-python> pnpm test:part-iv:cpu` runs the behavior tests and `BOOK_PYTHON=<environment-python> pnpm notebooks:part-iv` executes fresh kernels. The shared browser entry includes desktop/mobile, theme, language-switch, local-link and no-JavaScript checks for the new chapters.

## Part V: modern LLMs and KA-1

Chapters 22–33 now connect data provenance, scaling, block and architecture choices, training resources, internal evidence, generation, inference and serving to a frozen evaluation contract. All 24 language pages are included in the September 13, 2026 release. Twelve shared static figures, assigned resource/trace worksheets and three CPU notebooks accompany the text; core reading needs no execution or account.

KA-1 extends the existing assistant project and compares the retained MG-2 step-50 and step-600 configurations under one bilingual contract. All 144 attempts and nine-query lexical baselines are retained. Both configurations are rejected for the stated assistant use. The [English selection report](docs/ka1-selection-report.md) separates actual measurements, author review, estimates and dated documentary inspection of optional external candidates.

Run `pnpm validate:part-v`, `BOOK_PYTHON=<tested-python> pnpm test:part-v:cpu`, and `BOOK_PYTHON=<tested-python> pnpm notebooks:part-v`. The new content and numerical checks run in `pnpm ci:build`; the shared browser entry covers every Part V language page at desktop/mobile sizes, light/dark figures and no JavaScript. See [practice setup](code/part-v/README.md), [blueprint](docs/part-v-blueprint.md), [research](docs/part-v-research.md) and [actual validation](docs/part-v-validation.md).

## Part VI: adaptation decisions

Chapters 34–39 now provide complete bilingual instruction/preference/reasoning training, runtime budget, capability diagnosis and low-rank adaptation lessons. Six shared static figures, fixed candidates and independent numeric expectations support two executed CPU notebooks. The continuing KA-1 project adds a real 144-generation paired format comparison: literal English matching improves on one checkpoint, while semantic quality remains unchanged and both candidates remain rejected.

Run `pnpm validate:part-vi`, `BOOK_PYTHON=<tested-python> pnpm test:part-vi:cpu` and `BOOK_PYTHON=<tested-python> pnpm notebooks:part-vi`. The static and numeric checks join `ci:build`; the shared browser entry covers all twelve pages at desktop/mobile sizes, both figure themes and without JavaScript. See [practice](code/part-vi/README.md), [blueprint](docs/part-vi-blueprint.md), [research](docs/part-vi-research.md), [validation](docs/part-vi-validation.md) and [KA-1 adaptation decision](docs/ka1-adaptation-report.md). All twelve pages are included in the September 13, 2026 release.
