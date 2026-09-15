// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { assertPublicationState } from '../scripts/publication-state.mjs';
import { readFileSync } from 'node:fs';

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

test('The September 15 release promotes only its declared bilingual lessons', () => {
  const root = new URL('../', import.meta.url);
  const release = JSON.parse(readFileSync(new URL('data/releases/2026-09-15-publication.json', root), 'utf8'));
  const groups = [release.previous_published_ids, release.promoted_ids, release.remaining_drafts];
  const ids = groups.flat();
  assert.equal(new Set(ids).size, 60, 'Every chapter, primer and extension has one publication state');
  assert.equal(ids.length, 60, 'Publication groups must not overlap');
  for (const locale of ['en', 'zh-hans']) {
    for (const id of ids) {
      const source = readFileSync(new URL(`src/content/docs/${locale}/${id}.md`, root), 'utf8');
      const state = assertPublicationState(source.split('---')[1], `${locale}/${id}`);
      if (release.remaining_drafts.includes(id)) assert.equal(state.draft, true, `${id}: unauthorized promotion`);
      else {
        const date = release.promoted_ids.includes(id) ? release.published
          : /^ch-0[1-4]$/.test(id) ? '2026-09-10' : '2026-09-13';
        assert.deepEqual(state, { draft: false, published: date }, `${locale}/${id}: release date`);
      }
    }
  }
});
