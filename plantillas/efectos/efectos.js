// Librería de efectos para reels (1080x1920) con render(t) determinista.
// Los 10 efectos de la referencia: orbit, frameBreak, uiWorld, digitalZoom, phone, headlineWall,
// zoomThrough, chartGrow, doodle, glassType. Más: fondo vivo con brillo y grano, palabra por palabra.
// Uso: <script src="efectos.js"></script>; FX.tema({...}); cada función devuelve HTML para el cuadro v (segundos).
(function () {
  const T = { bg: '#0b1330', bg2: '#111C3B', a: '#34B614', a2: '#7DD818', t: '#ffffff', s: '#B8C4D6', r: '#FF4D4F', font: "'Inter',sans-serif" };
  const cl = (x, a, b) => Math.min(Math.max(x, a), b);
  const ease = x => 1 - Math.pow(1 - cl(x, 0, 1), 3);
  const inout = x => { x = cl(x, 0, 1); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const back = x => { x = cl(x, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const hash = n => { const s = Math.sin(n * 127.1) * 43758.5453; return s - Math.floor(s); };
  const ventana = (v, a, b, f = .3) => cl(Math.min((v - a) / f, (b - v) / f), 0, 1);
  const up = (v, a, d = .45, y = 70) => { const k = ease((v - a) / d); return `opacity:${cl((v - a) / .2, 0, 1)};transform:translateY(${(1 - k) * y}px)`; };
  const pop = (v, a, d = .4) => { const k = back((v - a) / d); return `opacity:${cl((v - a) / .12, 0, 1)};transform:scale(${.3 + .7 * k})`; };
  const css = () => `<style>
  .fx{position:absolute;inset:0;overflow:hidden;font-family:${T.font};color:${T.t}}
  .fx-ab{position:absolute}
  .fx-card{position:absolute;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.14);border-radius:30px;backdrop-filter:blur(14px);box-shadow:0 24px 60px rgba(0,0,0,.45)}
  .fx-big{font-weight:900;letter-spacing:-.035em;line-height:.98;text-transform:uppercase}
  .fx-glass{font-weight:900;letter-spacing:-.03em;text-transform:uppercase;color:transparent;background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(255,255,255,.35) 45%,${T.a2} 120%);-webkit-background-clip:text;background-clip:text;-webkit-text-stroke:2px rgba(255,255,255,.55);filter:drop-shadow(0 18px 30px rgba(0,0,0,.55)) drop-shadow(0 0 40px ${T.a}88)}
  .fx-tag{position:absolute;font-weight:900;text-transform:uppercase;letter-spacing:-.01em;padding:14px 26px;border-radius:14px;white-space:nowrap;box-shadow:0 14px 34px rgba(0,0,0,.45)}
  </style>`;

  // Fondo vivo: degradado, brillo que respira, cuadrícula, viñeta y grano
  function fondo(v, opt = {}) {
    const g = opt.brillo ?? 1, gx = 540 + Math.sin(v * .5) * 140, gy = (opt.y ?? 900) + Math.cos(v * .4) * 120;
    return `<div class="fx"><div class="fx-ab" style="inset:0;background:${T.bg}"></div>
    <div class="fx-ab" style="inset:0;background:radial-gradient(circle 560px at ${gx}px ${gy}px,${T.a}${Math.round(90 * g).toString(16).padStart(2, '0')},transparent 70%)"></div>
    <div class="fx-ab" style="inset:-100px;opacity:.5;background-image:linear-gradient(rgba(255,255,255,.04) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.04) 2px,transparent 2px);background-size:90px 90px;transform:translate(${(v * 18) % 90}px,${(v * 12) % 90}px)"></div>
    <div class="fx-ab" style="inset:0;background:radial-gradient(ellipse 75% 60% at 50% 45%,transparent 50%,rgba(0,0,0,.65))"></div></div>`;
  }
  function grano(v) {
    const f = Math.floor(v * 24) % 8;
    return `<svg class="fx-ab" style="inset:0;opacity:.09;mix-blend-mode:overlay;pointer-events:none" width="1080" height="1920"><filter id="g${f}"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="${f}"/></filter><rect width="1080" height="1920" filter="url(#g${f})"/></svg>`;
  }
  // Título de sección pequeño arriba del efecto (nunca logo arriba)
  const kicker = (v, a, txt, top = 330) => `<div class="fx-ab" style="left:0;right:0;top:${top}px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.22em;color:${T.a2};${up(v, a, .4, 20)}">${txt}</div>`;

  // 1 · ORBIT: íconos que giran alrededor de un núcleo (logo, foto o emoji)
  function orbit(v, a, b, centro, items, opt = {}) {
    const cx = opt.x ?? 540, cy = opt.y ?? 900, R = opt.r ?? 330, k = ease((v - a) / .6);
    let h = `<div class="fx" style="opacity:${ventana(v, a, b)}">`;
    for (const rr of [R * .62, R, R * 1.32]) h += `<div class="fx-ab" style="left:${cx - rr}px;top:${cy - rr * .42}px;width:${rr * 2}px;height:${rr * .84}px;border:2px solid rgba(255,255,255,${.12 * k});border-radius:50%"></div>`;
    const lst = items.map((it, i) => { const ang = (i / items.length) * Math.PI * 2 + v * (opt.vel ?? .9); return { it, i, x: cx + Math.cos(ang) * R * k, y: cy + Math.sin(ang) * R * .42 * k, z: Math.sin(ang) }; });
    const pinta = o => { const s = .75 + .3 * (o.z + 1) / 2; return `<div class="fx-ab" style="left:${o.x - 64}px;top:${o.y - 64}px;width:128px;height:128px;border-radius:34px;background:${T.bg2};border:2px solid rgba(255,255,255,.18);display:grid;place-items:center;font-size:62px;transform:scale(${s});opacity:${cl((v - a - .15 - o.i * .08) / .25, 0, 1) * (.55 + .45 * (o.z + 1) / 2)};box-shadow:0 0 40px ${T.a}55">${o.it}</div>`; };
    h += lst.filter(o => o.z < 0).map(pinta).join('');
    h += `<div class="fx-ab" style="left:${cx - 150}px;top:${cy - 150}px;width:300px;height:300px;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 35% 30%,${T.a2},${T.a} 55%,#0d4a08);box-shadow:0 0 120px ${T.a}aa;${pop(v, a, .5)}">${centro}</div>`;
    h += lst.filter(o => o.z >= 0).map(pinta).join('');
    return h + '</div>';
  }

  // 2 · FRAME BREAK: un objeto sale del marco (el marco recorta la parte de abajo y la de arriba sobresale)
  function frameBreak(v, a, b, objeto, opt = {}) {
    const x = opt.x ?? 150, y = opt.y ?? 620, w = opt.w ?? 780, hgt = opt.h ?? 560, k = back((v - a - .35) / .6);
    const sube = (1 - k) * 260;
    return `<div class="fx" style="opacity:${ventana(v, a, b)}">
      <div class="fx-ab" style="left:${x}px;top:${y}px;width:${w}px;height:${hgt}px;border-radius:34px;border:3px solid ${T.a2};background:rgba(255,255,255,.05);box-shadow:0 0 60px ${T.a}55;${up(v, a, .4, 40)}"><div style="position:absolute;left:24px;top:18px;font-size:22px;letter-spacing:.2em;color:${T.s}">● REC</div></div>
      <div class="fx-ab" style="left:${x}px;top:${y - 600}px;width:${w}px;height:${hgt + 600}px;overflow:hidden;clip-path:inset(0 0 ${0}px 0)">
        <div style="position:absolute;left:0;right:0;bottom:${-sube}px;display:flex;justify-content:center;filter:drop-shadow(0 30px 40px rgba(0,0,0,.5))">${objeto}</div></div></div>`;
  }

  // 3 · UI WORLD: tarjetas de interfaz que flotan alrededor (cada una: {x,y,w,html})
  function uiWorld(v, a, b, tarjetas) {
    return `<div class="fx" style="opacity:${ventana(v, a, b)}">${tarjetas.map((c, i) => {
      const t0 = a + .12 * i, k = ease((v - t0) / .5), fl = Math.sin(v * 1.6 + i * 1.7) * 14, rot = (hash(i + 3) - .5) * 8;
      return `<div class="fx-card" style="left:${c.x}px;top:${c.y + fl + (1 - k) * 120}px;width:${c.w}px;padding:24px 28px;opacity:${k};transform:perspective(900px) rotateY(${rot}deg) rotateX(${rot / 2}deg) scale(${.85 + .15 * k})">${c.html}</div>`;
    }).join('')}</div>`;
  }

  // 4 · DIGITAL ZOOM: número que sube con golpes de zoom y mira de cámara
  function digitalZoom(v, a, b, valor, opt = {}) {
    const k = ease((v - a) / (opt.dur ?? 1.2)), n = Math.round(valor * k), punch = 1 + .12 * Math.exp(-(((v - a - (opt.dur ?? 1.2)) * 6) ** 2));
    const txt = (opt.pre ?? '') + n.toLocaleString('es-MX') + (opt.suf ?? '');
    return `<div class="fx" style="opacity:${ventana(v, a, b)};transform:scale(${punch + (v - a) * .015})">
      <div class="fx-ab" style="left:60px;right:60px;top:${(opt.y ?? 760)}px;text-align:center"><span style="display:inline-block;border:4px solid ${opt.color ?? T.r};border-radius:26px;padding:18px 40px;font-weight:900;font-size:${opt.size ?? 150}px;letter-spacing:-.03em;color:#fff;box-shadow:0 0 70px ${(opt.color ?? T.r)}77;${pop(v, a, .35)}">${txt}</span></div>
      <svg class="fx-ab" style="left:490px;top:${(opt.y ?? 760) + 300}px" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="22" fill="none" stroke="${opt.color ?? T.r}" stroke-width="4"/><path d="M50 10v22M50 68v22M10 50h22M68 50h22" stroke="${opt.color ?? T.r}" stroke-width="4"/></svg></div>`;
  }

  // 5 · PHONE MOCKUP: celular con pantalla viva (contenido = función de v)
  function phone(v, a, b, pantalla, opt = {}) {
    const x = opt.x ?? 300, y = opt.y ?? 470, k = ease((v - a) / .55), rot = (1 - k) * 18 + Math.sin(v * .8) * 2.5;
    return `<div class="fx" style="opacity:${ventana(v, a, b)}"><div class="fx-ab" style="left:${x}px;top:${y + (1 - k) * 300}px;width:480px;height:960px;border-radius:70px;background:#05070f;border:10px solid #2a3350;box-shadow:0 50px 120px rgba(0,0,0,.6),0 0 90px ${T.a}44;transform:perspective(1400px) rotateY(${rot}deg) rotateX(${(1 - k) * 10}deg);overflow:hidden">
      <div style="position:absolute;left:170px;top:16px;width:120px;height:34px;border-radius:20px;background:#000;z-index:3"></div>
      <div style="position:absolute;inset:0;background:#f4f6fa;color:#111C3B">${pantalla(v)}</div></div></div>`;
  }

  // 6 · HEADLINE WALL: titulares que caen y se apilan inclinados
  function headlineWall(v, a, b, titulares, opt = {}) {
    return `<div class="fx" style="opacity:${ventana(v, a, b)}">${titulares.map((t, i) => {
      const t0 = a + i * (opt.paso ?? .28), k = back((v - t0) / .35), rot = (hash(i + 9) - .5) * 12, x = 80 + hash(i + 2) * 360, y = (opt.y ?? 560) + i * 118;
      const col = i % 3 === 1 ? [T.r, '#fff'] : i % 3 === 2 ? [T.a, '#fff'] : ['#fff', T.bg2];
      return `<div class="fx-tag" style="left:${x}px;top:${y}px;font-size:${opt.size ?? 46}px;background:${col[0]};color:${col[1]};opacity:${cl((v - t0) / .1, 0, 1)};transform:rotate(${rot}deg) scale(${2.2 - 1.2 * k})">${t}</div>`;
    }).join('')}</div>`;
  }

  // 7 · ZOOM THROUGH: transición, la cámara atraviesa un anillo/portal (dura ~.7 s centrada en c)
  function zoomThrough(v, c, opt = {}) {
    const d = opt.dur ?? .7, x = (v - (c - d / 2)) / d;
    if (x < 0 || x > 1) return '';
    const s = Math.pow(40, inout(x)) * .4, o = x < .85 ? 1 : (1 - x) / .15;
    return `<div class="fx" style="pointer-events:none"><div class="fx-ab" style="left:540px;top:${opt.y ?? 900}px;width:0;height:0">
      ${[0, 1, 2].map(i => `<div style="position:absolute;left:-300px;top:-300px;width:600px;height:600px;border-radius:50%;border:${10 - i * 3}px solid ${i ? T.a2 : T.a};opacity:${o * (1 - i * .25)};transform:scale(${s * (1 + i * .35)});box-shadow:0 0 80px ${T.a}"></div>`).join('')}</div>
      <div class="fx-ab" style="inset:0;background:${T.a2};opacity:${cl(1 - Math.abs(x - .55) / .12, 0, 1) * .35}"></div></div>`;
  }

  // 8 · CHART GROW: barras que crecen con contador
  function chartGrow(v, a, b, datos, opt = {}) {
    const x = opt.x ?? 110, y = opt.y ?? 560, w = 860, h = opt.h ?? 620, mx = Math.max(...datos.map(d => d[1]));
    const k = ease((v - a - .3) / 1.4), total = datos.reduce((s, d) => s + d[1], 0);
    const bw = (w - 80) / datos.length;
    return `<div class="fx" style="opacity:${ventana(v, a, b)}"><div class="fx-card" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${up(v, a, .4, 60)}">
      <div style="position:absolute;left:40px;top:30px;font-size:84px;font-weight:900;letter-spacing:-.03em">${(opt.pre ?? '')}${Math.round(total * k).toLocaleString('es-MX')}${opt.suf ?? ''}</div>
      <div style="position:absolute;right:40px;top:52px;font-size:26px;font-weight:700;color:${T.s}">${opt.titulo ?? ''}</div>
      ${datos.map((d, i) => { const kk = ease((v - a - .3 - i * .12) / .8), hh = (h - 260) * d[1] / mx * kk; return `<div style="position:absolute;left:${40 + i * bw + bw * .15}px;bottom:70px;width:${bw * .7}px;height:${hh}px;border-radius:14px 14px 4px 4px;background:linear-gradient(180deg,${T.a2},${T.a});box-shadow:0 0 30px ${T.a}66"></div><div style="position:absolute;left:${40 + i * bw}px;width:${bw}px;bottom:22px;text-align:center;font-size:24px;font-weight:700;color:${T.s}">${d[0]}</div>`; }).join('')}</div></div>`;
  }

  // 9 · DOODLE BOIL: garabato a mano que "hierve" (cambia 8 veces por segundo) alrededor de un texto
  function doodle(v, a, b, texto, opt = {}) {
    const f = Math.floor(v * 8), cx = 540, cy = opt.y ?? 900, rx = opt.rx ?? 380, ry = opt.ry ?? 190, k = ease((v - a) / .6);
    const pts = [...Array(40)].map((_, i) => { const t = i / 40 * Math.PI * 2, j = (hash(i * 7 + f) - .5) * 16; return [cx + Math.cos(t) * (rx + j), cy + Math.sin(t) * (ry + j)]; });
    const d = 'M' + pts.map(p => p.join(',')).join(' L') + ' Z';
    const rayos = [...Array(10)].map((_, i) => { const t = i / 10 * Math.PI * 2 + .3, j = (hash(i + f * 3) - .5) * 14; return `<path d="M${cx + Math.cos(t) * (rx + 40)},${cy + Math.sin(t) * (ry + 40)} L${cx + Math.cos(t) * (rx + 90 + j)},${cy + Math.sin(t) * (ry + 90 + j)}" stroke="${opt.color ?? '#fff'}" stroke-width="7" stroke-linecap="round"/>`; }).join('');
    const len = 2 * Math.PI * Math.sqrt((rx * rx + ry * ry) / 2);
    return `<div class="fx" style="opacity:${ventana(v, a, b)}"><svg class="fx-ab" style="left:0;top:0" width="1080" height="1920">
      <path d="${d}" fill="none" stroke="${opt.color ?? '#fff'}" stroke-width="8" stroke-linejoin="round" stroke-dasharray="${len * 1.1}" stroke-dashoffset="${len * 1.1 * (1 - k)}"/><g opacity="${cl((v - a - .5) / .2, 0, 1)}">${rayos}</g></svg>
      <div class="fx-ab" style="left:0;right:0;top:${cy - (opt.size ?? 150) * .62}px;text-align:center;font-size:${opt.size ?? 150}px;font-weight:900;transform:rotate(${(hash(f) - .5) * 4}deg);font-family:'Comic Sans MS','Marker Felt',${T.font};${pop(v, a + .2, .35)}">${texto}</div></div>`;
  }

  // 10 · GLASS TYPE: tipografía de cristal 3D con brillo que barre
  function glassType(v, a, b, texto, opt = {}) {
    const k = ease((v - a) / .7), sw = ((v - a) * 60) % 160 - 30, sz = opt.size ?? 190;
    return `<div class="fx" style="opacity:${ventana(v, a, b)}"><div class="fx-ab" style="left:0;right:0;top:${opt.y ?? 760}px;text-align:center;transform:perspective(1200px) rotateX(${(1 - k) * 60}deg) translateY(${(1 - k) * 80}px) scale(${.8 + .2 * k});opacity:${k}">
      <div class="fx-glass" style="font-size:${sz}px;line-height:1;position:relative;display:inline-block">${texto}
      <span style="position:absolute;inset:0;background:linear-gradient(100deg,transparent ${sw}%,rgba(255,255,255,.9) ${sw + 6}%,transparent ${sw + 12}%);-webkit-background-clip:text;background-clip:text;color:transparent">${texto}</span></div></div></div>`;
  }

  // Subtítulos palabra por palabra (W = [{t,w,raw}] de make_reel.py)
  function subtitulos(v, W, opt = {}) {
    let gi = -1; const g = []; let cur = [];
    W.forEach((w, i) => { cur.push(i); if (/[.,…:?;!]$/.test(w.raw || w.w) || cur.length >= (opt.max ?? 4) || i === W.length - 1) { g.push(cur); cur = []; } });
    for (let k = 0; k < g.length; k++) { const s = W[g[k][0]].t, e = k + 1 < g.length ? W[g[k + 1][0]].t : 99; if (v >= s - .05 && v < e) gi = k; }
    if (gi < 0) return '';
    return `<div class="fx-ab" style="left:70px;right:70px;top:${opt.y ?? 1500}px;text-align:center;font-weight:800;font-size:${opt.size ?? 60}px;line-height:1.14;color:#fff;-webkit-text-stroke:7px ${T.bg};paint-order:stroke fill;z-index:40">${g[gi].map(i => { const on = v >= W[i].t - .03, p = back((v - W[i].t) / .2); return `<span style="display:inline-block;color:${on ? T.a2 : '#fff'};transform:scale(${on ? .9 + .1 * p : 1})">${W[i].w}</span>`; }).join(' ')}</div>`;
  }

  // Momento de una palabra del guion (n = ocurrencia); palabras cortas se comparan exactas
  const at = (W, w, n = 0) => { const m = W.filter(x => { const s = (x.w || '').toLowerCase().replace(/[;:,.]$/, ''); return w.length <= 3 ? s === w : s.startsWith(w); }); return (m[n] || m[m.length - 1] || { t: 0 }).t; };

  window.FX = { tema: o => Object.assign(T, o), T, css, fondo, grano, kicker, orbit, frameBreak, uiWorld, digitalZoom, phone, headlineWall, zoomThrough, chartGrow, doodle, glassType, subtitulos, at, ease, back, cl, up, pop, ventana };
})();
