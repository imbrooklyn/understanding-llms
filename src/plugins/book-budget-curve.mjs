// SPDX-License-Identifier: Apache-2.0
import { readFileSync } from 'node:fs';
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'})[c]);

export function budgetCurve(figure, locale) {
  const data = JSON.parse(readFileSync(new URL('../../data/part-vi/budget-v1.json', import.meta.url), 'utf8'));
  const caps = data.budget.maxima;
  const series = data.independent_expected.primary_correct;
  const x = cap => 72 + (cap - 1) * 118;
  const y = correct => 278 - correct * 52;
  const label = name => escape(figure.labels[name][locale]);
  const dashes = ['', '8 5', '2 5', '12 4 2 4'];
  function marker(method, px, py) {
    if (method === 'direct') return `<circle cx="${px}" cy="${py}" r="5"/>`;
    if (method === 'steps') return `<rect x="${px-5}" y="${py-5}" width="10" height="10"/>`;
    if (method === 'vote') return `<path d="M${px} ${py-7} l7 12 h-14 Z"/>`;
    return `<path d="M${px} ${py-7} l7 7 l-7 7 l-7 -7 Z"/>`;
  }
  for (const values of Object.values(series)) {
    if (values.length !== caps.length || values.some(value => !Number.isInteger(value) || value < 0 || value > 4)) throw new Error('Budget figure axis range exceeded');
  }
  const lines = Object.entries(series).map(([method, values], index) => {
    const path = values.map((value, i) => `${i ? 'L' : 'M'}${x(caps[i])} ${y(value)}`).join(' ');
    return `<g data-series="${method}" stroke="currentColor" stroke-width="2" fill="none"><path d="${path}" stroke-dasharray="${dashes[index]}"/>${values.map((value, i) => marker(method, x(caps[i]), y(value))).join('')}</g>`;
  }).join('');
  return `<div class="book-plot-scroll"><svg viewBox="0 0 720 354" aria-hidden="true">
    <g stroke="currentColor" opacity=".2">${[0,1,2,3,4].map(value => `<path d="M72 ${y(value)} H662"/>`).join('')}</g>
    <path d="M72 58 V278 H662" fill="none" stroke="currentColor" stroke-width="2"/>${lines}
    <g fill="currentColor" font-size="17" font-family="var(--sl-font-system)">
      <text x="72" y="30">${label('y')}</text><text x="662" y="340" text-anchor="end">${label('x')}</text>
      ${[0,1,2,3,4].map(value => `<text x="55" y="${y(value)+6}" text-anchor="end">${value}</text>`).join('')}
      ${caps.map(cap => `<text x="${x(cap)}" y="305" text-anchor="middle">${cap}</text>`).join('')}
    </g></svg></div><p class="figure-flow">${label('legend')}</p><p class="figure-flow">${label('scope')}</p>`;
}
