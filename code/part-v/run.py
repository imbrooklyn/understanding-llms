# SPDX-License-Identifier: Apache-2.0
"""Recompute assigned examples without modifying independent expectations."""
import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
import math
from pathlib import Path
import platform
import re
from mechanisms import (distribution, draw_index, rotate_quarter, rmsnorm, swiglu,
                        kv_bytes, latency, quantize, weighted_gradient, speculative_correction,
                        row_matmul, linear_prefix, rescue, two_step_beam, confusion)

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def pipeline(fixture):
    validation = {row['text'] for row in load('data/mini-gpt/corpus.json')['validation']}
    seen, ledger, retained = {}, [], []
    for row in fixture['records']:
        raw = row['html']
        if not raw.startswith('<p>') or not raw.endswith('</p>') or '<' in raw[3:-4]:
            raise ValueError('teaching parser requires one plain p element')
        text = html.unescape(raw[3:-4])
        ratio = sum(c.isdecimal() for c in text) / len(text) if text else 0
        bad_filter = ratio >= fixture['rules']['bad_digit_ratio'] or text == fixture['rules']['boilerplate_exact']
        reason, duplicate_of = 'retained', None
        if text == fixture['rules']['boilerplate_exact']:
            reason = 'boilerplate'
        elif text in seen:
            reason, duplicate_of = 'exact_duplicate', seen[text]
        else:
            seen[text] = row['id']
        redacted = re.sub(fixture['rules']['redaction_pattern'], fixture['rules']['replacement'], text)
        if reason == 'retained' and text in validation:
            reason = 'evaluation_overlap'
        if reason == 'retained':
            retained.append(dict(id=row['id'], text=redacted, locale=row['locale']))
        ledger.append(dict(id=row['id'], parsed=text, code_points=len(text), digit_fraction=ratio,
                           bad_filter_rejects=bad_filter, revised_result=reason,
                           duplicate_of=duplicate_of, redacted=redacted))
    after_filter = sum(row['revised_result'] != 'boilerplate' for row in ledger)
    after_dedup = sum(row['revised_result'] not in {'boilerplate', 'exact_duplicate'} for row in ledger)
    return dict(ledger=ledger, retained=retained,
                stage_counts=[len(ledger), after_filter, after_dedup, after_dedup, len(retained)])


def run():
    d = load('data/part-v/mechanisms.json')
    c, a, t = d['components'], d['architectures'], d['training']
    logits = [math.log(x) for x in d['sampling']['masses']]
    policies = [('greedy',dict(temperature=0)), ('temperature-1',{}),
                ('temperature-2',dict(temperature=2)), ('top-k-2',dict(top_k=2)),
                *[(f'top-p-{p}',dict(top_p=p)) for p in d['sampling']['top_p']]]
    sampling = [dict(policy=name, probabilities=(probs:=distribution(logits,**kw)),
                     selections=[draw_index(probs,u) for u in d['sampling']['draws']]) for name, kw in policies]
    states = [t['parameters'] * t[key] for key in ['weight_bytes','gradient_bytes','master_bytes']]
    states.append(2*t['parameters']*t['moment_bytes_each'])
    activations = math.prod(t[key] for key in ['batch','tokens','width','layers','saved_arrays_per_layer','activation_bytes'])
    clean, corrupt = d['intervention']['clean'], d['intervention']['corrupt']
    hidden = [clean,corrupt,[clean[0],corrupt[1]],[corrupt[0],clean[1]],
              [corrupt[0],clean[1]],[clean[0],corrupt[1]]]
    intervention = [dict(hidden=x, logits=(z:=row_matmul(x,d['intervention']['readout'])), margin=z[0]-z[1]) for x in hidden]
    calibration = load('data/knowledge-assistant/ka1-calibration-v1.json')
    beam = d['sampling']['beam']
    schedules = {}
    for name in ['serial','continuous']:
        traces = [dict(id=r['id'],**latency(r['arrival_ms'],d['serving'][name][r['id']])) for r in d['serving']['requests']]
        end = max(v[-1] for v in d['serving'][name].values())
        count = sum(r['output_tokens'] for r in d['serving']['requests'])
        schedules[name] = dict(requests=traces,window_ms=[0,end],output_tokens=count,
                               throughput_tokens_per_second=count/(end/1000),
                               assumed_dollars=end/3600000*d['serving']['assumed_dollars_per_hour'])
    inputs = ['data/part-v/mechanisms.json','data/part-v/pipeline-input.json','data/mini-gpt/corpus.json',
              'code/part-v/mechanisms.py','code/part-v/run.py','data/knowledge-assistant/ka1-calibration-v1.json']
    return dict(version='part-v-derived-run-v1',status='CPU-derived results from assigned fixtures, not empirical model performance',
        recorded_at=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
        inputs_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
        budget_flops=[6*r['parameters']*r['training_tokens'] for r in d['budgets']],
        lifecycle_flops=[6*r['parameters']*r['training_tokens']+2*r['parameters']*d['scaling']['lifetime_output_tokens'] for r in d['budgets']],
        rotation_dots=[sum(x*y for x,y in zip(rotate_quarter(c['quarter_turn_vector'],m),rotate_quarter(c['quarter_turn_vector'],n))) for m,n in c['rotation_pairs']],
        rms=rmsnorm(c['rms_input'],0),rms_offset=rmsnorm(c['offset_input'],0),
        swiglu=swiglu(c['gate_input'],c['gate_matrix'],c['up_matrix'],c['down_matrix']),
        kv_bytes_per_layer=[kv_bytes(1,a['sequence_length'],heads,a['head_width'],a['bytes_per_value']) for heads in a['kv_heads']],
        training=dict(state_categories=states,state_bytes=sum(states),activation_bytes=activations,total_bytes=sum(states)+activations,
                      with_headroom_bytes=(sum(states)+activations)*(1+t['headroom_fraction']),
                      weighted_gradient=weighted_gradient(t['microbatch_mean_gradients'],t['microbatch_events'])),
        architecture=dict(total_parameters=a['shared_parameters']+a['experts']*a['expert_parameters'],
                          active_parameters=a['shared_parameters']+a['active_experts']*a['expert_parameters'],
                          linear=linear_prefix(a['linear_keys'],a['linear_values'])),
        intervention=intervention,rescue=[rescue(intervention[0]['margin'],intervention[1]['margin'],r['margin']) for r in intervention[2:4]],
        sampling=sampling,beam={str(w):two_step_beam(beam['first'],{'A':beam['after_A'],'B':beam['after_B']},w) for w in [1,2]},
        inference=latency(d['inference']['arrival_ms'],d['inference']['emission_ms']),
        small_cache_bytes=[kv_bytes(tokens=n,**d['inference']['small_kv']) for n in [8,9,10]],
        large_cache_bytes=kv_bytes(**d['inference']['large_kv']),
        quantization=quantize(d['inference']['quantization']['values'],0.5),
        serving=schedules,speculation=speculative_correction(d['serving']['speculative_target'],d['serving']['speculative_draft']),
        calibration={rule:confusion([r[field] for r in calibration['rows']],[r['semantic_score']==2 for r in calibration['rows']])
                     for rule,field in [('substring','contains_750'),('strict','strict_match')]},
        pipeline=pipeline(load('data/part-v/pipeline-input.json')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    arguments = parser.parse_args()
    result = run()
    if arguments.write:
        (ROOT/'data/part-v/derived-run.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ['budget_flops','rms','swiglu','training','serving']},indent=2))
