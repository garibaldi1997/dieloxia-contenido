#!/usr/bin/env python3
"""Lee el desempeño de cada publicación ya hecha y lo guarda en estado/metricas.json.

Instagram: me gusta y comentarios (y vistas/alcance/guardados si el token lo permite).
Facebook: reacciones, comentarios y veces compartido.

Sirve para aprender qué contenido funciona mejor y ajustar el plan de cada semana.
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publicar as p  # noqa: E402

METRICAS = os.path.join(p.RAIZ, "estado", "metricas.json")


def ig_metricas(cuenta, media_id):
    datos = cuenta.api("GET", media_id, fields="like_count,comments_count,media_product_type,permalink")
    try:
        ins = cuenta.api("GET", f"{media_id}/insights", metric="reach,saved,shares,views")
        for m in ins.get("data", []):
            datos[m["name"]] = m["values"][0]["value"]
    except p.ErrorMeta:
        pass  # sin permiso de estadísticas: nos quedamos con me gusta y comentarios
    return datos


def fb_metricas(cuenta, post_id):
    # Las fotos sueltas no tienen "shares"; los posts sí. Probamos de más a menos campos.
    for campos in ("shares,reactions.summary(true).limit(0),comments.summary(true).limit(0),permalink_url",
                   "reactions.summary(true).limit(0),comments.summary(true).limit(0)",
                   "likes.summary(true).limit(0),comments.summary(true).limit(0),permalink_url",  # videos
                   "likes.summary(true).limit(0),comments.summary(true).limit(0),link"):  # fotos
        try:
            d = cuenta.api("GET", post_id, fields=campos)
            return {
                "reacciones": (d.get("reactions") or d.get("likes") or {}).get("summary", {}).get("total_count", 0),
                "comentarios": d.get("comments", {}).get("summary", {}).get("total_count", 0),
                "compartidos": d.get("shares", {}).get("count", 0),
                "permalink": d.get("permalink_url") or d.get("link"),
            }
        except p.ErrorMeta as err:
            ultimo = err
    if "pages_read_user_content" in str(ultimo):
        return {"pendiente": "agregar el permiso pages_read_user_content en la app de Meta"}
    raise ultimo


def main():
    calendario = {e["id"]: e for e in p.cargar(p.CALENDARIO, [])}
    publicados = p.cargar(p.PUBLICADOS, {})
    _, cuentas = p.cargar_cuentas()
    salida = {"actualizado": datetime.now(timezone.utc).isoformat(timespec="seconds"), "publicaciones": {}}
    for pid, redes in publicados.items():
        e = calendario.get(pid, {})
        cuenta = cuentas.get(e.get("cuenta", p.CUENTA_POR_DEFECTO))
        if not cuenta:
            continue
        fila = {"tipo": e.get("tipo"), "fecha": e.get("fecha"), "tema": (e.get("texto") or "").split("\n")[0][:90]}
        for red, info in redes.items():
            if info.get("borrado") or red == "linkedin":
                continue
            try:
                fila[red] = ig_metricas(cuenta, info["id"]) if red == "instagram" else fb_metricas(cuenta, info["id"])
            except p.ErrorMeta as err:
                fila[red] = {"error": str(err)}
        salida["publicaciones"][pid] = fila
        print(pid, json.dumps({k: v for k, v in fila.items() if k in ("instagram", "facebook")}, ensure_ascii=False))
    p.guardar(METRICAS, salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
