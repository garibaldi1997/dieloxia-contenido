#!/usr/bin/env python3
"""Publica en Facebook e Instagram las entradas del calendario cuya hora ya llegó.

Admite varias páginas (cuentas). Cada cuenta se declara en cuentas.json con el
nombre del secreto de GitHub que guarda su token de página.

Usa solo la biblioteca estándar de Python y la API Graph de Meta.

Variables de entorno:
  META_TOKEN_*     Token de página de cada cuenta, con el nombre indicado en cuentas.json.
  GRAPH_VERSION    Versión de la API Graph (por defecto v26.0).
  RAW_BASE         URL pública base de los archivos del repositorio.
  DRY_RUN          "1" para simular sin publicar.

Uso:
  python scripts/publicar.py              # publica lo pendiente
  python scripts/publicar.py --verificar  # comprueba los tokens de todas las cuentas
  python scripts/publicar.py --validar    # revisa calendario e imágenes (sin red)
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linkedin import CuentaLinkedIn, ErrorLinkedIn, texto_linkedin  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALENDARIO = os.path.join(RAIZ, "calendario.json")
CUENTAS = os.path.join(RAIZ, "cuentas.json")
PUBLICADOS = os.path.join(RAIZ, "estado", "publicados.json")
INTENTOS = os.path.join(RAIZ, "estado", "intentos.json")  # intentos fallidos por pieza y red
MAX_INTENTOS = 3
VENTANA_ATRASO = timedelta(hours=36)  # no publicar entradas viejas olvidadas
CUENTA_POR_DEFECTO = "dieloxia"

GRAPH = os.environ.get("GRAPH_BASE", "https://graph.facebook.com") + "/" + os.environ.get("GRAPH_VERSION", "v26.0")
RAW_BASE = os.environ.get("RAW_BASE", "").rstrip("/")
VIDEO_BASE = os.environ.get("VIDEO_BASE", "").rstrip("/")  # CDN que entrega video/mp4 (jsDelivr)
DRY_RUN = os.environ.get("DRY_RUN") == "1"


class ErrorMeta(Exception):
    pass


def api(token, metodo, ruta, **params):
    params["access_token"] = token
    datos = urllib.parse.urlencode(params).encode()
    url = f"{GRAPH}/{ruta}"
    if metodo in ("GET", "DELETE"):
        req = urllib.request.Request(url + "?" + datos.decode(), method=metodo)
    else:
        req = urllib.request.Request(url, data=datos, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode(errors="replace")
        try:
            msg = json.loads(cuerpo)["error"]["message"]
        except Exception:
            msg = cuerpo
        raise ErrorMeta(f"{metodo} {ruta}: {msg}") from None


def url_publica(ruta_rel):
    return f"{RAW_BASE}/{urllib.parse.quote(ruta_rel)}"


def url_video(ruta_rel):
    """URL del video con tipo video/mp4. Prueba la CDN (y la calienta); si falla, usa la URL normal."""
    if VIDEO_BASE:
        url = f"{VIDEO_BASE}/{urllib.parse.quote(ruta_rel)}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=60) as r:
                tipo = r.headers.get("Content-Type", "")
            print(f"  video: {tipo} desde la CDN")
            if tipo.startswith("video/"):
                return url
        except Exception as err:  # noqa: BLE001
            print(f"  ⚠️ CDN no disponible ({err}); uso la URL normal")
    return url_publica(ruta_rel)


# ---------- Cuentas ----------
class Cuenta:
    def __init__(self, nombre, token):
        self.nombre, self.token = nombre, token
        self._datos = None

    def api(self, metodo, ruta, **params):
        return api(self.token, metodo, ruta, **params)

    def datos(self):
        if self._datos is None:
            p = self.api("GET", "me", fields="id,name,instagram_business_account{id,username}")
            ig = p.get("instagram_business_account") or {}
            self._datos = (p["id"], p["name"], ig.get("id"), ig.get("username"))
        return self._datos


def cargar_cuentas():
    config = cargar(CUENTAS, {})
    cuentas = {}
    for nombre, c in config.items():
        token = os.environ.get(c.get("secreto", ""), "").strip()
        li = c.get("linkedin") or {}
        li_token = os.environ.get(li.get("secreto", ""), "").strip()
        if token or li_token:
            cuentas[nombre] = Cuenta(nombre, token)
            cuentas[nombre].li = CuentaLinkedIn(li_token, li.get("organizacion")) if li_token else None
    return config, cuentas


# ---------- Instagram ----------
def ig_esperar(cuenta, contenedor, intentos=30):
    for _ in range(intentos):
        estado = cuenta.api("GET", contenedor, fields="status_code").get("status_code")
        if estado == "FINISHED":
            return
        if estado in ("ERROR", "EXPIRED"):
            raise ErrorMeta(f"Instagram rechazó el contenedor {contenedor}: {estado}")
        time.sleep(4)
    raise ErrorMeta(f"Instagram tardó demasiado en procesar {contenedor}")


def ig_publicar(cuenta, ig_id, entrada):
    tipo, imgs, texto = entrada["tipo"], entrada.get("imagenes", []), entrada.get("texto", "")
    if tipo == "reel":
        c = cuenta.api("POST", f"{ig_id}/media", media_type="REELS", video_url=url_video(entrada["video"]),
                       caption=texto, share_to_feed="true")["id"]
        ig_esperar(cuenta, c, intentos=90)  # el video tarda más en procesarse
        return cuenta.api("POST", f"{ig_id}/media_publish", creation_id=c)["id"]
    if tipo == "historia":
        c = cuenta.api("POST", f"{ig_id}/media", image_url=url_publica(imgs[0]), media_type="STORIES")["id"]
    elif tipo == "carrusel":
        hijos = []
        for img in imgs[:10]:
            h = cuenta.api("POST", f"{ig_id}/media", image_url=url_publica(img), is_carousel_item="true")["id"]
            ig_esperar(cuenta, h)
            hijos.append(h)
        c = cuenta.api("POST", f"{ig_id}/media", media_type="CAROUSEL", children=",".join(hijos), caption=texto)["id"]
    else:
        c = cuenta.api("POST", f"{ig_id}/media", image_url=url_publica(imgs[0]), caption=texto)["id"]
    ig_esperar(cuenta, c)
    return cuenta.api("POST", f"{ig_id}/media_publish", creation_id=c)["id"]


def ig_ya_publicado(cuenta, ig_id, entrada):
    """Busca en las últimas publicaciones de Instagram una con el mismo texto (evita duplicados
    cuando Meta responde con error pero sí publicó)."""
    texto = " ".join((entrada.get("texto") or "").split())[:80]
    if not texto or entrada["tipo"] == "historia":
        return None
    desde = datetime.fromisoformat(entrada["fecha"]) - timedelta(minutes=10)
    try:
        medios = cuenta.api("GET", f"{ig_id}/media", fields="id,caption,timestamp", limit=25).get("data", [])
    except ErrorMeta:
        return None
    for m in medios:
        cap = " ".join((m.get("caption") or "").split())[:80]
        cuando = datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if cap == texto and cuando >= desde:
            return m["id"]
    return None


def fb_ya_publicado(cuenta, page_id, entrada):
    """Igual que ig_ya_publicado, pero en la página de Facebook (evita repetir si dos corridas coinciden)."""
    texto = " ".join((entrada.get("texto") or "").split())[:80]
    if not texto or entrada["tipo"] == "historia":
        return None
    desde = datetime.fromisoformat(entrada["fecha"]) - timedelta(minutes=10)
    try:
        posts = cuenta.api("GET", f"{page_id}/posts", fields="id,message,created_time", limit=25).get("data", [])
    except ErrorMeta:
        return None
    for m in posts:
        msg = " ".join((m.get("message") or "").split())[:80]
        cuando = datetime.strptime(m["created_time"], "%Y-%m-%dT%H:%M:%S%z")
        if msg == texto and cuando >= desde:
            return m["id"]
    return None


# ---------- Facebook ----------
def fb_publicar(cuenta, page_id, entrada):
    tipo, imgs, texto = entrada["tipo"], entrada.get("imagenes", []), entrada.get("texto", "")
    if tipo == "reel":
        return cuenta.api("POST", f"{page_id}/videos", file_url=url_video(entrada["video"]), description=texto)["id"]
    if tipo == "historia":
        foto = cuenta.api("POST", f"{page_id}/photos", url=url_publica(imgs[0]), published="false")["id"]
        return cuenta.api("POST", f"{page_id}/photo_stories", photo_id=foto).get("post_id", foto)
    if len(imgs) == 1:
        return cuenta.api("POST", f"{page_id}/photos", url=url_publica(imgs[0]), caption=texto)["id"]
    adjuntos = {}
    for i, img in enumerate(imgs):
        fid = cuenta.api("POST", f"{page_id}/photos", url=url_publica(img), published="false")["id"]
        adjuntos[f"attached_media[{i}]"] = json.dumps({"media_fbid": fid})
    return cuenta.api("POST", f"{page_id}/feed", message=texto, **adjuntos)["id"]


# ---------- Utilidades ----------
def cargar(ruta, defecto):
    if not os.path.exists(ruta):
        return defecto
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def guardar(ruta, datos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        f.write("\n")


def validar(calendario, config):
    errores = []
    ids = set()
    for e in calendario:
        if e["id"] in ids:
            errores.append(f"id repetido: {e['id']}")
        ids.add(e["id"])
        datetime.fromisoformat(e["fecha"])
        cuenta = e.get("cuenta", CUENTA_POR_DEFECTO)
        if cuenta not in config:
            errores.append(f"{e['id']}: la cuenta '{cuenta}' no está en cuentas.json")
        if e["tipo"] not in ("imagen", "carrusel", "historia", "reel"):
            errores.append(f"{e['id']}: tipo inválido {e['tipo']}")
        if e["tipo"] == "reel":
            v = e.get("video", "")
            if not v.lower().endswith(".mp4") or not os.path.exists(os.path.join(RAIZ, v)):
                errores.append(f"{e['id']}: un reel necesita 'video' con un .mp4 existente")
        for img in e.get("imagenes", []):
            if not os.path.exists(os.path.join(RAIZ, img)):
                errores.append(f"{e['id']}: no existe {img}")
            if not img.lower().endswith((".jpg", ".jpeg")):
                errores.append(f"{e['id']}: Instagram solo acepta JPG ({img})")
        if e["tipo"] == "carrusel" and not 2 <= len(e["imagenes"]) <= 10:
            errores.append(f"{e['id']}: un carrusel lleva de 2 a 10 imágenes")
    return errores


# ---------- Ciclo principal ----------
def main():
    calendario = cargar(CALENDARIO, [])
    config, cuentas = cargar_cuentas()
    errores = validar(calendario, config)
    if errores:
        print("❌ El calendario tiene errores:\n  " + "\n  ".join(errores))
        return 1
    if "--validar" in sys.argv:
        print(f"✅ Calendario válido: {len(calendario)} entradas para {len(config)} cuenta(s).")
        return 0

    if "--verificar" in sys.argv:
        malos = 0
        for nombre, c in config.items():
            if nombre not in cuentas:
                print(f"⏸️ {nombre}: falta el secreto {c['secreto']}")
                malos += 1
                continue
            cu = cuentas[nombre]
            if cu.token:
                try:
                    page_id, page_name, ig_id, ig_user = cu.datos()
                    ig = f"Instagram @{ig_user}" if ig_id else "⚠️ sin Instagram profesional vinculado"
                    print(f"✅ {nombre}: página «{page_name}» · {ig}")
                except ErrorMeta as err:
                    print(f"❌ {nombre}: {err}")
                    malos += 1
            if cu.li:
                try:
                    print(f"✅ {nombre}: LinkedIn {cu.li.autor()} {getattr(cu.li, 'nombre', '')}")
                except ErrorLinkedIn as err:
                    print(f"❌ {nombre} LinkedIn: {err}")
                    malos += 1
        return 1 if malos else 0

    if not cuentas:
        print("⏸️ No hay tokens configurados: no se publica nada (ver README).")
        return 0

    publicados = cargar(PUBLICADOS, {})
    ahora = datetime.now(timezone.utc)
    fallos = 0
    for e in sorted(calendario, key=lambda x: x["fecha"]):
        fecha = datetime.fromisoformat(e["fecha"])
        if fecha > ahora or ahora - fecha > VENTANA_ATRASO:
            continue
        nombre = e.get("cuenta", CUENTA_POR_DEFECTO)
        cuenta = cuentas.get(nombre)
        if not cuenta:
            print(f"⏸️ {e['id']}: la cuenta '{nombre}' aún no tiene token")
            continue
        hecho = publicados.setdefault(e["id"], {})
        for red in e.get("redes", ["instagram", "facebook"]):
            if red in hecho:
                continue
            print(f"→ [{nombre}] {e['id']} en {red} ({e['tipo']}, {len(e.get('imagenes', []))} imagen/es)")
            if DRY_RUN:
                continue
            try:
                if red == "linkedin":
                    if e["tipo"] == "historia":
                        hecho[red] = {"omitido": "LinkedIn no tiene historias"}
                        continue
                    if not cuenta.li:
                        print("  ⏸️ sin token de LinkedIn")
                        continue
                    pid = cuenta.li.publicar(
                        e.get("texto_linkedin") or texto_linkedin(e.get("texto", "")),
                        imagenes=[os.path.join(RAIZ, i) for i in e.get("imagenes", [])],
                        video=os.path.join(RAIZ, e["video"]) if e["tipo"] == "reel" else None)
                    hecho[red] = {"id": pid, "fecha": ahora.isoformat(timespec="seconds")}
                    print(f"  ✅ publicado ({pid})")
                    guardar(PUBLICADOS, publicados)
                    continue
                if not cuenta.token:
                    print("  ⏸️ sin token de Meta")
                    continue
                page_id, _, ig_id, _ = cuenta.datos()
                if red == "instagram":
                    if not ig_id:
                        raise ErrorMeta("sin cuenta de Instagram vinculada")
                    intentos = cargar(INTENTOS, {})
                    clave = f"{e['id']}|instagram"
                    pid = ig_ya_publicado(cuenta, ig_id, e)
                    if pid:
                        print(f"  ℹ️ ya estaba publicado en Instagram ({pid}); no se repite")
                    elif intentos.get(clave, 0) >= MAX_INTENTOS:
                        hecho[red] = {"omitido": f"{MAX_INTENTOS} intentos fallidos; revisar a mano"}
                        guardar(PUBLICADOS, publicados)
                        print(f"  ⛔ {MAX_INTENTOS} intentos fallidos: no se reintenta")
                        continue
                    else:
                        intentos[clave] = intentos.get(clave, 0) + 1
                        guardar(INTENTOS, intentos)
                        try:
                            pid = ig_publicar(cuenta, ig_id, e)
                        except ErrorMeta:
                            time.sleep(20)  # Meta a veces publica aunque responda con error
                            pid = ig_ya_publicado(cuenta, ig_id, e)
                            if not pid:
                                raise
                            print(f"  ℹ️ Meta respondió con error, pero sí se publicó ({pid})")
                else:
                    pid = fb_ya_publicado(cuenta, page_id, e)
                    if pid:
                        print(f"  ℹ️ ya estaba publicado en Facebook ({pid}); no se repite")
                    else:
                        pid = fb_publicar(cuenta, page_id, e)
                hecho[red] = {"id": pid, "fecha": ahora.isoformat(timespec="seconds")}
                print(f"  ✅ publicado ({pid})")
                guardar(PUBLICADOS, publicados)
            except (ErrorMeta, ErrorLinkedIn) as err:
                fallos += 1
                print(f"  ❌ {err}")
        if not hecho:
            publicados.pop(e["id"], None)
    guardar(PUBLICADOS, publicados)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
