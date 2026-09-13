// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';

export function assertPublicationState(frontmatter, label) {
  assert.doesNotMatch(frontmatter, /^(?:pubDate|date):/m, `${label}: use published for the release date`);
  const draftFields = [...frontmatter.matchAll(/^draft:\s*(.*?)\s*$/gm)];
  const dateFields = [...frontmatter.matchAll(/^published:\s*(.*?)\s*$/gm)];
  assert.ok(draftFields.length <= 1 && dateFields.length <= 1, `${label}: duplicate publication fields`);
  if (draftFields.length) assert.match(draftFields[0][1], /^(true|false)$/, `${label}: draft must be boolean`);
  const draft = draftFields[0]?.[1] === 'true';
  const published = dateFields[0]?.[1];
  if (draft) {
    assert.equal(published, undefined, `${label}: a draft cannot have a release date`);
  } else {
    assert.match(published ?? '', /^\d{4}-\d{2}-\d{2}$/, `${label}: published content needs YYYY-MM-DD`);
    const parsed = new Date(`${published}T00:00:00.000Z`);
    assert.ok(Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === published,
      `${label}: invalid calendar date`);
  }
  return { draft, published };
}
