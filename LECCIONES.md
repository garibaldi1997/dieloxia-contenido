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

## 2026-10-25 · Pantallas con marca en las fotos
- Si una foto de Unsplash muestra una app o marca de terceros en la pantalla del celular (p. ej. "Copilot"), difumínala con un recorte `clip-path` + `backdrop-filter:blur` sobre la pantalla antes de usarla. En reels, las fotos de fondo van con velo oscuro y desenfoque donde hay pantallas.
- Los reels con historia se arman con `plantillas/efectos/efectos.js` + los ayudantes de `plantillas/reel_historia/rlib.js` (foto con Ken Burns, notificaciones, chat, lista de chats, cierre con logo) y subtítulos a `y:1330` para respetar la zona segura inferior.

## 2026-10-26 · Qué funcionó según las métricas
- Los mejores reels de la semana siguen siendo los de historia con hora + negocio + problema en el primer segundo: "Mientras tú dormías…" (126 de alcance) y "Es sábado por la mañana y tu gimnasio está lleno" (119). Carruseles y posts de imagen siguen en 1–2.
- Aplicar: los 4 reels diarios con voz en off y el gancho de hora/cifra en el segundo 0 (hoy: "Es lunes, 8 de la mañana… 37 mensajes sin leer", ferretería 9:00 y veterinaria 4:00); imágenes y carrusel solo como apoyo.
- Técnico: al anclar escenas con `FX.at(W, 'mito', n)` recuerda que las palabras de 4+ letras comparan por prefijo ("mito" también coincide con "mitos"); cuenta bien la ocurrencia.

## 2026-10-27 · Cuidados técnicos de la rutina
- Antes de elegir giro o nombre de guion revisa `ls voz/` y `calendario.json`: un guion nuevo con el nombre de uno viejo (p. ej. `historia-floreria`) deja el audio anterior, porque la acción solo genera los `.mp3` que faltan. Usa nombres nuevos (`historia-<giro>`).
- La acción "Generar voz de reels" solo corre con push a `main` (la rama `claude/…` no la dispara): empuja los guiones `voz/*.txt` a `main` primero y espera ~1 min.
- En el entorno de nube usa `/usr/bin/python3` (trae Pillow, numpy y edge-tts); instala Playwright para ese Python con `pip install --break-system-packages playwright` (el Chromium ya está en `/opt/pw-browsers/chromium`). Un reel de ~30 s tarda ~5 min en renderizar: lanza los renders en segundo plano y en serie.
- Con `SPEED 1.2` los reels con voz quedan en ~27–30 s (el guion de ~33 s a velocidad normal).

## 2026-10-28 · Cuidados técnicos (cierre y fotos)
- En `plantillas/reel_historia/rlib.js` el título del cierre no heredaba color y salía NEGRO sobre fondo oscuro (ilegible); ya lleva `color:#fff`. Al armar un cierre propio, revisa siempre un cuadro de los últimos 2 s.
- `scripts/fotos.py usar` rechaza la 2.ª foto del mismo fotógrafo aunque sea de la MISMA pieza; registra la 2.ª a mano en `estado/fotos_usadas.json` (huella con `fotos.huella`).
- Para corregir solo el final de un reel sin repetir 8 min de render: copia `make_reel.py` con un `START` de cuadro inicial (los cuadros anteriores en `frames/` se conservan) y vuelve a codificar.
- Con la voz de Edge, `SPEED 1.2–1.25` deja los guiones de ~35–37 s en ~29–30 s.

## 2026-11-02 · Cuidados técnicos (nombres de voz y fotos)
- Antes de nombrar un guion de voz, revisa `ls voz/ | grep <nombre>`: `reel-cuenta` ya existía y su .txt se sobrescribió (hubo que restaurarlo). Usa nombres nuevos y únicos.
- `scripts/fotos.py usar` ya detecta fotógrafo repetido en 30 días y fotos idénticas (p. ej. una foto usada en `reel-mitos`): corre `usar` ANTES de renderizar, no después, para no tener que re-renderizar escenas.
- En el efecto `glassType`, textos de más de ~6 letras con size 230 se cortan en los bordes: usa ≤5 caracteres o baja el tamaño. En `headlineWall` mantén frases cortas (≤18 caracteres con size 62).
- Los días 29/10–01/11 no hay entradas en calendario.json (la rutina no corrió); hoy se retomó la cuota.

