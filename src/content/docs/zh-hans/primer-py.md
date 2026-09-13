---
title: "Python 与 Notebook 基础"
description: "从读文件、字符计数和定位报错开始，学会在新内核中运行本书的小型 NumPy 与 CPU PyTorch 练习。"
published: 2026-09-13
---

## 让纸上的计算也能在程序里看清楚

请先读完[第 5 章](../ch-05/)核心正文。你已经知道行、维度和矩阵乘法是什么意思；这份补充材料教你怎样把这些运算表达给计算机。不需要预先学过编程，也不必学完整门 Python 课程才继续读书。我们的目标是看懂一小段计算，并能有把握地改动其中一个条件。

我们会从[第 4 章](../ch-04/)的 `ab`、`ab`、`ac` 开始计数，保留各条字符串的边界，然后回做参数化字符 N-gram 练习。之后再做第 5 章的 NumPy 形状练习，最后进入第 7 章训练实践。MG-0 的 **项目里程碑** 仍是完成那个计数生成器，不是保存神经模型参数的“模型检查点”。

程序是一串指令， **Python** 是这里使用的编程语言。以 `.py` 结尾的文件把指令保存为文本。 **Notebook** 文件以 `.ipynb` 结尾，按顺序保存多个单元格：有些放讲解，有些放可以执行的代码，代码单元格还可以保存输出。真正执行代码并记住变量的，是正在运行的 Python 进程，称为 **内核（kernel）**。

这份“记忆”可能掩盖问题。假如单元格 3 用了单元格 2 定义的变量，单独运行第 3 格，在旧内核中可能成功，换成新内核却会报错。文件里保存的输出只能说明过去执行过某次计算，不能证明眼前的代码今天还能复现它。因此，本书的复现规则是：重启内核，按顺序运行所有代码单元格。配套执行脚本会这样做。理解计算所需的信息也都直接列在教材中。

## 先找到文件，再运行代码

**文件路径（file path）** 告诉计算机文件在哪里。书籍仓库中的 `data/part-i/ngram.json` 保存原始字符串，`code/part-ii/ngram.py` 保存 Python 实现。斜杠分隔不同层级的目录。相对路径从程序的 **工作目录（working directory）** 出发解释；它不一定就是编辑器当前打开文件所在的目录。

**例 P.1 — 读取与教材相同的固定数据。** 先进入 `understanding-llms` 仓库目录。下面的代码读取文件并打印训练字符串：

```python
from pathlib import Path
import json

root = Path.cwd()
fixture_path = root / "data" / "part-i" / "ngram.json"
fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
print(fixture["train"])
```

输出为 `['ab', 'ab', 'ac']`。`Path.cwd()` 取得当前目录，这里的 `/` 用来拼接路径，并不是数值除法。`read_text` 按 UTF-8 编码读取文本，`json.loads` 再解析其中的数据结构。 **JSON** 是一种文本格式，可以表示列表、带名称的字段和简单数值。读取文件与执行文件是两件事。若提示找不到文件，先打印 `root` 和 `fixture_path`，确认程序究竟去了哪里；为了消除报错而改动数据，会改变实验本身。

配套 Notebook 会从当前目录向上查找，同时找到这份数据和书籍配置后，才认定找到了仓库根目录；找不到就明确报错。因此，从 Notebook 所在目录打开它也可以，不必猜测路径前面该写几个 `../`。

