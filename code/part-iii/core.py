# SPDX-License-Identifier: Apache-2.0
"""Deterministic sequence diagnostics; reuse Part II's checked numerical primitives."""
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code/part-ii'))
from numerical import dot, matmul, softmax, distribution


def fixture():
    data = json.loads((ROOT / 'data/part-iii/sequence-v1.json').read_text())
    source = ROOT / data['baseline_source']['path']
    if hashlib.sha256(source.read_bytes()).hexdigest() != data['baseline_source']['sha256']:
        raise ValueError('baseline source changed; review fixture version before comparing')
    data['long_task'] = json.loads(source.read_text())[data['baseline_source']['field']]
    return data


def recurrent(inputs, embedding, input_weight, recurrent_weight, hidden_bias, initial):
    """Return every input, previous activation, preactivation, and new activation."""
    state = list(initial)
    rows = []
    for step, token_id in enumerate(inputs, 1):
        if not 0 <= token_id < len(embedding):
            raise ValueError('token ID outside declared vocabulary')
        current = list(embedding[token_id])
        incoming = matmul([current], input_weight)[0]
        carried = matmul([state], recurrent_weight)[0]
        if not len(incoming) == len(carried) == len(hidden_bias) == len(state):
            raise ValueError('hidden dimensions differ')
        preactivation = [a + b + c for a, b, c in zip(incoming, carried, hidden_bias)]
        updated = [max(0.0, value) for value in preactivation]
        rows.append({'step': step, 'token_id': token_id, 'input': current,
                     'previous': state, 'preactivation': preactivation, 'state': updated})
        state = updated
    return rows


def readout(state, settings):
    logits = [a + b for a, b in zip(matmul([state], settings['output_weight'])[0], settings['output_bias'])]
    probabilities = softmax(logits)
    return {'logits': logits, 'probabilities': probabilities,
            'choice': max(range(len(logits)), key=logits.__getitem__)}


def rnn_log(inputs, settings):
    rows = recurrent(inputs, settings['embedding'], settings['input_weight'],
                     settings['recurrent_weight'], settings['hidden_bias'], settings['initial'])
    return [dict(row, **readout(row['state'], settings)) for row in rows]


def window_log(inputs, settings):
    if len(inputs) < 2:
        raise ValueError('two-token baseline requires at least two tokens')
    visible = inputs[-2:]
    joined = [x for token in visible for x in settings['embedding'][token]]
    state = [max(0, x) for x in matmul([joined], settings['window_weight'])[0]]
    return dict(visible_ids=visible, state=state, **readout(state, settings))


def scalar_bptt(inputs, weight, target, initial=0):
    """Linear positive-path diagnostic with one terminal half-squared loss."""
    states = [initial]
    for value in inputs:
        states.append(value + weight * states[-1])
    error = states[-1] - target
    gradients = [0.0] * len(inputs)
    contributions = [0.0] * len(inputs)
    carried = error
    for index in reversed(range(len(inputs))):
        gradients[index] = carried
        contributions[index] = carried * states[index]
        carried *= weight
    return {'states': states[1:], 'loss': .5 * error ** 2,
            'state_gradients': gradients, 'weight_contributions': contributions,
            'weight_gradient': math.fsum(contributions)}


def gate_examples(settings):
    lstm = settings['lstm']
    cell = lstm['forget'] * lstm['previous_cell'] + lstm['input'] * lstm['candidate']
    gru = settings['gru']
    candidate = math.tanh(gru['candidate_input'] + gru['candidate_recurrent_weight'] * gru['reset'] * gru['previous_hidden'])
    hidden = gru['update_retains_old'] * gru['previous_hidden'] + (1 - gru['update_retains_old']) * candidate
    return {'lstm_cell': cell, 'lstm_hidden': lstm['output'] * math.tanh(cell),
            'gru_candidate': candidate, 'gru_hidden': hidden,
            'retention_09_eight_edges': .9 ** 8, 'retention_099_hundred_edges': .99 ** 100}


def encode(inputs, settings):
    embedding = [[x * math.log(2) for x in row] for row in settings['embedding_in_units_of_ln2']]
    return recurrent(inputs, embedding, settings['input_weight'], settings['recurrent_weight'],
                     settings['hidden_bias'], settings['initial'])


