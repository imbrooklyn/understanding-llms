---
title: "全书路线图"
description: "《理解大语言模型》的九部分、57 章、基础补充资源与在线扩展。"
sidebar:
  order: 1
---

本书包含九个递进部分、57 个主线章节、两份基础补充资源和一个在线多模态扩展。章节完成后会在此路线图与侧边栏中开放。

## Part I：打开黑箱

- **CH-01** 先观察：LLM 是什么，又不是什么
- **CH-02** 一个 Token 的旅程：训练和模型运行不是一回事
- **CH-03** 文本怎样成为 Token、ID 和 Embedding
- **CH-04** 从 N-gram 到 Bigram：手算语言模型

## Part II：补齐必要地基

- **CH-05** Batch、Shape、Vector 和 Matrix
- **CH-06** 从 Logits 到 Probability、Loss 与 Perplexity
- **CH-07** 机器学习与神经网络的最小训练闭环
- **CH-08** 真实文本不是干净字符串
- **CH-09** Keyword、Bag-of-Words 与 TF-IDF：建立稀疏 baseline
- **CH-10** 从稀疏表示到 Word2Vec 与神经语言模型

## Part III：上下文为何困难

- **CH-11** RNN：把过去带到当前
- **CH-12** 为什么 RNN 会忘：BPTT、LSTM/GRU 与上下文化表示
- **CH-13** Seq2Seq：读完再写为何形成瓶颈
- **CH-14** Attention：当前输出应该看输入哪里

## Part IV：拆开 Transformer

- **CH-15** Self-Attention 与 Q/K/V
- **CH-16** Mask 与 Multi-Head Attention
- **CH-17** 拼出完整 Transformer Block
- **CH-18** Transformer 家族：BERT、GPT 与 T5
- **CH-19** Tokenizer 深入：BPE、WordPiece、SentencePiece 与 Byte-level
- **CH-20** 从零拼出 Mini GPT
- **CH-21** 训练、保存和审问 Mini GPT

## Part V：现代 LLM 如何形成和运行

- **CH-22** 什么使 Language Model 成为 LLM
- **CH-23** 预训练数据流水线与治理
- **CH-24** Scaling：Model、Data 与 Compute 怎样共同变化
- **CH-25** 现代 Dense LLM Block：RoPE、RMSNorm 与 SwiGLU
- **CH-26** 高效、稀疏与替代架构地图
- **CH-27** 大规模训练系统的地图与估算
- **CH-28** 机制可解释性：可解码、相关与因果不是一回事
- **CH-29** 生成策略：从 Logits 到 Sampling
- **CH-30** 模型 inference：Prefill、Decode、KV Cache 与量化
- **CH-31** Serving 效率：复用、内核、推测与批处理
- **CH-32** 先写模型评测契约
- **CH-33** 按证据选择 API 或本地模型

## Part VI：把基座模型变成可用能力

- **CH-34** SFT：从续写到遵循指令
- **CH-35** 偏好优化：RLHF、DPO 与对齐边界
- **CH-36** Reasoning 能力怎样训练：监督、RLVR 与 Verifier
- **CH-37** Test-Time Compute：采样、搜索、验证和停止
- **CH-38** 能力缺口决策：Prompt、RAG、Tool 还是改参数
- **CH-39** Continued Pretraining、Fine-tuning 与 LoRA/QLoRA

## Part VII：外接上下文、程序与知识

- **CH-40** Prompt 之后是 Context Engineering
- **CH-41** Structured Output：建立机器可验证的数据契约
- **CH-42** Function Calling 与 Tools：由谁真正执行
- **CH-43** MCP：稳定互操作概念与版本边界
- **CH-44** 现代检索：BM25、Dense、Hybrid 与 Reranker
- **CH-45** 从零构建有引用的 RAG
- **CH-46** RAG 工程与分层评测

## Part VIII：从工作流到可信 Agent

- **CH-47** Agent 之前先理解 Workflow、State 与 Memory
- **CH-48** Agent Skills：封装可复用做法
- **CH-49** 可靠 Agent：权限、预算、回放与恢复
- **CH-50** 从模型评测扩展到系统评测
- **CH-51** 幻觉、偏见、隐私与版权：持续治理
- **CH-52** Prompt Injection、Jailbreak 与不可信输入输出
- **CH-53** 秘密、权限、租户隔离与供应链安全

## Part IX：从原型到可维护系统

- **CH-54** 从 Notebook 到可用服务与可信 UX
- **CH-55** LLMOps I：版本、Trace、发布与回滚
- **CH-56** LLMOps II：Cache、韧性、SLO 与反馈
- **CH-57** 毕业项目：可评测的 Personal Knowledge Assistant

## 基础补充资源

- **Primer-PY**：Python、Notebook、NumPy/PyTorch Tensor 与读报错。
- **Primer-HTTP**：Client/Server、HTTP、JSON、认证、Streaming、Timeout 与 Retry。

## 在线选修

- **EXT-MM-01** 从文本 LLM 到多模态系统。
