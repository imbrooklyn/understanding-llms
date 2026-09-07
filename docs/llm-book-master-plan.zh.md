# 《理解大语言模型》全书方案

> 从一个 Token 出发，理解现代 LLM 如何形成、运行，并成为可靠的软件系统。

本书是一部 Web-first、中英双语、开放许可的技术教材。它从可观察的模型行为出发，依次建立语言建模、Transformer、现代 LLM、后训练、检索与工具、Agent、安全和生产系统的完整认知链，并用两个贯穿项目把概念落到可验证的工程成果。

## 1. 产品定义

| 维度 | 最终方案 |
| --- | --- |
| 中文书名 | 《理解大语言模型》 |
| 英文书名 | *Understanding Large Language Models from the Ground Up* |
| 主要读者 | 有一般软件开发经验、但没有系统 AI、机器学习或 NLP 背景的开发者 |
| 兼容读者 | 非计算机专业的技术型读者、学生、转行者和机器学习初学者 |
| 内容形态 | 一部完整的双语开放教材，配套代码、Notebook、数据、图示、自测和在线扩展 |
| 正式载体 | Web Edition；GitHub 承载可构建源稿与配套资产，Blog、RSS 和第三方平台只承担发现与导读 |
| 语言关系 | 英文版是技术事实基准；中文版保持概念、公式、结论、风险和依赖的语义等价，并对语言案例作必要本地化 |
| 核心项目 | Mini GPT 与 Personal Knowledge Assistant |
| 许可 | 原创正文使用 CC BY-SA 4.0；代码默认使用 Apache-2.0；图、数据和 Notebook 分项标明来源与许可 |
| 出版边界 | 本版不提供 PDF、EPUB 或纸书；不把模型价格、排行榜、具体 API 字段和供应商配置写入稳定正文 |
| 能力边界 | 不承诺从零训练前沿模型或建设工业训练集群；大规模训练覆盖原理、系统地图和资源估算 |

## 2. 读者契约

### 2.1 起点

“零基础”表示不要求 AI、机器学习、深度学习或 NLP 前置知识。核心理解路径不要求 Python、GPU、付费 API 或后端开发经验；实践路径所需的 Python、Notebook、Tensor、HTTP 和 JSON 基础由两份随书 Primer 补齐。

所有读者从 Part I 开始。已有数学或工程经验的读者可以快速通过熟悉内容，但不能跳过后续章节明确依赖的概念。

### 2.2 完成后的核心能力

读完全书核心内容后，读者能够：

1. 从 Text、Token、ID、Embedding、Transformer、Logits 到 Sampling，追踪一个 Token 的完整数据流。
2. 区分 Training、模型运行（inference）和解题推理（reasoning），说明参数、上下文、外部知识和系统状态分别改变什么。
3. 区分 Unigram、Bigram、Trigram 与一般 N-gram，并从统计稀疏、固定上下文等瓶颈解释 RNN、LSTM、Attention、Transformer、GPT、预训练和后训练为何出现。
4. 比较 BERT、GPT 和 T5 的架构与目标，说明现代 LLM 的数据、规模、训练、生成和服务约束。
5. 区分 Prompt、Context、RAG、Tool、继续预训练、SFT、全量微调和 PEFT，并根据评测基线选择方案。
6. 分层解释模型、检索、生成、工具、Agent 和端到端系统评测，以及治理、安全和人工责任边界。

完成实践路径后，读者还能够：

1. 在 CPU 或浏览器 Notebook 中实现可切换阶数的 N-gram、最小训练闭环、Attention 和 Mini GPT。
2. 从 Keyword、Bag-of-Words Count 与 TF-IDF baseline 演进一个 Personal Knowledge Assistant，并在每次升级后保留同基线的对照。
3. 为助手加入结构化输出、只读 Tool、MCP、带引用 RAG、可复用 Skill 和受约束 Workflow。
4. 交付可运行服务、分层评测、攻击回归、权限与恢复机制、Trace、版本信息和运行手册。

### 2.3 两种阅读模式

| 模式 | 每章内容 | 可跳过 | 完成证据 |
| --- | --- | --- | --- |
| 核心理解 | 问题链、机制图、最小数字例、失败边界和直觉自测 | 代码、环境配置、脚手架工程和独立挑战 | 能复述数据流、适用边界和下一问题，并通过 Part 概念检查点 |
| 动手实践 | 核心理解的全部内容，加 Notebook、工程思考和项目任务 | 仅明确标为 Online Extension 的时效实现 | 代码可复现、测试通过，项目增量满足工程验收 |

## 3. 内容与教学设计

### 3.1 主叙事

每章围绕一个可观察问题展开，结构为：

1. 现有模型或做法。
2. 可复现的失败。
3. 读者对改进方法的猜想。
4. 回答该问题的新机制。
5. 最小数字例、图示或实验。
6. 新增的理解或工程能力。
7. 机制的适用边界。
8. 自然引出的下一问题。

技术名称在问题和直觉之后出现；公式与代码用于验证机制，不替代解释。每个重要类比同时说明“它帮助理解什么”和“它在哪里失效”。事实、解释和教学性重构保持明确区分。

### 3.2 深度边界

| 层级 | 读者达到的程度 | 用途 |
| --- | --- | --- |
| L1 定位 | 知道概念解决什么问题、位于系统哪一层 | 扩展架构、协议与研究方向地图 |
| L2 机制 | 能复述核心结构、数据流与主要权衡 | 大多数背景与进阶主题 |
| L3 实作 | 能手算、实现、评测或作工程判断 | 本书主线能力 |
| L4 研究 | 能推导、复现论文或优化工业实现 | 只作为进一步学习方向 |

达到 L3 的主题包括语言建模、训练闭环、Attention、Transformer、Mini GPT、生成与基础 inference、RAG、Evaluation 和 Production Architecture。其余主题以支撑主线所需的 L1 或 L2 为界。

### 3.3 四个贯穿案例

| 案例 | 固定问题 | 首次出现 | 最终用途 |
| --- | --- | --- | --- |
| Generation | “The capital of France is ___”及自然中文等价例 | CH-01 | Token、概率、Logits、Sampling、GPT，以及“流畅但错误”的边界 |
| Context | 远距离信息影响当前词义或生成 | CH-01 | N-gram、RNN、Attention、长上下文与 Context Engineering |
| Knowledge | 北京差旅住宿标准从 600 元更新为 750 元 | CH-01 | 词法 baseline、知识新鲜度、RAG、引用、评测与治理 |
| Action | 查询订单状态；后续加入需审批的取消动作 | CH-01 | Structured Output、Tool、MCP、Agent、权限、幂等与恢复 |

机制案例在中英文版本中保持一致；Tokenization、歧义和文化案例可以本地化，但不得改变事实、公式、结论、风险或前置关系。

### 3.4 图示与交互

核心图采用五种语义结构：

- Journey：展示 Token、请求或数据的端到端旅程。
- Anatomy：拆解 Block、系统或数据结构。
- Evolution：用同一问题比较多代机制如何演进。
- Compare：在统一维度上比较模型、方法或系统。
- System：标出组件、数据流、控制流、信任边界与责任边界。

所有关键图都有图注和替代文本，不只依赖颜色传达信息，并能在窄屏、黑白和色弱场景下辨识。交互组件只用于帮助观察变量变化；核心结论始终在正文中独立成立。

