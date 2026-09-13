# Parts II–VI and the Python primer — September 13, 2026

## Authorization and scope

The user authorized publishing all current unpublished chapters on September 13, 2026. The repository contains complete draft manuscripts for Chapters 5–39 and Primer-PY: 36 bilingual pairs, or 72 new reading pages. These pairs now use `published: 2026-09-13`. Chapters 1–4 retain `published: 2026-09-10` and their accepted bodies. Chapters 40–57, Primer-HTTP and the multimodal extension contain only placeholders; their 40 language routes remain drafts, as required by the existing chapter publication contract.

The release includes the previously completed, uncommitted Parts II–VI prose and their supporting figures, code, fixed data, notebooks, research and validation records. It preserves all prior experiment outputs, checkpoints, failure cases and licenses. Earlier author records retain their historical draft/publication statements and saved hashes; this release supersedes their publication status without rewriting their measurements. No new model training or technical-content revision is claimed for this release.

## Publication changes

- Publish the 72 complete language pages without changing their bodies.
- Update the two home pages, roadmaps and changelogs. Roadmap titles now use the actual configured titles for every newly published chapter.
- Replace draft-only assertions with valid lifecycle checks; require matching publication dates for both languages, including supporting lessons.
- Keep all content, numerical, figure and notebook checks. Extend production checks to require every public reading page in routes and search, and every published chapter in its locale feed.
- Use the established website-owned GitHub Pages workflow. No alternate host or page redesign is introduced.

## Verification

- Book `pnpm ci:build`: passed all Parts I–VI content and numerical checks, 21 Node tests, Astro diagnostics (zero errors and warnings), production build and publication-output checks. Local versions were Node 23.10.0, pnpm 11.24.0 and Astro 7.3.1.
- Production output: 93 HTML pages, including 92 language pages indexed by Pagefind. Both RSS feeds contain 39 chapters with the correct source release dates. All 40 remaining draft language routes, links and search entries are excluded.
- Main website `pnpm ci:build` and `pnpm compose:site`: passed. All 306 composed book files matched the book output byte-for-byte. Inspection of the combined 99 HTML pages resolved 9,036 same-site links, assets and fragments without errors.
- Production browser verification used the actual combined artifact at `http://127.0.0.1:4326`, served by a task-owned Python HTTP server. The existing 184 chapter/primer cases passed on desktop 1440×1000 and mobile 390×844, including both languages, figure themes, language switching, local overflow and JavaScript-disabled reading.
- Eight release cases verify both home pages, all 39 roadmap links and the Python primer, all placeholder HTTP exclusions, and actual English/Chinese search leading to Chapter 39. All eight passed after correcting the test's textbox locator. The initial combined run reported 190 passes and two desktop search-test failures because the installed search input has the textbox role rather than `type="search"`; the focused corrected run passed 8/8. The 192 distinct cases are therefore covered across the complete run and the focused recheck. The application search implementation did not require a change.
- Actual home, roadmap and search screenshots were inspected in both languages and viewport sizes. Generated screenshots and command logs remain local ignored verification artifacts.
- SHA-256 comparison against the pre-release workspace confirmed that all 72 promoted chapter/primer bodies are unchanged after reversing only the metadata replacement. Published Part I sources also remain byte-identical.
- The staged publication-edited files pass `git diff --cached --check`. A whole-index check also reports pre-existing Markdown hard line breaks, raw log spacing and blank EOF lines in the previously uncommitted evidence/code. Those bytes are preserved to retain frozen execution hashes; they are not rewritten or represented as new release defects.

The initial Astro preview attempt rejected a background-server flag combination before starting a service. Serving the combined static artifact directly resolved that local preview setup issue. No unrelated preview service was stopped.

## Deployment record and boundaries

The source is published through the existing [website Pages workflow](https://github.com/imbrooklyn/imbrooklyn.github.io/actions/workflows/deploy.yml), whose run records the exact book revision. The local checks above precede that deployment; the workflow is the authoritative record of its completion. The reading entry points are the [Chinese edition](https://imbrooklyn.dev/books/understanding-llms/zh-hans/) and the [English edition](https://imbrooklyn.dev/books/understanding-llms/en/).

Publication does not change the limitations in the original author records. In particular, the KA-1 candidate systems remain rejected for the specified assistant use, optional external/GPU/PEFT training is not claimed, and fixed teaching calculations are not model-quality benchmarks. This release adds no PDF, EPUB, external messaging or new hosting platform.
