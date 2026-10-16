#!/usr/bin/env python3
"""Convierte las métricas en aprendizajes para el siguiente post: estado/aprendizajes.md.

Puntaje por post = guardados×4 + compartidos×4 + comentarios×2 + me gusta (IG + FB).
Solo cuenta posts con más de 24 h publicados (antes las cifras todavía crecen).
Lo leen las rutinas antes de crear contenido nuevo.
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publicar as p  # noqa: E402

CDMX = timezone(timedelta(hours=-6))
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
SALIDA = os.path.join(p.RAIZ, "estado", "aprendizajes.md")


def valores(m):
    ig, fb = m.get("instagram") or {}, m.get("facebook") or {}
    n = lambda d, k: d.get(k, 0) or 0  # noqa: E731
    g, c = n(ig, "saved"), n(ig, "shares") + n(fb, "compartidos")
    co, l = n(ig, "comments_count") + n(fb, "comentarios"), n(ig, "like_count") + n(fb, "reacciones")
    return {"puntaje": g * 4 + c * 4 + co * 2 + l, "alcance": n(ig, "reach"), "vistas": n(ig, "views"),
            "guardados": g, "compartidos": c, "comentarios": co, "likes": l}


def franja(h):
    return "mañana (6–11)" if 6 <= h < 12 else "mediodía (12–15)" if h < 16 else "tarde (16–19)" if h < 20 else "noche (20–5)"


def tabla(grupos, titulo):
    filas = sorted(grupos.items(), key=lambda kv: -sum(x["alcance"] for x in kv[1]) / len(kv[1]))
    out = [f"\n### Por {titulo}", "| | posts | alcance prom. | puntaje prom. |", "|---|---|---|---|"]
    for k, xs in filas:
        out.append(f"| {k} | {len(xs)} | {sum(x['alcance'] for x in xs) / len(xs):.0f} | {sum(x['puntaje'] for x in xs) / len(xs):.1f} |")
    return out


def main():
    met = p.cargar(os.path.join(p.RAIZ, "estado", "metricas.json"), {}).get("publicaciones", {})
    crec = p.cargar(os.path.join(p.RAIZ, "estado", "crecimiento.json"), [])
    ahora = datetime.now(timezone.utc)
    posts = []
    for pid, m in met.items():
        if not m.get("fecha") or "error" in (m.get("instagram") or {}) or m.get("tipo") == "historia":
            continue
        f = datetime.fromisoformat(m["fecha"])
        if ahora - f < timedelta(hours=24):
            continue
        fl = f.astimezone(CDMX)
        posts.append({"id": pid, "tipo": m.get("tipo"), "tema": m.get("tema", ""), "hora": fl.hour,
                      "dia": DIAS[fl.weekday()], **valores(m)})

    out = ["# Aprendizajes automáticos", f"_Actualizado: {ahora.astimezone(CDMX):%d/%m/%Y %H:%M} CDMX · {len(posts)} posts con más de 24 h (historias excluidas)._"]
    cuentas = sorted({c["cuenta"] for c in crec})
    if cuentas:
        out.append("\n## Seguidores")
        for cu in cuentas:
            serie = [c for c in crec if c["cuenta"] == cu]
            a, b = serie[0], serie[-1]
            delta = lambda k: (b.get(k) or 0) - (a.get(k) or 0)  # noqa: E731
            out.append(f"- **{cu}** ({b['fecha']}): Instagram {b.get('ig_seguidores')} ({delta('ig_seguidores'):+d} desde {a['fecha']}), "
                       f"Facebook {b.get('fb_seguidores')} ({delta('fb_seguidores'):+d})")
    if len(posts) < 3:
        out.append("\nTodavía hay pocos datos: sigue la estrategia y prueba formatos y horas distintos para aprender rápido.")
    else:
        posts.sort(key=lambda x: (-x["alcance"], -x["puntaje"]))
        out.append("\n## Mejores 3 (repetir el patrón: formato, tipo de gancho, hora)")
        for x in posts[:3]:
            out.append(f"- **{x['tema']}** · {x['tipo']} · {x['dia']} {x['hora']}:00 · alcance {x['alcance']}, vistas {x['vistas']}, guardados {x['guardados']}, compartidos {x['compartidos']}, comentarios {x['comentarios']}")
        out.append("\n## Peores 3 (no repetir ese gancho/formato/hora tal cual)")
        for x in posts[-3:]:
            out.append(f"- **{x['tema']}** · {x['tipo']} · {x['dia']} {x['hora']}:00 · alcance {x['alcance']}, puntaje {x['puntaje']}")
        por_tipo, por_franja, por_dia = defaultdict(list), defaultdict(list), defaultdict(list)
        for x in posts:
            por_tipo[x["tipo"]].append(x)
            por_franja[franja(x["hora"])].append(x)
            por_dia[x["dia"]].append(x)
        out += tabla(por_tipo, "formato") + tabla(por_franja, "horario") + tabla(por_dia, "día")
        mejor_tipo = max(por_tipo, key=lambda k: sum(x["alcance"] for x in por_tipo[k]) / len(por_tipo[k]))
        mejor_franja = max(por_franja, key=lambda k: sum(x["alcance"] for x in por_franja[k]) / len(por_franja[k]))
        out += ["\n## Reglas para el siguiente post",
                f"1. Formato con más alcance hasta hoy: **{mejor_tipo}**. Dale más espacio en el calendario.",
                f"2. Horario con más alcance: **{mejor_franja}**. Programa ahí lo más importante.",
                "3. Reescribe con un gancho DISTINTO los temas de los 3 peores; repite la estructura de los 3 mejores con otro tema.",
                "4. Si un post tiene alcance pero 0 guardados/compartidos, el gancho funciona pero falta valor: agrega plantilla, checklist o dato útil."]
    open(SALIDA, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
