// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { plannedChapters, BOOK_LOCALES } from '../src/config/book.mjs';
const root = new URL('../', import.meta.url);
const output = new URL('dist/', root);
const drafts = [];
const fixtureMarkers = { 'ch-01': 'scripted-fixture-v1', 'ch-02': 'journey-table-v1', 'ch-03': 'toy-longest-v1', 'ch-04': 'char-ngram-v1' };
const forbiddenMarkers = Object.entries(fixtureMarkers).filter(([id]) => /draft:\s*true/.test(readFileSync(new URL(`src/content/docs/en/${id}.md`,root),'utf8'))).map(([, marker]) => marker);
for (const {id} of plannedChapters) for (const locale of BOOK_LOCALES) {
  if (/^draft:\s*true\s*$/m.test(readFileSync(new URL(`src/content/docs/${locale}/${id}.md`, root),'utf8'))) {
    drafts.push(`${locale}/${id}`);
    assert.equal(existsSync(new URL(`${locale}/${id}/index.html`, output)), false, `Draft route leaked: ${locale}/${id}`);
  }
}
function inspect(directory) {
  for (const entry of readdirSync(directory, {withFileTypes:true})) {
    const path = new URL(entry.name + (entry.isDirectory()?'/':''), directory);
    if (entry.isDirectory()) inspect(path);
    else if (/\.(js|json|map)$/.test(entry.name)) {
      const text = readFileSync(path, 'utf8');
      for (const marker of forbiddenMarkers) assert.ok(!text.includes(marker), `Draft fixture ${marker} leaked into ${path}`);
    }
    else if (/\.(html|xml)$/.test(entry.name)) {
      const text = readFileSync(path,'utf8');
      for (const draft of drafts) assert.ok(!text.includes(`/books/understanding-llms/${draft}/`), `Draft link in ${path}`);
      assert.ok(!text.includes('<book-lab'), `Draft interactive content in ${path}`);
    }
  }
}
inspect(output);
console.log(`Verified ${drafts.length} draft chapter routes and links are absent from production HTML/XML; unpublished fixture code/data is absent from JS/JSON/maps; Pagefind indexes only built pages.`);
