# Understanding Large Language Models from the Ground Up

The source repository for a web-first bilingual open textbook published at [imbrooklyn.dev/books/understanding-llms/](https://imbrooklyn.dev/books/understanding-llms/).

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

Chapters 1–4 form the first public edition, dated September 10, 2026, with numbered worked examples, complete static data comparisons, six shared figures, summaries, and 35 exercises with visible solutions per language. Read the [English edition](https://imbrooklyn.dev/books/understanding-llms/en/ch-01/) or [Chinese edition](https://imbrooklyn.dev/books/understanding-llms/zh-hans/ch-01/). Later chapters remain drafts and are excluded from production.

For a passage that needs a clearer explanation, submit [reader feedback](https://github.com/imbrooklyn/understanding-llms/issues/new?template=reader-feedback.yml). Use the separate erratum template for specific corrections.

The [blueprint](docs/part-i-blueprint.md), [primary-source ledger](docs/part-i-research.md), [fixture card](data/part-i/README.md), and [validation record](docs/part-i-validation.md) document scope and evidence. All fixtures are original teaching constructions. Numerical code and independent expected values support author verification; the reader does not need to operate controls or run code.

Run `pnpm test` for numerical checks, `pnpm validate:part-i` for bilingual contracts, and `pnpm validate:language` for public documentation and comments. With the development server running, use `BOOK_PREVIEW_URL=http://127.0.0.1:<actual-port> pnpm test:browser` for desktop/mobile verification, including JavaScript-disabled reading. Complete `ci:build` before starting the final preview. If Astro serves old rendered content after a renderer change, stop your own preview, remove the generated `.astro/data-store.json`, and restart it.

Public documentation and code comments are English. The textbook and its localized figures, examples, and navigation remain bilingual. This edition is web-only; it does not include a PDF.