### 3.5 稳定正文与在线层

| 稳定正文 | Online Layer |
| --- | --- |
| Why、What、心智模型、稳定机制、方法边界、跨厂商工程原则 | 模型价格、排行榜、具体 API 字段、框架界面、协议字段、供应商配置 |
| 只有概念或证据发生实质变化时才需更新 | 标明 as_of、last_verified 和来源 |
| 可离线理解，不依赖单一产品 | 可随生态变化替换，不改变章节主线 |

多模态作为 CH-57 之后的双语 Online Extension，不进入 57 章主线，也不构成毕业项目的前置。

## 4. 全书架构

~~~mermaid
flowchart LR
  A["行为观察与 Token<br/>Part I"] --> B["数学、训练与文本基线<br/>Part II"]
  B --> C["序列模型与 Attention<br/>Part III"]
  C --> D["Transformer 与 Mini GPT<br/>Part IV"]
  D --> E["现代 LLM、生成与评测<br/>Part V"]
  E --> F["后训练、Reasoning 与适配<br/>Part VI"]
  F --> G["Context、Tool、MCP 与 RAG<br/>Part VII"]
  G --> H["Workflow、Agent、安全与治理<br/>Part VIII"]
  H --> I["服务、LLMOps 与毕业项目<br/>Part IX"]
~~~

### 4.1 九部分总览

| 部分 | 阶段性成果 | 主线 Chapter | Part 结束时的项目/证据 |
| --- | --- | --- | --- |
| I 打开黑箱 | 首次走通 LLM 全景和 N-gram/Bigram 闭环 | CH-01—CH-04 | 初始评测/失败/风险清单；区分 N-gram 阶数并手算 Bigram |
| II 补齐必要地基 | 获得后文所需数学、训练与 Keyword/BoW/TF-IDF 文本 baseline | CH-05—CH-10 | 可解释训练闭环；KA-0 三种词法 baseline 对照 |
| III 上下文为何困难 | 从递归瓶颈自然得到 Attention | CH-11—CH-14 | 序列/Attention 失败对照 |
| IV 拆开 Transformer | 追踪完整 Block，并完成 Mini GPT | CH-15—CH-21 | Mini GPT 可运行快照与结构解释 |
| V 现代 LLM 如何形成和运行 | 连接数据、规模、训练、生成、inference、评测和选型 | CH-22—CH-33 | 预训练/资源估算；KA-1 评测契约和选型报告 |
| VI 如何把基座模型变成可用能力 | 区分 SFT、偏好、reasoning、test-time 与适配 | CH-34—CH-39 | 能力缺口决策和可选 PEFT 实验 |
| VII 外接上下文、程序与知识 | 建立可靠接口及 L3 RAG | CH-40—CH-46 | KA-2—KA-4 与分层 RAG 评测 |
| VIII 从工作流到可信 Agent | 加入状态、Skill、恢复、系统评测、治理和安全 | CH-47—CH-53 | KA-5—KA-8；攻击与回放证据 |
| IX 从原型到可维护系统 | 服务化、运营化并综合交付 | CH-54—CH-57 | KA-9—KA-10 与 Capstone 证据包 |

### 4.2 基础补充资源

Primer 是随书桥接资源，不计入主线章节，也不构成核心理解路径的硬前置。

| 补充资源 | 使用位置 | 内容范围 | 完成标准 |
| --- | --- | --- | --- |
| Primer-PY | 完成 CH-05 核心内容后、首次运行 Python 实践前；通过后依次回做 CH-04 参数化字符 N-gram Notebook（以 Bigram 对照手算）、CH-05 NumPy，再用于 CH-07/15/20 | Notebook、文件/路径、变量、字符串、列表/字典、条件/循环、函数、异常、包、NumPy/PyTorch Tensor、dtype/device、读报错 | 在干净浏览器 Notebook 运行文本计数和 Tensor shape 练习；能切换 N-gram 阶数、修改一个参数并解释输出 |
| Primer-HTTP | 首次选择运行 CH-42/43/54 的工程实践 | Client/Server、URL、Request/Response、JSON、状态码、API Key/环境变量、Streaming、Timeout、Retry/Rate Limit、本地/远程共同接口 | 用安全占位密钥运行脚手架；能解释失败分支且代码不泄漏 Secret |

## 5. 完整目录

### 5.1 Part I：打开黑箱

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-01 先观察：LLM 是什么，又不是什么 | 给定五组固定对话记录，区分能力、随机现象、事实错误与系统风险；创建首批评测样例、失败案例和风险条目 | 无 | 可在浏览器复现；保存配置和输出，不要求 API | 流畅不等于真实；行为观察不能直接说明内部机制 → 一次回答内部经过什么 |
| CH-02 一个 Token 的旅程：训练和模型运行不是一回事 | 画出生成一个 Token 的全景图；用两条时间线区分 Training 与 inference；定位参数、Context、External Data、State | CH-01 | 用预制交互切换参数固定/上下文改变场景 | Model 不等于 System；上下文不等于参数或长期记忆 → 文本怎样变成模型输入 |
| CH-03 文本怎样成为 Token、ID 和 Embedding | 对中英文样例完成切分、查表和向量表示；准确区分 Token、ID、Embedding | CH-02 | 浏览器 tokenizer 观察与两个小向量相似度计算 | Token 不等于词；ID 不包含语义；相似不等于理解 → 向量怎样支持下一个 Token 预测 |
| CH-04 从 N-gram 到 Bigram：手算语言模型 | 区分 Unigram、Bigram、Trigram 和一般 N-gram，解释 N 与条件上下文长度 N−1；以 Bigram 计数表计算平滑前后条件/序列概率，比较留出样例并区分训练、生成与评测 | CH-01—CH-03 | 只使用预制的可切换阶数交互，不触发 Primer-PY 或 Python Notebook；参数化字符 N-gram Notebook 延后回做 | N-gram LM 与 GPT 共享 next-token 目标但不共享表示和上下文能力；未见组合、阶数增加造成的稀疏/存储增长与固定上下文 → 需要哪些数学和学习机制 |

