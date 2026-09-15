// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { renderFigure } from '../src/plugins/remark-book.mjs';
import { assertPublicationState } from './publication-state.mjs';
const root = new URL('../', import.meta.url);
const read = name => readFileSync(new URL(name, root), 'utf8');
const json = name => JSON.parse(read(name));
const hash = name => createHash('sha256').update(readFileSync(new URL(name, root))).digest('hex');
const locales = ['en','zh-hans'];
const ids = [...Array.from({length:7},(_,i)=>`ch-${i+40}`),'primer-http'];
const contract = {
  'ch-40':['128-20-12-8-8-24=56','ka2-context-v1','1,200'],
  'ch-41':['ka-answer-v1','additionalProperties','schema_version','max_tokens'],
  'ch-42':['A-104','B-205','orders:read:own','0.45'],
  'ch-43':['2026-07-28','clientCapabilities','structuredContent','-32602'],
  'ch-44':['1.574906','0.173765','0.953866','8/9'],
  'ch-45':['591','348','502','346','conflicting_evidence','local-extractive-v1'],
  'ch-46':['7/12','8/12','144','562','0.25'],
  'primer-http':['Retry-After','0.02','0.15','BOOK_DEMO_KEY','complete']
};
for (const id of ids) {
  const bodies = locales.map(locale=>read(`src/content/docs/${locale}/${id}.md`));
  for (const [i,body] of bodies.entries()) {
    assertPublicationState(body.split('---')[1], `${locales[i]}/${id}`);
    assert.doesNotMatch(body,/TODO|in progress|book-lab|<details|<button|<input|<select|<form/i);
    assert.match(body,locales[i]==='en'?/## Reference answers\n/:/## 参考解答\n/);
    assert.match(body,locales[i]==='en'?/## References\n/:/## 参考文献\n/);
    const sections=body.split(/^## /m);
    const exercises=sections.find(s=>s.startsWith(i===0?'Exercises\n':'习题\n'));
    const answers=sections.find(s=>s.startsWith(i===0?'Reference answers\n':'参考解答\n'));
    assert.deepEqual([...exercises.matchAll(/^(\d+)\. /gm)].map(m=>m[1]),[...answers.matchAll(/^(\d+)\. /gm)].map(m=>m[1]),id);
    for (const token of contract[id]) assert.ok(body.includes(token),`${locales[i]}/${id}: ${token}`);
    for (const match of body.matchAll(/```book-figure\n([^\n]+)\n```/g)) {
      const source=json(`src/assets/${match[1]}.json`);
      const html=renderFigure(match[1],locales[i]);
      assert.ok(html.includes(source.caption[locales[i]]));
      assert.ok(html.includes('CC BY-SA 4.0'));
      assert.doesNotMatch(html,/<button|<input|<details/);
    }
  }
  const headingLevels=body=>[...body.matchAll(/^(#{2,6}) /gm)].map(m=>m[1].length);
  assert.deepEqual(headingLevels(bodies[0]),headingLevels(bodies[1]),`${id} bilingual anchors`);
  const math=body=>[...body.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(m=>m[1].replace(/\s/g,''));
  assert.deepEqual(math(bodies[0]),math(bodies[1]),`${id} display math parity`);
  const sources=body=>[...body.matchAll(/\]\((https?:[^)]+)\)/g)].map(m=>m[1]).sort();
  assert.deepEqual(sources(bodies[0]),sources(bodies[1]),`${id} source parity`);
}
for (const name of ['inherited-freeze-v1.json','run-manifest.json','notebook-execution.json']) {
  for (const [path,digest] of Object.entries(json(`data/part-vii/${name}`).inputs_sha256)) assert.equal(hash(path),digest,`${name}: ${path}`);
}
for (const [name,digest] of Object.entries(json('data/part-vii/run-manifest.json').outputs_sha256)) assert.equal(hash(`data/part-vii/${name}`),digest,name);
for (const row of json('data/part-vii/notebook-execution.json').executions) {
  assert.equal(hash(row.notebook),row.artifact_sha256);
  const book=json(row.notebook), cells=book.cells.filter(c=>c.cell_type==='code');
  assert.equal(cells.length,row.code_cells);
  assert.ok(cells.every(c=>c.execution_count>0&&!c.outputs.some(o=>o.output_type==='error')));
}
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-10,`${a} differs from ${b}`);
const expected=json('data/part-vii/expected-v1.json');
const context=json('data/part-vii/context-run.json');
for (const locale of locales) near(context[locale].input_units,expected.context[locale==='en'?'en_units':'zh_units']);
const canonical=json('data/part-vii/rag-traces.json').traces;
for (const [locale,units] of [['en',502],['zh-hans',346]]) {
  assert.equal([...JSON.stringify(canonical[locale].answer)].length,units);
  assert.ok(units>canonical[locale].context.output_reserve,'The local reserve is not a model output cap');
}
const independentB=Math.log(12/7)*.88+Math.log(12/5)*44/35;
near(independentB,expected.bm25_current[1]);
near((1/Math.log2(3))/(3+1/Math.log2(3)),expected.graded.ndcg2);
const ranking=json('data/part-vii/retrieval-run.json');
for (const locale of locales) {
  assert.deepEqual(ranking.locales[locale].success_counts,expected.ranking_success);
  near(ranking.locales[locale].rows[0].scores.bm25['travel-v2'],independentB);
  assert.deepEqual(ranking.locales[locale].inherited.success_counts,{keyword:5,count:6,tfidf:7});
}
const evaluation=json('data/part-vii/eval-run.json');
assert.equal(evaluation.rows.length,144);
assert.deepEqual(evaluation.confidence.paired_differences,expected.evaluation.paired);
assert.deepEqual(evaluation.confidence.percentile95,[0,.25]);
for (const condition of ['baseline','filtered']) assert.equal(evaluation.summaries[condition].end_to_end.numerator,expected.evaluation[condition]);
for (const row of evaluation.rows) {
  if (row.trace.answer.status==='answered') assert.ok(row.trace.validation.support.supported);
}
for (const file of readdirSync(new URL('code/part-vii/',root)).filter(name=>name.endsWith('.py'))) assert.doesNotMatch(read(`code/part-vii/${file}`),/[\u3400-\u9fff]/,`English implementation: ${file}`);
console.log('Validated Part VII bilingual structure, evidence, independent arithmetic, immutable baselines, source/run hashes and executed notebooks.');
