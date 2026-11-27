'use strict';
const pngData=s=>typeof s==='string'&&/^data:image\/png;base64,[A-Za-z0-9+/=]+$/.test(s);
const finite=(x,min,max)=>typeof x==='number'&&Number.isFinite(x)&&x>=min&&x<=max;
const object=x=>x&&typeof x==='object'&&!Array.isArray(x);
const fail=msg=>{throw Error(msg);};
function validateClip(c,id='clip'){
  if(!object(c)||typeof c.name!=='string'||c.name.length>70||!finite(c.duration,.1,12)||typeof c.loop!=='boolean'||
     !Array.isArray(c.keys)||c.keys.length>300|| (c.event!==undefined&&!finite(c.event,0,c.duration)))fail('ข้อมูลคลิปไม่ถูกต้อง '+id);
  let last=-1;
  for(const k of c.keys){
    if(!object(k)||!finite(k.t,0,c.duration)||k.t<=last||!object(k.bones)||!object(k.slots)||Object.keys(k.bones).length>70||
      !['smooth','linear','hold'].includes(k.ease))fail('Keyframe ไม่ถูกต้อง');
    last=k.t;
    for(const [b,v] of Object.entries(k.bones)){
      if(!safeId(b)||!object(v)||!finite(v.x,-2000,2000)||!finite(v.y,-2000,2000)||!finite(v.a,-10000,10000))fail('ข้อมูลท่ากระดูกไม่ถูกต้อง');
    }
    for(const [s,v] of Object.entries(k.slots))if(!safeId(s)||!safeId(v))fail('ค่า Slot ไม่ถูกต้อง');
  }
  return c;
}
function validateProject(p){
  if(!object(p)||p.version!==5||typeof p.name!=='string'||p.name.length>70||!Array.isArray(p.bones)||
    !p.bones.length||p.bones.length>70||!Array.isArray(p.parts)||p.parts.length>72||!object(p.clips)||
    !Object.keys(p.clips).length||Object.keys(p.clips).length>36||!object(p.slots)||!object(p.springs))fail('ไฟล์โปรเจกต์ไม่ถูกต้อง');
  const boneIds=new Set();
  for(const b of p.bones){
    if(!object(b)||!safeId(b.id)||boneIds.has(b.id)||!(b.parent===null||safeId(b.parent))||!finite(b.x,-2000,2000)||!finite(b.y,-2000,2000)||
      !finite(b.a,-20,20)||!/^#[a-f\d]{6}$/i.test(b.color))fail('กระดูกไม่ถูกต้อง');
    boneIds.add(b.id);
  }
  const bones=Object.fromEntries(p.bones.map(b=>[b.id,b]));
  for(const b of p.bones){
    const seen=new Set([b.id]);let parent=b.parent;
    while(parent!==null){if(!boneIds.has(parent)||seen.has(parent))fail('โครงกระดูกวนซ้ำหรือขาดกระดูกแม่');seen.add(parent);parent=bones[parent].parent;}
  }
  const partIds=new Set();
  for(const p2 of p.parts){
    if(!object(p2)||!safeId(p2.id)||partIds.has(p2.id)||typeof p2.name!=='string'||p2.name.length>100||!boneIds.has(p2.bone)||
      !(p2.src===''||pngData(p2.src))||!['auto','rigid','zeus'].includes(p2.bind)||!finite(p2.step,5,40)||
      !finite(p2.x,-2000,2000)||!finite(p2.y,-2000,2000)||!finite(p2.a,-10000,10000)||!finite(p2.scale,.02,6)||
      !object(p2.paint)||!object(p2.variants)||!(p2.slot===''||safeId(p2.slot))||typeof p2.visible!=='boolean'||typeof p2.seam!=='boolean')fail('ชิ้นส่วนไม่ถูกต้อง');
    partIds.add(p2.id);
    for(const [id,values] of Object.entries(p2.paint)){
      if(!Number.isInteger(+id)||+id<0||+id>35000||!object(values)||!Object.keys(values).length||Object.keys(values).length>4)fail('Weight ไม่ถูกต้อง');
      let sum=0;
      for(const [id2,v] of Object.entries(values)){
        if(!boneIds.has(id2)||!finite(v,0,1))fail('Weight มีกระดูกที่ไม่อยู่ใน Rig');
        sum+=v;
      }
      if(Math.abs(sum-1)>.002)fail('ผลรวม Weight ต้องเท่ากับ 1');
    }
    for(const [id,a] of Object.entries(p2.variants))if(!safeId(id)||!pngData(a))fail('ภาพสลับ Slot ไม่ถูกต้อง');
  }
  for(const [id,v] of Object.entries(p.springs)){
    if(!boneIds.has(id)||!object(v)||!finite(v.stiffness,20,190)||!finite(v.damping,2,28)||!finite(v.amount,0,2))fail('Spring ไม่ถูกต้อง');
  }
  for(const [id,v] of Object.entries(p.slots))if(!safeId(id)||!safeId(v))fail('ค่า Slot ไม่ถูกต้อง');
  for(const [id,c] of Object.entries(p.clips)){if(!safeId(id))fail('ชื่อคลิปไม่ถูกต้อง');validateClip(c,id);}
  return p;
}
function newProject(name='New character'){
  return {version:5,name,bones:makeRig(),parts:[],slots:{hand:'closed',face:'neutral',weapon:'none'},springs:{},clips:copy(clips)};
}
function convertPrevious(d){
  if(d.version!==4)return d;
  if(Array.isArray(d.keys)&&d.pose){
    const p=zeusProject(), duration=1.45;
    const frames=d.keys.length?d.keys:[{...d.pose,t:0}];
    const converted=new Map();
    for(const v of frames){
      if(![v.t,v.upper,v.elbow,v.lean,v.squash].every(Number.isFinite)||v.t<0||v.t>duration)fail('ข้อมูล V0.4 ไม่ถูกต้อง');
      converted.set(v.t,makeKey(v.t,{upperL:v.upper,lowerL:v.elbow,chest:v.lean*.27,head:-v.lean*.22},{hips:[v.lean*.3,v.squash*65]},
        {hand:v.hand==='palm'?'open':'grip',weapon:v.bolt?'bolt':'none'}));
    }
    p.clips.imported={name:'คลิปนำเข้า V0.4',duration,loop:true,keys:[...converted.values()].sort((a,b)=>a.t-b.t)};
    return p;
  }
  if(object(d.parts)){
    const p=newProject('Legacy 0.4.1');p.bones=[];p.clips={};
    if(!Object.keys(d.parts).every(safeId))fail('ชื่อชิ้นส่วนรุ่นก่อนผิดรูปแบบ');
    const role={body:'chest',head:'head',arm_l:'upperL',arm_r:'upperR',arm_l_lower:'lowerL',arm_r_lower:'lowerR',leg_l:'thighL',leg_r:'thighR',leg_l_lower:'shinL',
      leg_r_lower:'shinR',ponytail:'hair',cape:'cloth',weapon:'handL'};
    const idOf=id=>role[id]||id;
    for(const [key,v] of Object.entries(d.parts)){
      const id=idOf(key), parent=v.parent==='root'?null:idOf(v.parent);
      p.bones.push({id,parent,x:v.x+(parent?0:265),y:v.y+(parent?0:225),a:v.angle*D2R,color:'#71d9c0'});
    }
    for(const bone of p.bones){
      let b=bone;const seen=new Set();
      while(b){
        if(seen.has(b.id))fail('โครงกระดูกจากโปรเจกต์เก่าวนซ้ำ');
        seen.add(b.id);const parent=b.parent;b=p.bones.find(x=>x.id===parent);
        if(parent&&!b)fail('โครงกระดูกจากโปรเจกต์เก่าขาดกระดูกแม่');
      }
    }
    const rest=fk(p.bones);
    p.clips.imported={name:'คลิปนำเข้า V0.4.1',duration:clamp(d.duration||1,.1,12),loop:true,keys:(d.frames||[]).map(f=>{
      const k=makeKey(f.time);
      for(const [key,o] of Object.entries(f.pose)){
        if(!d.parts[key])continue;
        const v=d.parts[key];
        k.bones[idOf(key)]={x:o.x-v.x,y:o.y-v.y,a:o.angle-v.angle};
      }
      return k;
    }).sort((a,b)=>a.t-b.t)};
    p.parts=Object.entries(d.parts).filter(([,v])=>pngData(v.src)).map(([key,v])=>({
      ...copy(partDefaults),id:key,name:key,src:v.src,bone:idOf(key),scale:v.scale,a:rest[idOf(key)].a/D2R,
      x:rest[idOf(key)].x,y:rest[idOf(key)].y,legacyOffset:[v.ox,v.oy],legacyLayer:v.z
    })).sort((a,b)=>a.legacyLayer-b.legacyLayer);
    return p;
  }
  return d;
}
async function completeLegacy(p){
  for(const part of p.parts){
    if(!part.legacyOffset)continue;
    const im=await fetchImage(part.src);
    const [x,y]=turn(part.legacyOffset[0]-im.width*part.scale/2,part.legacyOffset[1]-im.height*part.scale/2,part.a*D2R);
    part.x+=x;part.y+=y;
    delete part.legacyOffset;delete part.legacyLayer;
  }
  return p;
}
function characterParts(project){
  const rest=fk(project.bones), outline='#25384e', high='#94adbd', mid='#617e99', dark='#435b77', gold='#f2b96d';
  function piece(id,left,top,w,h,draw){
    const c=canvas(w,h),ctx=c.getContext('2d');
    ctx.translate(-left,-top);ctx.strokeStyle=outline;ctx.lineWidth=4;ctx.lineJoin='round';ctx.lineCap='round';
    draw(ctx);
    return {...copy(partDefaults),id:'demo_'+id,name:names[id]||id,src:c.toDataURL(),bone:id,x:left,y:top};
  }
  function shape(c,pts,fill,stroke=true){
    c.beginPath();c.moveTo(...pts[0]);for(const p of pts.slice(1))c.lineTo(...p);c.closePath();
    c.fillStyle=fill;c.fill();if(stroke)c.stroke();
  }
  function capsule(c,x,y,ex,ey,r,fill,band){
    const a=angle(ex-x,ey-y), d=Math.hypot(ex-x,ey-y);
    c.save();c.translate(x,y);c.rotate(a);
    c.beginPath();c.moveTo(0,-r);c.lineTo(d,-r);c.arc(d,0,r,-Math.PI/2,Math.PI/2);
    c.lineTo(0,r);c.arc(0,0,r,Math.PI/2,Math.PI*1.5);c.closePath();c.fillStyle=fill;c.fill();c.stroke();
    c.fillStyle=band;c.fillRect(0,-r+4,Math.max(7,d)*.77,3);c.restore();
  }
  function link(id,endId,r,fill=mid,band=high){
    const {x,y}=rest[id], to=rest[endId];
    const x0=x+(to.x-x)*.05,y0=y+(to.y-y)*.05;
    const x1=x+(to.x-x)*.88,y1=y+(to.y-y)*.88,e=r+4;
    const left=Math.min(x0,x1)-e,top=Math.min(y0,y1)-e;
    return piece(id,left,top,Math.ceil(Math.abs(x0-x1)+2*e),Math.ceil(Math.abs(y0-y1)+2*e),ctx=>capsule(ctx,x0,y0,x1,y1,r,fill,band));
  }
  const hand=(id,dir)=>{const {x,y}=rest[id];return piece(id,x-27,y-16,54,46,c=>capsule(c,x,y,x+dir*10,y+10,11,high,'#bad0d7'));};
  const boot=(id,dir)=>{const {x,y}=rest[id];return piece(id,x-37,y-20,74,49,c=>{
    shape(c,[[x-dir*11,y-11],[x+dir*10,y-11],[x+dir*14,y+7],[x+dir*23,y+13],[x+dir*23,y+24],[x-dir*16,y+24],[x-dir*16,y+11]],dark);
    shape(c,[[x-dir*9,y-3],[x+dir*9,y-3],[x+dir*13,y+11],[x-dir*13,y+11]],mid,false);
    c.fillStyle=high;c.fillRect(Math.min(x+dir*13,x+dir*20),y+16,7,3);
  });};
  return [
    link('upperR','lowerR',13),link('lowerR','handR',12),hand('handR',1),
    link('thighL','shinL',15,dark),link('thighR','shinR',15,dark),link('shinL','footL',12),link('shinR','footR',12),
    boot('footL',-1),boot('footR',1),
    piece('chest',216,211,106,117,c=>{
      shape(c,[[253,219],[278,218],[304,235],[310,270],[294,300],[273,315],[260,315],[237,298],[224,261],[230,239]],mid);
      shape(c,[[235,245],[265,230],[299,244],[292,268],[269,288],[240,273]],high);
      shape(c,[[266,246],[275,255],[266,268],[257,255]],gold);
      shape(c,[[245,294],[288,294],[286,306],[247,306]],dark);
    }),
    piece('cloth',207,293,117,72,c=>{
      shape(c,[[231,301],[299,301],[315,348],[298,360],[263,351],[230,360],[217,347]],dark);
      shape(c,[[254,305],[280,305],[280,347],[268,353],[253,345]],'#7086aa');
      shape(c,[[266,314],[273,322],[266,330],[259,322]],gold);
    }),
    link('upperL','lowerL',14),link('lowerL','handL',12),hand('handL',-1),
    piece('head',194,80,143,151,c=>{
      shape(c,[[209,123],[231,103],[269,91],[300,104],[323,127],[329,170],[321,200],[297,219],[232,219],[210,198],[201,166]],mid);
      shape(c,[[231,110],[269,99],[301,113],[309,130],[283,128],[266,138],[238,127],[216,139]],high,false);
      shape(c,[[212,149],[242,141],[271,154],[302,140],[319,150],[316,175],[271,186],[220,174]],outline);
      shape(c,[[225,153],[252,152],[261,160],[252,165],[227,163]],'#cce4e9',false);
      shape(c,[[287,154],[311,149],[309,161],[287,165],[281,161]],'#cce4e9',false);
      shape(c,[[228,183],[268,194],[305,181],[302,198],[287,210],[243,208],[231,200]],dark,false);
      shape(c,[[262,100],[269,98],[275,100],[276,139],[268,147],[260,139]],gold);
    })
  ];
}
