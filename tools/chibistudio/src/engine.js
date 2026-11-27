'use strict';
const W = 530, H = 490, D2R = Math.PI / 180;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const mix = (a, b, u) => a + (b-a)*u;
const smooth = u => { u=clamp(u,0,1); return u*u*(3-2*u); };
const turn = (x,y,a) => [x*Math.cos(a)-y*Math.sin(a), x*Math.sin(a)+y*Math.cos(a)];
const angle = (x,y) => Math.atan2(y,x);
const copy = x => JSON.parse(JSON.stringify(x));
const safeId = id => typeof id==='string' && /^[\w-]{1,40}$/.test(id) && !['__proto__','constructor','prototype'].includes(id);
const identity = {x:0,y:0,a:0};
const boneList = [
  ['root',null,265,454,'#fbbe73'], ['hips','root',265,314,'#ffc66f'],
  ['chest','hips',265,271,'#ffc66f'], ['head','chest',265,219,'#f2a7ff'],
  ['hair','head',265,99,'#f2a7ff'], ['cloth','hips',265,311,'#a99cff'],
  ['upperL','chest',226,241,'#5ee5cf'], ['lowerL','upperL',193,264,'#5ee5cf'], ['handL','lowerL',162,290,'#5ee5cf'],
  ['upperR','chest',324,245,'#ff9c9e'], ['lowerR','upperR',356,267,'#ff9c9e'], ['handR','lowerR',382,293,'#ff9c9e'],
  ['thighL','hips',236,360,'#75baff'], ['shinL','thighL',233,393,'#75baff'], ['footL','shinL',227,427,'#75baff'], ['toeL','footL',214,451,'#75baff'],
  ['thighR','hips',293,360,'#ffb275'], ['shinR','thighR',303,393,'#ffb275'], ['footR','shinR',309,427,'#ffb275'], ['toeR','footR',325,451,'#ffb275'],
];
const names = {root:'ฐาน',hips:'สะโพก',chest:'อก',head:'หัว',hair:'ผม',cloth:'ผ้า',upperL:'ต้นแขนซ้าย',lowerL:'ปลายแขนซ้าย',handL:'มือซ้าย',upperR:'ต้นแขนขวา',lowerR:'ปลายแขนขวา',handR:'มือขวา',thighL:'ต้นขาซ้าย',shinL:'หน้าแข้งซ้าย',footL:'เท้าซ้าย',toeL:'ปลายเท้าซ้าย',thighR:'ต้นขาขวา',shinR:'หน้าแข้งขวา',footR:'เท้าขวา',toeR:'ปลายเท้าขวา'};
const chains = [
  ['upperL','lowerL','handL',-1],['upperR','lowerR','handR',1],
  ['thighL','shinL','footL',1],['thighR','shinR','footR',-1],
];
function makeRig(){
  return boneList.map(([id,parent,x,y,color])=>{
    const p=boneList.find(b=>b[0]===parent);
    return {id,parent,x:x-(p?.[2]??0),y:y-(p?.[3]??0),a:0,color};
  });
}
function fk(bones,pose={}){
  const world=Object.create(null), byId=Object.fromEntries(bones.map(b=>[b.id,b]));
  function place(id){
    if(world[id]) return world[id];
    const bone=byId[id], p=bone.parent?place(bone.parent):identity, v=pose[id]||identity;
    const [dx,dy]=turn(bone.x+v.x,bone.y+v.y,p.a);
    return world[id]={x:p.x+dx,y:p.y+dy,a:p.a+bone.a+v.a*D2R};
  }
  for(const b of bones) place(b.id);
  return world;
}
function solveIK(bones,pose,chain,x,y,sign=chain[3]){
  const [top,mid,end]=chain, B=Object.fromEntries(bones.map(b=>[b.id,b]));
  if(!B[top]||B[mid]?.parent!==top||B[end]?.parent!==mid) return;
  const world=fk(bones,pose), a=world[top], p=world[B[top].parent]||identity;
  const m=pose[mid]||identity, e=pose[end]||identity;
  const mx=B[mid].x+m.x, my=B[mid].y+m.y, ex=B[end].x+e.x, ey=B[end].y+e.y;
  const l1=Math.hypot(mx,my), l2=Math.hypot(ex,ey);
  if(Math.min(l1,l2)<.01) return;
  const dx=x-a.x, dy=y-a.y, reach=clamp(Math.hypot(dx,dy),Math.abs(l1-l2)+.001,l1+l2-.001);
  const bend=sign*Math.acos(clamp((reach*reach-l1*l1-l2*l2)/(2*l1*l2),-1,1));
  const heading=angle(dx,dy)-angle(l1+l2*Math.cos(bend),l2*Math.sin(bend));
  const v1=angle(mx,my), v2=angle(ex,ey);
  const norm=a=>((a+540)%360+360)%360-180;
  pose[top]={...(pose[top]||identity),a:norm((heading-v1-p.a-B[top].a)/D2R)};
  pose[mid]={...m,a:norm((bend+v1-v2-B[mid].a)/D2R)};
}
function makeKey(t,angles={}, moves={}, slots={}, contact=null){
  const bones={};
  for(const id of new Set([...Object.keys(angles),...Object.keys(moves)])){
    const [x,y]=moves[id]||[0,0];
    bones[id]={x,y,a:angles[id]||0};
  }
  return {t,bones,slots,contact,ease:'smooth'};
}
const clips = {
  idle:{name:'ยืน',duration:1.8,loop:true,keys:[
    makeKey(0,{}, {}, {weapon:'bolt',hand:'grip'}),makeKey(.48,{chest:1.4,head:-1.1,upperL:3,lowerR:-3},{chest:[0,-2]},{weapon:'bolt',hand:'grip'}),
    makeKey(.86,{chest:-.8,head:1,upperR:2},{chest:[0,1]},{weapon:'bolt',hand:'grip',face:'blink'}),
    makeKey(.95,{chest:-1,head:1.1},{chest:[0,1]},{weapon:'bolt',hand:'grip'}),makeKey(1.8,{}, {}, {weapon:'bolt',hand:'grip'})
  ]},
  walk:{name:'เดิน',duration:.8,loop:true,keys:[
    makeKey(0,{thighL:-12,thighR:10,shinR:-5,footL:8,upperL:9,upperR:-8,chest:-3,head:3},{hips:[-2,1]},{weapon:'none'}),
    makeKey(.2,{thighL:4,thighR:6,shinR:-18,footR:16,upperL:0,upperR:1},{hips:[1,-6]},{weapon:'none'}),
    makeKey(.4,{thighL:10,thighR:-12,shinL:5,footR:8,upperL:-8,upperR:9,chest:3,head:-3},{hips:[2,1]},{weapon:'none'}),
    makeKey(.6,{thighL:6,thighR:4,shinL:18,footL:-16,upperL:1,upperR:0},{hips:[-1,-6]},{weapon:'none'}),
    makeKey(.8,{thighL:-12,thighR:10,shinR:-5,footL:8,upperL:9,upperR:-8,chest:-3,head:3},{hips:[-2,1]},{weapon:'none'})
  ]},
  attack:{name:'ปาสายฟ้า',duration:1.42,loop:true,event:.62,plant:true,keys:[
    makeKey(0,{upperL:11,lowerL:3},{},{weapon:'bolt',hand:'grip'}),
    makeKey(.17,{upperL:22,lowerL:8,upperR:-6,chest:3,head:-3},{hips:[3,2]},{weapon:'bolt',hand:'grip'}),
    makeKey(.44,{upperL:31,lowerL:43,upperR:-15,lowerR:4,chest:5,head:-6},{hips:[6,3],head:[1,-1]},{weapon:'bolt',hand:'grip',face:'focused'}),
    makeKey(.54,{upperL:34,lowerL:49,upperR:-16,lowerR:5,chest:6,head:-7},{hips:[7,3]},{weapon:'bolt',hand:'grip',face:'focused'}),
    makeKey(.62,{upperL:28,lowerL:8,upperR:6,lowerR:-9,chest:-5,head:5},{hips:[-9,6],head:[-3,1]},{hand:'open',weapon:'none',face:'shout'}),
    makeKey(.70,{upperL:12,lowerL:-7,upperR:13,lowerR:-6,chest:-7,head:7},{hips:[-9,5],head:[-4,1]},{hand:'open',weapon:'none',face:'shout'}),
    makeKey(.89,{upperL:4,lowerL:-5,upperR:3,chest:-3,head:2},{hips:[-6,5]},{hand:'open',weapon:'none'}),
    makeKey(1.08,{upperL:10,lowerL:1},{hips:[-1,1]},{weapon:'none'}),
    makeKey(1.24,{upperL:11,lowerL:3},{},{weapon:'bolt',hand:'grip'}),
    makeKey(1.42,{upperL:11,lowerL:3},{},{weapon:'bolt',hand:'grip'})
  ]},
  hit:{name:'โดนโจมตี',duration:.52,loop:false,keys:[
    makeKey(0,{}, {}, {weapon:'none'}),makeKey(.09,{chest:-8,head:9,upperL:-4,upperR:7},{hips:[-9,3]},{face:'blink',weapon:'none'}),
    makeKey(.24,{chest:4,head:-4},{hips:[3,4]},{weapon:'none'}),makeKey(.52,{}, {}, {weapon:'none'})
  ]}
};
function sample(clip,t){
  const keys=clip.keys;
  if(!keys.length) return makeKey(t);
  let i=keys.findIndex(k=>k.t>t+1e-8);
  if(i===0) return {...keys[0],t};
  if(i<0) return {...keys.at(-1),t};
  const a=keys[i-1], b=keys[i], f=clamp((t-a.t)/(b.t-a.t),0,1);
  const u=a.ease==='hold'?0:a.ease==='linear'?f:smooth(f);
  const bones={};
  for(const id of new Set([...Object.keys(a.bones),...Object.keys(b.bones)])){
    const x=a.bones[id]||identity, y=b.bones[id]||identity;
    const delta=((y.a-x.a+180)%360+360)%360-180;
    bones[id]={x:mix(x.x,y.x,u),y:mix(x.y,y.y,u),a:x.a+delta*u};
  }
  return {t,bones,slots:{...a.slots},ease:a.ease,freeFeet:{...a.freeFeet}};
}
function evaluate(project,clip,t,poseOverride){
  const pose=copy(poseOverride||sample(clip,t));
  const rest=fk(project.bones);
  if(pose.noPhysics)return pose;
  if(clip.plant&&!poseOverride){
    // Preserve the ground contact while the hips shift through the cast.
    for(const chain of chains.slice(2)){
      if(pose.freeFeet?.[chain[2]])continue;
      const target=rest[chain[2]];
      if(!target || !rest[chain[0]]) continue;
      const knee=rest[chain[1]], top=rest[chain[0]];
      const cross=(knee.x-top.x)*(target.y-knee.y)-(knee.y-top.y)*(target.x-knee.x);
      solveIK(project.bones,pose.bones,chain,target.x,target.y,Math.sign(cross)||chain[3]);
      const foot=project.bones.find(b=>b.id===chain[2]), world=fk(project.bones,pose.bones);
      if(foot&&world[foot.id]){
        const prev=pose.bones[foot.id]||identity;
        pose.bones[foot.id]={...prev,a:prev.a+(rest[foot.id].a-world[foot.id].a)/D2R};
      }
    }
  }
  for(const [id,key] of Object.entries(project.springs||{})){
    if(!key.amount||!rest[id]) continue;
    const v=pose.bones[id]||identity;
    let pos=0, speed=0;
    const step=1/60, parent=project.bones.find(b=>b.id===id).parent;
    for(let i=72;i>0;i--){
      const at=t-i*step, time=clip.loop?((at%clip.duration)+clip.duration)%clip.duration:clamp(at,0,clip.duration);
      const k=sample(clip,time).bones, root=k.hips||identity, p=k[parent]||identity;
      const drift=clip.loop?Math.sin(time*Math.PI*2/clip.duration+(id==='hair'?.5:1.1))*2.5:0;
      const target=key.amount*(-p.a*1.3-root.x*.8+drift);
      speed+=(key.stiffness*(target-pos)-key.damping*speed)*step;
      pos+=speed*step;
    }
    pose.bones[id]={...v,a:v.a+clamp(pos,-18,18)};
  }
  return pose;
}
function normalizeWeights(input){
  const picks=Object.entries(input).filter(([,v])=>v>.0001).sort((a,b)=>b[1]-a[1]).slice(0,4);
  const sum=picks.reduce((n,[,v])=>n+v,0);
  return Object.fromEntries(picks.map(([k,v])=>[k,v/sum]));
}
function zeusWeights(x,y){
  const w={chest:1};
  function blend(id,u){
    u=clamp(u,0,1);
    if(u<=0) return;
    for(const k of Object.keys(w)) w[k]*=1-u;
    w[id]=(w[id]||0)+u;
  }
  const gate=(a,b,v)=>smooth((v-a)/(b-a));
  blend('hips',gate(276,325,y));
  const side=x<265?'L':'R';
  const exit=side==='L' ? 226+clamp(y-241,0,70)*.18 : 323-clamp(y-245,0,70)*.22;
  const dx=side==='L'?exit-x:x-exit;
  const near=gate(-6,25,dx)*gate(219,238,y)*(1-gate(277,314,y));
  const far=gate(32,58,dx)*gate(224,243,y)*(1-gate(341,361,y));
  // The garment edge and arm are close in the source pose. Use the traced
  // underarm gap to keep the tunic and its ink on the torso during arm swings.
  const garmentLeft=mix(229,211,gate(243,273,y));
  const garmentRight=mix(315,334,gate(238,269,y));
  const clearance=side==='L'?garmentLeft-x:x-garmentRight;
  const arm=Math.max(near,far)*gate(0,19,clearance);
  const shoulder=side==='L'?[226,241]:[324,245];
  const along=(side==='L'?shoulder[0]-x:x-shoulder[0])*.78+(y-shoulder[1])*.63;
  if(arm>.001){
    blend('upper'+side,arm);
    blend('lower'+side,arm*gate(16,47,along));
    blend('hand'+side,arm*gate(70,94,along));
  }
  blend('head',1-gate(217,238,y));
  const hair=(1-gate(72,120,y))*gate(10,30,Math.abs(x-265));
  blend('hair',hair*.72);
  const skirtWidth=mix(48,94,gate(320,354,y));
  blend('cloth',gate(302,325,y)*(1-gate(366,382,y))*(1-gate(skirtWidth,skirtWidth+16,Math.abs(x-265)))*(.68+.32*gate(27,61,Math.abs(x-265))));
  // Trace the curved hem rather than starting thigh weights across the gold trim.
  const outer=Math.abs(x-265);
  const hem=mix(378,365,gate(11,53,outer));
  const isSkinSide=1-gate(49,58,outer);
  const legStart=mix(385,hem,isSkinSide);
  blend('thigh'+side,gate(legStart,legStart+14,y));
  // Keep the shin guard and sole coherent while blending across the real joints.
  blend('shin'+side,gate(389,405,y));
  blend('foot'+side,gate(414,427,y));
  blend('toe'+side,gate(438,454,y)*gate(29,62,outer)*.12);
  return normalizeWeights(w);
}
function alphaComponents(data,w,h){
  const len=w*h, seen=new Uint8Array(len), queue=new Int32Array(len), runs=[];
  for(let start=0;start<len;start++){
    if(seen[start]||data[start*4+3]<8) continue;
    let head=0,tail=1,x0=w,y0=h,x1=0,y1=0;
    queue[0]=start;seen[start]=1;
    while(head<tail){
      const p=queue[head++],x=p%w,y=(p/w)|0;
      x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);
      const xlo=Math.max(x-1,0), xhi=Math.min(x+1,w-1);
      for(let row=Math.max(y-1,0);row<=Math.min(y+1,h-1);row++){
        for(let col=xlo;col<=xhi;col++){
          const n=row*w+col;
          if(!seen[n]&&data[n*4+3]>=8){seen[n]=1;queue[tail++]=n;}
        }
      }
    }
    if(tail>=6) runs.push({x:x0,y:y0,w:x1-x0+1,h:y1-y0+1,count:tail,pixels:queue.slice(0,tail)});
  }
  return runs.sort((a,b)=>b.count-a.count);
}
