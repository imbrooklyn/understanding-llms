// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { chapterLabel, plannedChapters } from '../src/config/book.mjs';
const root = new URL('../', import.meta.url);
const read = (file) => readFileSync(new URL(file, root), 'utf8');
const blocks = (text, language) => [...text.matchAll(new RegExp('```' + language + '\\n([^`]+)```', 'g'))].map((match) => match[1].trim());
const sourceURLs = (text) => [...new Set([...text.matchAll(/\]\((https:\/\/[^)]+)\)/g)].map((match) => match[1]))].sort();
for (const chapter of plannedChapters.slice(0,4)) {
  const pages = ['en', 'zh-hans'].map((locale) => read(`src/content/docs/${locale}/${chapter.id}.md`));
  for (const [i, page] of pages.entries()) {
    const locale = ['en', 'zh-hans'][i];
    assert.ok(page.includes(`title: "${chapterLabel(chapter.id, locale)} ${chapter.title[locale]}"`));
    assert.ok(page.includes(chapter.title[locale]), `${chapter.id}: configured title mismatch`);
    assert.doesNotMatch(page, /placeholder|in progress and is visible|仅在本地开发模式可见|^# /m);
    assert.doesNotMatch(page, /^#{2,6} \d+\./m, 'Do not manually duplicate automatic section numbering');
    assert.doesNotMatch(page, /<(?:details|summary|input|select|textarea|button|form|book-lab)\b|```book-lab/i, 'Learning content must be completely static');
    assert.ok(sourceURLs(page).length >= 2, 'Primary sources are required');
    for (const figure of blocks(page, 'book-figure')) assert.ok(existsSync(new URL(`src/assets/${figure}.json`,root)));
    assert.ok(blocks(page, 'book-figure').length >= 1, 'A mechanism figure is required');
    const headings = locale === 'en' ? ['Exercises', 'Solutions', 'Summary'] : ['习题', '参考解答', '本章小结'];
    for (const heading of headings) assert.ok(page.includes(`## ${heading}`), `${chapter.id}: missing ${heading}`);
    const numbered = (heading) => page.split(`## ${heading}\n`)[1]?.split('\n## ')[0].match(/^\d+\. /gm)?.map((line) => parseInt(line));
    const questions = numbered(headings[0]), answers = numbered(headings[1]);
    assert.ok(questions?.length >= 6, 'Provide transfer exercises and reasoned solutions');
    assert.deepEqual(questions, Array.from({length: questions.length}, (_, i) => i + 1), 'Exercise numbers must be consecutive');
    assert.deepEqual(answers, questions, 'Every exercise needs a visible solution with matching number');
    assert.ok(page.includes(`## ${locale === 'en' ? 'References' : '参考文献'}\n`));
    assert.doesNotMatch(page, /\b(?:[EFR]-)?G[1-5](?:-[AB])?\b/, 'Use descriptive case names in textbook prose; keep record IDs in fixtures');
  }
  assert.deepEqual(pages.map((p) => /^draft: true$/m.test(p))[0], pages.map((p) => /^draft: true$/m.test(p))[1]);
  assert.deepEqual([...pages[0].matchAll(/^(#{2,6}) /gm)].map((m) => m[1]), [...pages[1].matchAll(/^(#{2,6}) /gm)].map((m) => m[1]), `${chapter.id}: heading structure differs`);
  assert.deepEqual([...pages[0].matchAll(/\$\$([\s\S]*?)\$\$/g)].map((m) => m[1].trim()), [...pages[1].matchAll(/\$\$([\s\S]*?)\$\$/g)].map((m) => m[1].trim()), `${chapter.id}: display equations differ`);
  const inline = (page) => [...page.matchAll(/(?<!\$)\$(?!\$)([^\n$]+)\$(?!\$)/g)].map((m) => m[1]).sort();
  assert.deepEqual(inline(pages[0]), inline(pages[1]), `${chapter.id}: inline equations differ`);
  assert.deepEqual(sourceURLs(pages[0]), sourceURLs(pages[1]), `${chapter.id}: source coverage differs`);
  const examples = (page) => [...page.matchAll(/(?:Example |例 )(\d+\.\d+)(?: —|——)/g)].map((m) => m[1]);
  const tables = (page) => [...page.matchAll(/(?:Table |表 )(\d+\.\d+)(?: —|——)/g)].map((m) => m[1]);
  assert.deepEqual(examples(pages[0]), examples(pages[1]), `${chapter.id}: worked examples differ`);
  assert.deepEqual(tables(pages[0]), tables(pages[1]), `${chapter.id}: table captions differ`);
  const questionCount = (page) => page.split(/## (?:Exercises|习题)\n/)[1].split('\n## ')[0].match(/^\d+\. /gm).length;
  assert.equal(questionCount(pages[0]), questionCount(pages[1]), `${chapter.id}: exercise counts differ`);
  for (const language of ['book-figure']) assert.deepEqual(blocks(pages[0],language), blocks(pages[1],language));
}
for (const file of ['observations','journey','tokenizer','ngram','expected']) {
  const data = JSON.parse(read(`data/part-i/${file}.json`));
  assert.equal(data.version, 'part-i-v1'); assert.equal(data.license, 'CC-BY-SA-4.0');
}
const observations = JSON.parse(read('data/part-i/observations.json'));
assert.equal(observations.groups.length, 5);
for (const group of observations.groups) {
  assert.equal(group.records.length, 2);
  for (const field of ['expected','failure','risk','control']) for (const locale of ['en','zh-hans']) assert.ok(group[field][locale]);
  for (const record of group.records) for (const field of ['input','output']) for (const locale of ['en','zh-hans']) assert.ok(record[field][locale]);
}
console.log('Validated Part I bilingual structure, equations, sources, figures, visible exercises/solutions, static content and fixture provenance.');
