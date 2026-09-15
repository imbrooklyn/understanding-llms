# SPDX-License-Identifier: Apache-2.0
"""KA-2: explicit context serialization and independently enforced output schema."""
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
from typing import Optional

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / 'data/knowledge-assistant' / name).read_text())


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def eligible(document, on_date, topic):
    date.fromisoformat(on_date)
    return (document['topic'] == topic and document['valid_from'] <= on_date
            and (document['valid_until'] is None or on_date < document['valid_until']))


def passage(document, locale, start=1, end=None):
    lines = document['text'][locale].splitlines()
    end = len(lines) if end is None else end
    if not 1 <= start <= end <= len(lines):
        raise ValueError('invalid_line_range')
    return dict(source_id=document['source_id'], version=document['version'],
                line_start=start, line_end=end, quote='\n'.join(lines[start - 1:end]))


def pack(question, evidence, locale='en', window=None, reserve=None):
    contract = load('ka2-context-contract-v1.json')
    content = load('ka2-content-v1.json')['locales'][locale]
    window = contract['window_units'] if window is None else window
    reserve = contract['output_reserve'] if reserve is None else reserve
    if not 0 <= reserve <= window:
        raise ValueError('invalid_budget')
    payload = dict(template=contract['version'], instruction=content['instruction'],
                   example=content['example'], evidence=evidence, question=question)
    serialized = encode(payload)
    used = len(serialized)
    return dict(status='ready' if used + reserve <= window else 'context_budget',
                input_units=used, output_reserve=reserve, window_units=window,
                serialized=serialized, evidence=evidence)


def build_context(question, on_date, topic, locale='en', documents=None, **budget):
    documents = load('ka4-documents-v1.json')['documents'] if documents is None else documents
    selected = [d for d in documents if eligible(d, on_date, topic)]
    selected.sort(key=lambda d: d['source_id'])
    selected.sort(key=lambda d: d['valid_from'], reverse=True)
    return pack(question, [passage(d, locale) for d in selected], locale, **budget)


@dataclass(frozen=True)
class Answer:
    schema_version: str
    status: str
    answer: Optional[str]
    amount_yuan: Optional[int]
    citations: list
    reason_code: Optional[str]


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate_key')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('non_json_number')


def validate_output(raw):
    try:
        value = json.loads(raw, object_pairs_hook=no_duplicates, parse_constant=reject_constant)
    except (ValueError, TypeError) as exc:
        return dict(stage='parse', error=str(exc), value=None)
    schema = load('ka2-answer-schema-v1.json')
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(value), key=lambda e: str(list(e.path)))
    if errors:
        return dict(stage='schema', error=errors[0].message, value=None)
    for citation in value['citations']:
        if citation['line_end'] < citation['line_start']:
            return dict(stage='application', error='reversed_line_range', value=None)
        # JSON Schema integers are mathematical integers, including JSON 1.0.
        citation['line_start'] = int(citation['line_start'])
        citation['line_end'] = int(citation['line_end'])
    if value['amount_yuan'] is not None:
        value['amount_yuan'] = int(value['amount_yuan'])
    return dict(stage='accepted_structure', error=None, value=Answer(**value))


def failure(reason, status='abstained'):
    return dict(schema_version='ka-answer-v1', status=status, answer=None,
                amount_yuan=None, citations=[], reason_code=reason)


def provider_boundary(raw, stop_reason='end_turn'):
    if stop_reason == 'refusal':
        return failure('provider_refusal', 'refused')
    if stop_reason != 'end_turn':
        return failure('incomplete_response', 'error')
    checked = validate_output(raw)
    if checked['value'] is None:
        return failure('invalid_output', 'error')
    return checked['value'].__dict__
