'use strict';
const $=id=>document.getElementById(id), view=$('view'), context=view.getContext('2d');
let project=zeusProject(), loaded=new Map(), demo, demoSurfaces, boltImage;
let clipId='attack', time=0, playing=false, draft=null, tab='animate', boneId='chest', partId='zeus';
let camera={scale:1,x:0,y:0},panMode=false;
let dirty=true, revision=0, pending=false, gesture=null, tool='', selection=null, paintUndo=null;
let autosaveTimer, exportBusy=false, filePurpose='project';
let battle={mode:'idle',t:0,hp:100,hit:false,flash:0}, last=0, ready=false;
const messages={animate:'เลือกคลิปหรือเลื่อน Timeline',rig:'แตะจุดสีเพื่อเลือกกระดูก',art:'นำเข้า PNG หรือลากชิ้นส่วนในท่าพัก',battle:'สนามทดสอบ',export:'ส่งออกเฟรมโปร่งใสพร้อมใช้ในเกม'};
const status=text=>{$('status').textContent=text;};
const renderSoon=()=>{dirty=true;};
const currentClip=()=>project.clips[clipId];
const currentPart=()=>project.parts.find(p=>p.id===partId);
const boneName=id=>names[id]||id;
function option(value,label=value){
  const o=document.createElement('option');o.value=value;o.textContent=label;return o;
}
function fill(id,rows,selected){
  const el=$(id);el.replaceChildren(...rows.map(x=>option(...x)));el.value=selected;
}
function button(label,callback){
  const b=document.createElement('button');b.textContent=label;b.onclick=callback;return b;
}
function clipOptions(){
  $('clipList').replaceChildren(...Object.entries(project.clips).map(([id,c])=>{
    const b=button(c.name,()=>selectClip(id,true));
    b.classList.toggle('active',id===clipId);return b;
  }));
}
function selectClip(id,run=false){
  if(!project.clips[id])return;
  clipId=id;time=0;draft=null;playing=run;clipOptions();syncClip();syncPose();renderSoon();
}
function toTime(t){
  time=clamp(t,0,currentClip().duration);playing=false;draft=null;syncPose();syncMarkers();renderSoon();
}
function updateTransport(){
  const d=currentClip().duration;
  $('seek').max=d;$('seek').value=time;$('time').value=time.toFixed(2)+' / '+d.toFixed(2);
  $('play').textContent=playing?'Ⅱ':'▶︎';
}
function syncMarkers(){
  $('markers').replaceChildren(...currentClip().keys.map(k=>{
    const b=button(k.t.toFixed(2),()=>toTime(k.t));
    b.classList.toggle('active',Math.abs(k.t-time)<.004);return b;
  }));
}
function syncClip(){
  const c=currentClip();$('clipName').value=c.name;$('duration').value=c.duration;$('clipLoop').checked=c.loop;
  syncMarkers();updateTransport();
}
function syncPose(){
  const values=draft||sample(currentClip(),time), v=values.bones[boneId]||identity;
  $('poseBone').value=boneId;$('poseAngle').value=Math.round(v.a*100)/100;
  $('poseX').value=Math.round(v.x*100)/100;$('poseY').value=Math.round(v.y*100)/100;
  $('ease').value=values.ease||'smooth';
  const slots={...project.slots,...values.slots};
  for(const el of $('slotFields').querySelectorAll('select'))el.value=slots[el.dataset.slot]||el.options[0]?.value||'';
}
function syncSlots(){
  const entries={hand:{closed:'ปกติ',grip:'กำ',open:'แบ'},face:{neutral:'ปกติ',blink:'กะพริบ',focused:'มุ่งมั่น',shout:'ตะโกน'},weapon:{none:'มือเปล่า',bolt:'สายฟ้า',sword:'ดาบ'}};
  const labels={hand:'มือซ้าย',face:'สีหน้า',weapon:'อาวุธ'};
  $('slotFields').replaceChildren(...Object.entries(entries).map(([key,values])=>{
    const el=document.createElement('label');el.textContent=labels[key];
    const select=document.createElement('select');select.dataset.slot=key;
    for(const p of project.parts)if(p.slot===key)for(const v of Object.keys(p.variants))values[v]??=v;
    for(const [id,n] of Object.entries(values))select.append(option(id,n));
    select.onchange=()=>{
      editPose();
      draft.slots[key]=select.value;renderSoon();
    };
    el.append(select);return el;
  }));
  syncPose();
}
function isDescendant(id,p){
  for(let b=project.bones.find(b=>b.id===id);b?.parent;b=project.bones.find(z=>z.id===b.parent)){
    if(b.parent===p)return true;
  }
  return false;
}
function syncRig(){
  const bone=project.bones.find(b=>b.id===boneId), rows=project.bones.map(b=>[b.id,boneName(b.id)]);
  if(!bone)return;
  fill('bone',rows,boneId);fill('poseBone',rows,boneId);
  fill('parent',[['','ไม่มี'],...rows.filter(([id])=>id!==boneId&&!isDescendant(id,boneId))],bone.parent||'');
  fill('weightBone',rows,$('weightBone').value||boneId);
  $('boneX').value=Math.round(bone.x*100)/100;$('boneY').value=Math.round(bone.y*100)/100;
  $('boneA').value=Math.round(bone.a/D2R*100)/100;
  const spring=project.springs[boneId];
  $('springOn').checked=!!spring;
  for(const [k,n] of Object.entries({stiffness:90,damping:12,amount:.75})){
    $(k).value=spring?.[k]??n;$(k).disabled=!spring;
  }
  syncPose();
}
function syncArt(){
  const p=currentPart(), previously=$('weightBone').value;
  fill('part',project.parts.map(p=>[p.id,p.name]),partId);
  fill('partBone',project.bones.map(b=>[b.id,boneName(b.id)]),p?.bone||boneId);
  if(previously)$('weightBone').value=previously;
  for(const [id,key] of Object.entries({partX:'x',partY:'y',partA:'a',partScale:'scale',partSlot:'slot',binding:'bind'})){
    $(id).value=p?.[key]??'';$(id).disabled=!p;
  }
  $('partVisible').checked=!!p?.visible;$('seam').checked=!!p?.seam;
  for(const id of ['snapPart','removePart','layerUp','layerDown','variantPNG','partVisible','seam','paint','cut','partBone'])$(id).disabled=!p;
  $('applyCut').disabled=!selection||!p;
  $('stageCut').hidden=tab!=='art'||!selection||!p;
  $('mergeMesh').disabled=!p||project.parts.indexOf(p)<1;
  $('undoPaint').disabled=!paintUndo;
}
function syncAll(){
  $('projectName').textContent=project.name;$('characterName').value=project.name;
  clipOptions();syncClip();syncRig();syncSlots();syncArt();
}
function chooseTab(id){
  tab=id;tool='';selection=null;gesture=null;
  camera={scale:1,x:0,y:0};panMode=false;$('pan').classList.remove('active');
  $('zoomControls').hidden=id!=='art'&&id!=='rig';
  if(id!=='animate')playing=false;
  for(const el of document.querySelectorAll('[data-tab]'))el.setAttribute('aria-pressed',el.dataset.tab===id);
  for(const el of document.querySelectorAll('.panel'))el.hidden=el.id!==id;
  syncArt();status(messages[id]);renderSoon();
}
function editPose(){
  if(!draft)draft=copy(evaluate(project,currentClip(),time));
  // Display spring motion from the sampled clip, while the key stores authored rotations.
  for(const id of Object.keys(project.springs)){
    const base=sample(currentClip(),time).bones[id];
    if(!draft.springDraft&&draft.bones[id])draft.bones[id].a=base?.a??0;
  }
  draft.springDraft=true;playing=false;
}
function saveDB(){
  return new Promise((resolve,reject)=>{
    const request=indexedDB.open('chibi-live-studio',1);
    request.onupgradeneeded=()=>request.result.createObjectStore('projects');
    request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);
  });
}
async function checkpoint(){
  const d=await saveDB();
  try{
    await new Promise((resolve,reject)=>{
      const tr=d.transaction('projects','readwrite');tr.objectStore('projects').put({project,clipId},'active');
      tr.oncomplete=resolve;tr.onerror=()=>reject(tr.error);tr.onabort=()=>reject(tr.error);
    });
  }finally{d.close();}
}
function modified(){
  renderSoon();clearTimeout(autosaveTimer);
  autosaveTimer=setTimeout(()=>checkpoint().catch(()=>{}),350);
}
async function refreshSurfaces(){
  const stamp=++revision;
  pending=true;
  try{
    const next=await preflight(project);
    if(stamp===revision){loaded=next;renderSoon();}
  }catch(e){if(stamp===revision)status(e.message);}
  finally{if(stamp===revision)pending=false;}
}
async function installProject(candidate,preferred){
  const next=await preflight(candidate);
  revision++;pending=false;
  project=candidate;loaded=next;draft=null;time=0;playing=false;tool='';selection=null;paintUndo=null;
  clipId=project.clips[preferred]?preferred:Object.keys(project.clips)[0];
  boneId=project.bones.some(b=>b.id==='chest')?'chest':project.bones[0].id;partId=project.parts[0]?.id||'';
  battle={mode:'idle',t:0,hp:100,hit:false,flash:0};
  syncAll();renderSoon();
}
const background=canvas(),cameraSurface=canvas();
{
  const c=background.getContext('2d'), g=c.createLinearGradient(0,0,0,H);
  g.addColorStop(0,'#e5edf3');g.addColorStop(1,'#c9d7e0');
  c.fillStyle=g;c.fillRect(0,0,W,H);
  c.strokeStyle='#7f9aaf22';c.lineWidth=1;
  for(let x=5;x<W;x+=26){c.beginPath();c.moveTo(x,0);c.lineTo(x,H);c.stroke();}
  for(let y=12;y<H;y+=26){c.beginPath();c.moveTo(0,y);c.lineTo(W,y);c.stroke();}
}
function shadow(c,x=265,y=454,rx=90){
  c.fillStyle='#42607738';c.beginPath();c.ellipse(x,y,rx,9,0,0,Math.PI*2);c.fill();
}
function stage(c,{clean=false,t=time,p=currentClip(),pose=null}={}){
  c.clearRect(0,0,W,H);
  if(!clean){c.drawImage(background,0,0);shadow(c);}
  const bind=tab==='art'||(tab==='rig'&&$('bindPose').checked);
  const overlay=clean?null:{bones:tab==='rig'||tab==='art'||$('poseBones').checked,bone:boneId,
    mesh:tab==='art'&&tool==='paint',part:partId,weight:$('weightBone').value};
  const active=clean?pose:bind?{...makeKey(0),noPhysics:true}:draft;
  const result=drawActor(c,project,loaded,p,t,active,overlay);
  if(clean||!bind)mainProjectile(c,project,p,t,boltImage);
  if(!clean&&tab==='art'){
    const part=currentPart(), s=part&&(loaded.get(part.id)?.base||Object.values(loaded.get(part.id)||{})[0]);
    if(part&&s&&tool!=='paint'){
      c.save();c.translate(part.x,part.y);c.rotate(part.a*D2R);c.strokeStyle='#417790';c.lineWidth=1.5;
      c.setLineDash([6,4]);c.strokeRect(0,0,s.w*part.scale,s.h*part.scale);c.restore();
    }
    const rect=gesture?.base&&gesture.type==='cut'?[gesture.base,gesture.latest]:selection;
    if(rect){
      c.fillStyle='#39daba35';c.strokeStyle='#106e69';c.lineWidth=2;
      const [a,b]=rect;c.fillRect(a.x,a.y,b.x-a.x,b.y-a.y);c.strokeRect(a.x,a.y,b.x-a.x,b.y-a.y);
    }
  }
  return result;
}
function battleScene(c){
  const g=c.createLinearGradient(0,0,0,H);
  g.addColorStop(0,'#3d3760');g.addColorStop(.64,'#7b5d77');g.addColorStop(1,'#ba8e80');
  c.fillStyle=g;c.fillRect(0,0,W,H);
  c.fillStyle='#f7bd9470';c.beginPath();c.arc(118,118,66,0,7);c.fill();
  c.fillStyle='#655270';c.beginPath();c.moveTo(0,300);c.lineTo(62,216);c.lineTo(120,286);c.lineTo(210,177);c.lineTo(336,305);c.lineTo(432,222);c.lineTo(530,294);c.lineTo(530,440);c.lineTo(0,440);c.fill();
  c.fillStyle='#705971';c.fillRect(0,340,W,150);
  c.strokeStyle='#a68a9b70';c.lineWidth=1;
  for(let y of [351,378,417,471]){c.beginPath();c.moveTo(0,y);c.lineTo(W,y);c.stroke();}
  shadow(c,118,424,51);shadow(c,350,430,65);
  const clip=project.clips[battle.mode]||clips[battle.mode]||currentClip();
  const t=clip.loop&&battle.mode==='idle'?battle.t%clip.duration:Math.min(clip.duration,battle.t);
  c.save();c.translate(169,116);c.scale(.69,.69);
  drawActor(c,project,loaded,clip,t);
  const projectile=mainProjectile(c,project,clip,t,boltImage,true);
  c.restore();
  if(projectile&&169+.69*projectile.x<150&&!battle.hit&&battle.hp>0){
    battle.hp=Math.max(0,battle.hp-25);battle.hit=true;battle.flash=.25;
  }
  c.save();c.translate(118,424);c.rotate(battle.hp===0?-.62:battle.flash>.1?-.18:0);c.scale(.40,.4);c.translate(-265,-454);
  if(demo&&demoSurfaces)drawActor(c,demo,demoSurfaces,battle.flash>0?clips.hit:clips.idle,battle.flash>0?.22-battle.flash:battle.t%1.8);
  c.restore();
  if(battle.flash>0){
    c.strokeStyle='#ffdda4';c.lineWidth=3;
    for(let i=0;i<8;i++){
      const a=i*Math.PI/4, r=20+(1-battle.flash/.25)*13;
      c.beginPath();c.moveTo(121+Math.cos(a)*9,330+Math.sin(a)*9);c.lineTo(121+Math.cos(a)*r,330+Math.sin(a)*r);c.stroke();
    }
  }
  c.fillStyle='#161e2b';c.fillRect(63,211,109,9);c.fillStyle='#f4a694';c.fillRect(63,211,battle.hp*1.09,9);
  c.fillStyle='#f4f3fa';c.textAlign='center';c.font='bold 15px system-ui';c.fillText(battle.hp+' / 100',118,202);
}
function animate(now){
  const elapsed=last?Math.min(.055,(now-last)/1000):0;last=now;
  if(ready&&tab==='battle'){
    battle.flash=Math.max(0,battle.flash-elapsed);battle.t+=elapsed;
    if(battle.mode!=='idle'&&battle.t>=(project.clips[battle.mode]||clips[battle.mode]).duration){
      battle.mode='idle';battle.t=0;
    }
    battleScene(context);
    $('sceneLabel').textContent='สนามซ้อม';$('stageInfo').textContent='เป้าฝึก '+battle.hp+' HP';
  }else if(ready&&(dirty||playing)){
    if(playing){
      const c=currentClip();time+=elapsed;
      if(time>c.duration){if(c.loop)time%=c.duration;else{time=c.duration;playing=false;syncPose();}}
    }
    let result;
    if(camera.scale===1)result=stage(context);
    else{
      result=stage(cameraSurface.getContext('2d'));
      context.clearRect(0,0,W,H);
      context.drawImage(cameraSurface,camera.x,camera.y,W*camera.scale,H*camera.scale);
    }
    dirty=false;updateTransport();
    $('sceneLabel').textContent=project.name+' / '+(tab==='rig'?'Rig':tab==='art'?'PNG':currentClip().name);
    $('stageInfo').textContent=result.folded?'เมชพับ '+result.folded+' จุด':result.triangles?result.triangles.toLocaleString()+' triangles':project.bones.length+' bones';
  }
  requestAnimationFrame(animate);
}
for(const b of document.querySelectorAll('[data-tab]'))b.onclick=()=>chooseTab(b.dataset.tab);
function setCamera(){
  camera.x=clamp(camera.x,W*(1-camera.scale),0);
  camera.y=clamp(camera.y,H*(1-camera.scale),0);
  if(camera.scale===1){panMode=false;$('pan').classList.remove('active');}
  renderSoon();
}
function zoomBy(delta){
  const scale=clamp(camera.scale+delta,1,3.5), q=scale/camera.scale;
  camera.x=W/2+(camera.x-W/2)*q;camera.y=H/2+(camera.y-H/2)*q;camera.scale=scale;
  setCamera();
}
$('zoomIn').onclick=()=>zoomBy(.5);
$('zoomOut').onclick=()=>zoomBy(-.5);
$('pan').onclick=()=>{
  if(camera.scale===1)zoomBy(.5);
  panMode=!panMode;$('pan').classList.toggle('active',panMode);
  if(panMode)status('ลากภาพเพื่อเลื่อนมุมมอง');
};

