# SPDX-License-Identifier: Apache-2.0
"""Print every diagnostic result; --record also saves a provenance-stamped CPU run."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import platform
import sys
from core import ROOT, results

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--record', action='store_true')
args = parser.parse_args()
paths = ['code/part-iii/core.py', 'code/part-iii/run.py', 'code/part-ii/numerical.py',
         'data/part-iii/sequence-v1.json', 'data/part-iii/expected.json', 'data/part-ii/nnlm-data.json']
record = {'as_of': datetime.now(timezone.utc).isoformat(), 'last_verified': '2026-09-12',
          'python': sys.version.split()[0], 'platform': platform.platform(), 'device': 'CPU',
          'seed': None, 'dependencies': 'Python standard library only',
          'command': 'python3 code/part-iii/run.py' + (' --record' if args.record else ''),
          'status': 'executed deterministic authored diagnostics; no model fitting',
          'sha256': {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths},
          'results': results()}
output = json.dumps(record, ensure_ascii=False, indent=2) + '\n'
if args.record:
    (ROOT / 'data/part-iii/run.json').write_text(output)
print(output, end='')
