# SPDX-License-Identifier: Apache-2.0
import json
from pathlib import Path
import unittest
from tokenizer import ByteBPE, train, load, BOS, EOS, PAD

ROOT = Path(__file__).resolve().parents[2]


class TokenizerTests(unittest.TestCase):
    def test_training_uses_only_declared_records(self):
        corpus = json.loads((ROOT / 'data/mini-gpt/corpus.json').read_text())
        saved = load(ROOT)
        fresh = ByteBPE(train([r['text'] for r in corpus['train']]))
        self.assertEqual(saved.artifact, fresh.artifact)
        self.assertEqual(saved.vocab_size, 291)
        self.assertEqual(len(set(saved.artifact['pieces_hex'][:256])), 256)
        for split in ('train', 'validation'):
            for r in corpus[split]:
                self.assertEqual(saved.decode(saved.encode(r['text'])), r['text'])

    def test_all_valid_codepoints_in_representative_ranges(self):
        t = load(ROOT)
        ranges = [range(128), range(0x300, 0x370), range(0x4e00, 0x4f00), range(0x1f600, 0x1f650)]
        for points in ranges:
            text = ''.join(map(chr, points))
            self.assertEqual(t.decode(t.encode(text)), text)
        self.assertEqual(t.decode([]), '')
        self.assertNotEqual(t.encode('e\u0301'), t.encode('\u00e9'))

    def test_no_cross_record_merge_and_ties(self):
        t = train(['ab', 'cd'], merge_count=2)
        self.assertEqual([m['pair'] for m in t['merges']], [[97, 98], [99, 100]])
        self.assertNotIn('6263', t['pieces_hex'])
        self.assertEqual(ByteBPE(t).decode(ByteBPE(t).encode('abcd')), 'abcd')

    def test_special_ids_and_invalid_generated_bytes(self):
        t = load(ROOT)
        self.assertEqual(t.encode('BOS'), [66, 79, 83])
        for i in (BOS, EOS, PAD):
            with self.assertRaises(ValueError):
                t.decode([i])
        with self.assertRaises(UnicodeDecodeError):
            t.decode([255])


if __name__ == '__main__':
    unittest.main()
