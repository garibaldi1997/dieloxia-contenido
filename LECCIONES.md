# Lecciones aprendidas · Dieloxia

Reglas obligatorias que salen de la retroalimentación de Garibaldi y de las métricas.
Las rutinas las leen ANTES de crear contenido. Cada lección nueva se agrega aquí con su fecha.

## 2026-10-23 · Qué funcionó según las métricas
- El mejor post de ayer fue el reel de las 10:00 (fonda, voz de hombre, cierre "Mándaselo a quien…"): alcance 54, 62 vistas y el primer compartido. Los carruseles y posts de imagen siguen en alcance 1–2.
- Aplicar: el reel de las 10:00 con una lista/pregunta clara y cierre de compartir; los reels con estructura de lista numerada o pregunta directa; no depender de posts de imagen para alcance (sirven como apoyo).

## 2026-10-23 · Fotos: nunca repetir
El dueño: "Veo que hay fotos que repites; nadie debe ser el mismo, o al menos un personaje ocasional."

- Ninguna foto se repite (ni en Dieloxia ni respecto a lo ya publicado). La misma persona o sesión de fotos solo vuelve como personaje ocasional, máximo 1 vez cada 30 días.
- Antes de usar cada foto de Unsplash: `python scripts/fotos.py revisar foto.jpg --fotografo "<autor>"` (detecta la misma foto aunque cambie el nombre o el recorte) y revisa también los unsplash_ids de content_log.json. Al usarla: `python scripts/fotos.py usar foto.jpg <id-pieza> --unsplash <id> --fotografo "<autor>"`. Registro en `estado/fotos_usadas.json`, que se sube con cada commit.
- El script no reconoce a la misma persona en OTRA foto: compara visualmente (hoja de contacto + Read) con las fotos de los últimos 30 días y evita dos fotos del mismo fotógrafo en 30 días.
- Busca con términos variados (giro + ciudad + edad + situación) y elige personas distintas a las de los últimos días.

## 2026-10-23 · Público: los negocios; más reels con historia; sin historias
El dueño: "Todo el contenido va dirigido a las empresas, no a los empleados." Métricas al 23/10: los reels traen 108 de 157 de alcance (el mejor: "Son las 2 de la tarde y tu fonda está llena", 54); imágenes y carruseles ~1; historias 0.

- Todo se dirige al DUEÑO o encargado del negocio (cómo vende más, pierde menos clientes, ahorra tiempo); nunca a sus clientes ni a sus empleados.
- Cuota diaria nueva: 4 REELS (al menos 2 con historia de un giro concreto, con la hora y el problema en el primer segundo, estilo "Son las 2 de la tarde y tu fonda está llena") + 1 CARRUSEL + 2 POSTS de imagen. HISTORIAS PAUSADAS hasta 100 seguidores.
- Los reels van en las franjas con más alcance (mañana 10:00 y mediodía 12:00 rinden más hasta hoy).

## 2026-10-22 · Voz: nunca la del dueño, alternar mujer y hombre
El dueño: "Ya no uses mi voz, se escucha feo. Usa mejor cualquier otra, variable entre hombre y mujer."

- PROHIBIDO usar la voz del dueño o el repo garibaldi-voz.
- Voz de Edge (acción "Generar voz de reels"): `#voz es-MX-DaliaNeural +4%` (mujer) o `#voz es-MX-JorgeNeural +4%` (hombre), alternando: nunca la misma voz en dos reels seguidos.
- En el guion, siglas escritas como se dicen ("inteligencia artificial", "recursos humanos").

## 2026-10-22 · Efectos en todos los reels
El dueño compartió el video "10 efectos de video con Claude" y pidió usarlos siempre.

- Todos los reels usan `plantillas/efectos/efectos.js` con el tema de Dieloxia: `FX.tema({bg:'#0d1b1e', bg2:'#06402b', a:'#00b35c', a2:'#2fd4b4'})`.
- Mínimo 4 efectos distintos por reel (orbit, frame break, UI world, digital zoom, phone mockup con chat de WhatsApp, headline wall, zoom through, chart grow, doodle boil, glass type), cambio de escena cada 2–4 s, voz de Edge alternando mujer/hombre y subtítulos palabra por palabra.
- Se combinan con la regla de fotos reales: las fotos van de fondo en escenas con `uiWorld`/`phone` encima. Detalle en `plantillas/efectos/README.md`.

## 2026-10-21 · Solo el negocio, nunca la persona
El dueño: "No hables nada de mí nunca, solo hablaremos de los negocios."

