#!/usr/bin/env python3
"""Genera docs/index.html: calendario de publicaciones y desempeño de cada una.

Se publica con GitHub Pages (carpeta docs/). Lo regeneran los workflows de
publicar y de métricas, así que siempre está al día.
"""
import html
import json
import os
from datetime import datetime, timedelta, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.environ.get("GITHUB_REPOSITORY", "garibaldi1997/dieloxia-contenido")
CDMX = timezone(timedelta(hours=-6))
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
TIPO = {"imagen": "Post", "carrusel": "Carrusel", "reel": "Reel", "historia": "Historia"}
RED = {"instagram": "IG", "facebook": "FB", "linkedin": "in"}


def cargar(ruta, defecto):
    p = os.path.join(RAIZ, ruta)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else defecto


def esc(t):
    return html.escape(str(t or ""))


def puntaje(m):
    """Prioridad de la estrategia: guardados y compartidos > comentarios > me gusta."""
    ig, fb = m.get("instagram") or {}, m.get("facebook") or {}
    g = ig.get("saved", 0) or 0
    c = (ig.get("shares", 0) or 0) + (fb.get("compartidos", 0) or 0)
    co = (ig.get("comments_count", 0) or 0) + (fb.get("comentarios", 0) or 0)
    l = (ig.get("like_count", 0) or 0) + (fb.get("reacciones", 0) or 0)
    return g * 4 + c * 4 + co * 2 + l, g, c, co, l, (ig.get("reach", 0) or 0), (ig.get("views", 0) or 0)


def main():
    cal = cargar("calendario.json", [])
    pub = cargar("estado/publicados.json", {})
    met = cargar("estado/metricas.json", {"publicaciones": {}})
    mp = met.get("publicaciones", {})
    ahora = datetime.now(timezone.utc)
    raw = f"https://raw.githubusercontent.com/{REPO}/main/"

    filas, prox = [], []
    tot = dict(pubs=0, alcance=0, guardados=0, compartidos=0, comentarios=0, likes=0)
    for e in sorted(cal, key=lambda x: x["fecha"]):
        f = datetime.fromisoformat(e["fecha"]).astimezone(CDMX)
        hecho = {r: i for r, i in pub.get(e["id"], {}).items() if not i.get("omitido")}
        vivos = {r: i for r, i in hecho.items() if not i.get("borrado")}
        img = (e.get("imagenes") or [None])[0]
        thumb = f'<img loading="lazy" src="{raw}{esc(img)}" alt="">' if img else '<div class="vid">▶</div>'
        tema = esc((e.get("texto") or "Historia").split("\n")[0][:110])
        redes = " ".join(
            f'<span class="red {"ok" if r in vivos else ("del" if r in hecho else "")}">{RED.get(r, r)}</span>'
            for r in e.get("redes", []))
        if hecho:
            m = mp.get(e["id"], {})
            s, g, c, co, l, al, vi = puntaje(m)
            if vivos:
                tot["pubs"] += 1
                for k, v in (("alcance", al), ("guardados", g), ("compartidos", c), ("comentarios", co), ("likes", l)):
                    tot[k] += v
            links = " ".join(
                f'<a href="{esc((m.get(r) or {}).get("permalink"))}" target="_blank" rel="noopener">{RED.get(r, r)}↗</a>'
                for r in vivos if (m.get(r) or {}).get("permalink"))
            filas.append((s, f"""<tr><td class="t">{thumb}</td><td><b>{tema}</b><small>{TIPO.get(e['tipo'], e['tipo'])} · {f.day} {MESES[f.month-1]} {f:%H:%M}</small><div>{redes} {links}</div></td>
<td class="n">{al}</td><td class="n">{l}</td><td class="n">{co}</td><td class="n">{c}</td><td class="n">{g}</td><td class="n s">{s}</td></tr>"""))
        elif f >= ahora.astimezone(CDMX) - timedelta(hours=1):
            prox.append((f, e, thumb, tema, redes))

    dias = {}
    for f, e, thumb, tema, redes in prox:
        dias.setdefault(f.date(), []).append(
            f'<div class="it"><div class="t">{thumb}</div><div><span class="hr">{f:%H:%M}</span> <span class="tp {e["tipo"]}">{TIPO.get(e["tipo"], e["tipo"])}</span><p>{tema}</p><div>{redes}</div></div></div>')
    cal_html = "".join(
        f'<section class="dia"><h3>{DIAS[d.weekday()]} {d.day} {MESES[d.month-1]}</h3>{"".join(v)}</section>'
        for d, v in sorted(dias.items())) or '<p class="vacio">No hay publicaciones programadas.</p>'
    filas.sort(key=lambda x: -x[0])
    act = met.get("actualizado", "")
    try:
        act = datetime.fromisoformat(act).astimezone(CDMX).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        pass

    kpis = "".join(f'<div class="k"><b>{v:,}</b><span>{t}</span></div>' for t, v in (
        ("Publicaciones activas", tot["pubs"]), ("Alcance IG", tot["alcance"]), ("Me gusta", tot["likes"]),
        ("Comentarios", tot["comentarios"]), ("Compartidos", tot["compartidos"]), ("Guardados", tot["guardados"])))

    out = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Panel de Contenido</title><meta name="robots" content="noindex">
