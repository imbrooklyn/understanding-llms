// SPDX-License-Identifier: Apache-2.0
// Shared by both languages, the browser, and the verification suite.
import tokenData from '../../data/part-i/tokenizer.json' with { type: 'json' };
import ngramData from '../../data/part-i/ngram.json' with { type: 'json' };
import journeyData from '../../data/part-i/journey.json' with { type: 'json' };

export type TokenizerVersion = keyof typeof tokenData.versions;
export function tokenize(input: string, version: TokenizerVersion = 'toy-longest-v1') {
  const vocabulary = tokenData.versions[version];
  if (!vocabulary) throw new RangeError('Unknown tokenizer version');
  const candidates = vocabulary.pieces.map((piece, id) => ({ piece, id }))
    .filter(({ id }) => id !== 0).sort((a, b) => b.piece.length - a.piece.length);
  const tokens: { text: string; piece: string; id: number; vector: number[] }[] = [];
  let remaining = input;
  while (remaining.length) {
    const match = candidates.find(({ piece }) => remaining.startsWith(piece));
    const raw = match?.piece ?? Array.from(remaining)[0]!;
    const id = match?.id ?? 0;
    tokens.push({ text: raw, piece: vocabulary.pieces[id]!, id, vector: [...vocabulary.embeddings[id]!] });
    remaining = remaining.slice(raw.length);
  }
  return { input, version, tokens, ids: tokens.map((token) => token.id),
    decoded: tokens.map((token) => token.piece).join(''),
    unknown: tokens.filter((token) => token.id === 0).length };
}

export function cosine(u: number[], v: number[]) {
  if (u.length !== 2 || v.length !== 2 || ![...u, ...v].every(Number.isFinite)) throw new RangeError('Expected two finite 2D vectors');
  const dot = u[0]! * v[0]! + u[1]! * v[1]!;
  const lengths = [Math.hypot(...u), Math.hypot(...v)];
  const denominator = lengths[0]! * lengths[1]!;
  return { u, v, dot, lengths, similarity: denominator === 0 ? null : dot / denominator };
}

export function journey(id: string) {
  const scenario = journeyData.scenarios.find((item) => item.id === id);
  if (!scenario) throw new RangeError('Unknown journey scenario');
  const table = journeyData.tables[scenario.parameters as keyof typeof journeyData.tables];
  const probabilities = table[scenario.context as keyof typeof table];
  return { ...scenario, probabilities: [...probabilities] };
}

export type NgramModel = { n: number; vocabulary: string[]; rows: Record<string, number[]>; events: number };
const key = (context: string[]) => JSON.stringify(context);
export function contextFor(prefix: string[], n: number): string[] {
  if (![1, 2, 3].includes(n)) throw new RangeError('Order must be 1, 2, or 3');
  return n === 1 ? [] : [...Array(n - 1).fill(ngramData.bos), ...prefix].slice(-(n - 1));
}
export function trainNgram(n: number, strings: string[] = ngramData.train): NgramModel {
  contextFor([], n);
  const vocabulary = [...ngramData.vocabulary];
  const rows: Record<string, number[]> = {};
  let events = 0;
  for (const text of strings) {
    const characters = Array.from(text);
    if (characters.some((token) => !vocabulary.slice(0, -1).includes(token))) throw new RangeError('Training text must use a, b, c');
    const prefix: string[] = [];
    for (const token of [...characters, ngramData.eos]) {
      const rowKey = key(contextFor(prefix, n));
      const row = rows[rowKey] ??= Array(vocabulary.length).fill(0);
      row[vocabulary.indexOf(token)]!++;
      prefix.push(token);
      events++;
    }
  }
  return { n, vocabulary, rows, events };
}
export function distribution(model: NgramModel, context: string[], alpha: number) {
  if (![0, 1].includes(alpha)) throw new RangeError('Smoothing must be 0 or 1');
  if (context.length !== model.n - 1) throw new RangeError('Context length must be N-1');
  const counts = [...(model.rows[key(context)] ?? Array(model.vocabulary.length).fill(0))];
  const total = counts.reduce((sum, count) => sum + count, 0);
  const denominator = total + alpha * model.vocabulary.length;
  const probabilities = denominator === 0 ? null : counts.map((count) => (count + alpha) / denominator);
  return { context: [...context], counts, total, alpha, denominator, probabilities };
}
export function scoreSequence(model: NgramModel, text: string, alpha: number) {
  const tokens = [...Array.from(text), ngramData.eos];
  if (tokens.some((token) => !model.vocabulary.includes(token))) throw new RangeError('Evaluation text must use a, b, c');
  const prefix: string[] = [];
  let probability: number | null = 1;
  const factors = tokens.map((token) => {
    const row = distribution(model, contextFor(prefix, model.n), alpha);
    const p = row.probabilities?.[model.vocabulary.indexOf(token)] ?? null;
    // A zero-probability prefix remains impossible even when a later row is undefined.
    if (p === 0 || probability === 0) probability = 0;
    else if (p === null || probability === null) probability = null;
    else probability *= p;
    prefix.push(token);
    return { context: row.context, token, probability: p };
  });
  return { text, probability, factors };
}
export function lcg32(seed: number) {
  if (!Number.isInteger(seed) || seed < 0 || seed > 0xffffffff) throw new RangeError('Seed must be an unsigned 32-bit integer');
  let state = seed >>> 0;
  return () => { state = (Math.imul(1664525, state) + 1013904223) >>> 0; return state / 4294967296; };
}
export function sampleIndex(probabilities: number[], draw: number) {
  if (draw < 0 || draw >= 1 || !Number.isFinite(draw)) throw new RangeError('Draw must be in [0,1)');
  const sum = probabilities.reduce((a, b) => a + b, 0);
  if (Math.abs(sum - 1) > 1e-10 || probabilities.some((p) => p < 0 || !Number.isFinite(p))) throw new RangeError('Invalid probability distribution');
  let cumulative = 0;
  for (let i = 0; i < probabilities.length; i++) {
    cumulative += probabilities[i]!;
    if (draw < cumulative) return i;
  }
  return probabilities.findLastIndex((p) => p > 0);
}
export function generate(model: NgramModel, alpha: number, seed = 42, maxDraws = 12) {
  if (!Number.isInteger(maxDraws) || maxDraws < 1 || maxDraws > 100) throw new RangeError('Invalid draw limit');
  const random = lcg32(seed);
  const prefix: string[] = [];
  const trace: { context: string[]; draw: number; token: string; probability: number }[] = [];
  let stop: 'eos' | 'limit' | 'undefined' = 'limit';
  for (let step = 0; step < maxDraws; step++) {
    const row = distribution(model, contextFor(prefix, model.n), alpha);
    if (!row.probabilities) { stop = 'undefined'; break; }
    const draw = random();
    const index = sampleIndex(row.probabilities, draw);
    const token = model.vocabulary[index]!;
    trace.push({ context: row.context, draw, token, probability: row.probabilities[index]! });
    if (token === ngramData.eos) { stop = 'eos'; break; }
    prefix.push(token);
  }
  return { seed, maxDraws, text: prefix.join(''), tokens: trace.map((step) => step.token), stop, trace };
}
