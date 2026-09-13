// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { assertPublicationState } from './publication-state.mjs';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { renderFigure } from '../src/plugins/remark-book.mjs';
import { checkPartVNumbers } from './part-v-evidence.mjs';
const root = new URL('../', import.meta.url);
const read = (path) => readFileSync(new URL(path,root),'utf8');
const json = (path) => JSON.parse(read(path));
const hash = (path) => createHash('sha256').update(readFileSync(new URL(path,root))).digest('hex');
const contract = json('data/part-v/content-contract.json');
const numerical = checkPartVNumbers();
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
for (const chapter of contract.chapters) {
  const id=`ch-${chapter}`, pages=['en','zh-hans'].map(locale=>read(`src/content/docs/${locale}/${id}.md`));
  for(const [i,page] of pages.entries()) {
    const locale=['en','zh-hans'][i], labels={...contract.headings[locale], ...(chapter===33 ? {exercises:contract.final_exercises[locale]} : {})};
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
    for(const value of contract.evidence[id]) assert.ok(page.replaceAll("{,}",",").includes(value),`${locale}/${id}: missing ${value}`);
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

    if(chapter===27) {
      const ledger=rows(page,locale,'27.1');
      assert.deepEqual(ledger.map(r=>Number(r.at(-1).replaceAll(',',''))),[2e6,2e6,4e6,8e6,16e6]);
    }
    if(chapter===29) {
      const distributions=rows(page,locale,'29.1');
      const expected=[[1,0,0,0],[.5,.25,.125,.125],numerical.derived.sampling.find(r=>r.policy==='temperature-2').probabilities,[2/3,1/3,0,0],[1,0,0,0],[2/3,1/3,0,0],[4/7,2/7,1/7,0]];
      assert.equal(distributions.length,expected.length);
      distributions.forEach((row,i)=>row.slice(1).forEach((s,j)=>{const [a,b='1']=s.split('/');near(Number(a)/Number(b),expected[i][j]);}));
      const matrix=rows(page,locale,'29.3'), fixture=json('data/part-v/generation-tasks.json');
      assert.equal(matrix.length,6);
      for(const [i,lang] of ['en','zh-hans'].entries()) for(const [j,policy] of fixture.policies.entries()) {
        const attempts=numerical.gen.rows.filter(r=>r.locale===lang&&r.policy===policy.id&&r.task===fixture.tasks[0].id);
        assert.deepEqual(matrix[i*3+j].slice(1).map(s=>s.slice(1,-1)),attempts.map(r=>r.output.completion));
      }
    }
    if(chapter===30) {
      assert.deepEqual(rows(page,locale,'30.1').map(row=>Number(row[1])),[8,9,10]);
      const quantum=rows(page,locale,'30.2');assert.equal(quantum.length,4);
      quantum.forEach((row,i)=>{near(row[2].replace('−','-'),numerical.derived.quantization.integers[i]);near(row[3].replace('−','-'),numerical.derived.quantization.decoded[i]);});
    }
    if(chapter===31) {
      const metrics=rows(page,locale,'31.2');assert.equal(metrics.length,3);
      metrics.forEach((row,i)=>{
        const a=numerical.derived.serving.serial.requests[i], b=numerical.derived.serving.continuous.requests[i];
        assert.equal(parseFloat(row[1]),a.ttft_ms);assert.equal(parseFloat(row[2]),b.ttft_ms);
        if(i<2){assert.equal(parseFloat(row[3]),a.tpot_ms);assert.equal(parseFloat(row[4]),b.tpot_ms);}else assert.ok(Number.isNaN(parseFloat(row[3]))&&Number.isNaN(parseFloat(row[4])));
      });
    }
    if(chapter===32) {
      const calibration=rows(page,locale,'32.2');
      assert.deepEqual(calibration.map(row=>row[0].slice(1,-1)),json('data/knowledge-assistant/ka1-calibration-v1.json').rows.map(row=>row.response[locale]));
      assert.ok(page.includes('ka1-provenance-note-v1.json'));
    }
    if(chapter===33) {
      const measured=rows(page,locale,'33.1');assert.equal(measured.length,4);
      for(const [i,candidate] of ['selected-50','final-600'].entries()) for(const [j,lang] of ['en','zh-hans'].entries()) {
        const s=numerical.review.summary.find(r=>r.candidate===candidate&&r.locale===lang&&r.policy==='greedy'),row=measured[i*2+j];
        assert.deepEqual(row.slice(1,4).map(Number),[s.strict_passes,s.semantic_passes,s.stable_semantic_cases]);
        assert.deepEqual(row[4].split(' / '),[s.median_complete_call_ms.toFixed(3),s.p95_complete_call_ms.toFixed(3)]);
      }
      const cases=json('data/knowledge-assistant/ka1-contract-v1.json').cases;
      for(const [i,lang] of ['en','zh-hans'].entries()) {
        const responses=rows(page,locale,`33.${i+2}`);assert.equal(responses.length,6);
        cases.forEach((c,k)=>['selected-50','final-600'].forEach((candidate,j)=>{
          const raw=numerical.run.rows.filter(r=>r.case===c.id&&r.locale===lang&&r.candidate===candidate&&r.policy==='greedy');
          assert.equal(raw.length,3);assert.ok(raw.every(r=>r.output.completion===responses[k][j+1].slice(1,-1)));
        }));
      }
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
  assert.deepEqual(sequence(pages[0],chapter===33?contract.final_exercises.en:'Exercises'),sequence(pages[1],chapter===33?contract.final_exercises['zh-hans']:contract.headings['zh-hans'].exercises));
}
const execution=json('data/part-v/notebook-execution.json');
for(const [path,digest] of Object.entries(execution.inputs_sha256)) assert.equal(hash(path),digest,`Stale notebook input: ${path}`);
const paths=readdirSync(new URL('notebooks/part-v/',root)).filter(p=>p.endsWith('.ipynb')).map(p=>`notebooks/part-v/${p}`);
assert.deepEqual(execution.executions.map(r=>r.notebook).sort(),paths.sort());
for(const record of execution.executions) {
  const nb=json(record.notebook), source=c=>Array.isArray(c.source)?c.source.join(''):c.source;
  const code=nb.cells.filter(c=>c.cell_type==='code');
  assert.equal(record.status,'passed');assert.equal(code.length,record.code_cells);
  assert.equal(createHash('sha256').update(code.map(source).join('\n')).digest('hex'),record.code_sha256);
  assert.ok(code.every((c,i)=>c.execution_count===i+1&&c.outputs.every(o=>o.output_type!=='error')));
  for(const cell of nb.cells) assert.doesNotMatch(source(cell),/\p{Script=Han}/u);
}
for(const dir of ['code/part-v']) for(const name of readdirSync(new URL(`${dir}/`,root)).filter(p=>p.endsWith('.py'))) assert.doesNotMatch(read(`${dir}/${name}`),/\p{Script=Han}/u);
for(const name of ['blueprint','research','validation']) assert.doesNotMatch(read(`docs/part-v-${name}.md`),/\p{Script=Han}/u);
console.log('Validated all twelve Part V chapter pairs, bilingual math/anchors/answers, twelve rendered figure sources, independent numeric evidence, 180 measured generation attempts and fresh notebook provenance.');
