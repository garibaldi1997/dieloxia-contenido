// Ayudas compartidas de los reels de Dieloxia (usan efectos.js)
FX.tema({ bg: '#0d1b1e', bg2: '#06402b', a: '#00b35c', a2: '#2fd4b4' });
const { at, up, pop, T, cl, ease } = FX;
const SPEED = window.SPEED || 1, W = window.WORDS || [], P = window.PH || {};
const WA = `<svg viewBox="0 0 24 24" width="34" height="34"><path fill="#fff" d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z"/></svg>`;
// foto de fondo con Ken Burns y velo oscuro (ventana a..b con fundido)
function foto(v, a, b, src, o = {}) {
  const k = cl((v - a) / (b - a), 0, 1), z = (o.z0 ?? 1.06) + ((o.z1 ?? 1.2) - (o.z0 ?? 1.06)) * k;
  const px = (o.x0 ?? 50) + ((o.x1 ?? o.x0 ?? 50) - (o.x0 ?? 50)) * k;
  return `<div class="fx" style="opacity:${FX.ventana(v, a, b, o.f ?? .25)}"><img src="${src}" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;object-position:${px}% ${o.y ?? 40}%;transform:scale(${z});filter:blur(${o.blur ?? 0}px) saturate(1.05)">
  <div class="fx-ab" style="inset:0;background:linear-gradient(180deg,rgba(13,27,30,${(o.dim ?? .5) - .1}),rgba(6,64,43,${(o.dim ?? .5) + .15}))"></div></div>`;
}
const chip = (v, a, b, txt, top = 250) => `<div class="fx" style="opacity:${FX.ventana(v, a, b, .2)}"><div class="fx-ab" style="left:0;right:0;top:${top}px;text-align:center"><span style="display:inline-block;background:rgba(13,27,30,.8);backdrop-filter:blur(6px);border:2px solid rgba(255,255,255,.18);border-radius:99px;padding:14px 32px;font-size:40px;font-weight:800;color:#fff">🕒 ${txt}</span></div></div>`;
const notif = (who, msg) => `<div style="display:flex;gap:18px;align-items:center"><div style="width:64px;height:64px;border-radius:18px;background:#25d366;display:grid;place-items:center;flex:none">${WA}</div><div><div style="font-size:30px;font-weight:800">${who}</div><div style="font-size:28px;color:#dfeee9;margin-top:2px">${msg}</div></div></div>`;
// una tarjeta de notificación que aparece en el momento a
const nt = (v, a, b, x, y, w, who, msg) => FX.uiWorld(v, a, b, [{ x, y, w, html: notif(who, msg) }]);
// pantalla de chat de WhatsApp (items [{t,s:'in'|'out',m}])
function chat(v, nombre, items, tag) {
  return `<div style="position:absolute;inset:0;background:#efeae2"><div style="position:absolute;left:0;right:0;top:0;height:128px;background:#075e54;color:#fff;padding:58px 24px 0;font-size:28px;font-weight:700">${nombre}${tag ? `<span style="float:right;font-size:20px;background:#2fd4b4;color:#06402b;border-radius:99px;padding:6px 14px;margin-top:-4px">${tag}</span>` : ''}</div>
  <div style="position:absolute;left:0;right:0;top:150px;padding:0 18px">${items.filter(i => v >= i.t).map(i => { const k = ease((v - i.t) / .35); return `<div style="display:flex;justify-content:${i.s === 'out' ? 'flex-end' : 'flex-start'};margin-bottom:16px;opacity:${k};transform:translateY(${(1 - k) * 30}px)"><div style="max-width:330px;font-size:26px;line-height:1.28;padding:14px 18px;border-radius:18px;background:${i.s === 'out' ? '#d9fdd3' : '#fff'};color:#0d1b1e;box-shadow:0 2px 4px rgba(0,0,0,.12)">${i.m}</div></div>`; }).join('')}</div></div>`;
}
// lista de chats (filas [{n,m,c,t,badge|ok|lost}]) con cambios por tiempo
function lista(v, filas) {
  return `<div style="position:absolute;inset:0;background:#fff"><div style="height:128px;background:#075e54;color:#fff;padding:60px 26px 0;font-size:32px;font-weight:800">WhatsApp Business</div>${filas.map(f => { const lost = f.lostAt && v >= f.lostAt, ok = f.okAt && v >= f.okAt;
    return `<div style="display:flex;gap:16px;align-items:center;padding:22px 24px;border-bottom:1px solid #eef0ef;background:${lost ? '#fde8ea' : ok ? '#f1fbf5' : '#fff'}"><div style="width:68px;height:68px;border-radius:50%;background:${f.c};color:#fff;font-weight:800;font-size:30px;display:grid;place-items:center;flex:none">${f.n[0]}</div><div style="flex:1;min-width:0"><div style="font-size:26px;font-weight:800">${f.n}</div><div style="font-size:22px;color:#5b6663;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${lost ? f.lost : ok ? '✓✓ ' + f.ok : f.m}</div></div>${lost ? '' : ok ? `<div style="font-size:18px;font-weight:800;background:#e8f7ef;color:#06402b;border-radius:99px;padding:5px 10px">${f.tag || 'Respondido'}</div>` : `<div style="background:#25d366;color:#fff;font-weight:800;font-size:20px;border-radius:99px;padding:3px 11px">1</div>`}</div>`; }).join('')}</div>`;
}
function cierre(v, a, titulo, linea, url = 'dieloxia.com') {
  const icono = `<div style="width:300px;height:300px;border-radius:70px;background:#fff;display:grid;place-items:center;box-shadow:0 0 80px ${T.a}99"><img src="${P.logo}" style="width:220px"></div>`;
  return FX.fondo(v, { brillo: 1.3 }) + FX.frameBreak(v, a, 999, icono, { x: 240, y: 560, w: 600, h: 200 })
    + `<div class="fx-ab fx-big" style="left:50px;right:50px;top:860px;text-align:center;font-size:76px;${up(v, a + .3, .4)}">${titulo}</div>
       <div class="fx-ab" style="left:60px;right:60px;top:1130px;text-align:center;font-size:42px;font-weight:700;color:${T.s};${up(v, a + .9, .4, 30)}">${linea}</div>
       <div class="fx-ab" style="left:0;right:0;top:1270px;text-align:center;font-size:50px;font-weight:900;color:${T.a2};${up(v, a + 1.3, .5, 30)}">${url}</div>`;
}
function montar(render) {
  window.render = t => { const v = t * SPEED; document.getElementById('root').innerHTML = FX.css() + render(v) + FX.grano(v); };
}
