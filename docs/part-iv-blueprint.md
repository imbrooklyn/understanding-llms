# Part IV content blueprint

Status: manuscript and practice implemented; acceptance evidence is maintained in `part-iv-validation.md`. Scope: Chapters 15–21, both languages, MG-1 and MG-2. All new learning pages remain drafts. No publication, commit, deployment, or Part I revision is authorized by this work.

## Starting state and dependencies

The workspace contains separate book and main-site repositories. The book already has uncommitted Part II/III prose, code, data, figures, validation, and Primer-PY; those are the starting state, not disposable scaffolding. The eight published Part I pages and their fixed assets are preserved. A task-start file-hash inventory is stored outside the repository for regression comparison. Historical validation records describe earlier runs; current results belong in `part-iv-validation.md`.

The audit read the master plan Sections 2–10, the corresponding private Chinese plan, CONTRIBUTING, the implementation plan, the chapter configuration, all eight Part I bodies, Part I author/release records, the fourteen target placeholders, Chapters 5–8 and 13–14 in both languages, Primer-PY, and the Chapter 22 boundary. It also inspected shared code, fixture cards, renderer, validators, browser tests, and production draft filtering.

Chapters 5–7 already explain row-vector multiplication, `[B,T,C]`, logits, row Softmax, mean loss over scored events, gradients, and the update loop. Chapter 8 distinguishes normalized search keys from original text. Chapter 13 implements the recurrent state-collision example; Chapter 14 implements unscaled cross-attention with supplied queries. Primer-PY has actual Python/NumPy/PyTorch practice. None is merely a title placeholder. The new text will briefly recall these conventions where used. The small additional Python bridge is the meaning of a class, `nn.Module`, registered parameters, and tensor reshape/transpose; it belongs at the corresponding Chapter 17/20 code, not in a replacement Primer.

There is no existing Mini GPT implementation to claim or extend. Part IV will add one continuing project under `code/mini-gpt/` and `data/mini-gpt/`, with Part-specific mechanisms under `code/part-iv/` and `data/part-iv/`, and executed notebooks under `notebooks/part-iv/`. Existing knowledge-assistant baselines and NNLM remain intact. The existing static `book-figure`, automatic heading numbering, KaTeX, localized navigation, and draft filtering are sufficient. A narrowly scoped curve renderer extension is permitted only if the existing renderer cannot read the new measured series.

## Common teaching and evidence contract

English is the technical baseline; each chapter is completed and checked before its Chinese counterpart is composed. Both editions share heading-depth anchors, mathematics, inputs, numerical evidence, figure identifiers, exercises and visible explanations of answers. Chinese is independently reread before the second bilingual comparison. Chapters distinguish author-chosen teaching values, independently derived values, locally measured results, and claims from papers. No authored probability table is called an experiment.

Row positions run from first to third in prose; Python uses indices 0–2. Shapes are ordered dimensions, not semantic proofs. Scores and probabilities are dimensionless; cross-entropy uses natural logarithms and nats per scored target. Decimal tables disclose rounding; full precision lives in the fixed data. Q/K/V names are introduced after the products, and do not imply a database, intention, or trustworthy memory. Architecture, objective, training stage, and product interface remain separate axes.

Each chapter contains a motivated problem, a baseline, a complete numbered example with explicit rules, a failure or changed condition, a useful mechanism and its limits, a summary, transfer exercises, visible worked answers, and annotated primary references. Figures show values, visibility, operations, or state transitions; they do not merely repeat a list of terms. All learning evidence remains present with JavaScript disabled.

## Chapter 15: make each position consult the sequence

- Question: how can a position choose other positions when the queries and stored representations come from the same input?
- Recall: Chapter 14 had decoder queries and encoder states. Here the source is one matrix, with a separate learned projection for each role.
- Baseline and example: three positions, two coordinates; `X=[[1,0],[0,1],[1,1]]`, `W_Q=I`, `W_K=[[1,1],[0,1]]`, `W_V=[[1,0],[1,2]]`. These are authored teaching parameters, not trained red/key features. Show every matrix from X through Q/K/V, the nine dot products, division by square root of 2, three row normalizers, and the weighted value sums. Expand at least one element of every operation and account for every axis.
- Independent evidence: express probabilities with `r=exp(1/sqrt(2))`, then evaluate independently and compare every NumPy element within a declared tolerance. A changed V leaves weights unchanged but changes output; a changed K can alter weights. Column normalization fails the per-query mixture interpretation.
- Figure/table: one numerical flow with parameter double borders; full score, weight, and output tables. Explain transpose and scale after the concrete problem they solve. Scaling is variance control under assumptions, not a bound or an overflow cure.
- Exercises: new query calculation, transposed-axis diagnosis, changed-value evidence, scaling assumptions. Answers retain calculation steps.
- Handoff: the mechanism currently lets every position see every other position; that includes an answer in a next-token training example.

