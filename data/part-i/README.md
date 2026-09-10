# Part I fixture card

Version: `part-i-v1`. Created: 2026-09-08. Author: Brooklyn Yu / Understanding LLMs contributors. License: **CC BY-SA 4.0** for every JSON file here. All data is original synthetic teaching material, freely redistributable under that license. No private records, external datasets, model weights, or third-party output are included.

- `observations.json`: five bilingual groups, ten authored transcripts, exact inputs/outputs/configuration, evaluation expectations, failures, risks and controls. `model: null` is intentional. These are static teaching records, not an LLM measurement. G2's probability bins and draws are explicit; no random experiment is silently claimed.
- `journey.json`: six scenarios and a hand-specified answer table. θ-A/θ-B are teaching parameter versions. Switching versions does not train a model. The answer labels denote whole answers, not measured token probabilities.
- `tokenizer.json`: exact longest-match pieces and hand-assigned 2D rows for `toy-longest-v1/v2`. Entry 0 is reserved for unknown-code-point fallback. No normalization or automatically added boundary markers. Unknown text does not round-trip. v2 adds `cats` at ID 18. No real checkpoint is compatible with these invented IDs.
- `ngram.json`: character corpus, fixed prediction vocabulary, boundary policy, N/α options, held-out diagnostics, seed, PRNG and stopping limit. Each training record is counted separately, prefixed with N−1 BOS and suffixed with one EOS; BOS is never predicted. All nine target events are counted, including EOS.
- `expected.json`: independent hand-calculated expected IDs, counts, similarities, six held-out comparisons, six journey outputs, and the seed-42 unsmoothed Bigram trace. `null` means mathematically undefined, not zero.

The held-out `ac` intentionally duplicates a training string, while `aa` contains an unseen transition. These are diagnostic fixtures, **not an independent generalization test or benchmark**. Neither scoring nor generation changes training counts. Changing settings while inspecting this set is exploratory evaluation.

Reader dependencies: none beyond the static chapters. The complete inputs, intermediate calculations, and results are printed in the prose. Author verification uses the pure functions in `code/part-i/core.ts` with Node; no API, GPU, credential, model download, or CDN is required.

Numerical verification uses IEEE-754 doubles. Chapter tables show exact fractions where applicable and label rounded decimals. Seeds are unsigned 32-bit integers. LCG32 uses `Math.imul` for explicit overflow; default seed is 42, with at most 12 draws including EOS. EOS, undefined distribution, and length limit are distinct stops. There are no browser notes, reset operations, or exports.

## Chapter 1 case names and fixture IDs

The textbook uses descriptive case names instead of exposing the fixture IDs. Each pair's first record is the `-A` record and its second is the `-B` record. The localized chapters use equivalent case names. This presentation change does not alter inputs, outputs, criteria, or numerical data.

| Textbook case | Worked example | Group | Evaluation / failure / risk IDs |
| --- | --- | --- | --- |
| Factual completion | 1.1 | G1 | E-G1 / F-G1 / R-G1 |
| Open-ended completion | 1.2 | G2 | E-G2 / F-G2 / R-G2 |
| Clue substitution | 1.3 | G3 | E-G3 / F-G3 / R-G3 |
| Policy updates | 1.4 | G4 | E-G4 / F-G4 / R-G4 |
| Order queries | 1.5 | G5 | E-G5 / F-G5 / R-G5 |

## Chapter 2 scenario names and fixture IDs

The textbook uses descriptive scenario labels in Table 2.7. The underlying states and numerical outputs have not changed.

| Textbook scenario | Fixture ID |
| --- | --- |
| Initial state | `old` |
| File replaced | `file` |
| New document supplied | `context` |
| History saved | `saved` |
| History supplied | `selected` |
| Parameters replaced | `parameters` |

Run `pnpm test` to verify the independent expected results; authoring dependencies are locked in `pnpm-lock.yaml`. No Python or Notebook is a Part I reader prerequisite.
