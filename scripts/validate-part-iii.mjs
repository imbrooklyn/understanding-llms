// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { assertPublicationState } from './publication-state.mjs';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { renderFigure } from '../src/plugins/remark-book.mjs';

const root = new URL('../', import.meta.url);
const read = (path) => readFileSync(new URL(path, root), 'utf8');
const json = (path) => JSON.parse(read(path));
const hash = (path) => createHash('sha256').update(readFileSync(new URL(path, root))).digest('hex');
const contract = json('data/part-iii/content-contract.json');
const fixture = json('data/part-iii/sequence-v1.json');
const expected = json('data/part-iii/expected.json');
const run = json('data/part-iii/run.json');
const headings = (page) => [...page.matchAll(/^(#{2,6}) (.+)$/gm)].map((m) => [m[1].length, m[2]]);
const figures = (page) => [...page.matchAll(/```book-figure\n([^`]+)```/g)].map((m) => m[1].trim());
const sources = (page) => [...new Set([...page.matchAll(/\]\((https:\/\/[^)]+)\)/g)].map((m) => m[1]))].sort();
const displayMath = (page) => [...page.matchAll(/\$\$([\s\S]*?)\$\$/g)].map((m) => m[1].trim());
const inlineMath = (page) => [...page.matchAll(/(?<!\$)\$(?!\$)([^\n$]+)\$(?!\$)/g)].map((m) => m[1]).sort();
const numbers = (page, label) => {
  const section = page.split(`## ${label}\n`)[1]?.split('\n## ')[0];
  assert.ok(section, `Missing visible section: ${label}`);
  return [...section.matchAll(/^(\d+)\. /gm)].map((m) => Number(m[1]));
};
const table = (page, locale, id) => {
  const after = page.split(`**${contract.captions[locale].table} ${id} —`)[1];
  assert.ok(after, `Missing table ${id}`);
  const block = after.match(/(?:^|\n)(\|[^\n]+\|(?:\n\|[^\n]+\|)+)/)?.[1];
  assert.ok(block, `Missing rows for table ${id}`);
  return block.split('\n').slice(2).map((line) => line.split('|').slice(1, -1).map((cell) => cell.trim()));
};
const fraction = (text) => {
  const parts = text.split('/').map(Number);
  assert.ok(parts.every(Number.isFinite));
  return parts.length === 1 ? parts[0] : parts[0] / parts[1];
};
const vector = (text) => text.replace(/[\[\]\s]/g, '').split(',').map(fraction);
const coefficient = (text) => {
  const match = text.trim().match(/^(\d*)a(?:\/(\d+))?$/);
  return match ? Number(match[1] || 1) / Number(match[2] || 1) : fraction(text);
};
const context = (text) => text.replace(/[\[\]\s]/g, '').split(',').map(coefficient);
const close = (a, b, tolerance = 1e-12) => assert.ok(Math.abs(a - b) <= tolerance, `${a} != ${b}`);

for (const chapter of [11, 12, 13, 14]) {
  const id = `ch-${chapter}`;
  const pages = ['en', 'zh-hans'].map((locale) => read(`src/content/docs/${locale}/${id}.md`));
  const exerciseNumbers = [];
  for (const [index, page] of pages.entries()) {
    const locale = ['en', 'zh-hans'][index], labels = contract.headings[locale];
    const frontmatter = page.match(/^---\n([\s\S]+?)\n---/)?.[1] ?? '';
    assertPublicationState(frontmatter, `${locale}/${id}`);
    assert.doesNotMatch(page, /<!--|TODO|placeholder|in progress and is visible|^# |^\+=/mi);
    assert.doesNotMatch(page, /<(?:input|select|textarea|button|form|details|summary|book-lab)\b|```book-lab/i);
    let previous = 1;
    for (const [depth, text] of headings(page)) {
      assert.ok(depth <= previous + 1, `${id}: skipped heading depth`);
      assert.doesNotMatch(text, /^\d+\./, `${id}: manual section number`);
      previous = depth;
    }
    for (const label of Object.values(labels)) assert.ok(headings(page).some((h) => h[1] === label), `${id}: missing ${label}`);
    const questions = numbers(page, labels.exercises);
    assert.ok(questions.length > 0);
    assert.deepEqual(questions, questions.map((_, i) => i + 1));
    assert.deepEqual(numbers(page, labels.answers), questions, `${id}: missing visible answer`);
    exerciseNumbers.push(questions);
    for (const evidence of contract.evidence[id]) assert.ok(page.includes(evidence), `${locale}/${id}: missing numerical evidence ${evidence}`);
    for (const figure of figures(page)) {
      const source = json(`src/assets/${figure}.json`);
      for (const field of ['alt', 'caption', 'credit']) assert.ok(source[field][locale]?.trim());
      const html = renderFigure(figure, locale);
      assert.match(html, /role="img" aria-label="[^"]+"/);
      assert.match(html, /CC BY-SA 4.0/);
      assert.doesNotMatch(html, /undefined|NaN|book-node-state/);
    }
    for (const match of page.matchAll(/\]\(\.\.\/([^/)]+)\//g)) assert.ok(existsSync(new URL(`src/content/docs/${locale}/${match[1]}.md`, root)), `${id}: broken source link`);
    if (chapter === 11) {
      for (const [i, row] of table(page, locale, '11.3').entries()) {
        assert.deepEqual(vector(row[1]), expected.short_states[0][i]);
        assert.deepEqual(vector(row[2]), run.results.short_rnn[0][i].logits);
        vector(row[3]).forEach((p, j) => close(p, run.results.short_rnn[0][i].probabilities[j], .00000051));
      }
      table(page, locale, '11.4').forEach((row, i) => assert.deepEqual(vector(row[2]), expected.long_states[i]));
    }
    if (chapter === 12) {
      for (const row of table(page, locale, '12.2')) {
        const edges = Number(row[0]);
        close(Number(row[1]), .5 ** edges);
        close(Number(row[2]), 1.5 ** edges);
      }
    }
    if (chapter === 13) {
      assert.deepEqual(table(page, locale, '13.3').map((row) => row[2]), expected.teacher_inputs);
      assert.deepEqual(table(page, locale, '13.3').map((row) => row[3]), expected.teacher_targets);
      for (const row of table(page, locale, '13.4')) assert.deepEqual(row.slice(1).map(Number), fixture.translation.conditional_rows[row[0]]);
      assert.deepEqual(table(page, locale, '13.5').map((row) => row[3]), expected.generated_outputs);
    }
    if (chapter === 14) {
      const rows = table(page, locale, '14.2').slice(1);
      assert.deepEqual(rows.map((row) => vector(row[1])), expected.slot_weights);
      assert.deepEqual(rows.map((row) => context(row[2])), expected.slot_contexts_in_units_of_ln2);
      assert.deepEqual(rows.map((row) => coefficient(row[3])), expected.slot_readouts_in_units_of_ln2);
      assert.deepEqual(table(page, locale, '14.3').map((row) => context(row[2])), expected.source_contexts_in_units_of_ln2);
      assert.ok(page.includes(contract.static_labels[locale].checkpoint));
    }
  }
  assert.deepEqual(headings(pages[0]).map((h) => h[0]), headings(pages[1]).map((h) => h[0]), `${id}: bilingual anchors`);
  assert.deepEqual(displayMath(pages[0]), displayMath(pages[1]), `${id}: display equations`);
  assert.deepEqual(inlineMath(pages[0]), inlineMath(pages[1]), `${id}: inline equations and notation`);
  assert.deepEqual(figures(pages[0]), figures(pages[1]), `${id}: figure order`);
  assert.deepEqual(sources(pages[0]), sources(pages[1]), `${id}: source parity`);
  assert.deepEqual(exerciseNumbers[0], exerciseNumbers[1]);
  for (const type of ['example', 'table']) {
    const captions = pages.map((page, i) => [...page.matchAll(new RegExp(`\\*\\*${contract.captions[['en', 'zh-hans'][i]][type]} (\\d+\\.\\d+) —`, 'g'))].map((m) => m[1]));
    assert.ok(captions[0].length > 0);
    assert.deepEqual(captions[0], captions[1], `${id}: caption parity`);
  }
}
assert.equal(fixture.baseline_source.sha256, hash(fixture.baseline_source.path));
const gradientNodes = json('src/assets/ch-12/backward.json').lanes[2].nodes;
assert.equal(gradientNodes[1].kind, 'vector', 'A gradient is computed evidence, not a stored model parameter');
assert.equal(gradientNodes[2].kind, 'parameter');
assert.ok(gradientNodes[2].text.en.includes(String(expected.updated_weight)));
for (const [path, digest] of Object.entries(run.sha256)) assert.equal(hash(path), digest, `Stale CPU run: ${path}`);
const execution = json('data/part-iii/notebook-execution.json');
for (const [path, digest] of Object.entries(execution.inputs_sha256)) assert.equal(hash(path), digest, `Stale notebook dependency: ${path}`);
const paths = readdirSync(new URL('notebooks/part-iii/', root)).filter((p) => p.endsWith('.ipynb')).map((p) => `notebooks/part-iii/${p}`);
assert.deepEqual(execution.executions.map((r) => r.notebook).sort(), paths.sort());
for (const record of execution.executions) {
  const notebook = json(record.notebook);
  const source = (cell) => Array.isArray(cell.source) ? cell.source.join('') : cell.source;
  const code = notebook.cells.filter((cell) => cell.cell_type === 'code');
  assert.equal(record.status, 'passed');
  assert.equal(record.code_cells, code.length);
  assert.equal(record.code_sha256, createHash('sha256').update(code.map(source).join('\n')).digest('hex'));
  assert.ok(code.every((cell, i) => cell.execution_count === i + 1 && cell.outputs.every((o) => o.output_type !== 'error')));
  for (const cell of notebook.cells) assert.doesNotMatch(source(cell), /\p{Script=Han}/u);
}
for (const name of readdirSync(new URL('code/part-iii/', root)).filter((p) => p.endsWith('.py'))) assert.doesNotMatch(read(`code/part-iii/${name}`), /\p{Script=Han}/u);
for (const name of ['blueprint', 'research', 'validation']) assert.doesNotMatch(read(`docs/part-iii-${name}.md`), /\p{Script=Han}/u);
const checked = spawnSync(process.env.BOOK_PYTHON ?? 'python3', ['-m', 'unittest', 'discover', '-s', 'code/part-iii', '-p', 'test_core.py', '-v'], { cwd: fileURLToPath(root), encoding: 'utf8' });
process.stdout.write(checked.stdout ?? '');
process.stderr.write(checked.stderr ?? '');
assert.equal(checked.status, 0, checked.error?.message ?? 'Sequence behavior checks failed');
console.log('Validated Part III chapter pairs, anchors, math, numerical tables, visible answers, figures, provenance, fresh notebook evidence and independent sequence behavior.');
