# Part IV validation and editorial record

`as_of: 2026-09-13`  
`last_verified: 2026-09-13`

The seven bilingual manuscripts, MG-1/MG-2 practice, editorial reviews and final build/browser/visual acceptance are complete in the stated environment. New chapters remain `draft: true` with no publication dates. This record distinguishes this task's actual runs from historical Part I–III evidence. No commit, push, publication or deployment is authorized or performed.

## Audit, prerequisites and preservation

The workspace contains separate book and main-site repositories. The book began with uncommitted Part II/III work; the main site began clean. No applicable AGENTS.md or Sites hosting configuration was found. Before authoring, the required master-plan sections 2–10, corresponding private Chinese plan, CONTRIBUTING, implementation plan, book configuration, all eight published Part I bodies, Part I author/release records, prerequisite and target bodies, Primer-PY, Chapter 22 boundary, practice assets, renderer and validation/release logic were read.

Chapters 5–8 and 13–14 and Primer-PY are complete implementations, not assumed placeholders. Part IV briefly recalls their shape, loss, text-boundary and learning-loop conventions. Chapter 20 adds the small class/Module/parameter-registration bridge at the point of use; no additional Primer page or rewrite was needed. Modern position/norm/FFN variants remain Chapter 25's responsibility. Chapter 22 remains the lifecycle handoff. Existing knowledge-assistant Keyword, BoW Count and TF-IDF comparisons and NNLM/sequence practice are preserved.

A SHA-256 inventory of 244 existing content, asset, code, author and test files plus starting Git status was saved outside the repository at `/private/tmp/part-iv-start-snapshot.json`. The final comparison found changes only in the fourteen target bodies, the notebook runner's additional Part IV option, the narrow curve-renderer extension and the implementation-plan addition among those inventoried files. All eight published Part I bodies and their inventoried figures/data/code/release records match the starting bytes. Existing Part II/III manuscript and project assets remain unchanged, apart from the shared runner/curve additions with their previous behavior preserved. Package scripts, targeted Chinese configuration titles and English maintenance documentation have intentional Part IV additions. The private author prompt was not copied into the public repository.

## Independent evidence and CPU checks

`attention.json` was established from hand-expanded integer products and symbolic scalar exponential ratios before the NumPy comparison. The separate `reference.py` uses scalar loops for the block. Tests perturb values, future inputs, padding and batch companions; the masked oracle is explicitly authored evidence, not learned performance. JavaScript independently checks matrix products, normalization, the first block row, all hand-BPE pair counts/ties, architecture visibility, byte reconstruction, forward coordinates/loss, step selection and generation append/stop behavior.

A fresh environment at `/private/tmp/llm-book-part-iv-venv` uses Python 3.12.10, NumPy 2.0.2 and PyTorch 2.7.0. The six direct requirements and full installed dependency list are in `code/part-iv/requirements.txt` and `requirements-tested.txt`. The first pip attempt encountered restricted sandbox network/proxy access; the approved retry succeeded. An initial NumPy trace used an existing same-version Part II environment while installation proceeded, then was regenerated in the clean environment. The clean runs use float64 CPU, one thread for Torch and deterministic algorithms; no GPU or remote model is involved.

Commands executed with the clean environment's Python, from the book root:

```sh
python code/part-iv/run.py --write
python code/part-iv/tokenizer_example.py
python code/mini-gpt/forward.py
python code/mini-gpt/run.py
BOOK_PYTHON=/private/tmp/llm-book-part-iv-venv/bin/python pnpm test:part-iv:cpu
```

The CPU entry passed all 23 tests: 10 attention/mask/head/norm/block checks, 9 Mini GPT behavior checks and 4 tokenizer checks. Coverage includes both opposite official PyTorch Boolean-mask adapters, intentionally wrong future visibility, valid all-masked rejection, padded query handling, independent scalar block/attention, analytic uniform loss, target shift/EOS/record boundaries, finite gradients and updates, checkpoint identity rejection/continuation, seeded generation and all stopping/invalid-byte cases. These are implementation checks, not evidence of general language ability.

The NumPy maximum absolute errors against independent expectations are 1.1102230246251565e-16 for weights and 2.220446049250313e-16 for output, below 1e-12. MG-1 has 13875 parameters and 32 scored events in its two-record batch. Mean loss is 5.670998865509144; the independent scalar route gives 5.670998865509145. The zero-logit baseline is ln(291)=5.673323267171493. Full inputs/intermediates remain in shared JSON, and key computations are visible in both chapter bodies.

## Actual MG-2 run and retained failures

