// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { assertPublicationState } from '../scripts/publication-state.mjs';

test('Drafts and published lessons have distinct valid metadata', () => {
  assert.deepEqual(assertPublicationState('draft: true', 'draft'), { draft: true, published: undefined });
  assert.deepEqual(assertPublicationState('published: 2026-09-13', 'release'), { draft: false, published: '2026-09-13' });
  assert.deepEqual(assertPublicationState('draft: false\npublished: 2024-02-29', 'leap day'), { draft: false, published: '2024-02-29' });
});

test('Publication metadata rejects missing, contradictory and invalid dates', () => {
  for (const frontmatter of ['', 'draft: true\npublished: 2026-09-13', 'published: 2026-02-30', 'published: 2026-13-01',
    'published: 2026-9-13', 'draft: yes', 'draft: false', 'pubDate: 2026-09-13',
    'published: 2026-09-13\npublished: 2026-09-14', 'draft: true\ndraft: false']) {
    assert.throws(() => assertPublicationState(frontmatter, 'invalid fixture'));
  }
});