### 5.2 Part II：补齐必要地基

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-05 Batch、Shape、Vector 和 Matrix | 读懂 `[B,T,C]`；手算 Dot Product、MatMul 和 Cosine，逐维解释输入输出 | CH-03—CH-04 | 先完成本章核心内容，再通过 Primer-PY；随后做 NumPy shape 检查并回做 CH-04 参数化字符 N-gram Notebook | Shape 对不代表语义对；余弦相似不代表等价 → 分数怎样成为可训练概率 |
| CH-06 从 Logits 到 Probability、Loss 与 Perplexity | 对小数字完成 Log/Softmax/Cross-Entropy；解释 Perplexity 和 KL 只回答什么 | CH-04—CH-05 | 用固定 logits 改变概率并验证数值 | 低损失不自动等于好产品；概率校准和事实正确不同 → 损失怎样改变参数 |
| CH-07 机器学习与神经网络的最小训练闭环 | 画出 Forward→Loss→Backward→Update；正确划分 Train/Validation/Test；诊断一次过拟合 | CH-01、CH-05—CH-06 | PyTorch 二维分类器和可复现记录，实践前置 Primer-PY | 训练集高分不是泛化；Validation、Schema 校验和 Verifier 不同 → 把闭环用于语言 |
| CH-08 真实文本不是干净字符串 | 识别语言歧义、任务粒度、Unicode/Byte 和规范化的信息损失；为双语样例写处理契约 | CH-03 | 测试一个纯函数的中英文规范化行为 | 清洗并非总是改进；字符、Byte、Token 不可互换 → 建立不依赖 LLM 的 baseline |
| CH-09 Keyword、Bag-of-Words 与 TF-IDF：建立稀疏 baseline | 从同一文档集构造 Count Vector 和 Document-Term Matrix，解释 Bag-of-Words；分别计算 TF、IDF、TF-IDF 与 Cosine，并区分检索、分类、序列标注、Span 抽取和生成；HMM/CRF 只作定位 | CH-07—CH-08 | CPU 上完成 KA-0：用同一 query/document/eval 集比较 Keyword、BoW Count、TF-IDF 的矩阵、排序、预测和错误；固定首版样例集 | BoW 忽略词序，TF-IDF 仍不能处理同义和语境，高维稀疏且词 N-gram 特征会扩大维度；N-gram 特征不等于 CH-04 的 N-gram LM → 表示能否从数据中学习 |
| CH-10 从稀疏表示到 Word2Vec 与神经语言模型 | 从 BoW/TF-IDF 的稀疏文档向量过渡到分布假设和静态稠密 Embedding，解释 Word2Vec/GloVe 与多义词失败；跟踪一个固定窗口神经 LM 的输入、输出和 Shape | CH-05—CH-07、CH-09 | 在同一任务上比较 BoW Count、TF-IDF、静态向量与小 NNLM，记录表示维度、排序/预测和错误变化 | 稠密不自动等于有语义；静态表示和固定窗口仍不随完整上下文变化 → 怎样携带过去 |

### 5.3 Part III：上下文为何困难

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-11 RNN：把过去带到当前 | 展开三个时间步，区分输入、Hidden State、参数共享、训练与 inference | CH-07、CH-10 | 小 RNN 的逐步状态日志 | Hidden State 不是 Agent State；顺序计算慢且远处信息衰减 → 为什么会忘 |
| CH-12 为什么 RNN 会忘：BPTT、LSTM/GRU 与上下文化表示 | 用连乘直觉解释梯度消失/爆炸；比较 RNN/LSTM/GRU；把 ELMo 放在静态表示到深层预训练之间 | CH-07、CH-11 | 可视化距离与梯度；代码可跳过 | 门控只是缓解；ELMo 的上下文化表示不等于 BERT → 一个序列怎样生成另一个序列 |
| CH-13 Seq2Seq：读完再写为何形成瓶颈 | 画出 Encoder/Decoder、目标右移、Teacher Forcing 与自回归生成时间线 | CH-06、CH-11 | 使用给定翻译 trace 定位 Exposure Bias | 训练时看到真值不等于生成时拥有真值；单向量压缩长输入 → 能否动态回看 |
| CH-14 Attention：当前输出应该看输入哪里 | 手算一次 Cross-Attention；解释对齐、固定向量瓶颈、递归路径和并行限制 | CH-12—CH-13 | NumPy 复算可选；比较删去不同输入的结果 | Attention Weight 不自动构成因果解释；Cross-Attention 仍依赖递归骨架 → 序列内部能否直接交互 |

### 5.4 Part IV：拆开 Transformer

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-15 Self-Attention 与 Q/K/V | 从输入投影到 `softmax(QKᵀ/√d)V` 逐数字、逐 Shape 走通一个 Head | CH-05—CH-06、CH-14 | NumPy 实现并与手算结果逐项比对 | Q/K/V 类比有边界；Self-Attention 不是完整 Transformer → 谁可看谁、为何多头 |
| CH-16 Mask 与 Multi-Head Attention | 对 Padding/Causal Mask 判断可见性；解释每头投影、拼接与输出投影 | CH-15 | 写 Mask 单元测试，故意制造未来泄漏 | 多头不保证每头对应人类概念；错误 Mask 会泄漏标签 → 顺序和非 Attention 计算从哪里来 |
| CH-17 拼出完整 Transformer Block | 在标注 Shape 的图中组合 Position、Attention、Residual、Norm、FFN；区分 Pre/Post Norm | CH-07、CH-15—CH-16 | 单 Block forward 与 Shape assertion | Attention 不等于 Transformer；位置机制和结构名不保证长上下文有效 → 三类架构怎样分叉 |
| CH-18 Transformer 家族：BERT、GPT 与 T5 | 从信息可见性、网络结构、MLM/Causal/Denoising 目标和任务比较三类模型 | CH-13、CH-16—CH-17 | 对同一任务填写架构/目标选择表 | 架构、训练目标、后训练阶段和产品名不是同一分类轴 → GPT 怎样真正接收文本 |
| CH-19 Tokenizer 深入：BPE、WordPiece、SentencePiece 与 Byte-level | 手工完成合并；比较词表、OOV、序列长度与中英文差异；记录 tokenizer 版本 | CH-03、CH-08 | 训练极小 tokenizer 并测试 round trip | Tokenizer 变化会改变数据和模型接口；更少 Token 不必然更好 → 构造 Mini GPT 数据 |
| CH-20 从零拼出 Mini GPT | 把 Dataset、Embedding、Causal Attention、Block、LM Head、Loss 在结构图和 Shape trace 中逐层对应 | CH-07、CH-15—CH-19 | CPU/浏览器实现单层 Mini GPT forward；实践前置 Primer-PY | 代码用来验证结构，不用框架隐藏核心解释；能 forward 不代表学会 → 如何训练与判断 |
| CH-21 训练、保存和审问 Mini GPT | 分析给定的小语料训练/验证曲线、Checkpoint 和生成 trace，解释可复现条件与局限 | CH-07、CH-20 | 运行训练并提交 MG-2 可复现快照、复现实验；固定 seed/依赖/数据版本 | 过拟合小语料和像语言的输出不等于通用能力 → 什么使语言模型成为现代 LLM |