The reference run was recorded at `2026-09-12T16:46:59.173889+00:00`, September 13 in Asia/Shanghai, on macOS 26.5.2 arm64. Its fixed corpus has 24 training and 8 validation records, 521/178 scored events, vocabulary size 291, context 64, width 16, two heads, one pre-norm ReLU block and no dropout. Initialization/batch/sampling seeds are 1729/101/31415. Adam settings, data/tokenizer/config identities and source hashes are recorded in `data/mini-gpt/training-run.json`.

All 600 updates, batch choices and pre-update losses are retained. Complete-split evaluation occurs at 0,50,...,600. The first minimum validation loss selects step 50 (2.405571231866604). At step 600 train loss is 0.15959935516353005 while validation is 4.068374448042549. Both selected and final weights remain available; the full curve exposes overfitting instead of replacing the run with an appealing output.

The main training section took 1.716514500323683 seconds; resumed training 0.7022572499699891; fresh-process training 1.7269503329880536; the complete pipeline 4.767545832786709. Earlier local repeats had different elapsed times, including a 6.245-second pipeline, but the same states/curves. Durations vary with startup and cache conditions and are not a benchmark or guaranteed runtime. Installation time is separate.

Continuation from the step-300 checkpoint exactly matches steps 301–600, all remaining curve points, final model/optimizer/batch-RNG/global-Torch-RNG state digests and the next batch. A fresh process starting from initialization exactly matches all 600 steps and 13 curve points as well as final state and selection. The four locally generated checkpoint files total 966540 bytes. Model-only snapshots, optimization-state checkpoints and the whole milestone evidence bundle have separate documented responsibilities. Earlier curve/selected-weight records are retained separately because an optimization checkpoint alone does not restore the historical best-validation selection.

The original no-space colon prompts produced unfavorable outputs. These remain unchanged in `generation-baseline.json`; separately versioned aligned/changed-clue probes were added after observing the tokenizer boundary, without changing corpus or selection. The final model produces `red.` on the aligned familiar red template and incorrectly produces `red.` after an explicit change to blue. Both snapshots fail the explicit 750-value probe. The original reversed-limit prompt never supplies the new value; its authored expected suffix is underdetermined, and both bodies explicitly reject treating that mismatch as an explicit-update violation. The full baseline and later generation traces, including probabilities, IDs, raw bytes and stop reasons, are retained.

## Notebook execution

The existing Part II runner now accepts `--part part-iv`, preserving its previous default and Part III branch. It creates one fresh kernel per notebook using the requested interpreter. The initial sandboxed execution could not bind Jupyter's loopback kernel sockets; the approved execution succeeded. No notebook was accepted merely because it opened.

Actual command:

```sh
/private/tmp/llm-book-part-iv-venv/bin/python code/part-ii/run_notebooks.py --part part-iv
```

| Notebook | Executed code cells | Observed duration | Result |
| --- | ---: | ---: | --- |
| `01-attention-and-block.ipynb` | 3 | 0.9515 s | Passed |
| `02-tokenizer-boundaries.ipynb` | 3 | 0.7645 s | Passed |
| `03-mini-gpt.ipynb` | 3 | 5.7956 s | Passed |

The third notebook performs actual forward/training/continuation/fresh-process/generation work in a temporary directory and preserves the reference files. Sequential counts, outputs, code hashes, imported dependency/input hashes and environment are in `data/part-iv/notebook-execution.json`. Implementation explanations and code are English; example strings are loaded from shared content resources. All three notebooks have no allowed or recorded cell errors.

## Editorial reviews

The first review read the full English technical baselines in chapter order and checked each against the primary-source ledger, independent scalar evidence and actual project records. It checked the source-position versus vocabulary axes, scaling assumptions, inclusive diagonal, key/query/loss masking, valid empty rows, two-head ordering, population-variance LayerNorm, pre/post order and final norm, T5 sentinels and separate matrices, tokenizer learning versus encoding, frozen IDs, one-time target shift, valid-event loss, continuation state and diagnostic scope. No industrial model accuracy or paper timing is presented as this book's measurement.

The second review read all seven Chinese bodies independently from beginning to end, then compared facts, limitations and structure to English. Revisions clarified the attention table's weight columns, replaced an opaque output-projection example title, explained likelihood and affine transformation where needed, improved Chinese word-count and task-contract phrasing, and added the complete 16-coordinate MG-1 input row to both editions so the mean/variance denominator can be checked directly. The Chapter 21 continuation-selection distinction was added to both editions. Chinese inference/reasoning are explicitly model running and problem-solving reasoning. The fourteen bodies share heading depth/order, formulas, sources, figure order, exercise numbers and visible answers; checks supplement, rather than replace, those readings.

There are 42 transfer exercises with independent visible explanations per language, chosen by mechanism rather than copied from Part I's count. All ten figure sources have both localized alternatives/captions/labels and original CC BY-SA 4.0 credits. Code has Apache-2.0 notices. No interactive teaching controls, collapsed answers or copy buttons were restored.

