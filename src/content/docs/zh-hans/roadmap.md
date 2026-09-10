---
title: "全书路线图"
description: "《理解大语言模型》的九部分、57 章、基础补充资源与在线扩展。"
sidebar:
  order: 1
---

全书规划为九个部分，共 57 章，另有两份基础补充和一个多模态在线扩展。第一部分（第 1—4 章）已于 2026 年 9 月 10 日发布中英文版本；后续章节正在编写，暂未开放阅读。

## Part I：打开黑箱

- [**第 1 章** 先观察：LLM 是什么，又不是什么](../ch-01/)
- [**第 2 章** 一个 Token 的旅程：训练和模型运行不是一回事](../ch-02/)
- [**第 3 章** 文本怎样变成 Token、ID 和嵌入向量](../ch-03/)
- [**第 4 章** 从 N-gram 到 Bigram：手算语言模型](../ch-04/)

## Part II：补齐必要地基

- **第 5 章** Batch、Shape、Vector 和 Matrix
- **第 6 章** 从 Logits 到 Probability、Loss 与 Perplexity
- **第 7 章** 机器学习与神经网络的最小训练闭环
- **第 8 章** 真实文本不是干净字符串
- **第 9 章** Keyword、Bag-of-Words 与 TF-IDF：建立稀疏 baseline
- **第 10 章** 从稀疏表示到 Word2Vec 与神经语言模型

## Part III：上下文为何困难

- **第 11 章** RNN：把过去带到当前
- **第 12 章** 为什么 RNN 会忘：BPTT、LSTM/GRU 与上下文化表示
- **第 13 章** Seq2Seq：读完再写为何形成瓶颈
- **第 14 章** Attention：当前输出应该看输入哪里

## Part IV：拆开 Transformer

- **第 15 章** Self-Attention 与 Q/K/V
- **第 16 章** Mask 与 Multi-Head Attention
- **第 17 章** 拼出完整 Transformer Block
- **第 18 章** Transformer 家族：BERT、GPT 与 T5
- **第 19 章** Tokenizer 深入：BPE、WordPiece、SentencePiece 与 Byte-level
- **第 20 章** 从零拼出 Mini GPT
- **第 21 章** 训练、保存和审问 Mini GPT

## Part V：现代 LLM 如何形成和运行

- **第 22 章** 什么使 Language Model 成为 LLM
- **第 23 章** 预训练数据流水线与治理
- **第 24 章** Scaling：Model、Data 与 Compute 怎样共同变化
- **第 25 章** 现代 Dense LLM Block：RoPE、RMSNorm 与 SwiGLU
- **第 26 章** 高效、稀疏与替代架构地图
- **第 27 章** 大规模训练系统的地图与估算
- **第 28 章** 机制可解释性：可解码、相关与因果不是一回事
- **第 29 章** 生成策略：从 Logits 到 Sampling
- **第 30 章** 模型 inference：Prefill、Decode、KV Cache 与量化
- **第 31 章** Serving 效率：复用、内核、推测与批处理
- **第 32 章** 先写模型评测契约
- **第 33 章** 按证据选择 API 或本地模型

## Part VI：把基座模型变成可用能力

- **第 34 章** SFT：从续写到遵循指令
- **第 35 章** 偏好优化：RLHF、DPO 与对齐边界
- **第 36 章** Reasoning 能力怎样训练：监督、RLVR 与 Verifier
- **第 37 章** Test-Time Compute：采样、搜索、验证和停止
- **第 38 章** 能力缺口决策：Prompt、RAG、Tool 还是改参数
- **第 39 章** Continued Pretraining、Fine-tuning 与 LoRA/QLoRA

## Part VII：外接上下文、程序与知识

- **第 40 章** Prompt 之后是 Context Engineering
- **第 41 章** Structured Output：建立机器可验证的数据契约
- **第 42 章** Function Calling 与 Tools：由谁真正执行
- **第 43 章** MCP：稳定互操作概念与版本边界
- **第 44 章** 现代检索：BM25、Dense、Hybrid 与 Reranker
- **第 45 章** 从零构建有引用的 RAG
- **第 46 章** RAG 工程与分层评测

## Part VIII：从工作流到可信 Agent

- **第 47 章** Agent 之前先理解 Workflow、State 与 Memory
- **第 48 章** Agent Skills：封装可复用做法
- **第 49 章** 可靠 Agent：权限、预算、回放与恢复
- **第 50 章** 从模型评测扩展到系统评测
- **第 51 章** 幻觉、偏见、隐私与版权：持续治理
- **第 52 章** Prompt Injection、Jailbreak 与不可信输入输出
- **第 53 章** 秘密、权限、租户隔离与供应链安全

## Part IX：从原型到可维护系统

- **第 54 章** 从 Notebook 到可用服务与可信 UX
- **第 55 章** LLMOps I：版本、Trace、发布与回滚
- **第 56 章** LLMOps II：Cache、韧性、SLO 与反馈
- **第 57 章** 毕业项目：可评测的 Personal Knowledge Assistant

## 基础补充资源

- **Primer-PY**：Python、Notebook、NumPy/PyTorch Tensor 与读报错。
- **Primer-HTTP**：Client/Server、HTTP、JSON、认证、Streaming、Timeout 与 Retry。

## 在线选修

- **EXT-MM-01** 从文本 LLM 到多模态系统。