<style>
:root{{--bg:#F2F6FB;--card:#fff;--ink:#111C3B;--mut:#5B6782;--line:#E1E7F0;--g:#34B614;--b:#0A4E94;--r:#E21B20}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0B1226;--card:#141D38;--ink:#EEF2F8;--mut:#9AA6C0;--line:#26304F}}}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--ink);padding:24px 16px 60px}}
.w{{max-width:1100px;margin:0 auto}}header{{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap}}
h1{{font-size:26px;letter-spacing:-.02em}}h1 span{{color:var(--g)}}h2{{font-size:18px;margin:28px 0 12px}}.mut{{color:var(--mut);font-size:13px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-top:18px}}.k{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px}}.k b{{display:block;font-size:24px}}.k span{{font-size:12px;color:var(--mut)}}
.cal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}}.dia{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px}}.dia h3{{font-size:14px;text-transform:capitalize;margin-bottom:8px;color:var(--b)}}
.it{{display:flex;gap:10px;padding:8px 0;border-top:1px solid var(--line)}}.it:first-of-type{{border-top:0}}.it p{{font-size:12.5px;line-height:1.35;margin:3px 0}}
.t img,.vid{{width:52px;height:64px;object-fit:cover;border-radius:8px;background:var(--line);display:grid;place-items:center;color:var(--mut)}}.hr{{font-weight:700;font-size:13px}}
.tp{{font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:99px;background:var(--line)}}.tp.reel{{background:#FDE7E7;color:var(--r)}}.tp.carrusel{{background:#E3EEFA;color:var(--b)}}.tp.imagen{{background:#E6F6E0;color:#1F7A0E}}
.red{{display:inline-block;font-size:10.5px;font-weight:700;border:1px solid var(--line);border-radius:6px;padding:1px 5px;color:var(--mut)}}.red.ok{{background:var(--g);border-color:var(--g);color:#fff}}.red.del{{text-decoration:line-through}}
.tw{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:14px}}table{{width:100%;border-collapse:collapse;font-size:13px;min-width:640px}}th{{text-align:left;font-size:11.5px;color:var(--mut);padding:10px;border-bottom:1px solid var(--line)}}
td{{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}}td small{{display:block;color:var(--mut);margin:2px 0 4px}}td.n{{text-align:right;font-variant-numeric:tabular-nums}}td.s{{font-weight:800;color:var(--g)}}td a{{font-size:11px;color:var(--b);margin-left:4px}}
.vacio{{color:var(--mut)}}footer{{margin-top:24px;font-size:12px;color:var(--mut)}}
</style></head><body><div class="w">
<header><div><h1>Panel de contenido · <span>Dieloxia</span></h1><p class="mut">Métricas actualizadas: {esc(act)} (hora CDMX) · se actualiza solo todos los días</p></div></header>
<div class="kpis">{kpis}</div>
<h2>📅 Próximas publicaciones</h2><div class="cal">{cal_html}</div>
<h2>🏆 Desempeño de lo publicado</h2><p class="mut" style="margin:-6px 0 10px">Ordenado por puntaje: guardados y compartidos ×4, comentarios ×2, me gusta ×1. Verde = publicado en esa red; tachado = borrado.</p>
<div class="tw"><table><tr><th></th><th>Publicación</th><th>Alcance</th><th>Me gusta</th><th>Coment.</th><th>Compart.</th><th>Guard.</th><th>Puntaje</th></tr>{"".join(f for _, f in filas)}</table></div>
<footer>LinkedIn todavía no reporta métricas (se activan cuando LinkedIn apruebe el acceso de la página).</footer>
</div></body></html>"""
    os.makedirs(os.path.join(RAIZ, "docs"), exist_ok=True)
    open(os.path.join(RAIZ, "docs", "index.html"), "w", encoding="utf-8").write(out)
    print(f"Panel: {len(filas)} publicadas, {len(prox)} programadas")


if __name__ == "__main__":
    main()
