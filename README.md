# Understanding Large Language Models from the Ground Up

The source repository for a web-first bilingual open textbook published at [imbrooklyn.dev/books/understanding-llms/](https://imbrooklyn.dev/books/understanding-llms/).

## Authoring

Book pages live in matching locale directories:

```text
src/content/docs/
├── en/
└── zh-hans/
```

Each planned chapter already has its final route, title, description, and sidebar metadata, plus `draft: true`. To publish a chapter:

1. Replace the placeholder body in both locale files.
2. Remove `draft: true` and add `published: YYYY-MM-DD` to both files.
3. Run `pnpm ci:build`.
4. Commit and push this repository.
5. Manually run the `Deploy to GitHub Pages` workflow in `imbrooklyn/imbrooklyn.github.io`.

No deployment workflow or cross-repository credential is required here. The website workflow checks out this public repository and publishes the combined static artifact.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the chapter contract and [docs/implementation-plan.zh.md](docs/implementation-plan.zh.md) for the publishing architecture.

## Local development

```sh
pnpm install
pnpm dev
```

The production path is `/books/understanding-llms/`; the Astro development server applies the same base path locally.

## Commands

- `pnpm dev` starts the local Starlight site, including draft pages.
- `pnpm validate:content` checks bilingual pairs, frontmatter, filenames, and draft parity.
- `pnpm check` runs Astro and TypeScript checks.
- `pnpm build` creates the production site in `dist/` and excludes drafts.
- `pnpm ci:build` runs the complete validation and build pipeline.

## License

Original prose is CC BY-SA 4.0. Code is Apache-2.0. See [LICENSE.md](LICENSE.md).
