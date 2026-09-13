# SPDX-License-Identifier: Apache-2.0
"""Behavioral checks against hand-derived results and retained KA-1 outputs."""
import copy
import json
import math
import sys
import unittest

from core import (ROOT, audit_serialized, dpo, fixture, kl, low_rank, masked_loss,
                  matmul, parse_amount, replay_case, reimburse, serialize, verify_amount, verify_process)
from run import run, verify
sys.path.insert(0, str(ROOT / 'code/knowledge-assistant'))
from format_adaptation import normalize, run as run_adaptation, key


class Mechanisms(unittest.TestCase):
    def test_execution_matches_independent_fixture(self):
        verify(run())

    def test_shift_targets_not_input_roles(self):
        data = fixture('sft-v1.json')
        result = serialize(data['messages'], data['vocabulary'])
        self.assertEqual(result['inputs'][7], data['vocabulary'].index('<assistant>'))
        self.assertEqual(result['targets'][7], data['vocabulary'].index('Paris'))
        self.assertEqual(result['mask'][7:], [1, 1, 1])
        self.assertEqual(result['targets'][-1], data['vocabulary'].index('<eot>'))
        self.assertEqual(sum(result['mask']), 3)
        with self.assertRaisesRegex(ValueError, 'shifted target'):
            audit_serialized(data['messages'], data['vocabulary'], result['ids'], [0] + result['mask'][:-1])

    def test_only_scored_probabilities_affect_loss(self):
        mask = fixture('expected.json')['sft']['mask']
        base = [0.01] * 7 + [.5, .25, .5]
        self.assertAlmostEqual(masked_loss(base, mask), math.log(16) / 3)
        self.assertAlmostEqual(masked_loss([.99] * 7 + base[7:], mask), masked_loss(base, mask))
        self.assertAlmostEqual(masked_loss(base[:-2] + [.5, .5], mask), math.log(8) / 3)
        self.assertAlmostEqual(masked_loss([.5, .25, .5, .25], [1] * 4), math.log(64) / 4)
        for probabilities, bits in [([.5], [0]), ([0], [1]), ([float('nan')], [1]), ([.5], [2]), ([], [1])]:
            with self.assertRaises(ValueError):
                masked_loss(probabilities, bits)

    def test_kl_direction_zero_and_missing_support(self):
        self.assertAlmostEqual(kl([.75, .25], [.5, .5]), .13081203594113697)
        self.assertAlmostEqual(kl([.5, .5], [.75, .25]), .14384103622589045)
        self.assertEqual(kl([0, 1], [0, 1]), 0)
        self.assertEqual(kl([.5, .5], [1, 0]), math.inf)
        self.assertEqual(kl([1, 0], [.5, .5]), math.log(2))
        with self.assertRaises(ValueError):
            kl([.6, .6], [.5, .5])

    def test_dpo_reference_changes_relative_preference(self):
        self.assertAlmostEqual(dpo(.75, .25, .5, .5)['probability'], .75)
        self.assertAlmostEqual(dpo(.75, .25, .8, .2)['probability'], 3 / 7)
        self.assertAlmostEqual(dpo(.25, .75, .5, .5)['loss'], math.log(4))
        self.assertAlmostEqual(dpo(.75, .25, .75, .25)['loss'], math.log(2))
        self.assertTrue(math.isfinite(dpo(1e-300, 1, .5, .5, beta=100)['loss']))
        with self.assertRaises(ValueError):
            dpo(.75, .25, .5, .5, beta=0)

    def test_rule_transfer_and_no_allowance_pooling(self):
        self.assertEqual(reimburse([680, 820], 750), 1430)
        self.assertEqual(reimburse([680, 820], 700), 1380)
        self.assertNotEqual(reimburse([680, 820], 750), min(680 + 820, 750 * 2))
        self.assertEqual(reimburse([0, 1000, 3], 600), 603)
        for costs, cap in [([], 750), ([True], 1), ([-1], 1), ([1], -1), ([1.5], 2)]:
            with self.assertRaises(ValueError):
                reimburse(costs, cap)

    def test_verifier_false_accepts_and_false_rejects(self):
        data = fixture('reasoning-v1.json')
        labels = [row['answer_correct'] for row in data['candidates']]
        predictions = data['expected_acceptance']
        for name, expected in [('substring', (2, 1)), ('exact', (0, 1)), ('rule', (0, 0))]:
            actual = predictions[name]
            self.assertEqual((sum(p and not y for p, y in zip(actual, labels)),
                              sum(not p and y for p, y in zip(actual, labels))), expected)
        lucky = data['candidates'][2]
        self.assertTrue(verify_amount(data['costs'], data['cap'], lucky['response'])['accepted'])
        self.assertFalse(verify_process(data['costs'], data['cap'], lucky))
        self.assertFalse(verify_amount([680, 820], 700, '1430')['accepted'])

    def test_amount_parser_enforces_declared_grammar(self):
        for text, value in [('1430', 1430), (' 1,430\n', 1430), ('0', 0), ('12,345,678', 12345678)]:
            self.assertEqual(parse_amount(text), value)
        for text in ['1,43', '01', '-1', '1.0', '１４３０', 'Not 1430; pay 1500.', '<answer>1430</answer>', '']:
            self.assertIsNone(parse_amount(text), text)

    def test_budget_reserves_check_and_retains_rejections(self):
        case = fixture('budget-v1.json')['cases'][0]
        empty = replay_case(case, 'search', 1, ['A', 'B', 'C'])
        self.assertEqual((empty['selected'], empty['calls'], empty['tokens']), (None, [], 0))
        failed = replay_case(case, 'search', 3, ['A', 'B', 'C'])
        self.assertIsNone(failed['selected'])
        self.assertEqual(failed['call_count'], 2)
        passed = replay_case(case, 'search', 4, ['A', 'B', 'C'])
        self.assertEqual([call['response'] for call in passed['calls']],
                         ['680 + 820 = 1500', 'reject', '680 + 750 = 1430', 'accept'])
        self.assertEqual(passed['tokens'], 58)

    def test_vote_can_regress_and_duplicates_are_charged(self):
        case = fixture('budget-v1.json')['cases'][2]
        first = replay_case(case, 'vote', 2, ['A', 'B', 'C'])
        third = replay_case(case, 'vote', 3, ['A', 'B', 'C'])
        self.assertTrue(first['correct'])
        self.assertFalse(third['correct'])
        self.assertEqual(third['tokens'], 42)
        self.assertEqual(third['call_count'], 3)

    def test_selector_reads_answer_text_not_gold_metadata(self):
        case = copy.deepcopy(fixture('budget-v1.json')['cases'][0])
        case['candidates'][0]['total'] = 1430
        result = replay_case(case, 'search', 2, ['A', 'B', 'C'])
        self.assertIsNone(result['selected'])
        self.assertEqual(result['calls'][1]['response'], 'reject')

    def test_low_rank_merge_scale_and_frozen_inputs(self):
        data = fixture('low-rank-v1.json')
        original = copy.deepcopy(data)
        result = low_rank(data['W0'], data['A'], data['B'], data['x'])
        self.assertEqual(result['combined_output'], [0, 2, 4, 1])
        self.assertEqual(result['combined_output'], result['merged_output'])
        self.assertEqual(data, original)
        self.assertEqual(low_rank(data['W0'], data['A'], data['B'], [1, 0, 0])['combined_output'], [3, 0, -2, 5])
        self.assertEqual(low_rank(data['W0'], data['A'], data['B'], data['x'], 2)['combined_output'], [-1, 2, 5, -1])
        self.assertEqual(low_rank(data['W0'], data['A'], [[0], [0], [0], [0]], data['x'])['combined_output'], [1, 2, 3, 3])

    def test_matrix_dimensions_and_parameter_counts(self):
        with self.assertRaises(ValueError):
            matmul([[1, 2]], [[1, 2]])
        with self.assertRaises(ValueError):
            matmul([[1], [1, 2]], [[1]])
        self.assertEqual(1 * (4 + 3), 7)
        self.assertGreater(2 * (4 + 3), 4 * 3)
        self.assertEqual(8 * (4096 + 4096) / 4096**2, 1 / 256)


