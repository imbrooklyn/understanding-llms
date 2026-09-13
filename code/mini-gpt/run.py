# SPDX-License-Identifier: Apache-2.0
"""MG-2: train, checkpoint, resume, rerun in a fresh process, and record generation."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
import torch
from model import ROOT, config, create_model, batch_records
from tokenizer import load, canonical_hash
from generate import generate
import forward


def digest(value):
    h = hashlib.sha256()
    def visit(x):
        if isinstance(x, torch.Tensor):
            h.update(str(x.dtype).encode())
            h.update(str(list(x.shape)).encode())
            h.update(x.detach().cpu().contiguous().numpy().tobytes())
        elif isinstance(x, dict):
            for key in sorted(x, key=str):
                h.update(str(key).encode()); visit(x[key])
        elif isinstance(x, (list, tuple)):
            for item in x:
                visit(item)
        else:
            h.update(repr(x).encode())
    visit(value)
    return h.hexdigest()


def identities(cfg, tokenizer, corpus):
    return dict(config=canonical_hash(cfg), tokenizer=tokenizer.sha256, corpus=canonical_hash(corpus))


def optimizer(model, cfg):
    return torch.optim.Adam(model.parameters(), lr=cfg['learning_rate'], betas=tuple(cfg['betas']),
                            eps=cfg['adam_epsilon'], weight_decay=cfg['weight_decay'], foreach=False)


def checkpoint(model, opt, rng, step, identity):
    return dict(model=copy.deepcopy(model.state_dict()), optimizer=copy.deepcopy(opt.state_dict()),
                batch_rng=rng.get_state(), torch_rng=torch.get_rng_state(), step=step,
                identities=identity, config=model.cfg)


def restore(path, cfg, tokenizer, corpus):
    saved = torch.load(path, map_location='cpu', weights_only=True)
    if saved['identities'] != identities(cfg, tokenizer, corpus):
        raise ValueError('checkpoint data, tokenizer, or configuration identity mismatch')
    model = create_model(cfg)
    opt = optimizer(model, cfg)
    model.load_state_dict(saved['model'])
    opt.load_state_dict(saved['optimizer'])
    rng = torch.Generator(device='cpu')
    rng.set_state(saved['batch_rng'])
    torch.set_rng_state(saved['torch_rng'])
    return model, opt, rng, saved['step']


def evaluate(model, batch):
    model.eval()
    with torch.no_grad():
        value = float(model(batch[0], batch[1], batch[2])[1])
    model.train()
    return value


def train(cfg, tokenizer, corpus, destination, resume=None):
    started = time.perf_counter()
    destination.mkdir(parents=True, exist_ok=True)
    if resume is None:
        model = create_model(cfg)
        opt = optimizer(model, cfg)
        rng = torch.Generator(device='cpu').manual_seed(cfg['batch_seed'])
        step0 = 0
    else:
        model, opt, rng, step0 = restore(resume, cfg, tokenizer, corpus)
    train_batch = batch_records(corpus['train'], tokenizer, cfg['context_length'])
    val_batch = batch_records(corpus['validation'], tokenizer, cfg['context_length'])
    curve, steps = [], []
    best_loss, best_step, best_state = float('inf'), None, None
    def measure(step):
        nonlocal best_loss, best_step, best_state
        row = dict(step=step, train_loss=evaluate(model, train_batch), validation_loss=evaluate(model, val_batch))
        curve.append(row)
        if row['validation_loss'] < best_loss:
            best_loss, best_step = row['validation_loss'], step
            best_state = copy.deepcopy(model.state_dict())
    measure(step0)
    for step in range(step0 + 1, cfg['steps'] + 1):
        indices = torch.randint(len(corpus['train']), (cfg['batch_size'],), generator=rng)
        batch = tuple(x[indices] for x in train_batch)
        model.train()
        opt.zero_grad(set_to_none=True)
        loss = model(batch[0], batch[1], batch[2])[1]
        loss.backward()
        opt.step()
        steps.append(dict(step=step, batch_indices=indices.tolist(), batch_loss_before_update=float(loss.detach())))
        if step % cfg['eval_every'] == 0:
            measure(step)
        if resume is None and step == cfg['resume_step']:
            torch.save(checkpoint(model, opt, rng, step, identities(cfg, tokenizer, corpus)), destination / 'resume-step300.pt')
    final = checkpoint(model, opt, rng, cfg['steps'], identities(cfg, tokenizer, corpus))
    torch.save(final, destination / 'resume-final.pt')
    torch.save(best_state, destination / 'weights-selected.pt')
    torch.save(model.state_dict(), destination / 'weights-final.pt')
    next_rng = torch.Generator().set_state(rng.get_state())
    next_indices = torch.randint(len(corpus['train']), (cfg['batch_size'],), generator=next_rng).tolist()
    result = dict(curve=curve, steps=steps, selected_step=best_step, selected_validation_loss=best_loss,
                  parameter_sha256=digest(model.state_dict()), optimizer_sha256=digest(opt.state_dict()),
                  batch_rng_sha256=digest(rng.get_state()), torch_rng_sha256=digest(torch.get_rng_state()),
                  next_batch_indices=next_indices, train_events=int(train_batch[1].sum()),
                  validation_events=int(val_batch[1].sum()), elapsed_seconds=time.perf_counter()-started)
    return model, result, best_state


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def pipeline(destination, single=False):
    start = time.perf_counter()
    cfg = config(); tokenizer = load(ROOT)
    corpus = json.loads((ROOT / 'data/mini-gpt/corpus.json').read_text())
    model, result, best_state = train(cfg, tokenizer, corpus, destination)
    if single:
        write_json(destination / 'single-run.json', result)
        return
    write_json(destination / 'forward.json', forward.run())
    with tempfile.TemporaryDirectory(prefix='mini-gpt-check-') as tmp:
        base = Path(tmp)
        resumed, resume_result, _ = train(cfg, tokenizer, corpus, base / 'resumed', destination / 'resume-step300.pt')
        resumed_checks = {key: result[key] == resume_result[key] for key in ['parameter_sha256','optimizer_sha256','batch_rng_sha256','torch_rng_sha256','next_batch_indices']}
        resumed_checks['steps_301_to_600'] = result['steps'][cfg['resume_step']:] == resume_result['steps']
        resumed_checks['curve_300_to_600'] = result['curve'][cfg['resume_step']//cfg['eval_every']:] == resume_result['curve']
        assert all(resumed_checks.values()), resumed_checks
        fresh_dir = base / 'fresh'
        subprocess.run([sys.executable, str(Path(__file__).resolve()), '--single-run', '--output', str(fresh_dir)], check=True, cwd=ROOT)
        fresh = json.loads((fresh_dir / 'single-run.json').read_text())
        fresh_checks = {key: result[key] == fresh[key] for key in ['curve','steps','selected_step','parameter_sha256','optimizer_sha256','batch_rng_sha256','torch_rng_sha256','next_batch_indices']}
        assert all(fresh_checks.values()), fresh_checks
        resume_seconds = resume_result['elapsed_seconds']
        fresh_seconds = fresh['elapsed_seconds']
    extra = json.loads((ROOT / 'data/mini-gpt/generation-probes.json').read_text())
    selected = create_model(cfg)
    selected.load_state_dict(best_state)
    generations = []
    baseline_generations = []
    for label, current in [('selected', selected), ('final', model)]:
        for i, probe in enumerate(corpus['diagnostics']):
            entry = generate(current, tokenizer, probe['prompt'], seed=cfg['sampling_seed'], max_new=cfg['max_new_tokens'])
            entry.update(checkpoint=label, diagnostic_index=i, expected_suffix=probe['expected_suffix'], exact_suffix_match=entry['completion']==probe['expected_suffix'])
            generations.append(entry)
            baseline_generations.append(entry)
        for temperature in (0.7, 1.2):
            old = generate(current, tokenizer, corpus['diagnostics'][0]['prompt'], mode='sample', temperature=temperature, top_k=5, seed=cfg['sampling_seed'], max_new=cfg['max_new_tokens'])
            old.update(checkpoint=label, diagnostic_index=0)
            baseline_generations.append(old)
        for probe in extra['probes']:
            entry = generate(current, tokenizer, probe['prompt'], seed=cfg['sampling_seed'], max_new=cfg['max_new_tokens'])
            entry.update(checkpoint=label, probe_id=probe['id'], expected_suffix=probe['expected_suffix'], exact_suffix_match=entry['completion']==probe['expected_suffix'])
            generations.append(entry)
        for temperature in (0.7, 1.2):
            entry = generate(current, tokenizer, extra['probes'][0]['prompt'], mode='sample', temperature=temperature, top_k=5, seed=cfg['sampling_seed'], max_new=cfg['max_new_tokens'])
            entry.update(checkpoint=label, probe_id='aligned-red')
            generations.append(entry)
    write_json(destination / 'generation-baseline.json', baseline_generations)
    write_json(destination / 'generation.json', generations)
    sources = ['data/mini-gpt/corpus.json','data/mini-gpt/config.json','data/mini-gpt/tokenizer.json','data/mini-gpt/generation-probes.json',
               'code/mini-gpt/model.py','code/mini-gpt/tokenizer.py','code/mini-gpt/forward.py','code/mini-gpt/generate.py','code/mini-gpt/run.py',
               'code/part-iv/requirements.txt','code/part-iv/requirements-tested.txt']
    result.update(milestone='MG-2', recorded_at=datetime.now(timezone.utc).isoformat(), config=cfg,
                  identities=identities(cfg, tokenizer, corpus),
                  environment=dict(python=platform.python_version(), torch=str(torch.__version__), platform=platform.platform(),
                                   machine=platform.machine(), device='cpu', dtype='float64', threads=torch.get_num_threads(),
                                   deterministic_algorithms=torch.are_deterministic_algorithms_enabled()),
                  resumed_checks=resumed_checks, fresh_process_checks=fresh_checks,
                  resume_elapsed_seconds=resume_seconds, fresh_elapsed_seconds=fresh_seconds,
                  total_elapsed_seconds=time.perf_counter()-start,
                  checkpoints={p.name:dict(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(destination.glob('*.pt'))},
                  source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})
    write_json(destination / 'training-run.json', result)
    print(json.dumps(dict(selected_step=result['selected_step'], curve=result['curve'],
                          resumed_checks=resumed_checks, fresh_process_checks=fresh_checks,
                          elapsed_seconds=result['elapsed_seconds'], total_elapsed_seconds=result['total_elapsed_seconds']), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'data/mini-gpt')
    parser.add_argument('--single-run', action='store_true')
    args = parser.parse_args()
    pipeline(args.output, args.single_run)
