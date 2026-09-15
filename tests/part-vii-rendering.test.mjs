// SPDX-License-Identifier: Apache-2.0
import { test } from 'node:test';
import assert from 'node:assert/strict';
import remarkBook from '../src/plugins/remark-book.mjs';

test('HTTP primer renders localized static figures without acquiring chapter numbers', () => {
  for (const locale of ['en', 'zh-hans']) {
    const heading = { type: 'heading', depth: 2, children: [{ type: 'text', value: 'HTTP' }] };
    const figure = { type: 'code', lang: 'book-figure', value: 'ch-42/http' };
    remarkBook()({ children: [heading, figure] }, { path: `/docs/${locale}/primer-http.md` });
    assert.deepEqual(heading.children, [{ type: 'text', value: 'HTTP' }]);
    assert.equal(heading.data, undefined);
    assert.equal(figure.type, 'html');
    assert.match(figure.value, /class="book-figure"/);
    assert.match(figure.value, locale === 'en' ? /Request/ : /请求/);
    assert.doesNotMatch(figure.value, /<button|<input|<script|undefined|NaN/);
  }
});

test('chapter numbering and unsupported teaching controls retain their boundaries', () => {
  const heading = { type: 'heading', depth: 2, children: [{ type: 'text', value: 'Evidence' }] };
  remarkBook()({ children: [heading] }, { path: '/docs/en/ch-40.md' });
  assert.equal(heading.children[0].value, '40.1 ');
  assert.equal(heading.data.hProperties.id, 's-40-1');
  assert.throws(() => remarkBook()({ children: [{ type: 'code', lang: 'book-lab' }] },
    { path: '/docs/en/primer-http.md' }), /unsupported/);
});
