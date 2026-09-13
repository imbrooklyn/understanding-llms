# SPDX-License-Identifier: Apache-2.0
"""A tiny deterministic UTF-8 byte BPE, with an explicit serialized interface."""
from collections import Counter
import hashlib
import json
from pathlib import Path

BOS, EOS, PAD = 256, 257, 258
VERSION = 'book-byte-bpe-v1'


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()


def merge_pair(ids, pair, new_id):
    out, i = [], 0
    while i < len(ids):
        if i + 1 < len(ids) and tuple(ids[i:i + 2]) == tuple(pair):
            out.append(new_id)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out


def train(records, merge_count=32):
    sequences = [list(text.encode('utf-8')) for text in records]
    pieces = [bytes([i]).hex() for i in range(256)] + [None, None, None]
    merges = []
    for rank in range(merge_count):
        counts = Counter((a, b) for ids in sequences for a, b in zip(ids, ids[1:]))
        if not counts:
            raise ValueError('merge budget exceeds available pairs')
        pair = min(counts, key=lambda p: (-counts[p], p))
        new_id = len(pieces)
        pieces.append(pieces[pair[0]] + pieces[pair[1]])
        sequences = [merge_pair(ids, pair, new_id) for ids in sequences]
        merges.append(dict(rank=rank, pair=list(pair), count=counts[pair], new_id=new_id,
                           bytes_hex=pieces[-1], token_count=sum(map(len, sequences))))
    return dict(version=VERSION, normalization='none', encoding='UTF-8',
                boundaries='each record separately; no pretokenization',
                tie_rule='highest pair count, then smallest ordered pair of token IDs',
                special_ids=dict(BOS=BOS, EOS=EOS, PAD=PAD),
                training_records_sha256=canonical_hash(records), pieces_hex=pieces, merges=merges)


class ByteBPE:
    def __init__(self, artifact):
        if artifact['version'] != VERSION or artifact['normalization'] != 'none':
            raise ValueError('unsupported tokenizer contract')
        self.artifact = artifact
        self.pieces = [bytes.fromhex(x) if x is not None else None for x in artifact['pieces_hex']]
        self.vocab_size = len(self.pieces)
        self.sha256 = canonical_hash(artifact)

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for merge in self.artifact['merges']:
            ids = merge_pair(ids, merge['pair'], merge['new_id'])
        return ids

    def to_bytes(self, ids):
        if any(i < 0 or i >= self.vocab_size or self.pieces[i] is None for i in ids):
            raise ValueError('decode requires ordinary token IDs only')
        return b''.join(self.pieces[i] for i in ids)

    def decode(self, ids):
        return self.to_bytes(ids).decode('utf-8', errors='strict')


def load(root):
    return ByteBPE(json.loads((Path(root) / 'data/mini-gpt/tokenizer.json').read_text()))


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[2]
    corpus = json.loads((root / 'data/mini-gpt/corpus.json').read_text())
    artifact = train([r['text'] for r in corpus['train']])
    path = root / 'data/mini-gpt/tokenizer.json'
    path.write_text(json.dumps(artifact, indent=2) + '\n')
    print(json.dumps(dict(path=str(path.relative_to(root)), vocab_size=len(artifact['pieces_hex']), sha256=canonical_hash(artifact))))
