// SPDX-License-Identifier: Apache-2.0
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const base='/books/understanding-llms';
const ids=[54,55,56,57].map(n=>`ch-${n}`);
const evidence:Record<string,string[]>={
 'ch-54':['202','400','750','InterruptedError'],
 'ch-55':['10/10','4/10','600','750'],
 'ch-56':['39.999','0.999949','18/20','40%'],
 'ch-57':['5/9','6/9','7/9','0/4','UNCERTAIN','DONE']
};
const forbidden='input,select,button,textarea,form,details,summary,book-lab';
const style='.header, mobile-starlight-toc, nav.sidebar, astro-dev-toolbar {visibility:hidden!important} html {scroll-behavior:auto!important}';
for(const locale of ['en','zh-hans']) for(const id of ids){
 test(`${locale}/${id}: Part IX complete static evidence and localized figures`,async({page,request},info)=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${base}/${locale}/${id}/`);await page.waitForLoadState('networkidle');
  const body=page.locator('.sl-markdown-content');
  await expect(body.locator('.book-figure')).toHaveCount(1);
  await expect(body.locator(forbidden)).toHaveCount(0);
  await expect(body.locator('.katex-error')).toHaveCount(0);
  await expect(page.locator('main h1')).toHaveCount(1);
  if(id.startsWith('ch-')){
   const number=Number(id.slice(3));
   await expect(page.locator('main h1 .book-chapter-label')).toContainText(String(number));
   for(const [i,h] of (await body.locator('h2').all()).entries()) await expect(h).toHaveAttribute('id',`s-${number}-${i+1}`);
  }
  for(const text of evidence[id]) await expect(body).toContainText(text);
  await expect(body.getByRole('heading',{name:new RegExp(locale==='en'?'Reference answers$':'参考解答$')})).toBeVisible();
  expect((await body.innerText()).match(/```book-|TODO|\*\*/g)??[]).toEqual([]);
  const broken=await body.locator('a[href^="#"]').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('href')!).filter(h=>!document.getElementById(decodeURIComponent(h.slice(1)))));
  expect(broken).toEqual([]);
  const links=await body.locator('a[href]').evaluateAll(nodes=>[...new Set(nodes.map(n=>(n as HTMLAnchorElement).href).filter(h=>h.startsWith(location.origin)))]);
  for(const href of links) expect((await request.get(href)).status(),href).toBe(200);
  for(const item of await body.locator('table,.katex-display,pre').all()){
   const size=await item.evaluate(el=>({extra:el.scrollWidth-el.clientWidth,overflow:getComputedStyle(el).overflowX}));
   if(size.extra>1) expect(size.overflow).toMatch(/auto|scroll/);
  }
  for(const wrapper of await body.locator('.book-case-comparison').all()){
   await wrapper.evaluate(el=>el.scrollIntoView({block:'start'}));
   const dimensions=await wrapper.evaluate(el=>({overflow:getComputedStyle(el).overflowX,width:el.clientWidth,content:el.scrollWidth}));
   if(dimensions.content>dimensions.width) expect(dimensions.overflow).toMatch(/auto|scroll/);
   await wrapper.evaluate(el=>el.scrollLeft=el.scrollWidth);
   await expect(wrapper.locator('th').last()).toBeInViewport();
   await wrapper.evaluate(el=>el.scrollLeft=0);
   await expect(wrapper.locator('th').first()).toBeInViewport();
  }
  for(const theme of ['light','dark']){
   await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);
   for(const figure of await body.locator('.book-figure').all()){
    const domId=(await figure.getAttribute('id'))!;
    const asset=domId.replace(/^figure-(ch-\d+)-/,'$1/');
    const source=JSON.parse(readFileSync(new URL(`../src/assets/${asset}.json`,import.meta.url),'utf8'));
    await expect(figure.locator('[role="img"]')).toHaveAttribute('aria-label',source.alt[locale]);
    await expect(figure).toContainText(source.caption[locale]);
    const expectedKinds=source.lanes.flatMap((lane:any)=>lane.nodes.map((node:any)=>`kind-${node.kind}`));
    expect(await figure.locator('li').evaluateAll(nodes=>nodes.map(node=>node.className))).toEqual(expectedKinds);
    for(const lane of source.lanes){await expect(figure).toContainText(lane.label[locale]);for(const node of lane.nodes)await expect(figure).toContainText(node.text[locale]);}
    await expect(figure.locator('figcaption')).toContainText('CC BY-SA 4.0');
    await figure.screenshot({path:info.outputPath(`${domId}-${theme}.png`),style,animations:'disabled'});
    await figure.locator('figcaption').scrollIntoViewIfNeeded();
    await expect(figure.locator('figcaption')).toBeInViewport();
    await page.screenshot({path:info.outputPath(`${domId}-${theme}-caption-viewport.png`),style,animations:'disabled'});
   }
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);
  }
  await page.evaluate(()=>{document.documentElement.dataset.theme='light';scrollTo(0,0)});
  await page.screenshot({path:info.outputPath('page-top.png'),animations:'disabled'});
  if(!(await page.locator('starlight-lang-select select:visible').count())) await page.locator('button[popovertarget="starlight__sidebar"]').click();
  const other=locale==='en'?'zh-hans':'en';
  await page.locator('starlight-lang-select select:visible').first().selectOption(`${base}/${other}/${id}/`);
  await expect(page).toHaveURL(new RegExp(`${other}/${id}/$`));
  expect(errors).toEqual([]);
 });
}
for(const locale of ['en','zh-hans']) test(`${locale}: all Part IX evidence without JavaScript`,async({browser},info)=>{
 test.setTimeout(60000);
 const context=await browser.newContext({javaScriptEnabled:false,viewport:info.project.use.viewport});const page=await context.newPage();
 for(const id of ids){
  await page.goto(`${info.project.use.baseURL}${base}/${locale}/${id}/`);
  const body=page.locator('.sl-markdown-content');
  await expect(body.locator('.book-figure')).toHaveCount(1);
  await expect(body.locator(forbidden)).toHaveCount(0);
  for(const text of evidence[id])await expect(body).toContainText(text);
  for(const fig of await body.locator('.book-figure').all())await expect(fig).toBeVisible();
  for(const math of await body.locator('.katex math').all())await expect(math).toBeVisible();
  await expect(body.getByRole('heading',{name:new RegExp(locale==='en'?'Reference answers$':'参考解答$')})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);
  await body.locator('ol').last().screenshot({path:info.outputPath(`${id}-answers-no-js.png`),style});
 }
 await context.close();
});
