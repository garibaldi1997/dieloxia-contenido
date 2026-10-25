"""Genera la voz en off de los reels (Edge TTS, gratis) con tiempos por palabra.

Por cada voz/<nombre>.txt sin su voz/<nombre>.mp3 crea:
  voz/<nombre>.mp3   narración
  voz/<nombre>.json  [{"t": inicio_s, "d": duración_s, "w": "palabra"}, ...]
La primera línea del .txt puede fijar voz y velocidad: "#voz es-MX-DaliaNeural +6%".
El .json trae UNA entrada por palabra escrita del guion (aunque la voz diga otra cosa, p. ej. CheckONOFF → "chek on of").
"""
import asyncio, difflib, json, pathlib, re, sys, unicodedata
import edge_tts

VOZ, VEL = "es-MX-DaliaNeural", "+6%"
# Cómo debe sonar cada término (la pantalla sigue mostrando la palabra escrita)
PRON = {r"CheckONOFF|CheckOnOff|Checkonoff|CHECKONOFF": "Chek on of", r"\bRRHH\b": "recursos humanos", r"\bRH\b": "recursos humanos",
        r"\bSTPS\b": "ese te pe ese", r"\bLFT\b": "Ley Federal del Trabajo", r"\bNOM-0?(\d+)\b": r"norma cero \1",
        r"\bIA\b": "inteligencia artificial", r"\bUMA\b": "umas"}
norm = lambda s: re.sub(r"[^a-z0-9ñ]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())


def hablar(s):
    for k, v in PRON.items():
        s = re.sub(k, v, s)
    return s


def alinear(escritas, palabras):
    """Reparte los tiempos de Edge (por palabra hablada) entre las palabras escritas del guion."""
    habladas, dueno = [], []
    for i, t in enumerate(escritas):
        for h in hablar(t).split():
            habladas.append(h); dueno.append(i)
    ww = [{"t": w["t"] + w["d"] * k / len(w["w"].split()), "d": w["d"] / len(w["w"].split()), "w": x}
          for w in palabras for k, x in enumerate(w["w"].split() or [w["w"]])]
    a, b = [norm(h) for h in habladas], [norm(w["w"]) for w in ww]
    tiempos = [None] * len(habladas)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                tiempos[i1 + k] = (ww[j1 + k]["t"], ww[j1 + k]["t"] + ww[j1 + k]["d"])
        elif tag == "replace":
            s0, e0 = ww[j1]["t"], ww[j2 - 1]["t"] + ww[j2 - 1]["d"]
            for k in range(i2 - i1):
                tiempos[i1 + k] = (s0 + (e0 - s0) * k / (i2 - i1), s0 + (e0 - s0) * (k + 1) / (i2 - i1))
    for i in range(len(tiempos)):
        if tiempos[i] is None:
            p = tiempos[i - 1][1] if i else 0
            n = next((x[0] for x in tiempos[i + 1:] if x), p + 0.3)
            tiempos[i] = (p, max(p + 0.1, n))
    salida = []
    for i, t in enumerate(escritas):
        ks = [k for k, d in enumerate(dueno) if d == i]
        s0, e0 = tiempos[ks[0]][0], tiempos[ks[-1]][1]
        salida.append({"t": round(s0, 3), "d": round(e0 - s0, 3), "w": t.strip(".,…:;¿?¡!")})
    return salida

async def generar(txt: pathlib.Path):
    lineas = txt.read_text(encoding="utf-8").splitlines()
    voz, vel = VOZ, VEL
    if lineas and lineas[0].startswith("#voz"):
        partes = lineas.pop(0).split()
        voz = partes[1] if len(partes) > 1 else voz
        vel = partes[2] if len(partes) > 2 else vel
    escritas = [t for l in lineas for t in l.split() if re.search(r"\w", t)]
    texto = hablar(" ".join(l.strip() for l in lineas if l.strip()))
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
    palabras = alinear(escritas, palabras)
    txt.with_suffix(".json").write_text(json.dumps(palabras, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", txt.name, len(palabras), "palabras")

async def main():
    pendientes = [t for t in sorted(pathlib.Path("voz").glob("*.txt"))
                  if not t.read_text(encoding="utf-8").startswith("#voz clon")  # esos los genera voz_clon.py
                  and (not t.with_suffix(".mp3").exists() or "--todo" in sys.argv)]
    for t in pendientes:
        await generar(t)
    if not pendientes:
        print("Sin textos pendientes.")

asyncio.run(main())
