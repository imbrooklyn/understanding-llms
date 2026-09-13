# SPDX-License-Identifier: Apache-2.0
"""Check actual project behavior and complete evidence without replacing historical logs."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/knowledge-assistant'))
import ka1
from tokenizer import load


def read(path):return json.loads((ROOT/path).read_text())
def key(row):return tuple(row[k] for k in ['candidate','policy','case','locale','repeat','seed'])


class KA1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archived=read('data/knowledge-assistant/ka1-run-v1.json')
        cls.replay=ka1.run(write=False)
        cls.contract=read('data/knowledge-assistant/ka1-contract-v1.json')

    def test_complete_paired_matrix_and_same_inputs(self):
        rows=self.archived['rows'];self.assertEqual(len(rows),144)
        self.assertEqual(len({key(r) for r in rows}),144)
        expected={(c['id'],p['id'],case['id'],lang,i+1,seed) for c in self.contract['candidates']
                  for p in self.contract['policies'] for case in self.contract['cases']
                  for lang in self.contract['locales'] for i,seed in enumerate(self.contract['seeds'])}
        self.assertEqual({key(r) for r in rows},expected)
        for row in rows:
            prompt=next(c for c in self.contract['cases'] if c['id']==row['case'])['prompt'][row['locale']]
            self.assertEqual(row['output']['prompt'],prompt)
            self.assertEqual(row['prompt_tokens_including_bos'],1+len(load(ROOT).encode(prompt)))
            self.assertGreaterEqual(row['elapsed_ms'],0)

    def test_cpu_replay_ids_bytes_stops_and_utf8(self):
        actual={key(r):r for r in self.replay['rows']}
        for row in self.archived['rows']:
            other=actual[key(row)]
            self.assertEqual(row['error'],other['error'])
            for field in ['generated_ids','generated_hex','completion','stop','valid_utf8']:
                self.assertEqual(row['output'][field],other['output'][field],(key(row),field))

    def test_frozen_inputs_and_recorded_source_hashes(self):
        freeze=read('data/knowledge-assistant/ka1-freeze-v1.json')
        self.assertLess(datetime.fromisoformat(freeze['recorded_at']),datetime.fromisoformat(self.archived['recorded_at']))
        for path,digest in self.archived['inputs_sha256'].items():self.assertEqual(ka1.sha(path),digest,path)
        self.assertEqual(self.archived['model_storage'][0]['parameter_tensor_bytes'],13_875*8)

    def test_adjudication_covers_every_attempt_and_handles_punctuation(self):
        review=read('data/knowledge-assistant/ka1-adjudication-v1.json')
        self.assertEqual(review['run_sha256'],ka1.sha('data/knowledge-assistant/ka1-run-v1.json'))
        indexed={key(r):r for r in review['rows']}
        self.assertEqual(set(indexed),{key(r) for r in self.archived['rows']})
        for row in self.archived['rows']:
            label=indexed[key(row)];completion=row['output']['completion']
            self.assertEqual(label['completion_sha256'],hashlib.sha256(completion.encode()).hexdigest())
            if label['semantic_score']==2:
                self.assertEqual(completion,'750.');self.assertIn(row['case'],['current-limit','stale-premise'])
                self.assertEqual(row['locale'],'en');self.assertFalse(row['strict_match'])
            if row['case']=='historical-limit' and completion=='750.':self.assertEqual(label['semantic_score'],0)
        self.assertEqual(sum(r['semantic_score']==2 for r in review['rows']),7)

    def test_both_languages_keep_all_lexical_baselines(self):
        for locale in self.contract['locales']:
            actual=self.replay['inherited_retrieval'][locale]
            self.assertEqual(actual,self.archived['inherited_retrieval'][locale])
            self.assertEqual(actual['success_counts'],dict(keyword=5,count=6,tfidf=7))
            self.assertEqual(actual['query_count'],9)

    def test_actual_stops_and_decoding_failure_are_retained(self):
        rows=self.archived['rows']
        self.assertTrue(any(r['output']['stop']=='context_limit' for r in rows))
        self.assertEqual(sum(not r['output']['valid_utf8'] for r in rows),1)
        self.assertFalse(any(r['strict_match'] for r in rows))
        self.assertFalse(ka1.strict_match('The cap is not 750; use 600.',['750']))
        self.assertTrue(ka1.strict_match('  PROCESSING  ',['processing']))
        self.assertEqual(ka1.percentile95(list(range(1,19))),18)


if __name__=='__main__':unittest.main()
