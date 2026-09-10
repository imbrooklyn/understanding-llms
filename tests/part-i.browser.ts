// SPDX-License-Identifier: Apache-2.0
import { test, expect } from '@playwright/test';

const base = '/books/understanding-llms';
const exerciseCounts = [8,8,9,10];
for (const locale of ['en','zh-hans']) for (const chapter of [1,2,3,4]) {
  const id = `ch-0${chapter}`;
  test(`${locale}/${id}: complete static textbook and localized navigation`, async ({ page }, testInfo) => {
    const errors: string[] = [], external: string[] = [];
    page.on('pageerror', (error) => errors.push(error.message));
    page.on('request', (request) => {
      if (/^https?:/.test(request.url()) && !request.url().startsWith(String(testInfo.project.use.baseURL))) external.push(request.url());
    });
    await page.goto(`${base}/${locale}/${id}/`);
    await page.waitForLoadState('networkidle');
    await page.addStyleTag({content:'astro-dev-toolbar { display: none !important; }'});
    const content = page.locator('.sl-markdown-content');
    await expect(page.locator('main h1')).toHaveCount(1);
    await expect(page.locator('main h1 .book-chapter-label')).toHaveText(locale === 'en' ? `Chapter ${chapter}` : `第 ${chapter} 章`);
    await expect(page.locator('.sidebar-content a[aria-current="page"]')).toContainText(`${chapter} · `);
    await expect(content.locator('h2').first()).toHaveAttribute('id', `s-${chapter}-1`);
    await expect(content.locator('h2').first()).toContainText(`${chapter}.1`);
    await expect(content.locator('input,select,textarea,button,form,details,summary,book-lab')).toHaveCount(0);
    expect(await content.innerText()).not.toContain('**');
    expect(await content.innerText()).not.toContain('```book-');
    await expect(content.getByRole('heading', {name: locale === 'en' ? /Solutions$/ : /参考解答$/})).toHaveCount(1);
    await expect(content.getByRole('heading', {name: locale === 'en' ? /References$/ : /参考文献$/})).toHaveCount(1);
    await expect(content.locator('ol').last().locator(':scope > li')).toHaveCount(exerciseCounts[chapter-1]);
    for (const figure of await content.locator('.book-figure').all()) {
      await expect(figure.locator('[role="img"]')).toHaveAttribute('aria-label', /.+/);
      await expect(figure.locator('figcaption')).toContainText('CC BY-SA 4.0');
      await figure.screenshot({path:testInfo.outputPath(`figure-${await figure.getAttribute('id')}.png`)});
    }
    if (chapter === 1) {
      const comparison = content.locator('table').last();
      await expect(comparison.locator('tbody tr td:first-child')).toHaveText(locale === 'en'
        ? ['Factual completion', 'Open-ended completion', 'Clue substitution', 'Policy updates', 'Order queries']
        : ['事实补全', '开放补全', '线索变化', '制度更新', '订单查询']);
      await comparison.screenshot({path:testInfo.outputPath('table-1-3.png')});
    }
    if (chapter === 3) {
      await expect(content.locator('.coordinate-figure')).toHaveCount(1);
      await expect(content.locator('.lookup-walk').first()).toContainText('16');
      await expect(content.locator('.coordinate-figure')).toContainText('u=[1,0]');
    }
    if (chapter === 4) {
      await expect(content).toContainText('2479403867');
      await expect(content).toContainText('1/25');
      await expect(content.locator('.ticket-bag b')).toHaveText(['b','b','c']);
    }
    if (chapter >= 2) {
      expect(await content.locator('.katex math').count()).toBeGreaterThan(0);
      await expect(content.locator('.katex-error')).toHaveCount(0);
      await content.locator('.katex-display').first().screenshot({path:testInfo.outputPath('equation.png')});
    }
    const lastAnswers = content.locator('ol').last();
    await lastAnswers.screenshot({path:testInfo.outputPath('solutions.png')});
    expect(await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)).toBeLessThanOrEqual(1);
    await page.evaluate(() => window.scrollTo(0,0));
    await page.screenshot({path:testInfo.outputPath('page-top.png')});
    await page.evaluate(() => document.documentElement.dataset.theme = 'dark');
    await content.locator('.book-figure').last().screenshot({path:testInfo.outputPath('figure-dark.png')});
    expect(errors).toEqual([]);
    expect(external).toEqual([]);
    const other = locale === 'en' ? 'zh-hans' : 'en';
    if (!(await page.locator('starlight-lang-select select:visible').count())) {
      await page.evaluate(() => window.scrollTo(0,0));
      await page.locator('button[popovertarget="starlight__sidebar"]').click();
    }
    await page.locator('starlight-lang-select select:visible').first().selectOption(`${base}/${other}/${id}/`);
    await expect(page).toHaveURL(new RegExp(`${other}/${id}/$`));
    await expect(page.locator('main h1 .book-chapter-label')).toHaveText(other === 'en' ? `Chapter ${chapter}` : `第 ${chapter} 章`);
  });
}

for (const locale of ['en','zh-hans']) test(`${locale}: every chapter and solution is available without JavaScript`, async ({ browser }, testInfo) => {
  const context = await browser.newContext({javaScriptEnabled:false, viewport:testInfo.project.use.viewport});
  const page = await context.newPage();
  for (const chapter of [1,2,3,4]) {
    await page.goto(`${testInfo.project.use.baseURL}${base}/${locale}/ch-0${chapter}/`);
    const content = page.locator('.sl-markdown-content');
    await expect(content.locator('input,select,textarea,button,form,details,summary,book-lab')).toHaveCount(0);
    await expect(content.locator('.book-figure').first()).toBeVisible();
    await expect(content.locator('ol').last().locator(':scope > li')).toHaveCount(exerciseCounts[chapter-1]);
    await expect(content.locator('ol').last()).toBeVisible();
    if (chapter >= 2) expect(await content.locator('.katex math').count()).toBeGreaterThan(0);
  }
  await context.close();
});
