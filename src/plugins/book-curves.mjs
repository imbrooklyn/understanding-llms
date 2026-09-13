// SPDX-License-Identifier: Apache-2.0
import { readFileSync } from 'node:fs';
const escape = (value) => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);

export function trainingCurve(figure, locale) {
  if (figure.structure === 'mini-gpt-curve') return miniGptCurve(figure, locale);
  if (figure.structure !== 'training-curve') return null;
  const run = JSON.parse(readFileSync(new URL('../../data/part-ii/classifier-run.json', import.meta.url), 'utf8'));
  const label = (key) => escape(figure.labels[key][locale]);
  const x = (step) => 64 + step / 600 * 500;
  const y = (loss) => 260 - loss / 10 * 210;
  const path = (split) => run.curve.map((row, index) => `${index ? 'L' : 'M'}${x(row.step).toFixed(2)},${y(row[split].loss).toFixed(2)}`).join(' ');
  if (run.curve.some(row => row.validation.loss > 10 || row.train.loss > 10)) throw new Error('Training figure axis range exceeded');
  return `<div class="book-plot-scroll"><svg viewBox="0 0 600 320" aria-hidden="true">
    <g stroke="currentColor" fill="none" opacity=".3">${[0,2,4,6,8,10].map(tick => `<path d="M64 ${y(tick)} H564"/>`).join('')}</g>
    <g stroke="currentColor" fill="none" stroke-width="2"><path d="M64 50 V260 H564"/><path d="${path('train')}"/><path d="${path('validation')}" stroke-dasharray="7 4"/></g>
    <path d="M${x(run.selected_step)} 50 V260" stroke="currentColor" stroke-dasharray="2 5" opacity=".7"/>
    <g fill="currentColor" font-size="16" font-family="var(--sl-font-system)">
      <text x="64" y="26">${label('y')}</text><text x="470" y="307">${label('x')}</text>
      ${[0,2,4,6,8,10].map(tick => `<text x="48" y="${y(tick)+5}" text-anchor="end">${tick}</text>`).join('')}
      ${[0,100,300,600].map(tick => `<text x="${x(tick)}" y="283" text-anchor="middle">${tick}</text>`).join('')}
    </g></svg></div><p class="figure-flow">${label('legend')} ${label('selection')}</p>`;
}

function miniGptCurve(figure, locale) {
  const run = JSON.parse(readFileSync(new URL('../../data/mini-gpt/training-run.json', import.meta.url), 'utf8'));
  const label = (key) => escape(figure.labels[key][locale]);
  const x = (step) => 64 + step / 600 * 500;
  const y = (loss) => 260 - loss / 6 * 210;
  for (const row of run.curve) {
    if (![row.train_loss, row.validation_loss].every(value => Number.isFinite(value) && value >= 0 && value <= 6)
      || row.step < 0 || row.step > 600) throw new Error('Mini GPT figure axis range exceeded');
  }
  const path = (key) => run.curve.map((row, i) => `${i ? 'L' : 'M'}${x(row.step).toFixed(2)},${y(row[key]).toFixed(2)}`).join(' ');
  const markers = run.curve.map(row => `<circle cx="${x(row.step)}" cy="${y(row.train_loss)}" r="3"/><rect x="${x(row.step)-3}" y="${y(row.validation_loss)-3}" width="6" height="6"/>`).join('');
  return `<div class="book-plot-scroll"><svg viewBox="0 0 600 320" aria-hidden="true">
    <g stroke="currentColor" fill="none" opacity=".25">${[0,1,2,3,4,5,6].map(tick => `<path d="M64 ${y(tick)} H564"/>`).join('')}</g>
    <g stroke="currentColor" fill="none" stroke-width="2"><path d="M64 50 V260 H564"/><path d="${path('train_loss')}"/><path d="${path('validation_loss')}" stroke-dasharray="7 4"/></g>
    <path d="M${x(run.selected_step)} 50 V260" stroke="currentColor" stroke-dasharray="2 5" opacity=".7"/>
    <g fill="currentColor">${markers}</g>
    <g fill="currentColor" font-size="16" font-family="var(--sl-font-system)">
      <text x="64" y="26">${label('y')}</text><text x="564" y="311" text-anchor="end">${label('x')}</text>
      ${[0,1,2,3,4,5,6].map(tick => `<text x="48" y="${y(tick)+5}" text-anchor="end">${tick}</text>`).join('')}
      ${[0,50,150,300,450,600].map(tick => `<text x="${x(tick)}" y="283" text-anchor="middle">${tick}</text>`).join('')}
    </g></svg></div><p class="figure-flow">${label('legend')} ${label('selection')}</p>`;
}
