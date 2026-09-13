// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const root = new URL('../', import.meta.url);
const json = path => JSON.parse(readFileSync(new URL(path, root), 'utf8'));
const hash = path => createHash('sha256').update(readFileSync(new URL(path, root))).digest('hex');
const near = (a,b) => assert.ok(Math.abs(a-b)<1e-12, a+' != '+b);

export function checkPartVINumbers() {
  const result = json('data/part-vi/mechanism-run-v1.json');
  for (const [path, digest] of Object.entries(result.source_sha256)) assert.equal(hash(path), digest, 'Stale mechanism input: '+path);
  assert.deepEqual(result.sft.ids, [0,1,2,3,4,5,3,6,7,8,3]);
  assert.deepEqual(result.sft.targets, [1,2,3,4,5,3,6,7,8,3]);
  assert.deepEqual(result.sft.mask, [0,0,0,0,0,0,0,1,1,1]);
  near(result.sft.loss, Math.log(16)/3);
  assert.equal(result.sft.audits.length,5);
  assert.deepEqual(result.preference.audits,['keep','reverse','quarantine','tie']);
  near(result.preference.kl, .75*Math.log(1.5)+.25*Math.log(.5));
  near(result.preference.reverse_kl, .5*Math.log(2/3)+.5*Math.log(2));
  near(result.preference.dpo.margin,Math.log(3));
  near(result.preference.dpo.loss,-Math.log(.75));
  assert.deepEqual(result.verifier.map(r=>r.substring),[true,false,true,false,true,true]);
  assert.deepEqual(result.verifier.map(r=>r.exact),[true,false,true,false,false,false]);
  assert.deepEqual(result.verifier.map(r=>r.rule.accepted),[true,false,true,true,false,false]);
  assert.deepEqual(result.verifier.map(r=>r.process),[true,false,false,true,false,false]);
  assert.equal(result.verifier[2].rule.accepted,true);
  assert.equal(result.verifier[2].process,false);

  const budget=json('data/part-vi/budget-v1.json');
  assert.equal(result.budget.length,60);
  const keys=new Set();
  for(const row of result.budget) {
    keys.add([row.order.join(''),row.maximum,row.method].join('|'));
    assert.equal(row.total,4); assert.equal(row.cases.length,4);
    assert.equal(row.correct,row.cases.filter(c=>c.correct).length);
    assert.equal(row.calls,row.cases.reduce((s,c)=>s+c.call_count,0));
    assert.equal(row.tokens,row.cases.reduce((s,c)=>s+c.tokens,0));
    assert.ok(Number.isFinite(row.replay_elapsed_ms)&&row.replay_elapsed_ms>=0);
    for(const [index,c] of row.cases.entries()) {
      const given=budget.cases[index];
      const total=given.costs.reduce((s,cost)=>s+Math.min(cost,given.cap),0);
      assert.equal(given.answer,total);
      assert.equal(c.correct,c.selected===total);
      assert.equal(c.call_count,c.calls.length);
      assert.ok(c.call_count<=row.maximum);
      assert.equal(c.tokens,c.calls.reduce((s,call)=>s+call.input_tokens+call.output_tokens,0));
      for(const call of c.calls) {
        assert.equal(call.input_tokens,call.kind==='verify'?14:9);
        assert.equal(call.output_tokens,call.kind==='verify'||row.method==='direct'?1:5);
      }
      if(row.method==='search') {
        assert.equal(c.call_count%2,0);
        for(let i=0;i<c.calls.length;i+=2) {
          assert.equal(c.calls[i].kind,'generate');assert.equal(c.calls[i+1].kind,'verify');
          const amount=Number(c.calls[i].response.split(' = ')[1]);
          assert.equal(c.calls[i+1].response,amount===total?'accept':'reject');
        }
        if(c.selected!==null) assert.equal(c.calls.at(-1).response,'accept');
      }
    }
  }
  assert.equal(keys.size,60);
  for(const [method,counts] of Object.entries(budget.independent_expected.primary_correct)) {
    assert.deepEqual(result.budget.filter(r=>r.order.join('')==='ABC'&&r.method===method).map(r=>r.correct),counts);
  }
  for(const [method,expected] of Object.entries(budget.independent_expected.budget4)) {
    const row=result.budget.find(r=>r.order.join('')==='ABC'&&r.method===method&&r.maximum===4);
    for(const [field,value] of Object.entries(expected)) assert.equal(row[field],value);
  }
  for(const [method,expected] of Object.entries(budget.independent_expected.repeat_budget4)) {
    assert.deepEqual(result.budget.filter(r=>r.method===method&&r.maximum===4).map(r=>r.correct),expected);
  }
  const last=result.budget.find(r=>r.order.join('')==='CBA'&&r.method==='search'&&r.maximum===6);
  assert.deepEqual([last.correct,last.calls,last.tokens],[4,16,232]);
  assert.deepEqual(result.low_rank.delta,[[2,0,-1],[0,0,0],[-2,0,1],[4,0,-2]]);
  assert.deepEqual(result.low_rank.combined_output,[0,2,4,1]);
  assert.deepEqual(result.low_rank.merged_output,result.low_rank.combined_output);
  assert.equal(result.low_rank.trainable_parameters,7);
  near(result.quantization.original,1.86);near(result.quantization.quantized,2);
  near(result.quantization.original_with_delta,1.96);near(result.quantization.quantized_with_delta,2.1);

  const actual=json('data/knowledge-assistant/ka1-format-run-v1.json');
  const frozen=json('data/knowledge-assistant/ka1-format-freeze-v1.json');
  assert.ok(Date.parse(frozen.recorded_at)<Date.parse(actual.recorded_at));
  assert.equal(actual.parameters_unchanged,true);
  for(const record of [frozen,actual]) for(const [path,digest] of Object.entries(record.inputs_sha256)) assert.equal(hash(path),digest,'Stale KA-1 input: '+path);
  const key=r=>[r.candidate,r.case,r.locale,r.policy,r.repeat,r.seed].join('|');
  const original=new Map(json('data/knowledge-assistant/ka1-run-v1.json').rows.map(r=>[key(r),r]));
  const labels=new Map(json('data/knowledge-assistant/ka1-adjudication-v1.json').rows.map(r=>[key(r),r]));
  const tasks=json('data/knowledge-assistant/ka1-contract-v1.json').cases;
  const amountCases=json('data/knowledge-assistant/ka1-format-adaptation-v1.json').intervention.amount_cases;
  assert.equal(actual.rows.length,144);assert.equal(new Set(actual.rows.map(key)).size,144);
  for(const row of actual.rows) {
    assert.deepEqual(row.output,original.get(key(row)).output);
    assert.equal(row.raw,row.output.completion);
    assert.equal(row.semantic_score,labels.get(key(row)).semantic_score);
    const match=/^([0-9]+)\.$/.exec(row.raw.trim());
    const transformed=amountCases.includes(row.case)&&row.output.valid_utf8&&match?match[1]:row.raw;
    assert.equal(row.normalized,transformed);
    assert.equal(row.changed,row.raw!==row.normalized);
    const accepted=tasks.find(c=>c.id===row.case).strict_accepted[row.locale];
    for(const arm of ['raw','normalized']) assert.equal(row[arm+'_strict'],row.output.valid_utf8&&accepted.includes(row[arm].trim()));
    assert.ok(row.generation_ms>=0&&row.normalization_ms>=0);
  }
  assert.equal(actual.summary.length,16);
  for(const summary of actual.summary) {
    const rows=actual.rows.filter(r=>['candidate','locale','policy'].every(k=>r[k]===summary[k]));
    assert.equal(rows.length,18);
    assert.equal(summary.strict_passes,rows.filter(r=>r[summary.arm+'_strict']).length);
    assert.equal(summary.semantic_passes,rows.filter(r=>r.semantic_score===2).length);
    const cases=[...new Set(rows.map(r=>r.case))]; assert.equal(cases.length,6);
    assert.equal(summary.stable_semantic_cases,cases.filter(c=>rows.filter(r=>r.case===c).every(r=>r.semantic_score===2)).length);
    const durations=rows.map(r=>r.generation_ms+(summary.arm==='normalized'?r.normalization_ms:0)).sort((a,b)=>a-b);
    near(summary.p95_ms,durations[Math.ceil(.95*durations.length)-1]);
    near(summary.median_ms,(durations[8]+durations[9])/2);
    assert.equal(summary.generated_tokens_including_eos,rows.reduce((s,r)=>s+r.output.trace.length,0));
    assert.equal(summary.decision,'reject');
  }
  const selected=actual.summary.filter(s=>s.candidate==='selected-50'&&s.policy==='greedy'&&s.locale==='en');
  assert.deepEqual(selected.map(s=>[s.strict_passes,s.semantic_passes,s.stable_semantic_cases]),[[0,6,2],[6,6,2]]);
  const execution=json('data/part-vi/notebook-execution.json');
  for(const [path,digest]of Object.entries(execution.inputs_sha256))assert.equal(hash(path),digest,'Stale notebook input: '+path);
  for(const record of execution.executions) {
    const notebook=json(record.notebook);
    const cells=notebook.cells.filter(c=>c.cell_type==='code');
    assert.equal(record.status,'passed');assert.equal(cells.length,record.code_cells);
    assert.equal(hash(record.notebook),record.artifact_sha256);
    const code=cells.map(c=>Array.isArray(c.source)?c.source.join(''):c.source).join('\n');
    assert.equal(createHash('sha256').update(code).digest('hex'),record.code_sha256);
    cells.forEach((cell,i)=>{assert.equal(cell.execution_count,i+1);assert.ok(cell.outputs.every(o=>o.output_type!=='error'));});
  }
  return {result,actual,budget};
}

