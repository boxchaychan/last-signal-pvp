'use strict';
const drawMesh=createPainter();
const partDefaults={x:0,y:0,a:0,scale:1,bone:'chest',bind:'rigid',step:11,seam:true,paint:{},variants:{},slot:'',visible:true};
function zeusProject(){
  return {version:5,name:'Zeus',bones:makeRig(),parts:[
    {...copy(partDefaults),id:'zeus',name:'ซุส · ภาพต่อเนื่อง',src:ART.source,x:105,y:27,bind:'zeus',step:9},
    {...copy(partDefaults),id:'weapon',name:'อาวุธ',src:'',bone:'handL',slot:'weapon',x:149,y:241,scale:.25,variants:{bolt:ART.bolt,sword:ART.sword}}
  ],slots:{hand:'closed',face:'neutral',weapon:'bolt'},springs:{hair:{stiffness:105,damping:13,amount:.65},cloth:{stiffness:82,damping:12,amount:.85}},clips:copy(clips)};
}
const zeusVariantCache=new Map();
async function makeZeusVariants(step){
  const source=await fetchImage(ART.source), result={};
  for(const hand of ['closed','grip','open'])for(const face of ['neutral','blink','focused','shout']){
    if(hand==='closed'&&face==='neutral')continue;
    const c=canvas(source.width,source.height),ctx=c.getContext('2d');
    ctx.drawImage(source,0,0);
    if(hand!=='closed'){
      ctx.save();
      ctx.beginPath();ctx.moveTo(0,250);ctx.lineTo(39,248);ctx.quadraticCurveTo(61,258,69,274);ctx.lineTo(69,315);ctx.lineTo(0,315);
      ctx.clip();ctx.clearRect(0,0,c.width,c.height);ctx.restore();
      ctx.globalCompositeOperation='destination-over';
      const open=hand==='open';
      ctx.drawImage(await fetchImage(ART['hand-'+hand]),open?19:25,open?233:241);
      ctx.globalCompositeOperation='source-over';
    }
    if(face!=='neutral')ctx.drawImage(await fetchImage(ART['face-'+face]),112,120);
    const tex=texture(c);
    result[hand+':'+face]={...tex,...meshFor(tex,step),image:c};
  }
  return result;
}
async function preflight(project){
  const parts=new Map(), rest=fk(project.bones);
  for(const part of project.parts){
    const variants=Object.entries(part.variants||{});
    const result={};
    for(const [key,value] of [['base',part.src],...variants]){
      if(value)result[key]={...(await makeSurface(value,part.step))};
    }
    if(part.bind==='zeus'&&part.src===ART.source){
      if(!zeusVariantCache.has(part.step))zeusVariantCache.set(part.step,makeZeusVariants(part.step));
      for(const [id,surface] of Object.entries(await zeusVariantCache.get(part.step)))result[id]={...surface};
    }
    if(part.bind!=='rigid') for(const s of Object.values(result)){
      s.weights=s.points.map((p,i)=>{
        const [x,y]=turn(p.x*part.scale,p.y*part.scale,part.a*D2R);
        return vertexWeights(part,i,part.x+x,part.y+y,rest);
      });
    }
    parts.set(part.id,result);
  }
  return parts;
}
function chooseSurface(part,surfaces,slots){
  if(part.bind==='zeus'&&part.src===ART.source){
    const key=slots.hand+':'+slots.face;
    return surfaces[key]||surfaces.base;
  }
  if(part.slot){
    const key=slots[part.slot];
    if(key==='none')return null;
    return surfaces[key]||surfaces.base;
  }
  return surfaces.base;
}
function drawActor(context,project,parts,clip,t,poseOverride=null,overlay=null){
  const pose=evaluate(project,clip,t,poseOverride), rest=fk(project.bones), world=fk(project.bones,pose.bones);
  const slots={...project.slots,...pose.slots};
  let folded=0, triangles=0;
  for(const part of project.parts){
    if(!part.visible)continue;
    const s=chooseSurface(part,parts.get(part.id)||{},slots);
    if(!s)continue;
    if(part.bind==='rigid'){
      if(part.id==='weapon'&&part.variants.bolt===ART.bolt&&slots.weapon==='bolt'&&world.handL){
        const wr=world.handL;
        const loc=transformPoint(wr,rest.handL,147,297);
        context.save();context.translate(...loc);context.rotate(wr.a*.82-.63);
        context.drawImage(s.image,-22,-39,44,78);context.restore();
      }else drawRigid(context,part,s,world,rest);
      continue;
    }
    const d=deform(part,s,world,rest);
    drawMesh(context,part,s,d.out);folded+=d.folded;triangles+=s.tris.length/3;
    if(overlay?.mesh&&overlay.part===part.id){
      context.save();context.strokeStyle='#48eed6a0';context.lineWidth=.6;
      context.beginPath();
      for(let i=0;i<s.tris.length;){
        let a=s.tris[i++]*2,b=s.tris[i++]*2,c=s.tris[i++]*2;
        context.moveTo(d.out[a],d.out[a+1]);context.lineTo(d.out[b],d.out[b+1]);context.lineTo(d.out[c],d.out[c+1]);context.closePath();
      }
      context.stroke();
      if(overlay.weight){
        for(let i=0;i<s.points.length;i++){
          const v=(s.weights[i]||{})[overlay.weight]||0;
          if(v<.02)continue;
          context.fillStyle='rgba(255,'+Math.round(210*(1-v))+',80,'+(.2+.8*v)+')';
          context.beginPath();context.arc(d.out[i*2],d.out[i*2+1],1.4+v*2.4,0,7);context.fill();
        }
      }
      context.restore();
    }
  }
  if(overlay?.bones){
    context.save();context.lineWidth=2;
    for(const b of project.bones){
      const p=world[b.parent], w=world[b.id], selected=overlay.bone===b.id;
      context.strokeStyle=b.color;
      context.fillStyle=selected?'#fff6da':b.color;
      if(p){
        context.beginPath();context.moveTo(p.x,p.y);context.lineTo(w.x,w.y);context.stroke();
      }
      context.beginPath();
      context.arc(w.x,w.y,chains.some(chain=>chain[2]===b.id)?6:4,0,7);
      context.fill();
    }
    context.restore();
  }
  return {world,rest,pose,folded,triangles};
}
function mainProjectile(ctx,project,clip,time,image,battle=false){
  const e=clip.event;
  if(typeof e!=='number'||time<e||time>=e+.36||!image) return null;
  const u=(time-e)/.36, world=fk(project.bones,evaluate(project,clip,e).bones), hand=world.handL;
  if(!hand)return null;
  const x=hand.x-10-204*u, y=hand.y-15+Math.sin(Math.PI*u)*-24+(battle?23*u:0);
  ctx.save();
  ctx.strokeStyle='rgba(87,224,255,'+(.8*(1-u))+')';ctx.lineCap='round';
  for(let i=0;i<3;i++){
    ctx.lineWidth=3-i*.6;
    ctx.beginPath();ctx.moveTo(x+10,y+(i-1)*8);ctx.lineTo(x+26,y+(i-1)*10-3);ctx.lineTo(x+41+i*6,y+(i-1)*12);ctx.stroke();
  }
  ctx.translate(x,y);ctx.rotate(-2.1);ctx.drawImage(image,-18,-31,36,62);ctx.restore();
  return {x,y};
}
