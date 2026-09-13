// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { assertPublicationState } from './publication-state.mjs';
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { renderFigure } from '../src/plugins/remark-book.mjs';
import { checkPartIVNumbers } from './part-iv-evidence.mjs';
const root = new URL('../', import.meta.url);
const read = (path) => readFileSync(new URL(path,root),'utf8');
const json = (path) => JSON.parse(read(path));
const hash = (path) => createHash('sha256').update(readFileSync(new URL(path,root))).digest('hex');
const contract = json('data/part-iv/content-contract.json');
const numerical = checkPartIVNumbers();
const extract = (page, expression) => [...page.matchAll(expression)].map(m=>m[1].trim());
const headings = (page) => [...page.matchAll(/^(#{2,6}) (.+)$/gm)].map(m=>[m[1].length,m[2]]);
const figures = (page) => extract(page,/```book-figure\n([^`]+)```/g);
const sequence = (page,label) => {
  const section=page.split(`## ${label}\n`)[1]?.split('\n## ')[0];
  assert.ok(section,`Missing static section: ${label}`);
  return extract(section,/^(\d+)\. /gm).map(Number);
};
const rows = (page,locale,id) => {
  const section=page.split(`**${contract.captions[locale].table} ${id}${contract.captions[locale].separator}`)[1];
  assert.ok(section,`Missing table ${id}`);
  const block=section.match(/(?:^|\n)(\|[^\n]+\|(?:\n\|[^\n]+\|)+)/)?.[1];
  assert.ok(block,`Missing table rows ${id}`);
  return block.split('\n').slice(2).map(line=>line.split('|').slice(1,-1).map(cell=>cell.trim()));
};
const near = (actual,expected) => assert.ok(Math.abs(Number(actual)-expected)<=.00000051,`${actual} != ${expected}`);
for (let chapter=15;chapter<=21;chapter++) {
  const id=`ch-${chapter}`, pages=['en','zh-hans'].map(locale=>read(`src/content/docs/${locale}/${id}.md`));
  for(const [i,page] of pages.entries()) {
    const locale=['en','zh-hans'][i], labels=contract.headings[locale];
    const front=page.match(/^---\n([\s\S]+?)\n---/)?.[1]??'';
    assertPublicationState(front, `${locale}/${id}`);
    assert.doesNotMatch(page,/<!--|TODO|in progress and is visible|^# |^\+##/mi);
    assert.doesNotMatch(page,/<(?:input|select|button|textarea|form|details|summary|book-lab)\b|```book-lab/i);
    let previous=1;
    for(const [depth,title] of headings(page)) { assert.ok(depth<=previous+1);assert.doesNotMatch(title,/^\d+\./);previous=depth; }
    for(const label of Object.values(labels)) assert.ok(headings(page).some(h=>h[1]===label));
    const exercises=sequence(page,labels.exercises);
    assert.ok(exercises.length>0);assert.deepEqual(exercises,exercises.map((_,i)=>i+1));
    assert.deepEqual(sequence(page,labels.answers),exercises);
    for(const value of contract.evidence[id]) assert.ok(page.includes(value),`${locale}/${id}: missing ${value}`);
    assert.ok(figures(page).length>0);
    for(const asset of figures(page)) {
      assert.ok(asset.startsWith(`${id}/`));
      const source=json(`src/assets/${asset}.json`);
      for(const key of ['alt','caption','credit']) assert.ok(source[key][locale]?.trim());
      const rendered=renderFigure(asset,locale);
      assert.match(rendered,/role="img" aria-label="[^"]+"/);assert.match(rendered,/CC BY-SA 4.0/);
      assert.doesNotMatch(rendered,/undefined|NaN|class="kind-state"/);
      for(const lane of source.lanes??[]) for(const node of lane.nodes) assert.ok(node.text[locale]?.trim());
    }
    for(const target of extract(page,/\]\(\.\.\/([^/)]+)\//g)) assert.ok(existsSync(new URL(`src/content/docs/${locale}/${target}.md`,root)));
    if(chapter===15) rows(page,locale,'15.1').forEach((row,i)=>row.slice(1).forEach((x,j)=>near(x,numerical.attention.attention.weights[i][j])));
    if(chapter===20) rows(page,locale,'20.5').forEach((row,i)=>{assert.equal(Number(row[0]),i);near(row[1],numerical.forward.selected_head_scores[i]);near(row[2],numerical.forward.selected_head_weights[i]);});
    if(chapter===21) {
      const curve=rows(page,locale,'21.2');assert.equal(curve.length,numerical.trained.curve.length);
      curve.forEach((row,i)=>{assert.equal(Number(row[0]),numerical.trained.curve[i].step);near(row[1],numerical.trained.curve[i].train_loss);near(row[2],numerical.trained.curve[i].validation_loss);});
      const trace=rows(page,locale,'21.5');
      const red=numerical.generated.find(x=>x.checkpoint==='final'&&x.probe_id==='aligned-red'&&x.mode==='greedy');
      trace.forEach((row,i)=>{assert.equal(Number(row[1]),red.trace[i].context_ids.length);near(row[4],red.trace[i].model_probability);});
      assert.ok(page.includes(contract.static_labels[locale].checkpoint));
    }
  }
  assert.deepEqual(headings(pages[0]).map(h=>h[0]),headings(pages[1]).map(h=>h[0]),`${id}: anchor parity`);
  for(const [name,expression,sort] of [
    ['display math',/\$\$([\s\S]*?)\$\$/g,false],
    ['inline math',/(?<!\$)\$(?!\$)([^\n$]+)\$(?!\$)/g,true],
    ['references',/\]\((https:\/\/[^)]+)\)/g,true],
  ]) {
    const values=pages.map(p=>extract(p,expression));if(sort)values.forEach(a=>a.sort());
    assert.deepEqual(values[0],values[1],`${id}: ${name} parity`);
  }
  assert.deepEqual(figures(pages[0]),figures(pages[1]));
  for(const type of ['example','table']) {
    const numbers=pages.map((page,i)=>extract(page,new RegExp(`\\*\\*${contract.captions[['en','zh-hans'][i]][type]} (\\d+\\.\\d+)${contract.captions[['en','zh-hans'][i]].separator}`,'g')));
    assert.ok(numbers[0].length>0);assert.deepEqual(numbers[0],numbers[1]);
    assert.deepEqual(numbers[0],numbers[0].map((_,i)=>`${chapter}.${i+1}`));
  }
  assert.deepEqual(sequence(pages[0],'Exercises'),sequence(pages[1],contract.headings['zh-hans'].exercises));
}
for(const [path,digest] of Object.entries(json('data/part-iv/validation-manifest.json').sha256)) assert.equal(hash(path),digest,`Stale numerical artifact: ${path}`);
for(const [path,digest] of Object.entries(numerical.trained.source_sha256)) assert.equal(hash(path),digest,`Stale training source: ${path}`);
for(const [name,file] of Object.entries(numerical.trained.checkpoints)) {
  const path=`data/mini-gpt/${name}`;
  assert.equal(hash(path),file.sha256);assert.equal(statSync(new URL(path,root)).size,file.bytes);
}
const execution=json('data/part-iv/notebook-execution.json');
for(const [path,digest] of Object.entries(execution.inputs_sha256)) assert.equal(hash(path),digest,`Stale notebook input: ${path}`);
const paths=readdirSync(new URL('notebooks/part-iv/',root)).filter(p=>p.endsWith('.ipynb')).map(p=>`notebooks/part-iv/${p}`);
assert.deepEqual(execution.executions.map(r=>r.notebook).sort(),paths.sort());
for(const record of execution.executions) {
  const nb=json(record.notebook), source=c=>Array.isArray(c.source)?c.source.join(''):c.source;
  const code=nb.cells.filter(c=>c.cell_type==='code');
  assert.equal(record.status,'passed');assert.equal(code.length,record.code_cells);
  assert.equal(createHash('sha256').update(code.map(source).join('\n')).digest('hex'),record.code_sha256);
  assert.ok(code.every((c,i)=>c.execution_count===i+1&&c.outputs.every(o=>o.output_type!=='error')));
  for(const cell of nb.cells) assert.doesNotMatch(source(cell),/\p{Script=Han}/u);
}
for(const dir of ['code/part-iv','code/mini-gpt']) for(const name of readdirSync(new URL(`${dir}/`,root)).filter(p=>p.endsWith('.py'))) assert.doesNotMatch(read(`${dir}/${name}`),/\p{Script=Han}/u);
for(const name of ['blueprint','research','validation']) assert.doesNotMatch(read(`docs/part-iv-${name}.md`),/\p{Script=Han}/u);
console.log('Validated all seven Part IV chapter pairs, bilingual math/anchors/answers, rendered figures, independent numeric evidence, actual MG records/checkpoints and fresh notebook provenance.');
