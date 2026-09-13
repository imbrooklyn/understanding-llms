// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const root = new URL('../', import.meta.url);
const json = path => JSON.parse(readFileSync(new URL(path,root),'utf8'));
const hash = path => createHash('sha256').update(readFileSync(new URL(path,root))).digest('hex');
const near = (a,b) => assert.ok(Math.abs(a-b)<1e-11, `${a} differs from ${b}`);
export function checkPartVNumbers() {
  const d=json('data/part-v/mechanisms.json'), r=json('data/part-v/derived-run.json'), e=json('data/part-v/expected.json');
  for (const [path,digest] of Object.entries(r.inputs_sha256)) assert.equal(hash(path),digest,`Stale derived input: ${path}`);
  d.budgets.forEach((b,i)=>{
    assert.equal(6n*BigInt(b.parameters)*BigInt(b.training_tokens),BigInt(e.budget_flops[i]));
    assert.equal(r.budget_flops[i],e.budget_flops[i]);assert.equal(r.lifecycle_flops[i],e.lifecycle_flops[i]);
  });
  assert.deepEqual(r.rotation_dots,[1,0,0,-1]);near(r.rms[0],3/Math.sqrt(25/2));near(r.rms[1],4/Math.sqrt(25/2));
  near(r.swiglu.output[0],(2*Math.E-3)/(1+Math.E));near(r.swiglu.output[1],-3/(1+Math.E));
  assert.deepEqual(r.kv_bytes_per_layer,[2**21,2**19,2**18]);
  assert.equal(r.architecture.total_parameters,20e6+4*10e6);assert.equal(r.architecture.active_parameters,20e6+2*10e6);
  assert.deepEqual(r.architecture.linear.map(x=>x.output),[4,6/3,9/4]);
  assert.equal(r.training.state_bytes,1e6*(2+2+4+4+4));assert.equal(r.training.activation_bytes,2*128*64*4*10*2);
  assert.equal(r.training.total_bytes,e.unsharded_total_bytes);assert.equal(r.training.with_headroom_bytes,e.with_headroom_bytes);
  near(r.training.weighted_gradient,(2*1+6*3)/8);
  assert.deepEqual(r.intervention.map(x=>x.margin),[4,-4,4,-4,-4,4]);assert.deepEqual(r.rescue,[1,0]);
  assert.deepEqual(r.sampling.find(x=>x.policy==='temperature-1').probabilities,[4/8,2/8,1/8,1/8]);
  const top=r.sampling.filter(x=>x.policy.startsWith('top-p-'));
  assert.deepEqual(top.map(x=>x.probabilities.filter(p=>p>0).length),[1,2,2,3]);
  r.sampling.forEach(x=>near(x.probabilities.reduce((a,b)=>a+b,0),1));
  const temp=r.sampling.find(x=>x.policy==='temperature-2').probabilities;
  [2,Math.sqrt(2),1,1].forEach((x,i)=>near(temp[i],x/(4+Math.sqrt(2))));
  assert.deepEqual(r.beam['1'][0].tokens,['A','EOS']);assert.deepEqual(r.beam['2'][0].tokens,['B','EOS']);near(r.beam['2'][0].probability,.4*.9);
  assert.equal(r.inference.ttft_ms,150);assert.deepEqual(r.inference.gaps_ms,[40,45,35]);assert.equal(r.inference.tpot_ms,(270-150)/3);
  assert.deepEqual(r.small_cache_bytes,[8,9,10].map(n=>2*2*n*2*4*2));assert.equal(r.large_cache_bytes,384*1024**2);
  assert.deepEqual(r.quantization.integers,[-2,0,1,4]);assert.deepEqual(r.quantization.decoded,[-1,0,.5,2]);
  ['serial','continuous'].forEach(name=>d.serving.requests.forEach((request,i)=>{
    const times=d.serving[name][request.id], actual=r.serving[name].requests[i];
    assert.equal(actual.ttft_ms,times[0]-request.arrival_ms);
    assert.equal(actual.tpot_ms,times.length===1?null:(times.at(-1)-times[0])/(times.length-1));
  }));
  near(r.serving.serial.throughput_tokens_per_second,6/.36);near(r.serving.continuous.throughput_tokens_per_second,6/.2);
  near(r.serving.serial.assumed_dollars,.36/3600*2);near(r.serving.continuous.assumed_dollars,.2/3600*2);
  r.speculation.accept.forEach((a,i)=>near(a,[.75,1][i]));assert.deepEqual(r.speculation.residual,[0,1]);
  assert.deepEqual(r.calibration.substring,{tp:3,fp:2,tn:1,fn:0});assert.deepEqual(r.calibration.strict,{tp:1,fp:0,tn:3,fn:2});
  assert.deepEqual(r.pipeline.stage_counts,[8,7,6,6,5]);
  const run=json('data/knowledge-assistant/ka1-run-v1.json'), review=json('data/knowledge-assistant/ka1-adjudication-v1.json'), freeze=json('data/knowledge-assistant/ka1-freeze-v1.json');
  assert.ok(Date.parse(freeze.recorded_at)<Date.parse(run.recorded_at));assert.equal(review.run_sha256,hash('data/knowledge-assistant/ka1-run-v1.json'));
  assert.equal(review.contract_sha256,hash('data/knowledge-assistant/ka1-contract-v1.json'));
  for(const record of [freeze,run,json('data/part-v/generation-run.json')]) for(const [path,digest] of Object.entries(record.inputs_sha256)) assert.equal(hash(path),digest,`Stale measured input: ${path}`);
  assert.equal(run.rows.length,144);assert.equal(review.rows.length,144);
  const key = r=>[r.candidate,r.case,r.locale,r.policy,r.repeat,r.seed].join('|');
  assert.equal(new Set(run.rows.map(key)).size,144);
  for(const [i,row] of run.rows.entries()) {
    const label=review.rows[i];assert.equal(key(row),key(label));
    assert.equal(label.completion_sha256,createHash('sha256').update(row.output.completion).digest('hex'));
    assert.ok([0,1,2].includes(label.semantic_score));assert.ok(label.reason.length>20);
    assert.ok(Number.isFinite(row.elapsed_ms)&&row.elapsed_ms>=0);
  }
  for(const summary of review.summary) {
    const subset=run.rows.filter(row=>['candidate','policy','locale'].every(k=>row[k]===summary[k]));
    const labels=review.rows.filter(row=>['candidate','policy','locale'].every(k=>row[k]===summary[k]));
    assert.equal(subset.length,18);assert.equal(subset.filter(x=>x.strict_match).length,summary.strict_passes);
    assert.equal(labels.filter(x=>x.semantic_score===2).length,summary.semantic_passes);
    const cases=[...new Set(labels.map(x=>x.case))];assert.equal(cases.length,6);
    assert.equal(cases.filter(c=>labels.filter(x=>x.case===c).every(x=>x.semantic_score===2)).length,summary.stable_semantic_cases);
    const sorted=subset.map(x=>x.elapsed_ms).sort((a,b)=>a-b);near((sorted[8]+sorted[9])/2,summary.median_complete_call_ms);near(sorted[17],summary.p95_complete_call_ms);
    assert.equal(summary.decision,'reject');
  }
  assert.equal(review.rows.filter(x=>x.semantic_score===2).length,7);
  const gen=json('data/part-v/generation-run.json');assert.equal(gen.rows.length,36);assert.equal(gen.rows.filter(x=>x.strict_match).length,0);
  for(const path of ['data/mini-gpt/data-card-v2.json','data/knowledge-assistant/data-card-v2.json']) {
    const card=json(path);assert.equal(hash(card.source),card.source_sha256);assert.ok(JSON.stringify(card).includes('2026-09-13'));assert.ok(JSON.stringify(card).includes('CC BY-SA'));
  }
  const note=json('data/knowledge-assistant/ka1-provenance-note-v1.json');
  assert.equal(note.contract_sha256,hash(note.frozen_contract));assert.ok(Date.parse(note.recorded_at)>Date.parse(run.recorded_at));
  return { derived:r, run, review, gen };
}
