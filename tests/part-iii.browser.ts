// SPDX-License-Identifier: Apache-2.0
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const contract = JSON.parse(readFileSync(new URL('../data/part-iii/content-contract.json', import.meta.url), 'utf8'));
const base = '/books/understanding-llms';
const chapters = ['ch-11', 'ch-12', 'ch-13', 'ch-14'];
const locales = ['en', 'zh-hans'];
const forbidden = 'input,select,button,textarea,form,details,summary,book-lab';
const captureStyle = '.header, mobile-starlight-toc, nav.sidebar, astro-dev-toolbar { display: none !important; } html { scroll-behavior: auto !important; }';

for (const locale of locales) for (const id of chapters) {
  test(`${locale}/${id}: Part III numerical evidence and readable static figures`, async ({ page, request }, info) => {
    const errors: string[] = [];
    page.on('pageerror', (error) => errors.push(error.message));
    await page.goto(`${base}/${locale}/${id}/`);
    await page.waitForLoadState('networkidle');
    await page.addStyleTag({ content: 'astro-dev-toolbar { display: none !important; }' });
    const content = page.locator('.sl-markdown-content');
    const chapter = Number(id.slice(3));
    await expect(page.locator('main h1')).toHaveCount(1);
    await expect(page.locator('main h1 .book-chapter-label')).toHaveText(new RegExp(`${chapter}`));
    await expect(content.locator('h2').first()).toHaveAttribute('id', `s-${chapter}-1`);
    await expect(content.locator('h2').first()).toContainText(`${chapter}.1`);
    await expect(content.locator(forbidden)).toHaveCount(0);
    await expect(content.locator('.katex-error')).toHaveCount(0);
    expect((await content.innerText()).match(/```book-|\*\*|TODO|\n\+##/g) ?? []).toEqual([]);
    for (const value of contract.evidence[id]) await expect(content).toContainText(value);
    for (const heading of Object.values(contract.headings[locale]) as string[]) await expect(content.getByRole('heading', { name: new RegExp(`${heading}$`) })).toHaveCount(1);
    const answerList = content.locator('ol').last();
    await expect(answerList).toBeVisible();
    await answerList.screenshot({ path: info.outputPath('answers.png'), style: captureStyle, animations: 'disabled' });
    await content.locator('.katex-display').first().screenshot({ path: info.outputPath('equation.png'), style: captureStyle, animations: 'disabled' });
    for (const [index, block] of (await content.locator('.katex-display, table').all()).entries()) {
      const geometry = await block.evaluate((element) => {
        const node = element as HTMLElement;
        const width = node.scrollWidth - node.clientWidth;
        const overflow = getComputedStyle(node).overflowX;
        node.scrollLeft = width;
        return { width, overflow, reached: node.scrollLeft };
      });
      if (geometry.width > 1) {
        expect(geometry.overflow).toMatch(/auto|scroll/);
        expect(geometry.reached).toBeGreaterThan(0);
        await block.screenshot({ path: info.outputPath(`wide-evidence-${index}-right.png`), style: captureStyle, animations: 'disabled' });
      }
      await block.evaluate((node) => { (node as HTMLElement).scrollLeft = 0; });
    }
    if (id === 'ch-13') {
      const tables = content.locator('table');
      await expect(tables.nth(2).locator('tbody tr')).toHaveCount(4);
      await expect(tables.nth(4).locator('tbody tr')).toHaveCount(4);
      await tables.nth(4).screenshot({ path: info.outputPath('generation-trace.png'), style: captureStyle, animations: 'disabled' });
    }
    if (id === 'ch-14') {
      await expect(content.getByRole('heading', { name: new RegExp(contract.static_labels[locale].checkpoint) })).toBeVisible();
      await content.locator('table').nth(1).screenshot({ path: info.outputPath('slot-deletion.png'), style: captureStyle, animations: 'disabled' });
      await content.locator('table').nth(2).screenshot({ path: info.outputPath('source-deletion.png'), style: captureStyle, animations: 'disabled' });
    }
    const brokenAnchors = await content.locator('a[href^="#"]').evaluateAll((links) => links.map((a) => a.getAttribute('href')!).filter((href) => href.length > 1 && !document.getElementById(decodeURIComponent(href.slice(1)))));
    expect(brokenAnchors).toEqual([]);
    const links = await content.locator('a[href]').evaluateAll((nodes) => [...new Set(nodes.map((node) => (node as HTMLAnchorElement).href).filter((href) => href.startsWith(location.origin) && new URL(href).pathname !== location.pathname))]);
    for (const href of links) expect((await request.get(href)).status(), href).toBe(200);
    for (const theme of ['light', 'dark']) {
      await page.evaluate((theme) => document.documentElement.dataset.theme = theme, theme);
      for (const figure of await content.locator('.book-figure').all()) {
        const figureId = (await figure.getAttribute('id'))!;
        const asset = figureId.replace(/^figure-(ch-\d+)-/, '$1/');
        const source = JSON.parse(readFileSync(new URL(`../src/assets/${asset}.json`, import.meta.url), 'utf8'));
        await expect(figure).toContainText(source.caption[locale]);
        for (const lane of source.lanes) {
          await expect(figure).toContainText(lane.label[locale]);
          await expect(figure).toContainText(lane.flow[locale]);
          for (const node of lane.nodes) await expect(figure).toContainText(node.text[locale]);
        }
        await expect(figure.locator('[role="img"]')).toHaveAttribute('aria-label', /.+/);
        await expect(figure.locator('figcaption')).toContainText('CC BY-SA 4.0');
        await expect(figure.locator('.book-node-state')).toHaveCount(0);
        for (const parameter of await figure.locator('.book-node-parameter').all()) await expect(parameter).toHaveCSS('border-top-style', 'double');
        await figure.screenshot({ path: info.outputPath(`${await figure.getAttribute('id')}-${theme}.png`), style: captureStyle, animations: 'disabled' });
      }
      expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
    }
    await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; scrollTo(0, 0); });
    await page.screenshot({ path: info.outputPath('page-top.png') });
    expect(errors).toEqual([]);
    if (!(await page.locator('starlight-lang-select select:visible').count())) await page.locator('button[popovertarget="starlight__sidebar"]').click();
    const other = locale === 'en' ? 'zh-hans' : 'en';
    await page.locator('starlight-lang-select select:visible').first().selectOption(`${base}/${other}/${id}/`);
    await expect(page).toHaveURL(new RegExp(`${other}/${id}/$`));
    await expect(page.locator('main h1')).toHaveCount(1);
  });
}

for (const locale of locales) test(`${locale}: all Part III evidence remains readable without JavaScript`, async ({ browser }, info) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: info.project.use.viewport });
  const page = await context.newPage();
  for (const id of chapters) {
    await page.goto(`${info.project.use.baseURL}${base}/${locale}/${id}/`);
    const content = page.locator('.sl-markdown-content');
    await expect(content.locator(forbidden)).toHaveCount(0);
    await expect(content.locator('.katex math').first()).toBeVisible();
    for (const value of contract.evidence[id]) await expect(content).toContainText(value);
    await expect(content.getByRole('heading', { name: new RegExp(`${contract.headings[locale].answers}$`) })).toBeVisible();
    await expect(content.locator('ol').last()).toBeVisible();
    for (const figure of await content.locator('.book-figure').all()) await expect(figure).toBeVisible();
    await content.locator('ol').last().screenshot({ path: info.outputPath(`${id}-no-js-answers.png`), style: captureStyle, animations: 'disabled' });
    expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
  }
  await context.close();
});
