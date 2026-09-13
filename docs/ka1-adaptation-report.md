# KA-1 runtime adaptation decision

As of / last verified: 2026-09-13. Status: completed local development comparison; both assistant candidates rejected. This is the Part VI increment to [the existing selection report](ka1-selection-report.md), not a second knowledge assistant.

## Decision and evidence

Retain the terminal-period normalizer as a narrow teaching diagnostic. It improves selected-checkpoint English literal matching from 0/18 to 6/18, while semantic passes remain 6/18 and robust semantic cases remain 2/6. Chinese remains 0/18. No original assistant gate passes. Do not infer that a shorter displayed response improved model capability or saved generation.

The next justified investigation is a paired input/template and current-versus-historical scope audit. It requires a new development input version, since the present prompts are frozen. Additional source freshness and live order access need separately evaluated retrieval/tool components in their assigned later chapters. Expensive parameter training on six already-inspected questions is not supported.

## Frozen contract and execution

The extension is `data/knowledge-assistant/ka1-format-adaptation-v1.json`. Its freeze, `ka1-format-freeze-v1.json`, occurred at `2026-09-13T12:23:33.409374+00:00`; `ka1-format-run-v1.json` was recorded at `2026-09-13T12:23:36.621417+00:00`. Hashes bind the previous contract, cases, checkpoints, tokenizer, original run and adjudication, shared code, new runner and pinned dependencies. Prior KA-1 failures were inspected before choosing this intervention: this is development evidence, not a blind test.

The sole intervention applies to the three amount tasks. If valid UTF-8 text, after surrounding whitespace removal, consists entirely of ASCII digits plus one period, return precisely those digits. Otherwise retain the decoded response. No answer extraction from prose, factual substitution, prompt edit, parameter update or judge relaxation occurs. Task scope is known from the contract, never inferred from the expected answer.

The experiment generated all 144 candidate/case/language/policy/seed combinations locally. Each actual generation supplies both raw and normalized conditions. It preserves six cases, two languages, selected step 50 and final step 600, greedy and temperature-0.7/top-5 policies, seeds 7/42/31415, 24 new tokens, 64 context positions and the original rubric/gates. Greedy repeats probe timing and repeatability; the denominator remains six distinct cases.

Python 3.12.10 / PyTorch 2.7.0 / one CPU thread / float64 / arm64 macOS 26.5.2. Models were warmed. Generation timing includes full-prefix recomputation, traces and byte decoding, and excludes loading. Normalization is timed immediately afterward; total adapted time is the sum. No GPU, paid API, downloaded external model or real order operation was used.

## Results and retained failures

| Primary greedy group | Strict raw → normalized | Semantic raw → normalized | Robust cases raw → normalized | Changed displays | Raw → normalized p95 ms | Generated tokens, including EOS |
| --- | --- | --- | --- | --- | --- | --- |
| Selected 50 / English | 0/18 → 6/18 | 6/18 → 6/18 | 2/6 → 2/6 | 9 | 0.982250 → 0.982542 | 66 |
| Selected 50 / Chinese | 0/18 → 0/18 | 0/18 → 0/18 | 0/6 → 0/6 | 0 | 2.185542 → 2.186292 | 114 |
| Final 600 / English | 0/18 → 0/18 | 0/18 → 0/18 | 0/6 → 0/6 | 0 | 5.020875 → 5.021208 | 207 |
| Final 600 / Chinese | 0/18 → 0/18 | 0/18 → 0/18 | 0/6 → 0/6 | 0 | 5.186250 → 5.186958 | 156 |

p95 uses nearest rank: rank ceil(0.95 × 18) = 18. Generated-token counts are identical across conditions because no model output is regenerated or removed from its computation trace. They are not fixture-lexer tokens from Chapter 37.

Selected English responds `750.` on current, stale-premise and historical tasks. All nine displays change, but the three historical responses retain the wrong digits. Status `blue.`, approval `France.` and unknown `new.` remain failures. Chinese fragments remain unchanged. Chapter 38 shows every selected primary response directly; both checkpoints' complete primary and stress responses remain in the existing and new JSON records.

Under the retained stress policy, selected English changes three responses, gains one strict pass (0/18 → 1/18), preserves one semantic pass and zero robust cases. The current response at seed 42 improves literal matching; historical responses at seeds 42 and 31415 remain wrong. Every other stress group has zero semantic passes. Invalid UTF-8 is preserved and cannot become a strict success.

Every raw completion, byte sequence, token trace and probability exactly reproduced its retained counterpart. Only then were the original disclosed AI-assisted author semantic judgments transferred. Deleting an amount's terminal period preserves all digits and scope, so the semantic scores stay fixed. This is not a new human panel, learned evaluator or judge API. Tensor equality before and after all calls confirms no parameter update.

The same nine KA-0 queries were also rerun: Keyword 5/9, BoW Count 6/9 and TF-IDF 7/9, separately in both languages. TF-IDF still misses the synonym request and selects the archived source for the stale-premise request. Source selection and generated-answer acceptance have separate denominators and are never pooled.

## Intervention choices

| Layer / proposal | Supporting evidence | Cost and next falsifying test | Veto or limitation |
| --- | --- | --- | --- |
| Input / prompt | Both policy versions are supplied but scope is mishandled | Inspect serialized inputs, then paired scope prompts; account for context tokens | Does not supply absent facts or permissions; the 64-position context is small |
| External evidence / RAG | KA-0 has retrieval failures; changing facts need versioned sources | Retain all nine queries; test source version and delivery, then generated use | KA-1 already receives its amounts; repeated retrieval alone does not establish a fix |
| Callable program / tool | A real status requires a query; exact arithmetic admits a program | Specify result, failure and access contracts in later chapters | No live query or cancellation interface is implemented; query permission is not cancellation permission |
| Domain parameters / continued pretraining | Tiny predominantly English training mix differs from bilingual target | Curate a licensed corpus, isolate domain exposure and retain other capabilities | Language, capacity, architecture, optimization and prompting are confounded; no demonstrated cost justification here |
| Behavioral parameters / SFT or preference training | Scope, abstention and approval responses fail with relevant information supplied | Representative reviewed data, independent families, training and retention comparisons | Training on the six inspected answers risks memorization; preference cannot certify facts or authorization |
| Runtime format / computation | Actual literal mismatch; a pool can contain useful alternatives | Measured wrapper overhead or charged generation/check budgets | Format repair has no semantic gain; extra computation requires useful candidates and a trusted acceptance rule |

Combinations are legitimate when each component has a stated hypothesis and can be ablated. No ordering implies that one method supersedes another. The completed result is a negative assistant selection with a positive narrow format diagnosis.

## Reproduction and limits

From the book root, in the declared CPU environment:

```sh
python code/knowledge-assistant/format_adaptation.py
python -m unittest discover -s code/part-vi -p 'test_*.py' -v
python code/part-vi/run_notebooks.py
```

Ordinary reproduction does not overwrite the recorded run or freeze. The test and second notebook re-generate all 144 attempts and compare observable outputs with the retained record. Timing is measured again and is expected to vary.

No SFT, continued pretraining, preference optimization, LoRA or QLoRA training benchmark has been performed. The Chapter 39 matrix calculation is explicitly author-assigned. No parameter-efficiency or new-task generalization claim follows from this comparison. Subsequent tuning must preserve the six cases as regression evidence and create unused acceptance families.

All amounts/accounts are fictional. Original fixture/weight content follows the existing CC BY-SA 4.0 records; new code is Apache-2.0. No third-party model license is silently inherited by a hypothetical adapter. See the Part VI data/code cards and [research ledger](part-vi-research.md).