### 5.5 Part V：现代 LLM 如何形成和运行

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-22 什么使 Language Model 成为 LLM | 在独立分类轴上区分 Foundation、LLM、Base、Instruct、Chat、Reasoning Model | CH-18、CH-21 | 阅读一份去厂商化 model card 并还原生命周期 | 参数量不是唯一答案；聊天界面不是模型类型 → 能力所需数据从哪里来 |
| CH-23 预训练数据流水线与治理 | 为小语料写来源、许可、解析、过滤、去重、PII、配比、污染和 Data Card | CH-08、CH-19、CH-22 | 版本化 Mini GPT 语料与 Knowledge Assistant 文档包 | robots/条款/许可不可混同；更多数据可能放大污染 → 数据、参数和算力怎样配比 |
| CH-24 Scaling：Model、Data 与 Compute 怎样共同变化 | 用给定表格估算参数、Token、FLOPs；解释经验幂律和 Compute-optimal 边界 | CH-06、CH-23 | 小型预算情景表，不需要 GPU | Scaling Law 不是自然定律；训练最优与服务成本最优不同 → 现代 Block 为何改变 |
| CH-25 现代 Dense LLM Block：RoPE、RMSNorm 与 SwiGLU | 分别解释位置、归一化和 FFN 激活的职责，并把三项标回 Transformer Block | CH-17、CH-22、CH-24 | 读取简化 config，把三类字段标回结构图 | 组件名称不保证长上下文或质量；不在本章堆叠服务优化 → 为什么还要改 Attention 与参数使用方式 |
| CH-26 高效、稀疏与替代架构地图 | 定位 MQA/GQA、MoE、高效/稀疏 Attention，以及线性 Attention 与状态空间/递归路线 | CH-17、CH-22、CH-24—CH-25 | 对给定模型卡标注 Dense/Sparse、Attention/Alternative 与 active parameter | 路线地图不是变体百科；不展开内核和完整替代架构实现 → 大规模训练受什么资源约束 |
| CH-27 大规模训练系统的地图与估算 | 估算参数/梯度/优化器/激活显存；解释精度、累积、并行和 Checkpoint/恢复 | CH-07、CH-24—CH-26 | 表格估算；GPU 实验明确可选 | 地图不等于工业集群能力；混合精度和并行各有数值/通信风险 → 如何谨慎研究内部机制 |
| CH-28 机制可解释性：可解码、相关与因果不是一回事 | 比较 Probe/Attribution、Logit Lens、Activation Patching 和 Circuit 的证据强度 | CH-12、CH-17、CH-22 | 分析提供的小模型干预结果；实验选做 | Attention/Probe 可视化不是自动解释；模型自述不是内部 reasoning 记录 → 运行时怎样选下个 Token |
| CH-29 生成策略：从 Logits 到 Sampling | 对固定 logits 比较 Greedy、Temperature、Top-k/p、Beam 边界、惩罚和停止 | CH-04、CH-18、CH-22 | 可复现实验矩阵，分别测试结构化与创造性任务 | Temperature 不改变知识；Seed 不保证跨栈完全复现 → 模型运行为何分两个阶段 |
| CH-30 模型 inference：Prefill、Decode、KV Cache 与量化 | 画出 Prefill/Decode 生命周期；解释 KV Cache 与量化的内存/质量权衡 | CH-17、CH-25、CH-29 | 从固定 trace 计算 TTFT、每 Token 延迟与 KV 显存 | inference 不是 reasoning；KV Cache 不是长期记忆或答案缓存 → 多请求如何高效服务 |
| CH-31 Serving 效率：复用、内核、推测与批处理 | 区分 Prefix Cache、FlashAttention、Speculative Decoding 与 Continuous Batching，并用 TTFT、TPOT、吞吐和成本比较 | CH-26、CH-30 | 对固定工作负载读性能 trace；框架配置选做 | Model/Engine/Server/Application 不同；单项优化可能移动瓶颈 → 比较方案前怎样定义成功 |
| CH-32 先写模型评测契约 | 从用户 Scenario 建 Dataset/Metric/Rubric/Baseline；加入重复运行、不确定性、人评、泄漏和版本 | CH-01、CH-07、CH-22、CH-29 | 固定 KA-1 eval-set 与失败分类 | 单一 benchmark 不等于产品质量；LLM Judge 不能在未校准时替代人 → 如何按证据选模型 |
| CH-33 按证据选择 API 或本地模型 | 在同一契约下比较能力、语言、延迟、成本、隐私、可用性、许可和运维 | CH-31—CH-32 | 完成 KA-1：带版本和核验日期的选型报告 | 排行和产品菜单会变；Open Weight 不自动等于 Open Source → Base Model 为何还不能协助 |

### 5.6 Part VI：把基座模型变成可用能力

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-34 SFT：从续写到遵循指令 | 把对话展开为 Token 与 Loss Mask；解释角色、Chat Template、数据质量和遗忘 | CH-18、CH-22 | 小数据格式检查；训练实验可选 | SFT 是目标/数据阶段，不等于 LoRA；模板错会造成训练/运行错配 → “更好”由谁定义 |
| CH-35 偏好优化：RLHF、DPO 与对齐边界 | 用最小 RL 词汇画出偏好数据、Reward Model、RLHF/DPO 流程和 KL 约束 | CH-06、CH-34 | 对 chosen/rejected 样例做 rubric 审核 | 合意不等于真实、公平或安全；Reward Hacking → 可验证任务能否减少人工偏好 |
| CH-36 Reasoning 能力怎样训练：监督、RLVR 与 Verifier | 区分过程/结果监督、可验证奖励、Verifier、探索、蒸馏和泛化证据 | CH-32、CH-34—CH-35 | 对固定候选和验证器做错误分类 | 格式投机和训练集高分不等于新题泛化 → 运行时多算是否有帮助 |
| CH-37 Test-Time Compute：采样、搜索、验证和停止 | 比较 direct、CoT、自洽性、搜索+Verifier；绘制质量/计算预算曲线和停止条件 | CH-29、CH-36 | 固定题集重复实验；记录 token/时间/质量 | 可见解释不等于内部过程；reasoning 不能替代事实检索 → 能力不足应改哪一层 |
| CH-38 能力缺口决策：Prompt、RAG、Tool 还是改参数 | 先分类知识/行为/格式/领域/任务缺口，再用 CH-32 baseline 作选择和否决理由 | CH-22、CH-32—CH-33 | 形成与 KA-1 绑定的适配选择报告 | 这些方法不是互相替代的万能阶梯；没有基线不得升级 → 真要改参数时改什么 |
| CH-39 Continued Pretraining、Fine-tuning 与 LoRA/QLoRA | 区分继续预训练、SFT、全量更新、Adapter 和量化基座；按同一契约公平评测 | CH-07、CH-23、CH-34、CH-38 | 可选 CPU/低资源 PEFT 实验与许可证记录 | LoRA 不是 SFT，量化不是 LoRA；频繁更新知识不优先微调 → 把不改参数的输入设计好 |

### 5.7 Part VII：外接上下文、程序与知识

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-40 Prompt 之后是 Context Engineering | 为指令、示例、上下文选择/排序/压缩、分隔和污染写可测试 Context Contract | CH-02、CH-29、CH-38 | KA-2：可回归的 Context 模板 | 长窗口不等于有效利用；Prompt 不是安全边界；参数外知识仍需来源 → 输出怎样成为程序数据 |
| CH-41 Structured Output：建立机器可验证的数据契约 | 区分自由 JSON、Schema 和约束解码；处理解析、类型、缺失、拒答、失败分支和版本 | CH-40 | KA-2：输出类型化对象及契约测试 | 合法 Schema 不保证事实正确；结构化输出没有执行动作 → 模型如何提出调用 |
| CH-42 Function Calling 与 Tools：由谁真正执行 | 画出提出—校验—授权—执行—回填循环；为读/写工具分别规定权限、超时、重试、幂等和确认 | CH-01、CH-41 | KA-3：只读查询 Tool；实践前置 Primer-HTTP | 模型不拥有执行权；工具结果是不可信输入；重试可能重复副作用 → 接口碎片怎样统一 |
| CH-43 MCP：稳定互操作概念与版本边界 | 解释 Host/Client/Server 与 Tools/Resources/Prompts；定位传输、认证、授权和协议不解决的问题 | CH-42 | KA-3：最小只读 MCP 接入；具体字段放带日期 Online Layer | MCP 不是模型、单个 Tool、RAG 或 Agent；旧协议机制不进入稳定论证 → 怎样取得相关知识 |
| CH-44 现代检索：BM25、Dense、Hybrid 与 Reranker | 区分 Embedding Model、Index、Retriever、Reranker；比较 Recall@k、MRR、nDCG | CH-09—CH-10、CH-32 | KA-4：在同一 FAQ 比较词法/稠密/混合并保留基线 | 向量库不是 RAG；语义相似不保证答案相关 → 检索结果怎样送入模型 |
| CH-45 从零构建有引用的 RAG | 走通 Parse→Chunk→Metadata→Index→Retrieve→Pack→Generate→Cite/Abstain | CH-40、CH-44 | KA-4：使用版本化双语小文档，回答附来源和检索 trace | RAG 不改变参数且不能根治幻觉；Chunk 和引用会失败 → 怎样定位和改进失败 |
| CH-46 RAG 工程与分层评测 | 使用 Rewrite/Filter、Parent-child、Hybrid/Rerank、Compression；分开评 retrieval/context/generation/citation | CH-32、CH-45 | 完成 KA-4：RAG eval-set、错误分类、改进前后置信报告 | 端到端好坏不能定位环节；主观“更像对”不是评测 → 开放目标如何选择下一步 |

