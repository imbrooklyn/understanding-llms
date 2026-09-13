---
title: "Python and Notebook Foundations"
description: "Learn enough Python to inspect files, count characters, diagnose errors, and run small NumPy and CPU PyTorch practices in a fresh notebook kernel."
published: 2026-09-13
---

## A program should make the paper calculation inspectable

Read the core of [Chapter 5](../ch-05/) first. You already know what a row, an axis and a matrix multiplication mean; this primer supplies a way to express those operations to a computer. No previous programming course is assumed. The goal is to inspect and change a small calculation, not to learn all of Python before continuing the book.

We will count the strings `ab`, `ab`, `ac` from [Chapter 4](../ch-04/), preserve their boundaries, and return to its parameterized character N-gram practice. Then run Chapter 5's NumPy shape exercise. Chapter 7's training practice comes after these steps. The MG-0 **project milestone** is still the completed counting generator; it is not a saved neural-model checkpoint.

A program is a sequence of instructions. **Python** is the language used here. A file ending in `.py` stores those instructions as text. A **Notebook**, ending in `.ipynb`, stores an ordered collection of cells: some explain the work, while code cells contain executable instructions and may save their output. The **kernel** is the running Python process that executes cells and remembers variables.

That memory can hide a mistake. If cell 3 uses a variable created in cell 2, running cell 3 alone may fail in a new kernel but appear to work in an old one. A saved output is evidence of an earlier execution, not proof that today's visible code can reproduce it. Our reproducibility rule is to restart the kernel and execute all code cells in order. The accompanying execution script does exactly that. Everything necessary for understanding the calculations is also printed in the chapters.

## Find the files before running them

A **file path** tells the computer where a file is. The book repository contains `data/part-i/ngram.json`, with the original strings, and `code/part-ii/ngram.py`, with the Python implementation. The slash separates directories. A relative path is interpreted from the program's **working directory**, which need not be the directory shown in an editor tab.

**Example P.1 — Read the same fixed data as the book.** Start in the `understanding-llms` repository directory. This code loads the file and prints the training strings:

```python
from pathlib import Path
import json

root = Path.cwd()
fixture_path = root / "data" / "part-i" / "ngram.json"
fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
print(fixture["train"])
```

The output is `['ab', 'ab', 'ac']`. `Path.cwd()` asks for the current directory. The `/` operations join path components here; they are not numerical division. `read_text` reads the file as UTF-8 text, and `json.loads` interprets its structured contents. **JSON** is a text format for lists, named fields and simple values. Reading a file is different from executing it. If the file is not found, first print `root` and `fixture_path`; changing the data to make an error disappear would change the experiment.

The supplied notebooks find the repository by looking in the current directory and its parents for this fixture and the book configuration. They fail explicitly if that boundary is missing. This permits opening a notebook from its own directory without guessing how many `../` segments to write.

The tested environment uses Python 3.12.10, NumPy 2.0.2 and PyTorch 2.7.0 on CPU. These are reproducibility choices, not claims about the newest versions. A **package** is reusable code installed into a Python environment; `import` makes its named tools available to your program. An environment keeps this exercise's packages separate from other projects. From a terminal—a window in which you type commands—in the book directory, the local setup is:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r code/part-ii/requirements.txt
.venv/bin/python code/part-ii/run_notebooks.py --only 01-primer-and-ngram.ipynb
```

The first command creates the environment, the second installs the pinned dependencies, and the third runs only the first notebook from a fresh kernel. Read the rest of this primer before that first run; later notebooks follow their chapters. If `python3.12` is not found, install Python 3.12 first; the [official release page](https://www.python.org/downloads/release/python-31210/) identifies the measured release and its platform installers. It is an archived reproducibility version, not the latest patch release. On Windows the environment's Python executable is `.venv\Scripts\python.exe`; use that in place of `.venv/bin/python`. Installation needs internet access; the exercises themselves use local data. No GPU, model account or paid API is needed. If an editor already supports notebooks, select the same environment as its kernel. The companion README documents the actual tested platform; the Windows command is a path adaptation, not a claim of a separate Windows test.

## Give a value a name, then inspect it

A **variable** is a name bound to a value. Assignment uses a single `=`; it tells Python what value the name refers to now. It does not assert an equation that Python must solve.

```python
text = "ab"
count = 2
count = count + 1
print(text, count)
```

The output is `ab 3`. The right side of the last assignment uses the old value 2, computes 3, then binds `count` to 3. `"ab"` is a **string**, an ordered sequence of text code points. `2` is an integer, whereas `"2"` is a string. Thus `2 + 1` is 3, but `"2" + "1"` is `"21"`: string `+` joins text. `int("2")` explicitly converts that valid numeral to an integer. A decimal value such as `0.5` uses floating-point storage; not every decimal fraction has an exact machine representation.

A **list** keeps multiple values in order, including repeats:

```python
texts = ["ab", "ab", "ac"]
print(texts[0], texts[-1], len(texts))
print(texts[0][1])
```

The two output lines are `ab ac 3` and `b`. Index 0 means the first element; −1 means the last. The second line first chooses the first string, then its character at index 1. `len(texts)` counts list elements, not the combined letters. Index 3 would fail because a three-element list has indices 0, 1, 2. The two copies of `ab` are two observations; removing repeats would change Chapter 4's counts.

A **dictionary** associates keys with values: `{"a": 0, "b": 0, "c": 0}` gives a count for each named character. Unlike a list index, the key `"b"` names what we want directly. `counts["b"]` retrieves its value; `counts["b"] = 2` replaces it. This is why the loaded JSON object's `"train"` field can retrieve the list of strings.

## Repeat an operation without losing sentence boundaries

**Example P.2 — Count letters, then distinguish them from prediction events.**

```python
texts = ["ab", "ab", "ac"]
counts = {"a": 0, "b": 0, "c": 0}
for text in texts:
    for character in text:
        counts[character] = counts[character] + 1
