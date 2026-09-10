# Contributing

## Chapter contract

Every chapter should contain:

1. A concrete question and its link to the surrounding chapters.
2. A self-contained explanation of the mechanism.
3. A minimal numerical example, diagram, or observable experiment.
4. At least one failure case and a clear applicability boundary.
5. A core-understanding self-check and answers.
6. References, with concise explanations of their relevance to the chapter.
7. A practical exercise when the topic calls for one.

Start headings inside chapter Markdown at `##`; the page title comes from frontmatter. Keep English and Chinese chapter filenames identical. Both versions must preserve technical meaning, equations, conclusions, risks, and dependencies.

## Language of public repository material

Textbook content, including its figures, examples, exercises, and localized navigation labels, is bilingual. All public material outside that content must be English: README files, contribution rules, plans, research and validation records, dataset documentation, code identifiers and comments, notebook implementation notes, commit messages, and pull-request descriptions. Keep localized book strings in clearly identified content resources. Do not add Chinese explanations to public code comments or documentation.

## Publishing a chapter

Draft files are visible during `pnpm dev` but excluded from production. A chapter is publishable only when both language files:

- have real content in place of the placeholder;
- no longer contain `draft: true`;
- contain the same `published: YYYY-MM-DD` release date;
- use the same chapter identifier;
- pass `pnpm ci:build`.

The main website owns production deployment. After pushing book content, manually run its Pages workflow.

## Assets

Put reusable source assets in `src/assets/<chapter-id>/`. Add meaningful alt text to every image and never rely on color alone. Keep source and license information adjacent to third-party assets.

Put notebooks, code, small datasets, and expected outputs in the matching top-level directories. Never commit credentials, restricted data, or unlicensed artifacts.

## Part I authoring infrastructure

Chapter section numbers are generated from the filename and heading levels (`1.1`, `1.1.1`, …), including the page TOC. Write unnumbered headings beginning at `##`; do not skip levels. Both languages use the same structural anchors (`s-1-1`). The frontmatter title combines the localized label returned by `chapterLabel()` with the configured chapter title. The page displays that label on a separate, smaller line; the sidebar uses the chapter number, a middle dot, and the title. Use natural chapter references in prose, such as `Chapter 2` in English and the corresponding localized label in Chinese. Keep filenames, routes, asset IDs, and anchors stable.

Use descriptive case names in the textbook. Within a two-record comparison, refer to the first or second record; when referring across sections, include the case name or worked-example number. Keep machine identifiers such as `G4-A` and `E-G4` in the data and author documentation, not in reader-facing tables. The Chapter 1 case-to-fixture mapping is documented in `data/part-i/README.md`.

Use `References` and its localized textbook equivalent for cited works. Explain what each work contributes and how it connects to the chapter. Add a separate `Further Reading` section only when it provides an additional reading path with a stated purpose; do not create a combined heading by default.

Use `$...$` for inline mathematics and `$$` blocks for display mathematics. KaTeX renders HTML and MathML during compilation; styles/fonts are bundled locally. Keep equations semantically equivalent across languages.

A `book-figure` fenced block containing an asset ID such as `ch-02/token-journey` renders bilingual source data from `src/assets/`. Each figure needs a numbered caption, meaningful alt text, a reference and explanation in the prose, and adjacent licensing information. Figures must make a relationship, state transition, or calculation visible. Tables and worked examples also use chapter-local numbers; write their captions in the source, not as headings.

## Textbook writing standard

The reference for pedagogical organization is [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/), especially its preface and CPU Scheduling chapter. Adopt the progression from a concrete problem through stated assumptions, a baseline, a counterexample, a revised mechanism, and a tradeoff. Do not copy its prose, figures, or distinctive expressions. Technical claims still require relevant primary LLM sources.

- Develop one coherent argument per chapter. Explain why each new concept is needed and how it changes the preceding example. A sequence of definitions or admonitions is not an explanation.
- Specify a worked example completely before calculating: inputs, conventions, variables, and the question to answer. Show the intermediate steps and interpret the result. Distinguish assumed teaching values from measured or derived values.
- Introduce notation with its object, domain, and meaning. Derive formulas from the example and apply them to a second case. Respect prerequisites; do not substitute unexplained names for postponed mechanisms.
- Assume Part I readers have used a chat interface but have not studied computing. Explain the need for an operation before naming it, demonstrate it on the running example, and only then give compact notation. Introduce unfamiliar table conventions, brackets, coordinates, and probability notation where they first matter. A transition should identify the unresolved question left by the previous example. Bound analogies explicitly: sampling tickets are replaced, IDs are labels, and hand-assigned coordinates have no assumed semantic axes. Keep exact reproduction details visible after the main reasoning they support.
- Write the Chinese edition as original Mainland Chinese textbook prose. First establish the English source's facts, logic, qualifications, tone, and terminology; then rebuild the explanation using natural Chinese syntax. Prefer concrete verbs and familiar collocations over noun-heavy phrases, long modifiers, mechanical passive constructions, and literal connectors. Sentences may be split, combined, or reordered, provided all important information and technical distinctions remain intact. Apply this standard to headings, captions, tables, exercises, solutions, and reference annotations as well as paragraphs.
- Include a summary, exercises that require transfer to new cases, and visible, reasoned solutions in separate sections. Use matching exercise numbers and equivalent technical content in both languages. Do not use word counts as a quality criterion.
- **Learning content is static.** Do not add inputs, selects, buttons, forms, custom interactive elements, or collapsed answers. Show all alternatives, fixed experiment results, and solutions in the chapter. Navigation, language selection, and site search remain ordinary site features. `book-lab` is unsupported. Code-block copy controls are disabled as well.
- Keep author verification code and independent numerical fixtures, but do not require a runtime, API, notebook, or UI action to understand Part I. The later programming-primer dependency is unchanged.
- This iteration delivers web content only. Do not generate PDFs or spend time on PDF typography without a new request.

`pnpm ci:build` checks bilingual contracts, numerical fixtures, Astro types, production output, and draft exclusion. Start a development server and run `BOOK_PREVIEW_URL=http://127.0.0.1:<actual-port> pnpm test:browser` for both languages on desktop/mobile, including disabled JavaScript. Browser checks verify static content, equations, figures, and navigation. They cannot certify pedagogical quality. No commit, push, publish, or deployment is authorized by these checks.

After changing Markdown renderers or figure source assets, inspect the actual generated diagram. Astro's development content cache (`.astro/data-store.json`) can retain old rendered HTML even after the build cache is cleared by `astro sync --force`. Stop your own preview process, remove that generated development cache, then restart and verify the new diagram. Do not stop other users' preview processes.