本次实测环境为 Python 3.12.10、NumPy 2.0.2、PyTorch 2.7.0，使用 CPU。这些版本用于固定复现条件，并不表示它们是最新版本。 **包（package）** 是安装到 Python 环境中、供程序复用的代码；`import` 把其中有名称的工具引入当前程序。单独的环境可以让本练习与其他项目的依赖分开。在终端——也就是输入命令的窗口——进入书籍目录后，本地准备步骤如下：

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r code/part-ii/requirements.txt
.venv/bin/python code/part-ii/run_notebooks.py --only 01-primer-and-ngram.ipynb
```

第一条命令创建环境，第二条安装固定版本的依赖，第三条只从新内核运行第一个 Notebook。先读完本 Primer，再执行这一步；其余 Notebook 按所在章节安排。如果系统找不到 `python3.12`，要先安装 Python 3.12；[官方发布页](https://www.python.org/downloads/release/python-31210/)列出了本次实测版本及各平台安装文件。这是用于复现的历史版本，不是最新补丁版本。Windows 中该环境的 Python 路径是 `.venv\Scripts\python.exe`，应替换上面的 `.venv/bin/python`。安装依赖需要联网，练习本身使用本地数据，不需要 GPU、模型账号或付费 API。如果编辑器已经支持 Notebook，选择同一个环境作为内核即可。配套 README 记录了实际测试的平台；Windows 路径只是使用方式的调整，不代表另做过 Windows 实测。

## 给数值起个名字，再看看它是什么

**变量（variable）** 是绑定到某个值的名称。单个 `=` 表示赋值，告诉 Python 这个名字现在指向什么；它不是让 Python 求解等式。

```python
text = "ab"
count = 2
count = count + 1
print(text, count)
```

输出是 `ab 3`。最后一次赋值先在右侧使用旧值 2，算出 3，再让 `count` 指向 3。`"ab"` 是 **字符串（string）**，其中的文本码点按顺序排列。`2` 是整数，`"2"` 却是字符串。因此 `2 + 1` 得到 3，`"2" + "1"` 得到 `"21"`：字符串的 `+` 表示拼接文本。`int("2")` 才会明确地把这个合法数字字符串转成整数。`0.5` 这样的值采用浮点数存储，但并非每个十进制小数都能在机器里精确表示。

**列表（list）** 按顺序保存多个值，重复项也会保留：

```python
texts = ["ab", "ab", "ac"]
print(texts[0], texts[-1], len(texts))
print(texts[0][1])
```

两行输出分别是 `ab ac 3` 和 `b`。下标 0 取第一项，−1 取最后一项。第二行先取第一个字符串，再取其中下标为 1 的字符。`len(texts)` 数的是列表项数，不是所有字母加起来有多少个。下标 3 会报错，因为三项列表只有 0、1、2 这三个下标。两份 `ab` 是两条观测，删除重复项会改变第 4 章的计数。

**字典（dictionary）** 则用键来对应值。例如 `{"a": 0, "b": 0, "c": 0}` 为每个有名称的字符保存一个计数。列表用位置取值，字典的键 `"b"` 则直接说出要找哪一项。`counts["b"]` 取得它的值，`counts["b"] = 2` 把它改为 2。这也解释了为什么能用 JSON 数据中的 `"train"` 字段取出那组训练字符串。

## 重复计算，同时守住字符串边界

**例 P.2 — 先数字母，再区分字母与预测事件。**

```python
texts = ["ab", "ab", "ac"]
counts = {"a": 0, "b": 0, "c": 0}
for text in texts:
    for character in text:
        counts[character] = counts[character] + 1
print(counts)
```

结果是 `{'a': 3, 'b': 2, 'c': 1}`。 **循环（loop）** 会重复执行缩进的代码。外层循环每次取一条字符串，内层循环逐个访问这条字符串的字符。Python 用缩进表明哪些语句属于循环；最后的 `print` 没有缩进，位于两个循环之外，所以只执行一次。

这六个字母还不是第 4 章的九次预测事件。三条字符串各自还要预测一次结束标记 `EOS`。我们也尚未得到 Bigram 计数：它需要记住前一个字符，并在每条新字符串开头把它重设为 `BOS`。下面只统计跟在 `a` 后面的目标：

```python
a_row = {"a": 0, "b": 0, "c": 0, "EOS": 0}
for text in texts:
    previous = "BOS"
    for target in list(text) + ["EOS"]:
        if previous == "a":
            a_row[target] += 1
        previous = target
print(a_row)
```

输出为 `{'a': 0, 'b': 2, 'c': 1, 'EOS': 0}`。`list(text)` 把字符串变成字符列表，再加上 `["EOS"]`，就多了一个结束标记。`if` 只在条件成立时执行其下方缩进的语句。`==` 比较两个值，与赋值用的 `=` 不同；`+= 1` 则把已有计数加一。最后的 `previous = target` 对每个目标都会执行，不管刚才条件是否成立。若把 `previous = "BOS"` 移到外层循环之外，就会错误地把不同字符串连起来。

## 把可复用的计算写成函数，并读懂失败

**函数（function）** 把一项操作封装起来，给输入命名，并明确输出。`def` 开始定义函数，`return` 把结果交回调用它的位置。

```python
def smoothed_probability(count, row_total, candidates, alpha):
    denominator = row_total + alpha * candidates
    if denominator == 0:
        raise ValueError("empty unsmoothed context")
    return (count + alpha) / denominator

