# SPDX-License-Identifier: Apache-2.0
"""KA-5: deterministic graph with exactly one optional bounded model decision."""
from copy import deepcopy
from contracts import load, failure
from rag import run as prepare, compose
from source_skill import verify


def run(question, locale='en', choose=None, max_transitions=8, on_date='2026-09-14', topic='travel', documents=None):
    specification = load('ka5-workflow-v1.json')
    corpus = deepcopy(load('ka4-documents-v1.json')['documents'] if documents is None else documents)
    result = dict(version=specification['version'], state='START', events=[], model_calls=0,
                  decision=None, answer=None, producer='deterministic host; choice adapter recorded separately')
    def move(state, **detail):
        if len(result['events']) >= max_transitions:
            result.update(state='STOPPED', answer=failure('transition_budget'))
            return False
        if state not in specification['states'][result['state']]:
            raise ValueError('illegal_transition')
        result['events'].append(dict(sequence=len(result['events'])+1, previous=result['state'], state=state, **detail))
        result['state'] = state
        return True
    # KA-4 supplies retrieval/context; composing the actual answer is deferred.
    retrieval = prepare(question, locale=locale, on_date=on_date, topic=topic, documents=corpus,
                        generator=lambda *args: failure('deferred'))
    result['retrieval'] = retrieval
    context = retrieval['context']
    if not move('RETRIEVED', source_ids=[row['source_id'] for row in context['evidence']]): return result
    candidate = compose(context, corpus, locale, on_date, topic)
    report = verify(context, candidate, locale, on_date, topic, corpus)
    result['source_report'] = report
    if not report['supported']:
        result['answer'] = failure(candidate['reason_code'] or 'source_check_failed')
        move('ABSTAINED', reason=result['answer']['reason_code']); return result
    if not move('VERIFIED', source_report=report): return result
    if len(result['events']) >= max_transitions:
        result.update(state='STOPPED', answer=failure('transition_budget')); return result
    content = load('ka5-content-v1.json')['locales'][locale]
    decision_input = dict(instruction=content['choice_instruction'], question=question, evidence=context['evidence'],
                          candidate_order=specification['candidate_order'])
    result['decision_input'] = decision_input
    if choose is None:
        result.update(state='STOPPED', answer=failure('decision_adapter_required'))
        return result
    result['model_calls'] += 1
    try: choice = choose(decision_input)
    except TimeoutError:
        result['answer'] = failure('decision_timeout'); move('STOPPED', reason='decision_timeout'); return result
    result['decision'] = choice
    if choice not in specification['candidate_order']:
        result['answer'] = failure('invalid_decision'); move('STOPPED', reason='invalid_decision'); return result
    if not move('DECIDED', choice=choice): return result
    if choice == 'abstain':
        result['answer'] = failure('model_abstained'); move('ABSTAINED', reason='model_abstained'); return result
    result['answer'] = candidate
    if not move('COMPOSED', amount_yuan=candidate['amount_yuan']): return result
    # The support gate remains a host obligation even after a model selects evidence.
    final = verify(context, result['answer'], locale, on_date, topic, corpus)
    if not final['supported']:
        result['answer'] = failure('source_check_failed'); move('ABSTAINED'); return result
    move('ANSWERED', amount_yuan=result['answer']['amount_yuan'])
    return result
