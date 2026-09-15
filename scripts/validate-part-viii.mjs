// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { renderFigure } from '../src/plugins/remark-book.mjs';
import { assertPublicationState } from './publication-state.mjs';
const root=new URL('../',import.meta.url);
const read=p=>readFileSync(new URL(p,root),'utf8');
const json=p=>JSON.parse(read(p));
const hash=p=>createHash('sha256').update(readFileSync(new URL(p,root))).digest('hex');
const chapters=Array.from({length:7},(_,i)=>47+i);
const evidence={47:['use_evidence','ABSTAINED','750','RNN'],48:['1.0.0','SKILL.md','225','1,511','1,127'],49:['0.35','0.05','UNCERTAIN','receipt'],50:['3/4','0/4','8/8','70\\%','75\\%','60\\%'],51:['750','600','4\\times2=8','4\\times1=4'],52:['DEMO-SECRET-ORCHID','DEMO-CABINET-42','send_http','Permission'],53:['458ce03a','orders:read:own','PermissionError','0/4']};
for(const n of chapters){
 const bodies=['en','zh-hans'].map(l=>read(`src/content/docs/${l}/ch-${n}.md`));
 for(const [i,body] of bodies.entries()){
  assertPublicationState(body.split('---')[1], `ch-${n}/${i}`);
  assert.doesNotMatch(body,/^date:|in progress|Replace the placeholder|TODO|<details|<button|<input|<select|<form|```book-lab/im);
  assert.match(body,i===0?/## Summary\n/:/## 本章小结\n/);
  assert.match(body,i===0?/## References\n/:/## 参考文献\n/);
  const sections=body.split(/^## /m),ex=sections.find(s=>s.startsWith(i===0?'Exercises\n':'习题\n')),answers=sections.find(s=>s.startsWith(i===0?'Reference answers\n':'参考解答\n')).split(/\*\*(?:Part checkpoint answers|本部分检查点解答)/)[0];
  const numbers=s=>[...s.matchAll(/^(\d+)\. /gm)].map(m=>+m[1]);
  assert.deepEqual(numbers(ex),numbers(answers),`${n} exercise/answer mapping`);
  assert.ok(numbers(ex).length>=4);
  for(const token of evidence[n]) if(!['receipt','Permission'].includes(token)) assert.ok(body.includes(token),`${n}/${i}: ${token}`);
  const figures=[...body.matchAll(/```book-figure\n([^\n]+)\n```/g)];assert.equal(figures.length,1);
  const locale=i===0?'en':'zh-hans',source=json(`src/assets/${figures[0][1]}.json`),html=renderFigure(figures[0][1],locale);
  assert.ok(html.includes(source.caption[locale]));assert.ok(html.includes('CC BY-SA 4.0'));assert.doesNotMatch(html,/<script|<button|undefined|NaN/);
 }
 const headings=s=>[...s.matchAll(/^(#{2,6}) /gm)].map(m=>m[1].length);
 const maths=s=>[...s.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(m=>m[1].replace(/\s/g,''));
 const links=s=>[...s.matchAll(/\]\((https?:[^)]+)\)/g)].map(m=>m[1]).sort();
 assert.deepEqual(headings(bodies[0]),headings(bodies[1]),`${n} structure`);
 assert.deepEqual(maths(bodies[0]),maths(bodies[1]),`${n} display mathematics`);
 assert.deepEqual(links(bodies[0]),links(bodies[1]),`${n} primary references`);
}
const risks=json('data/knowledge-assistant/risk-register-v3.json');
const roles=json('data/knowledge-assistant/governance-v1.json').roles;
for(const risk of risks.entries){assert.ok(roles[risk.owner]);assert.ok(risk.affected_data&&risk.residual);for(const path of risk.evidence_paths)assert.ok(existsSync(new URL(path,root)),path);}
const skill=json('data/part-viii/skill-run.json').trace;
assert.deepEqual(skill.slice(0,3).map(row=>row.utf8_bytes),[225,1511,1127]);
assert.equal(skill[3].returncode,0);assert.equal(skill[4].report.supported,true);
const expected=json('data/part-viii/expected-v1.json');
const workflow=json('data/part-viii/workflow-run.json');
for(const locale of ['en','zh-hans']){
 const cases=workflow.locales[locale];
 for(const name of ['valid','decline','invalid','empty']) assert.deepEqual(cases[name].events.map(e=>e.state),expected.workflow[name]);
 assert.equal(cases.valid.answer.amount_yuan,750);assert.equal(cases.empty.model_calls,0);assert.equal(cases.exhausted.model_calls,0);
}
const recovery=json('data/part-viii/recovery-run.json');
assert.equal(recovery.unsafe_duplicate_effects,2);
assert.equal(recovery.cases.after_commit.first_effects,1);assert.equal(recovery.cases.before_commit.first_effects,0);
for(const name of ['success','before_commit','after_commit']) assert.equal(recovery.cases[name].final_order.effects,1);
for(const name of ['denied','expired','budget','deadline']) assert.equal(recovery.cases[name].final_order.effects,0);
for(const row of Object.values(recovery.cases)) assert.equal(row.replay_mutations,0);
assert.ok(Math.abs(recovery.logical_schedule.elapsed_seconds-(.2+.05+.1))<1e-12);
assert.equal(recovery.short_deadline_schedule.events.length,1);
const evaluation=json('data/part-viii/system-eval-run.json');
assert.deepEqual(evaluation.rows.filter(r=>r.variant==='retrieval_variant').map(r=>r.checks.end_to_end),[false,true,true,true]);
assert.deepEqual(evaluation.rows.filter(r=>r.variant==='generation_variant').map(r=>r.checks.end_to_end),[true,false,true,true]);
for(const locale of ['en','zh-hans']) assert.deepEqual(evaluation.inherited[locale].success_counts,{keyword:5,count:6,tfidf:7});
const calibration=json('data/part-viii/judge-calibration.json');
assert.equal(calibration.travel_human_calibration.unique_human_cases,4);assert.equal(calibration.travel_human_calibration.matched,8);
assert.equal(calibration.human_calibration.agreed,0);assert.equal(calibration.human_calibration.position_consistent,3);
const human=json('data/part-viii/travel-human-labels-v1.json');assert.deepEqual(Object.values(human.labels),['pass','fail','pass','fail']);
const raw=json('data/part-viii/human-judge-run.json');
const calls=new Map(raw.calls.map(r=>[r.id,r.result]));const inverse={A:'B',B:'A',tie:'tie'};
for(const row of calibration.human_calibration.rows){assert.equal(row.forward,calls.get(`human-${row.question_id}-forward`));assert.equal(row.swapped_mapped,inverse[calls.get(`human-${row.question_id}-swapped`)]);assert.equal(row.agrees,row.conservative===row.human);}
const c=expected.exercise_confusion;assert.equal((c.tp+c.tn)/(c.tp+c.fp+c.tn+c.fn),c.accuracy);assert.equal(c.tp/(c.tp+c.fp),c.precision);assert.equal(c.tp/(c.tp+c.fn),c.recall);
const attacks=json('data/part-viii/attack-run.json');
assert.equal(attacks.cases.length,6);
for(const row of attacks.cases){assert.equal(row.unsafe.compromised,true);assert.equal(row.guarded.compromised,false);assert.equal(row.guarded.control,row.case.expected_control);}
const permissions=json('data/part-viii/permission-run.json');
assert.deepEqual(permissions.rows.filter(r=>r.allowed).map(r=>r.case),['own_read','south_own_read','approved_cancel']);
for(const row of permissions.rows) assert.equal(row.north_effects,row.case==='approved_cancel'?1:0);
const gov=json('data/part-viii/governance-run.json');assert.deepEqual(gov.deletion.after,{logs:1,memory:1,cache:1,feedback:1});assert.deepEqual(gov.expiry.remaining_ids,['audit']);
assert.deepEqual(gov.group_pairs.map(r=>r.amount_yuan),[750,750]);assert.equal(gov.correction.historical,600);
const supply=json('data/part-viii/supply-chain-run.json');for(const row of supply.cases){assert.equal(row.before,true);assert.equal(row.after,false);assert.equal(row.executed_changed_bytes,false);}assert.equal(supply.model_digest_case.accepted,false);
const sandbox=json('data/part-viii/sandbox-run.json').results;assert.equal(sandbox.confined.returncode,0);assert.equal(sandbox.unconfined.observation.network,'connected');assert.equal(sandbox.confined.observation.network.error,'PermissionError');assert.equal(sandbox.confined.observation.outside.error,'PermissionError');assert.equal(sandbox.confined.observation.allowed,'public-fixture');
for(const row of json('data/part-viii/reviewed-inventory-v1.json').files) assert.equal(hash(row.path),row.sha256,row.path);
for(const name of ['run-manifest.json','notebook-execution.json']) for(const [path,digest] of Object.entries(json(`data/part-viii/${name}`).inputs_sha256)) assert.equal(hash(path),digest,`${name}: ${path}`);
for(const [name,digest] of Object.entries(json('data/part-viii/run-manifest.json').outputs_sha256)) assert.equal(hash(`data/part-viii/${name}`),digest);
for(const row of json('data/part-viii/notebook-execution.json').executions){
 assert.equal(hash(row.notebook),row.artifact_sha256);const cells=json(row.notebook).cells.filter(c=>c.cell_type==='code');assert.equal(cells.length,row.code_cells);assert.ok(cells.every(c=>c.execution_count>0&&!c.outputs.some(o=>o.output_type==='error')));
}
for(const file of readdirSync(new URL('code/part-viii/',root)).filter(f=>f.endsWith('.py'))) assert.doesNotMatch(read(`code/part-viii/${file}`),/[\u3400-\u9fff]/,`English code: ${file}`);
console.log('Validated Part VIII bilingual chapters, independent expectations, raw/derived Judge evidence, control outcomes, reviewed inputs and executed notebooks.');