$('seek').oninput=e=>toTime(+e.target.value);
$('rewind').onclick=()=>toTime(0);
$('play').onclick=()=>{
  if(tab==='battle')return;
  if(tab==='art')chooseTab('animate');
  if(tab==='rig')$('bindPose').checked=false;
  if(!playing){draft=null;if(time>=currentClip().duration)time=0;}
  playing=!playing;if(!playing)syncPose();renderSoon();
};
$('newClip').onclick=()=>{
  if(Object.keys(project.clips).length>=36){status('เก็บได้สูงสุด 36 คลิป');return;}
  const id=nextId('clip',Object.keys(project.clips));
  project.clips[id]={name:'คลิป '+(Object.keys(project.clips).length+1),duration:1.2,loop:true,keys:[makeKey(0)]};
  selectClip(id);status('เพิ่มคลิปแล้ว');modified();
};
$('putKey').onclick=()=>{
  if(currentClip().keys.length>=300&&!currentClip().keys.some(k=>Math.abs(k.t-time)<.004)){status('เก็บได้สูงสุด 300 Keyframe');return;}
  const k=copy(draft||sample(currentClip(),time));
  k.t=Math.min(currentClip().duration,Math.round(time*1000)/1000);k.ease=$('ease').value;
  delete k.springDraft;
  currentClip().keys=currentClip().keys.filter(x=>Math.abs(x.t-k.t)>.003);
  currentClip().keys.push(k);currentClip().keys.sort((a,b)=>a.t-b.t);
  toTime(k.t);status('บันทึก Keyframe ที่ '+k.t.toFixed(3)+' วินาที');modified();
};
$('dropKey').onclick=()=>{
  const at=currentClip().keys.findIndex(k=>Math.abs(k.t-time)<.004);
  if(at<0){status('แตะเวลา Keyframe ที่ต้องการลบ');return;}
  currentClip().keys.splice(at,1);toTime(time);status('ลบ Keyframe แล้ว');modified();
};
$('duration').onchange=e=>{
  const c=currentClip(), next=clamp(+e.target.value||c.duration,.1,12);
  if(c.keys.some(k=>k.t>next)||c.event>next){e.target.value=c.duration;status('ย้ายหรือลบ Keyframe ท้ายคลิปก่อนลดเวลา');return;}
  c.duration=next;syncClip();modified();
};
$('clipName').onchange=e=>{currentClip().name=e.target.value.trim()||currentClip().name;clipOptions();modified();};
$('clipLoop').onchange=e=>{currentClip().loop=e.target.checked;modified();};
$('ease').onchange=e=>{editPose();draft.ease=e.target.value;renderSoon();};
$('poseBones').onchange=renderSoon;
$('bindPose').onchange=()=>{draft=null;playing=false;renderSoon();};
function selectBone(id){
  boneId=id;syncRig();renderSoon();
}
$('poseBone').onchange=e=>selectBone(e.target.value);
$('bone').onchange=e=>selectBone(e.target.value);
for(const [id,key] of Object.entries({poseAngle:'a',poseX:'x',poseY:'y'}))$(id).onchange=e=>{
  editPose();
  const v=draft.bones[boneId]||identity;
  draft.bones[boneId]={...v,[key]:clamp(+e.target.value||0,key==='a'?-180:-2000,key==='a'?180:2000)};
  syncPose();renderSoon();
};
for(const [id,key] of Object.entries({boneX:'x',boneY:'y',boneA:'a'}))$(id).onchange=e=>{
  const b=project.bones.find(b=>b.id===boneId), value=+e.target.value||0;
  b[key]=key==='a'?clamp(value,-180,180)*D2R:clamp(value,-2000,2000);
  modified();refreshSurfaces();syncRig();
};
$('parent').onchange=e=>{
  const parent=e.target.value||null;
  if(parent===boneId||isDescendant(parent,boneId))return;
  const model=fk(project.bones), b=project.bones.find(b=>b.id===boneId), w=model[boneId], p=model[parent]||identity;
  const [x,y]=turn(w.x-p.x,w.y-p.y,-p.a);
  Object.assign(b,{parent,x,y,a:w.a-p.a});syncRig();modified();refreshSurfaces();
};
$('addBone').onclick=()=>{
  const id=$('newBoneName').value.trim();
  if(!safeId(id)||project.bones.some(b=>b.id===id)||project.bones.length>=70){status('ชื่อกระดูกซ้ำหรือไม่ถูกต้อง');return;}
  project.bones.push({id,parent:boneId,x:20,y:20,a:0,color:'#98edb1'});
  boneId=id;$('newBoneName').value='';syncRig();syncArt();modified();refreshSurfaces();
};
$('dropBone').onclick=()=>{
  if(project.bones.length===1||project.bones.some(b=>b.parent===boneId)||project.parts.some(p=>p.bone===boneId)){
    status('ลบได้เฉพาะกระดูกปลายที่ไม่มีชิ้นส่วนผูกอยู่');return;
  }
  if(project.parts.some(p=>p.bind==='zeus')&&boneList.some(b=>b[0]===boneId)){
    status('กระดูกนี้เป็นส่วนหนึ่งของเมชซุส');return;
  }
  const old=boneId;project.bones=project.bones.filter(b=>b.id!==old);boneId=project.bones[0].id;
  for(const p of project.parts)for(const [i,w] of Object.entries(p.paint)){
    if(!(old in w))continue;delete w[old];p.paint[i]=normalizeWeights(w);
    if(!Object.keys(p.paint[i]).length)delete p.paint[i];
  }
  delete project.springs[old];
  for(const c of Object.values(project.clips))for(const k of c.keys)delete k.bones[old];
  syncRig();syncArt();modified();refreshSurfaces();
};
$('springOn').onchange=e=>{
  if(e.target.checked)project.springs[boneId]={stiffness:90,damping:12,amount:.75};
  else delete project.springs[boneId];syncRig();modified();
};
for(const [key,[lo,hi]] of Object.entries({stiffness:[20,190],damping:[2,28],amount:[0,2]}))$(key).onchange=e=>{
  const s=project.springs[boneId];if(!s)return;s[key]=clamp(Number(e.target.value),lo,hi);syncRig();modified();
};
function nextId(prefix,ids){
  let n=1;while(ids.includes(prefix+'_'+n))n++;return prefix+'_'+n;
}
function selectPart(id){
  partId=id;selection=null;tool='';syncArt();renderSoon();
}
$('part').onchange=e=>selectPart(e.target.value);
$('partBone').onchange=e=>{
  const p=currentPart();p.bone=e.target.value;modified();refreshSurfaces();
};
for(const [id,key] of Object.entries({partX:'x',partY:'y',partA:'a',partScale:'scale'}))$(id).onchange=e=>{
  const p=currentPart();p[key]=clamp(Number(e.target.value)||0,key==='scale'?.02:-2000,key==='scale'?6:2000);
  syncArt();modified();refreshSurfaces();
};
$('partSlot').onchange=e=>{
  currentPart().slot=e.target.value;syncSlots();modified();
};
$('partVisible').onchange=e=>{currentPart().visible=e.target.checked;modified();};
$('seam').onchange=e=>{currentPart().seam=e.target.checked;modified();};
$('binding').onchange=e=>{
  const p=currentPart();
  if(e.target.value==='zeus'&&p.src!==ART.source){syncArt();status('เมชซุสใช้กับภาพซุสดั้งเดิม');return;}
  p.bind=e.target.value;modified();refreshSurfaces();
};
function spriteInfo(p){
  const entry=loaded.get(p.id)||{};
  return entry.base||Object.values(entry)[0];
}
function pivotOffset(p,s){
  const id=p.bone;
  const u=id==='head'?.92:id.startsWith('foot')?.45:id==='chest'?.51:.19;
  return turn(s.w*p.scale*.5,s.h*p.scale*u,p.a*D2R);
}
function snapPart(p){
  const s=spriteInfo(p), b=fk(project.bones)[p.bone];
  if(!s||!b)return;
  const [x,y]=pivotOffset(p,s);p.x=b.x-x;p.y=b.y-y;
}
$('snapPart').onclick=()=>{snapPart(currentPart());syncArt();modified();refreshSurfaces();};
function moveLayer(dir){
  const ps=project.parts,i=ps.findIndex(p=>p.id===partId),j=i+dir;
  if(i<0||j<0||j>=ps.length)return;
  [ps[i],ps[j]]=[ps[j],ps[i]];syncArt();modified();
}
$('layerUp').onclick=()=>moveLayer(1);
$('layerDown').onclick=()=>moveLayer(-1);
$('removePart').onclick=()=>{
  project.parts=project.parts.filter(p=>p.id!==partId);
  if(paintUndo?.part===partId)paintUndo=null;
  selectPart(project.parts[0]?.id||'');syncSlots();modified();refreshSurfaces();
};
$('importPNG').onclick=()=>$('filePNG').click();
$('filePNG').onchange=async e=>{
  const files=[...e.target.files];e.target.value='';
  if(!files.length)return;
  const sourceProject=project, method=$('pngMode').value, additions=[], ids=project.parts.map(p=>p.id);
  try{
    for(const file of files){
      const c=await sourceFromFile(file);
      const items=method==='single'?[{src:c.toDataURL(),x:0,y:0,w:c.width,h:c.height}]:splitImage(c,method);
      if(!items.length)throw Error('ไม่พบชิ้นส่วนใน PNG');
      if(ids.length+items.length>72)throw Error('เก็บได้สูงสุด 72 ชิ้นต่อโปรเจกต์');
      const f=Math.min(1,360/c.width,400/c.height),rest=fk(sourceProject.bones);
      for(let i=0;i<items.length;i++){
        const item=items[i], id=nextId('part',ids), x=265+(item.x-c.width/2)*f,y=248+(item.y-c.height/2)*f;
        const target=[x+item.w*f/2,y+item.h*f/2];
        const near=sourceProject.bones.filter(b=>b.parent!==null);
        const bone=near.sort((a,b)=>Math.hypot(rest[a.id].x-target[0],rest[a.id].y-target[1])-Math.hypot(rest[b.id].x-target[0],rest[b.id].y-target[1]))[0]?.id||boneId;
        const name=file.name.replace(/\.png$/i,'').slice(0,86)+(items.length>1?' · '+(i+1):'');
        additions.push({...copy(partDefaults),id,name,src:item.src,x,y,scale:f,bone});
        ids.push(id);
      }
    }
    if(sourceProject!==project)return;
    project.parts.push(...additions);selectPart(additions[0].id);syncSlots();modified();
    await refreshSurfaces();status('นำเข้า '+additions.length+' ชิ้น');
  }catch(e){status(e.message);}
};
$('variantPNG').onclick=()=>{
  if(!currentPart()?.slot||!safeId($('variantName').value.trim())||$('variantName').value.trim()==='none'){
    status('เลือก Slot และตั้งชื่อภาพสลับด้วย a–z, 0–9 หรือ _');return;
  }
  if(Object.keys(currentPart().variants).length>=12&&!Object.hasOwn(currentPart().variants,$('variantName').value.trim())){
    status('เก็บได้สูงสุด 12 ภาพต่อชิ้น');return;
  }
  $('fileVariant').click();
};
$('fileVariant').onchange=async e=>{
  const file=e.target.files[0], part=currentPart(), id=$('variantName').value.trim();
  e.target.value='';if(!file||!part)return;
  try{
    const c=await sourceFromFile(file);
    part.variants[id]=c.toDataURL();syncSlots();modified();
    await refreshSurfaces();status('เพิ่มภาพสลับ '+id);
  }catch(e){status(e.message);}
};
$('cut').onclick=()=>{
  tool=tool==='cut'?'':'cut';selection=null;syncArt();renderSoon();
  if(tool){panMode=false;$('pan').classList.remove('active');view.scrollIntoView({block:'center'});}
  status(tool?'ลากกรอบบน PNG ที่เลือก':'ยกเลิกการตัด');
};
function localPoint(part,p){
  const [x,y]=turn(p.x-part.x,p.y-part.y,-part.a*D2R);
  return {x:x/part.scale,y:y/part.scale};
}
$('applyCut').onclick=async()=>{
  const p=currentPart(),s=p&&spriteInfo(p);
  if(!s||!selection)return;
  if(Object.keys(p.variants).length){status('เลือกชั้นภาพต้นฉบับที่ไม่มีภาพสลับก่อนตัด');return;}
  if(project.parts.length>=72){status('เก็บได้สูงสุด 72 ชิ้น');return;}
  const [a,b]=selection;
  const sourceBox=[a,b,{x:a.x,y:b.y},{x:b.x,y:a.y}].map(v=>localPoint(p,v));
  const x=clamp(Math.floor(Math.min(...sourceBox.map(p=>p.x))),0,s.w),y=clamp(Math.floor(Math.min(...sourceBox.map(p=>p.y))),0,s.h);
  const w=clamp(Math.ceil(Math.max(...sourceBox.map(p=>p.x))),0,s.w)-x,h=clamp(Math.ceil(Math.max(...sourceBox.map(p=>p.y))),0,s.h)-y;
  if(w<2||h<2){status('กรอบตัดอยู่นอกภาพ');return;}
  const remaining=canvas(s.w,s.h), rc=remaining.getContext('2d'), extracted=canvas(w,h), ec=extracted.getContext('2d');
  rc.drawImage(s.image,0,0);
  const piece=rc.getImageData(x,y,w,h);
  if(!piece.data.some((v,i)=>i%4===3&&v>0)){status('บริเวณนี้ไม่มีพิกเซล');return;}
  ec.putImageData(piece,0,0);rc.clearRect(x,y,w,h);
  p.src=remaining.toDataURL();
  if(p.bind==='zeus')p.bind='auto';
  const [dx,dy]=turn(x*p.scale,y*p.scale,p.a*D2R);
  const id=nextId('part',project.parts.map(p=>p.id));
  const piecePart={...copy(partDefaults),id,src:extracted.toDataURL(),name:p.name.slice(0,88)+' · ตัด',bone:p.bone,x:p.x+dx,y:p.y+dy,a:p.a,scale:p.scale};
  project.parts.splice(project.parts.indexOf(p)+1,0,piecePart);
  selectPart(id);modified();await refreshSurfaces();status('แยกชิ้นส่วนแล้ว');
};
$('stageCut').onclick=()=>$('applyCut').click();
$('paint').onclick=async()=>{
  const p=currentPart();if(!p||!spriteInfo(p))return;
  if(p.bind==='rigid'){p.bind='auto';modified();await refreshSurfaces();}
  tool=tool==='paint'?'':'paint';selection=null;syncArt();renderSoon();
  if(tool){panMode=false;$('pan').classList.remove('active');view.scrollIntoView({block:'center'});}
  status(tool?'เลือกกระดูก แล้วลากระบายจุดบนเมช':'ปิดแปรง Weight');
};
$('undoPaint').onclick=()=>{
  if(!paintUndo)return;
  const p=project.parts.find(p=>p.id===paintUndo.part);
  if(p)p.paint=paintUndo.paint;
  paintUndo=null;syncArt();modified();refreshSurfaces();
};
$('weightBone').onchange=renderSoon;
function brush({x,y}){
  const p=currentPart(), s=p&&spriteInfo(p), bone=$('weightBone').value, radius=+$('radius').value, amount=+$('strength').value;
  if(!s||!bone||!s.weights)return;
  const erase=$('brushMode').value==='erase';
  const update=new Map();
  for(let i=0;i<s.points.length;i++){
    const v=s.points[i],[u,z]=turn(v.x*p.scale,v.y*p.scale,p.a*D2R);
    const f=amount*smooth(1-Math.hypot(p.x+u-x,p.y+z-y)/radius);
    if(f<.005)continue;
    const weights={...(p.paint[i]||s.weights[i])};
    if(erase){
      const current=weights[bone]||0, other=Object.entries(weights).filter(([id])=>id!==bone);
      if(!current)continue;
      if(!other.length){
        const fallback=project.bones.find(b=>b.id===bone)?.parent||project.bones.find(b=>b.id!==bone)?.id;
        if(!fallback||fallback===bone)continue;
        weights[fallback]=current*f;
      }else for(const [id,value] of other)weights[id]=value+current*f*value/(1-current);
      weights[bone]=current*(1-f);
    }else{
      for(const id of Object.keys(weights))weights[id]*=1-f;
      weights[bone]=(weights[bone]||0)+f;
    }
    update.set(i,normalizeWeights(weights));
  }
  for(const [i,value] of update){
    p.paint[i]=value;
    for(const target of Object.values(loaded.get(p.id)||{}))if(target.weights?.[i])target.weights[i]=value;
  }
  if(update.size){renderSoon();gesture.changed=true;}
}
function screenPoint(e){
  const rect=view.getBoundingClientRect(), scale=Math.min(rect.width/W,rect.height/H);
  return {x:(e.clientX-rect.left-(rect.width-W*scale)/2)/scale,y:(e.clientY-rect.top-(rect.height-H*scale)/2)/scale};
}
function canvasPoint(e){
  const p=screenPoint(e);
  return {x:(p.x-camera.x)/camera.scale,y:(p.y-camera.y)/camera.scale};
}
function nearest(world,q,range){
  let result=null;
  for(const [id,w] of Object.entries(world)){
    const d=Math.hypot(q.x-w.x,q.y-w.y);
    if(d<range){result=id;range=d;}
  }
  return result;
}
function finishGesture(e){
  if(!gesture||gesture.pointer!==e.pointerId)return;
  const g=gesture;gesture=null;
  if(g.type==='cut'){selection=[g.base,g.latest];syncArt();}
  if(g.type==='part'&&g.changed&&$('snap').checked){
    const p=currentPart(),s=p&&spriteInfo(p), rest=fk(project.bones);
    if(s){
      const [x,y]=pivotOffset(p,s);
      const at=nearest(rest,{x:p.x+x,y:p.y+y},14);
      if(at){p.bone=at;snapPart(p);status('Snap เข้ากระดูก '+boneName(at));}
    }
  }
  if(g.changed&&['part','paint','rest'].includes(g.type)){
    modified();
    if(g.type!=='paint')refreshSurfaces();
  }
  syncRig();syncArt();renderSoon();
}
view.onpointerdown=e=>{
  if(!ready||pending||gesture||tab==='battle'||tab==='export')return;
  const q=canvasPoint(e);
  if(panMode){
    gesture={type:'pan',pointer:e.pointerId,point:screenPoint(e),x:camera.x,y:camera.y};
    view.setPointerCapture(e.pointerId);e.preventDefault();return;
  }
  if(tab==='art'){
    const p=currentPart(),s=p&&spriteInfo(p);
    if(!s)return;
    if(tool==='paint'){
      gesture={type:'paint',pointer:e.pointerId,latest:q};
      paintUndo={part:partId,paint:copy(p.paint)};brush(q);syncArt();
    }else if(tool==='cut')gesture={type:'cut',pointer:e.pointerId,base:q,latest:q};
    else{
      const found=project.parts.slice().reverse().find(c=>{
        const sprite=spriteInfo(c);
        if(!sprite||!c.visible)return false;
        const {x,y}=localPoint(c,q), i=(Math.floor(y)*sprite.w+Math.floor(x))*4+3;
        return x>=0&&y>=0&&x<sprite.w&&y<sprite.h&&sprite.pixels[i]>12;
      });
      if(!found)return;
      if(found.id!==partId)selectPart(found.id);
      gesture={type:'part',pointer:e.pointerId,base:q,x:found.x,y:found.y};
    }
  }else{
    const bind=tab==='rig'&&$('bindPose').checked;
    if(!bind&&tab!=='rig'&&!$('poseBones').checked)return;
    const w=fk(project.bones,bind?{}:(draft||evaluate(project,currentClip(),time)).bones);
    const id=nearest(w,q,18);
    if(!id)return;
    selectBone(id);
    if(!bind)editPose();
    const chain=chains.find(c=>c[2]===id&&project.bones.find(b=>b.id===c[1])?.parent===c[0]&&project.bones.find(b=>b.id===c[2])?.parent===c[1]);
    const bend=chain&&[w[chain[0]],w[chain[1]],w[chain[2]]];
    const sign=bend&&Math.sign((bend[1].x-bend[0].x)*(bend[2].y-bend[1].y)-(bend[1].y-bend[0].y)*(bend[2].x-bend[1].x));
    gesture={type:bind?'rest':chain&&$('poseIK').checked?'ik':'pose',pointer:e.pointerId,chain,sign:sign||chain?.[3],offset:[w[id].x-q.x,w[id].y-q.y]};
  }
  view.setPointerCapture(e.pointerId);e.preventDefault();renderSoon();
};
view.onpointermove=e=>{
  if(!gesture||gesture.pointer!==e.pointerId)return;
  const g=gesture, q=canvasPoint(e);
  if(g.type==='pan'){
    const p=screenPoint(e);camera.x=g.x+p.x-g.point.x;camera.y=g.y+p.y-g.point.y;setCamera();return;
  }
  if(g.type==='paint'){
    const d=Math.hypot(q.x-g.latest.x,q.y-g.latest.y), n=Math.min(25,Math.max(1,Math.ceil(d/(+$('radius').value*.36))));
    for(let i=1;i<=n;i++)brush({x:mix(g.latest.x,q.x,i/n),y:mix(g.latest.y,q.y,i/n)});
    g.latest=q;return;
  }
  if(g.type==='cut'){g.latest=q;renderSoon();return;}
  if(g.type==='part'){
    const p=currentPart();p.x=clamp(g.x+q.x-g.base.x,-2000,2000);p.y=clamp(g.y+q.y-g.base.y,-2000,2000);
  }else{
    const [dx,dy]=g.offset;
    let x=q.x+dx,y=q.y+dy;
    if(g.type==='rest'&&$('snap').checked){x=Math.round(x/5)*5;y=Math.round(y/5)*5;}
    if(g.type==='ik'){
      solveIK(project.bones,draft.bones,g.chain,x,y,g.sign);
      draft.freeFeet={...draft.freeFeet,[g.chain[2]]:true};
    }else{
      const b=project.bones.find(b=>b.id===boneId), w=fk(project.bones,g.type==='rest'?{}:draft.bones), p=w[b.parent]||identity;
      const [tx,ty]=turn(x-p.x,y-p.y,-p.a);
      if(g.type==='rest')Object.assign(b,{x:tx,y:ty});
      else draft.bones[boneId]={...(draft.bones[boneId]||identity),x:tx-b.x,y:ty-b.y};
    }
  }
  g.changed=true;renderSoon();
};
view.onpointerup=view.onpointercancel=view.onlostpointercapture=finishGesture;
$('battleAttack').onclick=()=>{battle.mode='attack';battle.t=0;battle.hit=false;};
$('battleHit').onclick=()=>{battle.mode='hit';battle.t=0;battle.hit=false;};
$('battleReset').onclick=()=>{battle={mode:'idle',t:0,hp:100,hit:false,flash:0};};
async function saveBlob(blob,name){
  if(!blob)throw Error('สร้างไฟล์ไม่สำเร็จ');
  if(window.AndroidFiles){
    const api=window.AndroidFiles;
    if(!api.begin(name,blob.type))throw Error('เปิดตัวบันทึก Android ไม่ได้');
    try{
      for(let i=0;i<blob.size;i+=128*1024){
        const bytes=new Uint8Array(await blob.slice(i,i+128*1024).arrayBuffer());
        let raw='';
        for(let n=0;n<bytes.length;n+=4096)raw+=String.fromCharCode(...bytes.subarray(n,n+4096));
        if(!api.append(btoa(raw)))throw Error('ส่งข้อมูลไปยัง Android ไม่สำเร็จ');
      }
      if(!api.finish())throw Error('เปิดให้เลือกตำแหน่งบันทึกไม่ได้');
      return true;
    }catch(e){api.abort();throw e;}
  }
  const url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download=name;document.body.append(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),18000);
  return false;
}
window.nativeExportStatus=state=>status(state==='ok'?'บันทึกไฟล์แล้ว':state==='cancel'?'ยกเลิกการบันทึก':'Android เขียนไฟล์ไม่สำเร็จ');
const jsonBlob=data=>new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
const filePrefix=()=>((project.name+'_'+clipId).replace(/[^a-z0-9_-]/gi,'_').slice(0,60)||'chibi');
function imageBlob(c){
  return new Promise(resolve=>c.toBlob(resolve,'image/png'));
}
function getFrames(sheet=false){
  const size=+$('size').value,fps=+$('fps').value,c=currentClip(),cols=+$('columns').value;
  const n=Math.max(2,Math.ceil(c.duration*fps));
  if(sheet && Math.ceil(n/cols)*size>4096)fail('Sprite Sheet สูงเกิน 4096 px ลองลดขนาดเฟรม ลด FPS หรือเพิ่มคอลัมน์');
  if(!sheet && n*size*size>28500000)fail('GIF ชุดนี้ใหญ่เกินหน่วยความจำที่ตั้งไว้ ลองลดขนาดเฟรมหรือ FPS');
  return {size,fps,cols,n,c,times:Array.from({length:n},(_,i)=>c.duration*i/(c.loop?n:n-1))};
}
function drawSquare(target,size,scratch,t,clip,override=null){
  stage(scratch.getContext('2d'),{clean:true,t,p:clip,pose:override});
  target.clearRect(0,0,size,size);
  const f=size/Math.max(W,H);
  target.drawImage(scratch,(size-W*f)/2,(size-H*f)/2,W*f,H*f);
}
function meta({size,fps,cols,n,c,times}){
  const effectiveFps=n/c.duration;
  return {schema:'chibi.sprite-sheet.v1',image:filePrefix()+'_sheet.png',clip:c.name,frameSize:{width:size,height:size},
    columns:cols,rows:Math.ceil(n/cols),fps:effectiveFps,requestedFps:fps,
    duration:c.duration,loop:c.loop,events:c.event===undefined?[]:[{name:'release',time:c.event}],
    pivot:{x:265/W,y:((W-H)/2+454)/W},frames:times.map((time,i)=>({index:i,time,x:i%cols*size,y:Math.floor(i/cols)*size,w:size,h:size}))};
}
async function runExport(work){
  if(!ready||pending||exportBusy)return;
  exportBusy=true;playing=false;
  const controls=[$('exportPNG'),$('exportGIF'),$('exportSheet'),$('saveProject'),$('exportMeta'),$('quickSave'),$('exportClip')];
  controls.forEach(x=>x.disabled=true);
  try{
    const [blob,name]=await work(), native=await saveBlob(blob,name);
    status(native?'เลือกตำแหน่งบันทึกใน Android': 'ส่งออก '+name+' แล้ว');
  }catch(e){status(e.message);}
  finally{exportBusy=false;controls.forEach(x=>x.disabled=false);renderSoon();}
}
$('exportPNG').onclick=()=>runExport(async()=>{
  const size=+$('size').value, c=canvas(size,size);
  drawSquare(c.getContext('2d'),size,canvas(),time,currentClip(),draft);
  return [await imageBlob(c),filePrefix()+'.png'];
});
$('exportSheet').onclick=()=>runExport(async()=>{
  const info=getFrames(true),{size,cols,n,times,c}=info;
  status('กำลังเรนเดอร์ '+n+' เฟรม');
  await new Promise(requestAnimationFrame);
  const square=canvas(size,size), dest=canvas(cols*size,Math.ceil(n/cols)*size), scratch=canvas();
  const x=square.getContext('2d'), out=dest.getContext('2d');
  for(let i=0;i<n;i++){
    drawSquare(x,size,scratch,times[i],c);out.drawImage(square,i%cols*size,Math.floor(i/cols)*size);
  }
  return [await imageBlob(dest),filePrefix()+'_sheet.png'];
});
$('exportMeta').onclick=()=>runExport(async()=>[jsonBlob(meta(getFrames(true))),filePrefix()+'_frames.json']);
$('exportGIF').onclick=()=>runExport(async()=>{
  const {size,n,times,c}=getFrames();
  status('กำลังเรนเดอร์ GIF '+n+' เฟรม');
  await new Promise(requestAnimationFrame);
  const square=canvas(size,size), scratch=canvas(), x=square.getContext('2d',{willReadFrequently:true}), frames=[];
  for(let i=0;i<n;i++){
    drawSquare(x,size,scratch,times[i],c);frames.push(x.getImageData(0,0,size,size).data);
  }
  return [createGif(frames,size,size,n/c.duration,c.loop),filePrefix()+'.gif'];
});
function exportProject(){
  runExport(async()=>[jsonBlob(project),filePrefix()+'_project.json']);
}
$('quickSave').onclick=$('saveProject').onclick=exportProject;
$('exportClip').onclick=()=>runExport(async()=>{
  const lengths=Object.fromEntries(project.bones.map(b=>[b.id,Math.hypot(b.x,b.y)]));
  return [jsonBlob({schema:'chibi.clip.v1',clip:currentClip(),lengths}),filePrefix()+'_clip.json'];
});
function browseJson(purpose){filePurpose=purpose;$('fileJson').click();}
$('loadProject').onclick=()=>browseJson('project');
$('importClip').onclick=()=>browseJson('clip');
$('fileJson').onchange=async e=>{
  const file=e.target.files[0], purpose=filePurpose;
  e.target.value='';if(!file)return;
  try{
    if(file.size>55*1024*1024)fail('JSON ใหญ่เกิน 55 MB');
    const data=JSON.parse(await file.text());
    if(purpose==='clip'){
      if(data.schema!=='chibi.clip.v1')fail('เลือก JSON คลิปที่ส่งจาก Chibi Live Studio');
      if(Object.keys(project.clips).length>=36)fail('เก็บได้สูงสุด 36 คลิป');
      const existing=new Map(project.bones.map(b=>[b.id,b]));
      const c=validateClip(data.clip), matched=new Set();
      const hasMotion=c.keys.some(k=>Object.keys(k.bones).length);
      for(const key of c.keys){
        for(const id of Object.keys(key.bones)){
          const b=existing.get(id);
          if(!b){delete key.bones[id];continue;}
          matched.add(id);
          const len=data.lengths?.[id], target=Math.hypot(b.x,b.y);
          const scale=id!=='root'&&finite(len,1,2000)?clamp(target/len,.25,4):1;
          key.bones[id].x=clamp(key.bones[id].x*scale,-2000,2000);
          key.bones[id].y=clamp(key.bones[id].y*scale,-2000,2000);
        }
      }
      if(!matched.size && hasMotion)fail('ชื่อกระดูกในคลิปไม่ตรงกับ Rig');
      const id=nextId('clip',Object.keys(project.clips));
      project.clips[id]=c;selectClip(id);modified();status('นำเข้าคลิปแล้ว · ตรงกัน '+matched.size+' กระดูก');
    }else{
      const older=data.version===4, parsed=convertPrevious(data);
      validateProject(parsed);await completeLegacy(parsed);
      await installProject(parsed,older?'imported':'attack');modified();
      status(older?'เปิดโปรเจกต์รุ่นก่อนแล้ว ตรวจท่าและภาพหลังแปลง':'เปิดโปรเจกต์แล้ว');
    }
  }catch(e){status('เปิดไฟล์ไม่ได้ · '+e.message);}
};
$('characterName').onchange=e=>{
  project.name=e.target.value.trim()||project.name;$('projectName').textContent=project.name;modified();
};
async function switchSample(build,label){
  try{
    if(draft)status('ท่าร่างยังไม่มี Keyframe');
    clearTimeout(autosaveTimer);
    await checkpoint().catch(()=>{});
    await installProject(build(),'attack');status(label);
  }catch(e){status(e.message);}
}
$('zeus').onclick=()=>switchSample(zeusProject,'เปิดซุส');
$('blank').onclick=()=>switchSample(()=>newProject('New character'),'เปิด Rig เปล่า');
$('dummy').onclick=()=>switchSample(()=>{const p=newProject('Practice knight');p.parts=characterParts(p);
  p.clips.attack.name='โจมตี';delete p.clips.attack.event;return p;},'เปิดหุ่นฝึก');
