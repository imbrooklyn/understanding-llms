# SPDX-License-Identifier: Apache-2.0
"""Paired diagnostic evaluation with retained faults and exact case-bootstrap mass."""
from collections import Counter
from copy import deepcopy
import math
from contracts import load
from rag import run


def corpus_for(case):
    docs = load('ka4-documents-v1.json')['documents']
    if case['corpus_variant'] == 'old_only':
        docs = [d for d in docs if d['source_id'] != 'travel-v2']
    if case['corpus_variant'] == 'conflict':
        extra = deepcopy(next(d for d in docs if d['source_id'] == 'travel-v2'))
        extra.update(source_id='travel-conflict-v1', candidate_id='F', version='conflict-v1', source_uri='book://travel-conflict-v1')
        extra['text'] = {locale: text.replace('750', '800') for locale, text in extra['text'].items()}
        extra['index_text'] = load('ka0-v1.json')['documents'][1]['index_text']
        docs.append(extra)
    return docs


def assess(case, trace):
    required = set(case['required_sources'])
    retrieved = set(trace['retrieved'])
    packed = {c['source_id'] for c in trace['context']['evidence']} if trace['context']['status'] == 'ready' else set()
    answer = trace['answer']
    retrieval = len(required & retrieved)/len(required) if required else None
    context = len(required & packed)/len(required) if required else None
    generation = trace['proposed']['status'] == case['expected_status'] and trace['proposed']['amount_yuan'] == case['expected_amount']
    cited = trace['validation']['support']['citations']
    citation_precision = sum(c['supports'] for c in cited)/len(cited) if cited else None
    end = answer['status'] == case['expected_status'] and answer['amount_yuan'] == case['expected_amount']
    if answer['status'] == 'answered':
        end = end and trace['validation']['support']['supported']
    if end:
        category = 'passed'
    elif required and retrieval < 1:
        category = 'retrieval'
    elif required and context < 1:
        category = 'context'
    elif not generation:
        category = 'generation'
    else:
        category = 'citation'
    return dict(retrieval_recall=retrieval, context_coverage=context, generation_task_pass=generation,
                citation_precision=citation_precision, answer_supported=trace['validation']['support']['supported'],
                end_to_end=end, first_failure=category)


def exact_bootstrap_interval(differences):
    """Enumerate integer sum probabilities by convolution, not random model trials."""
    counts = Counter(differences)
    n = len(differences)
    distribution = {0: 1.0}
    for _ in range(n):
        updated = Counter()
        for total, mass in distribution.items():
            for value, count in counts.items():
                updated[total + value] += mass * count/n
        distribution = updated
    def quantile(p):
        cumulative = 0
        for total, mass in sorted(distribution.items()):
            cumulative += mass
            if cumulative >= p:
                return total/n
        return max(distribution)/n
    return [quantile(.025), quantile(.975)]


def evaluate():
    contract = load('ka4-eval-v1.json')
    rows = []
    for case in contract['cases']:
        for locale in ['en', 'zh-hans']:
            for condition, options in contract['conditions'].items():
                for repetition in range(contract['repeats']):
                    trace = run(case['question'][locale], on_date=case['on_date'], topic=case['topic'], locale=locale,
                                documents=corpus_for(case), fault=case['fault'], window=250 if case['fault']=='budget' else 1400, **options)
                    rows.append(dict(case_id=case['id'], locale=locale, condition=condition, repetition=repetition+1,
                                     metrics=assess(case, trace), trace=trace))
    unique = [r for r in rows if r['locale']=='en' and r['repetition']==1]
    summaries = {}
    for condition in contract['conditions']:
        sample = [r for r in unique if r['condition']==condition]
        def mean(name):
            values = [r['metrics'][name] for r in sample if r['metrics'][name] is not None]
            return dict(numerator=sum(values), denominator=len(values), mean=sum(values)/len(values) if values else None)
        summaries[condition] = dict(end_to_end=mean('end_to_end'), retrieval=mean('retrieval_recall'), context=mean('context_coverage'),
                                    generation=mean('generation_task_pass'), citation_precision=mean('citation_precision'),
                                    failures=dict(Counter(r['metrics']['first_failure'] for r in sample)))
    paired = []
    for case in contract['cases']:
        pair = {r['condition']:r['metrics']['end_to_end'] for r in unique if r['case_id']==case['id']}
        paired.append(int(pair['filtered'])-int(pair['baseline']))
    return dict(version='ka4-eval-run-v1',producer='actual deterministic CPU pipeline; fault proposals authored and injected; no model sampling',
                rows=rows, summaries=summaries, confidence=dict(unit='one semantic case; translations and three repeats clustered, not independent samples',
                n=len(paired), paired_differences=paired, delta=sum(paired)/len(paired), percentile95=exact_bootstrap_interval(paired),
                method='exact nonparametric paired case bootstrap by probability convolution',
                limitation='conditional resampling of 12 authored development cases; not deployment confidence or held-out generalization'))


if __name__ == '__main__':
    import json
    value = evaluate()
    print(json.dumps({k:v for k,v in value.items() if k!='rows'},indent=2))


def ablations():
    """Separate diagnostic probes, never folded into the primary paired score."""
    results = []
    for locale, question in [('en', 'hotel allowance'), ('zh-hans', load('ka4-eval-v1.json')['cases'][3]['question']['zh-hans'])]:
        for rewrite in [False, True]:
            trace = run(question, locale=locale, rewrite=rewrite)
            results.append(dict(probe='synonym_rewrite', locale=locale, changed=rewrite, trace=trace))
    for parent in [False, True]:
        results.append(dict(probe='parent_expansion', changed=parent, trace=run('Beijing lodging', parent=parent)))
    docs = load('ka4-documents-v1.json')['documents']
    note = 'Administrative filing note. ' * 20
    for doc in docs:
        if doc['source_id'] == 'travel-v2':
            doc['text'] = {locale:text+'\n'+note for locale,text in doc['text'].items()}
    for compress in [False, True]:
        results.append(dict(probe='exact_line_compression', changed=compress, trace=run('Beijing lodging', documents=docs, compress=compress)))
    return dict(provenance='Authored changed-condition probes; filing note is synthetic irrelevant text, not added to the fixed core corpus.',results=results)
