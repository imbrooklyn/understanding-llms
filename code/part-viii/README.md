# Part VIII verification and experiment runners

This directory extends `code/knowledge-assistant/`. It does not fork the KA-0–KA-4 project. Core paths need CPU only, no model account, GPU, paid API or network service. Prerequisites: the Python Primer, HTTP Primer and the chapters' stated dependencies.

From the book repository root:

```sh
python3.12 -m venv /tmp/book-part-viii
/tmp/book-part-viii/bin/python -m pip install -r code/part-viii/requirements.txt
BOOK_PYTHON=/tmp/book-part-viii/bin/python pnpm test:part-viii:cpu
BOOK_PYTHON=/tmp/book-part-viii/bin/python pnpm notebooks:part-viii
pnpm validate:part-viii
```

For the exact recorded macOS environment, the installed versions are in the inherited `code/part-vii/requirements-tested.txt` and `data/part-viii/dependency-inventory.json`. `appnope` in that historical full freeze is macOS-specific; use direct requirements when preparing another platform and retain its own actual environment record. This task actually tested macOS CPU, not Linux.

`test_controls.py` checks observable state paths, call limits, approvals, tenant scope, expiry, effects after reopening, no-mutation replay, changed-byte rejection and identical adverse proposals on isolated state. `permission_records.py` gives a fresh database for each permission-matrix row. `run_records.py` refreshes deterministic observations and their hash manifest; it first checks the independently reviewed inventory. It does not refresh that inventory or rerun model probes. Re-running it intentionally updates execution timestamps. Do not use a new output as its own expected value.

The two notebooks execute the source helper, bounded workflow, durable recovery, permission matrix, layer diagnostics and governance/attack controls. Saved optional-model and OS records are analyzed as historical inputs, not represented as newly executed experiments. `run_notebooks.py` creates a fresh kernel for each notebook, executes every cell in order, rejects errors and records source/artifact digests.

Optional author commands `run_model_probes.py` and `run_human_calibration.py` require the exact pinned installed local Ollama model. `harvest_human.py` uses author-only pyarrow 20.0.0 to extract the pinned licensed human slice. None is required for core learning or validation. `run_sandbox.py` is an explicitly macOS-specific local probe, not a sandbox library. See `docs/part-viii-online.md` before repeating these experiments. No attack runner contacts a third-party destination or operates on real orders.

Source Skill entry: `code/knowledge-assistant/skills/source-verification/SKILL.md`. Its helper only validates supplied evidence and returns a report. The host decides activation and verifies reviewed bytes. Permissions come from the host, not Skill prose or an experimental metadata field.

Code is Apache-2.0. Original author documentation is CC BY-SA 4.0. Dataset and notebook licensing exceptions are recorded in `data/part-viii/README.md`.
