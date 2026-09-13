// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { assertPublicationState } from './publication-state.mjs';
import { readFileSync, existsSync } from 'node:fs';
import { renderFigure } from '../src/plugins/remark-book.mjs';
import { checkPartVINumbers } from './part-vi-evidence.mjs';
const root=new URL('../',import.meta.url);
const read=path=>readFileSync(new URL(path,root),'utf8');
const json=path=>JSON.parse(read(path));
const contract=json('data/part-vi/content-contract.json');
const {result,actual,budget}=checkPartVINumbers();
const extract=(page,re)=>[...page.matchAll(re)].map(m=>m[1].trim());
const headings=page=>[...page.matchAll(/^(#{2,6}) (.+)$/gm)].map(m=>[m[1].length,m[2]]);
const figureIds=page=>extract(page,/\x60{3}book-figure\n([\s\S]*?)\x60{3}/g);
const sequence=(page,label)=>extract(page.split('## '+label+'\n')[1]?.split('\n## ')[0]??'',/^(\d+)\. /gm).map(Number);
const rows=(page,locale,id)=>{
  const block=page.split('**'+contract.captions[locale].table+' '+id+contract.captions[locale].separator)[1]?.match(/\|[^\n]+\|(?:\n\|[^\n]+\|)+/)?.[0];
  assert.ok(block,'Missing table '+id);
  return block.split('\n').slice(2).map(line=>line.split('|').slice(1,-1).map(cell=>cell.trim()));
};
const near=(a,b)=>assert.ok(Math.abs(Number(a)-b)<.00000051,a+' != '+b);
for(const chapter of contract.chapters) {
  const id='ch-'+chapter;
  const pages=['en','zh-hans'].map(locale=>read('src/content/docs/'+locale+'/'+id+'.md'));
  for(const [index,page] of pages.entries()) {
    const locale=['en','zh-hans'][index], labels=contract.headings[locale];
    const front=page.match(/^---\n([\s\S]+?)\n---/)?.[1]??'';
    assertPublicationState(front, `${locale}/${id}`);
    assert.doesNotMatch(page,/<!--|TODO|in progress and is visible|^# |§|^\\\+##/mi);
    assert.doesNotMatch(page,/<(?:input|select|button|textarea|form|details|summary|book-lab)\b|\x60{3}book-lab/i);
    let previous=1;
    for(const [depth,title]of headings(page)){assert.ok(depth<=previous+1);assert.doesNotMatch(title,/^\d+\./);previous=depth;}
    for(const label of Object.values(labels))assert.ok(headings(page).some(h=>h[1]===label));
    const exercises=sequence(page,labels.exercises);
    assert.ok(exercises.length>0);assert.deepEqual(exercises,exercises.map((_,i)=>i+1));
    assert.deepEqual(sequence(page,labels.answers),exercises);
    for(const value of contract.evidence[id])assert.ok(page.replaceAll('{,}',',').includes(value),locale+'/'+id+': missing '+value);
    for(const asset of figureIds(page)){
      const source=json('src/assets/'+asset+'.json');
      for(const key of ['caption','alt','credit'])assert.ok(source[key][locale]?.trim());
      const rendered=renderFigure(asset,locale);
      assert.match(rendered,/role="img" aria-label="[^"]+"/);assert.match(rendered,/CC BY-SA 4.0/);
      assert.doesNotMatch(rendered,/undefined|NaN|class="kind-state"/);
      for(const lane of source.lanes??[])for(const node of lane.nodes)assert.ok(node.text[locale]?.trim());
    }
    assert.ok(figureIds(page).length>0);
    for(const target of extract(page,/\]\(\/books\/understanding-llms\/(?:en|zh-hans)\/([^/)]+)\//g))assert.ok(existsSync(new URL('src/content/docs/'+locale+'/'+target+'.md',root)));
    if(chapter===34){
      const mask=rows(page,locale,'34.2');
      assert.equal(mask.length,11);
      assert.deepEqual(mask.slice(0,10).map(r=>Number(r[3])),result.sft.mask);
      assert.deepEqual(mask.slice(0,10).map(r=>Number(r[2].match(/\/ (\d+)$/)[1])),result.sft.targets);
      assert.deepEqual(mask.map(r=>Number(r[0])),Array.from({length:11},(_,i)=>i));
    }
    if(chapter===35){
      const table=rows(page,locale,'35.2');
      const expected=[[.5,0,.5,.5],[.75,result.preference.kl,.75-result.preference.kl,.75-2*result.preference.kl]];
      table.forEach((r,i)=>r.slice(1).forEach((cell,j)=>near(cell,expected[i][j])));
      assert.equal(rows(page,locale,'35.1').length,result.preference.audits.length);
    }
    if(chapter===36){
      const candidates=rows(page,locale,'36.1');
      const fixed=json('data/part-vi/reasoning-v1.json').candidates;
      assert.deepEqual(candidates.map(r=>r[2].slice(1,-1)),fixed.map(c=>c.response));
      const checked=rows(page,locale,'36.2');
      const accepted=checked[0][1];
      assert.deepEqual(checked.map(r=>r.slice(1).map(value=>value===accepted)),result.verifier.map(r=>[r.substring,r.exact,r.rule.accepted]));
    }
    if(chapter===37){
      const table=rows(page,locale,'37.2');
      ['direct','steps','vote','search'].forEach((method,i)=>{
        const row=result.budget.find(r=>r.order.join('')==='ABC'&&r.maximum===4&&r.method===method);
        assert.deepEqual(table[i].slice(1,5).map(Number),[row.cases.flatMap(c=>c.calls).filter(c=>c.kind==='generate').length,row.cases.flatMap(c=>c.calls).filter(c=>c.kind==='verify').length,row.calls,row.tokens]);
        assert.equal(table[i][5],row.correct+'/4');near(table[i][6],row.replay_elapsed_ms);
      });
      assert.deepEqual(rows(page,locale,'37.3').map(r=>r.map((v,i)=>i?Number(v.split('/')[0]):Number(v))),budget.budget.maxima.map((maximum,i)=>[maximum,...['direct','steps','vote','search'].map(method=>budget.independent_expected.primary_correct[method][i])]));
      const pool=rows(page,locale,'37.1');assert.equal(pool.length,4);
      pool.forEach((r,i)=>assert.deepEqual(r.slice(1),[String(budget.cases[i].answer),budget.cases[i].direct,...budget.cases[i].candidates.map(c=>c.text)]));
    }
    if(chapter===38){
      const scores=rows(page,locale,'38.3'),costs=rows(page,locale,'38.4');
      ['selected-50','final-600'].forEach((candidate,i)=>['en','zh-hans'].forEach((lang,j)=>{
        const group=actual.summary.filter(s=>s.candidate===candidate&&s.locale===lang&&s.policy==='greedy');
        const raw=group.find(s=>s.arm==='raw'),norm=group.find(s=>s.arm==='normalized'),row=scores[i*2+j];
        assert.equal(row[1],raw.strict_passes+'/18 → '+norm.strict_passes+'/18');
        assert.equal(row[2],raw.semantic_passes+'/18 → '+norm.semantic_passes+'/18');
        assert.equal(row[3],raw.stable_semantic_cases+'/6 → '+norm.stable_semantic_cases+'/6');
        near(costs[i*2+j][1],raw.p95_ms);near(costs[i*2+j][2],norm.p95_ms);
        assert.equal(Number(costs[i*2+j][3]),raw.generated_tokens_including_eos);
      }));
      const responses=rows(page,locale,'38.2');
      const cases=json('data/knowledge-assistant/ka1-contract-v1.json').cases;
      cases.forEach((c,i)=>['en','zh-hans'].forEach((lang,j)=>{
        const output=actual.rows.find(r=>r.case===c.id&&r.locale===lang&&r.candidate==='selected-50'&&r.policy==='greedy');
        const raw=responses[i][j+1].match(/\x60([^\x60]+)\x60/)[1];
        assert.equal(raw,output.raw);
      }));
      assert.deepEqual(rows(page,locale,'38.6').map(r=>r.slice(1)),[['5/9','5/9'],['6/9','6/9'],['7/9','7/9']]);
    }
    if(chapter===39){
      const counts=rows(page,locale,'39.3');
      assert.deepEqual(counts.map(r=>r.slice(1,4).map(v=>Number(v.replaceAll(',','')))),[[1,12,7],[2,12,14],[8,4096**2,8*(4096+4096)]]);
      assert.equal(parseFloat(counts[2][4]),100/256);
    }
  }
  assert.deepEqual(headings(pages[0]).map(h=>h[0]),headings(pages[1]).map(h=>h[0]),id+': anchor parity');
  assert.deepEqual(figureIds(pages[0]),figureIds(pages[1]));
  for(const [name,re,sort]of [['display math',/\$\$([\s\S]*?)\$\$/g,false],['inline math',/(?<!\$)\$(?!\$)([^\n$]+)\$(?!\$)/g,true],['references',/\]\((https:\/\/[^)]+)\)/g,true]]){
    const values=pages.map(p=>extract(p,re));if(sort)values.forEach(a=>a.sort());
    assert.deepEqual(values[0],values[1],id+': '+name+' parity');
  }
  for(const type of ['example','table']){
    const numbers=pages.map((page,i)=>extract(page,new RegExp('\\*\\*'+contract.captions[['en','zh-hans'][i]][type]+' ('+chapter+'\\.\\d+)','g')));
    assert.deepEqual(numbers[0],numbers[1]);assert.deepEqual(numbers[0],numbers[0].map((_,i)=>chapter+'.'+(i+1)));
  }
}
console.log('Part VI: 12 manuscripts, six shared figures, numeric/behavior records, table bindings and executed notebooks verified.');
