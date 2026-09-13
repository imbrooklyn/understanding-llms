# Part VI validation and editorial record

As of / last verified: 2026-09-13. Status: complete draft delivery. Chapters 34–39 are complete in both languages; optional model training is explicitly unperformed. No commit, push, release or deployment was made.

## Audit and preserved work

The workspace root is not a Git repository. The book and main site are separate child repositories. No applicable AGENTS.md was found in the workspace or ancestor chain. Existing uncommitted Parts II–V and their continuing Mini GPT and knowledge-assistant projects were retained.

The required master-plan sections 2–10 and corresponding private plan scope, contribution/configuration/implementation files, all eight accepted Part I manuscripts and their records, every target manuscript, the specified bilingual prerequisites, Primer-PY, Chapter 40's scope, KA-1 contracts/code/results and existing rendering/validation/filtering paths were read. Chapters 6–7, 18, 22–23, 29 and 32–33 and Primer-PY are actually implemented. No missing prerequisite or new primer blocks this part. Chapter 40 and later interfaces were not implemented early.

A temporary initial SHA-256 inventory covered 441 non-generated book files. At completion, 422 are byte-identical. The 19 changed initial files are the twelve target manuscripts, four directly relevant maintenance files, book configuration, the illustration dispatch file and the Chinese roadmap. Part I manuscripts, code, data and figures, earlier model/project code, original frozen experiments, the lockfile and shared CSS remain identical to their audited starting state. Other existing Git changes were not reset. Configuration/frontmatter/roadmap changes polish only the four unfinished Chinese titles for Chapters 36–39; IDs, order, routes and published Part I titles remain fixed.

## Deliverables and source review

The twelve draft manuscripts contain complete arguments, worked calculations, counterexamples, numbered figures/tables, summaries, transfer exercises and visible reference answers. Exercise counts follow chapter needs: five each in Chapters 34–38, six in Chapter 39. Six original bilingual figure sources reuse the static lane renderer and its neutral double parameter borders. Chapter 37 adds one bounded static SVG curve branch; it does not add client interaction, new page design or controls.

Shared fixtures, independent expectations and actual mechanism replay are in `data/part-vi/`, with implementation and two executed notebooks in the corresponding code/notebook directories. The actual adaptation stays in the existing knowledge-assistant project. The [adaptation report](ka1-adaptation-report.md) retains rejected options, original gates and failures.

The [English blueprint](part-vi-blueprint.md) preceded research and prose. The [primary-source ledger](part-vi-research.md) identifies original versions, sections/equations/pages, setup and excluded inferences. InstructGPT, DPO, verifier/process-supervision studies, R1, CoT/self-consistency/test-time allocation, continued pretraining, adapters and LoRA/QLoRA were checked beyond abstracts. Official template documentation is dated separately from the dependency-free exercise. No paper benchmark is presented as this book's measurement.

Original narrative, fixtures, figures and recorded outputs use CC BY-SA 4.0; code uses Apache-2.0. Installed dependency license metadata and license-file hashes are in `dependency-licenses.json`. No external checkpoint, paper figure or restricted dataset was copied. Notebook implementation prose, author documents and code comments are English; localized lesson strings are in content resources.

## Actual CPU execution

A fresh environment at `/private/tmp/llm-book-part-vi-venv` used Python 3.12.10, PyTorch 2.7.0, NumPy 2.0.2, nbclient 0.10.2, nbformat 5.10.4 and ipykernel 6.29.5. It installed the pinned Part IV tested stack through the existing Part V requirements; the new Part VI requirements inherit that identical stack. Model generation used one CPU thread and float64 on arm64 macOS 26.5.2.

