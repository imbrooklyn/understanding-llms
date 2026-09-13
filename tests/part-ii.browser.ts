// SPDX-License-Identifier: Apache-2.0
import { test, expect } from '@playwright/test';

const base = '/books/understanding-llms';
const chapters = ['ch-05', 'ch-06', 'ch-07', 'ch-08', 'ch-09', 'ch-10', 'primer-py'];
const forbidden = 'input,select,textarea,button,form,details,summary,book-lab';
// Hide fixed navigation only while capturing an element, so it cannot obscure tall figures.
const captureStyle = '.header, mobile-starlight-toc, nav.sidebar, astro-dev-toolbar { display: none !important; } html { scroll-behavior: auto !important; }';
for (const locale of ['en', 'zh-hans']) for (const id of chapters) {
  test(`${locale}/${id}: Part II static evidence, navigation and responsive figures`, async ({ page, request }, testInfo) => {
    const errors: string[] = [];
    page.on('pageerror', (error) => errors.push(error.message));
    await page.goto(`${base}/${locale}/${id}/`);
    await page.waitForLoadState('networkidle');
    await page.addStyleTag({ content: 'astro-dev-toolbar { display: none !important; }' });
    const content = page.locator('.sl-markdown-content');
    await expect(page.locator('main h1')).toHaveCount(1);
    await expect(content.locator(forbidden)).toHaveCount(0);
    await expect(content.locator('.katex-error')).toHaveCount(0);
    const leakedMarkup = (await content.innerText()).match(/.{0,30}(?:```book-|\*\*|TODO).{0,45}/g) ?? [];
    expect(leakedMarkup).toEqual([]);
    const answers = content.getByRole('heading', { name: locale === 'en' ? /Reference answers$/ : /参考解答$/ });
    await expect(answers).toHaveCount(1);
    await expect(content.getByRole('heading', { name: locale === 'en' ? /References$/ : /参考文献$/ })).toHaveCount(1);
    await expect(content.locator('ol').last()).toBeVisible();
    await content.locator('ol').last().screenshot({ path: testInfo.outputPath('answers.png'), style: captureStyle, animations: 'disabled' });
    if (id.startsWith('ch-')) {
      const chapter = Number(id.slice(3));
      await expect(page.locator('main h1 .book-chapter-label')).toHaveText(locale === 'en' ? `Chapter ${chapter}` : `第 ${chapter} 章`);
      await expect(content.locator('h2').first()).toHaveAttribute('id', `s-${chapter}-1`);
      await expect(content.locator('h2').first()).toContainText(`${chapter}.1`);
      expect(await content.locator('.book-figure').count()).toBeGreaterThan(0);
    }
    if (['ch-05', 'ch-06', 'ch-07', 'ch-09', 'ch-10'].includes(id)) {
      expect(await content.locator('.katex math').count()).toBeGreaterThan(0);
      const atom = content.locator('.katex-html > .base, .katex-html > .katex-base').first();
      await expect(atom).toHaveCSS('display', 'inline-block');
      await expect(atom).toHaveCSS('white-space', 'nowrap');
      await content.locator('.katex-display').first().screenshot({ path: testInfo.outputPath('equation.png'), style: captureStyle, animations: 'disabled' });
    }
    if (id === 'ch-07') {
      await expect(content.locator('.book-plot-scroll svg')).toHaveCount(1);
      await expect(content).toContainText(locale === 'en' ? '38/48' : '48 个点中分对 38 个');
      await expect(content).toContainText('0.581859');
    }
    if (id === 'ch-09') {
      for (const result of ['5/9', '6/9', '7/9', '0.829270', '0.646660']) await expect(content).toContainText(result);
    }
    if (id === 'ch-10') {
      for (const result of ['5.475957', '4.155483', '4/9', '7/9']) await expect(content).toContainText(result);
    }
    const brokenAnchors = await content.locator('a[href^="#"]').evaluateAll((links) => links.map((link) => link.getAttribute('href')!).filter((href) => href.length > 1 && !document.getElementById(decodeURIComponent(href.slice(1)))));
    expect(brokenAnchors).toEqual([]);
    const localLinks = await content.locator('a[href]').evaluateAll((links) => [...new Set(links.map((link) => (link as HTMLAnchorElement).href).filter((href) => href.startsWith(location.origin) && new URL(href).pathname !== location.pathname))]);
    for (const href of localLinks) {
      const response = await request.get(href);
      expect(response.status(), href).toBe(200);
      if (new URL(href).hash) expect(await response.text()).toContain(`id="${decodeURIComponent(new URL(href).hash.slice(1))}"`);
    }
    for (const theme of ['light', 'dark']) {
      await page.evaluate((value) => document.documentElement.dataset.theme = value, theme);
      for (const figure of await content.locator('.book-figure').all()) {
        await expect(figure.locator('[role="img"]')).toHaveAttribute('aria-label', /.+/);
        await expect(figure.locator('figcaption')).toContainText('CC BY-SA 4.0');
        await figure.screenshot({ path: testInfo.outputPath(`${await figure.getAttribute('id')}-${theme}.png`), style: captureStyle, animations: 'disabled' });
        await figure.locator('figcaption').screenshot({ path: testInfo.outputPath(`${await figure.getAttribute('id')}-${theme}-caption.png`), style: captureStyle, animations: 'disabled' });
      }
      expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
    }
    await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; scrollTo(0, 0); });
    await page.screenshot({ path: testInfo.outputPath('page-top.png') });
    if (await content.locator('table').count()) await content.locator('table').first().screenshot({ path: testInfo.outputPath('first-table.png'), style: captureStyle, animations: 'disabled' });
    expect(errors).toEqual([]);
    const other = locale === 'en' ? 'zh-hans' : 'en';
    await page.evaluate(() => scrollTo(0, 0));
    if (!(await page.locator('starlight-lang-select select:visible').count())) await page.locator('button[popovertarget="starlight__sidebar"]').click();
    await page.locator('starlight-lang-select select:visible').first().selectOption(`${base}/${other}/${id}/`);
    await expect(page).toHaveURL(new RegExp(`${other}/${id}/$`));
    await expect(page.locator('main h1')).toHaveCount(1);
  });
}

for (const locale of ['en', 'zh-hans']) test(`${locale}: Part II and primer remain complete with JavaScript disabled`, async ({ browser }, testInfo) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: testInfo.project.use.viewport });
  const page = await context.newPage();
  for (const id of chapters) {
    await page.goto(`${testInfo.project.use.baseURL}${base}/${locale}/${id}/`);
    const content = page.locator('.sl-markdown-content');
    await expect(content.locator(forbidden)).toHaveCount(0);
    await expect(content.getByRole('heading', { name: locale === 'en' ? /Reference answers$/ : /参考解答$/ })).toBeVisible();
    await expect(content.locator('ol').last()).toBeVisible();
    if (id !== 'primer-py') await expect(content.locator('.book-figure').first()).toBeVisible();
    if (id === 'ch-07') await expect(content.locator('.book-plot-scroll svg')).toBeVisible();
    if (id === 'ch-09') await expect(content).toContainText('7/9');
    await content.locator('ol').last().screenshot({ path: testInfo.outputPath(`${id}-no-js-answers.png`), style: captureStyle, animations: 'disabled' });
    expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
  }
  await context.close();
});
