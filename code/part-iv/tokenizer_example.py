# SPDX-License-Identifier: Apache-2.0
"""Word-boundary BPE and supplied-vocabulary WordPiece teaching traces."""
from collections import Counter
import json
from pathlib import Path
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code/mini-gpt'))
from tokenizer import load, merge_pair


def hand_trace(spec):
    words = spec['words']
    segments = {word: list(word) + [spec['end_marker']] for word in words}
    trace = []
    for rank in range(spec['merge_budget']):
        counts = Counter()
        for word, pieces in segments.items():
            for pair in zip(pieces, pieces[1:]):
                counts[pair] += words[word]
        pair = min(counts, key=lambda p: (-counts[p], p))
        segments = {word: merge_pair(pieces, pair, ''.join(pair)) for word, pieces in segments.items()}
        trace.append(dict(rank=rank + 1, counts=[dict(pair=list(p), count=n) for p, n in sorted(counts.items())],
                          selected=list(pair), selected_count=counts[pair], segments=segments))
    return trace


def wordpiece(word, vocabulary):
    pieces, offset = [], 0
    while offset < len(word):
        candidates = [('' if offset == 0 else '##') + word[offset:end]
                      for end in range(len(word), offset, -1)]
        match = next((p for p in candidates if p in vocabulary), None)
        if match is None:
            return ['[UNK]']
        pieces.append(match)
        offset += len(match.removeprefix('##'))
    return pieces


def run():
    cases = json.loads((ROOT / 'data/part-iv/tokenizer-cases.json').read_text())
    trace = hand_trace(cases['hand_bpe'])
    assert [x['selected'] for x in trace] == cases['hand_bpe']['expected_pairs']
    assert [x['selected_count'] for x in trace] == cases['hand_bpe']['expected_counts']
    assert trace[-1]['segments'] == cases['hand_bpe']['expected_final']
    tokenizer = load(ROOT)
    roundtrips = []
    for text in cases['roundtrip_texts']:
        ids = tokenizer.encode(text)
        decoded = tokenizer.decode(ids)
        assert text == decoded
        roundtrips.append(dict(text=text, utf8_bytes=list(text.encode('utf-8')), codepoints=len(text),
                               byte_count=len(text.encode('utf-8')), ids=ids, token_count=len(ids), decoded=decoded))
    wp = []
    for c in cases['wordpiece']['cases']:
        result = wordpiece(c['text'], cases['wordpiece']['vocabulary'])
        assert result == c['expected']
        wp.append(dict(text=c['text'], pieces=result))
    raw = cases['normalization_counterexample']['raw']
    normalized = unicodedata.normalize('NFC', raw)
    assert normalized == cases['normalization_counterexample']['normalized_nfc'] and normalized != raw
    return dict(hand_bpe=trace, tokenizer_sha256=tokenizer.sha256, roundtrips=roundtrips,
                wordpiece=wp, unicode_data=unicodedata.unidata_version,
                normalization=dict(raw=raw, normalized=normalized, raw_equal=False))


if __name__ == '__main__':
    result = run()
    (ROOT / 'data/part-iv/tokenizer-run.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