def conditional_row(previous, settings):
    probabilities = settings['conditional_rows'][previous]
    distribution(probabilities)
    if len(probabilities) != len(settings['candidates']):
        raise ValueError('candidate order and probability row differ')
    return probabilities


def teacher_trace(settings):
    previous = settings['start']
    trace = []
    for step, target in enumerate(settings['target'], 1):
        probabilities = conditional_row(previous, settings)
        target_probability = probabilities[settings['candidates'].index(target)]
        trace.append({'step': step, 'input': previous, 'target': target,
                      'target_probability': target_probability,
                      'greedy': settings['candidates'][max(range(len(probabilities)), key=probabilities.__getitem__)]})
        previous = target
    return trace


def generate(settings):
    previous = settings['start']
    trace = []
    for step in range(1, settings['max_steps'] + 1):
        probabilities = conditional_row(previous, settings)
        chosen = max(range(len(probabilities)), key=probabilities.__getitem__)
        output = settings['candidates'][chosen]
        trace.append({'step': step, 'input': previous, 'output': output, 'probability': probabilities[chosen]})
        if output == settings['end']:
            return {'trace': trace, 'stopped_at_eos': True}
        previous = output
    return {'trace': trace, 'stopped_at_eos': False}


def attend(query, memory, keep=None):
    if not memory or not query or any(len(row) != len(query) for row in memory):
        raise ValueError('nonempty memory must match query width')
    indices = list(range(len(memory))) if keep is None else list(keep)
    if not indices or len(set(indices)) != len(indices) or any(i < 0 or i >= len(memory) for i in indices):
        raise ValueError('at least one distinct valid memory position required')
    scores = [dot(query, memory[i]) for i in indices]
    probabilities = softmax(scores)
    weights = [0.0] * len(memory)
    for i, probability in zip(indices, probabilities):
        weights[i] = probability
    context = [math.fsum(weight * row[j] for weight, row in zip(weights, memory)) for j in range(len(query))]
    return {'kept_positions': indices, 'scores_on_kept_positions': scores,
            'weights': weights, 'context': context}


def results(data=None):
    data = fixture() if data is None else data
    rnn = data['rnn']
    gradient = data['gradient']
    backward = scalar_bptt(gradient['inputs'], gradient['weight'], gradient['target'], gradient['initial'])
    updated_weight = gradient['weight'] - gradient['learning_rate'] * backward['weight_gradient']
    translation = data['translation']
    encoder = encode(translation['source_ids'], translation)
    memory = [row['state'] for row in encoder]
    attention = data['attention']
    probes = [attend(query, memory) for query in attention['queries']]
    slots, sources = [], []
    for removed in attention['deletion_indices']:
        slot = attend(attention['queries'][0], memory, [i for i in range(len(memory)) if i != removed])
        slot['readout'] = dot(slot['context'], attention['readout'])
        slots.append(dict(removed_position=removed, **slot))
        source_ids = [token for i, token in enumerate(translation['source_ids']) if i != removed]
        new_encoder = encode(source_ids, translation)
        source = attend(attention['queries'][0], [row['state'] for row in new_encoder])
        source['readout'] = dot(source['context'], attention['readout'])
        sources.append(dict(removed_position=removed, source_ids=source_ids, encoder=new_encoder, **source))
    teacher = teacher_trace(translation)
    probability = math.prod(row['target_probability'] for row in teacher)
    return {'short_rnn': [rnn_log(ids, rnn) for ids in rnn['short_inputs']],
            'long_rnn': [rnn_log(ids, rnn) for ids in data['long_task']['prefix_ids']],
            'window': [window_log(ids, rnn) for ids in data['long_task']['prefix_ids']],
            'bptt': backward, 'updated_weight': updated_weight,
            'after_update': scalar_bptt(gradient['inputs'], updated_weight, gradient['target']),
            'distance_products': [{'edges': d, 'contracting': .5 ** d, 'expanding': 1.5 ** d} for d in gradient['distances']],
            'gates': gate_examples(data['gates']), 'encoder': encoder,
            'contrast_encoder': encode(translation['contrast_source_ids'], translation),
            'teacher': teacher, 'generation': generate(translation),
            'target_sequence_probability': probability, 'target_total_nll': -math.log(probability),
            'target_mean_nll': -math.log(probability) / len(teacher),
            'attention': probes, 'slot_deletions': slots, 'source_deletions': sources}
