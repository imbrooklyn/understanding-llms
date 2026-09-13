// SPDX-License-Identifier: Apache-2.0
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { renderFigure } from '../src/plugins/remark-book.mjs';

test('Mini GPT curve plots the actual measurements with both line and marker distinctions', () => {
  const run=JSON.parse(readFileSync(new URL('../data/mini-gpt/training-run.json',import.meta.url),'utf8'));
  for(const locale of ['en','zh-hans']) {
    const html=renderFigure('ch-21/training-curve',locale);
    assert.equal((html.match(/<circle /g)??[]).length,run.curve.length);
    assert.equal((html.match(/<rect /g)??[]).length,run.curve.length);
    for(const row of run.curve) {
      const x=64+row.step/600*500, y=260-row.train_loss/6*210;
      assert.ok(html.includes(`cx="${x}" cy="${y}"`));
    }
    assert.match(html,/stroke-dasharray="7 4"/);
    assert.ok(html.includes(`M${64+run.selected_step/600*500} 50 V260`));
    assert.doesNotMatch(html,/<script|<button|<input|undefined|NaN/);
  }
});
