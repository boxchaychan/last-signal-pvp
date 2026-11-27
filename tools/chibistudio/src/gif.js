'use strict';
function buildPalette(frames){
  const cube=new Uint32Array(32768), bins=[];
  const cell=(r,g,b)=>r>>3<<10|g>>3<<5|b>>3;
  for(const frame of frames){
    for(let i=0;i<frame.length;i+=12){
      if(frame[i+3]>=128)cube[cell(frame[i],frame[i+1],frame[i+2])]++;
    }
  }
  for(let i=0;i<cube.length;i++)if(cube[i]){
    bins.push({rgb:[((i>>10)&31)*8+4,((i>>5)&31)*8+4,(i&31)*8+4],n:cube[i]});
  }
  function box(items){
    let lo=[255,255,255], hi=[0,0,0], n=0;
    for(const item of items){
      n+=item.n;
      for(let j=0;j<3;j++){lo[j]=Math.min(lo[j],item.rgb[j]);hi[j]=Math.max(hi[j],item.rgb[j]);}
    }
    const delta=hi.map((v,j)=>v-lo[j]), axis=delta.indexOf(Math.max(...delta));
    return {items,axis,n,value:items.length>1?delta[axis]*Math.sqrt(n):0};
  }
  const boxes=bins.length?[box(bins)]:[];
  while(boxes.length<255){
    boxes.sort((a,b)=>b.value-a.value);
    if(!boxes[0]?.value)break;
    const top=boxes.shift(),items=top.items;
    items.sort((a,b)=>a.rgb[top.axis]-b.rgb[top.axis]);
    let n=0,mid=0;
    do{n+=items[mid++].n;}while(mid<items.length-1&&n<top.n/2);
    boxes.push(box(items.slice(0,mid)),box(items.slice(mid)));
  }
  const pal=[[0,0,0],...boxes.map(b=>[0,1,2].map(j=>Math.round(b.items.reduce((n,i)=>n+i.rgb[j]*i.n,0)/b.n)))];
  const count=pal.length, cache=new Uint8Array(32768);
  while(pal.length<256)pal.push([0,0,0]);
  function lookup(r,g,b){
    const index=cell(r,g,b);
    if(cache[index])return cache[index];
    let dist=Infinity, found=1;
    const [R,G,B]=[((index>>10)&31)*8+4,((index>>5)&31)*8+4,(index&31)*8+4];
    for(let i=1;i<count;i++){
      const p=pal[i], d=(R-p[0])**2*.95+(G-p[1])**2*1.3+(B-p[2])**2*.85;
      if(d<dist){dist=d;found=i;}
    }
    cache[index]=found;
    return found;
  }
  return {pal,lookup};
}
function gifLzw(indexed){
  let bits=9,next=258,remainder=0,used=0,dict=new Map(),out=[];
  function emit(code){
    remainder|=code<<used;used+=bits;
    while(used>=8){out.push(remainder&255);remainder>>>=8;used-=8;}
  }
  emit(256);
  let p=indexed[0];
  for(let i=1;i<indexed.length;i++){
    const at=indexed[i], k=p*256+at, v=dict.get(k);
    if(v!==undefined){p=v;continue;}
    emit(p);
    if(next>=(1<<bits) && bits<12)bits++;
    if(next<4096)dict.set(k,next++);
    else{emit(256);dict.clear();bits=9;next=258;}
    p=at;
  }
  emit(p);
  if(next>=(1<<bits)&&bits<12)bits++;
  emit(257);
  if(used)out.push(remainder&255);
  return Uint8Array.from(out);
}
function createGif(frames,w,h,fps,loop){
  const {pal,lookup}=buildPalette(frames), chunks=[];
  const add=(...args)=>chunks.push(Uint8Array.from(args));
  const word=n=>[n&255,n>>8&255], ascii=s=>Array.from(s,c=>c.charCodeAt(0));
  add(...ascii('GIF89a'),...word(w),...word(h),0xf7,0,0);
  add(...pal.flat());
  if(loop)add(0x21,0xff,11,...ascii('NETSCAPE2.0'),3,1,0,0,0);
  for(let i=0;i<frames.length;i++){
    const f=frames[i], indexed=new Uint8Array(w*h);
    for(let j=0;j<indexed.length;j++)if(f[j*4+3]>=128)indexed[j]=lookup(f[j*4],f[j*4+1],f[j*4+2]);
    const delay=Math.round((i+1)*100/fps)-Math.round(i*100/fps);
    add(0x21,0xf9,4,9,...word(Math.max(2,delay)),0,0);
    add(0x2c,0,0,0,0,...word(w),...word(h),0,8);
    const compressed=gifLzw(indexed);
    for(let j=0;j<compressed.length;j+=255){
      const sub=compressed.subarray(j,j+255);
      add(sub.length);chunks.push(sub);
    }
    add(0);
  }
  add(0x3b);
  return new Blob(chunks,{type:'image/gif'});
}
