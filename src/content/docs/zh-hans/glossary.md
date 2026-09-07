---
title: "词汇表"
description: "全书采用的中英文术语、定义和概念边界。"
sidebar:
  order: 1
---

词汇表会随正式章节一起维护。术语首次出现时给出稳定的英文对应；同一个词在模型、训练、运行和系统层含义不同时，会明确标注所在层级。

| 中文 | English | 边界 |
| --- | --- | --- |
| 训练 | training | 通过优化过程改变模型参数。 |
| 模型运行 | inference | 使用固定参数执行模型计算，不等于 reasoning。 |
| 解题推理 | reasoning | 为解决问题组织中间计算或搜索，不等于 inference。 |
| 上下文 | context | 当前请求可见的信息，不等于参数、长期记忆或 Agent State。 |
