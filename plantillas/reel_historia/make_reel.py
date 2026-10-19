"""Renderiza un reel con historia: reel.html (render(t)) + voz/<n>.mp3/.json + fotos.
Uso: python3 make_reel.py <carpeta> <voz_sin_ext> <velocidad> <logo.png> [t_prueba ...]
Las fotos son los .jpg de la carpeta (PH[nombre]). Salida: <carpeta>/reel.mp4 (con música y sonidos si hay bed.wav)."""
import json, pathlib, re, subprocess, sys
from playwright.sync_api import sync_playwright
D, VOZ, SPEED, LOGO = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]), float(sys.argv[3]), pathlib.Path(sys.argv[4])
probes = [float(x) for x in sys.argv[5:]]
FPS = 30
words = json.load(open(VOZ.with_suffix('.json')))
toks = [t for l in VOZ.with_suffix('.txt').read_text().splitlines() if not l.startswith('#voz') for t in l.split()]
toks = [t for t in toks if re.search(r'\w', t)]
assert len(toks) == len(words), (len(toks), len(words))
for w, t in zip(words, toks):
    w['raw'] = t; w['w'] = t.strip('.,…:¿?¡!')
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(VOZ.with_suffix('.mp3'))])) / SPEED
ph = {p.stem: p.as_uri() for p in D.glob('*.jpg') if not p.stem.startswith(('probe', 'sheet'))}
ph['logo'] = LOGO.as_uri()
fr = D / 'frames'; fr.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.add_init_script(f"window.SPEED={SPEED};window.WORDS={json.dumps(words, ensure_ascii=False)};window.PH={json.dumps(ph)};")
    pg.goto((D / 'reel.html').as_uri()); pg.wait_for_timeout(500)
    ts = probes or [i / FPS for i in range(int((dur + .5) * FPS))]
    for i, t in enumerate(ts):
        pg.evaluate(f'render({t})')
        if i == 0: pg.wait_for_timeout(300)
        pg.screenshot(path=str(fr / (f'probe_{t}.jpg' if probes else f'f{i:04d}.jpg')), type='jpeg', quality=88)
    b.close()
if probes:
    from PIL import Image
    ims = [Image.open(fr / f'probe_{t}.jpg') for t in probes]
    sh = Image.new('RGB', (240 * len(ims), 427))
    for i, im in enumerate(ims): im.thumbnail((240, 427)); sh.paste(im, (i * 240, 0))
    sh.save(D / 'probe.jpg'); sys.exit()
bed = D / 'bed.wav'
inp = ['-i', str(bed)] if bed.exists() else ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono']
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', str(fr / 'f%04d.jpg'), '-i', str(VOZ.with_suffix('.mp3')), *inp, '-filter_complex',
  f"[1:a]atempo={SPEED},volume=1.6,aformat=sample_rates=44100:channel_layouts=mono,asplit=2[vo1][vo2];[2:a]volume=0.55,aformat=sample_rates=44100:channel_layouts=mono[bg];[bg][vo1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[bd];[bd][vo2]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5[aout]",
  '-map', '0:v', '-map', '[aout]', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '22', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-movflags', '+faststart', str(D / 'reel.mp4')], check=True)
print('ok', round(dur, 2))