## Build, browser and production checks

- Baseline book `pnpm ci:build` passed before Part IV edits; that historical task-start pass is not final acceptance.
- The final post-editorial/figure book `pnpm ci:build` passed on September 13: content/language/Part I–IV checks, 13 existing Part II and 9 Part III Python checks, 13 Node tests including the new measured-curve test, Astro check with zero errors/warnings/hints, and production build/draft filtering.
- `pnpm validate:part-iv` is integrated into `ci:build`. It checks all seven draft pairs, anchor/math/caption/source parity, visible answers, independently calculated numerical evidence, the actual curve/trace tables, rendered figure content and run/checkpoint/notebook provenance.
- Main-site `pnpm ci:build` passed using the approved local IPC exception needed by tsx; it produced seven main-site pages. The final `pnpm compose:site` and `node scripts/check-draft-output.mjs ../imbrooklyn.github.io/dist/books/understanding-llms` passed after the final book build. No main-site source change or deployment was needed.
- Book production has 21 HTML pages and 20 decoded Pagefind fragments. The existing generalized checker verifies all 112 draft/supporting routes and their links are absent from HTML/XML, JS/JSON/maps and decoded search fragments, including all fourteen new pages. Published Part I remains indexed. This covers sidebar/contents links, RSS and sitemap as production output, not only route existence.

The task-owned preview used `BOOK_PREVIEW_URL=http://127.0.0.1:4325`, selected after inspecting occupied ports 4321–4324. The first sandboxed preview/browser attempts failed before page testing; approved retries ran Chrome locally. Existing preview processes were not stopped. The first actual full browser run passed 102/104 tests and detected literal Markdown emphasis markers around a Chinese parenthesized term in Chapter 21. Adding proper delimiter spacing fixed both desktop/mobile failures; the next complete suite passed all 104 tests in 3.7 minutes.

Desktop is 1440×1000 and mobile is 390×844. The 32 Part IV cases visit all fourteen pages in both viewport projects, checking chapter numbers/anchors, same-chapter language switches, internal links, formulas, static evidence/answers, complete figure labels/credits, actual parameter double borders, both themes and local overflow. Four of these cases visit every Part IV page with JavaScript disabled. The remaining 72 cases retain Part I–III/Primer coverage. Static curve markers and all measured coordinates are checked separately.

Visual inspection of rendered screenshots found a Chapter 17 vector's final digit wrapping onto its own line. Figure resource strings now permit breaks after commas, preserving each numerical value. This change uses existing styling rather than a page redesign. The next browser attempt detected stale generated markup despite restarting the preview, so that run was interrupted. Only the task-owned preview was stopped, `.astro/data-store.json` was removed, and the preview was restarted on the same port. An HTTP check confirmed the corrected shape and vector strings before rerunning the suite. The final post-cache-refresh command below passed all 104 tests in 3.7 minutes with exit status 0. All 32 Part IV cases passed, including the four cases that each traverse seven chapters without JavaScript.

Final browser command, run from the book root:

```sh
BOOK_PREVIEW_URL=http://127.0.0.1:4325 pnpm test:browser
```

Actual screenshots from that final run were inspected, not just source JSON or a previous build. The review covered all ten figures in both languages, both viewport sizes and both themes (80 figure views); all fourteen page tops at both sizes; the two editions' visible answer sections; displayed equations; and the MG-1 coordinate and MG-2 failure tables. Right-edge screenshots confirm the end of long formulas and the curve's step-600 label/unit are reachable inside their local scrolling area without widening the page. The mobile diagrams stack in reading order, six-place vector values remain intact, neutral parameter double borders are visible, and the monochrome curve distinguishes series by line and marker shape. JavaScript-disabled mobile answer screenshots were also inspected, including rendered mathematics. No further visual defect remained in this review.

Playwright regenerates the ignored `test-results/` screenshots and report on each run. Raw local command logs and contact sheets used for visual review remain outside the repository under `/private/tmp/part-iv-*`; they are local audit aids, not third-party assets or manuscript dependencies. Repeating the documented entries regenerates the checks and screenshots. The final preservation inventory again found no modification to published Part I or unrelated prerequisite bodies/assets; the main-site source tree remains clean.

## Limits

The core practice is fully local CPU work in the stated clean stack. Cross-platform, cross-version and GPU reproduction have not been measured and are not promised to match bitwise. SentencePiece/BERT/GPT/T5 are researched architecture/tokenizer references, not models trained or benchmarked here. The tiny template-related split and qualitative diagnostic additions cannot establish broad language or update-following ability. No paid API, model account, PDF, EPUB, live order operation, public release or deployment was used.