### 5.8 Part VIII：从工作流到可信 Agent

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-47 Agent 之前先理解 Workflow、State 与 Memory | 区分 Single Call/Chain/Workflow/Agent；画出编排器、状态/记忆、规划/工具和停止条件 | CH-42、CH-46 | KA-5：确定性 RAG Workflow，只开放一处模型决策 | 循环调用 Tool 不自动是可靠 Agent；Context、Memory、RNN State、Agent State 不同 → 流程怎样复用 |
| CH-48 Agent Skills：封装可复用做法 | 区分 Skill、Prompt、Tool、MCP、Agent；解释渐进加载、资产、版本/测试和来源审查 | CH-43、CH-47 | KA-6：把“资料来源核验”封装为可测试 Skill | Skill 不是更长 Prompt，也不天然可信；能复用不等于能安全运行 → 长任务怎样受控 |
| CH-49 可靠 Agent：权限、预算、回放与恢复 | 为状态机规定最小权限/Approval、预算/Timeout、Retry/Compensation 和 Trace/Replay | CH-43、CH-47—CH-48 | 完成 KA-6：只读自动、写操作审批、依赖锁定、失败可恢复；A2A 仅侧栏定位 | 多 Agent 默认增加复杂度；A2A 不替代 MCP；无限循环和重复副作用 → 如何量化整个系统 |
| CH-50 从模型评测扩展到系统评测 | 建立模型/检索、生成/引用、工具/轨迹、端到端矩阵；校准 LLM Judge | CH-32、CH-46、CH-49 | KA-7：System eval-set、回归矩阵、失败归因报告 | Judge 有位置/长度/自偏好；线上反馈有选择偏差 → 质量合格是否等于责任可接受 |
| CH-51 幻觉、偏见、隐私与版权：持续治理 | 为数据、模型/检索、日志/输出和人工兜底维护责任、最小化、保留期与治理说明 | CH-01、CH-23、CH-50 | KA-8：更新 Risk Register、Data/System Card 和拒答策略 | Alignment 不等于事实、公平或合法；RAG 也会引用错误来源 → 对抗者如何利用系统 |
| CH-52 Prompt Injection、Jailbreak 与不可信输入输出 | 区分直接/间接 Injection、Jailbreak 与不可信内容/输出；建立攻击链和回归方法 | CH-42、CH-48—CH-51 | KA-8：Injection/Jailbreak 回归集、输出校验和隔离测试 | 指令与数据不能靠分隔符形成安全边界；内容安全不等于权限安全 → 权限和依赖怎样控制 |
| CH-53 秘密、权限、租户隔离与供应链安全 | 处理秘密外传、最小权限/租户隔离、MCP/Skill/权重/依赖供应链及 Allowlist/Sandbox/Approval | CH-43、CH-48—CH-49、CH-52 | 完成 KA-8：权限矩阵、审批测试、依赖来源清单和供应链回归 | 能力可用不等于来源可信；Sandbox 不能替代授权和审计 → 如何落实到服务 |

### 5.9 Part IX：从原型到可维护系统

| 章节 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| CH-54 从 Notebook 到可用服务与可信 UX | 划分 UI/业务/检索/模型层；解释鉴权、流式/并发、取消/重试和分层软件测试 | CH-46、CH-52—CH-53 | KA-9：CPU 可演示服务；加入引用、拒答、不确定性、撤销/接管和可访问 UI；实践前置 Primer-HTTP | Demo 可运行不等于用户可用；软件测试不能替代概率评测 → 上线后怎样管理版本 |
| CH-55 LLMOps I：版本、Trace、发布与回滚 | 建立组件版本图、Trace/Replay、评测发布门，以及灰度/回滚记录 | CH-50、CH-54 | KA-10：可重放发布候选、发布检查表与回滚演练 | 可重放不等于输出确定；版本号不替代证据 → 运行中怎样保持服务目标 |
| CH-56 LLMOps II：Cache、韧性、SLO 与反馈 | 区分 Response/Semantic Cache；定义限流、Fallback/Circuit Breaker、SLO/告警和反馈治理 | CH-31、CH-50、CH-54—CH-55 | KA-10：监控/告警、故障注入和受治理反馈管道 | Monitoring 观察分布，不证明因果；Cache 不是知识或记忆 → 怎样综合交付全部证据 |
| CH-57 毕业项目：可评测的 Personal Knowledge Assistant | 从需求/威胁模型到 baseline、选型、RAG、Structured Output、只读 Tool/MCP、Skill、评测、安全、服务和运维闭环 | CH-33、CH-38、CH-46、CH-49、CH-51—CH-56 | 完成 KA-10：可运行服务、架构图、测试/回归集、评测报告、许可/依赖清单、风险清单、Cards、运行/回滚手册 | 成功标准不是“看起来聪明”；必须列出未解决问题、已知风险和人工责任 |

### 5.10 在线选修：多模态基础模型

| 内容 | 核心内容与验收 | 前置 | 实践与交付 | 关键边界 |
| --- | --- | --- | --- | --- |
| EXT-MM-01（Online Extension）从文本 LLM 到多模态系统 | 定位视觉/音频 Encoder、投影/交叉注意力/统一 Token 路线及多模态评测、注入和无障碍 | CH-18、CH-22、CH-51—CH-53 | 双语选修设计与评测草图；不进入 CH-57 验收 | 多模态不等于把图片直接“塞给 LLM”；读者选修且不构成主线或毕业前置 |

## 6. 贯穿项目与阶段成果

### 6.1 Mini GPT

Mini GPT 回答“模型内部是什么”。读者依次完成 Tokenizer、Dataset、Embedding、Attention、Transformer Block、LM Head、Training、Checkpoint 和 Generation。项目只服务结构理解，能够在 CPU 或浏览器环境运行，不追求工业训练规模或生成质量。

### 6.2 Personal Knowledge Assistant

Personal Knowledge Assistant 回答“模型外部还需要什么”。项目从 Keyword、Bag-of-Words Count 和 TF-IDF baseline 出发，依次加入评测契约、Context、Structured Output、Tool、MCP、Retrieval、RAG、Workflow、Skill、系统评测、安全、服务和 LLMOps。三种词法 baseline 共用同一 query、document 和 eval 集，每次能力升级都与它们比较。

### 6.3 项目里程碑