print(counts)
```

The result is `{'a': 3, 'b': 2, 'c': 1}`. A **loop** repeats its indented body. The outer loop selects one string; the inner loop visits that string's characters. Python uses indentation to specify which statements belong to the loop. The final `print` is outside both loops and runs once.

These six letters are not yet Chapter 4's nine prediction events. Each of the three strings also predicts `EOS`, the end marker. Nor have we counted bigrams: those require knowing the preceding character and resetting it to `BOS` at each new string. The following fragment counts the targets following `a` only:

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

The output is `{'a': 0, 'b': 2, 'c': 1, 'EOS': 0}`. `list(text)` turns the string into a list of characters; adding `["EOS"]` appends one marker. `if` runs its indented body only when its condition is true. `==` compares values, unlike assignment `=`. `+= 1` adds one to the existing count. The final `previous = target` runs for every target, whether or not the condition was true. Moving `previous = "BOS"` outside the outer loop would incorrectly connect separate strings.

## Name reusable work and read failures

A **function** packages an operation with named inputs and an explicit output. `def` starts its definition; `return` sends the result back to the caller.

```python
def smoothed_probability(count, row_total, candidates, alpha):
    denominator = row_total + alpha * candidates
    if denominator == 0:
        raise ValueError("empty unsmoothed context")
    return (count + alpha) / denominator

print(smoothed_probability(2, 3, 4, 1))
```

This prints `0.42857142857142855`, the floating-point representation of $3/7$. The arguments mean observed count 2, row total 3, four possible targets, and one added count per target. The function does not look up the row or know which word is correct; its contract is just that arithmetic. The project's full implementation also checks order and vocabulary conditions.

When the denominator is zero, `raise` deliberately signals an **exception** instead of inventing a probability. A **traceback** shows the sequence of calls that led to an error. Read its final line for the error type and message, then find the last relevant line in your own code. An error from a library can originate in a bad shape or path you supplied.

**Table P.1 — Four failures and the first useful check.**

| Error | Typical cause here | First check |
| --- | --- | --- |
| `NameError: name 'texts' is not defined` | A setup cell has not run in this kernel | Restart and run from the first cell |
| `FileNotFoundError` | Relative path starts from a different working directory | Print the resolved path |
| `IndexError: list index out of range` | Index equals or exceeds the list length | Print the index and `len(...)` |
| `ModuleNotFoundError: No module named 'numpy'` | The selected Python environment lacks the package | Check which executable/kernel is in use |

You can handle an anticipated exception without hiding unrelated ones:

```python
try:
    smoothed_probability(0, 0, 4, 0)
except ValueError as error:
    print(str(error))
```

It prints `empty unsmoothed context`. This is an inspected failure, not a probability of zero. Catching every exception and returning 0 would mix missing data, coding mistakes and legitimate zero probabilities into one misleading result. Python's tutorial explains the general control-flow and exception rules; these counting examples are original. [Python tutorial](https://docs.python.org/3.12/tutorial/)

## Arrays add shape, storage type and an execution location

Ordinary lists preserve values but do not supply all the numerical operations we need. For example, `[1,2] * 2` repeats a list to `[1,2,1,2]`. A NumPy array instead supports numerical multiplication:

```python
import numpy as np

x = np.array([[2, 1], [1, -1]], dtype=np.float64)
w = np.array([[1, 0, -1], [0, 1, 1]], dtype=np.float64)
print(x.shape, (x @ w).tolist())
print((x * 2).tolist())
```

The first output is `(2, 2) [[2.0, 1.0, -1.0], [1.0, -1.0, -2.0]]`; the second is `[[4.0, 2.0], [2.0, -2.0]]`. Parentheses around the shape display a **tuple**, an ordered collection whose entries cannot be replaced in place. `@` performs Chapter 5's matrix multiplication; `*` multiplies entries here. `tolist()` makes the array contents easy to print.

A **dtype** specifies how each value is stored. `float64` uses 64 bits per floating-point value; it is a representation choice, not 64 decimal digits of accuracy. Integer IDs should remain integers. Converting an ID to a floating-point number does not turn it into an embedding.

PyTorch supplies tensor operations and records the dependencies needed for Chapter 7's gradients:

```python
import torch