class RuntimeAdaptation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replay = run_adaptation()
        cls.saved = json.loads((ROOT / 'data/knowledge-assistant/ka1-format-run-v1.json').read_text())

    def test_normalizer_narrow_scope_idempotence_and_digit_preservation(self):
        for text, expected in [('750.', '750'), (' 600.\n', '600'), ('00750.', '00750'),
                               ('750.0', '750.0'), ('not 750.', 'not 750.'), ('750 ye is t.', '750 ye is t.'),
                               ('７５０.', '７５０.'), ('750.\ufffd', '750.\ufffd')]:
            result = normalize(text, True)
            self.assertEqual(result, expected)
            self.assertEqual(normalize(result, True), result)
            self.assertEqual(normalize(text, False), text)
            self.assertEqual(normalize(text, True, False), text)
        self.assertEqual(normalize('750.', True), '750')

    def test_all_raw_generations_and_paired_decisions_reproduce(self):
        old = {key(row): row for row in self.saved['rows']}
        self.assertEqual(len(self.replay['rows']), 144)
        self.assertEqual(len(old), 144)
        for row in self.replay['rows']:
            saved = old[key(row)]
            for field in ('output', 'raw', 'normalized', 'semantic_score', 'raw_strict', 'normalized_strict', 'changed', 'processed_positions'):
                self.assertEqual(row[field], saved[field], (key(row), field))
            self.assertGreaterEqual(row['generation_ms'], 0)
            self.assertGreaterEqual(row['normalization_ms'], 0)
        self.assertTrue(self.replay['parameters_unchanged'])

    def test_gain_is_format_only_and_historical_failure_is_retained(self):
        rows = [row for row in self.replay['rows'] if row['candidate'] == 'selected-50'
                and row['locale'] == 'en' and row['policy'] == 'greedy']
        self.assertEqual(sum(row['changed'] for row in rows), 9)
        self.assertEqual(sum(row['raw_strict'] for row in rows), 0)
        self.assertEqual(sum(row['normalized_strict'] for row in rows), 6)
        self.assertEqual(sum(row['semantic_score'] == 2 for row in rows), 6)
        history = [row for row in rows if row['case'] == 'historical-limit']
        self.assertEqual(len(history), 3)
        self.assertTrue(all(row['normalized'] == '750' and row['semantic_score'] == 0 for row in history))
        for summary in self.replay['summary']:
            self.assertEqual(summary['decision'], 'reject')

    def test_retained_lexical_baselines_and_invalid_utf8(self):
        self.assertEqual(self.replay['inherited_retrieval'], self.saved['inherited_retrieval'])
        invalid = [row for row in self.replay['rows'] if not row['output']['valid_utf8']]
        self.assertTrue(invalid)
        self.assertTrue(all(row['normalized'] == row['raw'] and not row['normalized_strict'] for row in invalid))


if __name__ == '__main__':
    unittest.main()

