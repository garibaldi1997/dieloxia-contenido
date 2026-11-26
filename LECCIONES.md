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

## 2026-11-14 · Cuidados técnicos (plantilla de historia y fotos de comida)
- Unsplash no tiene fotos de barbacoa (solo tacos al pastor): elige el giro DESPUÉS de ver qué fotos hay, o regenera la voz con el giro que sí tiene fotos (hoy barbacoa → taquería; la voz nueva tardó ~1 min).
- Plantilla reutilizable de reel con historia: un `historia.js` genérico + `cfg.js` por reel (tiempos de la voz, fotos, notificaciones, lista de chats, chat y cierre) arma un reel en minutos con 7 efectos; los ganchos (`glassY`/`txtY` ≈ 960/1170) van abajo cuando la cara de la foto está arriba.
- Fotos horizontales en reels: mueve el encuadre con `x0` (p. ej. 78) para que la cara no se pierda al recortar a vertical.
- Cuatro renders en paralelo de ~29 s tardaron ~15 min. Un reel que se pasa de 30 s por décimas se recorta con `ffmpeg -t 29.95 -c copy`.

## 2026-11-15 · Métricas y cuidados técnicos
- Métricas al 14/11: lo que más alcanzó en la semana fueron los reels de la TARDE-NOCHE (estética viernes 18:00 = 30; "Hoy a las 12 de la noche arranca el Buen Fin" jueves 18:00 = 15). Los reels de historia de las 10:00 y 12:00 del 12–14/11 quedaron en 1–4, y las imágenes de las 11:00 en 0. Hoy: reel de historia nocturno a las 18:00, posts de imagen fuera de las 11:00 (13:00 y 20:00) y un formato en tendencia de polarización ("🚩 o 🟢") a las 16:00.
- Guiones de ~110 palabras salieron de 41–44 s con Edge: escribe los guiones de reel en ~90–95 palabras (≈34–37 s → SPEED 1.2–1.25). Para regenerar, usa un nombre NUEVO (la acción solo genera los .mp3 que faltan) y borra el guion viejo.
- `fotos.py revisar` rechazó 3 candidatas del post (Omar Lopez, Vitaly Gariev, Carlos de Almeida ya usados): busca en estado/fotos_usadas.json con `grep -i "<fotógrafo>"` antes de bajar la foto en grande.

## 2026-11-16 · Reporte semanal y cuidados técnicos
- Semana 9–14/11 (Instagram): reels 24 piezas = 160 de alcance y 193 vistas; carruseles 6 = 9; imágenes 12 = 6. 0 guardados y 0 compartidos en todo. Seguidores: 5 (+0 en la semana).
- Voz: los reels con voz de hombre (Jorge) promediaron 4.5 s de visualización y 103 de alcance en 11 reels; los de mujer (Dalia) 1.5 s y 57 en 13. Se sigue alternando (regla del dueño), pero los reels de los picos (12:00 y 18:00) van con Jorge.
- Lo mejor de la semana: historias de tienda/servicio a las 12:00 y 18:00 con hora + giro + problema (ferretería 33, estética 34, pizzería 19). Lo peor: imágenes de las 11:00 (0). Se dejan las imágenes en 14:00 y 20:00.
- Plantilla genérica de reel con historia ya en el repo: `plantillas/reel_historia/historia.js` + `cfg.js` (ver README ahí). Con ella los 3 reels de historia se arman en minutos; lo lento es el render (4 en paralelo ≈ 30 min).
- `estado/fotos_usadas.json` va con `indent=2`; si lo reescribes con `indent=1` (como `fotos.py usar`) el diff cambia todo el archivo.

## 2026-11-17 · Métricas y cuidados técnicos
- Métricas al 16/11: el mejor reciente fue el reel de historia de la panadería del domingo a las 10:00 (alcance 39) y la ferretería del sábado a las 12:00 (33). Los posts de imagen y los carruseles siguen en 0–2. Del 16/11 solo hay datos del mismo día (celulares 12:00 = 9). Seguidores: 5, sin cambio.
- El Buen Fin 2026 va del 13 al 17/11, así que hoy es el último día. Antes de escribir "hoy/mañana termina", revisa las fechas oficiales del año.
- Fotos de "dueña o dueño de tienda con celular": casi todos los fotógrafos buenos ya salieron en los últimos 30 días (Matthew Jackson, Reza Madani, Vitaly Gariev, Michael Krahn, Omar Lopez, Brooke Cagle…). Busca por giro concreto (barbería, carnicería, fisioterapia) en lugar de "shop owner". Para reels de tips, elige las fotos antes de escribir el guion.
- El reel de tips (sin historia) de hoy dejó solo 2 de 8 escenas con foto. En los reels de tips pon una foto difuminada de fondo también en las escenas del celular, para cumplir la regla de fotos visibles en buena parte del video.
- Un agente dejó vistas previas (`2.jpg`…) en la raíz del repo: antes de cada commit revisa `git status --short` y sube solo `AAAA-MM-DD/`, `calendario.json`, `estado/` y `voz/`.

