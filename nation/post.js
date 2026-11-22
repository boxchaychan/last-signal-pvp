'use strict';
/* ก่อร่างสร้างชาติ: the finishing pass on the whole picture: glow, film colour, miniature-style focus.
   Turns itself off on a device that cannot keep up. ?fx=0 turns it off by hand. */
(function () {
  if (new URLSearchParams(location.search).get('fx') === '0') return;
  const HQ = !MOBILE; let rt = null, a1, a2, b1, b2, w0 = 0, h0 = 0, lastT = 0, sum = 0, cnt = 0, slow = 0;
  const scene = new THREE.Scene(), cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1), quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2)); quad.frustumCulled = false; scene.add(quad);
  const vs = 'varying vec2 v;void main(){v=uv;gl_Position=vec4(position.xy,0.,1.);}';
  const mk = (u, fs) => new THREE.ShaderMaterial({ uniforms: u, vertexShader: vs, fragmentShader: fs, depthTest: false, depthWrite: false, toneMapped: false });
  const bright = mk({ t: { value: null }, th: { value: .9 } }, 'uniform sampler2D t;uniform float th;varying vec2 v;void main(){vec3 c=texture2D(t,v).rgb;float l=max(c.r,max(c.g,c.b));gl_FragColor=vec4(c*smoothstep(th,th+.22,l),1.);}');
  const blur = mk({ t: { value: null }, d: { value: new THREE.Vector2() } }, 'uniform sampler2D t;uniform vec2 d;varying vec2 v;void main(){vec3 c=texture2D(t,v).rgb*.227;c+=(texture2D(t,v+d*1.385).rgb+texture2D(t,v-d*1.385).rgb)*.316;c+=(texture2D(t,v+d*3.231).rgb+texture2D(t,v-d*3.231).rgb)*.07;gl_FragColor=vec4(c,1.);}');
  const final = mk({ t: { value: null }, b: { value: null }, c2: { value: null }, px: { value: new THREE.Vector2() }, tilt: { value: 0 }, night: { value: 0 } },
    'uniform sampler2D t,b,c2;uniform vec2 px;uniform float tilt,night;varying vec2 v;void main(){float k=smoothstep(.17,.52,abs(v.y-.5))*tilt;vec3 c=texture2D(t,v).rgb;' +
    (HQ ? 'if(k>.01){vec3 s=c;for(int i=0;i<8;i++){float a=float(i)*.7854+.39,r=mod(float(i),2.)<.5?3.2:5.6;s+=texture2D(t,v+vec2(cos(a),sin(a))*px*k*r).rgb;}c=s/9.;}' : '') +
    'vec3 g=texture2D(b,v).rgb*.75+texture2D(c2,v).rgb*.65;c+=g*(.24+night*.34);c=clamp(c,0.,1.);c=mix(c,c*c*(3.-2.*c),.34);float l=dot(c,vec3(.3,.59,.11));c=mix(vec3(l),c,1.14);c*=mix(vec3(1.025,1.,.955),vec3(.93,.98,1.1),night);gl_FragColor=vec4(clamp(c,0.,1.),1.);}');
  const pass = (m, target) => { quad.material = m; W.renderer.setRenderTarget(target); W.renderer.render(scene, cam); };
  function free() { for (const q of [rt, a1, a2, b1, b2]) if (q) q.dispose(); rt = null; }
  function alloc(w, h) {
    free(); w0 = w; h0 = h; const r = W.renderer, hdr = HQ && (r.extensions.has('EXT_color_buffer_float') || r.extensions.has('EXT_color_buffer_half_float')), type = hdr ? THREE.HalfFloatType : THREE.UnsignedByteType, o = { type, depthBuffer: false, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter };
    rt = new THREE.WebGLRenderTarget(w, h, { type, samples: HQ ? 4 : 0, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter });
    const q = (s) => new THREE.WebGLRenderTarget(Math.max(2, w >> s), Math.max(2, h >> s), o); a1 = q(2); a2 = q(2); b1 = q(4); b2 = q(4);
  }
  function off() { W.post = null; free(); W.renderer.setRenderTarget(null); if (!MOBILE) document.body.classList.add('hi'); }
  const size = new THREE.Vector2();
  W.post = function () {
    const now = performance.now(), ft = now - lastT; lastT = now; if (ft < 250 && document.visibilityState === 'visible') { sum += ft; if (++cnt >= 150) { slow = sum / cnt > 41 ? slow + 1 : 0; sum = 0; cnt = 0; if (slow >= 3) { off(); W.renderer.render(W.scene, W.camera); return; } } } else { sum = 0; cnt = 0; }
    const r = W.renderer; r.getDrawingBufferSize(size); if (size.x !== w0 || size.y !== h0 || !rt) alloc(size.x, size.y); document.body.classList.remove('hi');
    const night = W.nightU.value; r.setRenderTarget(rt); r.render(W.scene, W.camera);
    bright.uniforms.t.value = rt.texture; bright.uniforms.th.value = .93 - night * .36; pass(bright, a1);
    const B = (src, dst, x, y) => { blur.uniforms.t.value = src.texture; blur.uniforms.d.value.set(x / src.width, y / src.height); pass(blur, dst); };
    B(a1, a2, 1, 0); B(a2, a1, 0, 1); B(a1, b1, 1, 0); B(b1, b2, 0, 1); B(b2, b1, 1.4, 0); B(b1, b2, 0, 1.4);
    const u = final.uniforms; u.t.value = rt.texture; u.b.value = a1.texture; u.c2.value = b2.texture; u.px.value.set(1 / size.x, 1 / size.y); u.tilt.value = clamp(1.3 - W.cam.dist / 62, .12, 1) * (size.y / 720); u.night.value = night; pass(final, null);
  };
})();
