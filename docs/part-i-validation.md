# Part I validation record

Revision date: 2026-09-09. Scope: CH-01–CH-04 in both languages, explanatory assets, static authoring infrastructure, and English repository documentation. This record describes the pre-publication draft review. No commit, push, publication, or PDF generation occurred during that phase. The separately authorized September 10 release is documented in [the release record](releases/2026-09-10-part-i.md).

## Editorial result

The four arguments were rebuilt around task criteria, generation/training state, finite text representation, and progressively revised count models. Every fixed comparison and solution is directly visible. Six shared figures support the prose. Each language has 35 exercises with reasoned solutions: 8, 8, 9, and 10 by chapter. English was written first for each chapter, followed by equivalent Chinese content. CH-05 and later chapter bodies and primers were not rewritten.

The structural reference is OSTEP's problem, assumption, baseline, counterexample, mechanism, and tradeoff progression. This identifies the editorial method, not a claim of equivalent teaching quality. Software checks establish structure, numerical agreement, and rendering; they cannot demonstrate reader comprehension.

## Reader-facing presentation revision

All 57 chapter pairs now use localized chapter labels in frontmatter. Chapter openings display a smaller chapter label above the title; sidebar entries use the number, a middle dot, and the title. Both roadmaps and Part I prose references use natural chapter wording. Filenames, URLs, assets, section anchors, and draft status remain unchanged. Later chapter bodies retain their placeholders.

Table 1.3 now compares five named cases instead of displaying evaluation/failure/risk identifier triples. References throughout Chapter 1, including exercises and solutions, use case names, worked-example numbers, and first/second record descriptions. Original machine IDs and numerical fixtures are unchanged; their mapping to the textbook is recorded in the dataset README. The table uses a labeled, keyboard-focusable scroll region on narrow screens to preserve readable columns.

All eight Part I chapters end with a localized `References` section. Each entry now explains the work's contribution and its connection to the chapter argument. Primary source URLs and bilingual source coverage are preserved. Contribution rules, the blueprint, content validation, and existing browser checks were updated to enforce these conventions.

## Content and bilingual review

The Chinese prose in all four chapters was subsequently rewritten from the English meaning rather than the English sentence structure. The revision covers descriptions, section headings, arguments, captions, table labels, all 35 exercises and their solutions, and reference annotations. The six diagrams' Chinese descriptions and labels were revised as well, including the localized illustration-renderer strings. Chapter 3's Chinese title and its roadmap/configuration entries now name embedding vectors in Chinese. The glossary wording and English contribution rules were updated to match this editorial standard.

During that earlier Chinese-only revision, a pre-revision snapshot confirmed that English chapter files and all fixed dataset JSON files were byte-for-byte unchanged. Chapter code fences, numeric table cells, link targets, and inline-code value sets were preserved. Figure geometry and every non-Chinese JSON field were unchanged. Existing bilingual checks verify matching formula content, heading structure, example/table numbering, sources, and exercise counts. The semantic review checked sampling versus parameter updates, unknown-symbol information loss, model/tokenizer compatibility, cosine versus truth, sequence termination, zero versus undefined probabilities, smoothing redistribution, and finite-context limits. These checks support fidelity; stylistic quality still requires reading the revised prose.

