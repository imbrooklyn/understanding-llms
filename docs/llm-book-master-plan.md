# Understanding LLMs: master plan

Follow one token to understand how modern language models are formed, executed, and incorporated into reliable software systems.

This is a web-first, bilingual, openly licensed technical textbook. Its sequence connects observable behavior, language modeling, Transformers, modern LLMs, post-training, retrieval, tools, agents, security, and production systems. Two continuing projects turn the concepts into inspectable engineering results. This English plan preserves the curriculum contracts while incorporating the static-textbook and English-public-documentation requirements of 2026-09-09.

## 1. Product definition

| Dimension | Decision |
| --- | --- |
| Title | *Understanding Large Language Models from the Ground Up*; the localized book title is defined in `src/config/book.mjs` |
| Primary audience | Developers with general software experience but no systematic AI, machine-learning, or NLP background |
| Additional audience | Technically inclined readers, students, career changers, and beginning machine-learning learners |
| Form | A complete bilingual textbook with code, notebooks, data, diagrams, exercises, and online extensions |
| Authoritative edition | Web Edition; GitHub hosts buildable source and practice assets; blogs, RSS, and third-party platforms support discovery |
| Language relationship | English is the technical baseline; Chinese preserves concepts, equations, conclusions, risks, and dependencies, with appropriate linguistic examples |
| Continuing projects | Mini GPT and Personal Knowledge Assistant |
| License | Original prose: CC BY-SA 4.0; code: Apache-2.0; figures, data, and notebooks carry item-specific provenance and licensing |
| Publication boundary | No PDF, EPUB, or print edition in this iteration. Stable prose excludes changing prices, rankings, API fields, and vendor configuration |
| Capability boundary | Do not promise frontier-model training or industrial cluster operation from scratch; large-scale training is covered through principles, system maps, and estimates |

## 2. Reader contract

### 2.1 Starting point

No AI, machine-learning, deep-learning, or NLP prerequisites are assumed. The core conceptual path requires no Python, GPU, paid API, or backend-development experience. Two companion primers supply Python, notebooks, tensors, HTTP, and JSON where the practice path needs them.

Everyone begins with Part I. Experienced readers may move quickly through familiar material but must satisfy the concepts explicitly required by later chapters.

### 2.2 Outcomes

After the core path, readers can:

1. Trace text, tokens, IDs, embeddings, Transformer computation, logits, and selection through one token's journey.
2. Distinguish training, inference, and reasoning; identify changes to parameters, context, external information, and system state.
3. Explain Unigram, Bigram, Trigram, and general N-gram models, and use sparsity and context failures to motivate RNNs, LSTM, attention, Transformers, GPT, pretraining, and post-training.
4. Compare BERT, GPT, and T5 architectures and objectives; connect data, scale, training, generation, and serving constraints.
5. Distinguish prompts, context, RAG, tools, continued pretraining, SFT, full fine-tuning, and PEFT, selecting interventions against an evaluation baseline.
6. Explain model, retrieval, generation, tool, agent, and end-to-end evaluation, together with governance, security, and human responsibility.

After the practice path, readers can also implement configurable N-grams, a minimal training loop, attention, and Mini GPT on a CPU or browser notebook; evolve a knowledge assistant from keyword, count-vector, and TF-IDF baselines; add structured output, read-only tools, MCP, cited RAG, reusable skills, and bounded workflows; and deliver a service with layered evaluation, attack regressions, permissions, recovery, traces, versions, and an operating manual.

### 2.3 Two reading modes

| Mode | Required material | May skip | Evidence of completion |
| --- | --- | --- | --- |
| Core understanding | Problem progression, mechanism diagrams, numerical examples, failure boundaries, and conceptual exercises | Code, environment setup, scaffolding, and independent implementation challenges | Explain data flow, applicability, and the next problem; pass the part checkpoint |
| Hands-on practice | Core path plus notebooks, engineering analysis, and project increments | Only explicitly optional or time-sensitive online extensions | Reproducible code, relevant tests, and accepted project evidence |

## 3. Content and teaching design

### 3.1 Chapter argument

Each chapter develops an observable problem through an existing method, a reproducible failure, a proposed improvement, the new mechanism, complete numerical or diagrammatic evidence, the resulting capability, the applicability boundary, and the next question.

Use OSTEP's problem-centered organization as an editorial reference: state assumptions and a criterion, establish a baseline, expose a limitation with a counterexample, then derive the revision and its cost. Do not copy its prose, figures, or distinctive wording. Technical names follow a need for the concept. Formulas verify reasoning rather than replace it. Explain each analogy's useful correspondence and its limit. Distinguish facts, explanations, and constructed teaching examples.

Every chapter includes numbered worked examples, referenced figures/tables, a summary, transfer exercises, and visible reasoned solutions. A sequence of definitions, warnings, or interface instructions does not constitute a textbook argument. Word counts and software-test totals are not evidence that readers understand.

### 3.2 Depth

| Level | Reader capability | Use |
| --- | --- | --- |
| L1: orientation | Identify the problem and the system layer | Extensions and research maps |
| L2: mechanism | Explain structure, data flow, and tradeoffs | Most supporting and advanced topics |
| L3: execution | Calculate, implement, evaluate, or make an engineering decision | Main capabilities |
| L4: research | Derive, reproduce research, or optimize industrial implementations | Further study only |

Language modeling, the training loop, attention, Transformers, Mini GPT, generation and basic inference, RAG, evaluation, and production architecture reach L3. Other topics remain at the supporting L1/L2 depth needed by the main path.

### 3.3 Continuing cases

| Case | Fixed question | First use | Later role |
| --- | --- | --- | --- |
| Generation | Complete “The capital of France is ___” and its natural Chinese equivalent | CH-01 | Tokens, logits, probability, sampling, GPT, and plausible falsehoods |
| Context | A distant clue affects the required interpretation or continuation | CH-01 | N-grams, RNNs, attention, long contexts, and context engineering |
| Knowledge | The fictional Beijing lodging limit changes from 600 to 750 | CH-01 | Lexical baselines, freshness, RAG, citations, evaluation, and governance |
| Action | Read order status; later introduce cancellation requiring approval | CH-01 | Structured output, tools, MCP, agents, permissions, idempotency, and recovery |