## Chapter 16: control visibility and combine several mixtures

- Question: which positions may contribute to a prediction, and why allow more than one projection?
- Baseline: apply causal and padding visibility to Chapter 15's exact score matrix. Define visible/forbidden in words and a table before choosing a Boolean convention. Set forbidden logits to negative infinity before row Softmax. Include the diagonal because the current input predicts the next token.
- Failure: a deliberately supplied future-copy score matrix accesses the shifted target and gives a misleadingly low loss on held-out rows too. It is a constructed oracle, not learned skill. Perturb future input and test prefix-output invariance in real code. Key padding, query padding, and ignored loss events have different responsibilities. Valid all-masked rows raise an error; padded queries explicitly produce zero and do not count in loss.
- Multi-head example: two one-coordinate heads projected from the same three-by-two input. Compute independent causal mixtures, concatenate in a stated order, then apply a nonidentity two-by-two output projection. Generalize to `[B,H,T,d]`, with conventional `C=H*d`, and explain the transpose before matrix multiplication.
- Figure/table: visibility grid and a value-carrying head/concatenation/output trace. Neither a head index nor a heatmap establishes a human concept or a causal explanation.
- Exercises: a padded batch, future leakage, diagonal mistake, head permutation with and without compensating output weights. CPU tests target these observable failures.
- Handoff: attention still lacks order information, a path preserving the old representation, normalization, and a per-position nonlinear transform.

## Chapter 17: assemble a complete block

- Question: what is missing from attention alone when it must serve as one reusable layer?
- Baseline: a reordered input without positional information is equivariant under the same permutation, when its visibility is also permuted. Causal visibility changes the premise and must not be silently ignored.
- Example: add a small authored position table; trace one two-coordinate row through residual addition, population-variance LayerNorm, and a specified two-layer ReLU FFN. Explain epsilon, learned scale/offset, the last-coordinate reduction axis, and the FFN's shared weights across positions. Supply an independent scalar-loop block calculation beside vectorized NumPy.
- Architecture: a complete pre-norm block `x + Attention(LN(x))`, then `r + FFN(LN(r))`; contrast post-norm by writing its actual order. Positional addition occurs before the block; a final norm in Mini GPT follows the block. Equal residual shapes are necessary, while broadcastable but semantically wrong operands are rejected.
- Figure/code mapping: position, Q/K/V, split heads, score/mask, mixture, output projection, both additions, both norms, FFN, final shape. A CPU single-block forward asserts each boundary. Explain code objects only as needed.
- Limits/exercises: shape error, wrong normalization axis, shared FFN vs cross-position mixing, pre/post order, finite learned position table. RoPE, RMSNorm, and SwiGLU remain Chapter 25 topics.
- Handoff: the block is reusable, but visibility and prediction tasks produce different model families.

## Chapter 18: choose architecture and objective separately

- Question: for the same short red-key sentence, what can a position see and what must the model predict?
- Three explicit teaching records: BERT-style masked input with bidirectional visible positions and a missing-token target; GPT-style right-shifted next-token targets and triangular visibility; T5-style sentinel span corruption, encoder visibility, causal decoder visibility, and decoder-to-encoder visibility. Specify source/target lengths and that a sentinel sequence is not a verbatim reconstruction of original positions.
- Compare four independent axes: encoder/decoder structure, MLM/causal/span-denoising objective, pretraining/post-training stage, and a product name or chat UI. Original-paper choices are examples, not definitions of all descendants.
- Task decision: compare fixed-label classification, completion without future text, and source-conditioned revision on the same key task. State a feasible choice and a rejected assumption; no universal quality ranking without common data and evaluation.
- Figure/table: visible information and prediction targets in each family; annotated choice table with conditions. No fabricated benchmark or historic inevitability.
- Exercises: classify an unfamiliar combination, diagnose leaked source targets, distinguish objective and architecture, propose a fair task comparison.
- Handoff: any family still needs a versioned mapping between text and vocabulary rows.

## Chapter 19: obtain a vocabulary from data

- Question: how can the hand-written Chapter 3 vocabulary be replaced without making the text/model interface ambiguous?
- Hand BPE: disclose a tiny word-frequency corpus, initial character symbols, an explicit end-of-word marker, adjacent-pair counts including frequencies, lexical tie-breaking, and merge count. Print every selected pair and the complete intermediate segmentation. Learned merges are replayed by rank at encoding time; they are not recomputed from a new sentence.
- Distinguish training/encoding rules, original WordPiece vs the official BERT longest-match implementation, and SentencePiece as software supporting more than one model. Do not present an unofficial WordPiece training heuristic as the universal algorithm.
- Mini GPT interface: a separately named deterministic UTF-8 byte BPE, all 256 base bytes, reserved BOS/EOS IDs, no normalization, no merges across records or special tokens, deterministic tie rules and merge budget. Train on training records only. Unknown code points remain representable as bytes; generated arbitrary bytes need not form valid UTF-8. Report strict round trip for ASCII, Chinese, emoji, and combining characters, and a contrasting lossy normalization/unknown-token fixture.
- Compare measured token lengths on the same texts, not language-wide claims. Record algorithm version, ordered vocabulary, merge ranks, normalization, special tokens, training-data hash, and artifact hash. Swapped IDs with the same vocabulary size remain incompatible with a checkpoint.
- Figure/exercises: merge count transition, raw text/bytes/IDs/back trace, tie-breaking and normalization counterexamples, tokenizer migration decision.
- Handoff: freeze the tokenizer and record boundaries before building windows and shifted targets.

