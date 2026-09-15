# Complete core publication — September 15, 2026

## Scope and preserved evidence

The user explicitly authorized publication of every completed chapter and the HTTP primer. This release adds Chapters 40–53 and Primer-HTTP in both languages: 30 reading pages dated September 15, 2026. All 57 core chapters and both primers are now public. Only the unfinished multimodal extension remains draft. The inventory is `data/releases/2026-09-15-complete-publication.json`; it supersedes the scope of the earlier September 15 Part IX release without rewriting that historical record.

The 30 newly promoted pages change publication metadata only. Chapters 54 and 57 remove the temporary partial-publication notes and restore links to Chapters 46 and 49 and Primer-HTTP. All four corresponding language bodies match their originally accepted draft bodies byte for byte; their September 15 publication dates remain. Chapters 1–39 and the Python primer retain their previous dates and content. A private pre-change SHA-256 inventory of 804 tracked files verifies that existing code, data, notebooks, figures and measured authoring evidence are unchanged.

The bilingual home pages, roadmap and changelog now describe the continuous reading path. Parts VII and VIII validators use the existing valid-publication-state helper instead of requiring drafts; all content, numeric, behavioral, notebook and evidence-hash assertions remain. The independent publication test covers all 60 chapter/primer/extension identifiers, both languages and the exact previously published dates. No renderer, search dependency, diagram, service implementation or hosting configuration changes in this release.

## Actual local verification

Environment: macOS 26.5.2 arm64; Node 23.10.0; pnpm 11.24.0; Python 3.12.10 selected by `BOOK_PYTHON=/tmp/llm-book-part-ix-venv/bin/python`; Astro 7.3.1; Playwright 1.63.0; Chrome 153.0.8010.36. Verification was performed on September 15, 2026. The existing clean Python environment uses the pinned project dependencies. Publication does not rerun training or regenerate historical notebook measurements.

| Check | Observed result |
| --- | --- |
| Book `BOOK_PYTHON=/tmp/llm-book-part-ix-venv/bin/python pnpm ci:build` | Passed all applicable Part I–IX content and language validators, CPU suites, 26 Node tests, Astro checks, production build and draft-output inspection |
| Final `pnpm build` after restoring one original Markdown blank line | Passed; 131 HTML files including the root redirect, 130 indexed language pages, and 57 chapter entries in each language feed |
| `node scripts/check-draft-output.mjs` | Passed; both extension routes remain excluded from output and links |
| Main-site `pnpm ci:build` and `pnpm compose:site` | Passed; all 390 book files match the combined copy byte for byte |
| Combined artifact inspection | 15,282 same-site links, assets and fragments across 137 HTML pages; zero unresolved references |
| Initial production browser run | 98 passed and 2 failed: the same Chinese compound-word search case at desktop and mobile sizes; no reading-page failures |
| Final production browser run | 100 checks passed and 2 documented compound-query cases failed as expected; zero skips or unexpected failures, 2.4 minutes. Playwright reports all 102 outcomes as expected |
| Final `pnpm test` and `pnpm check` after the browser-test update | 26 Node tests passed; Astro checked 68 files with zero errors, warnings or hints |
| `git diff --check` | Passed for the publication changes |

The owned local static server exposes the combined production artifact at `http://127.0.0.1:4326`. Other existing preview servers were left running. Browser coverage uses 1440×1000 and 390×844 viewports and includes all 38 language pages for Chapters 40–57 and Primer-HTTP, no-JavaScript reading, visible answers, localized figures in light and dark themes, formulas, heading numbers, same-chapter language switching, anchors and whole-page overflow. Release tests inspect the home pages, all 59 available roadmap destinations, the two excluded extension routes, and actual search navigation to Chapter 53 and Primer-HTTP.

Rendered English and Chinese home pages, HTTP figures and real search results were visually inspected, including mobile captures. These checks use the production artifact; the earlier draft-authoring screenshots and notebook execution records remain separate historical evidence. Local browser output retains the initial failures and the final expected-failure traces in distinct run directories.

```sh
BOOK_RELEASE_CHECK=1 \
BOOK_PREVIEW_URL=http://127.0.0.1:4326 \
pnpm test:browser tests/part-vii.browser.ts tests/part-viii.browser.ts \
  tests/part-ix.browser.ts tests/release.browser.ts \
  --output test-results/complete-release-final-20260915 --reporter=list
```

## Known Chinese search limitation

The initial failures are a reproducible search limitation, not missing chapter output. Pagefind 1.5.2 indexes the Chinese term for “tenant” as one word; Chrome 153's `Intl.Segmenter` splits that query into two words. The actual API query for “tenant isolation” therefore returns Chapter 57 and omits Chapter 53, even though Chapter 53 contains the exact phrase in its title. Searches for the Chinese terms for “isolation” and “supply chain” return Chapter 53; its English title query also succeeds. Inspection of the generated Chinese fragment confirms that Chapter 53 is indexed.

This diagnosis was checked against the actual generated fragment, direct browser API results and verbose query normalization. Pagefind's [multilingual documentation](https://pagefind.app/docs/multilingual/) explains automatic CJK query segmentation, and the [pinned v1.5.2 query implementation](https://github.com/Pagefind/pagefind/blob/v1.5.2/pagefind_web_js/lib/coupled_search.ts#L544-L571) shows its use of `Intl.Segmenter`. Sources were last verified on September 15, 2026. These explain the mechanism; the concrete mismatch is an observation of this build and browser, not a claim about every browser or Chinese phrase.

The release smoke test uses the working “supply chain” query to check discovery of the newly published chapter. A separate expected-failure test preserves the desired “tenant isolation” behavior in both viewports, with the limitation explicitly named. An unexpected pass will require revisiting that annotation. This is not recorded as a repaired search bug or as an all-passing search audit. No chapter wording, keyword metadata or search engine is changed to conceal the failure. The complete roadmap remains available independently of search.

## Deployment and limits

The existing [website Pages workflow](https://github.com/imbrooklyn/imbrooklyn.github.io/actions/workflows/deploy.yml) records the exact book revision and owns deployment. Local results above precede deployment; the corresponding workflow run is the authoritative deployment record. Read the [Chinese roadmap](https://imbrooklyn.dev/books/understanding-llms/zh-hans/roadmap/), [English roadmap](https://imbrooklyn.dev/books/understanding-llms/en/roadmap/) or [HTTP primer](https://imbrooklyn.dev/books/understanding-llms/zh-hans/primer-http/).

The companion assistants remain local demonstrations. This publication does not expose a Python service, perform real order actions, migrate hosting, or produce PDF/EPUB output. Earlier limitations in model selection, small evaluation sets, accessibility coverage, fault drills, privacy and human responsibility remain in the original validation records and project cards. The Chinese compound-query limitation above remains unresolved.