Mechanism cases remain equivalent across languages. Linguistic and cultural localization must not change facts, formulas, conclusions, risks, or prerequisites.

### 3.4 Static figures, examples, and experimental records

Use journey diagrams for end-to-end flow, anatomy diagrams for structure, evolution diagrams for successive mechanisms, comparisons on shared dimensions, and system diagrams for data, control, trust, and responsibility boundaries.

Figures need captions and alternative descriptions, must work on narrow screens, and must not rely on color alone. Textbook learning content is static: no selectors, inputs, buttons, custom interactive elements, or collapsed solutions. Present variable changes as complete side-by-side cases, result tables, and traces. Refer to each figure and explain the relationship it establishes. Site navigation and language selection remain normal site features. This iteration spends no time on PDF production or typography.

### 3.5 Stable prose and the online layer

Stable prose contains motivations, concepts, mechanisms, applicability boundaries, and vendor-independent engineering principles. It must be understandable offline and without one product. The online layer contains prices, rankings, API and protocol fields, framework interfaces, and vendor settings, with `as_of`, `last_verified`, and sources. It can change without changing the chapter argument. Multimodality is a bilingual online extension after CH-57, not a prerequisite for the main path or capstone.

## 4. Curriculum and bridge resources

### 4.1 Nine parts

| Part | Chapters | Purpose | Main evidence |
| --- | --- | --- | --- |
| I | CH-01–04 | Open the black box through observation and a count model | Token journey and MG-0 calculations |
| II | CH-05–10 | Establish mathematical, learning, text, and representation foundations | Training loop and KA-0 lexical baselines |
| III | CH-11–14 | Explain why context is difficult | Sequence-model failure analysis and cross-attention |
| IV | CH-15–21 | Assemble a Transformer and Mini GPT | Reproducible model snapshot and structural explanation |
| V | CH-22–33 | Connect data, scale, training, generation, inference, evaluation, and choice | Resource estimates, KA-1 evaluation contract, and selection report |
| VI | CH-34–39 | Distinguish instruction, preference, reasoning, test-time compute, and adaptation | Evidence-based capability-gap decision and optional PEFT |
| VII | CH-40–46 | Connect context, programs, and knowledge | KA-2–4 and layered RAG evaluation |
| VIII | CH-47–53 | Make workflows and agents controlled, evaluable, and secure | KA-5–8, attack regressions, and replay evidence |
| IX | CH-54–57 | Deliver and operate a maintainable system | KA-9–10 and capstone evidence package |

### 4.2 Primers

Primers are bridge resources outside the numbered main chapters. They are not mandatory for the core conceptual path.

| Resource | Entry point | Contents | Completion criterion |
| --- | --- | --- | --- |
| Primer-PY | After CH-05 core, before the first Python practice; then revisit CH-04's configurable character N-gram notebook and CH-05 NumPy work; reused in CH-07/15/20 | Notebooks, files/paths, variables, strings, lists/dictionaries, conditionals/loops, functions, errors, packages, NumPy/PyTorch tensors, dtype/device, and reading failures | Run text counts and tensor-shape exercises in a clean browser notebook; change N or another parameter and explain the output |
| Primer-HTTP | Before choosing engineering practice in CH-42/43/54 | Client/server, URLs, requests/responses, JSON, status codes, API keys/environment variables, streaming, timeouts, retries/rate limits, and local/remote interfaces | Run scaffolding with safe placeholder credentials and explain failure paths without exposing secrets |

## 5. Complete chapter contracts

Titles and identifiers are authoritative in `src/config/book.mjs`. The tables below preserve learning outcomes, prerequisites, practice, and boundaries. An arrow in the boundary column introduces the next problem.

### 5.1 Part I: Opening the Black Box

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-01 | Classify capabilities, variation, factual errors, and system risks in five fixed conversation groups; create initial evaluation, failure, and risk entries | None | Complete static records and conditions, per-case judgments; no API | Fluency is not truth; behavior does not reveal an internal mechanism → follow one response |
| CH-02 | Map one token's generation; distinguish training and inference timelines; locate parameters, context, external data, and state | CH-01 | Static generation trace and complete comparisons of changes to each location | Model is not system; context is not parameters or permanent memory → encode text |
| CH-03 | Segment bilingual examples, find IDs, retrieve vectors, and distinguish token/ID/embedding | CH-02 | Complete vocabulary, encoding traces, unknown/version failures, and two small-vector similarity calculations | Tokens are not words; ID magnitude has no semantic metric; similarity is not understanding → estimate next-token probabilities |
| CH-04 | Distinguish N-gram orders and N−1 context; calculate Bigram conditional and sequence probabilities before/after smoothing; compare diagnostics and separate training/generation/evaluation | CH-01–03 | Static hand calculations, six order/smoothing settings, and seeded trace; no Python or primer yet; revisit the configurable notebook later | N-grams and GPT share a next-token task, not representation or context capability; unseen combinations, sparsity, storage pressure, and fixed windows → mathematical and learning foundations |