## 2026-11-18 · Métricas y cuidados técnicos
- Métricas al 17/11: el mejor reel reciente fue la barbería del martes a las 10:00 (alcance 82, 100 vistas, voz Dalia); la carnicería de las 12:00 quedó en 2 y los posts/carrusel en 0. Seguidores: 5, sin cambio. Hoy se repitió el patrón exacto del ganador (día + hora + giro + fila en el primer segundo, 10:00, CTA de comentarios) con el autolavado.
- Guiones de ~100 palabras salieron de 38–40 s con Edge y obligaron a SPEED 1.3–1.36: para quedarse en SPEED ≤1.25 escribe 85–90 palabras.
- En la plantilla `historia.js`, las tarjetas `ok1/ok2` ("Fecha apartada", "Respondido") tapan las burbujas del chat: tres agentes las movieron arriba del celular (y≈270–385). Conviene corregirlas en la plantilla del repo.
- Sesiones de posadas (Wonderhunt) traen niños en primer plano: usa solo las fotos sin menores o difumina el fondo completo.
- Formato en tendencia de la semana: "2026 is the new 2016" (nostalgia con filtros rosados). Se adaptó como "2016 vs. 2026 en el WhatsApp de tu negocio".

## 2026-11-19 · Métricas y cuidados técnicos
- Métricas al 18/11: el mejor de la semana sigue siendo la barbería del martes 10:00 (alcance 100, 114 vistas, Dalia) y el reel del Buen Fin del lunes 16:00 (40). El 18/11 solo tiene datos del mismo día (autolavado 10:00 = 3; banquetes 12:00 = 0). Imágenes de las 14:00 y 20:00 siguen en 0 → hoy las imágenes van a las 13:00 y 15:00. Seguidores: 5, sin cambio.
- Hoy se repitió el patrón del ganador ("Es jueves, 10 de la mañana, y tu florería ya está llena de nochebuenas", Dalia, CTA de comentarios) y se probó el formato en tendencia "Cosas que simplemente tienen sentido" (lista de 5) a las 16:00.
- La plantilla `historia.js` ya trae las tarjetas ok1/ok2 arriba del celular (y=270 y 385): los 3 agentes de hoy tuvieron que moverlas a mano.
- Guiones de 96–103 palabras con Edge = 35–39 s → SPEED 1.2–1.3 y renders de 30.2–30.4 s. Recortar con `-c copy` deja 30.03 s; re-codifica con `-t 29.9` o escribe 85–90 palabras.
- Flujo eficiente: empujar los 4 guiones primero, lanzar 4 agentes con un BRIEF común en el scratchpad (fotógrafos de 30 días en un .txt + `fotos_hoy.txt` compartido) y hacer carrusel/posts mientras renderizan; publicar cada pieza en cuanto está lista (commits parciales a main). Todo listo en ~25 min.
- Floristas latinas con rostro visible casi no hay libres en Unsplash: se usaron nochebuenas en primer plano + florista de espaldas/manos.

## 2026-11-20 · Métricas y cuidados técnicos
- Métricas al 19/11: el mejor reciente fue el taller del jueves a las 12:00 (alcance 33, Jorge); la florería de las 10:00 quedó en 0 y los dos posts (13:00 y 15:00) y el carrusel en 0. El 18/11: banquetes 12:00 = 9; spa 18:00 = 1. Seguidores: 5, sin cambio. Hoy: historias en 10:00 (uñas, Dalia), 12:00 (dental, Jorge) y 18:00 (gimnasio, Jorge); cuenta regresiva del aguinaldo a las 16:00 (patrón del reel del Buen Fin, 40); imágenes en 14:00 y 19:00 (franja sin probar).
- Fecha ancla para diciembre: el aguinaldo se paga a más tardar el 20 de diciembre (art. 87 LFT); el 20/11 faltan 30 días exactos. Sirve para cuentas regresivas.
- La rutina arrancó a las 6:50 CDMX (el reloj del contenedor está en UTC): hay margen para programar el carrusel a las 9:00. Todo quedó listo en ~35 min con 4 agentes en paralelo; guiones de 88–93 palabras quedaron en SPEED 1.25–1.32.
- Para tapar textos de fondo en una foto, un `backdrop-filter` con `mask-image` en degradado se ve natural; los rectángulos de desenfoque con borde duro se notan. Cuida no desenfocar el celular de la persona.

