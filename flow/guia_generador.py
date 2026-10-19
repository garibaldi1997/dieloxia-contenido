"""Genera las guías PDF de Flow (Dieloxia y CheckONOFF) con imagen inicial y prompts por escena."""
import base64, html, pathlib
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
NEG = "No on-screen text, no subtitles, no captions, no logos, no brand names, no readable phone screens, no music, no dialogue. Ambient sound only."
STYLE = "Vertical 9:16, photorealistic, natural documentary look, shot on a modern phone-style cinema camera, shallow depth of field, warm natural light, subtle handheld movement, real Mexican setting."

def b64(p): return 'data:image/jpeg;base64,' + base64.b64encode((D / p).read_bytes()).decode()

REELS = {
 'dieloxia': {
  'marca': 'Dieloxia', 'color': '#06402b', 'acento': '#2fd4b4',
  'reels': [
   {'id': 'D1', 'titulo': 'Taquería · "Doña Lupe"', 'img': 'D1_taqueria_imagen_inicial.jpg', 'voz': 'flow-taqueria.mp3',
    'personaje': 'Doña Lupe: Mexican woman, about 50, warm brown skin, dark hair in a low bun with a few grey strands, small gold earrings, short-sleeve navy blouse, black apron with pockets, black nitrile gloves. Busy street taquería at night in central Mexico: steel griddle (plancha), trompo of al pastor, clay salsa bowls, string lights, customers queuing on the sidewalk.',
    'escenas': [
     ('0–4 s', 'Frames to Video · imagen inicial D1', 'Close-up of gloved hands quickly flipping tortillas and chopping al pastor on a hot steel griddle at a busy night taquería, steam and sizzling, string lights and a line of customers blurred in the background. Fast, energetic rhythm, camera slowly pushes in.', 'Viernes, siete de la noche. Tienes la plancha llena y la fila hasta la banqueta.', 'Reloj: 7:02 pm', 'Chisporroteo de la plancha'),
     ('4–9 s', 'Ingredients to Video · personaje Doña Lupe', 'A smartphone lying face-up on the counter between salsa bowls lights up and vibrates again and again; the screen is out of focus and unreadable. In the background Doña Lupe keeps cooking, glancing at the phone without being able to pick it up.', 'Y el WhatsApp no para: ¿hacen pedidos para llevar? ¿cuánto la orden de pastor? ¿llegan a la colonia Jardín?', 'Encima: notificaciones (pantalla de bloqueo) · Reloj 7:15 → 7:40 pm', 'Ding en cada notificación'),
     ('9–13 s', 'Ingredients to Video · personaje Doña Lupe', 'Later in the night, the taquería is calmer. Doña Lupe takes off one glove, picks up the phone, reads, and her face falls into a disappointed sigh. Medium close-up, soft warm light.', 'Cuando por fin contestas… ya pidieron en otro lado.', 'Corte a: lista de chats "ya pedimos en otro lado" · Reloj 9:05 pm', 'Silencio corto + suspiro'),
     ('13–14 s', 'Edición (sin IA)', '—', '(pausa)', 'Efecto rebobinar ⏪ con glitch verde #2fd4b4 · Reloj vuelve a 7:02 pm', 'Whoosh de rebobinado'),
     ('14–21 s', 'Frames to Video · último cuadro de la escena 1', 'Same moment at 7 pm: the phone on the counter lights up, and this time a soft green glow pulses around it as if answered instantly. Doña Lupe smiles, nods and keeps cooking without stopping. Camera dollies from the phone to her face.', 'Ahora, con tu asistente de Dieloxia: toma el pedido, manda el menú y confirma la dirección al momento.', 'Encima: chat respondido por "Asistente con IA" + lista con "Pedido confirmado"', 'Pops suaves de mensaje enviado'),
     ('21–27 s', 'Ingredients to Video · personaje Doña Lupe', 'Doña Lupe hands a paper bag of tacos to a delivery rider at the counter, then laughs with customers eating at the street tables. Warm, happy, golden light. Slow motion at the end.', 'Tú sigues en la plancha. Y si quieres, tomas el control en un clic. Guárdalo si tienes taquería.', 'Tarjeta "Tomar el control · 1 clic" + cierre con logo al centro y dieloxia.com', 'Música sube al final'),
    ]},
   {'id': 'D2', 'titulo': 'Veterinaria · "Dr. Andrés"', 'img': 'D2_veterinaria_imagen_inicial.jpg', 'voz': 'flow-veterinaria.mp3',
    'personaje': 'Dr. Andrés: Latino man, early 30s, short light-brown hair, clean-shaven, white veterinary coat over a light shirt, calm and kind. Small bright veterinary clinic in Mexico: stainless steel exam table, white walls, a black-and-tan dachshund patient, a front desk with a phone.',
    'escenas': [
     ('0–4 s', 'Frames to Video · imagen inicial D2', 'Dr. Andrés gently holds a black-and-tan dachshund on a steel exam table, checking its paw with gloved hands; the dog looks at the camera. Bright clean clinic light, camera slowly pushes in.', 'Estás con un perrito en consulta y no puedes soltarlo.', 'Reloj: 10:02 am', 'Ladrido suave, ambiente de clínica'),
     ('4–9 s', 'Ingredients to Video · personaje Dr. Andrés', 'On the reception desk, a smartphone lights up and buzzes repeatedly, screen blurred and unreadable. In the background Dr. Andrés keeps examining the dog and glances at the phone, unable to answer.', 'Y te escriben: ¿tienen vacunas? ¿cuánto cuesta la estética? ¿abren el domingo?', 'Encima: notificaciones · Reloj 10:15 → 11:05 am', 'Ding en cada notificación'),
     ('9–13 s', 'Ingredients to Video · personaje Dr. Andrés', 'After the consultation, Dr. Andrés takes off his gloves, picks up the phone, reads and rubs his forehead, disappointed. Medium close-up.', 'Para cuando contestas, dos ya se fueron a otra veterinaria.', 'Corte a: lista de chats con 2 perdidos en rojo · Reloj 1:10 pm', 'Silencio corto'),
     ('13–14 s', 'Edición (sin IA)', '—', '(pausa)', 'Rebobinar ⏪ · Reloj vuelve a 10:02 am', 'Whoosh'),
     ('14–21 s', 'Frames to Video · último cuadro de la escena 1', 'Same moment at 10 am: the phone on the desk lights up with a soft green pulse as messages get answered instantly, while Dr. Andrés keeps calmly treating the dachshund and smiles. Rack focus from phone to doctor.', 'Ahora, con tu asistente de Dieloxia: responde precios, horarios y agenda la cita al momento.', 'Encima: chat "¡Claro! Vacunas desde $___, ¿te agendo el sábado 10:00?" + "Cita agendada"', 'Pops de mensaje'),
     ('21–27 s', 'Ingredients to Video · personaje Dr. Andrés', 'Dr. Andrés hands the happy dachshund back to its smiling owner at the front desk; the dog wags its tail. Warm, joyful ending, slight slow motion.', 'Tú sigues con tu paciente. Y si es urgencia, tomas el control en un clic. Guárdalo si tienes veterinaria.', '"Tomar el control · 1 clic" + cierre con logo', 'Música sube'),
    ]},
   {'id': 'D3', 'titulo': 'Frutería / puesto de mercado · "Doña Carmen"', 'img': 'D3_fruteria_imagen_inicial.jpg', 'voz': 'flow-fruteria.mp3',
    'personaje': 'Doña Carmen: Mexican woman, about 55, light-brown skin, dark hair pulled back, blue sleeveless apron over a beige long-sleeve top, friendly face. Colorful fruit and vegetable stall in a Mexican market: crates of potatoes, cucumbers, cabbages, avocados, hanging bags, morning light.',
    'escenas': [
     ('0–4 s', 'Frames to Video · imagen inicial D3', 'Doña Carmen sips coffee at her market stall at 7 am, then quickly starts weighing vegetables for a customer on a hanging scale; bustling market, morning light, camera slowly pushes in.', 'Siete de la mañana y ya hay clientes en el puesto.', 'Reloj: 7:00 am', 'Ambiente de mercado'),
     ('4–9 s', 'Ingredients to Video · personaje Doña Carmen', 'A smartphone resting on a crate of avocados lights up and buzzes again and again, screen blurred. Doña Carmen is busy bagging tomatoes for customers and cannot pick it up.', 'Mientras despachas, te llegan pedidos por WhatsApp: un kilo de aguacate, tres de jitomate… ¿a qué hora entregan?', 'Encima: notificaciones de pedidos · Reloj 7:20 → 8:10 am', 'Ding en cada notificación'),
     ('9–13 s', 'Ingredients to Video · personaje Doña Carmen', 'Mid-morning, the stall is calm. Doña Carmen wipes her hands on her apron, reads the phone and shakes her head with a resigned smile.', 'Cuando por fin contestas, ya compraron en el súper.', 'Corte a: chats "ya compré en el súper, gracias" · Reloj 10:30 am', 'Silencio corto'),
     ('13–14 s', 'Edición (sin IA)', '—', '(pausa)', 'Rebobinar ⏪ · Reloj vuelve a 7:00 am', 'Whoosh'),
     ('14–21 s', 'Frames to Video · último cuadro de la escena 1', 'Same morning moment: the phone on the avocados lights up with a soft green pulse as orders get confirmed, while Doña Carmen keeps serving customers and smiles at the phone.', 'Ahora, con tu asistente de Dieloxia: toma el pedido completo, confirma la hora de entrega y te lo deja listo.', 'Encima: chat con pedido resumido + "Entrega 11:00 ✅"', 'Pops'),
     ('21–27 s', 'Ingredients to Video · personaje Doña Carmen', 'Doña Carmen hands two full bags of fruit to a delivery boy on a bicycle, waves goodbye and laughs with a neighbor. Bright, happy market morning, slow motion.', 'Tú sigues despachando. Y si quieres, tomas el control en un clic. Guárdalo si vendes por WhatsApp.', 'Cierre con logo + dieloxia.com', 'Música sube'),
    ]},
  ]},
 'checkonoff': {
  'marca': 'CheckONOFF', 'color': '#111C3B', 'acento': '#7DD818',
  'reels': [
   {'id': 'C1', 'titulo': 'RRHH cierra la quincena · "Mariana"', 'img': 'C1_rrhh_quincena_imagen_inicial.jpg', 'voz': 'rrhh-quincena.mp3',
    'personaje': 'Mariana: young Latina HR analyst, about 28, dark skin, black hair in a low bun, white button-up blouse, black trousers, laptop and phone. Bright modern café-style office with wooden benches and a coffee mural.',
    'escenas': [
     ('0–3 s', 'Frames to Video · imagen inicial C1', 'Mariana sits at a wooden table with her laptop, talking on the phone, looking stressed and taking notes. Afternoon light, camera slowly pushes in.', 'Es jueves de quincena y tienes tres sucursales.', 'Reloj: Jueves 15 · 4:30 pm · chips "Sucursal Centro/Norte/Sur"', 'Ambiente oficina'),
     ('3–10 s', 'Ingredients to Video · personaje Mariana', 'Close-up of Mariana scrolling on her phone, frowning at photos of handwritten paper attendance lists; then she switches to a messy spreadsheet on her laptop and rubs her temples. Screens are blurred and unreadable.', 'Te llegan fotos de listas en papel… un Excel que se llama FINAL siete… y cuarenta mensajes de: ¿quién faltó?', 'Encima: lista en papel, Excel "FINAL_v7" y "40 sin leer" (pantallas de CheckONOFF ya hechas)', 'Ding en cada mensaje'),
     ('10–13 s', 'Ingredients to Video · personaje Mariana', 'Night: the office is dark except for the laptop glow on Mariana\'s tired face; she leans back and exhales, still on the phone. Cold blue light.', 'Son las diez de la noche y la nómina sigue sin cuadrar.', 'Reloj: 10:00 pm', 'Silencio, tic-tac'),
     ('13–14 s', 'Edición (sin IA)', '—', '(pausa)', 'Rebobinar ⏪ con glitch verde lima · Reloj vuelve a 4:30 pm', 'Whoosh'),
     ('14–25 s', 'Ingredients to Video · empleado operativo (otro personaje)', 'A young Mexican factory worker in a navy polo arrives at work in the morning and taps his phone to check in, smiling; a quick cut shows a fingerprint time clock on a wall being used. Bright morning light.', 'Ahora, con CheckONOFF: tu equipo checa desde su celular, por WhatsApp o en su checador, con ubicación y foto. Faltas, retardos y horas extra se calculan solos.', 'Encima: tarjeta "Entrada registrada ✅ 8:58" + tablero con Falta/Retardo/Extra', 'Pops'),
     ('25–32 s', 'Ingredients to Video · personaje Mariana', 'Mariana clicks one button on her laptop, smiles widely, closes the laptop at 6 pm and laughs, relaxed, grabbing her bag to go home. Warm golden light.', 'Y la prenómina sale en un clic. Tú cierras la quincena a las seis… y te vas a tu casa. Guárdalo si eres de recursos humanos.', 'Botón "Pre-nómina lista ✅" · Reloj 6:00 pm · cierre con logo al centro', 'Música sube'),
    ]},
   {'id': 'C2', 'titulo': 'Taller de costura · "Supervisora Rosa"', 'img': 'C2_maquila_imagen_inicial.jpg', 'voz': 'flow-maquila.mp3',
    'personaje': 'Rosa: Mexican woman, about 45, medium-brown skin, dark hair tied back, burgundy short-sleeve top, jeans, reading glasses on her head. Small garment workshop (maquila) in Mexico: industrial sewing machines, piles of denim, cinder-block walls, a standing fan, a paper sign-in sheet on a clipboard by the door.',
    'escenas': [
     ('0–4 s', 'Frames to Video · imagen inicial C2', 'Rosa works at an industrial sewing machine in a small garment workshop at 7 am, then looks up at the door as workers start arriving. Natural daylight, gentle push-in.', 'Siete de la mañana en el taller. ¿Quién llegó? ¿Quién checó por quién?', 'Reloj: 7:00 am', 'Máquinas de coser'),
     ('4–8 s', 'Ingredients to Video · personaje Rosa', 'Close-up of a paper sign-in sheet on a clipboard where two workers quickly scribble names and times; one signs for a friend who is not there. Rosa frowns while holding the clipboard.', 'La lista de papel dice una cosa… y la nómina, otra.', 'Encima: lista en papel con nombres tachados', 'Pluma sobre papel'),
     ('8–11 s', 'Ingredients to Video · personaje Rosa', 'Friday afternoon, Rosa sits at a small desk with a calculator and the clipboard, unsure, scratching her head over the overtime hours.', 'Y el viernes, las horas extra se pagan a ojo.', 'Reloj: Viernes 5:30 pm · "Horas extra: ¿?"', 'Calculadora'),
     ('11–12 s', 'Edición (sin IA)', '—', '(pausa)', 'Rebobinar ⏪ · Reloj vuelve a 7:00 am', 'Whoosh'),
     ('12–22 s', 'Ingredients to Video · trabajadora del taller', 'A young Mexican seamstress arrives at the workshop door and takes a quick selfie-style check-in with her phone, smiling; outside there is no signal, but she continues inside. Bright morning light.', 'Ahora, con CheckONOFF: cada persona checa con foto y ubicación, aunque no haya internet. Retardos, faltas y horas extra se calculan solos.', 'Encima: "Entrada ✅ 6:58 · 📍 Taller · 📸" + "Sin señal: se guarda y se sube sola" + tablero', 'Pops'),
     ('22–30 s', 'Ingredients to Video · personaje Rosa', 'Rosa checks the attendance on her phone while standing among the sewing machines, nods satisfied and smiles at her team, who wave back. Warm, happy light, slow motion.', 'Y tú tienes la asistencia real en tu celular. Guárdalo si tienes personal operativo.', 'Cierre con logo al centro + "Prueba 14 días gratis · checkonoff.mx"', 'Música sube'),
    ]},
  ]},
}

