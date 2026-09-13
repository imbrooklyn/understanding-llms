// SPDX-License-Identifier: Apache-2.0
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const contract = JSON.parse(readFileSync(new URL('../data/part-v/content-contract.json', import.meta.url), 'utf8'));
const base = '/books/understanding-llms';
const chapters = contract.chapters.map((n: number) => `ch-${n}`);
const locales = ['en', 'zh-hans'];
const forbidden = 'input,select,button,textarea,form,details,summary,book-lab';
const captureStyle = '.header, mobile-starlight-toc, nav.sidebar, astro-dev-toolbar { visibility: hidden !important; } html { scroll-behavior: auto !important; }';

for (const locale of locales) for (const id of chapters) {
  test(`${locale}/${id}: Part V static mechanisms and milestone evidence`, async ({ page, request }, info) => {
    const errors: string[] = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`${base}/${locale}/${id}/`);
    await page.waitForLoadState('networkidle');
    await page.addStyleTag({ content: 'astro-dev-toolbar { display: none !important; }' });
    const content = page.locator('.sl-markdown-content');
    const chapter = Number(id.slice(3));
    await expect(page.locator('main h1')).toHaveCount(1);
    await expect(page.locator('main h1 .book-chapter-label')).toHaveText(new RegExp(`${chapter}`));
    for (const [index, heading] of (await content.locator('h2').all()).entries()) {
      await expect(heading).toHaveAttribute('id', `s-${chapter}-${index + 1}`);
      await expect(heading).toContainText(`${chapter}.${index + 1}`);
    }
    await expect(content.locator(forbidden)).toHaveCount(0);
    await expect(content.locator('.katex-error')).toHaveCount(0);
    expect((await content.innerText()).match(/```book-|\*\*|TODO|\n\+##/g) ?? []).toEqual([]);
    for (const value of contract.evidence[id].filter((s: string) => !s.startsWith('['))) await expect(content).toContainText(value);
    for (const heading of Object.values({ ...contract.headings[locale], ...(id === 'ch-33' ? { exercises: contract.final_exercises[locale] } : {}) }) as string[]) await expect(content.getByRole('heading', { name: new RegExp(`${heading}$`) })).toHaveCount(1);
    await content.locator('ol').last().screenshot({ path: info.outputPath('answers.png'), style: captureStyle, animations: 'disabled' });
    if (await content.locator('.katex-display').count()) await content.locator('.katex-display').first().screenshot({ path: info.outputPath('equation.png'), style: captureStyle, animations: 'disabled' });
    for (const [index, block] of (await content.locator('.katex-display, table, .book-plot-scroll').all()).entries()) {
      const geometry = await block.evaluate(element => {
        const node = element as HTMLElement, width = node.scrollWidth - node.clientWidth;
        node.scrollLeft = width;
        return { width, overflow: getComputedStyle(node).overflowX, reached: node.scrollLeft };
      });
      if (geometry.width > 1) {
        expect(geometry.overflow).toMatch(/auto|scroll/);
        expect(geometry.reached).toBeGreaterThan(0);
        await block.screenshot({ path: info.outputPath(`wide-evidence-${index}-right.png`), style: captureStyle, animations: 'disabled' });
      }
      await block.evaluate(node => { (node as HTMLElement).scrollLeft = 0; });
    }
    if (id === 'ch-33') {
      await expect(content.locator('table').first().locator('tbody tr')).toHaveCount(4);
      await expect(content.locator('table').nth(1).locator('tbody tr')).toHaveCount(6);
      await expect(content.locator('table').nth(2).locator('tbody tr')).toHaveCount(6);
      await content.locator('table').first().screenshot({ path: info.outputPath('ka1-results.png'), style: captureStyle, animations: 'disabled' });
    }
    const brokenAnchors = await content.locator('a[href^="#"]').evaluateAll(links => links.map(a => a.getAttribute('href')!).filter(href => href.length > 1 && !document.getElementById(decodeURIComponent(href.slice(1)))));
    expect(brokenAnchors).toEqual([]);
    const links = await content.locator('a[href]').evaluateAll(nodes => [...new Set(nodes.map(node => (node as HTMLAnchorElement).href).filter(href => href.startsWith(location.origin) && new URL(href).pathname !== location.pathname))]);
    for (const href of links) expect((await request.get(href)).status(), href).toBe(200);
    for (const theme of ['light', 'dark']) {
      await page.evaluate(theme => document.documentElement.dataset.theme = theme, theme);
      for (const figure of await content.locator('.book-figure').all()) {
        const figureId = (await figure.getAttribute('id'))!;
        const asset = figureId.replace(/^figure-(ch-\d+)-/, '$1/');
        const source = JSON.parse(readFileSync(new URL(`../src/assets/${asset}.json`, import.meta.url), 'utf8'));
        await expect(figure).toContainText(source.caption[locale]);
        for (const [laneIndex, lane] of (source.lanes ?? []).entries()) {
          await expect(figure).toContainText(lane.label[locale]);
          await expect(figure).toContainText(lane.flow[locale]);
          for (const [nodeIndex, node] of lane.nodes.entries()) {
            await expect(figure).toContainText(node.text[locale]);
            await expect(figure.locator('.figure-lane').nth(laneIndex).locator('li').nth(nodeIndex)).toHaveClass(`kind-${node.kind}`);
          }
        }
        for (const label of Object.values(source.labels ?? {}) as Record<string, string>[]) await expect(figure).toContainText(label[locale]);
        await expect(figure.locator('[role="img"]')).toHaveAttribute('aria-label', source.alt[locale]);
        await expect(figure.locator('figcaption')).toContainText('CC BY-SA 4.0');
        const captionBounds = await figure.evaluate(element => {
          const outer = element.getBoundingClientRect(), caption = element.querySelector('figcaption')!.getBoundingClientRect();
          return { left: caption.left - outer.left, right: outer.right - caption.right, bottom: outer.bottom - caption.bottom };
        });
        for (const inset of Object.values(captionBounds)) expect(inset).toBeGreaterThanOrEqual(-1);
        await expect(figure.locator('.kind-state')).toHaveCount(0);
        for (const parameter of await figure.locator('.kind-parameter').all()) await expect(parameter).toHaveCSS('border-top-style', 'double');
        // Avoid viewport-edge clipping when scroll padding offsets a nearly full-height figure.
        await figure.evaluate(element => window.scrollTo({ top: scrollY + element.getBoundingClientRect().top, behavior: 'instant' }));
        await figure.screenshot({ path: info.outputPath(`${figureId}-${theme}.png`), style: captureStyle, animations: 'disabled' });
      }
      expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
    }
    await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; scrollTo(0, 0); });
    await page.evaluate(() => new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))));
    await page.screenshot({ path: info.outputPath('page-top.png'), animations: 'disabled' });
    expect(errors).toEqual([]);
    if (!(await page.locator('starlight-lang-select select:visible').count())) await page.locator('button[popovertarget="starlight__sidebar"]').click();
    const other = locale === 'en' ? 'zh-hans' : 'en';
    await page.locator('starlight-lang-select select:visible').first().selectOption(`${base}/${other}/${id}/`);
    await expect(page).toHaveURL(new RegExp(`${other}/${id}/$`));
  });
}

for (const locale of locales) test(`${locale}: all Part V evidence without JavaScript`, async ({ browser }, info) => {
  test.setTimeout(60000);
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: info.project.use.viewport });
  const page = await context.newPage();
  for (const id of chapters) {
    await page.goto(`${info.project.use.baseURL}${base}/${locale}/${id}/`);
    const content = page.locator('.sl-markdown-content');
    expect((await content.innerText()).match(/```book-|\*\*|TODO/g) ?? []).toEqual([]);
    await expect(content.locator(forbidden)).toHaveCount(0);
    for (const formula of await content.locator('.katex math').all()) await expect(formula).toBeVisible();
    for (const value of contract.evidence[id].filter((s: string) => !s.startsWith('['))) await expect(content).toContainText(value);
    await expect(content.getByRole('heading', { name: new RegExp(`${contract.headings[locale].answers}$`) })).toBeVisible();
    for (const figure of await content.locator('.book-figure').all()) await expect(figure).toBeVisible();
    await content.locator('ol').last().screenshot({ path: info.outputPath(`${id}-no-js-answers.png`), style: captureStyle, animations: 'disabled' });
    expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
  }
  await context.close();
});