### 5.2 Part II: Essential Foundations

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-05 | Read `[B,T,C]`; calculate dot products, matrix multiplication, and cosine; explain every input/output dimension | CH-03–04 | Complete the core, then Primer-PY; NumPy shape checks and deferred CH-04 notebook | Correct shapes do not guarantee meaning; cosine is not equivalence → trainable probabilities |
| CH-06 | Calculate log, softmax, and cross-entropy on small values; explain perplexity and KL | CH-04–05 | Fixed-logit numerical comparisons | Low loss is not product quality; calibration is not factual correctness → parameter updates |
| CH-07 | Explain forward/loss/backward/update, train/validation/test separation, and overfitting | CH-01, CH-05–06 | Reproducible PyTorch two-dimensional classifier after Primer-PY | Training scores are not generalization; distinguish validation datasets, schemas, and verifiers → apply learning to language |
| CH-08 | Identify ambiguity, task granularity, Unicode/bytes, and normalization loss; specify bilingual processing | CH-03 | Test a pure normalization function | Cleaning may lose information; characters, bytes, and tokens differ → non-LLM baselines |
| CH-09 | Construct count vectors and a document-term matrix; calculate TF, IDF, TF-IDF, and cosine; distinguish retrieval, classification, sequence labeling, span extraction, and generation; orient HMM/CRF only | CH-07–08 | KA-0 on one fixed query/document/evaluation collection: keyword, BoW count, and TF-IDF matrices, rankings, predictions, and errors | BoW discards order; TF-IDF remains sparse and context-limited; word N-gram features expand dimensions and are not an N-gram LM → learned representations |
| CH-10 | Connect sparse document vectors to the distributional hypothesis, Word2Vec/GloVe, static dense embeddings, polysemy failures, and a fixed-window neural LM with shapes | CH-05–07, CH-09 | Compare BoW, TF-IDF, static vectors, and a small NNLM on the same task, recording dimensions and errors | Dense does not automatically mean semantic; static rows and fixed windows remain limited → carrying history |

### 5.3 Part III: Why Context Is Hard

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-11 | Unroll three RNN steps; separate input, hidden state, parameter sharing, training, and inference | CH-07, CH-10 | Stepwise small-RNN state log | Hidden state is not agent state; sequential work and fading information → forgetting |
| CH-12 | Explain vanishing/exploding gradients through products; compare RNN/LSTM/GRU; locate ELMo between static and deeply pretrained representations | CH-07, CH-11 | Distance/gradient plots; code optional | Gates mitigate rather than eliminate limitations; ELMo is not BERT → sequence-to-sequence generation |
| CH-13 | Map encoder/decoder, target shifting, teacher forcing, and autoregressive timelines | CH-06, CH-11 | Identify exposure bias in a supplied translation trace | Training targets are unavailable during generation; one-vector compression is a bottleneck → dynamic access to input |
| CH-14 | Calculate cross-attention; explain alignment, fixed-vector bottlenecks, recurrent paths, and parallelism limits | CH-12–13 | Optional NumPy verification and input-removal comparison | Attention weights are not automatically causal explanations; recurrent cross-attention retains its skeleton → interactions within a sequence |

### 5.4 Part IV: Inside the Transformer

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-15 | Follow projections and `softmax(QKᵀ/√d)V` through one head numerically and by shape | CH-05–06, CH-14 | NumPy implementation checked against hand calculation | Q/K/V analogies have limits; a head is not a full Transformer → visibility and multiple heads |
| CH-16 | Apply padding/causal masks; explain per-head projections, concatenation, and output projection | CH-15 | Mask tests including intentional future leakage | Heads need not align with human concepts; wrong masks leak targets → position and non-attention computation |
| CH-17 | Assemble position, attention, residual, normalization, and FFN with shapes; distinguish pre/post norm | CH-07, CH-15–16 | One-block forward and shape assertions | Attention is not a Transformer; component names do not guarantee long-context effectiveness → architecture families |
| CH-18 | Compare BERT/GPT/T5 by visibility, structure, masked/causal/denoising objectives, and tasks | CH-13, CH-16–17 | Architecture/objective choice on the same task | Architecture, objective, training stage, and product name are separate axes → text input to GPT |
| CH-19 | Perform tokenizer merges; compare BPE/WordPiece/SentencePiece/byte-level vocabulary, OOV, length, and language behavior | CH-03, CH-08 | Train a tiny tokenizer and test round trips with version records | Tokenizer changes alter the data/model interface; fewer tokens need not be better → Mini GPT data |
| CH-20 | Map dataset, embedding, causal attention, block, LM head, and loss to diagrams and shape traces | CH-07, CH-15–19 | MG-1: single-layer CPU/browser Mini GPT forward after Primer-PY | Code verifies rather than hides structure; a forward pass does not imply learning → training and assessment |
| CH-21 | Analyze small-corpus training/validation curves, checkpoints, and generation traces | CH-07, CH-20 | MG-2 reproducible training snapshot with seed, data, and dependency versions | Small-corpus overfitting and language-like output are not general ability → modern LLM formation |