PASOS = """<ol>
<li>Entra a <b>labs.google/flow</b>, crea un proyecto nuevo y en ajustes elige <b>formato vertical 9:16</b> y el modelo <b>Veo 3 Fast</b> (gasta menos créditos; usa Veo 3 Quality solo para la escena final).</li>
<li><b>Escena 1:</b> modo <b>Frames to Video</b>, sube la <b>imagen inicial</b> de este documento y pega el prompt.</li>
<li><b>Personaje:</b> en <b>Ingredients to Video</b> sube la imagen inicial (o el mejor cuadro de la escena 1) como referencia y pega antes de cada prompt la <b>descripción del personaje</b>. Así se mantiene la misma persona en todas las escenas.</li>
<li>Pega siempre al final del prompt la línea de <b>reglas</b> (sin texto, sin logos, sin música). Los textos y pantallas los ponemos en edición porque la IA los escribe mal.</li>
<li>Genera 2 versiones por escena y quédate con la mejor. Si una sale rara, cambia una sola cosa del prompt y vuelve a generar.</li>
<li>Descarga los clips y en <b>CapCut</b> (o Edits): ordénalos, recorta a los segundos indicados, pon la <b>voz en off</b> (archivo mp3 incluido), los subtítulos automáticos (palabra resaltada en verde), el reloj, las pantallas y el efecto de rebobinar.</li>
<li>Mándame el video terminado o súbelo a la carpeta del repositorio y yo lo programo, lo mido y te digo qué mejorar.</li>
</ol>"""

