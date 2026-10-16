# dieloxia-contenido

Contenido y publicador automático de Dieloxia (Instagram y Facebook), sin Metricool.

## Cómo funciona
- Las imágenes y videos van en carpetas `AAAA-MM-DD/` (por ejemplo `2026-10-16/Dieloxia_2026-10-16_post1.jpg`).
- Cada publicación es una entrada en `calendario.json`. GitHub Actions (`publicar.yml`) revisa cada 15 minutos y publica las que ya llegaron a su hora (hasta 36 h de atraso).
- Lo publicado queda en `estado/publicados.json`, las métricas diarias en `estado/metricas.json` y el panel en `docs/index.html`.
- Secreto necesario en el repo: `META_TOKEN_DIELOXIA` (token de la página Dieloxia, app CheckONOFF Publicador).

## Formato de una entrada
```json
{
  "id": "2026-10-16-post1",
  "cuenta": "dieloxia",
  "fecha": "2026-10-16T10:00:00-06:00",
  "tipo": "imagen",
  "redes": ["instagram", "facebook"],
  "imagenes": ["2026-10-16/Dieloxia_2026-10-16_post1.jpg"],
  "texto": "Caption completo con hashtags al final"
}
```
- `tipo`: `imagen` (1 JPG), `carrusel` (2 a 10 JPG en orden), `historia` (1 JPG 1080x1920, `texto` vacío), `reel` (`"video": "AAAA-MM-DD/archivo.mp4"`, `imagenes` vacío; MP4 de máximo 15 MB).
- Solo JPG para imágenes. `id` único.
- Antes de subir: `python scripts/publicar.py --validar`.

## Comandos
- `publicar.yml` → modo `verificar` comprueba el token; `simular` corre sin publicar.
- `moderar.yml` → buscar, ocultar, borrar o editar publicaciones.
