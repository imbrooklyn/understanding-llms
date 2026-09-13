// SPDX-License-Identifier: Apache-2.0
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import remarkBook, { renderFigure } from '../src/plugins/remark-book.mjs';
import { checkPartVINumbers } from '../scripts/part-vi-evidence.mjs';
import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

test('Part VI arithmetic, stop/cost invariants and immutable paired evidence',()=>{checkPartVINumbers();});
test('Both languages render through Markdown, math and figure plugins without literal delimiters',async()=>{
  const processor=await createMarkdownProcessor({syntaxHighlight:false,remarkPlugins:[remarkMath,remarkBook],rehypePlugins:[[rehypeKatex,{strict:'error',trust:false}]]});
  for(const locale of ['en','zh-hans'])for(let chapter=34;chapter<=39;chapter++){
    const fileURL=new URL('../src/content/docs/'+locale+'/ch-'+chapter+'.md',import.meta.url);
    const source=readFileSync(fileURL,'utf8').replace(/^---\n[\s\S]*?\n---\n/,'');
    const {code}=await processor.render(source,{fileURL});
    assert.doesNotMatch(code,/\*\*|katex-error|§|<button|<details|<input/);
    assert.match(code,/<figure class="book-figure"/);
    assert.ok(code.includes('id="s-'+chapter+'-1"'));
  }
});
test('Every manuscript fence passes the actual Markdown figure transformation',()=>{
  for(const locale of ['en','zh-hans']) for(let chapter=34;chapter<=39;chapter++){
    const path=new URL('../src/content/docs/'+locale+'/ch-'+chapter+'.md',import.meta.url);
    const source=readFileSync(path,'utf8');
    const children=[...source.matchAll(/\x60{3}book-figure\n([\s\S]*?)\x60{3}/g)].map(m=>({type:'code',lang:'book-figure',value:m[1]}));
    assert.ok(children.length>0);
    const tree={type:'root',children};
    remarkBook()(tree,{path:path.pathname});
    for(const node of tree.children){assert.equal(node.type,'html');assert.match(node.value,/<figure class="book-figure"/);}
  }
});
test('Budget plot uses the declared quota axis and preserves all series points',()=>{
  for(const locale of ['en','zh-hans']) {
    const rendered=renderFigure('ch-37/budget-curve',locale);
    assert.match(rendered,/M72 174 L190 174 L308 174 L426 174 L662 174/);
    assert.match(rendered,/M72 122 L190 122 L308 174 L426 174 L662 174/);
    assert.match(rendered,/M72 278 L190 122 L308 122 L426 70 L662 70/);
    assert.equal((rendered.match(/data-series=/g)??[]).length,4);
    assert.match(rendered,/book-plot-scroll/);
    assert.doesNotMatch(rendered,/<script|<button|NaN|undefined/);
    const source=JSON.parse(readFileSync(new URL('../src/assets/ch-37/budget-curve.json',import.meta.url),'utf8'));
    assert.ok(rendered.includes(source.labels.x[locale]));
  }
});
test('All Part VI parameter nodes retain the shared neutral double-border role',()=>{
  const input=JSON.parse(readFileSync(new URL('../src/assets/ch-39/low-rank-path.json',import.meta.url),'utf8')).lanes[0].nodes[0];
  assert.equal(input.kind,'vector');
  const style=readFileSync(new URL('../src/styles/custom.css',import.meta.url),'utf8');
  assert.match(style,/\.kind-parameter[\s\S]*?border(?:-style)?:[^}]*double/);
  for(const asset of ['ch-34/target-mask','ch-35/preference-paths','ch-36/check-and-train','ch-39/low-rank-path']){
    const rendered=renderFigure(asset,'en');
    assert.match(rendered,/kind-parameter/);assert.doesNotMatch(rendered,/kind-state/);
  }
});
