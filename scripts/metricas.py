#!/usr/bin/env python3
"""Lee el desempeño de cada publicación ya hecha y lo guarda en estado/metricas.json.

Instagram: me gusta y comentarios (y vistas/alcance/guardados si el token lo permite).
Facebook: reacciones, comentarios y veces compartido.

Sirve para aprender qué contenido funciona mejor y ajustar el plan de cada semana.
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publicar as p  # noqa: E402

METRICAS = os.path.join(p.RAIZ, "estado", "metricas.json")
CRECIMIENTO = os.path.join(p.RAIZ, "estado", "crecimiento.json")


def cuenta_metricas(cuenta):
    """Seguidores de la cuenta hoy (para medir el crecimiento día a día)."""
    page_id, _, ig_id, _ = cuenta.datos()
    fila = {}
    if ig_id:
        d = cuenta.api("GET", ig_id, fields="followers_count,media_count")
        fila["ig_seguidores"], fila["ig_publicaciones"] = d.get("followers_count"), d.get("media_count")
    try:
        d = cuenta.api("GET", page_id, fields="followers_count,fan_count")
        fila["fb_seguidores"] = d.get("followers_count") or d.get("fan_count")
    except p.ErrorMeta:
        pass
    return fila


def ig_metricas(cuenta, media_id):
    datos = cuenta.api("GET", media_id, fields="like_count,comments_count,media_product_type,permalink")
    try:
        ins = cuenta.api("GET", f"{media_id}/insights", metric="reach,saved,shares,views")
        for m in ins.get("data", []):
            datos[m["name"]] = m["values"][0]["value"]
    except p.ErrorMeta:
        pass  # sin permiso de estadísticas: nos quedamos con me gusta y comentarios
    if datos.get("media_product_type") == "REELS":  # retención: cuánto ven en promedio cada reel
        try:
            ins = cuenta.api("GET", f"{media_id}/insights", metric="ig_reels_avg_watch_time,ig_reels_video_view_total_time")
            for m in ins.get("data", []):
                datos[m["name"]] = m["values"][0]["value"]  # milisegundos
        except p.ErrorMeta:
            pass
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
            if info.get("borrado") or info.get("omitido") or "id" not in info or str(info.get("id", "")).startswith("bloqueado") or red == "linkedin" or (red == "facebook" and e.get("tipo") == "historia"):
                continue
            try:
                fila[red] = ig_metricas(cuenta, info["id"]) if red == "instagram" else fb_metricas(cuenta, info["id"])
            except p.ErrorMeta as err:
                fila[red] = {"error": str(err)}
        salida["publicaciones"][pid] = fila
        print(pid, json.dumps({k: v for k, v in fila.items() if k in ("instagram", "facebook")}, ensure_ascii=False))
    p.guardar(METRICAS, salida)

    crecimiento = p.cargar(CRECIMIENTO, [])
    hoy = datetime.now(timezone(timedelta(hours=-6))).date().isoformat()  # fecha CDMX
    for nombre, cuenta in cuentas.items():
        if not cuenta.token:
            continue
        try:
            fila = {"fecha": hoy, "cuenta": nombre, **cuenta_metricas(cuenta)}
        except p.ErrorMeta as err:
            print(f"⚠️ {nombre}: no se pudieron leer los seguidores ({err})")
            continue
        crecimiento = [c for c in crecimiento if not (c["fecha"] == hoy and c["cuenta"] == nombre)] + [fila]
        print("Crecimiento:", json.dumps(fila, ensure_ascii=False))
    p.guardar(CRECIMIENTO, crecimiento)
    return 0


if __name__ == "__main__":
    sys.exit(main())
