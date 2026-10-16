#!/usr/bin/env python3
"""Publica en Instagram y Facebook las entradas del calendario cuya hora ya llegó.

Basado en el publicador de checkonoff-contenido, con una diferencia: la rutina
diaria de Dieloxia sube su contenido a ramas `claude/...` (no siempre puede
escribir en main). Por eso, con RAMAS=1 el publicador lee `calendario.json` de
todas las ramas actualizadas en los últimos días y publica cada entrada con la
URL de su propia rama. El registro de lo publicado vive en main.

Usa solo la biblioteca estándar de Python y la API Graph de Meta.

Variables de entorno:
  META_TOKEN_*     Token de página de cada cuenta, con el nombre indicado en cuentas.json.
  GRAPH_VERSION    Versión de la API Graph (por defecto v26.0).
  REPO             owner/repo, para armar las URLs públicas (p. ej. garibaldi1997/dieloxia-contenido).
  RAW_BASE         URL pública base de los archivos del checkout actual (modo sin ramas).
  RAMAS            "1" para leer el calendario de todas las ramas remotas recientes.
  DIAS_RAMAS       Antigüedad máxima (días) de una rama para leer su calendario (por defecto 4).
  DRY_RUN          "1" para simular sin publicar.

Uso:
  python scripts/publicar.py              # publica lo pendiente
  python scripts/publicar.py --verificar  # comprueba los tokens de todas las cuentas
  python scripts/publicar.py --validar    # revisa calendario.json y archivos del checkout (sin red)
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALENDARIO = os.path.join(RAIZ, "calendario.json")
CUENTAS = os.path.join(RAIZ, "cuentas.json")
PUBLICADOS = os.path.join(RAIZ, "estado", "publicados.json")
VENTANA_ATRASO = timedelta(hours=36)  # no publicar entradas viejas olvidadas
CUENTA_POR_DEFECTO = "dieloxia"
TIPOS = ("imagen", "carrusel", "historia", "reel")

GRAPH = os.environ.get("GRAPH_BASE", "https://graph.facebook.com") + "/" + os.environ.get("GRAPH_VERSION", "v26.0")
REPO = os.environ.get("REPO", "")
RAW_BASE = os.environ.get("RAW_BASE", "").rstrip("/")
VIDEO_BASE = os.environ.get("VIDEO_BASE", "").rstrip("/")  # CDN que entrega video/mp4 (jsDelivr)
RAMAS = os.environ.get("RAMAS") == "1"
DIAS_RAMAS = float(os.environ.get("DIAS_RAMAS", "4"))
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


def url_publica(entrada, ruta_rel):
    base = entrada.get("_raw") or RAW_BASE
    return f"{base}/{urllib.parse.quote(ruta_rel)}"


def url_video(entrada, ruta_rel):
    """URL del video con tipo video/mp4. Prueba la CDN (y la calienta); si falla, usa la URL normal."""
    base = entrada.get("_cdn") or VIDEO_BASE
    if base:
        url = f"{base}/{urllib.parse.quote(ruta_rel)}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=60) as r:
                tipo = r.headers.get("Content-Type", "")
            print(f"  video: {tipo} desde la CDN")
            if tipo.startswith("video/"):
                return url
        except Exception as err:  # noqa: BLE001
            print(f"  ⚠️ CDN no disponible ({err}); uso la URL normal")
    return url_publica(entrada, ruta_rel)


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
        if token:
            cuentas[nombre] = Cuenta(nombre, token)
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


def ig_publicar(cuenta, ig_id, e):
    tipo, imgs, texto = e["tipo"], e.get("imagenes", []), e.get("texto", "")
    if tipo == "reel":
        c = cuenta.api("POST", f"{ig_id}/media", media_type="REELS", video_url=url_video(e, e["video"]),
                       caption=texto, share_to_feed="true")["id"]
        ig_esperar(cuenta, c, intentos=90)  # el video tarda más en procesarse
    elif tipo == "historia":
        c = cuenta.api("POST", f"{ig_id}/media", image_url=url_publica(e, imgs[0]), media_type="STORIES")["id"]
        ig_esperar(cuenta, c)
    elif tipo == "carrusel":
        hijos = []
        for img in imgs[:10]:
            h = cuenta.api("POST", f"{ig_id}/media", image_url=url_publica(e, img), is_carousel_item="true")["id"]
            ig_esperar(cuenta, h)
            hijos.append(h)
        c = cuenta.api("POST", f"{ig_id}/media", media_type="CAROUSEL", children=",".join(hijos), caption=texto)["id"]
        ig_esperar(cuenta, c)
    else:
        c = cuenta.api("POST", f"{ig_id}/media", image_url=url_publica(e, imgs[0]), caption=texto)["id"]
        ig_esperar(cuenta, c)
    pid = cuenta.api("POST", f"{ig_id}/media_publish", creation_id=c)["id"]
    comentario = e.get("primer_comentario", "").strip()
    if comentario and tipo != "historia":
        try:
            cuenta.api("POST", f"{pid}/comments", message=comentario)
        except ErrorMeta as err:  # el post ya salió: no lo contamos como fallo
            print(f"  ⚠️ no se pudo poner el primer comentario: {err}")
    return pid


# ---------- Facebook ----------
def fb_publicar(cuenta, page_id, e):
    tipo, imgs = e["tipo"], e.get("imagenes", [])
    texto = e.get("texto_facebook") or e.get("texto", "")
    if tipo == "reel":
        return cuenta.api("POST", f"{page_id}/videos", file_url=url_video(e, e["video"]), description=texto)["id"]
    if tipo == "historia":
        foto = cuenta.api("POST", f"{page_id}/photos", url=url_publica(e, imgs[0]), published="false")["id"]
        return cuenta.api("POST", f"{page_id}/photo_stories", photo_id=foto).get("post_id", foto)
    if len(imgs) == 1:
        return cuenta.api("POST", f"{page_id}/photos", url=url_publica(e, imgs[0]), caption=texto)["id"]
    adjuntos = {}
    for i, img in enumerate(imgs):
        fid = cuenta.api("POST", f"{page_id}/photos", url=url_publica(e, img), published="false")["id"]
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


def git(*args):
    return subprocess.run(["git", "-C", RAIZ, *args], capture_output=True, text=True, check=True).stdout


def errores_entrada(e, config, existe):
    """Lista de problemas de una entrada. `existe(ruta)` dice si el archivo está en su rama."""
    errores = []
    try:
        datetime.fromisoformat(e["fecha"])
    except (KeyError, ValueError):
        errores.append("fecha inválida (usa ISO 8601 con zona, p. ej. 2026-10-20T10:00:00-06:00)")
    if e.get("cuenta", CUENTA_POR_DEFECTO) not in config:
        errores.append(f"la cuenta '{e.get('cuenta')}' no está en cuentas.json")
    tipo = e.get("tipo")
    if tipo not in TIPOS:
        errores.append(f"tipo inválido {tipo}")
    if tipo == "reel":
        v = e.get("video", "")
        if not v.lower().endswith(".mp4") or not existe(v):
            errores.append("un reel necesita 'video' con un .mp4 existente")
    else:
        imgs = e.get("imagenes", [])
        if not imgs:
            errores.append("faltan 'imagenes'")
        for img in imgs:
            if not img.lower().endswith((".jpg", ".jpeg")):
                errores.append(f"Instagram solo acepta JPG ({img})")
            elif not existe(img):
                errores.append(f"no existe {img}")
        if tipo == "carrusel" and not 2 <= len(imgs) <= 10:
            errores.append("un carrusel lleva de 2 a 10 imágenes")
    return errores


def validar_local(calendario, config):
    errores, ids = [], set()
    for e in calendario:
        if e.get("id") in ids:
            errores.append(f"id repetido: {e.get('id')}")
        ids.add(e.get("id"))
        errores += [f"{e.get('id')}: {m}" for m in errores_entrada(e, config, lambda r: os.path.exists(os.path.join(RAIZ, r)))]
    return errores


def entradas_de_ramas(config):
    """Junta las entradas de calendario.json de todas las ramas remotas recientes."""
    salida = git("for-each-ref", "refs/remotes/origin",
                 "--format=%(refname:short) %(objectname) %(committerdate:unix)")
    limite = time.time() - DIAS_RAMAS * 86400
    entradas, vistas = [], set()
    for linea in sorted(salida.splitlines(), key=lambda l: l.split()[0] != "origin/main"):  # main primero
        rama, sha, fecha = linea.split()
        if rama.endswith("/HEAD") or int(fecha) < limite:
            continue
        try:
            cal = json.loads(git("show", f"{sha}:calendario.json"))
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        archivos = None
        for e in cal:
            if not isinstance(e, dict) or e.get("id") in vistas:
                continue
            if archivos is None:
                archivos = set(git("ls-tree", "-r", "--name-only", sha).splitlines())
            problemas = errores_entrada(e, config, lambda r, a=archivos: r in a)
            if problemas:
                print(f"⚠️ {rama} · {e.get('id')}: se omite ({'; '.join(problemas)})")
                continue
            vistas.add(e["id"])
            e["_rama"] = rama
            e["_raw"] = f"https://raw.githubusercontent.com/{REPO}/{sha}"
            e["_cdn"] = f"https://cdn.jsdelivr.net/gh/{REPO}@{sha}"
            entradas.append(e)
    return entradas


# ---------- Ciclo principal ----------
def main():
    config, cuentas = cargar_cuentas()

    if "--validar" in sys.argv:
        calendario = cargar(CALENDARIO, [])
        errores = validar_local(calendario, config)
        if errores:
            print("❌ El calendario tiene errores:\n  " + "\n  ".join(errores))
            return 1
        print(f"✅ Calendario válido: {len(calendario)} entradas para {len(config)} cuenta(s).")
        return 0

    if "--verificar" in sys.argv:
        malos = 0
        for nombre, c in config.items():
            if nombre not in cuentas:
                print(f"⏸️ {nombre}: falta el secreto {c['secreto']}")
                malos += 1
                continue
            try:
                _, page_name, ig_id, ig_user = cuentas[nombre].datos()
                ig = f"Instagram @{ig_user}" if ig_id else "⚠️ sin Instagram profesional vinculado"
                print(f"✅ {nombre}: página «{page_name}» · {ig}")
            except ErrorMeta as err:
                print(f"❌ {nombre}: {err}")
                malos += 1
        return 1 if malos else 0

    if RAMAS:
        calendario = entradas_de_ramas(config)
    else:
        calendario = cargar(CALENDARIO, [])
        errores = validar_local(calendario, config)
        if errores:
            print("❌ El calendario tiene errores:\n  " + "\n  ".join(errores))
            return 1
    print(f"📅 {len(calendario)} entradas en el calendario.")

    if not cuentas:
        print("⏸️ No hay tokens configurados: no se publica nada (ver README).")
        return 0

    publicados = cargar(PUBLICADOS, {})
    ahora = datetime.now(timezone.utc)
    fallos = 0
    for e in sorted(calendario, key=lambda x: datetime.fromisoformat(x["fecha"])):
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
            print(f"→ [{nombre}] {e['id']} en {red} ({e['tipo']}) desde {e.get('_rama', 'checkout')}")
            if DRY_RUN:
                continue
            try:
                page_id, _, ig_id, _ = cuenta.datos()
                if red == "instagram":
                    if not ig_id:
                        raise ErrorMeta("sin cuenta de Instagram vinculada")
                    pid = ig_publicar(cuenta, ig_id, e)
                elif red == "facebook":
                    pid = fb_publicar(cuenta, page_id, e)
                else:
                    hecho[red] = {"omitido": f"red no soportada: {red}"}
                    continue
                hecho[red] = {"id": pid, "fecha": ahora.isoformat(timespec="seconds")}
                print(f"  ✅ publicado ({pid})")
                guardar(PUBLICADOS, publicados)
            except ErrorMeta as err:
                fallos += 1
                print(f"  ❌ {err}")
        if not hecho:
            publicados.pop(e["id"], None)
    guardar(PUBLICADOS, publicados)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
