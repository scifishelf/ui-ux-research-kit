import { chromium } from '@playwright/test';
import {fileURLToPath} from 'node:url';import os from 'node:os';
import http from 'node:http';import fs from 'node:fs/promises';import path from 'node:path';import {spawnSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dir=root+'/motion-patterns';const scratch=await fs.mkdtemp(path.join(os.tmpdir(),'ui-ux-motion-'));await fs.mkdir(dir+'/videos',{recursive:true});
const server=http.createServer(async(req,res)=>{try{const name=new URL(req.url,'http://local').pathname.slice(1)||'demo.html';const p=path.resolve(dir,name);if(!p.startsWith(dir+'/')){res.writeHead(403);res.end();return;}const data=await fs.readFile(p);res.setHeader('Content-Type',p.endsWith('.html')?'text/html':p.endsWith('.css')?'text/css':'application/javascript');res.end(data);}catch{res.writeHead(404);res.end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const port=server.address().port;
let browser;let results=[];
try{
browser=await chromium.launch({headless:true});
for(let i=1;i<=14;i++){
 const id='MP'+String(i).padStart(2,'0');const context=await browser.newContext({viewport:{width:1100,height:680},recordVideo:{dir:scratch,size:{width:1100,height:680}},locale:'en-US'});const page=await context.newPage();let errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(`http://127.0.0.1:${port}/demo.html`);await page.evaluate(id=>{document.querySelectorAll('section').forEach(s=>{if(s.id!==id)s.hidden=true;});document.querySelector('h1').textContent=id+' · Desktop demo';},id);
 await page.waitForTimeout(250);
 const section=page.locator('#'+id);
 if(id==='MP01'){await section.locator('.press').hover();await section.locator('.press').click({delay:180});}
 else if(id==='MP07')await section.locator('[data-route]').click();
 else if(id==='MP09')await section.locator('summary').click();
 else if(id==='MP10')await section.locator('[data-drag]').click();
 else if(id==='MP11')await section.locator('input').check();
 else await section.locator('[data-replay]').click();
 await page.waitForTimeout(900);
 if(id==='MP06'){await page.keyboard.press('Escape');await page.waitForTimeout(150);}
 const animated=await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length);
 await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(150);
 await page.evaluate(()=>{document.querySelector('h1').textContent+=' · Reduced Motion';});
 if(id==='MP07')await section.locator('[data-route]').click();else if(id==='MP10')await section.locator('[data-drag]').click();else if(id==='MP09')await section.locator('summary').click();else if(id==='MP11')await section.locator('input').uncheck();else await section.locator('[data-replay]').click();
 await page.waitForTimeout(300);if(id==='MP06')await page.keyboard.press('Escape');
 const reducedRunning=await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length);
 const badIds=await page.evaluate(()=>{const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return ids.filter((id,i)=>ids.indexOf(id)!==i);});
 await page.screenshot({path:scratch+'/'+id+'.png'});await page.waitForTimeout(350);const video=page.video();await context.close();const source=await video.path();
 const out=dir+'/videos/'+id.toLowerCase()+'-desktop.mp4';const r=spawnSync(process.env.MOTION_FFMPEG || 'ffmpeg',['-hide_banner','-loglevel','error','-y','-i',source,'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',out],{encoding:'utf8'});if(r.status!==0)throw new Error(r.stderr);
 results.push({pattern:id,browser:'Chromium',browserVersion:browser.version(),viewport:[1100,680],capture:'Playwright video; normal interaction then reduced-motion emulation',path:'motion-patterns/videos/'+id.toLowerCase()+'-desktop.mp4',errors,duplicateIds:badIds,runningAnimationsNormal:animated,runningAnimationsReduced:reducedRunning,standalonePwa:false});
 console.log(id,'captured',errors.length,'errors; reduced animations',reducedRunning);
 if(errors.length || badIds.length || reducedRunning)throw new Error(id+' demo checks failed');
}
await fs.writeFile(root+'/report/evidence/motion-capture.json',JSON.stringify({date:new Date().toISOString(),kind:'demonstration_not_product_benchmark',results},null,2)+'\n');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