ids = torch.tensor([0, 1], dtype=torch.long, device="cpu")
weights = torch.tensor([0.0, 0.0], dtype=torch.float64,
                       device="cpu", requires_grad=True)
print(tuple(ids.shape), weights.dtype, weights.device)
```

The result is `(2,) torch.float64 cpu`. **Device** identifies where computation and storage live; this practice explicitly uses the CPU. `torch.long` is the integer type used for lookup indices and class-index targets. `requires_grad=True` asks PyTorch to track operations involving the parameter so derivatives can be computed later. It neither trains the parameter immediately nor makes IDs differentiable. Inputs and parameters used together need compatible devices and dtypes. Converting one operand deliberately is a repair; repeatedly converting everything without knowing its role is not. [PyTorch tensor tutorial](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

## Return to MG-0, then the shape exercise

The first notebook imports `fit`, `sequence_probability` and `generate` from `code/part-ii/ngram.py`. `fit(texts, vocabulary, n=2, alpha=0)` names the order and smoothing explicitly. It resets each string boundary, uses $n-1$ preceding symbols, and includes `EOS` among the four targets. An unseen context with no smoothing has no defined distribution; a prefix that already has zero probability remains a zero-probability sequence.

**Table P.2 — The complete order/smoothing check, including EOS.** These expectations come from Chapter 4's fractions, independently of the Python implementation.

| Order $n$ | Added count $\alpha$ | $P(\texttt{ac})$ | $P(\texttt{aa})$ |
| --- | --- | --- | --- |
| 1 | 0 | $1/81$ | $1/27$ |
| 2 | 0 | $1/3$ | 0 |
| 3 | 0 | $1/3$ | 0 |
| 1 | 1 | $32/2197$ | $64/2197$ |
| 2 | 1 | $16/245$ | $4/343$ |
| 3 | 1 | $16/245$ | $1/49$ |

The bigram row after `a` is `[0,2,1,0]` in `a,b,c,EOS` order. With order 2, no smoothing, seed 42 and the book's fixed LCG32 generator, the successive draws are approximately 0.252345, 0.088125, 0.577281; the outputs are `a,b,EOS`. A seed alone is insufficient: the random algorithm and candidate order also matter. The existing `ac` diagnostic repeats a training string, so this table is not evidence of generalization.

After this reproduction, `02-shapes-and-loss.ipynb` begins with the Chapter 5 calculation. Its loss section is for use after Chapter 6. Run `03-training.ipynb` after Chapter 7. You can inspect the saved outputs first and then change a single declared condition. Preserve the original files or keep your variant separately so the reference run remains identifiable.

## Summary

Variables name values; lists preserve order and repetition; dictionaries associate names with values. Loops repeat indented work, conditions select branches, and functions expose a reusable input/output contract. Paths depend on a working directory, while notebook variables depend on a kernel's execution history. Arrays additionally declare axes, dtype and device. These details are part of an experiment's meaning, not incidental syntax.

## Exercises

1. Change the input list to `['ab','ac']`. What letter counts and bigram `a` row should appear? Explain why removing a duplicate changed a probability.
2. A notebook displays the expected output but fails with `NameError` after a kernel restart. What does the old output prove, and what needs to be repaired?
3. Someone uses `[1,2] * 2` when intending numerical scaling. Give its actual result and a NumPy repair. Which dtype would you choose for token IDs?
4. With an empty row, four candidates and $\alpha=1$, what does `smoothed_probability(0,0,4,1)` return? Contrast the no-smoothing case without confusing zero and undefined.

## Reference answers

1. Letter counts become `{'a':2,'b':1,'c':1}`. The `a` row becomes `[0,1,1,0]`; without smoothing $P(b\mid a)=1/2$, previously $2/3$. A duplicate was an additional training observation, not irrelevant formatting.
2. It records a past result from some execution state, possibly with earlier variables or different code. Restore the missing definition or correct cell order and run all cells in a new kernel. A screenshot or a saved result alone does not establish reproducibility.
3. The list repeats to `[1,2,1,2]`. `np.array([1,2]) * 2` gives numerical values `[2,4]`. IDs need an integer dtype, such as PyTorch's `torch.long` for embedding lookup; floating-point vectors belong to a different role.
4. The numerator is 1 and denominator is 4, so the result is $1/4$. With $\alpha=0$, both are zero and the function raises `ValueError`. That means this context has no estimated distribution; it is not an estimated probability of zero for one particular candidate.

## References

- [Python 3.12 tutorial](https://docs.python.org/3.12/tutorial/). Chapters 3–5 explain values, collections and control flow; chapters 7, 8 and 12 cover files, exceptions and environments. It provides the language rules behind the original exercises.
- [NumPy, `matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html). Specifies the matrix operation used after the counting notebook; the chapter teaches its numerical meaning before this syntax.
- [PyTorch, tensor tutorial](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html). Explains tensor attributes and numerical operations, including dtype and device. The companion files separately pin the versions actually run.
