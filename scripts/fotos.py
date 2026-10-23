"""Registro de fotos usadas: ninguna foto se repite y una misma sesión/modelo sale como máximo 1 vez cada 30 días.

  python scripts/fotos.py revisar foto.jpg [--fotografo NOMBRE]   → exit 1 si ya se usó (o se parece) o si la sesión salió hace < 30 días
  python scripts/fotos.py usar foto.jpg PIEZA [--unsplash ID] [--fotografo NOMBRE]   → la registra (revisa primero)
  python scripts/fotos.py lista                                    → muestra el registro

Compara por huella visual (dHash), así detecta la misma foto aunque tenga otro nombre, tamaño o recorte leve.
Registro: estado/fotos_usadas.json
"""
import argparse, datetime, json, pathlib, sys
from PIL import Image

REG = pathlib.Path(__file__).resolve().parent.parent / "estado" / "fotos_usadas.json"
DIAS_SESION = 30
UMBRAL = 10  # bits distintos de 64 para considerar "la misma foto"


def huella(ruta):
    im = Image.open(ruta).convert("L").resize((9, 8), Image.LANCZOS)
    px = list(im.tobytes())
    return "%016x" % sum(1 << i for i in range(64) if px[(i // 8) * 9 + i % 8] > px[(i // 8) * 9 + i % 8 + 1])


def cargar():
    return json.loads(REG.read_text(encoding="utf-8")) if REG.exists() else []


def revisar(ruta, fotografo=None, unsplash=None):
    h, hoy, prob = int(huella(ruta), 16), datetime.date.today(), []
    for r in cargar():
        if bin(h ^ int(r["huella"], 16)).count("1") <= UMBRAL or (unsplash and r.get("unsplash") == unsplash):
            prob.append(f"ya se usó en {r['pieza']} ({r['fecha']})")
        elif fotografo and r.get("fotografo", "").lower() == fotografo.lower() and (hoy - datetime.date.fromisoformat(r["fecha"])).days < DIAS_SESION:
            prob.append(f"misma sesión/fotógrafo ({fotografo}) en {r['pieza']} ({r['fecha']}); espera {DIAS_SESION} días")
    return prob


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=["revisar", "usar", "lista"])
    ap.add_argument("foto", nargs="?")
    ap.add_argument("pieza", nargs="?")
    ap.add_argument("--unsplash")
    ap.add_argument("--fotografo")
    a = ap.parse_args()
    if a.accion == "lista":
        for r in cargar():
            print(r["fecha"], r["pieza"], r.get("unsplash", ""), r.get("fotografo", ""), r["archivo"])
        return
    prob = revisar(a.foto, a.fotografo, a.unsplash)
    if prob:
        print("❌ " + pathlib.Path(a.foto).name + ": " + "; ".join(prob))
        sys.exit(1)
    if a.accion == "usar":
        reg = cargar()
        reg.append({"huella": huella(a.foto), "archivo": pathlib.Path(a.foto).name, "pieza": a.pieza, "fecha": datetime.date.today().isoformat(),
                    **({"unsplash": a.unsplash} if a.unsplash else {}), **({"fotografo": a.fotografo} if a.fotografo else {})})
        REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("✅ " + pathlib.Path(a.foto).name + (" registrada" if a.accion == "usar" else " libre"))


if __name__ == "__main__":
    main()
