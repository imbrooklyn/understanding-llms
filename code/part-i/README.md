# Shared Part I mechanisms

Original source code, Apache-2.0. `core.ts` exports pure functions for author verification of the static textbook's tokenization, cosine, state comparisons, N-gram estimation, scoring, and generation. Data comes from `data/part-i`; its fixture card specifies provenance, normalization, random-state, and stopping conventions.

Readers receive the complete worked examples, result tables, and solutions in the chapters. No runtime or browser controls are required. The parameterized Python/Notebook implementation is deferred until after CH-05 and Primer-PY.

Maintainer checks: `pnpm test`, `pnpm ci:build`, and `pnpm test:browser` against a local development server. Expected numerical results are stored separately from the implementation. Public comments and documentation are English; localized strings belong to textbook content resources.
