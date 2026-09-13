# SPDX-License-Identifier: Apache-2.0
"""MG-1: record raw inputs, shapes, selected coordinates, all logits of one prediction."""
import json
import math
from pathlib import Path
import torch
from model import ROOT, config, create_model, batch_records, IGNORE
from tokenizer import load, canonical_hash


def run():
    cfg = config()
    tokenizer = load(ROOT)
    corpus = json.loads((ROOT / 'data/mini-gpt/corpus.json').read_text())
    records = corpus['train'][4:6]
    ids, valid, targets = batch_records(records, tokenizer, cfg['context_length'])
    model = create_model(cfg)
    model.eval()
    with torch.no_grad():
        logits, loss, values = model(ids, valid, targets, trace=True)
    position = 5
    target = int(targets[0, position])
    row = logits[0, position]
    maximum = float(row.max())
    denominator = sum(math.exp(float(z) - maximum) for z in row)
    probability = math.exp(float(row[target]) - maximum) / denominator
    independent_losses = []
    for b in range(len(records)):
        for t in range(cfg['context_length']):
            if targets[b, t] == IGNORE:
                continue
            a = logits[b, t].tolist()
            m = max(a)
            independent_losses.append(m + math.log(sum(math.exp(z - m) for z in a)) - a[int(targets[b, t])])
    independent = sum(independent_losses) / len(independent_losses)
    assert abs(independent - float(loss)) < 1e-12
    zero_loss = torch.nn.functional.cross_entropy(torch.zeros((len(independent_losses), cfg['vocab_size']), dtype=torch.float64), torch.zeros(len(independent_losses), dtype=torch.long))
    assert abs(float(zero_loss) - math.log(cfg['vocab_size'])) < 1e-12
    selected = {}
    for name, value in values.items():
        if value.ndim == 3 and value.shape[0] == 2:
            selected[name] = value[0, position].tolist()
    selected['position_embedding'] = values['position_embedding'][position].tolist()
    return dict(milestone='MG-1', config=cfg, tokenizer_sha256=tokenizer.sha256,
                corpus_sha256=canonical_hash(corpus), parameter_count=sum(p.numel() for p in model.parameters()),
                records=[dict(id=r['id'], text=r['text'], ids=ids[b][valid[b]].tolist(),
                              targets=targets[b][valid[b]].tolist(), scored_events=int(valid[b].sum())) for b, r in enumerate(records)],
                padded_shape=list(ids.shape), shapes={k:list(v.shape) for k,v in values.items()},
                selected_position_zero_based=position, selected_rows=selected,
                selected_head_query=values['q_heads'][0, 0, position].tolist(),
                selected_head_key0=values['k_heads'][0, 0, 0].tolist(),
                selected_head_scores=values['scores'][0, 0, position, :position+1].tolist(),
                selected_head_weights=values['weights'][0, 0, position, :position+1].tolist(),
                target_id=target, target_logit=float(row[target]), row_maximum=maximum,
                shifted_exp_sum=denominator, target_probability=probability, target_loss=-math.log(probability),
                scored_events=len(independent_losses), loss=float(loss), scalar_mean_loss=independent,
                zero_logits_loss=float(zero_loss), analytic_zero_logits_loss=math.log(cfg['vocab_size']))


if __name__ == '__main__':
    result = run()
    (ROOT / 'data/mini-gpt/forward.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k:result[k] for k in ['parameter_count','target_id','target_probability','target_loss','scored_events','loss','zero_logits_loss']}, indent=2))