### 5.5 Part V: How Modern LLMs Are Formed and Run

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-22 | Distinguish foundation, LLM, base, instruct, chat, and reasoning models on separate axes | CH-18, CH-21 | Reconstruct a lifecycle from a vendor-neutral model card | Parameter count alone is insufficient; chat UI is not a model type → data sources |
| CH-23 | Document provenance, license, parsing, filtering, deduplication, PII, mixture, contamination, and data cards | CH-08, CH-19, CH-22 | Version Mini GPT corpus and knowledge-assistant documents | Robots rules, terms, and licenses differ; more data may amplify contamination → balancing resources |
| CH-24 | Estimate parameters, tokens, and FLOPs from given tables; explain empirical power laws and compute-optimal boundaries | CH-06, CH-23 | Budget scenarios without a GPU | Scaling laws are empirical; training-optimal and serving-optimal differ → modern blocks |
| CH-25 | Explain position, normalization, and FFN activation through RoPE, RMSNorm, and SwiGLU | CH-17, CH-22, CH-24 | Map simplified configuration fields onto the block | Names do not guarantee quality or long-context use; defer serving optimizations → attention and parameter efficiency |
| CH-26 | Locate MQA/GQA, MoE, efficient/sparse attention, linear attention, and state-space/recurrent alternatives | CH-17, CH-22, CH-24–25 | Annotate dense/sparse, attention/alternative, and active parameters in cards | An architecture map, not a variant encyclopedia or kernel implementation course → training resources |
| CH-27 | Estimate parameter/gradient/optimizer/activation memory; explain precision, accumulation, parallelism, checkpointing, and recovery | CH-07, CH-24–26 | Resource tables; GPU work explicitly optional | System orientation is not industrial-cluster capability; numerical and communication risks differ → evidence about internals |
| CH-28 | Compare probes/attribution, logit lens, activation patching, and circuits by evidence strength | CH-12, CH-17, CH-22 | Analyze supplied small-model interventions; experiments optional | Decodability and correlation do not establish causation; self-reports are not internal traces → token selection |
| CH-29 | Compare greedy, temperature, top-k/p, beam-search limits, penalties, and stopping on fixed logits | CH-04, CH-18, CH-22 | Reproducible structured/creative-task matrix | Temperature does not change knowledge; seeds do not guarantee cross-stack identity → inference stages |
| CH-30 | Map prefill/decode and KV cache; explain quantization's memory/quality tradeoff | CH-17, CH-25, CH-29 | Calculate TTFT, per-token latency, and KV memory from traces | Inference is not reasoning; KV cache is not long-term memory or an answer cache → many-request serving |
| CH-31 | Distinguish prefix caching, FlashAttention, speculative decoding, and continuous batching using latency, throughput, and cost | CH-26, CH-30 | Fixed-workload trace analysis; framework settings optional | Model/engine/server/application differ; an optimization can move a bottleneck → define success |
| CH-32 | Build scenario, dataset, metric, rubric, and baseline contracts; include repetition, uncertainty, human judgment, leakage, and versions | CH-01, CH-07, CH-22, CH-29 | Freeze KA-1 evaluation collection and failure taxonomy | One benchmark is not product quality; uncalibrated LLM judges cannot replace human evidence → model choice |
| CH-33 | Compare API/local options under one contract across capability, language, latency, cost, privacy, availability, license, and operations | CH-31–32 | KA-1 selection report with versions and verification dates | Rankings change; open weights do not automatically mean open source → post-training |

### 5.6 Part VI: Turning Base Models into Useful Capabilities

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-34 | Unroll conversations into tokens/loss masks; explain roles, chat templates, data quality, and forgetting | CH-18, CH-22 | Small-data format checks; training optional | SFT is a data/objective stage, not LoRA; template mismatch breaks training/execution alignment → defining better behavior |
| CH-35 | Use minimal RL vocabulary to explain preference data, reward models, RLHF/DPO, and KL constraints | CH-06, CH-34 | Audit chosen/rejected examples against a rubric | Preference is not truth, fairness, or security; reward hacking → verifiable tasks |
| CH-36 | Distinguish process/outcome supervision, verifiable rewards, verifiers, exploration, distillation, and generalization evidence | CH-32, CH-34–35 | Classify fixed candidates and verifier errors | Format gaming and training scores do not establish new-problem generalization → computation at run time |
| CH-37 | Compare direct answers, CoT, self-consistency, search/verifiers, quality/budget curves, and stopping | CH-29, CH-36 | Repeated fixed-task experiments with token/time/quality records | Visible explanations are not internal traces; reasoning cannot replace factual retrieval → locate capability gaps |
| CH-38 | Classify knowledge, behavior, format, domain, and task gaps before choosing prompts/RAG/tools/parameter changes | CH-22, CH-32–33 | Adaptation decision and rejected alternatives tied to KA-1 | Methods are not a universal upgrade ladder; no escalation without a baseline → what to update |
| CH-39 | Distinguish continued pretraining, SFT, full updates, adapters, and quantized bases; compare under one contract | CH-07, CH-23, CH-34, CH-38 | Optional CPU/low-resource PEFT with license record | LoRA is not SFT; quantization is not LoRA; frequently changing knowledge is not a default fine-tuning task → input design |

### 5.7 Part VII: Connecting Context, Programs, and Knowledge

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-40 | Specify testable contracts for instructions, examples, selection, ordering, compression, delimiters, and contamination | CH-02, CH-29, CH-38 | KA-2 regression-tested context templates | Long windows do not ensure use; prompts are not security boundaries; external knowledge needs provenance → machine-readable output |
| CH-41 | Distinguish free JSON, schemas, and constrained decoding; handle parsing, types, missing values, refusal, failures, and versions | CH-40 | KA-2 typed output and contract tests | Valid schema does not guarantee factual correctness; structured data executes no action → proposed calls |
| CH-42 | Map propose/validate/authorize/execute/return; distinguish read/write permissions, timeouts, retry, idempotency, and confirmation | CH-01, CH-41 | KA-3 read-only query tool after Primer-HTTP | Applications execute tools; tool results are untrusted inputs; retries can repeat side effects → interoperability |
| CH-43 | Explain host/client/server and tools/resources/prompts; locate transport, authentication, authorization, and protocol limits | CH-42 | KA-3 minimal read-only MCP integration; dated online fields | MCP is not a model, tool, RAG, or agent; obsolete protocol details stay outside stable arguments → retrieval |
| CH-44 | Separate embedding model, index, retriever, and reranker; compare BM25/dense/hybrid with Recall@k, MRR, and nDCG | CH-09–10, CH-32 | KA-4 lexical/dense/hybrid comparison on one FAQ with baselines retained | A vector database is not RAG; similarity is not answer relevance → supplied retrieval context |
| CH-45 | Trace parse/chunk/metadata/index/retrieve/pack/generate/cite-or-abstain | CH-40, CH-44 | KA-4 versioned bilingual documents, citations, and retrieval traces | RAG does not update parameters or eliminate hallucination; chunks and citations can fail → locating failures |
| CH-46 | Apply rewriting/filtering, parent-child retrieval, hybrid/reranking, and compression; evaluate retrieval/context/generation/citations separately | CH-32, CH-45 | Complete KA-4 with cases, error classes, and before/after uncertainty reporting | End-to-end scores do not locate failure; plausibility is not evaluation → choosing next actions |