def pagina(marca):
    M = REELS[marca]; c, a = M['color'], M['acento']
    out = [f"""<section class="cover" style="background:{c}"><div class="k" style="color:{a}">GUÍA DE REELS PARA FLOW</div><h1>{M['marca']}</h1>
<p>{len(M['reels'])} reels con historia, escena por escena: imagen inicial, prompt para Flow, voz en off, texto en pantalla y sonidos.</p>
<div class="box"><h3>Cómo usar esta guía</h3>{PASOS}<p class="neg"><b>Estilo (agrégalo a cada prompt):</b> {html.escape(STYLE)}</p><p class="neg"><b>Reglas (al final de cada prompt):</b> {html.escape(NEG)}</p></div></section>"""]
    for r in M['reels']:
        filas = ''.join(f"""<tr><td class="n">{i+1}<br><small>{html.escape(d)}</small></td><td><div class="modo">{html.escape(m)}</div><div class="pr">{html.escape(p)}</div></td><td><div class="vo">🎙️ {html.escape(v)}</div><div class="ov">🖼️ {html.escape(o)}</div><div class="sx">🔊 {html.escape(s)}</div></td></tr>""" for i, (d, m, p, v, o, s) in enumerate(r['escenas']))
        out.append(f"""<section class="reel"><div class="head" style="border-color:{a}"><img src="{b64(r['img'])}"><div><div class="k" style="color:{c}">{r['id']} · REEL CON HISTORIA</div><h2>{html.escape(r['titulo'])}</h2>
<p><b>Imagen inicial:</b> {r['img']} (9:16, foto real de Unsplash, uso libre).</p><p><b>Voz en off:</b> {r['voz']} (voz mexicana, ya generada).</p>
<div class="pj"><b>Descripción del personaje (pégala en cada escena):</b><br>{html.escape(r['personaje'])}</div></div></div>
<table><tr><th>#</th><th>Prompt para Flow (inglés: Veo lo entiende mejor)</th><th>En la edición</th></tr>{filas}</table></section>""")
    css = f"""*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Inter,sans-serif;color:#1b2430;font-size:12.5px;line-height:1.45}}
section{{page-break-after:always;padding:28px 32px}}.cover{{color:#fff;min-height:100vh;padding:56px}}.cover h1{{font-size:54px;margin:8px 0 12px}}.cover p{{font-size:15px;opacity:.9}}
.k{{font-weight:800;letter-spacing:.14em;font-size:12px}}.box{{background:#fff;color:#1b2430;border-radius:18px;padding:22px 26px;margin-top:28px}}.box h3{{margin-bottom:10px;font-size:18px}}
.box ol{{padding-left:20px}}.box li{{margin-bottom:7px}}.neg{{margin-top:10px;font-size:12px;background:#f3f5f8;border-radius:10px;padding:10px 12px}}
.head{{display:flex;gap:22px;border-left:6px solid;padding-left:18px;margin-bottom:16px}}.head img{{width:190px;height:338px;object-fit:cover;border-radius:14px;flex-shrink:0}}
.head h2{{font-size:24px;margin:4px 0 8px}}.head p{{margin-bottom:4px}}.pj{{margin-top:10px;background:#f3f5f8;border-radius:10px;padding:10px 12px;font-size:12px}}
table{{width:100%;border-collapse:collapse}}th{{background:{c};color:#fff;text-align:left;padding:8px;font-size:12px}}td{{border-bottom:1px solid #e3e7ee;padding:9px 8px;vertical-align:top}}
td.n{{font-weight:800;font-size:18px;width:52px;color:{c}}}td.n small{{font-size:10px;font-weight:600;color:#6b7690}}.modo{{font-weight:700;color:{c};margin-bottom:4px}}
.pr{{font-family:'DejaVu Sans Mono',monospace;font-size:11px;background:#f7f8fa;border-radius:8px;padding:8px}}.vo{{font-weight:600;margin-bottom:5px}}.ov,.sx{{color:#4a5670;margin-bottom:4px}}tr{{page-break-inside:avoid}}"""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(out)}</body></html>"

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page()
    for marca, nombre in [('dieloxia', 'Guia_Flow_Dieloxia.pdf'), ('checkonoff', 'Guia_Flow_CheckONOFF.pdf')]:
        pg.set_content(pagina(marca)); pg.wait_for_timeout(300)
        pg.pdf(path=str(D / nombre), format='Letter', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        pg.screenshot(path=str(D / f'prev_{marca}.png'), full_page=True)
    b.close()
print('ok')
