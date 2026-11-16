// Reel con historia genérico (Dieloxia). Requiere efectos.js, rlib.js y window.CFG (cfg.js).
// Escenas: gancho (foto+glassType) → notificaciones (uiWorld) → lista perdida (phone+digitalZoom) → rebobinar (zoomThrough)
// → chat resuelto (phone+uiWorld) → control humano (foto+uiWorld) → cierre (frameBreak). Tiempos = palabras ancla de la voz.
const C = window.CFG;
const A = k => { const x = C.anc[k]; return Array.isArray(x) ? at(W, x[0], x[1] || 0) : x; };
montar(v => {
  const tN = A('notif'), tC = A('cuando'), tL = A('loss'), tA = A('ahora'), tT = A('tu'), tF = A('fin');
  const Q = C.q.map(x => at(W, x[0], x[1] || 0));
  let h = FX.fondo(v);
  // 1 · gancho
  if (v < tN + .3) h += foto(v, -1, tN + .3, P[C.f1], C.f1o || {}) + chip(v, -1, tN + .3, C.hora1)
    + FX.glassType(v, 0, tN + .3, C.hook.glass, { y: C.hook.glassY ?? 960, size: C.hook.size ?? 200 })
    + `<div class="fx" style="opacity:${FX.ventana(v, -1, tN + .3)}"><div class="fx-ab fx-big" style="left:60px;right:60px;top:${C.hook.txtY ?? 1170}px;text-align:center;font-size:${C.hook.txtSize ?? 70}px;color:#fff;text-shadow:0 6px 24px rgba(0,0,0,.6);${up(v, .25, .4)}">${C.hook.txt}</div></div>`;
  // 2 · notificaciones que se acumulan
  if (v > tN && v < tC + .3) { h += foto(v, tN, tC + .3, P[C.f2], Object.assign({ dim: .62 }, C.f2o || {})) + chip(v, tN, tC + .3, C.hora1);
    C.notifs.forEach((n, i) => { const t0 = i === 0 ? tN + .3 : Q[i - 1] ?? (tN + i); h += nt(v, t0, tC + .3, 70, 420 + i * 175, 880, n[0], n[1]); }); }
  // 3 · cuando por fin contestas: lista perdida
  if (v > tC && v < tA + .2) { h += FX.phone(v, tC, tA + .2, s => lista(s, C.lista.map(f => Object.assign({ lostAt: f.lost ? tL : 0 }, f))), { y: 540 }) + chip(v, tC, tA + .2, C.hora2, 250);
    h += FX.digitalZoom(v, tL, tA + .2, C.lossN, { pre: '−', suf: ' ' + C.lossTxt, size: 84, y: 370, dur: .6 }); }
  // rebobinar
  h += FX.zoomThrough(v, tA, { dur: .8 });
  if (v > tA - .2 && v < tA + .5) h += `<div class="fx"><div class="fx-ab" style="left:0;right:0;top:820px;text-align:center;font-size:190px;opacity:${FX.ventana(v, tA - .2, tA + .5, .15)};filter:drop-shadow(0 0 40px #2fd4b4)">⏪</div></div>`;
  // 4 · ahora con tu asistente: chat resuelto
  if (v > tA + .2 && v < tT + .2) { h += foto(v, tA + .2, tT + .2, P[C.f3 || C.f1], { dim: .7, blur: 8, z0: 1.15, z1: 1.25 });
    const d = (tT - tA) / (C.chat.items.length + 1);
    h += FX.phone(v, tA + .2, tT + .2, s => chat(s, C.chat.nombre, C.chat.items.map((it, i) => Object.assign({ t: tA + .5 + i * d }, it)), '⚡ Asistente'), { y: 500 });
    h += FX.uiWorld(v, tA + .5 + d * 1.5, tT + .2, [{ x: 600, y: 1020, w: 400, html: `<div style="font-size:30px;font-weight:800">✅ ${C.ok1}</div>` }, { x: 70, y: 1170, w: 420, html: `<div style="font-size:30px;font-weight:800">⚡ ${C.ok2}</div>` }]); }
  // 5 · el dueño sigue con lo suyo + control humano
  if (v > tT && v < tF + .2) h += foto(v, tT, tF + .2, P[C.f4 || C.f2], Object.assign({ dim: .45 }, C.f4o || {})) + chip(v, tT, tF + .2, C.hora3)
    + FX.uiWorld(v, tT + .5, tF + .2, [{ x: 140, y: 1020, w: 800, html: `<div style="display:flex;gap:20px;align-items:center"><div style="font-size:54px">🖐️</div><div><div style="font-size:36px;font-weight:900">Tomar el control</div><div style="font-size:28px;color:#dfeee9">Pasas al chat humano en 1 clic</div></div></div>` }]);
  // 6 · cierre
  if (v > tF) h += cierre(v, tF, C.cierre[0], C.cierre[1]);
  h += FX.subtitulos(v, W, { y: v > tF ? 1400 : 1330, size: 58 });
  return h;
});