### 5.8 Part VIII: From Workflows to Trustworthy Agents

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-47 | Distinguish single calls, chains, workflows, and agents; map orchestration, state/memory, plans/tools, and stopping | CH-42, CH-46 | KA-5 deterministic RAG workflow with one bounded model decision | Tool loops do not guarantee reliable agents; context, memory, RNN state, and agent state differ → reusable procedures |
| CH-48 | Distinguish skills, prompts, tools, MCP, and agents; explain progressive loading, assets, versions/tests, and provenance | CH-43, CH-47 | KA-6 testable source-verification skill | A skill is not merely a longer prompt and is not inherently trusted → controlling long tasks |
| CH-49 | Specify least privilege/approval, budgets/timeouts, retry/compensation, and trace/replay in a state machine | CH-43, CH-47–48 | Complete KA-6 with automatic reads, approved writes, locked dependencies, and recovery; A2A orientation only | Multiple agents add complexity; A2A does not replace MCP; bound loops and repeated side effects → whole-system evaluation |
| CH-50 | Build model/retrieval, generation/citation, tool/trace, and end-to-end evaluation matrices; calibrate judges | CH-32, CH-46, CH-49 | KA-7 system cases, regressions, and failure attribution | Judges have position/length/self-preference biases; online feedback has selection bias → responsibility |
| CH-51 | Maintain responsibility, minimization, retention, and governance across data, models/retrieval, logs/output, and human fallback | CH-01, CH-23, CH-50 | KA-8 risk register, data/system cards, and abstention policy | Alignment is not truth, fairness, or legality; RAG can cite bad sources → adversarial use |
| CH-52 | Distinguish direct/indirect injection, jailbreaks, untrusted content, and unsafe output handling; construct attack chains | CH-42, CH-48–51 | KA-8 injection/jailbreak regressions, output validation, and isolation tests | Delimiters do not enforce instruction/data trust boundaries; content safety is not authorization → permissions and dependencies |
| CH-53 | Address secret exfiltration, least privilege, tenant isolation, and MCP/skill/weight/dependency supply chains with allowlists, sandboxing, and approvals | CH-43, CH-48–49, CH-52 | Complete KA-8 permission matrix, approval tests, provenance inventory, and supply-chain regressions | Available capability is not trusted provenance; a sandbox does not replace authorization or audit → service delivery |

### 5.9 Part IX: From Prototype to Maintainable System

| Chapter | Core understanding and acceptance | Prerequisites | Practice and deliverable | Boundary and next question |
| --- | --- | --- | --- | --- |
| CH-54 | Separate UI/business/retrieval/model layers; explain authentication, streaming/concurrency, cancellation/retry, and layered software tests | CH-46, CH-52–53 | KA-9 CPU-demonstrable service with citations, abstention, uncertainty, undo/handoff, and accessible UI after Primer-HTTP | A running demo is not a usable product; software tests do not replace probabilistic evaluation → version management |
| CH-55 | Map component versions, trace/replay, evaluation release gates, staged rollout, and rollback | CH-50, CH-54 | KA-10 replayable candidate, release checklist, and rollback exercise | Replay does not guarantee identical output; version labels do not replace evidence → operating targets |
| CH-56 | Distinguish response/semantic caches; define rate limits, fallback/circuit breakers, SLOs/alerts, and governed feedback | CH-31, CH-50, CH-54–55 | KA-10 monitoring, fault injection, and governed feedback pipeline | Monitoring describes distributions, not causal proof; caches are not knowledge or memory → integrated evidence |
| CH-57 | Connect requirements/threat model, baselines, selection, RAG, structured output, read-only tools/MCP, skills, evaluation, security, service, and operations | CH-33, CH-38, CH-46, CH-49, CH-51–56 | Complete KA-10: service, architecture, tests/regressions, evaluation, licenses/dependencies, risks, cards, operation and rollback manuals | Success is not looking intelligent; disclose unresolved issues, known risks, and human responsibilities |

### 5.10 Optional online extension: multimodal foundation models

EXT-MM-01 locates vision/audio encoders, projection/cross-attention/unified-token approaches, multimodal evaluation, injection, and accessibility. Prerequisites: CH-18, CH-22, CH-51–53. Deliver a bilingual optional design and evaluation sketch. It is not part of CH-57 acceptance. Multimodality requires an interface and representation, not simply placing an image into a text LLM.

## 6. Continuing projects and milestones

### 6.1 Mini GPT

Mini GPT answers what happens inside the model. Readers assemble tokenizer, dataset, embedding, attention, Transformer block, LM head, training, checkpoint, and generation. The project serves structural understanding on CPU/browser resources rather than industrial scale or competitive generation quality.

### 6.2 Personal Knowledge Assistant

The assistant answers what is needed around the model. It evolves from keyword, BoW count, and TF-IDF baselines through evaluation contracts, context, structured output, tools, MCP, retrieval, RAG, workflows, skills, system evaluation, security, serving, and LLMOps. The three lexical baselines share queries, documents, and evaluation cases; compare each subsequent capability with them.

### 6.3 Project milestones

| Milestone | Chapter | Increment | Acceptance evidence |
| --- | --- | --- | --- |
| MG-0 | CH-04 | N-gram family and complete hand-calculated Bigram | Context-order table, counts, smoothing comparison, unseen combinations, and fixed-context failure |
| MG-1 | CH-20 | Mini GPT forward and loss | Shape log and module-to-diagram mapping |
| MG-2 | CH-21 | Training, checkpoint, and generation | Seed, data/dependency versions, validation curves, limitations |
| KA-0 | CH-09 | Keyword/BoW count/TF-IDF search | Fixed shared query/document/evaluation collection, document-term matrix, rankings/predictions, and errors |
| KA-1 | CH-32–33 | Evaluation contract and model selection | Baselines, versions, repeated runs, cost and latency |
| KA-2 | CH-40–41 | Context contract and structured output | Schema, failure paths, contract tests |
| KA-3 | CH-42–43 | Read-only tools and MCP | Authorization, arguments, results, timeout traces |
| KA-4 | CH-44–46 | Cited RAG and layered evaluation | Retrieval, generation, and citation metrics |
| KA-5 | CH-47 | Deterministic workflow with bounded model decisions | State, stopping rules, decision-point comparisons |
| KA-6 | CH-48–49 | Reusable skill and recoverable agent | Provenance, permissions, approvals, budgets, replay |
| KA-7 | CH-50 | Layered system evaluation | Regression matrix, judge calibration, failure attribution |
| KA-8 | CH-51–53 | Governance, attacks, permissions, and supply-chain security | Cards, attack regressions, permission matrix, dependency provenance |
| KA-9 | CH-54 | Usable service and trustworthy UX | Software tests, request lifecycle, handoff, accessibility |
| KA-10 | CH-55–57 | Versioned operations and integrated delivery | Traces, SLOs, alerts, releases/rollback, final evidence package |

