# SPDX-License-Identifier: Apache-2.0
"""Independent fractions, polynomial sensitivity, and observable sequence failures."""
import copy
from fractions import Fraction
import json
import math
import unittest
from core import ROOT, attend, encode, fixture, generate, results, rnn_log, scalar_bptt, window_log


class SequenceEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = fixture()
        cls.actual = results(cls.data)
        cls.expected = json.loads((ROOT / 'data/part-iii/expected.json').read_text())

    def close_rows(self, actual, expected):
        self.assertEqual(len(actual), len(expected))
        for left, right in zip(actual, expected):
            self.assertEqual(len(left), len(right))
            for a, b in zip(left, right):
                self.assertAlmostEqual(a, b, places=12)

    def test_three_steps_and_input_independence(self):
        for actual, expected in zip(self.actual['short_rnn'], self.expected['short_states']):
            self.close_rows([row['state'] for row in actual], expected)
            self.assertEqual(actual[0]['previous'], [0, 0])
            self.assertEqual(actual[1]['previous'], actual[0]['state'])
        self.assertEqual([rows[-1]['choice'] for rows in self.actual['short_rnn']], [0, 1])
        settings = copy.deepcopy(self.data['rnn'])
        rnn_log([1, 3, 4], settings)
        self.assertEqual(settings, self.data['rnn'])

    def test_same_task_two_different_failures(self):
        red, blue = self.actual['long_rnn']
        self.assertEqual(red[-1]['state'], [float(Fraction(1, 256)), 0])
        self.assertEqual(blue[-1]['state'], [0, float(Fraction(1, 256))])
        self.assertNotEqual(red[-1]['probabilities'], blue[-1]['probabilities'])
        self.assertEqual([red[-1]['choice'], blue[-1]['choice']], [0, 0])
        left, right = self.actual['window']
        self.assertEqual(left, right)
        self.assertGreater(blue[-1]['state'][1], 0)

    def test_tie_boundary_and_retention_change(self):
        settings = copy.deepcopy(self.data['rnn'])
        self.assertEqual(rnn_log([1, 3, 4], settings)[-1]['choice'], 1)
        tied = rnn_log([1, 2, 3, 4], settings)[-1]
        self.assertEqual(tied['logits'], [.125, .125])
        self.assertEqual(tied['choice'], 0)
        settings['recurrent_weight'] = [[1, 0], [0, 1]]
        self.assertEqual(rnn_log(self.data['long_task']['prefix_ids'][1], settings)[-1]['choice'], 1)
        self.assertEqual(rnn_log([1, 1, 1], settings)[-1]['state'], [0, 3])

    def test_bptt_against_closed_polynomial_and_difference(self):
        actual = self.actual['bptt']
        for key in ['state_gradients', 'weight_contributions', 'weight_gradient', 'loss']:
            self.assertEqual(actual[key], self.expected[key])
        for weight in [.2, .5, .8, 1.2]:
            gradient = scalar_bptt([1, 0, 0], weight, 1)['weight_gradient']
            self.assertAlmostEqual(gradient, 2 * weight * (weight ** 2 - 1), places=12)
            delta = 1e-6
            polynomial = lambda w: .5 * (w * w - 1) ** 2
            difference = (polynomial(weight + delta) - polynomial(weight - delta)) / (2 * delta)
            self.assertAlmostEqual(gradient, difference, places=8)
        self.assertAlmostEqual(self.actual['after_update']['loss'], self.expected['updated_loss'])
        self.assertLess(self.actual['after_update']['loss'], actual['loss'])

    def test_products_and_gate_arithmetic(self):
        for row in self.actual['distance_products']:
            self.assertEqual(row['contracting'], float(Fraction(1, 2) ** row['edges']))
            self.assertEqual(row['expanding'], float(Fraction(3, 2) ** row['edges']))
        gates = self.actual['gates']
        self.assertAlmostEqual(gates['lstm_cell'], float(Fraction(41, 50)))
        self.assertAlmostEqual(gates['lstm_hidden'], .5063024061289558)
        self.assertAlmostEqual(gates['gru_hidden'], .7397375320224904)
        self.assertLess(gates['retention_099_hundred_edges'], .37)

    def test_computed_encoder_collision(self):
        scale = math.log(2)
        for key, expected_key in [('encoder', 'encoder_states_in_units_of_ln2'), ('contrast_encoder', 'contrast_states_in_units_of_ln2')]:
            self.close_rows([row['state'] for row in self.actual[key]], [[scale * x for x in row] for row in self.expected[expected_key]])
        self.assertEqual(self.actual['encoder'][-1]['state'], self.actual['contrast_encoder'][-1]['state'])
        self.assertNotEqual(self.actual['encoder'][0]['state'], self.actual['contrast_encoder'][0]['state'])

    def test_teacher_generation_divergence_and_eos(self):
        teacher = self.actual['teacher']
        generated = self.actual['generation']
        self.assertEqual([row['input'] for row in teacher], self.expected['teacher_inputs'])
        self.assertEqual([row['target'] for row in teacher], self.expected['teacher_targets'])
        self.assertEqual([row['output'] for row in generated['trace']], self.expected['generated_outputs'])
        self.assertEqual([row['input'] for row in generated['trace']], self.expected['generated_inputs'])
        self.assertTrue(generated['stopped_at_eos'])
        self.assertEqual(teacher[0]['greedy'], 'blue')
        self.assertEqual(teacher[1]['input'], 'red')
        self.assertAlmostEqual(self.actual['target_sequence_probability'], float(Fraction(36, 125)))
        capped = copy.deepcopy(self.data['translation'])
        capped['max_steps'] = 2
        self.assertFalse(generate(capped)['stopped_at_eos'])

    def test_attention_exact_oracles_and_interventions(self):
        scale = math.log(2)
        for key, expected_key in [('attention', 'contexts_in_units_of_ln2'), ('slot_deletions', 'slot_contexts_in_units_of_ln2'), ('source_deletions', 'source_contexts_in_units_of_ln2')]:
            self.close_rows([row['context'] for row in self.actual[key]], [[scale * x for x in row] for row in self.expected[expected_key]])
        self.close_rows([row['weights'] for row in self.actual['attention']], self.expected['attention_weights'])
        self.close_rows([row['weights'] for row in self.actual['slot_deletions']], self.expected['slot_weights'])
        for key, expected_key in [('slot_deletions', 'slot_readouts_in_units_of_ln2'), ('source_deletions', 'source_readouts_in_units_of_ln2')]:
            for row, target in zip(self.actual[key], self.expected[expected_key]):
                self.assertAlmostEqual(row['readout'], scale * target)
        self.assertNotEqual(self.actual['slot_deletions'][1]['context'], self.actual['source_deletions'][1]['context'])

    def test_attention_invariants_and_invalid_memory(self):
        memory = [[math.log(2), 0], [0, math.log(2)], [0, 0]]
        original = attend([1, 0], memory)
        shifted = attend([1, 0], [[row[0] + 1000, row[1]] for row in memory])
        self.close_rows([shifted['weights']], [original['weights']])
        self.close_rows([attend([0, 0], memory)['weights']], [[1/3, 1/3, 1/3]])
        self.assertEqual(attend([1, 0], memory, [1])['context'], memory[1])
        for keep in [[], [0, 0], [3], [-1]]:
            with self.assertRaises(ValueError):
                attend([1, 0], memory, keep)
        with self.assertRaises(ValueError):
            attend([1], memory)


if __name__ == '__main__':
    unittest.main()