| Executed command from the book root | Actual result |
| --- | --- |
| `python code/part-vi/run.py --write` with the fresh interpreter | 60 order/cap/method replays, five rejected format mutations, checked preference/verifier/low-rank results; source hashes and real replay timings saved |
| `python code/knowledge-assistant/format_adaptation.py --freeze`, then `--write` | Freeze preceded the new actual 144-generation comparison; all original raw outputs reproduced exactly and all parameters remained unchanged |
| `BOOK_PYTHON=/private/tmp/llm-book-part-vi-venv/bin/python pnpm test:part-vi:cpu` | 17 behavioral tests passed, including another complete 144-output reproduction, invalid UTF-8 preservation and unchanged rejection gates |
| `/private/tmp/llm-book-part-vi-venv/bin/python code/part-vi/run_notebooks.py` | Two fresh kernels; four code cells each; all cells executed in order without allowed errors; 1.041097 s and 1.222037 s in the recorded execution |
| `pnpm validate:part-vi` | Bilingual structures/math/references, direct table-to-evidence bindings, independent numeric checks, source provenance and notebook code/artifact hashes passed |

The actual KA-1 freeze/run times and full traces are immutable project records. Selected English strict passes improve from 0/18 to 6/18; semantic passes remain 6/18, robust semantic cases 2/6. Chinese remains zero; both checkpoints remain rejected. Nine selected-English primary displays change but three historical answers remain wrong. The retained stress condition gains one strict pass without a semantic change. Original disclosed AI-assisted author judgments are transferred only after exact raw-output reproduction; no independent human panel or hidden judge API is claimed.

Keyword 5/9, BoW Count 6/9 and TF-IDF 7/9 were recomputed on the same nine queries in each language. These source-selection counts are separate from the six KA-1 answer cases. Invalid outputs, historical/unknown/approval failures and all seeds remain present.

Hand-derived integer arrays and symbolic expectations preceded implementation. Tests change caps, reverse KL, exercise missing probability support, distinguish lucky totals from valid work, reserve check costs, retain duplicate/rejected candidates and confirm that answer extraction uses text rather than gold metadata. Low-rank output is independently checked through separate paths and a merged matrix, including new inputs and scaling. Fixture-lexer tokens and controller time are never labeled model tokens or serving latency.

## Two editorial passes

The first pass reviewed each English technical baseline against the contract, primary sources and independently derived numbers, then checked bilingual equivalence. It verified target-position mask alignment, selected-token denominators, directional KL, DPO reference ratios, verifier input/output and claim scope, budget/correlation/stopping rules, retained KA-1 denominators and the independent data/objective versus parameter axes.

The second pass read the Chinese manuscripts continuously for natural mainland usage and sufficient nontechnical steps, then returned to the English facts and limitations. It checked pronouns, causal transitions, first-use terminology, captions, table cells, exercise/answer parity and cross-chapter responsibility. This was an author editorial review, not an independent external native-speaker panel.

| Chapter | Specific review outcome |
| --- | --- |
| 34 | The assistant header's prediction is scored; zero prompt loss does not freeze prompt-processing parameters. The terminator and three-target denominator are explicit. Loss-mask terminology was made consistent in the figure. |
| 35 | The sigmoid maps a real difference **to** a probability value; reversed/tied/unsupported labels remain distinguishable. KL is named and separated from a physical distance. Citation delimiters were repaired. |
| 36 | Amount acceptance does not certify C's process or a model's internal computation. Lightman's reward-model training is not mislabeled generator RL. Process/output, format and new-family evidence remain separate. |
| 37 | “Charged” means counted in the declared quota, not a paid API fee. All candidates and verification costs are visible; order repeats are not independent task families. Actual controller milliseconds were added beside counts. |
| 38 | Shorter table headings leave the original→normalized convention in the caption. Exact microsecond timestamps follow the main comparison. Formatting success never becomes a semantic or deployment claim. |
| 39 | Every matrix dimension/product and count has an explained object. The combined output is named; the input figure node is correctly a numerical vector. Five diagnostic axes are explicit. Assigned factors and uniform rounding are not claimed PEFT/NF4 training. |

All twelve sources also pass the actual Markdown/math/figure transformation test. The review repaired Chinese emphasis boundaries by keeping parenthetical English outside the bold Chinese term. Source reading and rendered inspection, rather than word counts or automated checks alone, supported the editorial judgment.

## Browser and visual verification

The task checked listening ports, left the pre-existing services alone, and started its own preview with:

```sh
ASTRO_DEV_BACKGROUND=1 pnpm dev --host 127.0.0.1 --port 4326 --ignore-lock
BOOK_PREVIEW_URL=http://127.0.0.1:4326 pnpm test:browser
```