### 6.4 Part completion criteria

| Part | Core result | Practice result |
| --- | --- | --- |
| I | Draw the token journey, distinguish training/inference, explain N−1 context, and calculate Bigram probabilities | Analyze fixed records and static Unigram/Bigram/Trigram comparisons |
| II | Read shapes, connect logits/loss/gradient/update, and explain sparse text representations | Compare three lexical baselines on shared data and run a minimal training loop |
| III | Derive the need for attention from fixed-vector, gradient, and recurrent bottlenecks | Reproduce a sequence-model failure or analyze a supplied trace |
| IV | Explain attention and block shapes; compare BERT/GPT/T5 | Run Mini GPT on clean CPU resources with reproducible checkpoints |
| V | Connect data, scale, training, generation, inference, evaluation, and model choice | Compare at least two models/configurations under a fixed contract |
| VI | Distinguish pretraining, SFT, preference optimization, reasoning, test-time compute, and PEFT | Compare one training-side or run-time adaptation under the same evaluation |
| VII | Distinguish schema, tools, MCP, retrievers, and RAG; locate failed stages | Cited RAG with abstention and layered retrieval/generation/citation evaluation |
| VIII | Distinguish workflows, agents, skills, and A2A; explain control, recovery, evaluation, governance, and security | Budgets, approvals, replay, attack regressions, dependency evidence |
| IX | Explain the system from model to product | A service with operating metrics, rollback, and the CH-57 evidence package |

## 7. Concept boundaries

### 7.1 Responsibilities across chapters

| Concept | First definition | Development | Final use | Do not conflate |
| --- | --- | --- | --- | --- |
| Model/system | CH-01–02 | CH-30–31, CH-42 | CH-54–57 | Model, engine, server, application |
| Training/inference | CH-02 | CH-04, CH-07, CH-21, CH-30 | CH-34–37, CH-55–56 | Inference and reasoning; use their distinct localized glossary terms |
| Token/ID | CH-03 | CH-08, CH-19, CH-23 | CH-40, CH-55–56 | Word, ID, vector, training tokens, billable tokens, compute budget |
| Embedding | CH-03 | CH-10, CH-17 | CH-44–46 | Input table, contextual representation, retrieval embedding, index |
| Language model | CH-04 | CH-10, CH-18 | CH-20–22, CH-34 | Shared objective and shared architecture/capability |
| N-gram | CH-04 | CH-09 features, CH-10 neural comparison | CH-20 | N-token fragment, BoW N-gram feature, N−1-context language model |
| Sparse text representation | CH-09 | CH-10 | CH-44–46 | Keyword, count vector, document-term matrix, BoW, TF-IDF, embedding, index |
| Probability/loss | CH-04, CH-06 | CH-07, CH-15 | CH-21, CH-32, CH-35 | Probability, factual correctness, reward, preference |
| Validation | CH-07 | CH-32 | CH-36, CH-41, CH-50 | Validation dataset, schema validation, verifier; name the object |
| Evaluation | CH-01 | CH-07, CH-32 | CH-46, CH-50, CH-57 | Evaluation, software tests, online monitoring |
| Risk/responsibility | CH-01 | CH-23, CH-42, CH-45 | CH-49, CH-51–57 | Each new data/model/tool/MCP/skill dependency needs associated risks and tests |
| Text processing | CH-03 | CH-08–09, CH-19 | CH-23, CH-44–45 | Cleaning and lossless processing; characters, bytes, tokens |
| Baseline | CH-01 | CH-07, CH-09 | CH-32–33, CH-38, CH-46, CH-57 | Base model and evaluation baseline |
| Context/state/memory | CH-02 | CH-11, CH-30, CH-40 | CH-45, CH-47, CH-55–56 | Context window, KV cache, long-term memory, agent state, answer cache |
| Attention | CH-14 | CH-15–17 | CH-20, CH-25–26, CH-28 | Cross/self-attention; weight visualization and causal explanation |
| Transformer | CH-17 | CH-18, CH-20 | CH-22, CH-25–26 | Attention, Transformer, GPT, LLM |
| Architecture/objective/stage | CH-18 | CH-22, CH-34–36 | CH-38–39 | Encoder/decoder, MLM/CLM, base/SFT, product names |
| Tokenizer | CH-03 | CH-19 | CH-20, CH-23 | Versioned tokenizer/checkpoint compatibility is mandatory |
| Pretraining/fine-tuning/LoRA | CH-18 | CH-23–24, CH-34 | CH-38–39 | SFT stage/objective, LoRA update method, quantization |
| Sampling/cache | CH-04 | CH-29–31 | CH-37, CH-55–56 | Temperature and knowledge; KV/prefix/response/semantic caches |
| Reasoning | CH-02 distinction, CH-22 orientation | CH-36 | CH-37, CH-50 | Visible CoT and faithful internal causes; reasoning and factual retrieval |
| Prompt/context | CH-38 decision | CH-40 | CH-45, CH-47, CH-57 | Prompting is part of context engineering, not an enforced security boundary |
| Structured output/tools | CH-41 | CH-42 | CH-47, CH-54, CH-57 | Data contracts and execution; application owns execution |
| MCP/skill/agent/A2A | CH-43 | CH-47–49 | CH-57 | No upgrade ladder: MCP connects capabilities, skills reuse procedures, A2A connects independent agents |
| Retrieval/RAG | CH-09 baseline | CH-44–46 | CH-50, CH-57 | Retrieval and correct use; RAG and parameter updates |
| Alignment/governance/security | CH-35 | CH-42, CH-49 | CH-51–53, CH-57 | Preference, correctness, fairness, content safety, authorization safety |