- CH-01 preserves five groups and ten authored records, with task-specific criteria, source/action evidence, and a complete initial evaluation/failure/risk register. The six-out-of-ten calculation and duplicate-weighting exercise are explicitly about constructed records, not measured model accuracy.
- CH-02 follows one sentence through representations, selection, and append; adds complete target alignment; and displays the full assigned function and all six state comparisons. Assumed probabilities are separate from embeddings and empirical measurements. A forward pass or a loss alone does not establish a parameter update.
- CH-03 states the complete encoding rule and table, traces both languages, explains an irreversible collision, analyzes consistent ID permutation and model compatibility, and calculates directional similarity. The zero vector remains undefined for cosine. Initial, contextual, and retrieval representations are distinct.
- CH-04 begins with a Unigram failure, constructs all nine Bigram events, derives conditional and complete-sequence probabilities, and distinguishes the exact chain-rule product from the finite-history approximation. EOS, zero versus undefined, smoothing redistribution, seeded generation, six diagnostic settings, and fixed-window/sparsity limitations remain explicit.
- New transfer exercises use changed strings, changed corpora, alternative smoothing, prefix/completion distinctions, sampling order, and criterion-dependent evaluation. Independent fractions and generator states were checked against the pure implementation where applicable.
- Both languages have matching heading levels, worked-example/table captions, shared figure IDs, display formulas, inline-formula sets, source URLs, exercise numbers, and visible solutions. Terminology and chapter dependencies were reviewed; Part I requires neither Python nor a notebook.

## Explanation revision for readers without a computing background

The subsequent revision addresses missing prerequisites and abrupt conceptual transitions in all eight chapter files. Each chapter's English baseline was revised before its Chinese counterpart. The scope includes complete explanatory steps, rather than wording changes alone:

- CH-01 defines everyday input/output and application/model roles before using them. Replaceable tickets introduce chance, fractions, decimals, and sampling intervals. The five cases progress from answer criteria to dependence on clues, external sources, and action evidence.
- CH-02 relates supplied input, stored parameters, and calculated results to one multiplication example. It explains why numerical IDs need a separate lookup, how brackets and vector dimensions are read, how probability interval endpoints are obtained, how one sentence supplies several training targets, and why measuring error does not update parameters. Table 2.7 and its references use descriptive scenario names, mapped to unchanged fixture IDs in the data README.
- CH-03 explains reusable pieces and table lookup before the complete traces. Code points and normalization receive immediate definitions. The geometric section introduces axes, signed coordinates, straight arrows, squared length, square roots, and the interpretation of the cosine ratio before applying its boundary cases.
- CH-04 motivates boundary markers, observed frequency, and model names through the counting example. Conditional probability is explained using a separate ticket bag for each row; tickets are returned after each draw. The sequence product is expanded back into the three steps of `ab`. The generation table focuses on selections; all original LCG constants and states remain visible in a following reproduction paragraph. Smoothing, likelihood, and sparsity are tied to their preceding problems. MG-0 is identified as a project milestone, distinct from a saved model checkpoint.

A separate snapshot comparison confirmed that all five fixed JSON datasets and all six figure assets remain byte-identical in this revision. Existing display formulas, primary-source URL sets, and figure sequences are preserved. The added arithmetic examples were checked directly: replacement preserves sampling probabilities, one half of two thirds is one third, the cosine interpretation uses the horizontal unit vector, and add-one increases the four-candidate row total by four. Bilingual checks pass for matching structure, formulas, captions, sources, and all 35 exercises and solutions. No new test merely asserting prose wording was added.

Manual preview review covered the new Chinese probability explanation on desktop, English ID lookup on mobile, Chinese coordinate introduction on desktop, Chinese conditional-probability explanation on mobile, and English counting/generation figure on desktop. The served pages contained the new text and had no page-wide horizontal overflow. The complete existing browser suite also passed for both languages, both viewports, and JavaScript-disabled reading. This is editorial and rendering review, not a measured novice-reader comprehension study.

## Static infrastructure and public language

The four browser labs and their client runtime were removed. Unsupported `book-lab` syntax now fails compilation rather than hiding content. Native answer disclosures were replaced by visible solution sections. Framework-generated code-copy buttons are disabled, so there are no buttons, inputs, selectors, forms, or disclosures inside chapter content. Navigation, search, and language controls remain site features.

Heading numbering and stable bilingual anchors come from the Markdown AST. KaTeX produces locally styled HTML/MathML. Shared JSON supplies original figures, including an SVG coordinate diagram for cosine. Licensing and localized descriptions accompany each figure. Numerical code is retained for author verification.

