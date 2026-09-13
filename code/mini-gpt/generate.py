# SPDX-License-Identifier: Apache-2.0
"""Bounded generation with a separate sampling generator and explicit byte decoding."""
import torch
from tokenizer import BOS, EOS, PAD


def generate(model, tokenizer, prompt, mode='greedy', temperature=1.0, top_k=None, seed=31415, max_new=24):
    if temperature <= 0 or max_new < 0:
        raise ValueError('temperature must be positive and max_new nonnegative')
    if mode not in ('greedy', 'sample') or (top_k is not None and top_k < 1):
        raise ValueError('invalid sampling policy')
    context = [BOS] + tokenizer.encode(prompt)
    if len(context) > model.cfg['context_length']:
        raise ValueError('prompt exceeds context')
    rng = torch.Generator(device='cpu').manual_seed(seed)
    generated, trace, stop = [], [], 'max_new_tokens'
    model.eval()
    with torch.no_grad():
        for step in range(max_new):
            if len(context) >= model.cfg['context_length']:
                stop = 'context_limit'
                break
            logits = model(torch.tensor([context], dtype=torch.long))[0][0, -1]
            model_probs = logits.softmax(-1)
            adjusted = logits.clone() / temperature
            adjusted[[BOS, PAD]] = float('-inf')
            if top_k is not None:
                selected = torch.argsort(adjusted, descending=True, stable=True)[:min(top_k, tokenizer.vocab_size - 2)]
                keep = torch.zeros_like(adjusted, dtype=torch.bool)
                keep[selected] = True
                adjusted[~keep] = float('-inf')
            probabilities = adjusted.softmax(-1)
            chosen = int(adjusted.argmax()) if mode == 'greedy' else int(torch.multinomial(probabilities, 1, generator=rng))
            candidates = torch.argsort(logits, descending=True, stable=True)[:5].tolist()
            trace.append(dict(step=step + 1, context_ids=list(context), chosen_id=chosen,
                              chosen_hex=tokenizer.artifact['pieces_hex'][chosen],
                              model_probability=float(model_probs[chosen]), sampling_probability=float(probabilities[chosen]),
                              top5=[dict(id=i, bytes_hex=tokenizer.artifact['pieces_hex'][i], logit=float(logits[i]),
                                         model_probability=float(model_probs[i]), sampling_probability=float(probabilities[i])) for i in candidates]))
            context.append(chosen)
            if chosen == EOS:
                stop = 'EOS'
                break
            generated.append(chosen)
    payload = tokenizer.to_bytes(generated)
    try:
        decoded = payload.decode('utf-8', errors='strict')
        valid_utf8 = True
    except UnicodeDecodeError:
        decoded = payload.decode('utf-8', errors='replace')
        valid_utf8 = False
    return dict(prompt=prompt, mode=mode, temperature=temperature, top_k=top_k, seed=seed,
                max_new_tokens=max_new, stop=stop, generated_ids=generated, generated_hex=payload.hex(),
                valid_utf8=valid_utf8, display_decode='strict' if valid_utf8 else 'replace',
                completion=decoded, trace=trace)
