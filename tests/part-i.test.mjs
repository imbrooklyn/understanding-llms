// SPDX-License-Identifier: Apache-2.0
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { tokenize, cosine, journey, trainNgram, contextFor, distribution, scoreSequence, generate, lcg32, sampleIndex } from '../code/part-i/core.ts';
import remarkBook, { renderFigure } from '../src/plugins/remark-book.mjs';
const read = (path) => JSON.parse(readFileSync(new URL(path, import.meta.url), 'utf8'));
const expected = read('../data/part-i/expected.json');
const near = (actual, value) => assert.ok(Math.abs(actual - value) < 1e-12, `${actual} != ${value}`);

test('bilingual tokenization, round trip, version change and unknown failure match independent fixtures', () => {
  for (const item of expected.tokenizer) {
    const result = tokenize(item.input, item.version);
    assert.deepEqual(result.ids, item.ids); assert.equal(result.decoded, item.decoded); assert.equal(result.unknown, item.unknown);
  }
  assert.deepEqual(tokenize('').ids, []);
  assert.equal(tokenize('🙂🙂').unknown, 2);
  assert.notDeepEqual(tokenize('The').ids, tokenize('the').ids);
  assert.equal(tokenize('  ').decoded, '  ');
  assert.throws(() => tokenize('cats', 'missing'), RangeError);
});
test('cosine distinguishes geometry, opposite direction and undefined zero vector', () => {
  near(cosine([1,0], [1,1]).similarity, expected.cosines[0]);
  assert.equal(cosine([1,0], [-1,0]).similarity, -1);
  assert.equal(cosine([1,0], [0,0]).similarity, null);
  assert.equal(cosine([1,0], [2,0]).similarity, 1);
  assert.throws(() => cosine([1], [1,0]), RangeError);
});
test('all six scenarios preserve parameters/context/external/state distinctions', () => {
  const ids = ['old', 'file', 'context', 'saved', 'selected', 'parameters'];
  ids.forEach((id, i) => assert.deepEqual(journey(id).probabilities, expected.journey_probabilities[i]));
  assert.equal(journey('file').context, journey('old').context);
  assert.equal(journey('context').parameters, journey('old').parameters);
  assert.notEqual(journey('file').external, journey('old').external);
});
test('Bigram counts include EOS, exclude predicted BOS, and never cross sequence boundaries', () => {
  const model = trainNgram(2);
  assert.equal(model.events, 9);
  for (const [h, counts] of Object.entries(expected.bigram_rows)) assert.deepEqual(model.rows[JSON.stringify([h])], counts);
  assert.equal(Object.keys(model.rows).length, 4);
  assert.equal(model.vocabulary.includes('BOS'), false);
  assert.equal(model.rows['["EOS"]'], undefined);
  assert.equal(Object.values(trainNgram(1).rows)[0].reduce((a,b) => a+b), 9);
  assert.deepEqual(trainNgram(3).rows['["BOS","BOS"]'], [3,0,0,0]);
  assert.throws(() => trainNgram(0), RangeError);
  assert.throws(() => trainNgram(2, ['ad']), RangeError);
});
test('normalization, add-one denominators, zero transitions, and unseen context are distinct', () => {
  for (const n of [1,2,3]) for (const alpha of [0,1]) {
    const model = trainNgram(n);
    for (const h of Object.keys(model.rows)) near(distribution(model, JSON.parse(h), alpha).probabilities.reduce((a,b) => a+b), 1);
  }
  assert.equal(distribution(trainNgram(2), ['a'], 0).probabilities[0], 0);
  assert.equal(distribution(trainNgram(2), ['a'], 1).denominator, 7);
  assert.equal(distribution(trainNgram(3), ['a','a'], 0).probabilities, null);
  assert.deepEqual(distribution(trainNgram(3), ['a','a'], 1).probabilities, [0.25,0.25,0.25,0.25]);
  assert.equal(scoreSequence(trainNgram(3), 'aa', 0).probability, 0);
  assert.equal(scoreSequence(trainNgram(3), 'aa', 0).factors.at(-1).probability, null);
});
test('all six held-out comparisons and complete-sequence calculations match hand fractions', () => {
  for (const row of expected.held_out) for (const text of ['ac','aa']) near(scoreSequence(trainNgram(row.n), text, row.alpha).probability, row[text]);
  near(scoreSequence(trainNgram(2), 'ab', 1).probability, 6/49);
  near(scoreSequence(trainNgram(2), '', 1).probability, 1/7);
  assert.equal(scoreSequence(trainNgram(2), '', 0).probability, 0);
  assert.throws(() => scoreSequence(trainNgram(2), 'ad', 0), RangeError);
});
test('generation matches frozen PRNG trace and cannot train on its output', () => {
  const model = trainNgram(2), before = structuredClone(model);
  const result = generate(model, 0, 42);
  assert.equal(result.text, expected.generation.text);
  assert.equal(result.stop, 'eos'); assert.deepEqual(result.tokens, expected.generation.tokens);
  result.trace.forEach((step, i) => near(step.draw, expected.generation.draws[i]));
  assert.deepEqual(generate(model, 0, 42), result);
  scoreSequence(model, 'aa', 1); assert.deepEqual(model, before);
  assert.equal(generate(model, 0, 42, 1).stop, 'limit');
  assert.equal(generate(trainNgram(2, []), 0, 42).stop, 'undefined');
  assert.throws(() => lcg32(-1), RangeError); assert.throws(() => lcg32(0.5), RangeError);
  assert.equal(sampleIndex([0.6,0.4], 0.6), 1);
  assert.equal(sampleIndex([0,1,0], 0), 1);
});
test('changing unseen earlier prefixes cannot change identical selected context distributions', () => {
  const model = trainNgram(3);
  const a = distribution(model, contextFor(['a','b','b'], 3), 1), b = distribution(model, contextFor(['c','b','b'], 3), 1);
  assert.deepEqual(a, b);
});
test('heading numbers and anchors agree across languages, reset subsections, and skip nonchapters', () => {
  const source = () => ({ children: [2,3,3,2,3].map((depth) => ({type:'heading', depth, children:[{type:'text',value:'Heading'}]})) });
  for (const locale of ['en', 'zh-hans']) {
    const tree = source(); remarkBook()(tree, {path:`/content/${locale}/ch-03.md`});
    assert.deepEqual(tree.children.map((n) => n.children[0].value), ['3.1 ','3.1.1 ','3.1.2 ','3.2 ','3.2.1 ']);
    assert.equal(tree.children[0].data.hProperties.id, 's-3-1');
  }
  const tree=source(); remarkBook()(tree, {path:'/content/en/about.md'}); assert.equal(tree.children[0].children[0].value, 'Heading');
  assert.throws(() => remarkBook()({children:[{type:'heading',depth:1,children:[]}]}, {path:'/en/ch-01.md'}));
});
test('all diagrams render localized descriptions, licensed captions and worked evidence', () => {
  for (const id of ['ch-01/model-system','ch-02/token-journey','ch-02/two-timelines','ch-03/lookup','ch-03/cosine','ch-04/count-predict']) for (const locale of ['en','zh-hans']) {
    const html = renderFigure(id, locale);
    assert.match(html, /role="img" aria-label="[^"]+"/); assert.match(html, /<figcaption>/); assert.match(html, /CC BY-SA 4.0/);
    assert.ok(html.includes('<strong>') || html.includes('<svg'));  assert.equal(html.includes('undefined'), false);
    if(id === 'ch-03/lookup') { assert.match(html, /16/); assert.match(html, /\[1, 0\]/); }
    if(id === 'ch-04/count-predict') { assert.match(html, /b: 2 \/ 3/); assert.match(html, /c: 1 \/ 3/); }
  }
});


