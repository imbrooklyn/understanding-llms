# SPDX-License-Identifier: Apache-2.0
"""KA-7 layer attribution: keep adverse cases, denominators and raw intermediates."""
from copy import deepcopy
from contracts import load
from rag import run, compose
from baselines import run_locale, load_fixture


def evaluate():
    tasks=[dict(id='current',question='Beijing lodging',on_date='2026-09-14',topic='travel',wanted=750),
           dict(id='historical',question='Beijing lodging',on_date='2025-09-14',topic='travel',wanted=600),
           dict(id='approval',question='order approval',on_date='2026-09-14',topic='approval',wanted=None),
           dict(id='unknown',question='unknown lunar lodging',on_date='2026-09-14',topic='unknown',wanted='abstain')]
    rows=[]
    for variant in ['retrieval_variant','generation_variant']:
        for task in tasks:
            kwargs={k:task[k] for k in ['question','on_date','topic']}
            if variant=='retrieval_variant' and task['id']=='current':kwargs['documents']=[]
            if variant=='generation_variant' and task['id']=='historical':
                def faulty(*args):
                    value=compose(*args);value['amount_yuan']=750;return value
                kwargs['generator']=faulty
            trace=run(**kwargs)
            answer=trace['answer'];positive=task['wanted']!='abstain'
            retrieval_ok=bool(trace['retrieved']) if positive else not trace['retrieved']
            context_ok=bool(trace['context']['evidence']) if positive and retrieval_ok else None
            proposed=trace['proposed']
            generation_ok=proposed['status']=='answered' and proposed['amount_yuan']==task['wanted'] if positive and context_ok else None
            citation_ok=trace['validation']['support']['supported'] if positive and generation_ok else None
            success=(answer['status']=='answered' and answer['amount_yuan']==task['wanted']) if positive else answer['status']=='abstained'
            layer='retrieval' if not retrieval_ok else 'context' if context_ok is False else 'generation' if generation_ok is False else 'citation' if citation_ok is False else None
            rows.append(dict(variant=variant,task=task,checks=dict(retrieval=retrieval_ok,context=context_ok,generation=generation_ok,citation=citation_ok,end_to_end=success),first_failure=layer,trace=trace))
    fixture=load_fixture()
    return dict(version='ka7-system-eval-v1',provenance='Actual local deterministic paths with two explicitly injected faults; no population benchmark.',
                rows=rows,summaries={v:dict(passed=sum(r['checks']['end_to_end'] for r in rows if r['variant']==v),total=4) for v in ['retrieval_variant','generation_variant']},
                inherited={locale:run_locale(fixture,locale) for locale in ['en','zh-hans']})


def judge_report(model_run,human_run,human_cases):
    calls={row['id']:row for row in model_run['calls']}
    oracle=load('../part-viii/judge-cases-v1.json')['cases']
    verdicts=[]
    for locale in ['en','zh-hans']:
        for case in oracle:
            actual=calls['judge-'+locale+'-'+case['id']]['choice']
            verdicts.append(dict(locale=locale,id=case['id'],expected=case['oracle'],actual=actual,match=actual==case['oracle']))
    human_calls={row['id']:row for row in human_run['calls']}
    mapped=[]
    inverse={'A':'B','B':'A','tie':'tie','invalid':'invalid','truncated':'truncated'}
    for row in human_cases['cases']:
        qid=row['question_id'];reference={'model_a':'A','model_b':'B','tie':'tie'}[row['winner']]
        forward=human_calls[f'human-{qid}-forward']['result']
        swapped=inverse[human_calls[f'human-{qid}-swapped']['result']]
        decision=forward if forward==swapped else 'tie'
        mapped.append(dict(question_id=qid,source_row=row['source_row'],human=reference,forward=forward,swapped_mapped=swapped,consistent=forward==swapped,conservative=decision,agrees=decision==reference))
    own=[]
    for row in human_cases['cases']:
        qid=row['question_id'];first=human_calls[f'self-{qid}-forward']['result'];second=human_calls[f'self-{qid}-swapped']['result']
        own.append(dict(question_id=qid,forward=first,swapped=second,own_wins_both=first=='A' and second=='B',independent_human_quality_label=None))
    travel_labels=load('../part-viii/travel-human-labels-v1.json')['labels']
    travel_rows=[dict(**row,human=travel_labels[row['id']],human_match=row['actual']==travel_labels[row['id']]) for row in verdicts]
    return dict(travel_human_calibration=dict(rows=travel_rows,matched=sum(row['human_match'] for row in travel_rows),model_decisions=8,unique_human_cases=4,annotators=1,decision='retain_narrow_in_domain_evidence_only'),authored_oracle=dict(rows=verdicts,matched=sum(r['match'] for r in verdicts),total=len(verdicts)),
                human_calibration=dict(rows=mapped,agreed=sum(r['agrees'] for r in mapped),total=len(mapped),position_consistent=sum(r['consistent'] for r in mapped),decision='reject_as_automatic_release_judge'),
                self_comparison=dict(rows=own,own_wins_both=sum(r['own_wins_both'] for r in own),total=len(own),boundary='Exploratory own-answer preference only; new pairs lack independent human quality labels, so no causal self-bias conclusion.'))