## Chapter 20: MG-1, raw text to loss

- Question: can one follow every value-producing module from a text record to a scored next-token distribution?
- Freeze a small original corpus, record-level train/validation split, tokenizer artifact, context length, seed, dtype, CPU configuration, architecture, and target-loss mask. No windows span records or mix splits; BOS and EOS policies are explicit. Show raw text, its complete IDs for one short record, x/y shift, padding, and count of scored targets.
- Model: one small decoder-only pre-norm block with learned token/position embeddings, explicit Q/K/V matrix products, causal/key masks, concatenation/output projection, ReLU FFN, final norm, untied LM head, and mean cross-entropy. Use PyTorch tensors/autograd, not a packaged Transformer or pretrained model. Map every named code boundary to a complete structural figure and actual shape log.
- Numerical evidence: a full readable actual forward trace with selected coordinate/logit values and one target's probability/loss; an independent all-zero-logit check gives `ln(V)`. A loop implementation checks an attention slice. A future-perturbation test and padded-loss invariance check test semantics beyond shapes.
- Practice bridge: what a class instance and `nn.Module` store, where parameters are registered, why IDs are integers, why softmax normalizes keys while loss normalizes vocabulary, and how batch/heads reshape works. Primer-PY remains the practice prerequisite.
- MG-1 artifact: runnable CPU command, frozen configuration, parameter count, raw input/IDs/shapes/logits/loss, hashes, and tests. Forward success is not evidence of learning.
- Handoff: what changes after backward/update, and what evidence separates memorization from improvement on held-out records?

## Chapter 21: MG-2, train, restore, and inspect generation

- Question: what would make a small training run reproducible and its apparent success interpretable?
- Run bounded actual CPU training on the unchanged Chapter 20 model and split. Log train/validation loss at stated steps with evaluation mode and denominator; show the real curves and a fixed step-selection rule. Treat repeated inspection of validation as development, not a final independent test.
- Save three distinct things: model-only state, full resume state (optimizer, step, random generators, configuration and data/tokenizer identity), and a milestone evidence bundle. Use locally generated small checkpoints or a completely specified regeneration command; never download unknown weights.
- Resume experiment: compare uninterrupted and interrupted/resumed parameters, optimizer state, next batch, losses, and generation under the same stack. A second fresh run checks repeatability. Document versions, CPU threads, dtype, seed, environment, actual elapsed time, and cross-stack limitations. A seed alone is insufficient.
- Generation: prefill a fixed prompt, inspect the last-position logits, choose a token under greedy and two declared sampling settings, append, and rerun. Store the complete chosen-token trace, probabilities, context, stops, and decoded output. Separate training RNG from sampling RNG. Distinguish EOS from the context/output cap and invalid-byte decoding.
- Failure/limits: inspect a held-out changed red/blue or 600/750 condition and repetition/memorization. Outputs are evidence for this tiny corpus, not general language understanding, policy reliability, or order execution authority.
- Exercises and Part checkpoint: reconstruct a whole block, diagnose visibility/target/tokenizer mistakes, identify what a checkpoint can restore, assess a curve, and design a controlled test. Full visible answers. Final handoff asks about data, scale, training stages, and evaluation in Chapter 22 without teaching that chapter prematurely.

## Research and validation plan

Before drafting technical claims, read supporting sections of the Transformer, BERT, GPT, T5, BPE/subword, and SentencePiece primary papers, official BERT tokenization code, and maintained NumPy/PyTorch mask/tensor/checkpoint documentation. Record exact links, versions, sections, assumptions, and non-claims in `part-iv-research.md`. Library mask conventions are examples, not mathematical definitions.

Build independent expected values before implementation comparisons. Add Part IV bilingual/content/number checks and mechanism tests to the actual CI entry. Run the core project in a declared clean CPU environment and execute each notebook from its first cell with a fresh kernel. Save real output and provenance hashes. Use a task-owned preview port, then run the complete browser suite with `BOOK_PREVIEW_URL` set explicitly. Cover fourteen pages, both viewport sizes, both themes, formulas, figure contents, language switching, anchors, local links, and no-JavaScript reading. Inspect rendered screenshots, not only source. Finally run production build/draft exclusion and any relevant integration build without deployment. Record failures as well as successful reruns; never prefill success.