## 2026-11-03 · Cuidados técnicos (anclas de voz y render)
- `FX.at(W, 'palabra')` compara en minúsculas: escribe SIEMPRE la palabra ancla en minúsculas ('dieloxia', no 'Dieloxia') o devuelve 0 y la escena sale mal.
- Si una palabra ancla no existe en el guion (p. ej. 'sigues'), `at` devuelve 0 y una escena tapa todo el video: revisa un cuadro cada ~5 s con ffmpeg antes de publicar.
- Cuatro renders en paralelo en 4 núcleos tardan ~25 min; con un solo render un reel de 30 s tarda ~8 min. Lanza los renders apenas existan guion y fotos.
- El logo oficial vive en la rama claude/fervent-ramanujan-pql9o2 (assets/logo.png).

## 2026-11-04 · Cuidados técnicos (lista de chats, anclas y pip)
- `lista()` de `rlib.js` heredaba el color blanco de `.fx` y los nombres de los chats salían invisibles; ya lleva `color:#0d1b1e`. Las tarjetas de `nt()` ahora van con fondo sólido (`#12332f`) para no verse translúcidas sobre el celular. Evita emojis en el título de esas tarjetas.
- `FX.at(W,'con')` coincide con la PRIMERA "con" del guion (palabras ≤3 letras comparan exacto): ancla con una palabra única ("dieloxia"). `at(W,'contesta')` también coincide con "contestar"; usa el índice `n` y revisa un cuadro por escena antes del render largo. `cuatro` en un guion que empieza con "Cuatro…" necesita n=1.
- En la nube: `/usr/bin/python3 -m pip install --break-system-packages playwright` (el `pip` suelto es de otro Python). `make_reel.py` pide la ruta ABSOLUTA del logo.
- Para corregir una escena sin repetir todo el render: renderiza solo el rango de cuadros (copia de make_reel con `F0,F1`) y vuelve a codificar; 120 cuadros tardan ~15 s.
- El contenedor de la rutina rinde 4 reels de ~30 s en paralelo en ~8 min; `estado/fotos_usadas.json` es el registro real de fotos (content_log.json de Drive quedó sin uso desde el 8/10).

## 2026-11-05 · Cuidados técnicos (agentes en paralelo y nombres de voz)
- Al lanzar un agente por reel, dale un guion nuevo con nombre ÚNICO: `reel-control-humano.txt` ya existía y se sobrescribió (se restauró del historial). Haz `ls voz | grep <nombre>` antes de escribir.
- La acción de voz puede fallar por conflicto de rebase si dos pushes caen seguidos a `main`: espera a que termine la primera antes del segundo push o dispara `voz.yml` con workflow_dispatch.
- `fotos.py revisar` rechaza fotos de la misma sesión de un fotógrafo usada en 30 días (veterinaria 26/10): busca la sesión de otro fotógrafo desde el inicio.
- Un guion de ~36 s necesita SPEED 1.25 para quedar ≤30 s; uno de ~27 s a 1.2 queda en ~23 s.
- Los agentes de reel no deben correr `fotos.py usar` (carrera en estado/fotos_usadas.json): registra tú todas las fotos al final.

## 2026-11-06 · Cuidados técnicos (fotos y agentes)
- `scripts/fotos.py` fallaba con `ValueError` si una entrada de `estado/fotos_usadas.json` tenía `huella` vacía (registros manuales); ya se ignora la huella vacía.
- Con `/usr/bin/python3` instala `edge-tts` solo si hay DNS a speech.platform.bing.com; en la nube no hay: la voz se genera empujando `voz/*.txt` a `main` (la acción tarda ~1 min).
- Dos agentes buscando fotos a la vez funcionaron bien con consultas distintas; el registro de fotos lo hace la sesión principal al final con `fotos.huella`. Los reels con guion de ~38 s necesitan SPEED 1.3–1.35 para quedar ≤30 s.
- Las búsquedas de Unsplash devuelven pocas personas latinas: la foto del post se eligió por fotógrafo libre en 30 días; prueba con «Mexico» + giro.

## 2026-11-07 · Cuidados técnicos (fotógrafo repetido y tarjetas sobre rostros)
- `fotos.py revisar` solo se acuerda de lo ya registrado: dos piezas del MISMO día pueden usar al mismo fotógrafo si nadie registra entre una y otra (post y reel con Rodrigo Rodrigues). Antes de elegir la foto del post, revisa los fotógrafos que usaron los agentes de reel.
- Las tarjetas de `uiWorld` ("Tomar el control") tapaban los ojos de la foto de fondo: colócalas en y≥1000 cuando el rostro ocupa el centro.
- Para re-renderizar un rango de cuadros: copia `make_reel.py` con `ts = range(F0, F1)` y nombra `f{i+F0:04d}.jpg`; luego re-codifica con el ffmpeg del final del script (en la nube Playwright de `/usr/bin/python3` requiere `executable_path='/opt/pw-browsers/chromium'`).
- Las búsquedas de Unsplash devuelven ~15k tokens con per_page=12: usa per_page≤4.

