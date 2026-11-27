'use strict';
function canvas(w=W,h=H){
  const c=document.createElement('canvas');c.width=w;c.height=h;return c;
}
function readImage(src){
  return new Promise((resolve,reject)=>{
    const im=new Image();
    im.onload=()=>resolve(im);
    im.onerror=()=>reject(Error('เปิดภาพ PNG ไม่ได้'));
    im.src=src;
  });
}
const imageCache=new Map(), surfaceCache=new Map();
async function fetchImage(src){
  if(!imageCache.has(src)){
    const task=readImage(src).catch(e=>{imageCache.delete(src);throw e;});
    imageCache.set(src,task);
  }
  return imageCache.get(src);
}
function texture(c){
  const context=c.getContext('2d'), {width:w,height:h}=c;
  return {w,h,pixels:context.getImageData(0,0,w,h).data};
}
function meshFor(tex,step){
  const {w,h,pixels}=tex;
  const cols=Math.ceil(w/step), rows=Math.ceil(h/step), stride=cols+1, points=[], tris=[];
  const X=Array.from({length:stride},(_,i)=>i*w/cols), Y=Array.from({length:rows+1},(_,j)=>j*h/rows);
  for(const y of Y)for(const x of X) points.push({x,y});
  for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){
    let used=false;
    for(let y=Math.max(0,Math.floor(Y[j])-1);y<Math.min(h,Math.ceil(Y[j+1])+1)&&!used;y++){
      for(let x=Math.max(0,Math.floor(X[i])-1);x<Math.min(w,Math.ceil(X[i+1])+1);x++){
        if(pixels[(y*w+x)*4+3]) {used=true;break;}
      }
    }
    if(used){
      const p=j*stride+i;
      tris.push(p,p+1,p+stride,p+1,p+stride+1,p+stride);
    }
  }
  return {points,tris};
}
async function makeSurface(src,step){
  const key=src+'#'+step;
  if(!surfaceCache.has(key)){
    const task=(async()=>{
      const im=await fetchImage(src), c=canvas(im.width,im.height);
      c.getContext('2d').drawImage(im,0,0);
      const tex=texture(c);
      return {...tex,...meshFor(tex,step),image:im};
    })().catch(e=>{surfaceCache.delete(key);throw e;});
    surfaceCache.set(key,task);
  }
  return surfaceCache.get(key);
}
function transformPoint(b,r,x,y){
  const a=b.a-r.a, co=Math.cos(a), si=Math.sin(a), dx=x-r.x, dy=y-r.y;
  return [b.x+co*dx-si*dy,b.y+si*dx+co*dy];
}
function vertexWeights(part,index,x,y,world){
  const custom=part.paint?.[index];
  if(custom) return custom;
  if(part.bind==='zeus') return zeusWeights(x,y);
  if(part.bind==='auto'){
    const influences={};
    for(const id of Object.keys(world)){
      if(id==='root')continue;
      const d2=(world[id].x-x)**2+(world[id].y-y)**2;
      influences[id]=1/((d2+225)**2);
    }
    const result=normalizeWeights(influences);
    if(Object.keys(result).length)return result;
  }
  return {[part.bone]:1};
}
function signed(position,a,b,c){
  return (position[b*2]-position[a*2])*(position[c*2+1]-position[a*2+1])-
    (position[b*2+1]-position[a*2+1])*(position[c*2]-position[a*2]);
}
function deform(part,surface,world,rest){
  const out=new Float32Array(surface.points.length*2);
  const cof={};
  for(const [id,b] of Object.entries(world)){
    const r=rest[id], d=b.a-r.a, co=Math.cos(d),si=Math.sin(d);
    cof[id]=[co,si,b.x-r.x*co+r.y*si,b.y-r.x*si-r.y*co];
  }
  const weights=surface.weights;
  const rotation=part.a*D2R, ca=Math.cos(rotation),sa=Math.sin(rotation);
  for(let i=0;i<surface.points.length;i++){
    const p=surface.points[i], sx=p.x*part.scale,sy=p.y*part.scale;
    const x=part.x+sx*ca-sy*sa, y=part.y+sx*sa+sy*ca;
    const set=weights?.[i]||vertexWeights(part,i,x,y,rest);
    for(const [id,v] of Object.entries(set)){
      const [co,si,dx,dy]=cof[id]||cof[part.bone]||[1,0,0,0];
      out[i*2]+=(co*x-si*y+dx)*v;
      out[i*2+1]+=(si*x+co*y+dy)*v;
    }
  }
  const tris=surface.tris;
  let folded=0;
  if(part.seam){
    for(let k=0;k<14;k++){
      let changes=0;
      for(let i=0;i<tris.length;i+=3){
        const a=tris[i], b=tris[i+1], c=tris[i+2], area=signed(out,a,b,c);
        if(area>.8)continue;
        const ax=out[b*2+1]-out[c*2+1],ay=out[c*2]-out[b*2],bx=out[c*2+1]-out[a*2+1],by=out[a*2]-out[c*2];
        const cx=-ax-bx,cy=-ay-by,den=ax*ax+ay*ay+bx*bx+by*by+cx*cx+cy*cy;
        if(den<.00001)continue;
        const f=(.9-area)/den*.9;
        out[2*a]+=ax*f;out[2*a+1]+=ay*f;out[2*b]+=bx*f;out[2*b+1]+=by*f;out[2*c]+=cx*f;out[2*c+1]+=cy*f;
        changes++;
      }
      if(!changes)break;
    }
  }
  for(let i=0;i<tris.length;i+=3)if(signed(out,tris[i],tris[i+1],tris[i+2])<=0)folded++;
  return {out,folded};
}
function cpuPainter(){
  const layer=canvas(), ctx=layer.getContext('2d'), rgba=ctx.createImageData(W,H);
  function draw(context,part,s,verts){
    const {pixels,points,tris,w,h}=s, dst=rgba.data;
    dst.fill(0);
    for(let i=0;i<tris.length;i+=3){
      const ai=tris[i],bi=tris[i+1],ci=tris[i+2];
      const ax=verts[ai*2],ay=verts[ai*2+1], bx=verts[bi*2],by=verts[bi*2+1], cx=verts[ci*2],cy=verts[ci*2+1];
      const dx=bx-ax,dy=by-ay,ex=cx-ax,ey=cy-ay,det=dx*ey-dy*ex;
      if(det<.0001)continue;
      const a=points[ai],b=points[bi],c=points[ci];
      const x0=Math.max(0,Math.floor(Math.min(ax,bx,cx))),x1=Math.min(W-1,Math.ceil(Math.max(ax,bx,cx)));
      const y0=Math.max(0,Math.floor(Math.min(ay,by,cy))),y1=Math.min(H-1,Math.ceil(Math.max(ay,by,cy)));
      for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){
        const px=x+.5-ax, py=y+.5-ay, s1=(px*ey-py*ex)/det, s2=(dx*py-dy*px)/det;
        if(s1<-.00001||s2<-.00001||s1+s2>1.00001)continue;
        const u=clamp(a.x+s1*(b.x-a.x)+s2*(c.x-a.x)-.5,0,w-1);
        const v=clamp(a.y+s1*(b.y-a.y)+s2*(c.y-a.y)-.5,0,h-1);
        const U=u|0,V=v|0,fu=u-U,fv=v-V,k=(V*w+U)*4;
        const k1=k+(U+1<w?4:0),k2=k+(V+1<h?w*4:0),k3=k2+k1-k;
        const p0=(1-fu)*(1-fv)*pixels[k+3],p1=fu*(1-fv)*pixels[k1+3],p2=(1-fu)*fv*pixels[k2+3],p3=fu*fv*pixels[k3+3];
        const a1=p0+p1+p2+p3;
        if(a1<.9)continue;
        const j=(y*W+x)*4;
        for(let l=0;l<3;l++)dst[j+l]=(pixels[k+l]*p0+pixels[k1+l]*p1+pixels[k2+l]*p2+pixels[k3+l]*p3)/a1;
        dst[j+3]=a1;
      }
    }
    ctx.putImageData(rgba,0,0);
    context.drawImage(layer,0,0);
  }
  return draw;
}
function gpuPainter(){
  const surface=canvas();
  const gl=surface.getContext('webgl',{alpha:true,antialias:false,premultipliedAlpha:true,preserveDrawingBuffer:true});
  if(!gl)throw Error('WebGL unavailable');
  function shader(type,source){
    const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);
    if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));
    return s;
  }
  const p=gl.createProgram();
  gl.attachShader(p,shader(gl.VERTEX_SHADER,`attribute vec2 position;attribute vec2 uv;varying vec2 tex;
    void main(){gl_Position=vec4(position.x/530.0*2.0-1.0,1.0-position.y/490.0*2.0,0.0,1.0);tex=uv;}`));
  gl.attachShader(p,shader(gl.FRAGMENT_SHADER,`precision mediump float;uniform sampler2D art;varying vec2 tex;
    void main(){gl_FragColor=texture2D(art,tex);}`));
  gl.linkProgram(p);
  if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(p));
  gl.useProgram(p);gl.viewport(0,0,W,H);gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL,true);
  gl.frontFace(gl.CW);gl.enable(gl.CULL_FACE);
  gl.enable(gl.BLEND);gl.blendFunc(gl.ONE,gl.ONE_MINUS_SRC_ALPHA);
  const position=gl.getAttribLocation(p,'position'), uv=gl.getAttribLocation(p,'uv'), vb=gl.createBuffer(),cache=new WeakMap();
  gl.enableVertexAttribArray(position);gl.enableVertexAttribArray(uv);
  function geometry(s){
    if(cache.has(s.image))return cache.get(s.image);
    const tex=gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D,tex);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,s.image);
    for(const [name,v] of [[gl.TEXTURE_MIN_FILTER,gl.LINEAR],[gl.TEXTURE_MAG_FILTER,gl.LINEAR],
      [gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE],[gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE]])gl.texParameteri(gl.TEXTURE_2D,name,v);
    const buffers=new Map(), g={tex,buffers};cache.set(s.image,g);
    return g;
  }
  function draw(c,part,s,vertices){
    if(gl.isContextLost()||s.points.length>65535)return false;
    const g=geometry(s);
    if(!g.buffers.has(part.step)){
      const e=gl.createBuffer(),uvBuffer=gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER,uvBuffer);
      gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(s.points.flatMap(p=>[p.x/s.w,p.y/s.h])),gl.STATIC_DRAW);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,e);
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,new Uint16Array(s.tris),gl.STATIC_DRAW);
      g.buffers.set(part.step,[e,uvBuffer]);
    }
    const [triangles,coords]=g.buffers.get(part.step);
    gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);
    gl.bindTexture(gl.TEXTURE_2D,g.tex);
    gl.bindBuffer(gl.ARRAY_BUFFER,coords);gl.vertexAttribPointer(uv,2,gl.FLOAT,false,0,0);
    gl.bindBuffer(gl.ARRAY_BUFFER,vb);gl.bufferData(gl.ARRAY_BUFFER,vertices,gl.STREAM_DRAW);
    gl.vertexAttribPointer(position,2,gl.FLOAT,false,0,0);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,triangles);
    gl.drawElements(gl.TRIANGLES,s.tris.length,gl.UNSIGNED_SHORT,0);
    c.drawImage(surface,0,0);return true;
  }
  return draw;
}
let renderBackend='CPU';
function createPainter(){
  const cpu=cpuPainter();
  let gpu=null;
  if(new URLSearchParams(location.search).get('renderer')!=='cpu'){
    try{gpu=gpuPainter();renderBackend='WebGL';}catch(e){gpu=null;}
  }
  return (c,p,s,v)=>{
    if(gpu&&gpu(c,p,s,v))return;
    renderBackend='CPU';cpu(c,p,s,v);
  };
}
function drawRigid(context,part,s,world,rest){
  const b=world[part.bone], r=rest[part.bone], [x,y]=transformPoint(b,r,part.x,part.y);
  context.save();context.translate(x,y);context.rotate(b.a-r.a+part.a*D2R);context.scale(part.scale,part.scale);
  context.drawImage(s.image,0,0);context.restore();
}
async function sourceFromFile(file, max=900){
  if(file.size>18*1024*1024)throw Error('PNG ใหญ่เกิน 18 MB');
  const data=new Uint8Array(await file.slice(0,8).arrayBuffer());
  if(data.length!==8||![137,80,78,71,13,10,26,10].every((n,i)=>data[i]===n))throw Error('เลือกไฟล์ PNG');
  const url=URL.createObjectURL(file);
  try{
    const im=await readImage(url), f=Math.min(1,max/Math.max(im.width,im.height)), c=canvas(Math.round(im.width*f),Math.round(im.height*f));
    c.getContext('2d').drawImage(im,0,0,c.width,c.height);
    return c;
  }finally{URL.revokeObjectURL(url);}
}
function splitImage(c,method='alpha'){
  const ctx=c.getContext('2d'), {w,h,pixels}=texture(c);
  if(method==='green'){
    for(let i=0;i<pixels.length;i+=4){
      const [r,g,b]=pixels.subarray(i,i+3), d=g-Math.max(r,b);
      if(g>85&&d>25)pixels[i+3]*=1-smooth((d-25)/48);
    }
  }
  const groups=alphaComponents(pixels,w,h);
  if(groups.length>48)throw Error('พบชิ้นส่วนมากกว่า 48 ชิ้น ลองแบ่งชีทเป็นภาพย่อย');
  return groups.map(g=>{
    const can=canvas(g.w,g.h), x=can.getContext('2d'), block=x.createImageData(g.w,g.h);
    for(const index of g.pixels){
      const at=(((index/w|0)-g.y)*g.w+(index%w-g.x))*4;
      block.data.set(pixels.subarray(index*4,index*4+4),at);
    }
    x.putImageData(block,0,0);
    return {src:can.toDataURL('image/png'),x:g.x,y:g.y,w:g.w,h:g.h};
  });
}
function composeJoint(bottom,top){
  const lower=bottom.getContext('2d'),upper=top.getContext('2d'),w=bottom.width,h=bottom.height;
  const base=lower.getImageData(0,0,w,h).data, edge=upper.getImageData(0,0,w,h), out=edge.data;
  const stable=new Uint8Array(w*h);
  for(let j=0;j<stable.length;j++)stable[j]=out[j*4+3];
  // Erase internal dark ink only where the lower layer already covers the silhouette.
  for(let y=4;y<h-4;y++)for(let x=4;x<w-4;x++){
    const p=y*w+x,i=p*4;
    if(base[i+3]<250||stable[p]<8||out[i]+out[i+1]+out[i+2]>235)continue;
    let clip=false;
    for(let d=1;d<=4;d++){
      if(Math.min(stable[p-d],stable[p+d],stable[p-d*w],stable[p+d*w])<75){clip=true;break;}
    }
    if(clip)out[i+3]=0;
  }
  upper.putImageData(edge,0,0);
  lower.drawImage(top,0,0);
  return bottom;
}