test('textbook transfer exercises agree with independent fractions and preserve fitting boundaries', () => {
  assert.deepEqual(tokenize('cats cats').ids, [16,17,15,16,17]);
  assert.deepEqual(tokenize('cats cats', 'toy-longest-v2').ids, [18,15,18]);
  assert.deepEqual(tokenize('Thecat').ids, [1,16]);
  assert.deepEqual(tokenize('thecat').ids, [0,0,0,16]);
  assert.deepEqual(tokenize('cat🙂').ids, tokenize('cat🚀').ids);
  near(cosine([1,0], [3,3]).similarity, 1 / Math.sqrt(2));
  near(cosine([1,0], [-3,-3]).similarity, -1 / Math.sqrt(2));
  const changed = trainNgram(2, ['ab','ac','ac']);
  assert.deepEqual(changed.rows['["a"]'], [0,1,2,0]);
  near(scoreSequence(changed, 'ac', 0).probability, 2/3);
  const addedAA = trainNgram(2, ['ab','ab','ac','aa']);
  assert.deepEqual(addedAA.rows['["a"]'], [1,2,1,1]);
  near(scoreSequence(addedAA, 'aa', 0).probability, 1/25);
  const addedABA = trainNgram(2, ['ab','ab','ac','aba']);
  assert.equal(addedABA.events, 13);
  assert.deepEqual(addedABA.rows['["a"]'], [0,3,1,1]);
  assert.deepEqual(addedABA.rows['["b"]'], [1,0,0,2]);
  near(scoreSequence(addedABA, 'aba', 0).probability, 1/25);
  const draw = lcg32(42);
  assert.deepEqual([draw(),draw(),draw()].map((n) => n * 2**32), [1083814273,378494188,2479403867]);
});

test('removed learning-control syntax fails authoring instead of silently hiding content', () => {
  assert.throws(() => remarkBook()({children:[{type:'code',lang:'book-lab',value:'tokens'}]}, {path:'/en/ch-03.md'}), /static/);
});
