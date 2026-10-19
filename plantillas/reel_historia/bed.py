"""Música original suave + sonidos. Uso: python3 bed.py salida.wav duracion "dings" "whoosh_ini,whoosh_fin" [pops]"""
import numpy as np, wave, sys
SR = 44100; out, DUR = sys.argv[1], float(sys.argv[2])
dings = [float(x) for x in sys.argv[3].split(',') if x]; wa, wb = [float(x) for x in sys.argv[4].split(',')]
pops = [float(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 and sys.argv[5] else []
n = int(SR * DUR); t = np.arange(n) / SR; mus = np.zeros(n)
note = lambda m: 440 * 2 ** ((m - 69) / 12)
prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
for i in range(int(DUR / 2) + 1):
    a = int(i * 2 * SR); b = min(n, a + int(2.1 * SR))
    if a >= n: break
    tt = np.arange(b - a) / SR; env = np.minimum(1, tt / .3) * np.exp(-tt * .6); ch = prog[i % 4]
    for m in ch: mus[a:b] += .05 * np.sin(2 * np.pi * note(m) * tt) * env + .02 * np.sin(2 * np.pi * note(m + 12) * tt) * env
    mus[a:b] += .08 * np.sin(2 * np.pi * note(ch[0] - 12) * tt) * np.exp(-tt * 3)
for k in np.arange(0, DUR, .535):
    a = int(k * SR); m = min(n, a + int(.12 * SR)); tt = np.arange(m - a) / SR
    mus[a:m] += .12 * np.sin(2 * np.pi * (90 - 300 * tt) * tt) * np.exp(-tt * 35)
g = np.ones(n); g[(t > wa) & (t < wb)] = .25; g[t > wb] = 1.25; mus *= g
sfx = np.zeros(n)
def ding(ts, f):
    a = int(ts * SR); m = min(n, a + int(.35 * SR)); tt = np.arange(m - a) / SR
    sfx[a:m] += .22 * (np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 1.5 * tt)) * np.exp(-tt * 12)
for d in dings: ding(d, 1320)
for d in pops: ding(d, 1760)
a, m = int(wa * SR), int(wb * SR); tt = np.arange(m - a) / SR
sfx[a:m] += .15 * (np.random.randn(m - a) * .4 + np.sin(2 * np.pi * (1200 - 900 * tt / tt[-1]) * tt)) * np.sin(np.pi * tt / tt[-1])
o = np.clip(mus * .7 + sfx, -1, 1)
w = wave.open(out, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32000).astype(np.int16).tobytes()); w.close()