- Ningún post, imagen, reel ni voz en off menciona al dueño: sin nombre, sin "soy el doctor…", sin su foto ni su cargo.
- Los cierres hablan de Dieloxia y de lo que resuelve.

## 2026-10-16 · No usar "Escríbenos BOT" en todo
Garibaldi: "A todos los post le pones Escríbenos BOT. Esto no es muy atractivo."

- PROHIBIDO "Escríbenos BOT", "Escribe BOT", "Manda BOT" o "BOT por DM", en el texto y en las imágenes.
- Un solo llamado a la acción por pieza, natural y con beneficio claro. Rótalos; no repitas el mismo CTA dos veces seguidas en el día:
  - **Guardar o compartir:** "Guárdalo para tu próximo cierre de ventas", "Mándaselo a quien contesta WhatsApp en tu negocio".
  - **Conversación:** una pregunta fácil de contestar en comentarios, por ejemplo "¿En cuánto contestas hoy un mensaje? Te leo 👇".
  - **Seguir:** "Sígueme para más ideas de atención por WhatsApp".
  - **Recurso útil (máximo 1 de cada 4 piezas):** "Comenta PLANTILLA y te mando los 5 mensajes listos para copiar". La palabra describe lo que la persona recibe, nunca "BOT".
  - **Sitio, suave:** "Mira cómo funciona en dieloxia.com". Solo en piezas de producto, como cierre secundario.
- En historias: "Responde esta historia", "Ver el reel en el perfil", "Vota en los comentarios del post" o solo el logo con dieloxia.com.
- En reels: el cierre invita a guardar, comentar o ver el siguiente video, no a escribir una palabra clave.
- Primero valor y luego venta: la mayoría de las piezas no deben vender.

## 2026-10-19 · Nunca el logo en la parte superior
Garibaldi: "Siempre pones el logo en la parte superior, eso se ve feo."

- PROHIBIDO poner el logo arriba (encabezado, esquina superior o barra superior) en posts, carruseles, historias y reels.
- En el feed: logo pequeño abajo, o solo en la última lámina.
- En reels: sin logo durante el video; el logo va solo en el cierre.
- En historias: logo pequeño abajo, respetando la zona segura inferior.

## 2026-10-19 · Reels con historia, como la competencia
Garibaldi compartió un reel de la competencia como referencia: "así son los reels". Desde hoy, al menos 1 de los 3 reels diarios sigue este formato:

- **Historia de 25–30 s de un negocio concreto** (consultorio, estética, taller, restaurante…) con un mismo protagonista: fotos de la MISMA sesión de Unsplash (mismo fotógrafo y lugar).
- **Voz en off en español de México** + subtítulos palabra por palabra al centro (la palabra que se dice cambia a #2fd4b4, texto blanco con contorno oscuro). La voz se genera gratis: escribe el guion en `voz/<nombre>.txt`, haz push y la acción "Generar voz de reels" deja `voz/<nombre>.mp3` y `voz/<nombre>.json` (tiempos por palabra) en unos 30 s.
- **Estructura:** 1) el dueño ocupado con las manos en su trabajo, 2) reloj en pantalla que avanza y notificaciones que se acumulan (precios, horarios, citas), 3) lista de chats cuando por fin contesta: "dos ya agendaron en otro lado", 4) efecto de rebobinar ⏪ al mismo momento, 5) "Ahora, con tu asistente": cada mensaje respondido al instante y etiquetas de "Cita agendada", 6) el dueño termina su trabajo tranquilo + control humano en 1 clic, 7) cierre con logo al centro y un CTA natural.
- Música original suave + sonido en cada notificación + whoosh en el rebobinado; la música baja cuando habla la voz.
- Difumina nombres bordados, gafetes o marcas reales que aparezcan en las fotos.
- Referencia hecha: `2026-10-19/Dieloxia_2026-10-19_reel_historia_dentista.mp4`.

## 2026-10-19 · Varía el tipo de negocio en cada reel con historia
Garibaldi: "variable los videos para todo tipo de negocio".
- Cada reel con historia es de un giro distinto; no repitas giro en 7 días. Rotación sugerida: consultorio dental, estética/barbería, taller mecánico, taquería/restaurante, veterinaria, boutique de ropa, inmobiliaria, gimnasio, escuela/academia, ferretería, florería, hotel/hostal, abogado/contador, laboratorio clínico, tienda de celulares, pastelería.
- Ajusta el guion al dolor real del giro (citas, cotizaciones, pedidos, apartados, horarios, precios) y usa fotos de la misma sesión para el protagonista.
- Herramientas listas en `plantillas/reel_historia/` (render, música y ejemplo).
