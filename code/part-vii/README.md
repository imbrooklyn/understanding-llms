# Part VII CPU practice

KA-2, KA-3 and KA-4 extend [the continuing knowledge assistant](../knowledge-assistant/README.md). Original code is Apache-2.0. This directory contains validation and execution runners, not another independent assistant. The core uses Python 3.12, CPU, local files, an OS-assigned loopback HTTP port and an actual MCP child process. There is no GPU, paid API, model login or write operation. The generator is a deterministic exact-source composer, not an LLM. Authored proposals/faults are labeled in every retained experiment.

From the book root, create a fresh environment (choose a writable path):

```sh
python3.12 -m venv /tmp/book-vii-venv
/tmp/book-vii-venv/bin/python -m pip install -r code/part-vii/requirements-tested.txt
export BOOK_PYTHON=/tmp/book-vii-venv/bin/python
pnpm test:part-vii:cpu
```

`requirements.txt` pins direct dependencies; `requirements-tested.txt` records the complete actually installed environment. The tested host is documented in the validation record. Platform-specific transitive dependencies may need a newly recorded lock on other operating systems. Python 3.9 is not the declared environment.

For build validation alone, `requirements-ci.txt` pins just the schema validator and its runtime dependencies from that environment. The book CI and the main site's book-build step install this subset with Python 3.12.10 before `pnpm ci:build`. Notebook execution still requires the full practice environment. Workflow edits do not run or authorize a release.

To reproduce records and execute every Notebook cell in fresh kernels:

```sh
"$BOOK_PYTHON" code/part-vii/run_records.py
pnpm notebooks:part-vii
pnpm validate:part-vii
pnpm ci:build
```

Record reproduction overwrites only new `data/part-vii/` execution records and new Part VII Notebook outputs. Never run inherited scripts in write mode merely to reproduce their baselines. The inherited freeze verifies their byte identity. KA-1's original model experiments and evaluators are retained; no accepted general generator is claimed.

The HTTP notebook cells require the HTTP Primer. `http_scaffold.py` creates and closes its own loopback server; it never binds a public address. The fixed credential is a public demonstration placeholder, not a real API key. Saved records redact credential fields. The MCP subset pins 2026-07-28 and implements discovery/list/read over stdio; it is not a complete production server or a remote OAuth integration. See [the dated online layer](../../docs/part-vii-online.md).

For browser verification, start an owned `pnpm dev --host 127.0.0.1 --port PORT`, read the actual listening URL, set `BOOK_PREVIEW_URL` to it, and run `pnpm test:browser`. Part VII tests run both configured viewports, languages and themes, and a no-JavaScript reading path. Production `ci:build` verifies that these drafts are excluded from routes, search, RSS, sitemap and public navigation.
