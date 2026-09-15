# SPDX-License-Identifier: Apache-2.0
"""Fresh CPU kernel per Part VII notebook, with actual output and provenance."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT=Path(__file__).resolve().parents[2]


def run():
    records=[]
    with tempfile.TemporaryDirectory(prefix='book-vii-kernel-') as directory:
        root=Path(directory);kernel=root/'kernels/book-vii';kernel.mkdir(parents=True)
        (kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Book VII CPU','language':'python','env':{'IPYTHONDIR':str(root/'ipython')}}))
        specs=KernelSpecManager(kernel_dirs=[str(kernel.parent)])
        for path in sorted((ROOT/'notebooks/part-vii').glob('*.ipynb')):
            book=nbformat.read(path,as_version=4)
            source='\n'.join(c.source for c in book.cells if c.cell_type=='code')
            manager=KernelManager(kernel_name='book-vii',kernel_spec_manager=specs)
            started=time.perf_counter()
            try:
                NotebookClient(book,km=manager,timeout=120,allow_errors=False,resources={'metadata':{'path':str(ROOT)}}).execute()
            finally:
                if manager.has_kernel:manager.shutdown_kernel(now=True)
            nbformat.write(book,path)
            record=dict(notebook=str(path.relative_to(ROOT)),code_sha256=hashlib.sha256(source.encode()).hexdigest(),artifact_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),code_cells=sum(c.cell_type=='code' for c in book.cells),elapsed_seconds=round(time.perf_counter()-started,6),status='passed')
            records.append(record);print(json.dumps(record),flush=True)
    manifest=json.loads((ROOT/'data/part-vii/run-manifest.json').read_text())
    report=dict(recorded_at=datetime.now(timezone.utc).isoformat(),python=sys.version,condition='fresh CPU kernel per notebook; all cells in order; no allowed errors; actual loopback and subprocess tests; no external model',inputs_sha256=manifest['inputs_sha256'],executions=records)
    (ROOT/'data/part-vii/notebook-execution.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':run()