Public plans, README files, research/validation records, data documentation, and comments use English. The former `*.zh.md` public planning documents were replaced with English `*.md` files and their references updated. The full master plan retains all 57 chapter contracts, bridge resources, project milestones, and conceptual boundaries. Localized book strings remain textbook content. `validate:language` checks public Markdown outside the textbook and source comments.

## Executed checks

Environment: Node v23.10.0, pnpm 11.24.0, lockfile-managed dependencies, local Chrome. Browser viewports: desktop 1440×1000 and mobile emulation 390×844.

| Check | Result |
| --- | --- |
| `pnpm validate:content` | Passed: 57 bilingual chapter pairs and supporting pages |
| `pnpm validate:language` | Passed: English public documentation and source comments |
| `pnpm validate:part-i` | Passed: bilingual contracts, formulas, sources, figures, numbering, static content, exercise/solution matching, and fixture provenance |
| `pnpm test` | Passed: 12 numerical and authoring tests, including new transfer-exercise calculations and rejection of removed lab syntax |
| `pnpm check` | Passed: 0 errors, 0 warnings, 0 hints |
| `pnpm ci:build` | Passed after the explanation revision; 13 production pages built and indexed |
| Draft isolation | Passed: 114 draft chapter routes/links absent from production; unpublished fixture payloads absent from client JS/JSON/maps |
| Main-site `pnpm compose:site` | Passed during the preceding content revision; not repeated for this local book presentation revision; no deployment |
| `BOOK_PREVIEW_URL=http://127.0.0.1:4323 pnpm test:browser` | Passed after the explanation revision: 20/20 in 33.6 seconds |
| `git diff --check` | Passed |

The browser suite covers eight chapter/locale combinations on both viewports, plus four JavaScript-disabled checks traversing all chapters. It verifies a single main title, numbered headings, absent learning controls, visible solutions, described/licensed figures, concrete lookup/coordinate/counting contents, math output, no leaked Markdown fences or emphasis delimiters, no page-wide horizontal overflow, no page errors or external HTTP requests, and same-chapter language switching. Screenshots capture page openings, each figure, equations, solutions, and dark-mode figures.

Manual visual review included both language openings, a mobile Chinese chapter opening, the English training/inference comparison, the Chinese count-to-probability figure, the mobile coordinate diagram in light/dark presentations, and mobile Chinese cosine and English conditional-probability formulas. No PDF proof was created. This is Chrome mobile emulation, not a claim of testing physical devices or every browser/assistive technology.

The preceding revision's first browser run detected Expressive Code's default copy buttons inside otherwise static chapters. The installed plugin option was checked, the buttons disabled, and the full build and browser suite rerun successfully. During the presentation revision, the old development process served cached sidebar labels and chapter bodies; its browser run was stopped, the generated development content cache cleared, and the task's preview restarted before the successful full run. After the Chinese prose and figure revision, that task preview was refreshed again. The explanation revision replaced only that task-owned preview and cleared its generated content cache before verification. Final preview process: PID 14236.

Presentation screenshots were reviewed in both languages and at desktop/mobile sizes. The mobile comparison table initially squeezed Chinese case names into one-character lines. A minimum table width and local scroll region corrected that issue without page-wide overflow. A separate mobile check verified that the table can scroll to its final column in both languages.

The Chinese prose revision was also reviewed in the refreshed preview: the desktop Chapter 1 opening, desktop training/model-run diagram, mobile Chapter 3 opening, and mobile counting/generation/evaluation diagram all displayed the revised text. Existing checks passed for both languages, both viewport sizes, and JavaScript-disabled reading.

## Local review

- [English CH-01](http://127.0.0.1:4323/books/understanding-llms/en/ch-01/)
- [Chinese CH-01](http://127.0.0.1:4323/books/understanding-llms/zh-hans/ch-01/)

Use the Part I sidebar for CH-02–CH-04. Language switching preserves the chapter. Drafts are intentionally available only in development; if the server is later restarted on another port, use the URL printed by Astro. Local screenshots and browser reports remain ignored in `test-results/` and `playwright-report/`.
