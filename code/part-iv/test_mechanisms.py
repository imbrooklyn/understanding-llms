# SPDX-License-Identifier: Apache-2.0
import json
import math
from pathlib import Path
import unittest
import numpy as np
import torch
from mechanisms import projected_attention, masked_softmax, two_heads, layer_norm, residual, small_block
import reference

ROOT = Path(__file__).resolve().parents[2]
A = json.loads((ROOT / 'data/part-iv/attention.json').read_text())
M = json.loads((ROOT / 'data/part-iv/mask-cases.json').read_text())


class MechanismTests(unittest.TestCase):
    def setUp(self):
        self.trace = projected_attention(*(A[k] for k in ('X', 'WQ', 'WK', 'WV')))

    def test_every_hand_element(self):
        for key, expected in A['expected'].items():
            np.testing.assert_allclose(self.trace[key], expected, atol=1e-12, rtol=0)
        x = A['X']
        for role in ('Q', 'K', 'V'):
            np.testing.assert_allclose(self.trace[role], reference.matmul(x, A['W' + role]), atol=0, rtol=0)

    def test_value_change_and_convex_bounds(self):
        weights = self.trace['weights']
        np.testing.assert_allclose(weights.sum(-1), 1, atol=1e-15)
        np.testing.assert_allclose(weights @ (self.trace['V'] + [2, -1]), self.trace['output'] + [2, -1], atol=1e-12)
        np.testing.assert_array_equal(weights @ np.zeros((3, 2)), np.zeros((3, 2)))
        self.assertTrue(np.all(self.trace['output'] >= self.trace['V'].min(0)))
        self.assertTrue(np.all(self.trace['output'] <= self.trace['V'].max(0)))

    def test_causal_and_padding(self):
        a = masked_softmax(self.trace['scores'], M['causal'])
        np.testing.assert_allclose(a, M['causal_expected_weights'], atol=1e-12, rtol=0)
        np.testing.assert_allclose(a @ self.trace['V'], M['causal_expected_output'], atol=1e-12, rtol=0)
        padded = masked_softmax(self.trace['scores'], M['causal_with_padding'], M['query_valid'])
        np.testing.assert_allclose(padded @ self.trace['V'], M['padded_expected_output'], atol=1e-12, rtol=0)
        with self.assertRaisesRegex(ValueError, 'no visible key'):
            masked_softmax(np.zeros((3, 3)), np.tril(np.ones((3, 3)), -1))
        zeros = masked_softmax(np.zeros((1, 3)), np.zeros((1, 3)), [False])
        np.testing.assert_array_equal(zeros, [[0, 0, 0]])

    def test_future_perturbation_and_bad_masks(self):
        changed = np.array(A['X'], dtype=float)
        changed[2] = [9, -7]
        alt = projected_attention(changed, A['WQ'], A['WK'], A['WV'])
        def result(t, mask):
            return masked_softmax(t['scores'], mask) @ t['V']
        correct = result(self.trace, M['causal'])
        np.testing.assert_allclose(correct[:2], result(alt, M['causal'])[:2], atol=1e-12)
        for wrong in (np.ones((3, 3)), np.triu(np.ones((3, 3)))):
            self.assertGreater(np.max(np.abs(result(self.trace, wrong)[:2] - result(alt, wrong)[:2])), 0.1)

    def test_leakage_oracle(self):
        leak = M['leakage']
        for target, future in enumerate(leak['future_values']):
            v = np.array([leak['current_value'], future])
            for mask, name in [([[True, True]], 'future_visible'), ([[True, False]], 'future_hidden')]:
                p = (masked_softmax([[0, math.log(99)]], mask) @ v)[0, target]
                self.assertAlmostEqual(p, leak[name + '_probability'], places=14)
                self.assertAlmostEqual(-math.log(p), leak[name + '_loss'], places=14)

    def test_multihead_order_and_projection(self):
        t = two_heads(A['X'])
        np.testing.assert_allclose(t['output'], M['multihead_expected'], atol=1e-12)
        wo = np.array(M['output_projection'])
        np.testing.assert_allclose(t['joined'][:, ::-1] @ wo[::-1], t['output'], atol=1e-12)
        self.assertFalse(np.allclose(t['joined'][:, ::-1] @ wo, t['output']))

    def test_library_mask_conventions(self):
        q, k, v = (torch.tensor(self.trace[key], dtype=torch.float64)[None, None] for key in ('Q', 'K', 'V'))
        visible = torch.tensor(M['causal'])
        actual = torch.nn.functional.scaled_dot_product_attention(q, k, v, attn_mask=visible, dropout_p=0)
        np.testing.assert_allclose(actual[0, 0].numpy(), M['causal_expected_output'], atol=1e-12)
        module = torch.nn.MultiheadAttention(2, 1, bias=False, batch_first=True, dtype=torch.float64)
        with torch.no_grad():
            module.in_proj_weight.copy_(torch.cat([torch.eye(2, dtype=torch.float64)] * 3))
            module.out_proj.weight.copy_(torch.eye(2, dtype=torch.float64))
        actual, _ = module(q[0], k[0], v[0], attn_mask=~visible)
        np.testing.assert_allclose(actual.detach().numpy()[0], M['causal_expected_output'], atol=1e-12)

    def test_norm_and_residual_semantics(self):
        x = np.array([[1., 3.], [10., 10.]])
        np.testing.assert_allclose(layer_norm(x), [reference.norm(row) for row in x], atol=1e-12)
        np.testing.assert_array_equal(layer_norm(x)[1], [0, 0])
        np.testing.assert_allclose(layer_norm(x), torch.nn.LayerNorm(2, dtype=torch.float64)(torch.tensor(x)).detach().numpy(), atol=1e-12)
        with self.assertRaisesRegex(ValueError, 'exactly'):
            residual(x, np.zeros((1, 2)))

    def test_block_scalar_path_and_prefix(self):
        x = np.array(A['X']) + [[0, 0], [0, 1], [1, 0]]
        out = small_block(x)['output']
        np.testing.assert_allclose(out, reference.block(x.tolist()), atol=1e-12, rtol=0)
        x[2] = [-7, 4]
        np.testing.assert_allclose(out[:2], small_block(x)['output'][:2], atol=1e-12)

    def test_position_free_equivariance(self):
        perm = [2, 0, 1]
        alt = projected_attention(np.array(A['X'])[perm], A['WQ'], A['WK'], A['WV'])
        np.testing.assert_allclose(alt['output'], self.trace['output'][perm], atol=1e-12)
        wrong = projected_attention(np.array(A['X'])[perm] + [[0, 0], [0, 1], [1, 0]], A['WQ'], A['WK'], A['WV'])
        original = projected_attention(np.array(A['X']) + [[0, 0], [0, 1], [1, 0]], A['WQ'], A['WK'], A['WV'])
        self.assertFalse(np.allclose(wrong['output'], original['output'][perm]))


if __name__ == '__main__':
    unittest.main()
