---
title: "Book roadmap"
description: "The nine parts, 57 chapters, primers, and online extension in Understanding Large Language Models from the Ground Up."
sidebar:
  order: 1
---

The book contains nine progressive parts, 57 core chapters, two foundation primers and one optional online multimodal extension. All 57 chapters and both primers are available in English and Chinese. Chapters 40–57 and the HTTP primer were released on September 15, 2026; earlier publication dates are unchanged. The multimodal extension remains planned and unpublished.

## Part I: Opening the Black Box

- [**Chapter 1** Start by Observing: What an LLM Is—and Is Not](../ch-01/)
- [**Chapter 2** The Journey of a Token: Training Is Not Inference](../ch-02/)
- [**Chapter 3** How Text Becomes Tokens, IDs, and Embeddings](../ch-03/)
- [**Chapter 4** From N-grams to Bigrams: A Language Model by Hand](../ch-04/)

## Part II: Essential Foundations

- [**Chapter 5** Batches, Shapes, Vectors, and Matrices](../ch-05/)
- [**Chapter 6** From Logits to Probability, Loss, and Perplexity](../ch-06/)
- [**Chapter 7** The Smallest Machine-Learning and Neural-Network Training Loop](../ch-07/)
- [**Chapter 8** Real Text Is Not a Clean String](../ch-08/)
- [**Chapter 9** Keywords, Bag of Words, and TF-IDF: Establishing a Sparse Baseline](../ch-09/)
- [**Chapter 10** From Sparse Representations to Word2Vec and Neural Language Models](../ch-10/)

## Part III: Why Context Is Hard

- [**Chapter 11** RNNs: Carrying the Past into the Present](../ch-11/)
- [**Chapter 12** Why RNNs Forget: BPTT, LSTM/GRU, and Contextual Representations](../ch-12/)
- [**Chapter 13** Seq2Seq: Why Read-Then-Write Becomes a Bottleneck](../ch-13/)
- [**Chapter 14** Attention: Where Should the Current Output Look?](../ch-14/)

## Part IV: Inside the Transformer

- [**Chapter 15** Self-Attention and Q/K/V](../ch-15/)
- [**Chapter 16** Masks and Multi-Head Attention](../ch-16/)
- [**Chapter 17** Assembling a Complete Transformer Block](../ch-17/)
- [**Chapter 18** Transformer Families: BERT, GPT, and T5](../ch-18/)
- [**Chapter 19** Tokenizers in Depth: BPE, WordPiece, SentencePiece, and Byte-Level Models](../ch-19/)
- [**Chapter 20** Building a Mini GPT from Scratch](../ch-20/)
- [**Chapter 21** Training, Saving, and Interrogating a Mini GPT](../ch-21/)

## Part V: How Modern LLMs Are Built and Run

- [**Chapter 22** What Makes a Language Model an LLM](../ch-22/)
- [**Chapter 23** Pretraining Data Pipelines and Governance](../ch-23/)
- [**Chapter 24** Scaling: How Model, Data, and Compute Grow Together](../ch-24/)
- [**Chapter 25** Modern Dense LLM Blocks: RoPE, RMSNorm, and SwiGLU](../ch-25/)
- [**Chapter 26** A Map of Efficient, Sparse, and Alternative Architectures](../ch-26/)
- [**Chapter 27** Mapping and Estimating Large-Scale Training Systems](../ch-27/)
- [**Chapter 28** Mechanistic Interpretability: Decodability, Correlation, and Causality](../ch-28/)
- [**Chapter 29** Generation Strategies: From Logits to Sampling](../ch-29/)
- [**Chapter 30** Model Inference: Prefill, Decode, KV Cache, and Quantization](../ch-30/)
- [**Chapter 31** Serving Efficiency: Reuse, Kernels, Speculation, and Batching](../ch-31/)
- [**Chapter 32** Write the Model Evaluation Contract First](../ch-32/)
- [**Chapter 33** Choosing an API or Local Model from Evidence](../ch-33/)

## Part VI: Turning Base Models into Useful Capabilities

- [**Chapter 34** SFT: From Completion to Instruction Following](../ch-34/)
- [**Chapter 35** Preference Optimization: RLHF, DPO, and the Limits of Alignment](../ch-35/)
- [**Chapter 36** Training Reasoning Capabilities: Supervision, RLVR, and Verifiers](../ch-36/)
- [**Chapter 37** Test-Time Compute: Sampling, Search, Verification, and Stopping](../ch-37/)
- [**Chapter 38** Diagnosing Capability Gaps: Prompt, RAG, Tools, or Parameter Updates](../ch-38/)
- [**Chapter 39** Continued Pretraining, Fine-Tuning, and LoRA/QLoRA](../ch-39/)

## Part VII: Connecting Context, Tools, and Knowledge

- [**Chapter 40** Beyond Prompts: Context Engineering](../ch-40/)
- [**Chapter 41** Structured Output: A Machine-Checkable Data Contract](../ch-41/)
- [**Chapter 42** Function Calling and Tools: Who Actually Executes?](../ch-42/)
- [**Chapter 43** MCP: Stable Interoperability Concepts and Version Boundaries](../ch-43/)
- [**Chapter 44** Modern Retrieval: BM25, Dense, Hybrid, and Rerankers](../ch-44/)
- [**Chapter 45** Building a Cited RAG System from Scratch](../ch-45/)
- [**Chapter 46** RAG Engineering and Layered Evaluation](../ch-46/)

## Part VIII: From Workflows to Trustworthy Agents

- [**Chapter 47** Before Agents: Workflows, State, and Memory](../ch-47/)
- [**Chapter 48** Agent Skills: Packaging Reusable Practices](../ch-48/)
- [**Chapter 49** Reliable Agents: Permissions, Budgets, Replay, and Recovery](../ch-49/)
- [**Chapter 50** From Model Evaluation to System Evaluation](../ch-50/)
- [**Chapter 51** Hallucination, Bias, Privacy, and Copyright: Continuous Governance](../ch-51/)
- [**Chapter 52** Prompt Injection, Jailbreaks, and Untrusted Input/Output](../ch-52/)
- [**Chapter 53** Secrets, Permissions, Tenant Isolation, and Supply Chain Security](../ch-53/)

## Part IX: From Prototype to Maintainable Systems

- [**Chapter 54** From Notebook to Usable Service and Trustworthy UX](../ch-54/)
- [**Chapter 55** LLMOps I: Versions, Traces, Releases, and Rollbacks](../ch-55/)
- [**Chapter 56** LLMOps II: Caching, Resilience, SLOs, and Feedback](../ch-56/)
- [**Chapter 57** Capstone: An Evaluable Personal Knowledge Assistant](../ch-57/)

## Foundation primers

- [**Primer-PY**: Python, notebooks, NumPy/PyTorch tensors, and reading errors](../primer-py/). Read after the core of Chapter 5 and before the programming exercises.
- [**Primer-HTTP**: Client/server systems, HTTP, JSON, authentication, streaming, timeouts, and retries](../primer-http/). Read before Chapter 42’s practice; Chapters 43 and 54 reuse it.

## Online extension

- **EXT-MM-01** From Text LLMs to Multimodal Systems.
