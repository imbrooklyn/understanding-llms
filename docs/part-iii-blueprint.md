# Part III content blueprint

as_of: 2026-09-12

## Audit and scope

The workspace contains separate book and main-site Git repositories and a private Chinese master plan. No applicable AGENTS.md or Sites hosting configuration was found. The book already has uncommitted Part II work: completed CH-05–10 and Primer-PY, numerical functions, CPU training, five executed notebooks, the continuing KA-0 project, a static curve renderer and validation. Preserve that work. The eight published Part I bodies, their data and figure sources are the accepted reading baseline and remain unchanged. At the initial audit, CH-11–14 and CH-15 contained placeholders. Ignore their obsolete instruction to remove the draft flag on completion.

Read before authoring: master-plan sections 2–10 and the corresponding private curriculum contracts; CONTRIBUTING.md; implementation-plan.md; book.mjs; all eight current Part I bodies; Part I blueprint/research/validation and September 10 release record; complete bilingual CH-05–07, CH-10, Primer-PY and CH-11–15; shared figures/data/code, Part II evidence and tests; Markdown renderer, CSS, content lifecycle, browser configuration and production filters. Historical passing results are not current test results.

No blocking prerequisite is missing. First-use bridges will explain recurrent time indices, local sensitivity products, elementwise gates, source/target indices and source-position normalization. Primer-PY already supplies the optional programming prerequisite; do not rewrite or duplicate it. Reuse the existing book-figure lanes, neutral double-border parameter nodes, KaTeX, automatic numbering and draft filtering. Computed hidden states use vector nodes, since the existing state node means an application record. No new learning control, renderer, website design or publication change is needed.

Deliver eight complete bilingual draft bodies, chapter-local shared diagrams and licenses, one connected Part III practice package, frozen inputs and independent expectations, executed notebooks, and English research/validation records. No new KA milestone is prescribed here: retain and regression-check the existing Keyword, Count and TF-IDF collection instead of constructing another assistant. The Part III increment is inspectable sequence failure analysis leading toward Mini GPT's attention component.

## Chapter arguments

### CH-11: retain information outside a fixed window

- Question: can the earlier red/blue key clue influence a prediction after it leaves a two-token window?
- Baseline: reuse CH-10's exact five-symbol alphabet and nine-token diagnostic pair; add a versioned three-token short pair. The task and color criterion are identical for both methods. Supplied window and recurrent parameters are demonstrations, not fitted models or quality benchmarks.
- Mechanism: a two-coordinate ReLU RNN, identity input/output matrices, half-identity recurrent matrix, zero hidden bias, initial zero state and output bias [1/8,0]. Show the shared parameters in a time table before writing recurrence. Calculate red/key/is fully, including each input, previous state, new state, logits and softmax outputs; substitute blue.
- Failure: retain exact long-pair states and probabilities. The RNN can distinguish the distributions, but its fading clue loses to the fixed red output bias. This differs from identical window inputs and from literal rounding to zero. Parameter sharing does not mean three independently trained cells.
- Figures: three unrolled uses, explicit state arrows and one shared parameter set. Tables separate state changes in execution from parameter updates after backward computation.
- Exercises: changed retention, sequence boundary reset, same-window impossibility, transient state versus a stored application record, sequential scheduling.
- Practice: deterministic complete logs and matched short/long failures on CPU; no training claim. Handoff: how a late loss reaches an earlier operation.

### CH-12: separate signal transport from gradient transport

- Question: a late target was wrong; how strongly can its loss influence an early calculation?
- Baseline: local factors 1/2 and 3/2, with distances measured in recurrent edges. Show exact products at 0, 1, 2, 4, 8 and 16; these are derived sensitivities, not measured training curves.
- Mechanism: unroll CH-11's positive scalar path, h=[1,1/2,1/4], and a new explicit squared terminal loss. Backpropagate -3/4, -3/8, -3/16; sum the two nonzero shared-weight contributions to -3/4. Independently check the polynomial loss and finite differences. Explain nonlinear derivatives and multiple vector paths without an unexplained matrix theorem.
- Gates: explain sigmoid retain/write/expose roles, an additive LSTM cell path, a complete supplied scalar LSTM update, and Cho-convention GRU retain/reset/candidate computation. State which gate values are supplied and which values are calculated. Distinguish the original LSTM from the later forget-gate formulation. Saturation, overwrite, finite capacity and recurrent scheduling remain limits.
- Representation map: static train row versus context-dependent occurrences; ELMo's separately directed pretrained stacked LSTMs, concatenated contextual states and task-specific layer mixture. Explain the default frozen feature use and distinguish it from BERT's jointly contextual masked Transformer orientation only.
- Figures: backward factors/contribution routes and contextual representation flow. The gate paths are compared in Table 12.3 and the fully calculated scalar examples. Exercises calculate a new gradient/distance/gate case and diagnose an invalid ELMo next-token evaluation.
- Practice: static distance table and optional numerical reproduction, including a finite-difference independent path. Handoff: a sequence representation used to generate a different sequence.

