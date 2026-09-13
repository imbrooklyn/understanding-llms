# SPDX-License-Identifier: Apache-2.0
"""One explicit CPU decoder block. Matrix rows are inputs, columns are outputs."""
import json
from pathlib import Path
import torch
from torch import nn
from tokenizer import BOS, EOS, PAD

ROOT = Path(__file__).resolve().parents[2]
DTYPE = torch.float64
IGNORE = -100


def config():
    return json.loads((ROOT / 'data/mini-gpt/config.json').read_text())


def parameter(rows, columns, std):
    return nn.Parameter(torch.randn(rows, columns, dtype=DTYPE) * std)


class RowNorm(nn.Module):
    def __init__(self, width, epsilon):
        super().__init__()
        self.scale = nn.Parameter(torch.ones(width, dtype=DTYPE))
        self.offset = nn.Parameter(torch.zeros(width, dtype=DTYPE))
        self.epsilon = epsilon

    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)
        variance = ((x - mean) ** 2).mean(dim=-1, keepdim=True)
        return (x - mean) / torch.sqrt(variance + self.epsilon) * self.scale + self.offset


class Block(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        c, f = cfg['width'], cfg['ffn_width']
        self.heads = cfg['heads']
        if c % self.heads:
            raise ValueError('width must be divisible by heads')
        self.norm1 = RowNorm(c, cfg['epsilon'])
        self.norm2 = RowNorm(c, cfg['epsilon'])
        self.wq, self.wk, self.wv, self.wo = (parameter(c, c, cfg['init_std']) for _ in range(4))
        self.w1 = parameter(c, f, cfg['init_std'])
        self.b1 = nn.Parameter(torch.zeros(f, dtype=DTYPE))
        self.w2 = parameter(f, c, cfg['init_std'])
        self.b2 = nn.Parameter(torch.zeros(c, dtype=DTYPE))

    def forward(self, x, valid, log):
        b, t, c = x.shape
        h, d = self.heads, c // self.heads
        n1 = log('norm1', self.norm1(x))
        q0, k0, v0 = (log(name, n1 @ w) for name, w in [('q_projection', self.wq), ('k_projection', self.wk), ('v_projection', self.wv)])
        q, k, v = (log(name, value.reshape(b, t, h, d).transpose(1, 2)) for name, value in [('q_heads', q0), ('k_heads', k0), ('v_heads', v0)])
        scores = log('scores', (q @ k.transpose(-1, -2)) / (d ** 0.5))
        causal = torch.arange(t)[:, None] >= torch.arange(t)[None, :]
        visible = log('visible', causal[None, None] & valid[:, None, None, :])
        active = valid[:, None, :, None]
        if torch.any(active & ~visible.any(dim=-1, keepdim=True)):
            raise ValueError('a valid query has no visible key')
        masked = scores.masked_fill(~visible, float('-inf'))
        safe = torch.where(active, masked, torch.zeros_like(masked))
        weights = log('weights', torch.where(active, torch.softmax(safe, dim=-1), torch.zeros_like(safe)))
        mixtures = log('mixtures', weights @ v)
        joined = log('joined', mixtures.transpose(1, 2).reshape(b, t, c))
        update = log('attention_output', joined @ self.wo)
        assert update.shape == x.shape
        r = log('residual1', x + update)
        n2 = log('norm2', self.norm2(r))
        pre = log('ffn_linear', n2 @ self.w1 + self.b1)
        hidden = log('ffn_relu', torch.relu(pre))
        ffn = log('ffn_output', hidden @ self.w2 + self.b2)
        assert ffn.shape == r.shape
        return log('block_output', r + ffn)


class MiniGPT(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = dict(cfg)
        c, v = cfg['width'], cfg['vocab_size']
        self.token_embedding = parameter(v, c, cfg['init_std'])
        self.position_embedding = parameter(cfg['context_length'], c, cfg['init_std'])
        self.block = Block(cfg)
        self.final_norm = RowNorm(c, cfg['epsilon'])
        self.lm_weight = parameter(c, v, cfg['init_std'])
        self.lm_bias = nn.Parameter(torch.zeros(v, dtype=DTYPE))

    def forward(self, ids, valid=None, targets=None, trace=False):
        if ids.ndim != 2 or ids.dtype != torch.long or ids.device.type != 'cpu':
            raise ValueError('ids must be a CPU long tensor [B,T]')
        b, t = ids.shape
        if b == 0 or t == 0 or t > self.cfg['context_length']:
            raise ValueError('empty input or context limit exceeded')
        if torch.any(ids < 0) or torch.any(ids >= self.cfg['vocab_size']):
            raise ValueError('token ID outside vocabulary')
        valid = torch.ones_like(ids, dtype=torch.bool) if valid is None else valid
        if valid.shape != ids.shape or valid.dtype != torch.bool:
            raise ValueError('valid must be Boolean [B,T]')
        values = {}
        def log(name, value):
            if trace:
                values[name] = value.detach().clone()
            return value
        token = log('token_embedding', self.token_embedding[ids])
        position = log('position_embedding', self.position_embedding[:t])
        x = log('block_input', token + position[None])
        y = self.block(x, valid, log)
        final = log('final_norm', self.final_norm(y))
        logits = log('logits', final @ self.lm_weight + self.lm_bias)
        assert logits.shape == (b, t, self.cfg['vocab_size'])
        loss = None
        if targets is not None:
            if targets.shape != ids.shape or targets.dtype != torch.long:
                raise ValueError('targets must be long [B,T]')
            if not torch.any(targets != IGNORE):
                raise ValueError('loss requires at least one scored target')
            if torch.any((targets != IGNORE) & ~valid):
                raise ValueError('invalid query cannot have a scored target')
            loss = torch.nn.functional.cross_entropy(logits.reshape(b * t, -1), targets.reshape(b * t), ignore_index=IGNORE)
        return logits, loss, values


def create_model(cfg):
    torch.set_num_threads(cfg['threads'])
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(cfg['init_seed'])
    return MiniGPT(cfg)


def batch_records(records, tokenizer, context):
    if not records:
        raise ValueError('batch needs at least one record')
    ids = torch.full((len(records), context), PAD, dtype=torch.long)
    targets = torch.full_like(ids, IGNORE)
    valid = torch.zeros_like(ids, dtype=torch.bool)
    for i, record in enumerate(records):
        tokens = [BOS] + tokenizer.encode(record['text']) + [EOS]
        count = len(tokens) - 1
        if count > context:
            raise ValueError('record exceeds context; no silent truncation')
        ids[i, :count] = torch.tensor(tokens[:-1])
        targets[i, :count] = torch.tensor(tokens[1:])
        valid[i, :count] = True
    return ids, valid, targets
