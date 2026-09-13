# SPDX-License-Identifier: Apache-2.0
"""Execute Part VI notebooks in fresh CPU kernels without changing older runners."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    paths = sorted((ROOT / 'notebooks/part-vi').glob('*.ipynb'))
    if not paths:
        raise ValueError('no Part VI notebooks')
    records = []
    with tempfile.TemporaryDirectory(prefix='book-part-vi-notebooks-') as directory:
        temporary = Path(directory)
        kernel = temporary / 'kernels/part-vi'
        kernel.mkdir(parents=True)
        (kernel / 'kernel.json').write_text(json.dumps({
            'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            'display_name': 'Part VI CPU', 'language': 'python',
            'env': {'IPYTHONDIR': str(temporary / 'ipython'), 'MPLBACKEND': 'Agg'}}))
        specifications = KernelSpecManager(kernel_dirs=[str(kernel.parent)])
        for path in paths:
            notebook = nbformat.read(path, as_version=4)
            source = '\n'.join(cell.source for cell in notebook.cells if cell.cell_type == 'code')
            manager = KernelManager(kernel_name='part-vi', kernel_spec_manager=specifications)
            started = time.perf_counter()
            client = NotebookClient(notebook, km=manager, timeout=180, allow_errors=False,
                                    resources={'metadata': {'path': str(ROOT)}})
            try:
                client.execute()
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
            nbformat.write(notebook, path)
            record = dict(notebook=str(path.relative_to(ROOT)),
                          code_sha256=hashlib.sha256(source.encode()).hexdigest(),
                          artifact_sha256=digest(path),
                          code_cells=sum(cell.cell_type == 'code' for cell in notebook.cells),
                          elapsed_seconds=round(time.perf_counter() - started, 6), status='passed')
            records.append(record)
            print(json.dumps(record), flush=True)
    mechanism = json.loads((ROOT / 'data/part-vi/mechanism-run-v1.json').read_text())
    frozen = json.loads((ROOT / 'data/knowledge-assistant/ka1-format-freeze-v1.json').read_text())
    dependencies = set(mechanism['source_sha256']) | set(frozen['inputs_sha256'])
    dependencies.update(['code/part-vi/run_notebooks.py', 'data/part-vi/mechanism-run-v1.json',
                         'data/knowledge-assistant/ka1-format-run-v1.json'])
    result = dict(as_of=datetime.now(timezone.utc).isoformat(), python=sys.version.split()[0],
                  condition='fresh kernel per notebook; CPU; no allowed errors; all cells executed in order',
                  inputs_sha256={name: digest(ROOT / name) for name in sorted(dependencies)},
                  executions=records)
    (ROOT / 'data/part-vi/notebook-execution.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    run()