print(smoothed_probability(2, 3, 4, 1))
```

这段代码打印 `0.42857142857142855`，也就是 $3/7$ 的浮点表示。四个实参依次表示：观察计数 2、该行总数 3、四个候选目标、每个候选补一个计数。函数并不负责查表，也不知道哪个词正确；它的契约只是完成这项计算。项目里的完整实现还会检查阶数、词表等条件。

分母为零时，`raise` 会主动发出 **异常（exception）**，而不是编造一个概率。报错中的 **调用追踪（traceback）** 列出通向错误的调用过程。先读最后一行的错误类型和消息，再找到自己代码中最后一处相关位置。即使错误来自某个库，起因也可能是你传入的形状或路径不对。

**表 P.1 — 四类报错与第一步检查。**

| 错误 | 在这里常见的原因 | 先检查什么 |
| --- | --- | --- |
| `NameError: name 'texts' is not defined` | 当前内核尚未运行准备数据的单元格 | 重启并从第一格开始运行 |
| `FileNotFoundError` | 相对路径从另一个工作目录出发 | 打印解析后的完整路径 |
| `IndexError: list index out of range` | 下标达到或超过列表长度 | 打印下标和 `len(...)` |
| `ModuleNotFoundError: No module named 'numpy'` | 当前 Python 环境没有安装这个包 | 确认正在使用哪个 Python 或内核 |

可以处理预料之中的异常，同时让无关错误继续显现：

```python
try:
    smoothed_probability(0, 0, 4, 0)
except ValueError as error:
    print(str(error))
```

输出为 `empty unsmoothed context`。这是一次被明确检查的失败，不是概率为零。如果把所有异常都捕获后返回 0，就会把数据缺失、程序错误和合法的零概率混成同一种结果。Python 教程说明了通用的控制流程与异常规则；这里的计数练习由本书原创。[Python 教程](https://docs.python.org/3.12/tutorial/)

## 数组还要说明形状、存储类型和运行位置

普通列表能保存数值，却不直接提供这里所需的所有数值运算。例如 `[1,2] * 2` 会把列表重复成 `[1,2,1,2]`。NumPy 数组则支持数值乘法：

```python
import numpy as np

x = np.array([[2, 1], [1, -1]], dtype=np.float64)
w = np.array([[1, 0, -1], [0, 1, 1]], dtype=np.float64)
print(x.shape, (x @ w).tolist())
print((x * 2).tolist())
```

第一行输出为 `(2, 2) [[2.0, 1.0, -1.0], [1.0, -1.0, -2.0]]`，第二行是 `[[4.0, 2.0], [2.0, -2.0]]`。形状外的圆括号表示 **元组（tuple）**：它也按顺序存放内容，但不能直接替换其中某一项。`@` 执行第 5 章的矩阵乘法，`*` 在这里逐项相乘，`tolist()` 则把数组内容转成便于打印的列表。

**数据类型（dtype）** 规定每个值怎样存储。`float64` 为每个浮点数使用 64 位，并不意味着有 64 位十进制有效数字。整数 ID 应保持为整数；把 ID 转成浮点数，也不会让它变成嵌入向量。

PyTorch 提供张量运算，还能记录第 7 章计算梯度所需的依赖关系：

```python
import torch

ids = torch.tensor([0, 1], dtype=torch.long, device="cpu")
weights = torch.tensor([0.0, 0.0], dtype=torch.float64,
                       device="cpu", requires_grad=True)