| 里程碑 | 章节 | 能力增量 | 验收证据 |
| --- | --- | --- | --- |
| MG-0 | CH-04 | N-gram 家族定位与手算/交互 Bigram | Unigram/Bigram/Trigram 上下文表、计数、平滑前后、未见组合和固定上下文失败样例 |
| MG-1 | CH-20 | Mini GPT forward 和 loss | Shape log、模块对结构图 |
| MG-2 | CH-21 | 训练、Checkpoint、生成 | seed、数据/依赖版本、验证曲线、局限 |
| KA-0 | CH-09 | Keyword/BoW Count/TF-IDF 知识搜索 | 同一固定 query/document/eval 集、Document-Term Matrix、三种 baseline 的排序/预测与错误对照 |
| KA-1 | CH-32—33 | 评测契约和模型选择 | baseline、版本、重复运行、成本/延迟 |
| KA-2 | CH-40—41 | Context Contract + Structured Output | schema、失败分支、契约测试 |
| KA-3 | CH-42—43 | 只读 Tool + MCP 接入 | 授权、参数、结果、超时 trace |
| KA-4 | CH-44—46 | 带引用 RAG 和分层评测 | retrieval/generation/citation 指标 |
| KA-5 | CH-47 | 确定性 Workflow 和受限模型决策 | 状态、停止、决策点对照 |
| KA-6 | CH-48—49 | 可复用 Skill 与可恢复 Agent | 来源、权限、审批、预算、回放 |
| KA-7 | CH-50 | 分层系统评测 | 回归矩阵、Judge 校准、失败归因 |
| KA-8 | CH-51—53 | 治理、输入输出攻击与权限/供应链安全 | Cards、攻击回归、权限矩阵、依赖来源 |
| KA-9 | CH-54 | 可用服务与可信 UX | 软件测试、请求生命周期、接管与可访问性 |
| KA-10 | CH-55—57 | 版本化运营与综合交付 | Trace、SLO、告警、发布/回滚、最终证据包 |

### 6.4 各部分完成标准

| 部分 | 核心理解成果 | 实践成果 |
| --- | --- | --- |
| I | 能画出 Token Journey，区分 Training 与 inference；能解释 N−1 上下文并手算 Bigram | 重放固定行为样例；在交互中比较 Unigram、Bigram 和 Trigram |
| II | 能读 Shape，连起 Logit→Loss→Gradient→Update；能构造并解释稀疏文本表示 | 在同一数据集上比较 Keyword、BoW Count 和 TF-IDF，并运行最小训练闭环 |
| III | 能从固定向量、梯度和递归瓶颈推出 Attention | 复现至少一个序列模型失败或分析给定 Trace |
| IV | 能逐 Shape 解释 Attention 与 Transformer Block，并比较 BERT、GPT 和 T5 | Mini GPT 可在干净 CPU 环境运行，Checkpoint 可复现 |
| V | 能连接数据、规模、训练、生成、inference、评测和模型选择 | 用固定评测契约比较至少两种模型或配置 |
| VI | 能区分预训练、SFT、偏好优化、reasoning、test-time compute 和 PEFT | 在同一评测集上比较一次训练侧或运行侧适配 |
| VII | 能区分 Schema、Tool、MCP、Retriever 和 RAG，并定位 RAG 失败层 | 带引用 RAG 能拒答，并通过检索、生成和引用的分层评测 |
| VIII | 能区分 Workflow、Agent、Skill 和 A2A，并解释权限、恢复、评测、治理和安全 | 系统具备预算、审批、回放、攻击回归和依赖来源证据 |
| IX | 能从模型层到产品层解释系统边界 | 完成可运行服务、运行指标、回滚能力和 CH-57 综合证据包 |

## 7. 核心概念边界

### 7.1 跨章职责

| 概念 | 首次定义 | 深化/回调 | 最终应用 | 禁止混淆 |
| --- | --- | --- | --- | --- |
| Model 与 System | CH-01—02 | CH-30—31、CH-42 | CH-54—57 | 模型、Engine、Server、Application 不是同一层 |
| Training / inference | CH-02 | CH-04、CH-07、CH-21、CH-30 | CH-34—37、CH-55—56 | 模型运行 inference 与解题 reasoning 不共用一个未限定的“推理” |
| Token / ID | CH-03 | CH-08、CH-19、CH-23 | CH-40、CH-55—56 | Token 不是词；ID 不是向量、训练 Token、计费 Token 或计算预算 |
| Embedding | CH-03 | CH-10、CH-17 | CH-44—46 | Embedding Table、上下文化表示、Retrieval Embedding 和 Index 分层 |
| Language Model | CH-04 | CH-10、CH-18 | CH-20—22、CH-34 | 同一目标不表示同一架构或能力规模 |
| N-gram | CH-04 | CH-09 区分特征用法、CH-10 对照神经 LM | CH-20 | N-gram 片段、BoW 中的词 N-gram 特征和用 N−1 上下文估计下一 Token 的 N-gram LM 不是同一层概念 |
| 稀疏文本表示 | CH-09 | CH-10 的稀疏→稠密比较 | CH-44—46 | Keyword、Count Vector、Document-Term Matrix、BoW、TF-IDF、Embedding 和 Index 不可互换 |
| Probability / Loss | CH-04、CH-06 | CH-07、CH-15 | CH-21、CH-32、CH-35 | 概率、事实正确性、奖励和偏好不可互换 |
| Validation | CH-07 | CH-32 | CH-36、CH-41、CH-50 | Validation Set、Schema Validation 和 Verifier 必须带对象 |
| Evaluation | CH-01 建立 | CH-07、CH-32 | CH-46、CH-50、CH-57 | Evaluation、软件 Test、线上 Monitoring 互不替代 |
| 风险与责任 | CH-01 建立 | CH-23、CH-42、CH-45 | CH-49、CH-51—57 | 任何新数据、模型、Tool、MCP 或 Skill 同步新增风险和测试 |
| 文本处理 | CH-03 | CH-08—09、CH-19 | CH-23、CH-44—45 | 清洗并非无损；Character/Byte/Token 不混用 |
| Baseline | CH-01 初始行为 | CH-07、CH-09 | CH-32—33、CH-38、CH-46、CH-57 | Base Model 与 Baseline 只是拼写相似 |
| Context / State / Memory | CH-02 | CH-11、CH-30、CH-40 | CH-45、CH-47、CH-55—56 | Context Window、KV Cache、长期 Memory、Agent State 和答案 Cache 分层 |
| Attention | CH-14 | CH-15—17 | CH-20、CH-25—26、CH-28 | Cross/Self-Attention 有别；Attention Weight 不自动是因果解释 |
| Transformer | CH-17 | CH-18、CH-20 | CH-22、CH-25—26 | Attention、Transformer、GPT、LLM 不是同义词 |
| 架构/目标/阶段 | CH-18 | CH-22、CH-34—36 | CH-38—39 | Encoder/Decoder、MLM/CLM、Base/SFT、产品名是不同分类轴 |
| Tokenizer | CH-03 基础 | CH-19 | CH-20、CH-23 | Tokenizer 必须与模型/Checkpoint 配套且版本化 |
| Pretraining / Fine-tuning / LoRA | CH-18 | CH-23—24、CH-34 | CH-38—39 | SFT 是训练阶段/目标；LoRA 是参数更新方法；量化不是 LoRA |
| Sampling / Cache | CH-04 预告 | CH-29—31 | CH-37、CH-55—56 | Temperature 不改知识；KV/Prefix/Response/Semantic Cache 不同 |
| Reasoning | CH-22 定位 | CH-36 | CH-37、CH-50 | 可见 CoT 不等于内部真实过程；reasoning 不替代检索 |
| Prompt / Context | CH-38 决策层 | CH-40 | CH-45、CH-47、CH-57 | Prompt 是 Context Engineering 一部分，也不是安全边界 |
| Structured Output / Tool | CH-41 | CH-42 | CH-47、CH-54、CH-57 | 数据契约不执行动作；应用而非模型执行 Tool |
| MCP / Skill / Agent / A2A | CH-43 | CH-47—49 | CH-57 | 它们不是版本升级链；MCP 连能力，Skill 复用做法，A2A 只连独立 Agent |
| Retrieval / RAG | CH-09 baseline | CH-44—46 | CH-50、CH-57 | RAG 不改参数；检索到和正确使用必须分开评 |
| Alignment / Governance / Security | CH-35 | CH-42、CH-49 | CH-51—53、CH-57 | 合意、正确、公平、内容安全和权限安全是不同判断 |

