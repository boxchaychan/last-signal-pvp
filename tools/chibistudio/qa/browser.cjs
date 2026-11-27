const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_PACKAGE||'playwright');
const out=path.resolve(process.env.STUDIO_QA_OUT||'qa-output');
fs.mkdirSync(out,{recursive:true});
const app=path.resolve(process.argv[2]||'chibi_live_studio.html');
const local = value=>'file://'+value;
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM||undefined,args:['--no-sandbox',...(process.env.STUDIO_QA_GPU?['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']:[])]});
  try{
    const p=await b.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true,acceptDownloads:true});
    const errors=[];
    p.on('pageerror',e=>errors.push(e.message));
    await p.goto(local(app)+(process.env.STUDIO_QA_GPU?'':'?renderer=cpu'));
    await p.waitForFunction('ready');
    const backend=await p.evaluate('renderBackend');
    assert.equal(backend,process.env.STUDIO_QA_GPU?'WebGL':'CPU');
    const checkViewport=async()=>{
      const sizes=await p.evaluate(()=>({w:innerWidth,actual:document.documentElement.scrollWidth}));
      assert.ok(sizes.actual<=sizes.w,'horizontal overflow');
    };
    const tap=async(sel)=>p.locator(sel).tap();
    const seek=async(z)=>p.locator('#seek').evaluate((s,z)=>{s.value=z;s.dispatchEvent(new Event('input'));},z);
    const openDetails=async(sel)=>p.locator(sel).evaluate(el=>el.open=true);
    const putFile=async(id,filename,data,mime='application/json')=>
      p.locator(id).setInputFiles({name:filename,mimeType:mime,buffer:Buffer.from(data)});
    async function download(id){
      const waiting=p.waitForEvent('download',{timeout:25000});
      await tap(id);
      const d=await waiting, file=path.join(out,d.suggestedFilename());
      await d.saveAs(file);
      return file;
    }
    await checkViewport();
    await tap('#play');
    await p.waitForFunction('playing && time>.18');
    await tap('#play');
    assert.equal(await p.evaluate('playing'),false);
    const garmentIsolation=await p.evaluate(()=>{
      const sumArm=(x,y)=>Object.entries(zeusWeights(x,y))
        .filter(([id])=>/^(upper|lower|hand)/.test(id)).reduce((n,[,v])=>n+v,0);
      return {leftEdge:sumArm(225,282),rightEdge:sumArm(316,265),cuff:sumArm(170,272)};
    });
    assert.equal(garmentIsolation.leftEdge,0);
    assert.equal(garmentIsolation.rightEdge,0);
    assert.ok(garmentIsolation.cuff>.90);
    const folded=await p.evaluate(()=>{
      const output=canvas().getContext('2d'), result={};
      for(const [name,c] of Object.entries(project.clips)){
        const count=Math.ceil(c.duration*30);
        result[name]=Array.from({length:count},(_,i)=>stage(output,{clean:true,t:i*c.duration/count,p:c}).folded);
      }
      return result;
    });
    assert.equal(Object.values(folded).flat().filter(Boolean).length,0,'preset triangle inversions');
    await seek(.5);await p.screenshot({path:path.join(out,'mobile-workspace.png'),fullPage:true});
    await tap('[data-tab=export]');await checkViewport();
    await p.locator('#size').selectOption('512');
    await download('#exportPNG');
    await download('#exportSheet');
    const meta=JSON.parse(fs.readFileSync(await download('#exportMeta')));
    assert.equal(meta.frames.length,35);assert.equal(meta.frameSize.width,512);
    await download('#exportGIF');
    await openDetails('#export details');
    const json=await download('#saveProject');
    await tap('[data-tab=rig]');
    await p.locator('#bone').selectOption('hair');
    await openDetails('#rig details:nth-of-type(2)');
    await seek(.67);
    const spring=await p.evaluate(()=>{
      const c=project.clips.attack,t=.67, prior=evaluate(project,c,t).bones.hair.a;
      const s=project.springs.hair;delete project.springs.hair;
      const without=evaluate(project,c,t).bones.hair?.a||0;project.springs.hair=s;
      return [prior,without];
    });
    assert.notEqual(...spring);
    await p.locator('#bindPose').uncheck();
    const reaches=await p.evaluate(()=>{
      const p=zeusProject(), rest=fk(p.bones);
      return chains.map((c,i)=>{
        const q={}, end=rest[c[2]],top=rest[c[0]], mid=rest[c[1]];
        const x=end.x+(top.x-end.x)*.16+(i%2?4:-4), y=end.y+(top.y-end.y)*.15;
        const cross=(mid.x-top.x)*(end.y-mid.y)-(mid.y-top.y)*(end.x-mid.x);
        solveIK(p.bones,q,c,x,y,Math.sign(cross)||c[3]);const v=fk(p.bones,q)[c[2]];
        return Math.hypot(v.x-x,v.y-y);
      });
    });
    assert.ok(reaches.every(x=>x<.01));
    const coords=await p.evaluate(()=>{
      const r=view.getBoundingClientRect(), f=Math.min(r.width/W,r.height/H);
      const screen=(x,y)=>({x:r.left+(r.width-W*f)/2+x*f,y:r.top+(r.height-H*f)/2+y*f});
      const w=fk(project.bones,evaluate(project,currentClip(),time).bones), q=w.handR;
      return {a:screen(q.x,q.y),b:screen(q.x-12,q.y+11)};
    });
    await p.mouse.move(coords.a.x,coords.a.y);await p.mouse.down();await p.mouse.move(coords.b.x,coords.b.y,{steps:5});await p.mouse.up();
    assert.equal(await p.evaluate('boneId'),'handR');
    assert.ok(await p.evaluate('Number.isFinite(draft?.bones.lowerR?.a)'));
    await tap('[data-tab=animate]');await openDetails('#editPose');
    await p.locator('[data-slot=face]').selectOption('shout');
    await p.locator('[data-slot=hand]').selectOption('open');
    await p.locator('[data-slot=weapon]').selectOption('sword');
    await tap('#putKey');
    assert.equal(await p.evaluate('currentClip().keys.find(k=>k.t===.67).slots.weapon'),'sword');
    await tap('#newClip');await seek(.26);
    await p.locator('#poseBone').selectOption('head');
    await p.locator('#poseAngle').fill('14');await p.locator('#poseAngle').press('Tab');await tap('#putKey');
    assert.equal(await p.evaluate('currentClip().keys.at(-1).bones.head.a'),14);
    await openDetails('#editClip');
    const clip=await download('#exportClip');
    await tap('[data-tab=export]');await openDetails('#export details');
    await tap('#dummy');await p.waitForFunction("project.name==='Practice knight'");
    await tap('[data-tab=animate]');await openDetails('#editClip');
    await p.locator('#importClip').evaluate(el=>el.click());
    await putFile('#fileJson','shared.json',fs.readFileSync(clip));
    await p.waitForFunction("currentClip().keys.at(-1).bones.head?.a===14");
    await p.screenshot({path:path.join(out,'mobile-second-rig.png'),fullPage:true});
    await tap('[data-tab=export]');await openDetails('#export details');
    await tap('#blank');await p.waitForFunction("project.name==='New character'");
    await tap('[data-tab=art]');
    const png=await p.evaluate(()=>{
      const c=canvas(180,140), x=c.getContext('2d');
      x.fillStyle='#8448a9';x.fillRect(24,19,70,43);x.fillStyle='#cda374';x.fillRect(112,75,40,40);
      return c.toDataURL().split(',')[1];
    });
    await p.locator('#pngMode').selectOption('alpha');
    await putFile('#filePNG','parts.png',Buffer.from(png,'base64'),'image/png');
    await p.waitForFunction('project.parts.length===2 && !pending');
    await p.locator('#partBone').selectOption('chest');
    await tap('#snapPart');await p.waitForFunction('!pending');
    assert.ok(await p.evaluate(()=>{
      const p=currentPart(), offset=pivotOffset(p,spriteInfo(p)), b=fk(project.bones)[p.bone];
      return Math.hypot(p.x+offset[0]-b.x,p.y+offset[1]-b.y)<.01;
    }));
    await p.locator('#binding').selectOption('auto');await p.waitForFunction('!pending');
    await tap('#paint');await p.locator('#view').scrollIntoViewIfNeeded();
    const swatch=await p.evaluate(()=>{
      const r=view.getBoundingClientRect(),f=Math.min(r.width/W,r.height/H),p=currentPart();
      return {x:r.left+(r.width-W*f)/2+(p.x+22)*f,y:r.top+(r.height-H*f)/2+(p.y+20)*f};
    });
    await p.mouse.move(swatch.x,swatch.y);await p.mouse.down();await p.mouse.move(swatch.x+12,swatch.y+7,{steps:5});await p.mouse.up();
    assert.ok(await p.evaluate('Object.keys(currentPart().paint).length>2'));
    await tap('#undoPaint');
    assert.equal(await p.evaluate('Object.keys(currentPart().paint).length'),0);
    await p.waitForFunction('!pending');
    await openDetails('#art details:nth-of-type(2)');
    await tap('#cut');await p.locator('#view').scrollIntoViewIfNeeded();
    const cut=await p.evaluate(()=>{
      const r=view.getBoundingClientRect(),f=Math.min(r.width/W,r.height/H),p=currentPart();
      const s=(x,y)=>[r.left+(r.width-W*f)/2+(p.x+x)*f,r.top+(r.height-H*f)/2+(p.y+y)*f];
      return [s(4,4),s(30,23)];
    });
    await p.mouse.move(...cut[0]);await p.mouse.down();await p.mouse.move(...cut[1],{steps:5});await p.mouse.up();
    await tap('#applyCut');await p.waitForFunction('project.parts.length===3 && !pending');
    const artValidation=await p.evaluate(()=>{
      const c=canvas(96,64),x=c.getContext('2d');x.fillStyle='#00f500';x.fillRect(0,0,96,64);
      x.fillStyle='#732568';x.fillRect(5,8,21,26);x.fillStyle='#fb9349';x.fillRect(44,6,36,39);
      const green=splitImage(c,'green').length;
      const a=canvas(64,64),b=canvas(64,64),u=a.getContext('2d'),v=b.getContext('2d');
      u.fillStyle='#2a90a9';u.fillRect(5,14,38,32);v.fillStyle='#120912';v.fillRect(29,12,24,37);
      v.fillStyle='#a661a8';v.fillRect(32,15,18,31);
      const join=composeJoint(a,b).getContext('2d');
      return {green,inside:Array.from(join.getImageData(29,23,1,1).data),outer:Array.from(join.getImageData(52,23,1,1).data)};
    });
    assert.deepEqual(artValidation,{green:2,inside:[42,144,169,255],outer:[18,9,18,255]});
    await tap('#mergeMesh');await p.waitForFunction("project.parts.length===4 && !pending");
    assert.equal(await p.evaluate("project.parts.filter(p=>!p.visible).length"),2);
    const actualV04={version:4,pose:{t:0,upper:25,elbow:-20,lean:0,squash:0,hand:'fist',bolt:true},keys:[]};
    assert.equal(await p.evaluate(d=>validateProject(convertPrevious(d)).clips.imported.keys.length,actualV04),1);
    await tap('[data-tab=export]');await openDetails('#export details');
    await p.locator('#loadProject').evaluate(el=>el.click());
    await putFile('#fileJson','zeus.json',fs.readFileSync(json));
    await p.waitForFunction("project.name==='Zeus' && !pending");
    await tap('[data-tab=battle]');await tap('#battleAttack');
    await p.waitForFunction('battle.hp===75',{timeout:5000});await p.screenshot({path:path.join(out,'mobile-battle.png'),fullPage:true});
    await tap('#battleReset');assert.equal(await p.evaluate('battle.hp'),100);
    await tap('#battleHit');
    assert.equal(await p.evaluate('battle.mode'),'hit');
    const battleStats=await p.evaluate(()=>({hp:battle.hp,mode:battle.mode}));
    await p.setViewportSize({width:320,height:700});await checkViewport();
    await p.setViewportSize({width:1180,height:820});await checkViewport();
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify({mobileViewport:'390×844, Chromium touch emulation',viewportWidths:[320,390,1180],
      backend,garmentIsolation,checkedFrames:Object.fromEntries(Object.entries(folded).map(([k,v])=>[k,v.length])),
      meshInversions:0,IKDistanceErrors:reaches,poseKeyframe:true,assetImportSplit:true,manualCrop:true,greenScreenSplit:true,outlinePreservedAtMerge:true,snap:true,weightBrushUndo:true,
      clipSharedAcrossRigs:true,projectRoundTrip:true,PNG:true,GIF:true,sheet:true,metadata:true,battle:battleStats,browserErrors:errors,androidOnDevice:false},null,2));
  }finally{await b.close();}
})().catch(e=>{console.error(e);process.exit(1);});