print(tuple(ids.shape), weights.dtype, weights.device)
```

结果是 `(2,) torch.float64 cpu`。 **设备（device）** 表示数值存在哪里、计算在哪里进行；本练习明确使用 CPU。`torch.long` 是查表下标和类别编号目标使用的整数类型。`requires_grad=True` 请求 PyTorch 跟踪涉及该参数的运算，以便稍后计算导数；它不会立即开始训练，也不会让 ID 变成可求导的数值。一起参与运算的输入和参数，需要有兼容的设备与数据类型。知道各自职责后有意转换一个操作数，才是在修复问题；不了解职责而反复把所有内容转来转去，无法解释错误的来源。[PyTorch 张量教程](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

## 回做 MG-0，再完成形状练习

第一个 Notebook 从 `code/part-ii/ngram.py` 导入 `fit`、`sequence_probability` 和 `generate`。`fit(texts, vocabulary, n=2, alpha=0)` 明确指定阶数与平滑量。实现会在每条字符串开头重置边界，使用前 $n-1$ 个符号，并把 `EOS` 包含在四个目标中。一个从未见过、又未做平滑的上下文没有定义好的概率分布；若前缀的概率已经是零，整条序列也只能是零概率。

**表 P.2 — 包含 EOS 的全部阶数与平滑对照。** 预期值来自第 4 章的分数推导，独立于 Python 实现。

| 阶数 $n$ | 补入计数 $\alpha$ | $P(\texttt{ac})$ | $P(\texttt{aa})$ |
| --- | --- | --- | --- |
| 1 | 0 | $1/81$ | $1/27$ |
| 2 | 0 | $1/3$ | 0 |
| 3 | 0 | $1/3$ | 0 |
| 1 | 1 | $32/2197$ | $64/2197$ |
| 2 | 1 | $16/245$ | $4/343$ |
| 3 | 1 | $16/245$ | $1/49$ |

按 `a,b,c,EOS` 的顺序，Bigram 的 `a` 行是 `[0,2,1,0]`。固定阶数 2、不做平滑、种子 42，并使用本书指定的 LCG32 随机数算法，三次抽取值约为 0.252345、0.088125、0.577281，对应输出 `a,b,EOS`。只有种子还不够，随机算法和候选顺序也必须一致。原有诊断样例 `ac` 与训练字符串重复，因此这张表不能证明泛化能力。

完成复现后，再打开 `02-shapes-and-loss.ipynb`。它先做第 5 章的形状计算，其中损失部分读完第 6 章后再做；`03-training.ipynb` 则安排在第 7 章之后。可以先看保存的输出，再改一个明确条件。保留原文件，或把自己的变体另存一份，才能分清哪个结果属于基准运行。

## 小结

变量为值命名，列表保留顺序和重复项，字典让名称与值对应。循环重复缩进的代码，条件选择分支，函数则把可复用操作的输入输出写清楚。路径依赖工作目录，Notebook 中的变量依赖内核执行过什么。数组还要声明各维、数据类型和设备。这些细节决定实验的含义，并非可以随意忽略的语法装饰。

## 习题

1. 把输入改为 `['ab','ac']`，字母计数和 Bigram 的 `a` 行各是什么？为什么删掉一条重复记录会改变概率？
2. Notebook 显示着预期输出，重启内核后却出现 `NameError`。旧输出能证明什么？还要修复什么？
3. 有人想把数值乘以 2，却写了 `[1,2] * 2`。实际结果是什么？怎样用 NumPy 修正？Token ID 应使用什么数据类型？
4. 某行没有观测，候选数为 4，$\alpha=1$。`smoothed_probability(0,0,4,1)` 返回什么？再解释不做平滑时的情况，分清零与未定义。

## 参考解答

1. 字母计数变为 `{'a':2,'b':1,'c':1}`，`a` 行变为 `[0,1,1,0]`。不做平滑时，$P(b\mid a)=1/2$，原来则是 $2/3$。重复记录是多出来的一次训练观测，不是无关的排版。
2. 它记录某次过去执行的结果，当时可能留有旧变量，也可能运行了不同代码。应补上缺失的定义或修正单元格顺序，再从新内核完整运行。截图或保存的结果本身不能证明可以复现。
3. 列表会重复为 `[1,2,1,2]`。`np.array([1,2]) * 2` 才会得到数值 `[2,4]`。ID 应用整数类型，例如 PyTorch 嵌入查表使用 `torch.long`；浮点向量承担的是另一种职责。
4. 分子为 1，分母为 4，结果是 $1/4$。若 $\alpha=0$，分子与分母都为零，函数会抛出 `ValueError`。这表示无法为该上下文估计一个分布，不表示某个候选的估计概率恰好为零。

## 参考文献

- [Python 3.12 教程](https://docs.python.org/3.12/tutorial/)。第 3—5 章解释值、容器与控制流程，第 7、8、12 章介绍文件、异常与环境，可查本书原创练习背后的语言规则。
- [NumPy：`matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)。规定计数 Notebook 之后所用的矩阵运算；教材先解释数值含义，再在这里引入语法。
- [PyTorch：张量教程](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)。解释张量属性与数值操作，包括 dtype 和 device。实际运行版本另在配套文件中固定。
