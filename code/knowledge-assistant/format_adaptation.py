# SPDX-License-Identifier: Apache-2.0
"""Paired runtime format adaptation on the unchanged KA-1 diagnostic."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code/knowledge-assistant'))
from ka1 import load, sha, load_candidates, strict_match, percentile95
from baselines import load_fixture, run_locale
from tokenizer import load as load_tokenizer
from generate import generate
import torch

CONTRACT = 'data/knowledge-assistant/ka1-format-adaptation-v1.json'
FREEZE = 'data/knowledge-assistant/ka1-format-freeze-v1.json'
OUTPUT = 'data/knowledge-assistant/ka1-format-run-v1.json'
PATTERN = re.compile(r'([0-9]+)\.')


def normalize(response, amount_task, valid_utf8=True):
    if not amount_task or not valid_utf8:
        return response
    match = PATTERN.fullmatch(response.strip())
    return match.group(1) if match else response


def key(row):
    return tuple(row[name] for name in ('candidate', 'case', 'locale', 'policy', 'repeat', 'seed'))


def freeze():
    destination = ROOT / FREEZE
    if destination.exists():
        raise ValueError('adaptation freeze already exists')
    dependencies = list(load('data/knowledge-assistant/ka1-freeze-v1.json')['inputs_sha256'])
    dependencies += [CONTRACT, 'code/knowledge-assistant/format_adaptation.py',
        'data/knowledge-assistant/ka1-run-v1.json', 'data/knowledge-assistant/ka1-adjudication-v1.json',
        'code/knowledge-assistant/ka1.py', 'code/knowledge-assistant/baselines.py',
        'code/mini-gpt/model.py', 'code/mini-gpt/tokenizer.py', 'code/mini-gpt/generate.py',
        'code/part-vi/requirements.txt', 'code/part-iv/requirements-tested.txt']
    result = dict(recorded_at=datetime.now(timezone.utc).isoformat(),
                  status='frozen before new execution; inspected development cases',
                  inputs_sha256={path: sha(path) for path in sorted(set(dependencies))})
    destination.write_text(json.dumps(result, indent=2) + '\n')
    return result


def summarize(rows):
    results = []
    for candidate, policy, locale in sorted({(r['candidate'], r['policy'], r['locale']) for r in rows}):
        group = [r for r in rows if (r['candidate'], r['policy'], r['locale']) == (candidate, policy, locale)]
        cases = sorted({r['case'] for r in group})
        for arm in ('raw', 'normalized'):
            durations = [r['generation_ms'] + (r['normalization_ms'] if arm == 'normalized' else 0) for r in group]
            stable = sum(all(r['semantic_score'] == 2 for r in group if r['case'] == case) for case in cases)
            results.append(dict(candidate=candidate, policy=policy, locale=locale, arm=arm, attempts=len(group),
                strict_passes=sum(r[arm + '_strict'] for r in group),
                semantic_passes=sum(r['semantic_score'] == 2 for r in group),
                stable_semantic_cases=stable, cases=len(cases),
                changed_displays=sum(r['changed'] for r in group) if arm == 'normalized' else 0,
                median_ms=statistics.median(durations), p95_ms=percentile95(durations),
                generated_tokens_including_eos=sum(len(r['output']['trace']) for r in group),
                full_prefix_positions_processed=sum(r['processed_positions'] for r in group),
                decision='reject' if stable < len(cases) else 'diagnostic gate requires both locales'))
    return results


def run(write=False):
    contract, frozen = load(CONTRACT), load(FREEZE)
    for path, digest in frozen['inputs_sha256'].items():
        if sha(path) != digest:
            raise ValueError('frozen adaptation input changed: ' + path)
    original = load('data/knowledge-assistant/ka1-contract-v1.json')
    historical = {key(row): row for row in load('data/knowledge-assistant/ka1-run-v1.json')['rows']}
    reviews = {key(row): row for row in load('data/knowledge-assistant/ka1-adjudication-v1.json')['rows']}
    models, tokenizer = load_candidates(original), load_tokenizer(ROOT)
    before = {name: {k: v.clone() for k, v in model.state_dict().items()} for name, model in models.items()}
    for model in models.values():
        for _ in range(original['runtime']['warmup_calls_per_candidate']):
            generate(model, tokenizer, original['cases'][0]['prompt']['en'], max_new=2)
    rows = []
    for repeat, seed in enumerate(original['seeds']):
        order = list(models) if repeat % 2 == 0 else list(reversed(models))
        for case in original['cases']:
            for locale in original['locales']:
                for policy in original['policies']:
                    for candidate in order:
                        started = time.perf_counter_ns()
                        output = generate(models[candidate], tokenizer, case['prompt'][locale],
                            mode=policy['mode'], temperature=policy['temperature'], top_k=policy['top_k'],
                            seed=seed, max_new=original['adaptation']['max_new_tokens'])
                        generated = time.perf_counter_ns()
                        transformed = normalize(output['completion'],
                            case['id'] in contract['intervention']['amount_cases'], output['valid_utf8'])
                        finished = time.perf_counter_ns()
                        row = dict(candidate=candidate, case=case['id'], locale=locale,
                                   policy=policy['id'], repeat=repeat+1, seed=seed)
                        old = historical[key(row)]
                        if old['error'] is not None or output != old['output']:
                            raise ValueError('new output requires adjudication: ' + str(key(row)))
                        review = reviews[key(row)]
                        raw = output['completion']
                        row.update(output=output, raw=raw, normalized=transformed,
                            changed=raw != transformed,
                            raw_strict=output['valid_utf8'] and strict_match(raw, case['strict_accepted'][locale]),
                            normalized_strict=output['valid_utf8'] and strict_match(transformed, case['strict_accepted'][locale]),
                            semantic_score=review['semantic_score'],
                            semantic_reason=review['reason'],
                            transfer_reason='Exact raw replay; deleting one terminal period preserves every amount digit and factual scope.' if raw != transformed else 'Exact unchanged raw response and original disclosed adjudication.',
                            generation_ms=(generated-started)/1_000_000, normalization_ms=(finished-generated)/1_000_000,
                            prompt_tokens_including_bos=1+len(tokenizer.encode(case['prompt'][locale])),
                            processed_positions=sum(len(step['context_ids']) for step in output['trace']))
                        rows.append(row)
    unchanged = all(torch.equal(value, before[name][k]) for name, model in models.items() for k, value in model.state_dict().items())
    if not unchanged:
        raise ValueError('runtime adaptation changed parameters')
    result = dict(version='ka1-format-run-v1', recorded_at=datetime.now(timezone.utc).isoformat(),
        frozen_at=frozen['recorded_at'], inputs_sha256=frozen['inputs_sha256'],
        environment=dict(python=platform.python_version(), torch=torch.__version__, platform=platform.platform(),
                         device='cpu', dtype='float64', threads=torch.get_num_threads(),
                         timing='warm complete generate with trace, then immediate normalization; model/tokenizer loading excluded'),
        tokenizer_semantic_sha256=tokenizer.sha256, parameters_unchanged=unchanged,
        rows=rows, summary=summarize(rows),
        inherited_retrieval={locale: run_locale(load_fixture(), locale) for locale in original['locales']},
        review_method='Original disclosed AI-assisted author judgments transferred only after exact raw-output reproduction; terminal-period-only amount repair preserves semantic scores. No independent human panel or judge API.')
    if write:
        destination = ROOT / OUTPUT
        if destination.exists():
            raise ValueError('record already exists; replay without --write')
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', action='store_true')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = freeze() if args.freeze else run(args.write)
    print(json.dumps(result if args.freeze else dict(environment=result['environment'], summary=result['summary']), indent=2))
