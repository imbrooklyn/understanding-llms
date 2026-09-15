# SPDX-License-Identifier: Apache-2.0
"""KA-4 local extractive RAG path; not a neural generation experiment."""
from copy import deepcopy
import hashlib
import re
from contracts import load, eligible, passage, pack, failure, encode, validate_output
from baselines import load_fixture, tokens
from retrieval import bm25


def parse_documents(documents, locale):
    chunks = []
    for doc in documents:
        lines = doc['text'][locale].splitlines()
        offset = 0
        for number, line in enumerate(lines, 1):
            chunks.append(dict(chunk_id=f"{doc['source_id']}:L{number}", source_id=doc['source_id'],
                               version=doc['version'], line_start=number, line_end=number,
                               start_codepoint=offset, end_codepoint=offset+len(line), text=line,
                               parent_id=doc['source_id'], license=doc['license']))
            offset += len(line) + 1
    return chunks


def extract_amount(text):
    numbers = re.findall(r'(?<![0-9])(?:600|750|800)(?![0-9])', text)
    return int(numbers[-1]) if numbers else None


def citation_support(answer, documents, locale, on_date, topic):
    sources = {d['source_id']: d for d in documents}
    checks = []
    for item in answer['citations']:
        doc = sources.get(item['source_id'])
        exists = doc is not None
        exact = scope = complete = value = False
        if doc:
            try:
                exact = item == passage(doc, locale, item['line_start'], item['line_end'])
            except (ValueError, KeyError):
                pass
            scope = eligible(doc, on_date, topic)
            complete = item['line_start'] <= doc['support_range'][0] and item['line_end'] >= doc['support_range'][1]
            value = answer['amount_yuan'] == extract_amount(item['quote'])
        checks.append(dict(exists=exists, exact=exact, eligible=scope, complete_scope=complete, amount_matches=value,
                           supports=exists and exact and scope and complete and value))
    has_answer = answer['status'] == 'answered'
    expected_text = '\n'.join(item['quote'] + f" [{item['source_id']}:{item['line_start']}-{item['line_end']}]" for item in answer['citations'])
    text_matches = has_answer and answer['answer'] == expected_text
    return dict(citations=checks, text_matches_extractive_claim=text_matches,
                supported=has_answer and bool(checks) and all(c['supports'] for c in checks) and text_matches)


def compose(context, documents, locale, on_date, topic):
    """Exact-source composer with limited amount extraction, no learned parameters."""
    if context['status'] != 'ready':
        return failure('context_budget')
    if topic not in {'travel', 'approval'}:
        return failure('unsupported_task')
    evidence = context['evidence']
    sources = {d['source_id']: d for d in documents}
    valid = [item for item in evidence if item['source_id'] in sources and eligible(sources[item['source_id']], on_date, topic)
             and item == passage(sources[item['source_id']], locale, item['line_start'], item['line_end'])
             and item['line_start'] <= sources[item['source_id']]['support_range'][0]
             and item['line_end'] >= sources[item['source_id']]['support_range'][1]]
    if not valid or len(valid) != len(evidence):
        return failure('insufficient_evidence')
    amounts = {extract_amount(item['quote']) for item in valid}
    if len(amounts) > 1:
        return failure('conflicting_evidence')
    amount = next(iter(amounts))
    if topic == 'travel' and amount is None:
        return failure('insufficient_evidence')
    answer = '\n'.join(item['quote'] + f" [{item['source_id']}:{item['line_start']}-{item['line_end']}]" for item in valid)
    return dict(schema_version='ka-answer-v1', status='answered', answer=answer, amount_yuan=amount,
                citations=valid, reason_code=None)


def run(question, on_date='2026-09-14', topic='travel', locale='en', scope_filter=True,
        parent=True, window=1400, documents=None, generator=compose, fault=None, rewrite=False, compress=False):
    documents = deepcopy(documents if documents is not None else load('ka4-documents-v1.json')['documents'])
    fixture = load_fixture()
    chunks = parse_documents(documents, locale)
    cards = {d['id']: d['index_text'][locale] for d in fixture['documents']}
    candidates = [doc for doc in documents if not scope_filter or eligible(doc, on_date, topic)]
    all_indexed = [tokens(cards.get(doc['source_id'], doc.get('index_text', {}).get(locale, doc['text'][locale])), locale, fixture) for doc in documents]
    retrieval_query = question
    if rewrite:
        for original, replacement in load('ka4-retrieval-rules-v1.json')['rewrites'][locale].items():
            retrieval_query = retrieval_query.replace(original, replacement)
    all_scores = bm25(tokens(retrieval_query, locale, fixture), all_indexed)
    indexed = [all_indexed[documents.index(doc)] for doc in candidates]
    scores = [all_scores[documents.index(doc)] for doc in candidates]
    ranking = sorted(range(len(candidates)), key=lambda i: (-round(scores[i], 12), documents.index(candidates[i])))
    retrieved = [candidates[i] for i in ranking if scores[i] > 0][:1]
    # Expansion is explicit: all same-topic, same-authority, same-start siblings are checked.
    if retrieved:
        first = retrieved[0]
        retrieved += [d for d in candidates if d not in retrieved and d['topic'] == first['topic'] and d['authority'] == first['authority'] and d['valid_from'] == first['valid_from']]
    evidence = [passage(doc, locale, 1 if parent else len(doc['text'][locale].splitlines())) for doc in retrieved]
    if compress:
        evidence = [passage(doc, locale, *doc['support_range']) for doc in retrieved]
    if fault == 'context_drop':
        evidence = []
    context = pack(question, evidence, locale, window=window)
    proposed = generator(context, documents, locale, on_date, topic)
    if fault == 'wrong_amount' and proposed['status'] == 'answered':
        proposed['amount_yuan'] = 600
        proposed['answer'] = proposed['answer'].replace('750', '600')
    if fault == 'wrong_citation' and proposed['status'] == 'answered':
        old = next(d for d in documents if d['source_id'] == 'travel-v1')
        proposed['citations'] = [passage(old, locale)]
    structure = validate_output(encode(proposed))
    support = (citation_support(structure['value'].__dict__, documents, locale, on_date, topic)
               if structure['value'] is not None else
               dict(citations=[], text_matches_extractive_claim=False, supported=False))
    final = proposed
    if structure['value'] is None:
        final = failure('invalid_output', 'error')
    elif proposed['status'] == 'answered' and not support['supported']:
        final = failure('unsupported_claim')
    return dict(producer='local-extractive-v1; original deterministic Python, not an LLM or replay',
                question=question, retrieval_query=retrieval_query, on_date=on_date, topic=topic, locale=locale,
                parsed_chunks=chunks, index=[dict(source_id=d['source_id'], chunk_id=d['source_id']+':card', parent_id=d['source_id'], representation='authored KA-0 card; not a citation quote', terms=t, score=s) for d,t,s in zip(candidates,indexed,scores)],
                ranked=[dict(source_id=candidates[i]['source_id'],score=scores[i]) for i in ranking],
                retrieved=[d['source_id'] for d in retrieved], context=context, proposed=proposed,
                validation=dict(structure=structure['stage'], support=support), answer=final,
                model_parameter_updates=0,
                corpus_sha256=hashlib.sha256(encode(documents).encode()).hexdigest())