### 7.2 可复用心智模型

| 心智模型 | 首次建立 | 后续应用 |
| --- | --- | --- |
| Model ≠ System | CH-01 | CH-57 |
| 一个 Token 的旅程 | CH-02 | CH-20、CH-30 |
| Training ≠ inference ≠ reasoning | CH-02 | CH-37 |
| Token ≠ Word；ID ≠ Embedding | CH-03 | CH-19、CH-44 |
| N−1 Token Context → P(next token)：N-gram LM | CH-04 | CH-10、CH-20、CH-29 |
| Forward → Loss → Gradient → Update | CH-07 | CH-21、CH-39 |
| 同一问题的多代上下文机制 | CH-10 | CH-14—17 |
| Q/K/V 与信息流 | CH-14—15 | CH-20、CH-28 |
| Attention + Residual/Norm + FFN | CH-17 | CH-25—26 |
| Architecture ≠ Objective ≠ Training Stage | CH-18 | CH-22、CH-34 |
| Model + Data + Compute | CH-24 | CH-27 |
| Prompt/RAG/Tool/Training 改变不同层 | CH-38 | CH-57 |
| Prompt → Prefill → KV Cache → Decode | CH-30 | CH-55—56 |
| Retrieve → Context → Generate → Cite | CH-45 | CH-46、CH-57 |
| Model proposes; application validates and executes | CH-42 | CH-49、CH-57 |
| Agent = Model + Orchestrator + State + Tools + Policy | CH-47 | CH-49 |
| 分层 Evaluation 定位失败 | CH-32 | CH-46、CH-50 |
| Probabilistic Model + Deterministic Controls | CH-41 | CH-52—57 |
| Count → Reweight → Learn：BoW → TF-IDF → Static Dense → Contextual | CH-09 | CH-10、CH-18、CH-44 |

## 8. 内容资产与发布形态

### 8.1 每章成品

每个主线章节都包含：

- 一个明确问题及其与前后章节的联系。
- 自洽的核心解释，不把唯一结论藏在代码、侧栏或外部链接中。
- 至少一个最小数字例、机制图或可观察实验。
- 至少一个失败案例，以及适用范围和容易混淆的边界。
- 核心理解自测与答案。
- 适用时提供 CPU 或浏览器可运行的代码、Notebook、数据和工程任务。
- 核心来源与进一步阅读。

### 8.2 代码、数据与图形

- 中英文版本共享同一套代码逻辑；标识符和代码注释使用英文，Notebook 叙述可以本地化。
- 核心代码优先使用小函数、显式输入输出和可见 Shape；失败输出作为测试资产保留。
- 核心实践可在 CPU 或浏览器运行；GPU 实验明确标为选做。
- 可复现实验包含依赖、随机种子、数据版本、模型或 tokenizer 版本和预期输出。
- 随书数据体量小、许可清楚、可再分发，并覆盖中英文案例。
- Token、ID、Vector、Parameter、Computation、External Data 和 State 在图中使用稳定的视觉编码；数据流、参数更新和控制流彼此可辨。
- 图、数据、Notebook 与第三方素材逐项标明来源和许可；无再分发权的内容只提供链接。

### 8.3 双语关系

- 英文与中文使用相同的章节编号、概念依赖、公式、图示结构和工程行为。
- 中文术语在首次出现时给出稳定英文对应；关键术语在全书保持一致。
- 本地化可以替换语言与文化案例，但不能新增只存在于中文版本的技术事实。
- 代码标识符、配置键、协议字段和错误文本保留原文，解释与替代文本本地化。
- 每个语言页面都能切换到同一章节的另一语言版本。

### 8.4 渠道职责

| 渠道 | 内容 |
| --- | --- |
| Web Edition | 中英文完整正文、目录、搜索、交叉引用、自测、勘误、代码快照和在线扩展 |
| GitHub | 可构建源稿、代码、Notebook、语义图源、测试、数据说明与 Issue |
| Blog | 发布公告、主题导读和 Part 摘要，不复制章节正文 |
| RSS | 按语言提供摘要并链接到对应章节 |
| 第三方平台 | 短节选、导读或公告，链接回正式 Web 页面 |

PDF、EPUB 和纸书不属于本版交付范围。

### 8.5 Web 形态

Web Edition 使用 Astro Starlight 构建，以 GitHub Pages 和自有域名作为默认托管组合。Starlight 负责书籍内容路由、双语导航、站内搜索和阅读界面，并通过 Custom CSS 与组件覆盖复用主站的颜色、字体、间距和交互语言，避免形成割裂的独立站点。主站发布工作流从公开的书籍仓库检出源码，将 Starlight 静态产物合并到统一的 GitHub Pages Artifact；书籍仓库不单独部署，也不需要跨仓库发布凭据。

页面包含双语目录、站内搜索、交叉引用、公式、代码、无障碍图示、移动端布局、RSS、Sitemap、Canonical URL 和 hreflang。每本书占用 `/books/<book-slug>/` 命名空间；本书的永久 `book-slug` 为 `understanding-llms`，语言路径位于书籍路径之下，以便未来新增书籍时保持边界稳定。

稳定路径为：

~~~text
/books/understanding-llms/
/books/understanding-llms/en/ch-01/
/books/understanding-llms/zh-hans/ch-01/
/books/understanding-llms/en/rss.xml
/books/understanding-llms/zh-hans/rss.xml
/books/understanding-llms/en/glossary/
/books/understanding-llms/zh-hans/glossary/
/books/understanding-llms/en/changelog/
/books/understanding-llms/zh-hans/changelog/
/books/understanding-llms/en/errata/
/books/understanding-llms/zh-hans/errata/
/blog/
/rss.xml
/about/
~~~

每个完整语言页面使用本语言自指 Canonical，并与对应页面双向关联；语言切换保持在当前章节。英文和中文分别生成搜索索引、Sitemap 和 RSS。

## 9. 质量标准