## 2026-11-21 · Métricas y cuidados técnicos
- Métricas al 20/11: el mejor del 19/11 fue el taller de las 12:00 (alcance 103, 116 vistas, 7.2 s de visualización promedio, Jorge); florería 10:00 = 14, hotel 18:00 = 4, "Cosas que tienen sentido" 16:00 = 2. Del 20/11 solo hay datos del mismo día (todo en 0). Carruseles e imágenes siguen en 0. Seguidores: 5, sin cambio. Hoy: el reel del pico de las 12:00 va con Jorge (estética canina) y repite "día + hora + giro + problema"; carrusel con tema nuevo (pedir reseñas por WhatsApp) e imágenes a las 11:00 y 14:00.
- Un agente dejó legible el rótulo de una tienda ("LORDMAUL") con solo velo oscuro: el velo no basta. Revisa cada foto de fondo con un recorte ampliado al 100 % y difumina rótulos con blur ≥ 30 px o sácalos del encuadre.
- Un guion tipo lista de 85 palabras con varias preguntas salió de 40 s con Edge (las preguntas y los dos puntos alargan las pausas) y necesitó SPEED 1.38: para listas escribe 70–75 palabras.
- Flujo de hoy: 4 guiones a main → 4 agentes con BRIEF común → carrusel y posts mientras renderizan → cada pieza a main en cuanto está lista (`add_reel.sh`). Todo programado en ~35 min.

## 2026-11-22 · Métricas y cuidados técnicos
- Métricas al 21/11: el 20/11 ganaron los reels de historia de los extremos del día: gimnasio viernes 18:00 "Es viernes, 9 de la noche, y tu gimnasio ya cerró" (alcance 96, Jorge) y uñas 10:00 (82, 94 vistas, 1 compartido, Dalia). Dental 12:00 = 10; el reel de cuenta regresiva del aguinaldo (16:00) = 0; posts y carrusel = 0. Del 21/11 solo hay datos del mismo día (óptica 10:00 = 3). Seguidores: 5, sin cambio.
- Hoy (domingo): historias en 10:00 (pastelería, Dalia), 12:00 (cafetería, Jorge) y 18:00 nocturna (academia de inglés, Jorge, patrón "ya cerró"); el 16:00 se probó el formato "POV" en lugar de la cuenta regresiva que quedó en 0. Carrusel guardable de 5 etiquetas de WhatsApp Business (recurso útil: comenta ETIQUETAS) y posts en 14:00 (editorial con foto) y 20:00 (antes/después tipográfico).
- Playwright de `/usr/bin/python3` busca `chromium_headless_shell-1255` y no existe: lanza siempre con `executable_path='/opt/pw-browsers/chromium'`.
- `fotos.py revisar` rechazó la foto de R.D. Smith (ya usada el 17/11 en el reel del Buen Fin): las búsquedas "Latina small business owner phone" devuelven casi siempre fotógrafos ya usados. Funcionó buscar por escena ("metal shutter shop") en lugar de por persona.

## 2026-11-23 · Reporte semanal (16–22/11) y cuidados técnicos
- Semana 16–22/11 (Instagram): reels 26 piezas = 583 de alcance y 682 vistas (3.6× la semana anterior, 160); carruseles 7 = 6; imágenes 13 = 1. Guardados 0 y 1 compartido (uñas). Seguidores: 5 (+0 en la semana, +0 en 2 semanas).
- Reels por hora: 10:00 promedia 33 de alcance (barbería 100, uñas 82), 12:00 = 23 (taller 103), 18:00 = 23 (gimnasio 96, sushi 29) y 16:00 = 10 (solo el Buen Fin pasó de 11). Los formatos sin historia de las 16:00 casi no alcanzan: si la semana siguiente siguen bajo 10, cambiar el 16:00 por un cuarto reel con historia.
- Voz: Dalia 13 reels = 286 de alcance y 6.1 s de visualización promedio (la sube el reel de uñas, 37.8 s); Jorge 13 reels = 297 y 5.1 s. Ya no hay diferencia clara entre voces: se mantiene la alternancia.
- CTA: los 4 mejores reels cerraron con comentarios ("¿…? Te leo") o compartir ("Mándaselo a…"); el recurso útil (comenta PALABRA) en carruseles no generó comentarios. Hoy: carrusel a las 8:00 (prueba de hora; el de las 9:00 quedó en 0 cinco días seguidos).
- Black Friday 2026 en México: viernes 27/11 (Cyber Monday 30/11). Hoy se usó como tema del carrusel y del reel de las 16:00.
- Un agente dejó vistas previas (`2.jpg`…`5.jpg`) otra vez en la raíz del repo: súbelas nunca; usa `git add` con rutas explícitas.

