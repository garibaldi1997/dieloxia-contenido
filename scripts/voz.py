"""Genera la voz en off de los reels (Edge TTS, gratis) con tiempos por palabra.

Por cada voz/<nombre>.txt sin su voz/<nombre>.mp3 crea:
  voz/<nombre>.mp3   narración
  voz/<nombre>.json  [{"t": inicio_s, "d": duración_s, "w": "palabra"}, ...]
La primera línea del .txt puede fijar voz y velocidad: "#voz es-MX-DaliaNeural +6%".
"""
import asyncio, json, pathlib, sys
import edge_tts

VOZ, VEL = "es-MX-DaliaNeural", "+6%"

async def generar(txt: pathlib.Path):
    lineas = txt.read_text(encoding="utf-8").splitlines()
    voz, vel = VOZ, VEL
    if lineas and lineas[0].startswith("#voz"):
        partes = lineas.pop(0).split()
        voz = partes[1] if len(partes) > 1 else voz
        vel = partes[2] if len(partes) > 2 else vel
    texto = " ".join(l.strip() for l in lineas if l.strip())
    try:
        com = edge_tts.Communicate(texto, voz, rate=vel, boundary="WordBoundary")
    except TypeError:
        com = edge_tts.Communicate(texto, voz, rate=vel)
    palabras, audio = [], bytearray()
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            palabras.append({"t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7, "w": ch["text"]})
    txt.with_suffix(".mp3").write_bytes(bytes(audio))
    txt.with_suffix(".json").write_text(json.dumps(palabras, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", txt.name, len(palabras), "palabras")

async def main():
    pendientes = [t for t in sorted(pathlib.Path("voz").glob("*.txt")) if not t.with_suffix(".mp3").exists() or "--todo" in sys.argv]
    for t in pendientes:
        await generar(t)
    if not pendientes:
        print("Sin textos pendientes.")

asyncio.run(main())
