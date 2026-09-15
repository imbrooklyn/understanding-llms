# SPDX-License-Identifier: Apache-2.0
"""Explicit one-Skill host integration, reusing the KA-4 support contract."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from contracts import load, encode, validate_output
from rag import citation_support

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).parent / 'skills/source-verification'


def verify(context, answer, locale='en', on_date='2026-09-14', topic='travel', documents=None):
    documents = load('ka4-documents-v1.json')['documents'] if documents is None else documents
    sources = {row['source_id']: row for row in documents}
    structured = validate_output(encode(answer))['value'] is not None
    checks = citation_support(answer, documents, locale, on_date, topic) if structured else None
    evidence = context.get('evidence', [])
    authority = bool(evidence) and all(sources.get(row.get('source_id'), {}).get('authority') == 'fictional-policy-office' for row in evidence)
    matches = evidence == answer.get('citations')
    ok = bool(structured and checks['supported'] and authority and matches and context['status'] == 'ready')
    return dict(schema_version='source-verification-report-v1', supported=ok, authority_ok=authority,
                context_matches=matches, reason='supported' if ok else 'source_check_failed', checks=checks)


def load_trace(request, expected_hashes=None, package=PACKAGE):
    """The caller selects this package; selection is not an additional model choice."""
    trace = []
    files = ['SKILL.md', 'references/evidence-contract.md', 'scripts/verify.py', 'assets/report-template.json']
    if expected_hashes is not None:
        for name in files:
            path = package / name
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hashes[name]:
                raise ValueError('package_integrity')
    text = (package / 'SKILL.md').read_text()
    header = text.split('---', 2)[1]
    metadata = {line.split(':', 1)[0]: line.split(':', 1)[1].strip() for line in header.splitlines() if line.startswith(('name:', 'description:'))}
    trace.append(dict(stage='discover', loaded_fields=metadata, utf8_bytes=len(encode(metadata).encode())))
    trace.append(dict(stage='activate', path='SKILL.md', utf8_bytes=len(text.encode())))
    reference = (package / files[1]).read_bytes()
    trace.append(dict(stage='reference', path=files[1], utf8_bytes=len(reference)))
    result = subprocess.run([sys.executable, str(package / files[2])], input=encode(request), text=True,
                            capture_output=True, timeout=2, check=True)
    report = json.loads(result.stdout)
    trace.append(dict(stage='execute', path=files[2], returncode=result.returncode, report=report))
    template = json.loads((package / files[3]).read_text())
    template.update(report)
    trace.append(dict(stage='report', path=files[3], report=template))
    return trace