### CH-13: distinguish target feedback from source compression

- Question: how can a complete source message produce a differently ordered/length target?
- Task: a tiny explicitly tokenized translation of red/blue key plus punctuation. Source and target vocabularies, BOS/EOS and candidate order are fixed. The target contains red, key, period, EOS.
- Mechanism: a supplied two-coordinate ReLU encoder with all embedding rows and weights exposed. Compute three states, the last of which is zero for both colors. Show source encoding, teacher-forced target right shift and generated-prefix timelines separately. Distinct encoder/decoder parameter sets each share within their own time axis.
- Complete trace: an authored conditional table predicts blue first, but teacher forcing supplies red at the second step. Free generation supplies blue and then door. Print every conditional row and the four scored target factors; explain exactly when the input diverges and how loss counts EOS.
- Two limitations: teacher-forced likelihood describes probabilities on reference prefixes, not actual error-free generation; exposure bias is an input-distribution difference, not proof of inevitable cascading error. Separately, two sources with identical final encoder state cannot be distinguished by a decoder receiving only that state. Finite-dimensional state is not a theorem that all real-number encoders collide; this encoder's collision is explicitly calculated.
- Exercises: right shift, EOS scoring, recovery versus cascade, hidden-state reset, information collision. Practice analyzes/replays the supplied trace without pretending to train a translation system. Handoff: keep intermediate encoder states accessible.

### CH-14: calculate one source read for each output position

- Question: when writing a color versus an object, can the decoder consult different source positions?
- Mechanism: reuse the exact CH-13 computed encoder states. Supply two decoder probe states separately; do not mislabel them as a learned trajectory. Define unscaled dot-product scores throughout this chapter (Luong-style score, not Bahdanau's additive parameterization). Show [ln 2,0,0] and [0,ln 2,0], exponentials, denominators, source-position weights and coordinatewise weighted sums. Define every dimension and distinguish attention weights from vocabulary probabilities. Concatenate context with previous target embedding and decoder state as a declared decoder interface.
- Interventions: remove individual stored source states, renormalize and compute all contexts. A specified downstream scalar readout stays unchanged after removing the largest-weight state, establishing a concrete limit of weight-as-explanation. Separately delete raw source tokens and recompute the encoder; deleting key changes later states, unlike removing only its stored slot. Keep query fixed for the controlled intervention and disclaim a full-generation causal result.
- Costs and boundary: source-state storage scales with source length; score comparisons with source times target length. Source and target recurrences still impose serial paths even when teacher-forced targets are known. Cross-attention shortens access to a retained source state, without making a recurrent encoder or decoder parallel. No complete Transformer, multihead mechanism or mask implementation here.
- Figures: the two numerical reads and the retained recurrence plus new read path. Exercises cover a zero query, changed scores, deletion denominator, downstream evidence and scheduling. End with the Part III concept checkpoint and visible explanations.
- Practice: shared scalar code and optional NumPy replication, checked against exact fractions and independently computed expressions. Handoff: CH-15 changes access within a sequence and introduces learned Q/K/V projections and scaled dot products explicitly.

## Evidence, bilingual workflow and acceptance

Research original Elman, long-dependency/gradient work, LSTM and forget gates, GRU/encoder-decoder, Seq2Seq, recurrent attention and ELMo before drafting their claims. Record actual read locations, publication/version, source links, limitations and access failures. Original constructed values are separate from outputs derived by rules, actual local execution metadata and any paper measurement. No paper accuracy number is imported into this book's results.

Write each complete English technical baseline before Chinese. Then independently read Chinese for clear actors, references, transitions and ordinary Mainland usage; recheck technical equivalence against English. Mirror explanatory repairs in both languages. Keep anchors, formulas, candidate order, example/table numbers, exercises, answers and citations aligned. All author records, README files, code/comments and notebook implementation notes are English; bilingual labels live in chapter Markdown and explicitly identified figure/content resources.

Acceptance will check meaningful numerical invariants, failure cases and matched source data; actual clean-CPU execution; fresh notebook kernels with no errors; bilingual/static contracts; current Part I/II regression; pnpm ci:build; all eight pages on desktop/mobile with light/dark figures and JavaScript disabled; same-chapter language switching and anchors; production route/link/search/RSS/sitemap exclusion. Record results only after execution. No commit, push, publish, deployment, PDF or EPUB is authorized.
