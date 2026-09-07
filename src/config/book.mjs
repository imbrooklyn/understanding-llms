export const BOOK_SLUG = "understanding-llms";
export const BOOK_BASE = `/books/${BOOK_SLUG}`;
export const BOOK_SITE = "https://imbrooklyn.dev";
export const BOOK_REPOSITORY = "https://github.com/imbrooklyn/understanding-llms";
export const BOOK_LOCALES = ["en", "zh-hans"];

export const bookParts = [
  {
    "id": "part-1",
    "label": {
      "zh-hans": "Part I：打开黑箱",
      "en": "Part I: Opening the Black Box"
    },
    "chapters": [
      {
        "id": "ch-01",
        "title": {
          "zh-hans": "先观察：LLM 是什么，又不是什么",
          "en": "Start by Observing: What an LLM Is—and Is Not"
        }
      },
      {
        "id": "ch-02",
        "title": {
          "zh-hans": "一个 Token 的旅程：训练和模型运行不是一回事",
          "en": "The Journey of a Token: Training Is Not Inference"
        }
      },
      {
        "id": "ch-03",
        "title": {
          "zh-hans": "文本怎样成为 Token、ID 和 Embedding",
          "en": "How Text Becomes Tokens, IDs, and Embeddings"
        }
      },
      {
        "id": "ch-04",
        "title": {
          "zh-hans": "从 N-gram 到 Bigram：手算语言模型",
          "en": "From N-grams to Bigrams: A Language Model by Hand"
        }
      }
    ]
  },
  {
    "id": "part-2",
    "label": {
      "zh-hans": "Part II：补齐必要地基",
      "en": "Part II: Essential Foundations"
    },
    "chapters": [
      {
        "id": "ch-05",
        "title": {
          "zh-hans": "Batch、Shape、Vector 和 Matrix",
          "en": "Batches, Shapes, Vectors, and Matrices"
        }
      },
      {
        "id": "ch-06",
        "title": {
          "zh-hans": "从 Logits 到 Probability、Loss 与 Perplexity",
          "en": "From Logits to Probability, Loss, and Perplexity"
        }
      },
      {
        "id": "ch-07",
        "title": {
          "zh-hans": "机器学习与神经网络的最小训练闭环",
          "en": "The Smallest Machine-Learning and Neural-Network Training Loop"
        }
      },
      {
        "id": "ch-08",
        "title": {
          "zh-hans": "真实文本不是干净字符串",
          "en": "Real Text Is Not a Clean String"
        }
      },
      {
        "id": "ch-09",
        "title": {
          "zh-hans": "Keyword、Bag-of-Words 与 TF-IDF：建立稀疏 baseline",
          "en": "Keywords, Bag of Words, and TF-IDF: Establishing a Sparse Baseline"
        }
      },
      {
        "id": "ch-10",
        "title": {
          "zh-hans": "从稀疏表示到 Word2Vec 与神经语言模型",
          "en": "From Sparse Representations to Word2Vec and Neural Language Models"
        }
      }
    ]
  },
  {
    "id": "part-3",
    "label": {
      "zh-hans": "Part III：上下文为何困难",
      "en": "Part III: Why Context Is Hard"
    },
    "chapters": [
      {
        "id": "ch-11",
        "title": {
          "zh-hans": "RNN：把过去带到当前",
          "en": "RNNs: Carrying the Past into the Present"
        }
      },
      {
        "id": "ch-12",
        "title": {
          "zh-hans": "为什么 RNN 会忘：BPTT、LSTM/GRU 与上下文化表示",
          "en": "Why RNNs Forget: BPTT, LSTM/GRU, and Contextual Representations"
        }
      },
      {
        "id": "ch-13",
        "title": {
          "zh-hans": "Seq2Seq：读完再写为何形成瓶颈",
          "en": "Seq2Seq: Why Read-Then-Write Becomes a Bottleneck"
        }
      },
      {
        "id": "ch-14",
        "title": {
          "zh-hans": "Attention：当前输出应该看输入哪里",
          "en": "Attention: Where Should the Current Output Look?"
        }
      }
    ]
  },
  {
    "id": "part-4",
    "label": {
      "zh-hans": "Part IV：拆开 Transformer",
      "en": "Part IV: Inside the Transformer"
    },
    "chapters": [
      {
        "id": "ch-15",
        "title": {
          "zh-hans": "Self-Attention 与 Q/K/V",
          "en": "Self-Attention and Q/K/V"
        }
      },
      {
        "id": "ch-16",
        "title": {
          "zh-hans": "Mask 与 Multi-Head Attention",
          "en": "Masks and Multi-Head Attention"
        }
      },
      {
        "id": "ch-17",
        "title": {
          "zh-hans": "拼出完整 Transformer Block",
          "en": "Assembling a Complete Transformer Block"
        }
      },
      {
        "id": "ch-18",
        "title": {
          "zh-hans": "Transformer 家族：BERT、GPT 与 T5",
          "en": "Transformer Families: BERT, GPT, and T5"
        }
      },
      {
        "id": "ch-19",
        "title": {
          "zh-hans": "Tokenizer 深入：BPE、WordPiece、SentencePiece 与 Byte-level",
          "en": "Tokenizers in Depth: BPE, WordPiece, SentencePiece, and Byte-Level Models"
        }
      },
      {
        "id": "ch-20",
        "title": {
          "zh-hans": "从零拼出 Mini GPT",
          "en": "Building a Mini GPT from Scratch"
        }
      },
      {
        "id": "ch-21",
        "title": {
          "zh-hans": "训练、保存和审问 Mini GPT",
          "en": "Training, Saving, and Interrogating a Mini GPT"
        }
      }
    ]
  },
  {
    "id": "part-5",
    "label": {
      "zh-hans": "Part V：现代 LLM 如何形成和运行",
      "en": "Part V: How Modern LLMs Are Built and Run"
    },
    "chapters": [
      {
        "id": "ch-22",
        "title": {
          "zh-hans": "什么使 Language Model 成为 LLM",
          "en": "What Makes a Language Model an LLM"
        }
      },
      {
        "id": "ch-23",
        "title": {
          "zh-hans": "预训练数据流水线与治理",
          "en": "Pretraining Data Pipelines and Governance"
        }
      },
      {
        "id": "ch-24",
        "title": {
          "zh-hans": "Scaling：Model、Data 与 Compute 怎样共同变化",
          "en": "Scaling: How Model, Data, and Compute Grow Together"
        }
      },
      {
        "id": "ch-25",
        "title": {
          "zh-hans": "现代 Dense LLM Block：RoPE、RMSNorm 与 SwiGLU",
          "en": "Modern Dense LLM Blocks: RoPE, RMSNorm, and SwiGLU"
        }
      },
      {
        "id": "ch-26",
        "title": {
          "zh-hans": "高效、稀疏与替代架构地图",
          "en": "A Map of Efficient, Sparse, and Alternative Architectures"
        }
      },
      {
        "id": "ch-27",
        "title": {
          "zh-hans": "大规模训练系统的地图与估算",
          "en": "Mapping and Estimating Large-Scale Training Systems"
        }
      },
      {
        "id": "ch-28",
        "title": {
          "zh-hans": "机制可解释性：可解码、相关与因果不是一回事",
          "en": "Mechanistic Interpretability: Decodability, Correlation, and Causality"
        }
      },
      {
        "id": "ch-29",
        "title": {
          "zh-hans": "生成策略：从 Logits 到 Sampling",
          "en": "Generation Strategies: From Logits to Sampling"
        }
      },
      {
        "id": "ch-30",
        "title": {
          "zh-hans": "模型 inference：Prefill、Decode、KV Cache 与量化",
          "en": "Model Inference: Prefill, Decode, KV Cache, and Quantization"
        }
      },
      {
        "id": "ch-31",
        "title": {
          "zh-hans": "Serving 效率：复用、内核、推测与批处理",
          "en": "Serving Efficiency: Reuse, Kernels, Speculation, and Batching"
        }
      },
      {
        "id": "ch-32",
        "title": {
          "zh-hans": "先写模型评测契约",
          "en": "Write the Model Evaluation Contract First"
        }
      },
      {
        "id": "ch-33",
        "title": {
          "zh-hans": "按证据选择 API 或本地模型",
          "en": "Choosing an API or Local Model from Evidence"
        }
      }
    ]
  },
  {
    "id": "part-6",
    "label": {
      "zh-hans": "Part VI：把基座模型变成可用能力",
      "en": "Part VI: Turning Base Models into Useful Capabilities"
    },
    "chapters": [
      {
        "id": "ch-34",
        "title": {
          "zh-hans": "SFT：从续写到遵循指令",
          "en": "SFT: From Completion to Instruction Following"
        }
      },
      {
        "id": "ch-35",
        "title": {
          "zh-hans": "偏好优化：RLHF、DPO 与对齐边界",
          "en": "Preference Optimization: RLHF, DPO, and the Limits of Alignment"
        }
      },
      {
        "id": "ch-36",
        "title": {
          "zh-hans": "Reasoning 能力怎样训练：监督、RLVR 与 Verifier",
          "en": "Training Reasoning Capabilities: Supervision, RLVR, and Verifiers"
        }
      },
      {
        "id": "ch-37",
        "title": {
          "zh-hans": "Test-Time Compute：采样、搜索、验证和停止",
          "en": "Test-Time Compute: Sampling, Search, Verification, and Stopping"
        }
      },
      {
        "id": "ch-38",
        "title": {
          "zh-hans": "能力缺口决策：Prompt、RAG、Tool 还是改参数",
          "en": "Diagnosing Capability Gaps: Prompt, RAG, Tools, or Parameter Updates"
        }
      },
      {
        "id": "ch-39",
        "title": {
          "zh-hans": "Continued Pretraining、Fine-tuning 与 LoRA/QLoRA",
          "en": "Continued Pretraining, Fine-Tuning, and LoRA/QLoRA"
        }
      }
    ]
  },
  {
    "id": "part-7",
    "label": {
      "zh-hans": "Part VII：外接上下文、程序与知识",
      "en": "Part VII: Connecting Context, Tools, and Knowledge"
    },
    "chapters": [
      {
        "id": "ch-40",
        "title": {
          "zh-hans": "Prompt 之后是 Context Engineering",
          "en": "Beyond Prompts: Context Engineering"
        }
      },
      {
        "id": "ch-41",
        "title": {
          "zh-hans": "Structured Output：建立机器可验证的数据契约",
          "en": "Structured Output: A Machine-Checkable Data Contract"
        }
      },
      {
        "id": "ch-42",
        "title": {
          "zh-hans": "Function Calling 与 Tools：由谁真正执行",
          "en": "Function Calling and Tools: Who Actually Executes?"
        }
      },
      {
        "id": "ch-43",
        "title": {
          "zh-hans": "MCP：稳定互操作概念与版本边界",
          "en": "MCP: Stable Interoperability Concepts and Version Boundaries"
        }
      },
      {
        "id": "ch-44",
        "title": {
          "zh-hans": "现代检索：BM25、Dense、Hybrid 与 Reranker",
          "en": "Modern Retrieval: BM25, Dense, Hybrid, and Rerankers"
        }
      },
      {
        "id": "ch-45",
        "title": {
          "zh-hans": "从零构建有引用的 RAG",
          "en": "Building a Cited RAG System from Scratch"
        }
      },
      {
        "id": "ch-46",
        "title": {
          "zh-hans": "RAG 工程与分层评测",
          "en": "RAG Engineering and Layered Evaluation"
        }
      }
    ]
  },
  {
    "id": "part-8",
    "label": {
      "zh-hans": "Part VIII：从工作流到可信 Agent",
      "en": "Part VIII: From Workflows to Trustworthy Agents"
    },
    "chapters": [
      {
        "id": "ch-47",
        "title": {
          "zh-hans": "Agent 之前先理解 Workflow、State 与 Memory",
          "en": "Before Agents: Workflows, State, and Memory"
        }
      },
      {
        "id": "ch-48",
        "title": {
          "zh-hans": "Agent Skills：封装可复用做法",
          "en": "Agent Skills: Packaging Reusable Practices"
        }
      },
      {
        "id": "ch-49",
        "title": {
          "zh-hans": "可靠 Agent：权限、预算、回放与恢复",
          "en": "Reliable Agents: Permissions, Budgets, Replay, and Recovery"
        }
      },
      {
        "id": "ch-50",
        "title": {
          "zh-hans": "从模型评测扩展到系统评测",
          "en": "From Model Evaluation to System Evaluation"
        }
      },
      {
        "id": "ch-51",
        "title": {
          "zh-hans": "幻觉、偏见、隐私与版权：持续治理",
          "en": "Hallucination, Bias, Privacy, and Copyright: Continuous Governance"
        }
      },
      {
        "id": "ch-52",
        "title": {
          "zh-hans": "Prompt Injection、Jailbreak 与不可信输入输出",
          "en": "Prompt Injection, Jailbreaks, and Untrusted Input/Output"
        }
      },
      {
        "id": "ch-53",
        "title": {
          "zh-hans": "秘密、权限、租户隔离与供应链安全",
          "en": "Secrets, Permissions, Tenant Isolation, and Supply Chain Security"
        }
      }
    ]
  },
  {
    "id": "part-9",
    "label": {
      "zh-hans": "Part IX：从原型到可维护系统",
      "en": "Part IX: From Prototype to Maintainable Systems"
    },
    "chapters": [
      {
        "id": "ch-54",
        "title": {
          "zh-hans": "从 Notebook 到可用服务与可信 UX",
          "en": "From Notebook to Usable Service and Trustworthy UX"
        }
      },
      {
        "id": "ch-55",
        "title": {
          "zh-hans": "LLMOps I：版本、Trace、发布与回滚",
          "en": "LLMOps I: Versions, Traces, Releases, and Rollbacks"
        }
      },
      {
        "id": "ch-56",
        "title": {
          "zh-hans": "LLMOps II：Cache、韧性、SLO 与反馈",
          "en": "LLMOps II: Caching, Resilience, SLOs, and Feedback"
        }
      },
      {
        "id": "ch-57",
        "title": {
          "zh-hans": "毕业项目：可评测的 Personal Knowledge Assistant",
          "en": "Capstone: An Evaluable Personal Knowledge Assistant"
        }
      }
    ]
  }
];

export const plannedChapters = bookParts.flatMap((part) =>
  part.chapters.map((chapter) => ({ ...chapter, part: part.id })),
);