## 2026-11-09 · Cuidados técnicos (fotos entre agentes y búsqueda)
- Dos agentes de reel del mismo día eligieron la MISMA foto (tienda de Anaclara Vardiero) y el post eligió otra que luego usó un reel (Reza Madani): `fotos.py revisar` no lo detecta hasta que alguien registra. Pide a cada agente que anote el id Unsplash elegido en un archivo común (`scratchpad/w/fotos_hoy.txt`) y que lo consulte antes de bajar fotos; el post se elige DESPUÉS de los reels.
- Las búsquedas de Unsplash con per_page 3–4 cuestan ~8k tokens y devuelven pocos mexicanos; los términos "market stall"/"Mexico City" dan fotos de otros países (rechaza las de rótulos en inglés). Mejor: giro concreto + "México" (p. ej. memelera, abarrotes, florería).
- Si no hay foto adecuada, el post va tipográfico y se anota en el resumen; los reels llevan las fotos.

## 2026-11-11 · Métricas y cuidados técnicos
- Métricas al 10/11: los reels con historia del 9 y 10/11 (laboratorio, contador, taller, gimnasio) quedaron en alcance 0; lo mejor de esos días fue el carrusel (alcance 2) y el reel "Faltan 4 días para el Buen Fin" (alcance 2). Hoy se probó un formato distinto en tendencia ("Expectativa vs. realidad") y se repitió la estructura del mejor reel histórico ("Mientras tú dormías", de noche) a las 18:00. Si siguen en 0, revisar si la cuenta está limitada (Estado de la cuenta en Instagram) antes de seguir con 4 reels diarios.
- Mueblería y escenas nocturnas casi no tienen fotos de personas latinas libres en Unsplash: usa sala de exhibición + manos/persona de espaldas, y deja la foto con persona latina para otro reel del día.
- Un script `sheet.sh` (7 cuadros: 0.5 s, cada 1/6 y final) en una sola tira basta para revisar cada reel con Read.

## 2026-11-12 · Métricas y cuidados técnicos
- `estado/metricas.json` y `aprendizajes.md` no se actualizan desde el 10/11 a las 14:36 (no hay datos del 11/11). Sin error de token en el archivo; revisar que la acción `metricas.yml` siga corriendo.
- Hoy se movió un reel de historia a las 10:00 (zapatería) y otro a las 12:00 (cafetería), y se repitió el patrón nocturno del mejor reel ("Hoy a las 12 de la noche arranca el Buen Fin") a las 18:00.
- En los guiones de voz escribe la pregunta tal cual ("¿Precio?"), nunca "signo de interrogación": Edge lo lee literal.
- Los agentes de reel pueden agregar promesas que no están en el guion ("sin riesgo de bloqueo"): revisa todas las tarjetas de texto antes de publicar y usa frases verificables ("Conectado con Meta").
- Mientras `pip install playwright` termina para `/usr/bin/python3` (tarda minutos), el carrusel y los posts se pueden renderizar ya con el Playwright de Node (`require('playwright')`).

## 2026-11-13 · Métricas y cuidados técnicos
- `metricas.yml` corre a diario ~20:40 UTC, pero el 12/11 midió los posts el MISMO día (todos en 0) y la corrida del 11/11 se quedó en "queued": el "mejor post de ayer" se debe leer con los datos de hace 2 días. Último dato útil: 11/11 reel de pastelería 10:00 (alcance 13); peor, imagen 11:00 "¿Contestas el WhatsApp?" (0).
- Hoy (viernes, primer día del Buen Fin) se repitió el patrón del mejor reel histórico (viernes 18:00, "Mientras tú dormías") con la historia nocturna de la estética a las 18:00, y los dos reels de historia en los picos 10:00 y 12:00 (Metricool: 10:00 = 6734, el más alto del viernes).
- Guiones de ~45 s obligan a SPEED 1.55 y la voz se oye acelerada: escribe los guiones de reel en 220–240 palabras como máximo (≈35–38 s) para quedarse en SPEED 1.3.
- Unsplash casi no devuelve dueños de negocio latinos con celular: sirvió "shop owner checking phone counter" (recorta el rótulo en inglés antes de usar la foto) y el post tipográfico de línea de tiempo (minuto 0 → 2 horas) salió sin foto.
- El registro de fotos de varios agentes se hace al final desde la sesión principal escribiendo directo en `estado/fotos_usadas.json` con `fotos.huella` (así se aceptan 2–3 fotos del mismo fotógrafo de la misma pieza); comprobando antes que no choquen con registros de días anteriores.
- LinkedIn sigue SIN token en el repo (`cuentas.json` solo tiene META_TOKEN_DIELOXIA): los `texto_linkedin` quedan listos en el calendario pero nadie los publica.
