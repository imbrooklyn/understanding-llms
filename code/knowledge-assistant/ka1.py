# SPDX-License-Identifier: Apache-2.0
"""Run the frozen KA-1 diagnostic on existing CPU checkpoints; never call a service."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code/mini-gpt'))
import torch
from model import create_model, config
from tokenizer import load as load_tokenizer, BOS
from generate import generate
from baselines import load_fixture, run_locale


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def strict_match(completion, accepted):
    return completion.strip().casefold() in {s.strip().casefold() for s in accepted}


def percentile95(values):
    if not values:
        return None
    return sorted(values)[math.ceil(0.95 * len(values)) - 1]


def load_candidates(contract):
    models = {}
    for candidate in contract['candidates']:
        model = create_model(config())
        model.load_state_dict(torch.load(ROOT / candidate['checkpoint'], map_location='cpu', weights_only=True))
        model.eval()
        models[candidate['id']] = model
    return models


def summarize(rows):
    summaries = []
    groups = sorted({(r['candidate'], r['policy'], r['locale']) for r in rows})
    for candidate, policy, locale in groups:
        chosen = [r for r in rows if (r['candidate'], r['policy'], r['locale']) == (candidate, policy, locale)]
        durations = [r['elapsed_ms'] for r in chosen if r['error'] is None]
        by_case = {key: [r for r in chosen if r['case'] == key] for key in dict.fromkeys(r['case'] for r in chosen)}
        summaries.append(dict(candidate=candidate, policy=policy, locale=locale, attempts=len(chosen),
            strict_passes=sum(r['strict_match'] for r in chosen),
            stable_strict_cases=sum(all(r['strict_match'] for r in group) for group in by_case.values()),
            cases=len(by_case), errors=sum(r['error'] is not None for r in chosen),
            invalid_utf8=sum(r['error'] is None and not r['output']['valid_utf8'] for r in chosen),
            median_complete_call_ms=statistics.median(durations) if durations else None,
            p95_complete_call_ms=percentile95(durations)))
    return summaries


def run(write=False):
    contract = load('data/knowledge-assistant/ka1-contract-v1.json')
    freeze = load('data/knowledge-assistant/ka1-freeze-v1.json')
    for path, digest in freeze['inputs_sha256'].items():
        if sha(path) != digest:
            raise ValueError(f'frozen input changed: {path}')
    tokenizer = load_tokenizer(ROOT)
    models = load_candidates(contract)
    for model in models.values():
        for _ in range(contract['runtime']['warmup_calls_per_candidate']):
            generate(model, tokenizer, contract['cases'][0]['prompt']['en'], max_new=2)
    rows = []
    for repeat, seed in enumerate(contract['seeds']):
        order = list(models) if repeat % 2 == 0 else list(reversed(models))
        for case in contract['cases']:
            for locale in contract['locales']:
                for policy in contract['policies']:
                    for candidate in order:
                        started = time.perf_counter_ns()
                        output, error = None, None
                        try:
                            output = generate(models[candidate], tokenizer, case['prompt'][locale],
                                mode=policy['mode'], temperature=policy['temperature'], top_k=policy['top_k'],
                                seed=seed, max_new=contract['adaptation']['max_new_tokens'])
                        except ValueError as exc:
                            error = str(exc)
                        elapsed = (time.perf_counter_ns() - started) / 1_000_000
                        rows.append(dict(candidate=candidate,case=case['id'],locale=locale,policy=policy['id'],
                            repeat=repeat+1,seed=seed,prompt_tokens_including_bos=1+len(tokenizer.encode(case['prompt'][locale])),
                            elapsed_ms=elapsed,error=error,output=output,
                            strict_match=output is not None and output['valid_utf8'] and strict_match(output['completion'],case['strict_accepted'][locale])))
    dependencies = list(freeze['inputs_sha256']) + ['code/knowledge-assistant/ka1.py','code/knowledge-assistant/baselines.py',
        'code/mini-gpt/model.py','code/mini-gpt/tokenizer.py','code/mini-gpt/generate.py',
        'code/part-ii/text_processing.py','code/part-ii/numerical.py','code/part-v/requirements.txt','code/part-iv/requirements-tested.txt']
    result = dict(version='ka1-run-v1',recorded_at=datetime.now(timezone.utc).isoformat(),contract_frozen_at=freeze['recorded_at'],
        environment=dict(python=platform.python_version(),torch=torch.__version__,platform=platform.platform(),machine=platform.machine(),
                         threads=torch.get_num_threads(),dtype='float64',device='cpu',timing='complete generate call with trace collection; warm model; no KV cache'),
        inputs_sha256={p:sha(p) for p in dependencies},tokenizer_semantic_sha256=tokenizer.sha256,
        model_storage=[dict(candidate=key,parameters=sum(p.numel() for p in model.parameters()),
                            parameter_tensor_bytes=sum(p.numel()*p.element_size() for p in model.parameters())) for key,model in models.items()],
        rows=rows,summary=summarize(rows),
        inherited_retrieval={locale:run_locale(load_fixture(),locale) for locale in contract['locales']})
    if write:
        (ROOT/'data/knowledge-assistant/ka1-run-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args = parser.parse_args()
    result = run(args.write)
    print(json.dumps(dict(environment=result['environment'],summary=result['summary']),indent=2))
