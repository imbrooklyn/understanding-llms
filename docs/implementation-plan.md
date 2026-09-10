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

The September 10, 2026 release covers bilingual CH-01–CH-04 following explicit publication authorization. It produces no PDF and makes no PDF-layout investment. Later chapters remain drafts; future releases require their own editorial review and authorization. Public documentation and code comments are English; the book and its associated localized content remain bilingual. See CONTRIBUTING.md for the editorial contract.

## Content lifecycle

1. Create matching locale files with stable frontmatter and `draft: true`.
2. Complete both bodies and review technical equivalence.
3. Only when publication is authorized, remove both draft flags and give both files the same `published: YYYY-MM-DD` date.
4. Validate filenames, bilingual pairs, publishing state, numerical assets, and the independent book build.
5. The author manually runs the main site's Pages workflow to publish the combined source.

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
- An authorized release includes the main-site deployment and live-site verification of the published routes, navigation, search, and feedback links.
