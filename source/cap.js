const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const [,,mode,a,b,out]=process.argv;
(async()=>{const br=await chromium.launch();const p=await br.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.error('ERR',e.message));
await p.goto('file://'+__dirname+'/anim.html');await p.evaluate(()=>document.fonts.ready);
if(mode==='total'){console.log(await p.evaluate(()=>TOTAL));}
else if(mode==='test'){for(const t of a.split(',')){await p.evaluate(t=>renderAt(t),+t);await p.screenshot({path:`test/t${t}.png`});}}
else{for(let f=+a;f<+b;f++){await p.evaluate(t=>renderAt(t),f/30);await p.screenshot({path:`${out}/f${String(f).padStart(6,'0')}.jpg`,type:'jpeg',quality:90});}}
await br.close();})();