$('recover').onclick=async()=>{
  clearTimeout(autosaveTimer);
  try{
    const d=await saveDB();
    const previous=await new Promise((resolve,reject)=>{
      const q=d.transaction('projects').objectStore('projects').get('active');
      q.onsuccess=()=>resolve(q.result);q.onerror=()=>reject(q.error);
    });
    d.close();
    if(!previous)fail('ยังไม่มีฉบับบันทึกในเครื่อง');
    await installProject(validateProject(previous.project),previous.clipId);status('เปิดฉบับบันทึกในเครื่องแล้ว');
  }catch(e){status(e.message);}
};
const boot=async()=>{
  try{
    demo=newProject('Training dummy');demo.parts=characterParts(demo);
    [loaded,demoSurfaces,boltImage]=await Promise.all([preflight(project),preflight(demo),fetchImage(ART.bolt)]);
    ready=true;syncAll();status(messages.animate);renderSoon();
    requestAnimationFrame(animate);
  }catch(e){status('เปิด Studio ไม่ได้ · '+e.message);}
};
boot();
$('mergeMesh').onclick=async()=>{
  const top=currentPart(), index=project.parts.indexOf(top), below=project.parts[index-1];
  if(!top||!below||!top.visible||!below.visible||top.slot||below.slot){
    status('เลือก PNG สองชั้นที่แสดงอยู่และไม่ได้ผูกกับ Slot');return;
  }
  if(project.parts.length>=72){status('เก็บได้สูงสุด 72 ชิ้น');return;}
  const sides=[below,top], images=sides.map(spriteInfo);
  if(images.some(x=>!x))return;
  const corners=sides.flatMap((part,i)=>{
    const s=images[i];
    return [[0,0],[s.w,0],[0,s.h],[s.w,s.h]].map(([u,v])=>{
      const [x,y]=turn(u*part.scale,v*part.scale,part.a*D2R);return [part.x+x,part.y+y];
    });
  });
  const x=Math.floor(Math.min(...corners.map(p=>p[0])))-1,y=Math.floor(Math.min(...corners.map(p=>p[1])))-1;
  const w=Math.ceil(Math.max(...corners.map(p=>p[0])))-x+1,h=Math.ceil(Math.max(...corners.map(p=>p[1])))-y+1;
  if(Math.max(w,h)>900){status('ชิ้นส่วนรวมใหญ่กว่า 900 px');return;}
  const layers=sides.map((part,i)=>{
    const c=canvas(w,h), ctx=c.getContext('2d');
    ctx.translate(part.x-x,part.y-y);ctx.rotate(part.a*D2R);ctx.scale(part.scale,part.scale);
    ctx.drawImage(images[i].image,0,0);return c;
  });
  const merged=composeJoint(...layers), id=nextId('part',project.parts.map(p=>p.id));
  const part={...copy(partDefaults),id,name:'เมชรวม · '+top.name.slice(0,86),src:merged.toDataURL(),x,y,bone:top.bone,bind:'auto'};
  top.visible=false;below.visible=false;project.parts.splice(index+1,0,part);
  selectPart(id);modified();await refreshSurfaces();status('รวมเมชแล้ว เปิดชั้นเดิมกลับได้จากตัวเลือกแสดงชิ้น');
};
