// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { BOOK_BASE, BOOK_SITE, BOOK_LOCALES } from '../src/config/book.mjs';
const root = new URL('../', import.meta.url);
const output = new URL((process.argv[2] ?? 'dist').replace(/\/?$/, '/'), root);
const drafts = [];
const publishedPages = [];
const fixtureMarkers = { 'ch-01': 'scripted-fixture-v1', 'ch-02': 'journey-table-v1', 'ch-03': 'toy-longest-v1', 'ch-04': 'char-ngram-v1' };
const forbiddenMarkers = Object.entries(fixtureMarkers).filter(([id]) => /draft:\s*true/.test(readFileSync(new URL(`src/content/docs/en/${id}.md`,root),'utf8'))).map(([, marker]) => marker);
for (const locale of BOOK_LOCALES) {
  for (const filename of readdirSync(new URL(`src/content/docs/${locale}/`, root)).filter((name) => name.endsWith('.md'))) {
    const id = filename.slice(0, -3);
    const source = readFileSync(new URL(`src/content/docs/${locale}/${filename}`, root), 'utf8');
    if (/^draft:\s*true\s*$/m.test(source)) {
      drafts.push(`${locale}/${id}`);
      assert.equal(existsSync(new URL(`${locale}/${id}/index.html`, output)), false, `Draft route leaked: ${locale}/${id}`);
    } else {
      const route = `${locale}/${id === 'index' ? '' : `${id}/`}`;
      assert.ok(existsSync(new URL(`${route}index.html`, output)), `Published route missing: ${route}`);
      publishedPages.push({ locale, id, route, date: source.match(/^published:\s*(\d{4}-\d{2}-\d{2})\s*$/m)?.[1] });
    }
  }
}
function inspect(directory) {
  for (const entry of readdirSync(directory, {withFileTypes:true})) {
    const path = new URL(entry.name + (entry.isDirectory()?'/':''), directory);
    if (entry.isDirectory()) inspect(path);
    else if (/\.(js|json|map)$/.test(entry.name)) {
      const text = readFileSync(path, 'utf8');
      for (const marker of forbiddenMarkers) assert.ok(!text.includes(marker), `Draft fixture ${marker} leaked into ${path}`);
      for (const draft of drafts) assert.ok(!text.includes(`/books/understanding-llms/${draft}/`), `Draft route in client asset ${path}`);
    }
    else if (/\.(html|xml)$/.test(entry.name)) {
      const text = readFileSync(path,'utf8');
      for (const draft of drafts) assert.ok(!text.includes(`/books/understanding-llms/${draft}/`), `Draft link in ${path}`);
      assert.ok(!text.includes('<book-lab'), `Draft interactive content in ${path}`);
    }
  }
}
inspect(output);
const searchDirectory = new URL('pagefind/fragment/', output);
const indexedURLs = [];
for (const name of readdirSync(searchDirectory).filter((name) => name.endsWith('.pf_fragment'))) {
  const decoded = gunzipSync(readFileSync(new URL(name, searchDirectory))).toString('utf8');
  assert.ok(decoded.startsWith('pagefind_dcd'), 'Unknown Pagefind fragment encoding: review the installed format');
  const fragment = JSON.parse(decoded.slice('pagefind_dcd'.length));
  const route = fragment.url.replace(/^\/books\/understanding-llms/, '').replace(/^\//, '');
  assert.ok(!drafts.includes(route.replace(/\/$/, '')), `Draft is searchable: ${route}`);
  assert.ok(existsSync(new URL(`${route}index.html`, output)), `Search fragment has no built page: ${route}`);
  indexedURLs.push(route);
}
const sitemap = readFileSync(new URL('sitemap-0.xml', output), 'utf8');
for (const { route } of publishedPages) {
  assert.ok(indexedURLs.includes(route), `Published page missing from search: ${route}`);
  assert.ok(sitemap.includes(`${BOOK_SITE}${BOOK_BASE}/${route}`), `Published page missing from sitemap: ${route}`);
}
for (const locale of BOOK_LOCALES) {
  const feed = readFileSync(new URL(`${locale}/rss.xml`, output), 'utf8');
  const items = [...feed.matchAll(/<item>([\s\S]*?)<\/item>/g)].map(match => match[1]);
  const chapters = publishedPages.filter(page => page.locale === locale && /^ch-\d{2}$/.test(page.id));
  assert.equal(items.length, chapters.length, `${locale}: feed must include every published chapter exactly once`);
  const roadmap = readFileSync(new URL(`${locale}/roadmap/index.html`, output), 'utf8');
  for (const chapter of chapters) {
    const href = `${BOOK_SITE}${BOOK_BASE}/${chapter.route}`;
    const item = items.find(item => item.includes(`<link>${href}</link>`));
    assert.ok(item, `Published chapter missing from RSS: ${chapter.route}`);
    const date = item.match(/<pubDate>(.*?)<\/pubDate>/)?.[1];
    assert.equal(new Date(date).toISOString().slice(0, 10), chapter.date, `${chapter.route}: RSS release date`);
    assert.ok(roadmap.includes(`href="${BOOK_BASE}/${chapter.route}"`), `Published chapter missing from roadmap: ${chapter.route}`);
  }
}
console.log(`Verified ${drafts.length} draft routes and links are excluded; all ${publishedPages.length} public language pages are built, indexed and in the sitemap; both chapter feeds and roadmaps are complete.`);
