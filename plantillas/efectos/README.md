# Efectos para reels (estándar obligatorio desde el 22/10/2026)

`efectos.js` trae los 10 efectos de la referencia, listos para `render(t)`, más un fondo vivo, grano y subtítulos palabra por palabra:

| # | Efecto | Función | Úsalo para |
|---|---|---|---|
| 1 | Orbit | `FX.orbit` | la marca o el producto al centro, beneficios girando |
| 2 | Frame break | `FX.frameBreak` | algo que "se sale" del marco (cierre, revelación) |
| 3 | UI world | `FX.uiWorld` | tarjetas de interfaz flotando alrededor |
| 4 | Digital zoom | `FX.digitalZoom` | cifras que suben con golpe de zoom (multas, %, $) |
| 5 | Phone mockup | `FX.phone` | la app o WhatsApp funcionando en un celular |
| 6 | Headline wall | `FX.headlineWall` | titulares que caen y se apilan |
| 7 | Zoom through | `FX.zoomThrough` | transición entre escenas atravesando un anillo |
| 8 | Chart grow | `FX.chartGrow` | gráficas que crecen con un contador |
| 9 | Doodle boil | `FX.doodle` | garabato a mano alrededor de una pregunta o "¡WOW!" |
| 10 | Glass type | `FX.glassType` | número o palabra gancho en cristal 3D |

Reglas:
- Cada reel usa **al menos 4 efectos distintos** y cambia de escena cada 2–4 s, sincronizado con la voz (`FX.at(W, 'palabra')`).
- Gancho en el segundo 0 con `glassType`, `digitalZoom` o `headlineWall`. Subtítulos con `FX.subtitulos` y `FX.grano` al final.
- Voz de Edge alternando mujer (es-MX-DaliaNeural) y hombre (es-MX-JorgeNeural); nunca la voz del dueño. Nunca hablar del dueño. Nunca logo arriba: el logo va al centro en `orbit`/`frameBreak` o en el cierre.
- Colores: CheckONOFF es el tema por defecto. Dieloxia: `FX.tema({bg:'#0d1b1e', bg2:'#06402b', a:'#00b35c', a2:'#2fd4b4'})`.

Cómo armar uno: copia `ejemplo_registro_2027.html` como `reel.html` en una carpeta con `efectos.js`, `voz.mp3` y `voz.json`, ajusta las escenas y corre `plantillas/reel_historia/make_reel.py <carpeta> <carpeta>/voz 1.0 <logo.png>` (con `bed.py` para música y sonidos).