### 7.2 Reusable models of the system

| Model of the system | Established | Reused |
| --- | --- | --- |
| Model is one component of a system | CH-01 | CH-57 |
| One token's journey | CH-02 | CH-20, CH-30 |
| Training, inference, and reasoning are distinct | CH-02 | CH-37 |
| Token is not word; ID is not embedding | CH-03 | CH-19, CH-44 |
| N−1 context determines a next-token distribution in an N-gram LM | CH-04 | CH-10, CH-20, CH-29 |
| Forward → loss → gradient → update | CH-07 | CH-21, CH-39 |
| Successive context mechanisms address the same problem | CH-10 | CH-14–17 |
| Q/K/V and information flow | CH-14–15 | CH-20, CH-28 |
| Attention plus residual/normalization and FFN | CH-17 | CH-25–26 |
| Architecture, objective, and training stage are separate axes | CH-18 | CH-22, CH-34 |
| Model, data, and compute interact | CH-24 | CH-27 |
| Prompts, RAG, tools, and training change different layers | CH-38 | CH-57 |
| Prompt → prefill → KV cache → decode | CH-30 | CH-55–56 |
| Retrieve → context → generate → cite | CH-45 | CH-46, CH-57 |
| Model proposes; application validates and executes | CH-42 | CH-49, CH-57 |
| Agent combines model, orchestrator, state, tools, and policy | CH-47 | CH-49 |
| Layered evaluation locates failures | CH-32 | CH-46, CH-50 |
| Probabilistic model with deterministic controls | CH-41 | CH-52–57 |
| Count → reweight → learn: BoW, TF-IDF, static dense, contextual representations | CH-09 | CH-10, CH-18, CH-44 |

## 8. Content assets and publication

### 8.1 Chapter deliverables

Each chapter contains a definite question connected to adjacent chapters; a self-contained mechanism explanation; complete numerical, diagrammatic, or observable evidence; a failure case and applicability boundary; a summary, conceptual/transfer exercises, and visible answers; primary sources and further reading; and appropriate CPU/browser practice assets where the topic calls for them. Do not hide the only explanation in code, a sidebar, or an external link.

### 8.2 Code, data, and figures

Both languages share code logic. Public identifiers, code comments, notebook implementation notes, README files, plans, research logs, and other repository documentation are English. Bilingual prose and localized figures/examples are textbook content, including when their strings reside in source data. Keep that boundary explicit.

Prefer small functions with explicit inputs/outputs and visible shapes. Retain failure outputs as test assets. Core practice runs on CPU/browser resources; GPU experiments are optional. Reproducible records include dependencies, seeds, data and model/tokenizer versions, and expected results. Keep redistributable bilingual teaching datasets small and licensed.

Use stable figure labels for tokens, IDs, vectors, parameters, computation, external data, and state. Distinguish data flow, parameter updates, and control. Give every original or third-party asset provenance and licensing; link rather than redistribute material lacking redistribution permission.

### 8.3 Bilingual equivalence

Use matching chapter numbers, dependencies, formulas, figure structures, and engineering behavior. Establish stable English equivalents when localized technical terms first appear. Localize linguistic examples without adding technical facts to only one edition. Keep code identifiers, configuration keys, protocol fields, and error messages in their source form; localize textbook explanations and alternative descriptions. Language switching stays on the same chapter.

### 8.4 Channel responsibilities

| Channel | Role |
| --- | --- |
| Web Edition | Complete bilingual prose, contents, search, cross-references, exercises, errata, code snapshots, and online extensions |
| GitHub | Buildable source, code, notebooks, diagram sources, tests, dataset documentation, and issues |
| Blog | Announcements, reading guides, and part summaries; do not duplicate complete chapters |
| RSS | Locale-specific summaries linking to chapters |
| Third-party platforms | Short excerpts, guides, or announcements linking to the authoritative edition |

No PDF, EPUB, or print edition is delivered in this iteration. Keeping learning content static preserves future reuse without requiring present PDF work.

### 8.5 Web architecture

Astro Starlight provides routing, bilingual navigation, search, and reading UI, with custom CSS/components matching the main site's design. The main site's manually triggered GitHub Pages workflow checks out the public book repository, builds it, and merges the output into one Pages artifact. The book does not deploy separately and needs no cross-repository publication credentials.

Each book owns `/books/<book-slug>/`; this book's permanent slug is `understanding-llms`. Its root redirects to `/books/understanding-llms/en/`. Both `en` and `zh-hans` prefixes remain stable for chapters, glossary, changelog, errata, and RSS. Each language page has a self-canonical URL and reciprocal alternate-language links. Maintain localized navigation/search/RSS and discoverable sitemap entries. Formula rendering, code, accessible figures, and mobile reading are part of the web edition.

## 9. Quality criteria

| Area | Acceptance condition |
| --- | --- |
| Chapter content | Problem, mechanism, complete evidence, failure boundary, summary, exercises/answers, and sources; prerequisite concepts already established |
| Teaching | Core path independent of code; bounded analogies; explained intermediate steps; a clear new capability and next problem; test totals do not certify comprehension |
| Technical accuracy | Primary support for substantive claims; consistent formulas, terminology, figures, and cross-chapter definitions; dates and sources for changing information |
| Practice | Reproducible CPU/browser assets with complete data, dependency, and randomness information |
| Bilingual quality | Equivalent technical meaning, equations, risks, and behavior; localization preserves conclusions |
| Public language | English repository documentation and code comments outside localized textbook content |
| Accessibility | Described figures, information independent of color, usable narrow-screen navigation, code, and formulas; all learning content available without controls |
| System reliability | Layered evaluation, permissions, recovery, attack regressions, traces, versions, and operating instructions |
| Licensing/security | Documented provenance and licenses; no secrets, restricted data, or unknown-origin dependencies |
| Book completeness | CH-01–57, two primers, two projects, and EXT-MM-01 satisfy the reader contract without known serious factual, security, or licensing defects |

