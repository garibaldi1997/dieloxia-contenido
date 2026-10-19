# Reels con historia (formato de referencia de la competencia)

1. Escribe el guion en `voz/<nombre>.txt` (primera línea `#voz es-MX-JorgeNeural +8%` o `es-MX-DaliaNeural`) y haz push: la acción "Generar voz de reels" deja `voz/<nombre>.mp3` y `.json` con tiempos por palabra.
2. Copia `ejemplo_dentista.html` a una carpeta de trabajo como `reel.html`, pon ahí las fotos (`<nombre>.jpg`, se usan como `P.<nombre>`) y ajusta las escenas a los tiempos de la voz (`v` = segundo de la voz).
3. Música y sonidos: `python3 bed.py <carpeta>/bed.wav <duración> "<dings>" "<rebobinado_ini>,<fin>" "<pops>"` (tiempos del video = tiempo de voz ÷ velocidad).
4. Prueba cuadros: `python3 make_reel.py <carpeta> voz/<nombre> 1.1 logo.png 2 6 10 …` y revisa `<carpeta>/probe.jpg`.
5. Render final: el mismo comando sin tiempos → `<carpeta>/reel.mp4` (máx. 15 MB).

Estructura: dolor con reloj en pantalla → notificaciones/caos → consecuencia → rebobinar ⏪ → "Ahora, con tu asistente de Dieloxia" → producto resolviendo → final feliz → cierre con logo al centro. Nunca logo arriba. Difumina nombres reales en uniformes o gafetes.
