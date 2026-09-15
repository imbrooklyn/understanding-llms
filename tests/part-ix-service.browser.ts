// SPDX-License-Identifier: Apache-2.0
import { test,expect } from '@playwright/test';
import { spawn, type ChildProcess } from 'node:child_process';
import { readFileSync } from 'node:fs';
const content=JSON.parse(readFileSync(new URL('../data/knowledge-assistant/service-content-v1.json',import.meta.url),'utf8'));
let process:ChildProcess,base:string;
test.beforeAll(async()=>{
 process=spawn(global.process.env.BOOK_PYTHON??'python3',['code/knowledge-assistant/service.py','--port','0'],{cwd:new URL('../',import.meta.url),stdio:['ignore','pipe','pipe']});
 base=await new Promise<string>((resolve,reject)=>{
  let output='',errors='';const timeout=setTimeout(()=>reject(new Error(`Service startup timeout: ${errors}`)),15000);
  process.stderr!.on('data',chunk=>errors+=chunk);
  process.stdout!.on('data',chunk=>{output+=chunk;if(output.includes('\n')){clearTimeout(timeout);try{resolve(JSON.parse(output.split('\n')[0]).url);}catch(error){reject(error);}}});
  process.on('exit',code=>{clearTimeout(timeout);reject(new Error(`Service exited ${code}: ${errors}`));});
 });
});
test.afterAll(async()=>{
 if(process?.exitCode===null){process.kill('SIGINT');await new Promise<void>(resolve=>{process.once('exit',()=>resolve());setTimeout(()=>{if(process.exitCode===null)process.kill('SIGKILL');resolve();},5000);});}
});
for(const locale of ['en','zh-hans'])test(`KA service ${locale}: actual query, source, keyboard, undo, handoff and feedback`,async({page},info)=>{
 const strings=content[locale];
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`${base}/?lang=${locale}`);
 await expect(page.locator('#question')).toHaveAccessibleName(strings.question);
 await expect(page.locator('#on-date')).toHaveAccessibleName(strings.date);
 await expect(page.locator('#status')).toHaveAttribute('role','status');
 await page.locator('#question').focus();await page.keyboard.press('Tab');
 await expect(page.locator('#on-date')).toBeFocused();
 expect(await page.locator('#on-date').evaluate(el=>getComputedStyle(el).outlineStyle)).not.toBe('none');
 await page.locator('#submit').click();
 await expect(page.locator('#answer')).toContainText('750');
 await expect(page.locator('#citations')).toContainText('travel-v2');
 await expect(page.locator('#citations blockquote')).toContainText('2026-01-01');
 for(const colorScheme of ['light','dark'] as const){
  await page.emulateMedia({colorScheme});
  await page.screenshot({path:info.outputPath(`service-${locale}-${colorScheme}.png`),fullPage:true});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);
 }
 await page.locator('#handoff').click();await expect(page.locator('#handoff-note')).toContainText('2026-09-14');
 await page.locator('[data-category="wrong_source"]').click();await expect(page.locator('#status')).toContainText(strings.feedback_saved);
 await page.locator('#clear').click();await expect(page.locator('#answer')).toBeEmpty();await expect(page.locator('#question')).toBeFocused();
 await page.locator('#undo').click();await expect(page.locator('#answer')).toContainText('750');
 await page.locator('#question').fill('volcano');await page.locator('#submit').click();
 await expect(page.locator('#answer')).toContainText(strings.abstained);
 await expect(page.locator('#citations')).toBeEmpty();
 await page.locator('#order').click();await expect(page.locator('#answer')).toContainText('A-104');
 await expect(page.locator('#answer')).toContainText(strings.processing);
 expect(errors).toEqual([]);
});
test('KA service: Stop waits for acknowledgement and does not show a late answer',async({page,request})=>{
 await page.goto(`${base}/?lang=en`);
 // Delay only the acknowledgement: terminal progress can arrive first.
 await page.route('**/cancel',async route=>{const response=await route.fetch();await new Promise(resolve=>setTimeout(resolve,150));await route.fulfill({response});});
 // Refill the demo account's bucket without changing its production policy.
 await page.waitForTimeout(1100);
 await page.locator('#question').fill('Beijing lodging policy');
 await page.locator('#submit').click();
 await expect(page.locator('#cancel')).toBeEnabled();await page.locator('#cancel').click();
 await expect(page.locator('#status')).toHaveText(content.en.cancelled);
 await page.waitForTimeout(250);await expect(page.locator('#status')).toHaveText(content.en.cancelled);await expect(page.locator('#answer')).not.toContainText('750');
 const result=await request.post(base+'/api/requests',{headers:{Authorization:'Bearer demo-north'},data:{question:'Beijing lodging',on_date:'2026-09-14',topic:'travel',locale:'en',tenant:'south'}});
 expect(result.status()).toBe(400);
});
