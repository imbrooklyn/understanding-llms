# SPDX-License-Identifier: Apache-2.0
"""Deterministic source check; no network and no business writes."""
from pathlib import Path
import json
import sys

ASSISTANT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ASSISTANT))
from source_skill import verify

if __name__ == '__main__':
    try:
        request = json.load(sys.stdin)
        report = verify(**request)
    except (ValueError, KeyError, TypeError) as error:
        report = dict(schema_version='source-verification-report-v1', supported=False,
                      reason='invalid_request', error=type(error).__name__)
    print(json.dumps(report, ensure_ascii=False, allow_nan=False))
