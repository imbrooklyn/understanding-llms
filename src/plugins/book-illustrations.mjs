// SPDX-License-Identifier: Apache-2.0
import { readFileSync } from 'node:fs';
import { trainingCurve } from './book-curves.mjs';
import { budgetCurve } from './book-budget-curve.mjs';
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
const data = (name) => JSON.parse(readFileSync(new URL(`../../data/part-i/${name}.json`,import.meta.url),'utf8'));

export function workedIllustration(structure,locale,figure = {}) {
  if (structure === 'budget-curve') return budgetCurve(figure, locale);
  const curve = trainingCurve(figure, locale);
  if (curve) return curve;
  const t = (en,zh) => locale === 'en' ? en : zh;
  if (structure === 'cosine') {
    const vectors = figure.vectors;
    const origin = [240, 215], scale = 115;
    return `<svg class="coordinate-figure" viewBox="0 0 480 300" aria-hidden="true"><defs><marker id="vector-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
      <g stroke="currentColor" stroke-width="1" opacity=".4"><path d="M 45 215 H 430 M 240 270 V 30"/><path d="M 125 211 V 219 M 355 211 V 219 M 236 100 H 244"/></g>
      <path d="M 355 215 V 100 H 240" fill="none" stroke="currentColor" stroke-dasharray="4 5" opacity=".5"/>
      ${vectors.map(([x,y],i) => `<path d="M ${origin[0]} ${origin[1]} L ${origin[0]+x*scale} ${origin[1]-y*scale}" fill="none" stroke="currentColor" stroke-width="${i === 1 ? 3 : 2}" ${i === 2 ? 'stroke-dasharray="7 4"' : ''} marker-end="url(#vector-arrow)"/>`).join('')}
      <g fill="currentColor" font-size="17" font-family="var(--sl-font-mono)"><text x="252" y="244">0</text><text x="94" y="248">−1</text><text x="350" y="248">1</text><text x="211" y="106">1</text><text x="403" y="244">x</text><text x="253" y="43">y</text><text x="271" y="194">u=[1,0]</text><text x="290" y="77">v=[1,1]</text><text x="52" y="192">w=[−1,0]</text></g></svg><p class="figure-flow">${t('u · v = 1; |u| = 1; |v| = √2. Opposite pair: u and w.', 'u · v = 1；|u| = 1；|v| = √2。u 与 w 的方向相反。')}</p>`;
  }
  if (structure === 'lookup') {
    const vocabulary=data('tokenizer').versions['toy-longest-v1'];
    return `<p><strong>${t('One word → two pieces → two numerical rows','一个词 → 两个片段 → 两行数值')}</strong></p><div class="lookup-source"><code>cats</code><span aria-hidden="true">↓</span><span><b>cat</b> | <b>s</b></span></div>${[16,17].map((id,i) => `<div class="lookup-walk"><div><small>${t('Piece','片段')} ${i+1}</small><strong>${esc(vocabulary.pieces[id])}</strong></div><span aria-hidden="true">→</span><div><small>${t('Vocabulary address','词表编号')}</small><strong>${id}</strong></div><span aria-hidden="true">→</span><div><small>${t(`Read stored row ${id}`,`读取第 ${id} 号行`)}</small><strong>[${vocabulary.embeddings[id].join(', ')}]</strong></div></div>`).join('')}<p class="figure-flow">${t('Keep the two retrieved rows in input order: [[1,0], [0,1]]. Nothing here adds or multiplies the IDs.', '按输入顺序保留取出的两行：[[1,0], [0,1]]。这里没有对 ID 做加法或乘法。')}</p>`;
  }
  if(structure === 'count-predict') {
    const corpus=data('ngram').train;
    const successors=corpus.flatMap((text) => Array.from(text).flatMap((token,i,a) => token === 'a' && a[i+1] ? [a[i+1]] : []));
    return `<p><strong>${t('Follow only the arrows leaving a','只看 a 后面接什么')}</strong></p><div class="corpus-strips">${corpus.map((text,i) => `<div><small>${t('Example','样例')} ${i+1}</small><span>BOS → <b>a → ${esc(text[1])}</b> → EOS</span></div>`).join('')}</div><div class="ticket-bag"><span>${t('Collected successors:','a 后面依次是：')}</span>${successors.map((token) => `<b>${esc(token)}</b>`).join('')}</div><div class="fraction-choices"><div><strong>b: 2 / 3</strong><span>${t('Two of the three tickets','三张中的两张')}</span><div aria-hidden="true"><i></i><i></i><i class="empty"></i></div></div><div><strong>c: 1 / 3</strong><span>${t('One of the three tickets','三张中的一张')}</span><div aria-hidden="true"><i></i><i class="empty"></i><i class="empty"></i></div></div></div><p class="figure-flow">${t('Freeze this table. The next operation can take either branch ↓','计数表不再改动。接下来有两种用法 ↓')}</p><div class="diagram-fork"><div><strong>${t('Generate','生成')}</strong><p>${t('Choose b or c using these shares, append it, then look up the next row.','按这里的概率选 b 或 c，接到序列末尾，再查下一行。')}</p></div><div><strong>${t('Evaluate','评测')}</strong><p>${t('If the supplied next token is b, read 2/3. If it is c, read 1/3.','下一项已知是 b，就取概率 2/3；已知是 c，就取 1/3。')}</p></div></div><p>${t('Both branches read the counts. Neither adds a training observation.','两种用法都只读取计数，不增加训练样本。')}</p>`;
  }
  return null;
}
