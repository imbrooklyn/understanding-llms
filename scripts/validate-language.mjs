// SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import ts from 'typescript';

const root = resolve(import.meta.dirname, '..');
const ignored = new Set(['node_modules', '.git', '.astro', 'dist', 'test-results', 'playwright-report']);
const han = /\p{Script=Han}/u;
const failures = [];
function inspect(directory) {
  for (const item of readdirSync(directory, {withFileTypes:true})) {
    if (ignored.has(item.name)) continue;
    const path = resolve(directory, item.name), name = relative(root, path).replaceAll('\\', '/');
    if (item.isDirectory()) { inspect(path); continue; }
    if (!/\.(md|mjs|ts|astro|css)$/.test(name)) continue;
    const source = readFileSync(path, 'utf8');
    if (name.endsWith('.md') && !name.startsWith('src/content/docs/')) {
      if (han.test(source)) failures.push(`${name}: non-English public documentation`);
    } else if (/\.(mjs|ts)$/.test(name)) {
      // Scan actual comments; localized textbook strings and fixtures are content.
      const scanner = ts.createScanner(ts.ScriptTarget.Latest, false, ts.LanguageVariant.Standard, source);
      for (let kind = scanner.scan(); kind !== ts.SyntaxKind.EndOfFileToken; kind = scanner.scan()) {
        if ([ts.SyntaxKind.SingleLineCommentTrivia, ts.SyntaxKind.MultiLineCommentTrivia].includes(kind) && han.test(scanner.getTokenText())) failures.push(`${name}: non-English code comment`);
      }
    } else if (/\.(astro|css)$/.test(name)) {
      for (const comment of source.matchAll(/<!--[^]*?-->|\/\*[^]*?\*\//g)) if (han.test(comment[0])) failures.push(`${name}: non-English source comment`);
    }
  }
}
inspect(root);
assert.deepEqual(failures, [], failures.join('\n'));
console.log('Validated English public documentation and source comments; localized textbook content is preserved.');
