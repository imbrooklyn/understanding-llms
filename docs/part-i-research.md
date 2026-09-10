# Part I evidence ledger

Research checked 2026-09-08. English is the technical baseline. Only author/publisher papers, the authors' textbook, and official software documentation are used. Papers are linked, not redistributed. All conversations, corpora, vectors, probabilities, and diagrams in Part I are original teaching constructions, not measurements reported by these papers.

| Source | Checked location / claim supported | Use and limit |
| --- | --- | --- |
| [Brown et al., 2020, v4](https://arxiv.org/html/2005.14165v4) | Abstract, §1–2: demonstrations supplied in context without gradient updates | CH-02: context change is not a parameter update; no claim about current products or universal success |
| [Lin et al., 2022, TruthfulQA](https://aclanthology.org/2022.acl-long.229/) | Abstract: false answers can imitate common misconceptions | CH-01: fluent text is insufficient evidence of truth; no historical benchmark percentages used as current capability estimates |
| [Liu et al., 2023, v3](https://arxiv.org/abs/2307.03172) | Abstract: performance changes with location of relevant information | CH-01/04: context availability does not establish effective use; the short color example does not reproduce this study |
| [Lewis et al., 2020/2021, v4](https://arxiv.org/abs/2005.11401) | Abstract: distinction between parametric model and explicit external memory | CH-01/02: external source is a separate system layer; our supplied excerpt is not a complete RAG implementation |
| [Yao et al., 2023, ReAct](https://arxiv.org/abs/2210.03629) | Abstract: generated actions interact with external environments and return observations | CH-01: text, action requests, execution and observed results are distinct; approval rules are the book's own application design |
| [Vaswani et al., 2017](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) | Architecture entry point | CH-02 journey is explicitly a simplified causal Transformer map, not an encoder-decoder reproduction or all-LLM definition |
| [Turpin et al., 2023, v2](https://arxiv.org/abs/2305.04388) | Abstract: visible explanations can misrepresent causes of predictions | CH-02: reasoning text is not a faithful internal trace; no claim that every explanation is false |
| [Sennrich et al., 2016](https://aclanthology.org/P16-1162.pdf) | §3, especially §3.2 and unknown-symbol footnote | CH-03: subword motivation, units need not be words; no BPE training or third-party tokenizer artifacts |
| [Kudo & Richardson, 2018](https://aclanthology.org/D18-2012/) | Abstract: raw-text subword tokenization without pre-tokenized words | CH-03: tokenization is not universally splitting on spaces; our longest-match tokenizer is not SentencePiece |
| [Bengio et al., 2003](https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf) | §2: learn feature vectors with a sequence probability function | CH-03/04: learned representations can share statistical structure; toy vectors are hand assigned and not learned semantic facts |
| [Peters et al., 2018](https://aclanthology.org/N18-1202/) | Contextual representation paper and metadata | CH-03: reading pointer separating fixed entry lookup from representations computed in context; model details postponed |
| [Jurafsky & Martin, SLP3, chapter 3](https://web.stanford.edu/~jurafsky/slp3/3.pdf) | 2026-08-19 draft; §3.1 N-gram conditional counts and boundaries, §3.2–3.3 held-out evaluation, §3.6.1 add-one | CH-04: mathematical cross-check only; all prose, ab/ab/ac data, calculations and diagrams are original. Add-one is a teaching baseline, not best practice |
| [Astro Markdown guide](https://docs.astro.build/en/guides/markdown-content/) and installed Astro config types | Astro 7 processor API | Explicit unified processor required for remark/rehype; local installed APIs checked |
| [remark-math](https://github.com/remarkjs/remark-math) | Compile-time KaTeX and CSS requirement | Local font/CSS and HTML+MathML; no math rendering CDN |

## Decisions from research

1. Five replay groups demonstrate how to classify evidence; synthetic transcripts cannot establish a real model's error rate or mechanism.
2. Keep the entire parameter/context/external-data/state distinction in both languages; use the distinct glossary translations of inference and reasoning.
3. ID is an arbitrary address under a versioned vocabulary. An embedding table is distinct from contextual activations and retrieval embeddings. Similarity is a geometric score, not entailment or truth.
4. Boundary tokens and the predictable vocabulary are explicit before any count. An unseen transition (zero numerator) differs from an unseen context (zero denominator). Add-one smooths every candidate, including EOS, but never BOS.
5. The frozen held-out set ac/aa is a diagnostic fixture: ac deliberately repeats a training string to compare seen vs unseen combinations. It is not independent evidence of generalization and is not a blind test set. Repeated setting comparisons are exploratory evaluation.
6. Sequence products include EOS. No cross-tokenizer likelihood comparison, no inference of factual correctness from probability, no claim that a larger N always helps.

The textbook's Words/Tokens and Embeddings PDF endpoints returned tool errors; no substantive claim relies on having read those PDFs. No quotations, paper figures, commercial model traces, external model weights, private data, or third-party datasets are copied into the repository.

## Editorial revision, 2026-09-09

The expanded explanations reuse the verified primary-source claims above. Added ticket, catalogue, calculator, coordinate, and path examples are original teaching constructions, not new empirical claims. The N-gram combinatorial bound now explicitly counts formal combinations before the EOS stop rule; BOS contexts are separate. Existing independent numerical fixtures remain unchanged.

## Static textbook revision, 2026-09-09

The editorial reference is [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/). The [preface](https://pages.cs.wisc.edu/~remzi/OSTEP/preface.pdf) explains problem-centered chapter organization and accompanying exercises. The [CPU Scheduling chapter](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf) develops assumptions, metrics, numerical workloads, counterexamples, revised policies, and tradeoffs. Those sources informed chapter structure, not LLM technical claims. No text or diagrams were copied.

The revised chapters expose all fixed comparisons and solutions statically. Added examples cover criterion-dependent scoring, target alignment, same-answer/different-state cases, encoding collisions, ID relabeling, direction versus length, Unigram's order loss, prefix versus complete-sequence probability, and changed-corpus exercises. These are original deductions under explicitly stated teaching rules, not additional empirical model results. No PDF is produced in this iteration.
