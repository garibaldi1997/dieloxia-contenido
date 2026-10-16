"""Publicación en LinkedIn (perfil personal o página de empresa).

Usa la API v2 de LinkedIn (ugcPosts + assets), disponible con el producto
"Share on LinkedIn" (scope w_member_social) para perfiles y con
"Community Management API" (w_organization_social) para páginas.
Las imágenes y videos se suben directo desde el repositorio.
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.linkedin.com/v2"


class ErrorLinkedIn(Exception):
    pass


class CuentaLinkedIn:
    def __init__(self, token, organizacion=None):
        self.token = token
        self.organizacion = organizacion  # id numérico de la página; None = perfil personal
        self._autor = None

    def _req(self, metodo, url, cuerpo=None, binario=None, tipo="application/json"):
        datos = binario if binario is not None else (json.dumps(cuerpo).encode() if cuerpo is not None else None)
        req = urllib.request.Request(url, data=datos, method=metodo)
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("X-Restli-Protocol-Version", "2.0.0")
        if datos is not None:
            req.add_header("Content-Type", tipo)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                txt = r.read().decode() or "{}"
                return json.loads(txt), dict(r.headers)
        except urllib.error.HTTPError as e:
            raise ErrorLinkedIn(f"{metodo} {url.split('?')[0]}: {e.code} {e.read().decode(errors='replace')[:400]}") from None

    def autor(self):
        if self._autor is None:
            if self.organizacion:
                self._autor = f"urn:li:organization:{self.organizacion}"
            else:
                info, _ = self._req("GET", f"{API}/userinfo")
                self._autor = f"urn:li:person:{info['sub']}"
                self.nombre = info.get("name", "")
        return self._autor

    def subir(self, ruta, video=False):
        receta = "feedshare-video" if video else "feedshare-image"
        cuerpo = {"registerUploadRequest": {
            "recipes": [f"urn:li:digitalmediaRecipe:{receta}"],
            "owner": self.autor(),
            "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}],
        }}
        r, _ = self._req("POST", f"{API}/assets?action=registerUpload", cuerpo)
        valor = r["value"]
        url = valor["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        with open(ruta, "rb") as f:
            self._req("PUT", url, binario=f.read(), tipo="application/octet-stream")
        asset = valor["asset"]
        if video:  # esperar a que LinkedIn procese el video
            for _ in range(60):
                st, _ = self._req("GET", f"{API}/assets/{asset.split(':')[-1]}")
                estado = (st.get("recipes") or [{}])[0].get("status")
                if estado == "AVAILABLE":
                    break
                if estado in ("PROCESSING_FAILED", "CLIENT_ERROR"):
                    raise ErrorLinkedIn(f"LinkedIn no pudo procesar el video: {estado}")
                time.sleep(5)
        return asset

    def publicar(self, texto, imagenes=(), video=None):
        categoria, media = "NONE", []
        if video:
            categoria, media = "VIDEO", [self.subir(video, video=True)]
        elif imagenes:
            categoria, media = "IMAGE", [self.subir(i) for i in imagenes[:9]]
        cuerpo = {
            "author": self.autor(),
            "lifecycleState": "PUBLISHED",
            "specificContent": {"com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": texto},
                "shareMediaCategory": categoria,
                **({"media": [{"status": "READY", "media": m} for m in media]} if media else {}),
            }},
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }
        r, h = self._req("POST", f"{API}/ugcPosts", cuerpo)
        return r.get("id") or h.get("x-restli-id") or h.get("X-RestLi-Id")

    def borrar(self, post_id):
        self._req("DELETE", f"{API}/ugcPosts/{urllib.parse.quote(post_id, safe='')}")


def texto_linkedin(texto):
    """Adapta el texto de Instagram/Facebook: quita referencias a la bio y deja máximo 5 hashtags."""
    lineas = [l for l in texto.splitlines() if "bio" not in l.lower() or "http" in l]
    t = "\n".join(lineas)
    t = re.sub(r"\(link en nuestra bio\)", "", t, flags=re.I)
    tags = re.findall(r"#\w+", t)
    for extra in tags[5:]:
        t = t.replace(extra, "")
    return re.sub(r"[ \t]+\n", "\n", re.sub(r"\n{3,}", "\n\n", t)).strip()