| 范围 | 合格条件 |
| --- | --- |
| 章节内容 | 问题、机制、最小证据、失败边界、自测、答案和来源齐全；前置概念已在正文建立 |
| 教学效果 | 核心理解路径不依赖代码；类比边界明确；章末能够说明新增能力和下一问题 |
| 技术准确性 | 重要论断有可靠来源；公式、术语、图示和跨章定义一致；时效信息带日期与来源 |
| 实践资产 | 核心代码和 Notebook 可在干净 CPU 或浏览器环境复现；依赖、数据和随机性信息完整 |
| 双语质量 | 中英文技术含义、公式、风险和工程行为一致；本地化不改变结论 |
| 可访问性 | 图有替代文本，信息不只依赖颜色；导航、代码和公式可在移动端使用 |
| 系统可靠性 | 项目含分层评测、权限边界、失败恢复、攻击回归、Trace、版本和运行说明 |
| 许可与安全 | 所有公开资产来源和许可明确；不含 Secret、受限数据或来源不明的依赖 |
| 全书完整性 | CH-01—CH-57、两份 Primer、两个贯穿项目和 EXT-MM-01 共同覆盖读者契约；不存在已知的严重事实、安全或许可问题 |

## 10. 参考框架与核心资料

以下资料构成本书的课程框架、技术论证和工程实现参考。

### 10.1 构建、托管与国际化

- [Astro Starlight 文档](https://starlight.astro.build/)
- [Starlight 国际化](https://starlight.astro.build/guides/i18n/)
- [Starlight 自定义样式](https://starlight.astro.build/guides/css-and-tailwind/)
- [Google 多语言站点指南](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)
- [GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub Pages 平台限制](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [GitHub Pages 自有域名配置](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)

### 10.2 教材与课程

- Jurafsky、Martin：[Speech and Language Processing（2026 在线稿）](https://web.stanford.edu/~jurafsky/slp3/)——覆盖 token、n-gram、分类、embedding、LLM、Transformer、后训练、masked LM、RAG、RNN/LSTM 等主线。
- Stanford：[CS336 Language Modeling from Scratch（2026）](https://cs336.stanford.edu/)——覆盖 tokenizer、架构、GPU/内核、并行、scaling law、模型推断、评测、数据、SFT/RLHF/RLVR 与多模态。
- Hugging Face：[LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)——作为模型使用、tokenizer、数据集、微调和常见 NLP 任务的实践补充；其本身要求 Python，本书通过 Primer-PY 和相关基础章节填补这一门槛。

### 10.3 Transformer、预训练与规模化

- Vaswani et al.：[Attention Is All You Need](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)。
- Kudo、Richardson：[SentencePiece](https://aclanthology.org/D18-2012/)。
- Peters et al.：[Deep Contextualized Word Representations（ELMo）](https://aclanthology.org/N18-1202/)。
- Devlin et al.：[BERT](https://aclanthology.org/N19-1423/)。
- Radford et al.：[Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)。
- Raffel et al.：[T5](https://www.jmlr.org/papers/v21/20-074.html)。
- Kaplan et al.：[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)。
- Hoffmann et al.：[Training Compute-Optimal Large Language Models](https://proceedings.neurips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract.html)。
- Fedus et al.：[Switch Transformers](https://arxiv.org/abs/2101.03961)。
- Gu、Dao：[Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)——用于给线性 Attention、状态空间模型等 Transformer 替代路线定位置，而不是另开一条完整实现线。
- Jurafsky、Martin：[Speech and Language Processing：Interpretability](https://web.stanford.edu/~jurafsky/slp3/10.pdf)——用于区分 probing、attribution、causal intervention 等不同解释证据。

### 10.4 后训练、解题推理与高效适配

- Ouyang et al.：[Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)。
- Rafailov et al.：[Direct Preference Optimization](https://arxiv.org/abs/2305.18290)。
- Lightman et al.：[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)——过程监督与结果监督的代表性入口。
- DeepSeek-AI et al.：[DeepSeek-R1](https://arxiv.org/abs/2501.12948)——用于理解可验证奖励、解题推理行为和蒸馏的现代实例，不把单一模型训练配方写成通用定律。
- Wei et al.：[Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)。
- Snell et al.：[Scaling LLM Test-Time Compute Optimally](https://arxiv.org/abs/2408.03314)。
- Hu et al.：[LoRA](https://arxiv.org/abs/2106.09685)。
- Dettmers et al.：[QLoRA](https://arxiv.org/abs/2305.14314)。
- Dao et al.：[FlashAttention](https://arxiv.org/abs/2205.14135)。
- Ainslie et al.：[Grouped-Query Attention](https://arxiv.org/abs/2305.13245)。
- Leviathan et al.：[Speculative Decoding](https://arxiv.org/abs/2211.17192)。

### 10.5 Function Calling、MCP、Skills 与 Agent

- OpenAI：[Function Calling Guide](https://developers.openai.com/api/docs/guides/function-calling)——用于校准“模型提出工具调用、应用执行并回填结果”的基本循环；具体 API 字段只作为实现示例，不当作跨厂商标准。
- Model Context Protocol：[2026-07-28 Specification](https://modelcontextprotocol.io/specification/2026-07-28)——规范入口，涵盖无会话核心、逐请求元数据、`server/discover`、Tools/Resources/Prompts、multi-round-trip input、授权和扩展。
- Model Context Protocol：[The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)——版本说明；明确 Roots、Sampling、Logging 和旧 HTTP+SSE 已弃用，并说明 Tasks/MCP Apps 的扩展定位。
- Model Context Protocol：[SEP-2577](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging)——用于防止旧教程中的 Roots/Sampling/Logging 被误写成新实现应采用的核心能力。
- Agent Skills：[Specification](https://agentskills.io/specification)——开放 Skill 目录、SKILL.md、渐进加载及 scripts/references/assets 等约定。
- Model Context Protocol：[Skills Over MCP Working Group](https://modelcontextprotocol.io/community/working-groups/skills-over-mcp)——用于跟踪 Skill 发现和分发如何与 MCP 协作。
- Agent2Agent Protocol：[A2A Specification](https://a2a-protocol.org/latest/specification/)——用于说明独立 Agent 之间协作的协议边界；只作进阶定位，不让初学者误以为多 Agent 是默认架构。
- Yao et al.：[ReAct](https://arxiv.org/abs/2210.03629)。

### 10.6 RAG、评测与安全

- Lewis et al.：[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://proceedings.neurips.cc/paper/2020/hash/6b493230-Abstract.html)。
- Stanford CRFM：[HELM](https://crfm.stanford.edu/helm/)——强调跨场景、多指标、透明和可复现的整体评测。
- NIST：[AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)——用于把治理组织为 Govern、Map、Measure、Manage 的持续过程，而不是上线前的一次检查。
- OWASP GenAI Security Project：[Top 10 for LLM Applications 2025](https://genai.owasp.org/download/43299/)——用于应用安全主题的威胁清单。
- Full Stack Deep Learning：[LLM Bootcamp：LLMOps](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/llmops/)——作为部署、可观测性、反馈和持续迭代的工程入口；具体平台界面不进入稳定主线。

### 10.7 多模态基础模型

- Radford et al.：[CLIP](https://proceedings.mlr.press/v139/radford21a.html)。
- Alayrac et al.：[Flamingo](https://proceedings.neurips.cc/paper_files/paper/2022/hash/960a172bc7fbf0177ccccbb411a7d800-Abstract-Conference.html)。
- Liu et al.：[LLaVA](https://arxiv.org/abs/2304.08485)。
