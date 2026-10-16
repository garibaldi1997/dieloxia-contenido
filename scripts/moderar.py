#!/usr/bin/env python3
"""Busca, oculta o borra publicaciones ya hechas (Facebook e Instagram).

Uso:
  python scripts/moderar.py buscar "texto"        # lista publicaciones que contienen el texto
  python scripts/moderar.py ocultar "texto o id"  # oculta en Facebook (Instagram no permite ocultar por API)
  python scripts/moderar.py borrar "id"           # borra; acepta el id del calendario o el id de Meta
  python scripts/moderar.py editar "id"           # cambia el texto de un post de Facebook por el de TEXTO

La cuenta se toma de CUENTA (por defecto dieloxia).
"""
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publicar as p  # noqa: E402


def buscar(cuenta, texto):
    page_id, _, ig_id, _ = cuenta.datos()
    texto = texto.lower()
    hallados = []
    for post in cuenta.api("GET", f"{page_id}/posts", fields="id,message,created_time,permalink_url", limit=100).get("data", []):
        if texto in (post.get("message") or "").lower():
            hallados.append(("facebook", post["id"], post.get("created_time"), post.get("permalink_url"), post.get("message")))
    if ig_id:
        for m in cuenta.api("GET", f"{ig_id}/media", fields="id,caption,timestamp,permalink", limit=100).get("data", []):
            if texto in (m.get("caption") or "").lower():
                hallados.append(("instagram", m["id"], m.get("timestamp"), m.get("permalink"), m.get("caption")))
    for red, mid, fecha, link, msg in hallados:
        print(f"• {red} {mid} ({fecha}) {link}\n    {(msg or '').splitlines()[0][:100]}")
    if not hallados:
        print("No encontré publicaciones con ese texto.")
    return hallados


def main():
    accion, objetivo = sys.argv[1], sys.argv[2].strip()
    _, cuentas = p.cargar_cuentas()
    cuenta = cuentas.get(os.environ.get("CUENTA", p.CUENTA_POR_DEFECTO))
    if not cuenta:
        print("⏸️ Falta el token de la cuenta.")
        return 1
    if accion == "buscar":
        buscar(cuenta, objetivo)
        return 0

    publicados = p.cargar(p.PUBLICADOS, {})
    if objetivo in publicados:  # id del calendario: actúa sobre todas sus redes
        blancos = [(red, info["id"], info) for red, info in publicados[objetivo].items()]
    elif objetivo.replace("_", "").isdigit():
        blancos = [("facebook" if "_" in objetivo else "?", objetivo, None)]
    else:  # texto: busca primero
        blancos = [(red, mid, None) for red, mid, *_ in buscar(cuenta, objetivo)]

    fallos = 0
    ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for red, mid, info in blancos:
        try:
            if accion == "ocultar":
                if red == "instagram":
                    print(f"⚠️ {mid}: Instagram no permite ocultar por API; archívalo desde la app.")
                    continue
                cuenta.api("POST", mid, is_hidden="true")
                print(f"🙈 oculto en Facebook: {mid}")
            elif accion == "editar":
                if red == "instagram":
                    print(f"⚠️ {mid}: Instagram no permite editar el texto por API; edítalo desde la app.")
                    continue
                cuenta.api("POST", mid, message=os.environ["TEXTO"])
                print(f"✏️ texto actualizado en Facebook: {mid}")
            elif accion == "borrar":
                cuenta.api("DELETE", mid)
                print(f"🗑️ borrado en {red}: {mid}")
                if info is not None:
                    info["borrado"] = ahora
            else:
                print(f"Acción desconocida: {accion}")
                return 1
        except p.ErrorMeta as err:
            fallos += 1
            print(f"❌ {red} {mid}: {err}")
    p.guardar(p.PUBLICADOS, publicados)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
