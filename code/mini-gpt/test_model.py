# SPDX-License-Identifier: Apache-2.0
import copy
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
import torch
from model import ROOT, config, create_model, batch_records, IGNORE
from tokenizer import load, PAD, EOS
from generate import generate
from run import checkpoint, restore, optimizer, identities, digest
sys.path.insert(0, str(ROOT / 'code/part-iv'))
import reference


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.cfg = config()
        self.tokenizer = load(ROOT)
        self.corpus = json.loads((ROOT / 'data/mini-gpt/corpus.json').read_text())
        self.model = create_model(self.cfg)
        self.batch = batch_records(self.corpus['train'][4:6], self.tokenizer, self.cfg['context_length'])

    def test_shift_eos_and_record_boundaries(self):
        ids, valid, targets = self.batch
        self.assertEqual(valid.sum(-1).tolist(), [15, 17])
        for b, record in enumerate(self.corpus['train'][4:6]):
            n = int(valid[b].sum())
            self.assertEqual(ids[b, 0], 256)
            self.assertEqual(targets[b, n - 1], EOS)
            self.assertEqual(ids[b, 1:n].tolist(), targets[b, :n - 1].tolist())
            self.assertTrue(torch.all(targets[b, n:] == IGNORE))
            self.assertEqual(self.tokenizer.decode(ids[b, 1:n].tolist()), record['text'])
        self.assertTrue(set(r['text'] for r in self.corpus['train']).isdisjoint(r['text'] for r in self.corpus['validation']))
        with self.assertRaisesRegex(ValueError, 'no silent truncation'):
            batch_records([{'text': 'z' * 100}], self.tokenizer, 64)

    def test_shapes_parameter_count_and_scalar_attention(self):
        logits, loss, trace = self.model(*self.batch[:2], targets=self.batch[2], trace=True)
        c, v, t, f = 16, 291, 64, 64
        expected_count = 2*v*c + t*c + 4*c*c + c*f+f + f*c+c + 3*2*c + v
        self.assertEqual(sum(p.numel() for p in self.model.parameters()), expected_count)
        self.assertEqual(expected_count, 13875)
        self.assertEqual(tuple(logits.shape), (2, 64, 291))
        q, k, value = (trace[x][0, 0, :15].tolist() for x in ('q_heads','k_heads','v_heads'))
        expected = reference.attention(q, k, value, [[j<=i for j in range(15)] for i in range(15)])
        torch.testing.assert_close(trace['mixtures'][0, 0, :15], torch.tensor(expected, dtype=torch.float64), atol=1e-12, rtol=0)
        self.assertTrue(torch.isfinite(loss))

    def test_uniform_loss_and_ignored_targets(self):
        with torch.no_grad():
            self.model.lm_weight.zero_(); self.model.lm_bias.zero_()
        _, loss, _ = self.model(*self.batch[:2], targets=self.batch[2])
        self.assertAlmostEqual(float(loss.detach()), math.log(291), places=12)
        targets = self.batch[2].clone(); targets[:, 1:] = IGNORE
        _, short, _ = self.model(*self.batch[:2], targets=targets)
        self.assertAlmostEqual(float(short.detach()), math.log(291), places=12)
        with self.assertRaisesRegex(ValueError, 'at least one'):
            self.model(*self.batch[:2], targets=torch.full_like(targets, IGNORE))

    def test_causal_prefix_and_padding_and_batch_independence(self):
        ids, valid, _ = self.batch
        original = self.model(ids, valid)[0].detach()
        changed = ids.clone(); changed[:, 8:] = 65
        altered = self.model(changed, valid)[0].detach()
        torch.testing.assert_close(original[:, :8], altered[:, :8], atol=1e-12, rtol=0)
        changed = ids.clone(); changed[~valid] = 255
        padded = self.model(changed, valid)[0].detach()
        torch.testing.assert_close(original[valid], padded[valid], atol=1e-12, rtol=0)
        one = self.model(ids[:1, :15])[0].detach()
        torch.testing.assert_close(original[:1, :15], one, atol=1e-12, rtol=0)

    def test_backward_reaches_the_block_and_update(self):
        before = self.model.block.wq.detach().clone()
        opt = optimizer(self.model, self.cfg)
        loss = self.model(*self.batch[:2], targets=self.batch[2])[1]
        loss.backward()
        for name in ['token_embedding','block.wq','block.wk','block.wv','block.w1','block.w2','lm_weight']:
            p = dict(self.model.named_parameters())[name]
            self.assertTrue(torch.isfinite(p.grad).all(), name)
            self.assertGreater(float(p.grad.abs().sum()), 0, name)
        opt.step()
        self.assertFalse(torch.equal(before, self.model.block.wq))

    def test_checkpoint_next_update_and_identity_guard(self):
        opt = optimizer(self.model, self.cfg)
        rng = torch.Generator().manual_seed(101)
        def update(m, o):
            o.zero_grad(set_to_none=True)
            m(*self.batch[:2], targets=self.batch[2])[1].backward(); o.step()
        update(self.model, opt)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'resume.pt'
            torch.save(checkpoint(self.model, opt, rng, 1, identities(self.cfg,self.tokenizer,self.corpus)),path)
            update(self.model,opt)
            restored, ropt, rrng, step = restore(path,self.cfg,self.tokenizer,self.corpus)
            self.assertEqual(step,1)
            update(restored,ropt)
            self.assertEqual(digest(restored.state_dict()),digest(self.model.state_dict()))
            self.assertEqual(digest(ropt.state_dict()),digest(opt.state_dict()))
            changed=copy.deepcopy(self.corpus);changed['train'][0]['text']+='!'
            with self.assertRaisesRegex(ValueError,'identity mismatch'):
                restore(path,self.cfg,self.tokenizer,changed)

    def test_generation_stops_bytes_and_seed(self):
        with torch.no_grad():
            self.model.lm_weight.zero_();self.model.lm_bias.fill_(-100);self.model.lm_bias[EOS]=100
        self.assertEqual(generate(self.model,self.tokenizer,'')['stop'],'EOS')
        with torch.no_grad():
            self.model.lm_bias.fill_(-100);self.model.lm_bias[65]=100
        limited=generate(self.model,self.tokenizer,'',max_new=2)
        self.assertEqual((limited['completion'],limited['stop']),('AA','max_new_tokens'))
        self.assertEqual(generate(self.model,self.tokenizer,'z'*63)['stop'],'context_limit')
        with torch.no_grad():
            self.model.lm_bias[65]=-100;self.model.lm_bias[255]=100
        invalid=generate(self.model,self.tokenizer,'',max_new=1)
        self.assertFalse(invalid['valid_utf8']);self.assertEqual(invalid['generated_hex'],'ff')
        self.assertEqual(invalid['display_decode'],'replace')
        a=generate(self.model,self.tokenizer,'',mode='sample',seed=7,max_new=3)
        b=generate(self.model,self.tokenizer,'',mode='sample',seed=7,max_new=3)
        self.assertEqual(a,b)

    def test_text_prefix_is_not_always_a_token_prefix(self):
        full=self.tokenizer.encode(self.corpus['train'][4]['text'])
        prompt=self.corpus['diagnostics'][0]['prompt']
        short=self.tokenizer.encode(prompt);aligned=self.tokenizer.encode(prompt+' ')
        self.assertNotEqual(short,full[:len(short)])
        self.assertEqual(aligned,full[:len(aligned)])
        self.assertEqual((short[-1],aligned[-1]),(58,259))

    def test_invalid_shapes_and_context(self):
        with self.assertRaisesRegex(ValueError,'long tensor'):
            self.model(torch.zeros(2,4))
        with self.assertRaisesRegex(ValueError,'context limit'):
            self.model(torch.zeros(1,65,dtype=torch.long))
        with self.assertRaisesRegex(ValueError,'outside vocabulary'):
            self.model(torch.tensor([[291]],dtype=torch.long))


if __name__ == '__main__':
    unittest.main()