## 2026-11-24 · Métricas y cuidados técnicos
- Métricas al 23/11: lo último completo es del 21/11 (sushi sábado 18:00 = 36, óptica 10:00 = 21) y del 22/11 (pastelería 10:00 = 10; cafetería, POV y academia ≤ 3). Del 23/11 solo hay datos del mismo día (imprenta 12:00 = 1, lo demás 0). El alcance de los reels viene bajando desde el 22/11 y los reels sin historia de las 16:00 siguieron bajo 10 (POV 2, Black Friday 0): se aplicó la regla del 23/11 y hoy los 4 reels son con historia (el de la tarde a las 16:30, Metricool martes 17:00 > 16:00).
- Para refrescar los ganchos se usaron giros nunca usados (estudio de fotografía, farmacia, agencia de viajes) y una variante del mejor reel histórico a las 18:00: "Mientras tú cenabas, cinco negocios le escribieron a tu despacho contable".
- La plantilla `historia.js` deja el último subtítulo de la voz debajo del cierre y repite el CTA o "dieloxia punto com": el agente de farmacia lo ocultó en su copia (subtítulos apagados durante el cierre). Conviene llevar ese cambio a la plantilla del repo.
- Foto de dueña latina con delantal en su negocio: "woman owner bakery apron phone" (página 2) devolvió una libre (Centre for Ageing Better). Recorta rótulos en inglés (neón "Bread") fuera del encuadre.

## 2026-11-25 · Métricas y cuidados técnicos
- Métricas al 24/11: el mejor del 23/11 fue otra vez el reel nocturno "ya cerró" (joyería lunes 18:00 = 48 de alcance, 56 vistas); lavandería 10:00 = 0, imprenta 12:00 = 1, Black Friday 16:00 = 2; imágenes y carrusel en 0. Del 24/11 solo hay datos del mismo día (todo en 0). Seguidores: 5, sin cambio. El patrón "Son las 9 de la noche y tu <giro> ya cerró" a las 18:00 suma 4 aciertos seguidos (gimnasio 96, joyería 48, sushi 36): hoy se repitió con tienda de regalos/canastas navideñas.
- Hoy: carrusel a las 8:30 (8:00 y 9:00 siguen en 0), los 4 reels con historia (boutique 10:00 Dalia, taquería 12:00 Jorge, veterinaria 16:30 Dalia, regalos 18:00 Jorge) y posts en 14:00 (editorial con foto) y 19:30 (plantilla de 3 mensajes para Black Friday, guardable).
- Buena fuente de fotos mexicanas libres: Alex Quezada (Aguascalientes) tiene mercados y tiendas reales; buscar con el filtro `user: alex_quezada`.
- Flujo de hoy: 4 guiones a main → voces en ~1 min → 4 agentes con BRIEF común → carrusel y posts subidos mientras renderizaban; los 4 reels listos en ~11 min. `fotos.py usar` reescribe `estado/fotos_usadas.json` con indent=1: vuelve a guardarlo con indent=2 antes del commit.

## 2026-11-26 · Métricas y cuidados técnicos
- Métricas al 25/11: el alcance de los reels se desplomó desde el 24/11 (fotografía 10:00 = 3; farmacia, agencia de viajes y despacho contable = 1, incluida la variante nocturna "Mientras tú cenabas" a las 18:00). Del 25/11 solo hay datos del mismo día (boutique 1, lo demás 0). El último acierto fue la joyería "ya cerró" del 23/11 (62). Seguidores: 5, sin cambio. Si el 26–27/11 los reels siguen en ≤3, revisar en Instagram "Estado de la cuenta" (posible limitación de alcance) y probar un reel sin plantilla de historia (formato en tendencia "small text zoom", Later 30/10).
- Hoy: giros nunca usados (yoga 10:00 Dalia, electrónica con Black Friday 12:00 Jorge, taller de bicicletas 16:30 Dalia, estudio de maquillaje "ya cerró" 18:00 Jorge); carrusel nuevo de "5 estados de WhatsApp que venden en diciembre" a las 8:45; posts a las 11:00 (pantalla de bloqueo con notificaciones del Black Friday) y 14:30 (mito vs. realidad con foto).
- Un agente entregó el reel con UNA sola foto (no encontró vendedor latino de electrónica libre): pide la 2.ª foto desde el brief como "cliente con celular" si el protagonista escasea. Los agentes a veces dejan textos como "(precio de ejemplo)" dentro del chat o una palabra sola en el gancho: revisa la tira de cuadros antes de subir.
- Los agentes deben conservar `frames/` hasta que la sesión principal apruebe el reel: uno lo borró y tuvo que repetir el render completo para corregir solo el gancho.
