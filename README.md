# dieloxia-contenido

Contenido de Dieloxia y publicación automática **gratis** en **Instagram** y **Facebook** con la API oficial de Meta (sin Metricool).

- `cuentas.json` → la página que maneja el sistema y el nombre del secreto con su token.
- `calendario.json` → qué se publica, cuándo (hora de Ciudad de México) y con qué texto.
- `AAAA-MM-DD/` → las imágenes (JPG) y videos (MP4) de cada día.
- `.github/workflows/publicar.yml` → GitHub Actions revisa el calendario cada 15 minutos y publica lo que toque.
- `estado/publicados.json` → registro de lo ya publicado (evita duplicados).

Tipos de publicación: `imagen`, `carrusel` (2 a 10 imágenes), `historia` y `reel`.

**Ramas de contenido:** la rutina diaria a veces no puede escribir en `main` y sube su contenido a ramas `claude/...`. El publicador lee `calendario.json` de **todas las ramas actualizadas en los últimos 4 días** (y de `main`) y publica cada entrada con los archivos de su propia rama. No hace falta fusionar nada.

---

## Configuración única (≈15 minutos)

> Solo se hace una vez. Meta exige que la persona dueña de la página autorice el acceso.

### 1. Requisitos
- Instagram @dieloxia como **cuenta profesional** (Empresa o Creador).
- Instagram **vinculado a la página de Facebook** de Dieloxia.

### 2. App de Meta
Si ya tienes la app de Meta que usas para CheckONOFF, **usa esa misma**: no hace falta otra. Si no:
1. Entra a <https://developers.facebook.com> → **Mis apps** → **Crear app**.
2. Elige los casos de uso para **administrar una página** y **publicar contenido en Instagram**.
3. Déjala en **modo desarrollo**: así publica en tus propias cuentas sin revisión de Meta.

### 3. Obtener el token de la página de Dieloxia
1. Abre el **Explorador de la API Graph**: <https://developers.facebook.com/tools/explorer>
2. Elige tu app → **Obtener token de usuario** con los permisos:
   `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`, `business_management`
3. **Generate Access Token** → al aceptar, **marca la página de Dieloxia y su Instagram** (además de las que ya tengas).
4. Copia el token, ábrelo en el **Depurador de tokens**: <https://developers.facebook.com/tools/debug/accesstoken> → **Ampliar token de acceso** → copia el token largo.
5. En el Explorador pega el token largo y consulta `me/accounts`.
6. Busca la página **Dieloxia** en la respuesta y copia su `access_token`: ese es el **token de página** (por lo general no caduca).

### 4. Guardarlo en GitHub
En **este** repositorio (dieloxia-contenido): **Settings → Secrets and variables → Actions → New repository secret**
- Nombre: `META_TOKEN_DIELOXIA`
- Valor: el token de página de Dieloxia

No lo pegues en ningún chat.

### 5. Probar
**Actions → Publicar en redes → Run workflow** → modo `verificar`.
Debe decir `✅ dieloxia: página «Dieloxia» · Instagram @dieloxia`. Desde ese momento se publica solo.

---

## Formato del calendario

```json
{
  "id": "2026-10-20-errores-whatsapp",
  "fecha": "2026-10-20T10:00:00-06:00",
  "tipo": "carrusel",
  "redes": ["instagram", "facebook"],
  "imagenes": ["2026-10-20/Dieloxia_2026-10-20_carrusel_slide1.jpg", "2026-10-20/Dieloxia_2026-10-20_carrusel_slide2.jpg"],
  "texto": "Texto de Instagram",
  "primer_comentario": "#WhatsAppBusiness #SanLuisPotosi #Dieloxia",
  "texto_facebook": "Texto de Facebook (opcional; si falta se usa 'texto')"
}
```

Para un reel: `"tipo": "reel"` y `"video": "2026-10-20/Dieloxia_2026-10-20_reel1.mp4"` (sin `imagenes`). Para una historia: `"tipo": "historia"` con una sola imagen y sin texto.

## Notas
- Instagram solo acepta **JPG** por API. El flujo `Validar calendario` revisa formato, rutas y número de imágenes en cada push.
- Las historias por API no admiten stickers de enlace, encuesta ni música: el llamado a la acción va dentro de la imagen.
- Las entradas con más de 36 horas de atraso no se publican (para no saturar el feed si algo falló).
- Si la API de Meta cambia de versión, crea la variable `GRAPH_VERSION` (Settings → Variables) con la versión nueva, p. ej. `v27.0`.
- Basado en el publicador de `checkonoff-contenido`.