The observed preview URL was `http://127.0.0.1:4326/books/understanding-llms/`. The full suite passed **184 tests** in 6.8 minutes, including all earlier parts and 28 Part VI cases. Playwright 1.63.0 used desktop 1440×1000 and mobile 390×844.

After the final figure terminology and table refinements, the same entry ran four Chapter 34/39 desktop checks (10.6 s), four Chapter 38 desktop/mobile checks (10.1 s), and four JavaScript-disabled checks across all six chapters and both viewports (12.3 s). These targeted checks supersede the earlier screenshots for the refined material.

Every Part VI page was checked for complete body/answers, one numbered title, stable section anchors, same-chapter language switching, reachable internal links, no lesson controls, no raw delimiters or KaTeX errors, and no whole-page horizontal overflow. Both figure themes were captured; all source labels, captions, alternative text, licenses and parameter border roles were checked. Wide tables, formulas and the budget plot were scrolled locally to their right edges and reset. JavaScript-disabled contexts retained all evidence and visible answers.

Generated screenshots were actually viewed: all six figures in both languages, themes and viewports; bilingual page openings; wide-plot/formula/table endpoints; paired KA-1 results; and visible solutions. Original-resolution contact sheets facilitated comparison. The latest Chapter 34/39 figure and Chapter 38 table captures were viewed after their refinements. No visual acceptance is inferred solely from SVG/Markdown source. Screenshots are local ignored artifacts; the validation manifest records their hashes and supersession choices.

## Failures encountered and resolved

- The first restricted dependency installation could not reach the configured proxy. An automatically approved environment retry installed the pinned stack; no user credential or paid service was needed.
- Jupyter's initial kernel launch was blocked from binding localhost ports. The authorized retry ran both notebooks successfully in fresh kernels. A failed launch was not counted as executed cells.
- The main site's tsx validator initially hit a sandbox IPC-pipe restriction. Its approved retry completed the main build.
- Initial figure fences used JSON objects while the existing plugin expects plain asset IDs. Production filtering had hidden this draft-rendering issue from route generation. Preview exposed it; all twelve fences were fixed and a direct plugin/full Markdown regression test now covers it. The early production-only pass was not treated as draft-page acceptance.
- The first browser run passed 177 cases and failed seven Chinese desktop/no-JavaScript cases on visible emphasis delimiters. Source corrections and a full rerun produced 184 passes. Subsequent limited rechecks cover the final editorial refinements.
- Temporary authoring syntax/marker errors were repaired before the final records/checks. No malformed run or assumed success replaces the actual saved evidence.

No unrelated preview service was stopped or reset. No site redesign or cache-dependent workaround was introduced.

## Production and integration checks

`pnpm ci:build` passed with Node 23.10.0 / pnpm 11.24.0 / Astro 7.3.1. This includes Parts I–VI checks, 19 Node tests, Astro checking (zero errors and zero warnings), the static build and draft-output verification. The book build produces 21 HTML pages. The checker confirms that 112 draft chapter/supporting routes and their links are absent from production HTML/XML and client JS/JSON/maps; decoded Pagefind fragments contain built pages only, including every published Part I chapter. RSS, sitemap and published-page links remain free of new draft routes.

The main-site `pnpm ci:build` passed. `pnpm compose:site` completed without deployment. All 143 composed book files were compared byte-for-byte with the book build; counts match and Part VI routes are absent. `git diff --check` also passed.

## Limits and completion

No required Part VI deliverable remains blocked. No continued pretraining, SFT, RLHF, DPO, RLVR, LoRA or QLoRA model-training benchmark was run. Those optional experiments are not needed to read the mechanisms or to reproduce the completed runtime comparison. The authored candidate pool does not demonstrate real-model scaling or generalization. KA-1 remains a failed teaching assistant, not a validated product. External-model compatibility, GPU behavior and real service latency are not claimed.

The work remains uncommitted in the workspace. All twelve chapters stay `draft: true` without publication dates; published Part I stays published. No PDF, EPUB, public release, push or deployment was produced.
