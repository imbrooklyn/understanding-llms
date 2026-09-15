// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { renderFigure } from '../src/plugins/remark-book.mjs';
import { assertPublicationState } from './publication-state.mjs';
const root=new URL('../',import.meta.url);
const read=p=>readFileSync(new URL(p,root),'utf8');
const json=p=>JSON.parse(read(p));
const hash=p=>createHash('sha256').update(readFileSync(new URL(p,root))).digest('hex');
const canonical=value=>Array.isArray(value)?value.map(canonical):value&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])])):value;
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-10,`${a} != ${b}`);
const fragments={54:['202','400','750','InterruptedError'],55:['10/10','4/10','600','750'],56:['39.999','40','0.999949','18/20','40\\%'],57:['5/9','6/9','7/9','0/4','UNCERTAIN','DONE']};
for(const n of [54,55,56,57]){
 const bodies=['en','zh-hans'].map(locale=>read(`src/content/docs/${locale}/ch-${n}.md`));
 for(const [i,body] of bodies.entries()){
  assertPublicationState(body.split('---')[1], `ch-${n}/${i}`);
  assert.doesNotMatch(body,/^date:|Replace the placeholder|This chapter is in progress|TODO|<details|<button|<input|<select|<form|```book-lab/im);
  assert.match(body,i===0?/## Summary\n/:/## 本章小结\n/);
  assert.match(body,i===0?/## References\n/:/## 参考文献\n/);
  const sections=body.split(/^## /m);
  const exercises=sections.find(s=>s.startsWith(i===0?'Exercises\n':'习题\n'));
  const answers=sections.find(s=>s.startsWith(i===0?'Reference answers\n':'参考解答\n'));
  const numbers=s=>[...s.matchAll(/^(\d+)\. /gm)].map(m=>Number(m[1]));
  assert.ok(exercises&&answers,`${n} visible exercises and answers`);
  assert.deepEqual(numbers(exercises),numbers(answers),`${n} answer coverage`);
  assert.deepEqual(numbers(exercises),Array.from({length:numbers(exercises).length},(_,j)=>j+1));
  for(const token of fragments[n])assert.ok(body.includes(token),`${n}/${i} explained evidence ${token}`);
  assert.match(body,new RegExp(i===0?`Example ${n}\\.1`:`例 ${n}\\.1`));
  assert.match(body,new RegExp(i===0?`Table ${n}\\.1`:`表 ${n}\\.1`));
  const figures=[...body.matchAll(/```book-figure\n([^\n]+)\n```/g)];
  assert.equal(figures.length,1);
  for(const [,asset] of figures){
   const locale=i===0?'en':'zh-hans',source=json(`src/assets/${asset}.json`),html=renderFigure(asset,locale);
   assert.ok(source.alt[locale]&&source.caption[locale]&&source.credit[locale]);
   assert.ok(html.includes(source.caption[locale]));assert.ok(html.includes('CC BY-SA 4.0'));
   assert.doesNotMatch(html,/<script|<button|undefined|NaN/);
  }
 }
 const headings=s=>[...s.matchAll(/^(#{2,6}) /gm)].map(m=>m[1].length);
 const maths=s=>[...s.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(m=>m[1].replace(/\s/g,''));
 const links=s=>[...s.matchAll(/\]\((https?:[^)]+)\)/g)].map(m=>m[1]).sort();
 assert.deepEqual(headings(bodies[0]),headings(bodies[1]),`${n} structure anchors`);
 assert.deepEqual(maths(bodies[0]),maths(bodies[1]),`${n} display derivation`);
 assert.deepEqual(links(bodies[0]),links(bodies[1]),`${n} references`);
}
const expected=json('data/part-ix/expected-v1.json'),policy=json('data/part-ix/policy-run.json');
const d=expected.deadline;
assert.equal(d.budget_ms-d.queue_ms-d.retrieval_ms-d.attempt_ms-d.backoff_ms,400);
assert.equal(d.remaining_ms,400);
assert.deepEqual(expected.cache.lookup_times.map(t=>t<expected.cache.inserted_at+expected.cache.ttl_seconds),expected.cache.hits);
assert.deepEqual(policy.bucket.map(r=>r.allowed),[true,true,false,false,true,false,true]);
assert.deepEqual(policy.bucket.map(r=>r.remaining),[1,0,0,.5,0,.5,0]);
assert.deepEqual(policy.breaker.map(r=>r.allowed),[true,true,false,true,true]);
assert.deepEqual(policy.breaker.map(r=>r.state),['closed','open','open','closed','closed']);
near(policy.semantic_similarity,.99/Math.hypot(.99,.01));
assert.ok(policy.semantic_similarity>.999);assert.equal(policy.semantic_cache_enabled,false);
assert.notEqual(expected.semantic.historical_amount,expected.semantic.current_amount);
const eligible=policy.slo_rows.filter(r=>r.arrival>=0&&r.arrival<60&&r.eligible&&r.outcome!=='cancelled');
const good=eligible.filter(r=>['answered','abstained','refused'].includes(r.outcome)&&r.duration<=3);
assert.equal(eligible.length,20);assert.equal(good.length,18);
for(const [key,value] of Object.entries({total:20,good:18,bad:2,sli:18/20,budget:20*.05,burn:(2/20)/.05}))near(policy.slo[key],value);
assert.equal(policy.slo.alert,false);
// Transfer calculations use independent arithmetic, not production functions.
near(48/50,.96);near((50-48)/(50*.02),2);near((53-48)/(53*.02),4.716981132075471);
const service=json('data/part-ix/service-run.json');
const traces=Object.fromEntries(service.traces.map(r=>[r.label,r.trace]));
for(const key of ['current','current_zh','cached'])assert.equal(traces[key].result.answer.amount_yuan,750);
assert.equal(traces.historical.result.answer.amount_yuan,600);
for(const key of ['absent','synonym']){assert.equal(traces[key].result.answer.status,'abstained');assert.deepEqual(traces[key].result.answer.citations,[]);}
assert.equal(traces.own_order.result.order.order_id,'A-104');
assert.equal(traces.forbidden_order.state,'refused');
const stages=traces.cancelled.events.map(e=>e.stage);
assert.equal(traces.cancelled.state,'cancelled');assert.ok(stages.includes('worker_stopped'));
assert.ok(!stages.includes('dependency_failure')&&!stages.includes('answered')&&!stages.includes('cache_hit'));
assert.ok(traces.cached.events.some(e=>e.stage==='cache_hit'));
for(const trace of Object.values(traces)){
 assert.match(trace.trace_id,/^[0-9a-f]{32}$/);assert.equal(trace.model_calls,0);
 assert.equal(trace.events.filter(e=>['answered','abstained','refused','error','cancelled'].includes(e.stage)).length,1);
 for(let i=1;i<trace.events.length;i++)assert.ok(trace.events[i].elapsed_ms>=trace.events[i-1].elapsed_ms);
}
const releases=json('data/part-ix/release-run.json');
for(const [name,count] of Object.entries(expected.expected_release_passes)){
 const gate=releases.gates[name],candidate=json(`data/part-ix/${name}.json`);
 const {digest,...manifestBody}=candidate;
 assert.equal(createHash('sha256').update(JSON.stringify(canonical(manifestBody))).digest('hex'),digest);
 assert.equal(gate.passed_cases,count);assert.equal(gate.total,10);assert.equal(gate.manifest,candidate.digest);
 assert.equal(gate.passed,count===10);
 for(const row of gate.rows){assert.equal(row.passed,JSON.stringify(row.expected)===JSON.stringify(row.actual));}
 for(const [path,digest] of Object.entries(candidate.files))assert.equal(hash(path),digest,`${name}: ${path}`);
}
assert.equal(releases.rejected_candidate_reason,'release_gate');
assert.equal(releases.cohort.filter(r=>r.release==='rc-b').length,1);
assert.equal(releases.cohort.filter(r=>r.release==='rc-a').length,9);
assert.equal(releases.failed.result.answer.amount_yuan,600);assert.equal(releases.rollback.result.answer.amount_yuan,750);assert.equal(releases.inflight.result.answer.amount_yuan,600);
assert.equal(releases.replay.new_order_effects,0);assert.equal(releases.replay.new_model_calls,0);assert.equal(releases.replay.same,true);
const resilience=json('data/part-ix/resilience-run.json');
assert.deepEqual(resilience.traces.map(r=>r.trace.state),['answered','error','error','error','answered']);
assert.equal(resilience.traces[0].trace.events.filter(e=>e.stage==='attempt').length,2);
assert.equal(resilience.traces[3].trace.events.filter(e=>e.stage==='attempt').length,0);
assert.equal(resilience.traces[4].breaker,'closed');
assert.equal(resilience.monitor.total,5);assert.equal(resilience.monitor.good,2);assert.equal(resilience.monitor.bad,3);
near(resilience.monitor.sli,2/5);near(resilience.monitor.burn,(3/5)/.05);assert.equal(resilience.monitor.alert,true);
assert.equal(resilience.deadline.result.reason,'deadline');assert.equal(resilience.overload[0],503);assert.equal(resilience.rate_limit[0],429);
const feedback=json('data/part-ix/feedback-run.json');
assert.equal(feedback.submitted.state,'quarantined');assert.deepEqual(feedback.regressions_before,[]);assert.equal(feedback.regressions_after.length,1);
assert.deepEqual(feedback.retained_reports_after_deletion,[]);assert.equal(feedback.regression_result.passed,true);
assert.ok(!('subject' in feedback.reviewed)&&!('request_id' in feedback.reviewed));
const capstone=json('data/part-ix/capstone-run.json');
for(const locale of ['en','zh-hans'])assert.deepEqual(capstone.lexical[locale].success_counts,{keyword:5,count:6,tfidf:7});
assert.equal(capstone.permissions.rows.length,20);
assert.deepEqual(capstone.permissions.rows.filter(r=>r.allowed).map(r=>r.case),['own_read','south_own_read','approved_cancel']);
assert.equal(capstone.recovery.first.state,'UNCERTAIN');assert.equal(capstone.recovery.after_reopen.state,'DONE');assert.equal(capstone.recovery.final_order.effects,1);assert.equal(capstone.recovery.replay_mutations,0);
for(const row of capstone.attacks){assert.equal(row.unsafe.compromised,true);assert.equal(row.guarded.compromised,false);}
assert.equal(capstone.attacks.length,6);
assert.equal(capstone.mcp.exchanges[2].response.result.structuredContent.order_id,'A-104');assert.equal(capstone.mcp.exchanges[4].response.error.message,'Unknown tool');
for(const [path,digest] of Object.entries(capstone.historical_model_evidence))assert.equal(hash(path),digest);
for(const name of ['run-manifest.json','notebook-execution.json'])for(const [path,digest] of Object.entries(json(`data/part-ix/${name}`).inputs_sha256))assert.equal(hash(path),digest,`${name}: ${path}`);
for(const [name,digest] of Object.entries(json('data/part-ix/run-manifest.json').outputs_sha256))assert.equal(hash(`data/part-ix/${name}`),digest);
for(const row of json('data/part-ix/notebook-execution.json').executions){
 assert.equal(hash(row.notebook),row.artifact_sha256);
 const cells=json(row.notebook).cells.filter(c=>c.cell_type==='code');assert.equal(cells.length,row.code_cells);
 assert.ok(cells.every(c=>c.execution_count>0&&!c.outputs.some(o=>o.output_type==='error')));
}
const runbook=json('data/part-ix/runbook-run.json');assert.equal(runbook.input_sha256,hash('docs/part-ix-runbook.md'));assert.equal(runbook.status,'passed');assert.equal(runbook.cohort.filter(n=>n==='rc-b').length,1);
for(const row of json('data/part-ix/risk-register-v1.json').entries){assert.ok(row.owner&&row.residual);for(const path of row.evidence_paths)assert.ok(existsSync(new URL(path,root)));}
for(const file of readdirSync(new URL('code/part-ix/',root)).filter(f=>f.endsWith('.py')))assert.doesNotMatch(read(`code/part-ix/${file}`),/[\u3400-\u9fff]/,`English implementation: ${file}`);
for(const locale of ['en','zh-hans'])assertPublicationState(read(`src/content/docs/${locale}/primer-http.md`).split('---')[1], `${locale}/primer-http`);
console.log('Validated Part IX bilingual mechanisms, static figures, independent arithmetic, HTTP/fault/release evidence, inherited comparisons, provenance and executed notebooks.');
