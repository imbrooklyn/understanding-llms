# Part IX: local service and operations evidence

Original code: Apache-2.0. Original documentation and notebook prose: CC BY-SA 4.0. See [the capstone handover](../../docs/part-ix-capstone.md), [runbook](../../docs/part-ix-runbook.md), [dated implementation note](../../docs/part-ix-online.md) and [data inventory](../../data/part-ix/README.md).

The implementation extends `../knowledge-assistant/`; this directory contains experiment clients, independently specified gates, behavioral tests and record/notebook runners. It does not contain a second assistant. `support.py` shares HTTP clients and the release-case evaluator between tests, records and notebooks. Expected outcomes are authored separately in `data/part-ix/expected-v1.json`.

## Reproduce on a CPU

Run from the book repository root. Python 3.12.10 on macOS arm64 was actually tested in a fresh virtual environment. `python3.12` must refer to an installed Python 3.12 interpreter; the system `python3` may be older. The service uses POSIX process-group termination. Windows is not supported by this implementation; Linux has not been validated in this increment. No GPU, model server, credentials or paid API is needed.

```sh
python3.12 -m venv /tmp/ka-part-ix-venv
/tmp/ka-part-ix-venv/bin/python -m pip install -r code/part-ix/requirements.txt
export BOOK_PYTHON=/tmp/ka-part-ix-venv/bin/python
pnpm test:part-ix:cpu
pnpm records:part-ix
pnpm notebooks:part-ix
pnpm validate:part-ix
```

Dependency installation needs package-index access; all subsequent core practice runs locally. For the exact measured macOS package set, install `requirements-tested.txt` instead. It includes platform-specific notebook dependencies and is not a cross-platform lock. The service itself uses the standard library plus the inherited `jsonschema` validation dependency. The notebook runner adds the pinned Jupyter packages inherited from Part VII and creates a fresh private kernel for each notebook.

`records:part-ix` regenerates current `data/part-ix/*-run.json`, candidate manifests, the run manifest and dependency inventory. It never overwrites earlier parts' results. Copy a current evidence bundle to a separately named directory before intentionally changing an implementation or fixture; retained initial defect records must not be replaced. Request IDs, ephemeral ports, wall-clock times, durations and byte hashes change across runs. Expected amounts, permission outcomes, retry bounds and logical-clock arithmetic must not.

The notebooks are executable and include visible explanations, exercises and answers. `01-service.ipynb` performs real loopback requests and cancellation. `02-operations.ipynb` runs the local gate and policy calculations, then explicitly reads the saved rollback record. Reading that record is not a fresh rollback or model invocation. The runner writes completed notebook outputs and `notebook-execution.json`; a notebook merely opening is not acceptance.

## Demonstrate

```sh
"$BOOK_PYTHON" code/knowledge-assistant/service.py --port 0
```

Open the exact loopback URL printed on the first line. The OS chooses an available port. Switch language using the ordinary navigation links. The fictional default question returns the dated source; try a historical date, `volcano`, own order `A-104`, Stop, clear/undo, handoff and categorized feedback. Stop affects a request, clear/undo affects the view, and neither cancels an order. Handoff prepares local text without sending a message. Ctrl-C stops only this service and its child workers.

The public demo keys `demo-north` and `demo-south` map to fictional host principals. They are test fixtures, not an identity provider. Do not expose this loopback server through a public proxy. The CLI has no fault, release, approval or arbitrary-tool HTTP endpoint. Controlled faults and candidate switches occur through the in-process operator object in `run_records.py`.

## Verification entries

- `pnpm test:part-ix:cpu`: observable HTTP, cancellation race, ownership, retry/deadline, release binding, cache/bucket/breaker boundaries, feedback and unchanged lexical outcomes.
- `pnpm validate:part-ix`: bilingual structure, independent numerical/evidence checks, input/output integrity, diagrams and executed notebooks.
- `BOOK_PREVIEW_URL=http://127.0.0.1:PORT pnpm test:browser`: all book suites plus Part IX static desktop/mobile/no-JavaScript coverage and the separately managed live service UI suite. The book preview must be started and owned by the caller.
- `pnpm ci:build`: all repository content/behavior checks, type checks, production build and draft-output audit. It does not publish anything.

Real sockets and child processes are required for the behavior and notebook runs. A sandbox refusal to bind is an environment failure, not a passing simulated test. No performance benchmark or new neural-model evaluation is implied by these commands.
