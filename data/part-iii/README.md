# Part III fixed sequence evidence

As of / last verified: 2026-09-12. Original data and mathematical constructions: CC BY-SA 4.0. No third-party corpus, model weights, tokenizer, account, order, or API response is distributed. `sequence-v1.json` is an explicit content resource, including the small source-language token vocabulary used by both language editions.

- `sequence-v1.json`: complete supplied RNN and encoder weights; input/output candidate orders; deterministic first-candidate tie rule; reset boundaries; scalar gradient objective; supplied gate activations; conditional decoder rows; target shift and EOS/cap rules; supplied query probes; frozen-memory and re-encoded-source intervention definitions.
- `expected.json`: independent exact expectations frozen before implementation. Halving uses fractions; the scalar loss is checked as `(w² − 1)² / 2`; attention uses `exp(ln(2)) = 2`. Coefficients of ln(2) remain exact mathematical values; JSON stores their binary64 approximations when a fraction has no finite binary representation.
- `run.json`: an actual standard-library CPU execution, with versions and input/code hashes. This is a reproduction of authored rules, not a training or performance log.
- `notebook-execution.json`: written only after every notebook executes successfully in a fresh kernel; includes code and imported-input hashes. Notebook outputs are retained in the notebooks.
- `environment.txt`: actual package freeze from the isolated Python 3.12 CPU environment, with direct dependencies pinned in `code/part-iii/requirements.txt`.
- `content-contract.json`: explicit bilingual heading labels and fixed numerical evidence required by the content/browser checks; learning strings belong here and in chapter/figure resources, not implementation comments.

## Comparability and units

The long color task is read from `data/part-ii/nnlm-data.json`, field `window_collision`, and checked against the source hash. Vocabulary IDs, two nine-token prefixes, target IDs, and the two-token window are unchanged. The diagnostic feedforward baseline and RNN use the same embeddings, final-position color criterion, candidate order, and output head. They are not the trained Part II NNLM. No fitting occurs, so there is no new train/validation/test split or random seed; the fixed paired diagnostic is not a sampled accuracy estimate. Short cases are an additional versioned distance probe, not a replacement for the long failure.

The translation encoder is a separate supplied ReLU network. Its states are computed. The decoder probability table is an authored conditional lookup at a fixed context; no complete learned recurrent decoder is claimed. Attention queries and gate activations are supplied. Attention scores are unscaled dot products throughout; no projection or scaling is silently introduced. The same-state and recomputed-source deletion results hold the query and readout fixed and do not represent a free-generation intervention.

Coordinates, logits, local sensitivities, and gates are dimensionless. Loss uses natural logarithms (nats; mean divided by the explicitly scored target count). Time indices count input or output positions, not seconds. Distance counts dependency edges. Float64 logical-storage estimates assume eight bytes per scalar and exclude containers, parameters, and training intermediates. The gradient table is a calculated power table, not an observed training curve.

Compute at full binary64 precision; round displayed probabilities and ordinary approximate values to six decimals. Exact fractions take precedence over printed decimals. No sampling occurs, so seed is null. Retain v1 when upgrading examples and document changed conditions instead of replacing unfavorable cases.

## Reproduction

From the book root, `python3 code/part-iii/run.py` prints all states, predictions, target timelines, gradients, and interventions without writing files. `--record` also replaces the run evidence after successful calculation. `pnpm validate:part-iii` checks bilingual content, recorded evidence, and independent numerical/behavioral invariants. Notebook and clean-environment commands are in `code/part-iii/README.md`.

The existing knowledge-assistant project remains in `code/knowledge-assistant` and `data/knowledge-assistant`. Its KA-0 Keyword, BoW Count, and TF-IDF comparisons are preserved; this part adds sequence diagnostics, not a second assistant or an unmeasured retrieval claim.