## 10. Reference framework

These sources establish the curriculum, technical research directions, and implementation references. Time-sensitive APIs and protocol details belong to dated online material and must be checked when their chapters are implemented. The source ledger records the actual scope checked for Part I.

### 10.1 Build, hosting, and internationalization

- [Astro Starlight](https://starlight.astro.build/)
- [Starlight internationalization](https://starlight.astro.build/guides/i18n/)
- [Starlight custom CSS](https://starlight.astro.build/guides/css-and-tailwind/)
- [Google multilingual-site guidance](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [GitHub Pages custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)

### 10.2 Textbooks and courses

- [Arpaci-Dusseau and Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*](https://pages.cs.wisc.edu/~remzi/OSTEP/). Editorial reference for assumptions, metrics, worked examples, counterexamples, mechanisms, tradeoffs, and exercises; not LLM technical evidence.
- [Jurafsky and Martin, *Speech and Language Processing*](https://web.stanford.edu/~jurafsky/slp3/). Language modeling, text, representations, Transformers, post-training, retrieval, and sequence foundations.
- [Stanford CS336: Language Modeling from Scratch](https://cs336.stanford.edu/). Tokenizers, architecture, resources, training, evaluation, and data.
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1). Supplementary practical model/tokenizer/data use; this book supplies its Python bridge separately.

### 10.3 Transformers, pretraining, and scale

- [Vaswani et al., *Attention Is All You Need*](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)
- [Kudo and Richardson, *SentencePiece*](https://aclanthology.org/D18-2012/)
- [Peters et al., *Deep Contextualized Word Representations*](https://aclanthology.org/N18-1202/)
- [Devlin et al., *BERT*](https://aclanthology.org/N19-1423/)
- [Radford et al., *Improving Language Understanding by Generative Pre-Training*](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)
- [Raffel et al., *T5*](https://www.jmlr.org/papers/v21/20-074.html)
- [Kaplan et al., *Scaling Laws for Neural Language Models*](https://arxiv.org/abs/2001.08361)
- [Hoffmann et al., *Training Compute-Optimal Large Language Models*](https://proceedings.neurips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract.html)
- [Fedus et al., *Switch Transformers*](https://arxiv.org/abs/2101.03961)
- [Gu and Dao, *Mamba*](https://arxiv.org/abs/2312.00752). Orientation for alternatives, not a separate implementation track.
- [Jurafsky and Martin, *Interpretability*](https://web.stanford.edu/~jurafsky/slp3/10.pdf). Distinguish probing, attribution, and intervention evidence.

### 10.4 Post-training, reasoning, and efficient adaptation

- [Ouyang et al., *Training Language Models to Follow Instructions with Human Feedback*](https://arxiv.org/abs/2203.02155)
- [Rafailov et al., *Direct Preference Optimization*](https://arxiv.org/abs/2305.18290)
- [Lightman et al., *Let's Verify Step by Step*](https://arxiv.org/abs/2305.20050). Process/outcome supervision.
- [DeepSeek-AI et al., *DeepSeek-R1*](https://arxiv.org/abs/2501.12948). An instance of verifiable rewards, reasoning, and distillation; no single recipe is a universal law.
- [Wei et al., *Chain-of-Thought Prompting*](https://arxiv.org/abs/2201.11903)
- [Snell et al., *Scaling LLM Test-Time Compute Optimally*](https://arxiv.org/abs/2408.03314)
- [Hu et al., *LoRA*](https://arxiv.org/abs/2106.09685)
- [Dettmers et al., *QLoRA*](https://arxiv.org/abs/2305.14314)
- [Dao et al., *FlashAttention*](https://arxiv.org/abs/2205.14135)
- [Ainslie et al., *Grouped-Query Attention*](https://arxiv.org/abs/2305.13245)
- [Leviathan et al., *Speculative Decoding*](https://arxiv.org/abs/2211.17192)

### 10.5 Function calling, MCP, skills, and agents

- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling). Model proposals, application execution, and returned results; vendor fields are implementation examples.
- [MCP specification snapshot, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP snapshot release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP SEP-2577](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging). Check version boundaries rather than importing old tutorial mechanisms into stable explanations.
- [Agent Skills specification](https://agentskills.io/specification). Skill directories, progressive loading, scripts, references, and assets.
- [Skills over MCP working group](https://modelcontextprotocol.io/community/working-groups/skills-over-mcp). Discovery/distribution interoperability.
- [A2A specification](https://a2a-protocol.org/latest/specification/). Independent-agent collaboration; advanced orientation rather than a default architecture.
- [Yao et al., *ReAct*](https://arxiv.org/abs/2210.03629)

### 10.6 Retrieval, evaluation, and security

- [Lewis et al., *Retrieval-Augmented Generation*](https://arxiv.org/abs/2005.11401)
- [Stanford CRFM, *HELM*](https://crfm.stanford.edu/helm/). Transparent, reproducible, multi-scenario and multi-metric evaluation.
- [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/). Ongoing govern/map/measure/manage activities.
- [OWASP GenAI Top 10, 2025](https://genai.owasp.org/download/43299/). Application-security threat inventory.
- [Full Stack Deep Learning, LLMOps](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/llmops/). Deployment, observability, feedback, and iteration; platform UI stays outside stable prose.

### 10.7 Multimodal foundations

- [Radford et al., *CLIP*](https://proceedings.mlr.press/v139/radford21a.html)
- [Alayrac et al., *Flamingo*](https://proceedings.neurips.cc/paper_files/paper/2022/hash/960a172bc7fbf0177ccccbb411a7d800-Abstract-Conference.html)
- [Liu et al., *LLaVA*](https://arxiv.org/abs/2304.08485)
