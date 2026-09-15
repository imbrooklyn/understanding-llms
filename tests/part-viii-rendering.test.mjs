// SPDX-License-Identifier: Apache-2.0
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import remarkBook from '../src/plugins/remark-book.mjs';
const figures=['control','loading','recovery','attribution','lifecycle','boundaries','trust'];
for(const locale of ['en','zh-hans']) test(`${locale}: Part VIII figures preserve evidence and accessible static structure`,()=>{
 for(const [i,name] of figures.entries()){
  const id=`ch-${47+i}/${name}`;const source=JSON.parse(readFileSync(new URL(`../src/assets/${id}.json`,import.meta.url),'utf8'));
  const heading={type:'heading',depth:2,children:[{type:'text',value:'Evidence'}]};const block={type:'code',lang:'book-figure',value:id};
  remarkBook()({children:[heading,block]},{path:`/docs/${locale}/ch-${47+i}.md`});
  assert.equal(heading.data.hProperties.id,`s-${47+i}-1`);assert.equal(block.type,'html');assert.ok(block.value.includes(source.caption[locale]));
  if([48,51,53].includes(47+i)) assert.doesNotMatch(block.value,/class="kind-id"/, 'Metadata, receipts and principals are application records, not embedding row IDs');
  assert.match(block.value,/role="img"/);assert.doesNotMatch(block.value,/<script|<button|<details|undefined|NaN/);
 }
});
