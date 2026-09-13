// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const json = (name) => JSON.parse(readFileSync(new URL(`../data/${name}.json`, import.meta.url), 'utf8'));
const close = (a, b, tolerance = 1e-12) => assert.ok(Number.isFinite(a) && Math.abs(a-b) <= tolerance, `${a} differs from ${b}`);
const vectorClose = (a, b) => { assert.equal(a.length, b.length); a.forEach((v,i) => Array.isArray(v) ? vectorClose(v,b[i]) : close(v,b[i])); };
const multiply = (a,b) => a.map(row => b[0].map((_, j) => row.reduce((sum,v,k) => sum+v*b[k][j],0)));
const transpose = (a) => a[0].map((_,i) => a.map(row => row[i]));
const probabilities = (row) => { const m=Math.max(...row), e=row.map(v=>Math.exp(v-m)), s=e.reduce((a,b)=>a+b,0); return e.map(v=>v/s); };
const norm = (row) => { const m=row.reduce((a,b)=>a+b,0)/row.length, v=row.reduce((a,b)=>a+(b-m)**2,0)/row.length; return row.map(x=>(x-m)/Math.sqrt(v+1e-5)); };

export function checkPartIVNumbers() {
  const a = json('part-iv/attention'), masks = json('part-iv/mask-cases'), run = json('part-iv/numpy-run');
  const q=multiply(a.X,a.WQ), k=multiply(a.X,a.WK), v=multiply(a.X,a.WV);
  const dots=multiply(q,transpose(k)), scores=dots.map(row=>row.map(x=>x/Math.sqrt(2)));
  const weights=scores.map(probabilities), output=multiply(weights,v);
  for (const [key, actual] of Object.entries({Q:q,K:k,V:v,dots,scores,weights,output})) {
    if (key in a.expected) vectorClose(actual,a.expected[key]);
    vectorClose(actual,run.attention[key]);
  }
  const causal=scores.map((row,i)=>probabilities(row.map((x,j)=>j<=i?x:-Infinity)));
  vectorClose(causal,masks.causal_expected_weights);
  vectorClose(multiply(causal,v),masks.causal_expected_output);
  const padded=causal.map((row,i)=>row.map((x,j)=>masks.query_valid[i]&&j<2?x:0));
  vectorClose(multiply(padded,v),masks.padded_expected_output);
  for (let i=0;i<3;i++) for(let j=0;j<3;j++) {
    assert.equal(masks.causal[i][j],j<=i);
    assert.equal(masks.causal_with_padding[i][j],j<=i&&j<2);
  }
  const leak=masks.leakage;
  close(leak.future_visible_probability,.01*.5+.99);
  close(leak.future_visible_loss,-Math.log(.995));
  close(leak.future_hidden_loss,Math.log(2));
  assert.ok(leak.future_hidden_loss>100*leak.future_visible_loss);
  const joined=a.X.map((row,i)=>row.map((_,h)=>{
    const w=probabilities(a.X.slice(0,i+1).map(key=>row[h]*key[h]));
    return w.reduce((sum,p,j)=>sum+p*a.X[j][h],0);
  }));
  vectorClose(joined,run.multihead.joined);
  vectorClose(multiply(joined,masks.output_projection),masks.multihead_expected);
  const scale=.5/Math.sqrt(.25+1e-5), u=(2*scale-1)/(2*Math.sqrt(((2*scale-1)/2)**2+1e-5));
  vectorClose(run.block.output[0],[1+u,2*scale+u]);
  for(let i=0;i<3;i++) vectorClose(norm(run.block.input[i]),run.block.norm1[i]);

  const models=json('part-iv/architectures').models;
  assert.deepEqual(models.bert.targets,['red',null,null]);
  assert.ok(models.bert.visible.flat().every(Boolean));
  for(const name of ['gpt','t5']) {
    const model=models[name];
    assert.deepEqual(model.input.slice(1),model.targets.slice(0,-1));
    model.visible.forEach((row,i)=>row.forEach((allowed,j)=>assert.equal(allowed,j<=i)));
  }
  assert.equal(models.t5.source_visible.flat().filter(Boolean).length,4);
  assert.equal(models.t5.cross_visible.flat().filter(Boolean).length,10);
  assert.equal(models.t5.visible.flat().filter(Boolean).length,15);

  const tok=json('mini-gpt/tokenizer'), cases=json('part-iv/tokenizer-cases'), traced=json('part-iv/tokenizer-run');
  assert.equal(tok.pieces_hex.length,291);
  assert.deepEqual(tok.special_ids,{BOS:256,EOS:257,PAD:258});
  for(let i=0;i<256;i++) assert.equal(tok.pieces_hex[i],i.toString(16).padStart(2,'0'));
  assert.deepEqual(traced.hand_bpe.map(row=>row.selected),cases.hand_bpe.expected_pairs);
  assert.deepEqual(traced.hand_bpe.map(row=>row.selected_count),[3,3,2,1]);
  let segments=Object.fromEntries(Object.keys(cases.hand_bpe.words).map(word=>[word,[...word,'</w>']]));
  for (const row of traced.hand_bpe) {
    const counts=new Map();
    for(const [word,pieces] of Object.entries(segments)) for(let i=0;i<pieces.length-1;i++) {
      const key=JSON.stringify([pieces[i],pieces[i+1]]); counts.set(key,(counts.get(key)??0)+cases.hand_bpe.words[word]);
    }
    assert.equal(counts.size,row.counts.length);
    for (const item of row.counts) assert.equal(counts.get(JSON.stringify(item.pair)),item.count);
    assert.equal(Math.max(...counts.values()),row.selected_count);
    const tied=[...counts].filter(([,n])=>n===row.selected_count).map(([key])=>JSON.parse(key)).sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:a[1]<b[1]?-1:a[1]>b[1]?1:0);
    assert.deepEqual(row.selected,tied[0]); segments=row.segments;
  }
  assert.deepEqual(segments,cases.hand_bpe.expected_final);
  for(const row of traced.roundtrips) {
    const bytes=Buffer.concat(row.ids.map(id=>Buffer.from(tok.pieces_hex[id],'hex')));
    assert.equal(new TextDecoder('utf-8',{fatal:true}).decode(bytes),row.text);
    assert.equal(bytes.length,row.byte_count);assert.equal([...row.text].length,row.codepoints);assert.equal(row.ids.length,row.token_count);
  }
  assert.throws(()=>new TextDecoder('utf-8',{fatal:true}).decode(new Uint8Array([255])));
  assert.notEqual(cases.normalization_counterexample.raw,cases.normalization_counterexample.normalized_nfc);

  const f=json('mini-gpt/forward'), cfg=json('mini-gpt/config');
  assert.equal(f.parameter_count,291*16+64*16+4*16*16+16*64+64+64*16+16+3*32+16*291+291);
  assert.equal(f.scored_events,32);assert.deepEqual(f.records.map(r=>r.scored_events),[15,17]);
  for(const r of f.records) {assert.equal(r.ids[0],256);assert.equal(r.targets.at(-1),257);assert.deepEqual(r.ids.slice(1),r.targets.slice(0,-1));}
  assert.deepEqual(f.shapes.scores,[2,2,64,64]);assert.deepEqual(f.shapes.logits,[2,64,291]);
  const rows=f.selected_rows;
  vectorClose(rows.block_input,rows.token_embedding.map((x,i)=>x+rows.position_embedding[i]));
  vectorClose(rows.norm1,norm(rows.block_input));
  vectorClose(rows.residual1,rows.block_input.map((x,i)=>x+rows.attention_output[i]));
  vectorClose(rows.ffn_relu,rows.ffn_linear.map(x=>Math.max(0,x)));
  vectorClose(rows.block_output,rows.residual1.map((x,i)=>x+rows.ffn_output[i]));
  close(f.selected_head_scores[0],f.selected_head_query.reduce((sum,x,i)=>sum+x*f.selected_head_key0[i],0)/Math.sqrt(8));
  vectorClose(f.selected_head_weights,probabilities(f.selected_head_scores));
  const p=probabilities(rows.logits)[f.target_id];close(p,f.target_probability);close(-Math.log(p),f.target_loss);
  close(f.zero_logits_loss,Math.log(cfg.vocab_size));close(f.loss,f.scalar_mean_loss);

  const trained=json('mini-gpt/training-run');
  assert.equal(trained.steps.length,cfg.steps);assert.equal(trained.curve.length,13);
  const selected=trained.curve.reduce((best,row)=>row.validation_loss<best.validation_loss?row:best);
  assert.equal(selected.step,50);assert.equal(selected.step,trained.selected_step);
  assert.equal(trained.train_events,521);assert.equal(trained.validation_events,178);
  trained.steps.forEach((row,i)=>{assert.equal(row.step,i+1);assert.equal(row.batch_indices.length,8);assert.ok(row.batch_indices.every(j=>j>=0&&j<24));assert.ok(Number.isFinite(row.batch_loss_before_update));});
  assert.ok(Object.values(trained.resumed_checks).every(x=>x===true));
  assert.ok(Object.values(trained.fresh_process_checks).every(x=>x===true));
  assert.ok(trained.curve.at(-1).train_loss<selected.train_loss && trained.curve.at(-1).validation_loss>selected.validation_loss);
  assert.equal(Object.values(trained.checkpoints).reduce((n,x)=>n+x.bytes,0),966540);

  const generated=json('mini-gpt/generation'), baseline=json('mini-gpt/generation-baseline');
  assert.equal(generated.length,20);assert.equal(baseline.length,12);
  for(const row of baseline.filter(x=>x.mode==='greedy')) assert.ok(generated.some(x=>JSON.stringify(x)===JSON.stringify(row)), 'Original unfavorable greedy probe was removed');
  for(const row of generated) {
    for(let i=1;i<row.trace.length;i++) assert.deepEqual(row.trace[i].context_ids,[...row.trace[i-1].context_ids,row.trace[i-1].chosen_id]);
    assert.ok(row.trace.every(x=>x.chosen_id!==256&&x.chosen_id!==258));
    if(row.stop==='EOS') assert.equal(row.trace.at(-1).chosen_id,257);
    assert.equal(Buffer.from(row.generated_hex,'hex').toString('utf8'),row.completion);
    assert.ok(row.trace.length<=24);assert.ok(row.trace.every(x=>x.context_ids.length<64));
  }
  const red=generated.find(x=>x.checkpoint==='final'&&x.probe_id==='aligned-red'&&x.mode==='greedy');
  assert.deepEqual(red.trace.map(x=>x.chosen_id),[270,46,257]);assert.equal(red.completion,'red.');
  assert.equal(generated.find(x=>x.checkpoint==='final'&&x.probe_id==='changed-color').exact_suffix_match,false);
  return {attention:run, forward:f, trained, generated};
}
