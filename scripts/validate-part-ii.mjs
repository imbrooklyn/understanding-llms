// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { assertPublicationState } from './publication-state.mjs';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import remarkBook, { renderFigure } from '../src/plugins/remark-book.mjs';

const require = createRequire(import.meta.url);
const rendererRequire = createRequire(require.resolve('rehype-katex'));
assert.equal(require('katex').version, rendererRequire('katex').version,
  'The imported KaTeX stylesheet and rehype renderer must use the same version.');

const root = new URL('../', import.meta.url);
const read = (path) => readFileSync(new URL(path, root), 'utf8');
const json = (path) => JSON.parse(read(path));
const ids = ['ch-05', 'ch-06', 'ch-07', 'ch-08', 'ch-09', 'ch-10', 'primer-py'];
const locales = ['en', 'zh-hans'];
const sourceURLs = (page) => [...new Set([...page.matchAll(/\]\((https:\/\/[^)]+)\)/g)].map((m) => m[1]))].sort();
const figures = (page) => [...page.matchAll(/```book-figure\n([^`]+)```/g)].map((m) => m[1].trim());
const headings = (page) => [...page.matchAll(/^(#{2,6}) (.+)$/gm)].map((m) => ({ depth: m[1].length, text: m[2] }));
const displayMath = (page) => [...page.matchAll(/\$\$([\s\S]*?)\$\$/g)].map((m) => m[1].trim());
const inlineMath = (page) => [...page.matchAll(/(?<!\$)\$(?!\$)([^\n$]+)\$(?!\$)/g)].map((m) => m[1]).sort();
const numbered = (page, heading) => {
  const section = page.split(`## ${heading}\n`)[1]?.split('\n## ')[0];
  assert.ok(section, `Missing visible ${heading}`);
  return [...section.matchAll(/^(\d+)\. (.+)/gm)].map((m) => Number(m[1]));
};
for (const id of ids) {
  const pages = locales.map((locale) => read(`src/content/docs/${locale}/${id}.md`));
  const questionNumbers = [];
  for (const [index, page] of pages.entries()) {
    const locale = locales[index], prefix = `${locale}/${id}`;
    const frontmatter = page.match(/^---\n([\s\S]+?)\n---/)?.[1];
    assertPublicationState(frontmatter ?? '', prefix);
    assert.doesNotMatch(page, /placeholder|TODO|in progress and is visible|写完.*draft|仅在本地开发模式可见|^# /mi, `${prefix}: unfinished content`);
    assert.doesNotMatch(page, /<(?:details|summary|input|select|textarea|button|form|book-lab)\b|```book-lab/i, `${prefix}: hidden or interactive learning content`);
    assert.doesNotMatch(page, /^#{2,6} \d+\./m, `${prefix}: manual section numbers`);
    let previous = 1;
    for (const heading of headings(page)) {
      assert.ok(heading.depth <= previous + 1, `${prefix}: skipped heading depth`);
      previous = heading.depth;
    }
    const questions = numbered(page, locale === 'en' ? 'Exercises' : '习题');
    const answers = numbered(page, locale === 'en' ? 'Reference answers' : '参考解答');
    assert.ok(questions.length > 0);
    assert.deepEqual(questions, questions.map((_, i) => i + 1), `${prefix}: consecutive exercise numbers`);
    assert.deepEqual(answers, questions, `${prefix}: every exercise has an answer`);
    questionNumbers.push(questions);
    assert.ok(page.includes(`## ${locale === 'en' ? 'References' : '参考文献'}\n`));
    assert.ok(sourceURLs(page).length > 0, `${prefix}: annotated sources`);
    if (id.startsWith('ch-')) {
      assert.ok(headings(page).some((h) => (locale === 'en' ? /chapter summary$/i : /本章小结$/).test(h.text)), `${prefix}: chapter summary`);
      assert.ok(figures(page).length > 0, `${prefix}: mechanism figure`);
    }
    for (const figure of figures(page)) {
      const path = `src/assets/${figure}.json`;
      assert.ok(existsSync(new URL(path, root)), `${prefix}: missing ${figure}`);
      const source = json(path);
      for (const field of ['alt', 'caption', 'credit']) assert.ok(source[field][locale]?.trim(), `${path}: ${field}/${locale}`);
      const html = renderFigure(figure, locale);
      assert.match(html, /role="img" aria-label="[^"]+"/);
      assert.match(html, /CC BY-SA 4.0/);
      assert.doesNotMatch(html, /undefined|NaN/);
    }
    // Check local content links against source pages, including shared anchors.
    for (const match of page.matchAll(/\]\(\.\.\/([^/)]+)\/(?:#([^)]*))?\)/g)) {
      const path = `src/content/docs/${locale}/${match[1]}.md`;
      assert.ok(existsSync(new URL(path, root)), `${prefix}: missing linked page ${match[1]}`);
      if (match[2]?.startsWith('s-')) {
        const tree = { children: headings(read(path)).map((h) => ({ type: 'heading', depth: h.depth, children: [{ type: 'text', value: h.text }] })) };
        remarkBook()(tree, { path });
        assert.ok(tree.children.some((node) => node.data?.hProperties?.id === match[2]), `${prefix}: missing anchor ${match[2]}`);
      }
    }
  }
  assert.deepEqual(headings(pages[0]).map((h) => h.depth), headings(pages[1]).map((h) => h.depth), `${id}: structural anchors differ`);
  assert.deepEqual(displayMath(pages[0]), displayMath(pages[1]), `${id}: display math differs`);
  assert.deepEqual(inlineMath(pages[0]), inlineMath(pages[1]), `${id}: inline math differs`);
  assert.deepEqual(sourceURLs(pages[0]), sourceURLs(pages[1]), `${id}: primary-source coverage differs`);
  assert.deepEqual(figures(pages[0]), figures(pages[1]), `${id}: figure order differs`);
  assert.deepEqual(questionNumbers[0], questionNumbers[1], `${id}: exercise numbering differs`);
  for (const terms of [['Example', '例'], ['Table', '表']]) {
    const numbers = pages.map((page, i) => [...page.matchAll(new RegExp(`\\*\\*${terms[i]} (\\d+\\.\\d+) —`, 'g'))].map((m) => m[1]));
    assert.deepEqual(numbers[0], numbers[1], `${id}: ${terms[0]} captions differ`);
  }
}
const execution = json('data/part-ii/notebook-execution.json');
const notebookPaths = readdirSync(new URL('notebooks/part-ii/', root)).filter((name) => name.endsWith('.ipynb')).map((name) => `notebooks/part-ii/${name}`);
assert.deepEqual(execution.executions.map((row) => row.notebook).sort(), notebookPaths.sort());
for (const record of execution.executions) {
  const notebook = json(record.notebook);
  const source = (cell) => Array.isArray(cell.source) ? cell.source.join('') : cell.source;
  const code = notebook.cells.filter((cell) => cell.cell_type === 'code');
  assert.equal(record.status, 'passed');
  assert.equal(record.code_cells, code.length);
  assert.equal(record.code_sha256, createHash('sha256').update(code.map(source).join('\n')).digest('hex'), `${record.notebook}: stale execution`);
  assert.ok(code.every((cell, i) => cell.execution_count === i + 1), `${record.notebook}: not a complete fresh execution`);
  assert.ok(code.every((cell) => cell.outputs.every((output) => output.output_type !== 'error')));
  for (const cell of notebook.cells) assert.doesNotMatch(source(cell), /\p{Script=Han}/u, `${record.notebook}: keep bilingual strings in content resources`);
}
for (const directory of ['code/part-ii', 'code/knowledge-assistant']) for (const file of readdirSync(new URL(`${directory}/`, root)).filter((name) => name.endsWith('.py'))) {
  assert.doesNotMatch(read(`${directory}/${file}`), /\p{Script=Han}/u, `${file}: implementation is English; bilingual examples belong in resources`);
}
const cpuIndependent = spawnSync(process.env.BOOK_PYTHON ?? 'python3', ['-m', 'unittest', 'discover', '-s', 'code/part-ii', '-p', 'test_core.py', '-v'], { cwd: fileURLToPath(root), encoding: 'utf8' });
process.stdout.write(cpuIndependent.stdout ?? '');
process.stderr.write(cpuIndependent.stderr ?? '');
assert.equal(cpuIndependent.status, 0, cpuIndependent.error?.message ?? 'Part II behavioral checks failed');
console.log('Validated Part II bilingual manuscripts, structural anchors, equations, captions, sources, visible answers, rendered figures, fresh notebook evidence and independent numerical/behavior checks.');
