"""Sound design for the VISORA real-estate-only ad.
Every placed sound is synthesised once with its own recipe, so nothing repeats."""
import numpy as np, scipy.signal as sg, os
from scipy.io import wavfile
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR = 48000; DUR = 21.3; N = int(SR * DUR)
rng = np.random.default_rng(41)
dry = np.zeros((N, 2)); wet = np.zeros((N, 2)); log = []

def t_(d): return np.arange(int(SR * d)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def sos(kind, f, order=2): return sg.butter(order, f, kind, fs=SR, output='sos')
def lp(x, f, o=2): return sg.sosfilt(sos('lowpass', f, o), x)
def hp(x, f, o=2): return sg.sosfilt(sos('highpass', f, o), x)
def bp(x, lo, hi, o=2): return sg.sosfilt(sos('bandpass', [lo, min(hi, SR / 2 - 200)], o), x)
def noise(d): return rng.standard_normal(int(SR * d))
def pink(d):
    w = noise(d); b, a = [0.049922035, -0.095993537, 0.050612699, -0.004408786], [1, -2.494956002, 2.017265875, -0.522189400]
    return sg.lfilter(b, a, w)
def sweep(f0, f1, d, curve='exp'):
    t = t_(d); f = f0 * (f1 / f0) ** (t / d) if curve == 'exp' else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def ring(f, d, k): t = t_(d); return np.sin(2 * np.pi * f * t) * np.exp(-t * k)
def pad(x, n): return np.pad(x, (0, max(0, n - len(x))))[:n]
def mix(*parts):
    n = max(len(p) for p in parts); return sum(pad(p, n) for p in parts)
def at(x, d, off):
    y = np.zeros(int(SR * d)); i = int(off * SR); y[i:i + len(x)] += x[:len(y) - i]; return y
def karplus(f, d, damp=0.996, bright=0.5):
    n = int(SR * d); p = int(SR / f); buf = rng.uniform(-1, 1, p); buf = lp(buf, 800 + 9000 * bright) if p > 16 else buf
    out = np.zeros(n); prev = 0.0
    for i in range(n):
        v = buf[i % p]; out[i] = v; nv = damp * 0.5 * (v + prev); prev = v; buf[i % p] = nv
    return out

# ---------- one recipe per sound ----------
def plotter(d=1.8):
    out = np.zeros(int(SR * d)); t0 = 0.0
    while t0 < d - 0.05:
        L = rng.uniform(0.09, 0.17); f = rng.choice([196, 233, 262, 311, 349, 392, 466])
        t = t_(min(L, d - t0)); x = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 3, 5, 7))
        x *= np.minimum(1, t / 0.01) * np.minimum(1, (t[-1] - t + 1e-4) / 0.012)
        out = out + at(x, d, t0) + at(ring(3400, 0.01, 600) * 0.4, d, t0); t0 += L + rng.uniform(0, 0.03)
    return lp(out, 2400) * (0.55 + 0.45 * np.sin(np.pi * t_(d) / d))
def breath(d=0.9):
    x = pink(d); x = bp(x, 700, 900) * 1.2 + bp(x, 1100, 1400) + bp(x, 2400, 3200) * 0.5
    return x * np.sin(np.pi * t_(d) / d) ** 2
def laser_measure():
    return mix(sweep(1200, 3600, 0.16) * np.hanning(int(SR * 0.16)), at(ring(3600, 0.12, 40), 0.3, 0.16) * 0.6)
def reverse_cymbal(d=1.4):
    x = hp(noise(d), 3000) + 0.6 * bp(noise(d), 6000, 9500); e = np.exp(-t_(d) * 3.2)
    return (x * e)[::-1] * np.minimum(1, t_(d)[::-1] / 0.004)
def glass_shimmer(d=0.55):
    out = np.zeros(int(SR * d))
    for g in range(40):
        st = rng.uniform(0, d - 0.08); f = 1800 * (1 + 1.5 * st / d) * rng.choice([1, 2.76, 5.4]) * rng.uniform(.98, 1.02)
        tg = t_(0.07); out += at(np.sin(2 * np.pi * f * tg) * np.hanning(len(tg)), d, st)
    return out * (t_(d) / d) ** 0.7
def fm_impact(d=1.6):
    t = t_(d); idx = 8 * np.exp(-t * 6); m = np.sin(2 * np.pi * 55 * 1.41 * t)
    body = np.sin(2 * np.pi * 55 * t + idx * m) * np.exp(-t * 3.5)
    return body + 0.5 * lp(noise(d), 900) * np.exp(-t * 28)
def doppler(d=0.9):
    x = pink(d); t = t_(d); fc = 300 + 2400 * np.sin(np.pi * np.clip(t / d * 1.15, 0, 1)) ** 2
    y = np.zeros_like(x); lo = bd = 0.0; q = 0.35
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * fc[i] / SR); hi = x[i] - lo - q * bd; bd += f * hi; lo += f * bd; y[i] = bd
    y *= np.sin(np.pi * t / d) ** 1.5; pan = np.clip(t / d, 0, 1)
    return np.stack([y * np.cos(pan * np.pi / 2), y * np.sin(pan * np.pi / 2)], 1)
def fm_bell_chord(notes=(784, 1175), d=1.6):
    t = t_(d); out = 0
    for f in notes: out = out + np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t * 3) * np.sin(2 * np.pi * f * 3.5 * t)) * np.exp(-t * 2.4)
    return out * np.minimum(1, t / 0.003)
def pluck_arp(notes=(523.25, 659.25, 783.99)):
    return mix(*[at(karplus(f, 1.0, 0.9965, 0.7), 1.3, i * 0.07) for i, f in enumerate(notes)])
def felt_mallet(f=196, d=0.7):
    t = t_(d); return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)) * np.minimum(1, t / 0.008) * np.exp(-t * 6)
def blinds_rattle(d=0.5):
    out = np.zeros(int(SR * d))
    for k in range(10):
        st = 0.035 * k + rng.uniform(-0.01, 0.01); c = bp(noise(0.03), 1500, 5000) * np.exp(-t_(0.03) * 160)
        out += at(mix(c, 0.5 * ring(rng.uniform(900, 1700), 0.06, 70)), d, max(0, st))
    return out
def door_latch():
    a = mix(hp(noise(0.01), 2000) * np.exp(-t_(0.01) * 500), ring(2800, 0.08, 45))
    b_ = mix(ring(1900, 0.1, 40) * 0.8, ring(120, 0.08, 50))
    return mix(a, at(b_, 0.2, 0.06))
def wood_knock():
    t = t_(0.35); x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in ((180, 1, 25), (410, .7, 35), (690, .45, 45), (1130, .25, 60)))
    return x + 0.4 * bp(noise(0.35), 800, 3000) * np.exp(-t * 300)
def light_switch():
    t = t_(0.15); return ring(1200, 0.15, 80) * 0.6 + ring(90, 0.15, 60) + hp(noise(0.15), 3000) * np.exp(-t * 900)
def page_turn(d=0.5):
    t = t_(d); x = bp(noise(d), 800, 6000) * (0.6 + 0.4 * np.sin(2 * np.pi * (25 + 20 * t / d) * t))
    return x * np.sin(np.pi * t / d) ** 2 * np.exp(-t * 2)
def card_slap():
    t = t_(0.25); return bp(noise(0.25), 300, 1500) * np.exp(-t * 40) + 0.8 * np.sin(2 * np.pi * 140 * t) * np.exp(-t * 30)
def muted_pluck(): return karplus(98, 0.5, 0.985, 0.25)
def sparkle_sweep(d=0.9):
    out = np.zeros(int(SR * d))
    for g in range(70):
        st = d * (g / 70) ** 1.3 + rng.uniform(0, 0.01); f = 2000 + 5000 * st / d + rng.uniform(-200, 200)
        tg = t_(0.03); out += at(np.sin(2 * np.pi * f * tg) * np.hanning(len(tg)) * rng.uniform(.4, 1), d, min(st, d - 0.031))
    return out
def glass_ping():
    t = t_(0.9); return sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in ((2700, 1, 5), (5100, .5, 8), (7300, .3, 12)))
def marimba3(notes=(392, 523.25, 659.25)):
    def bar(f):
        t = t_(0.5); return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 3.93 * f * t) * np.exp(-t * 20)) * np.exp(-t * 11) + 0.2 * hp(noise(0.5), 4000) * np.exp(-t * 400)
    return mix(*[at(bar(f), 0.8, i * 0.09) for i, f in enumerate(notes)])
def harp_cascade(notes=(523.25, 587.33, 659.25, 783.99, 880, 1046.5), step=0.1709):
    return mix(*[at(karplus(f, 0.9, 0.997, 0.85), 2.0, i * step) for i, f in enumerate(notes)])
def slide_thunk(d=0.42):
    t = t_(d); r = lp(noise(d), 220) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t)) * np.minimum(1, t / 0.08)
    th = mix(np.sin(2 * np.pi * 70 * t_(0.4)) * np.exp(-t_(0.4) * 9), bp(noise(0.4), 300, 1200) * np.exp(-t_(0.4) * 40))
    return mix(r, at(th * 1.4, d + 0.4, d))
def focus_motor(d=0.5):
    t = t_(d); f = 140 + 70 * np.sin(np.pi * t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 9)); return lp(x, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * t)) * np.sin(np.pi * t / d)
def shepard_riser(d=1.0):
    t = t_(d); out = 0
    for k in range(6):
        f = 110 * 2 ** (k + t / d); w = np.exp(-0.5 * ((np.log2(f / 880)) / 1.1) ** 2)
        out = out + w * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return out * (t / d) ** 1.6
def waterfall_crash(d=2.6):
    t = t_(d); spray = lp(noise(d), 1200) * 0.8 + bp(noise(d), 2000, 5000) * 0.6
    sub = np.sin(2 * np.pi * np.cumsum(35 + 10 * np.exp(-t * 4)) / SR) * np.exp(-t * 3)
    return spray * np.exp(-t * 1.4) * np.minimum(1, t / 0.005) + sub * 1.2
def tape_flanger(d=0.7):
    x = pink(d); t = t_(d); dl = (0.001 + 0.005 * t / d) * SR; n = np.arange(len(x))
    y = x + 0.75 * np.interp(n - dl, n, x, left=0); return y * np.sin(np.pi * t / d) ** 2
def piano_chord(notes=(392, 493.88, 587.33)):
    return mix(*[karplus(f, 1.8, 0.9985, 0.9) + 0.5 * karplus(f * 1.003, 1.8, 0.9985, 0.9) for f in notes])
def droplet():
    a = sweep(600, 2200, 0.025) * np.hanning(int(SR * 0.025)); b_ = sweep(900, 2800, 0.02) * np.hanning(int(SR * 0.02)) * 0.4
    return mix(a, at(b_, 0.2, 0.09))
def mirror_slap():
    t = t_(0.5); th = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-t * 8) + 50) / SR) * np.exp(-t * 14)
    spring = np.sin(2 * np.pi * 3100 * t + 3 * np.sin(2 * np.pi * 7 * t)) * np.exp(-t * 18) * 0.35
    return th + spring + hp(noise(0.5), 2500) * np.exp(-t * 500) * 0.6
def harmonic_glide(d=1.0):
    t = t_(d); f = 440 * 1.5 ** (np.clip(t / d, 0, 1) ** 2); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)) * np.sin(np.pi * t / d)
def film_ratchet():
    return mix(*[at(ring(f, 0.04, 140) + hp(noise(0.04), 3000) * np.exp(-t_(0.04) * 700), 0.3, i * 0.045) for i, f in enumerate((2200, 2500, 2100, 2700))],
               lp(noise(0.25), 400) * 0.3 * np.sin(np.pi * t_(0.25) / 0.25))
def projector(d=2.7):
    t = t_(d); clat = bp(noise(d), 1000, 4000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 24 * t))) * 0.6
    hum = 0.3 * np.sin(2 * np.pi * 50 * t) + 0.2 * np.sin(2 * np.pi * 100 * t)
    return (clat + hum) * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.3)
def tape_rip(d=0.25):
    t = t_(d); g = (rng.uniform(0, 1, len(t)) > 0.985).astype(float); g = lp(g, 300) * 30
    return hp(noise(d), 2200) * np.clip(g, 0, 1) * np.sin(np.pi * t / d) * (0.5 + t / d)
def low_tom():
    t = t_(0.6); return np.sin(2 * np.pi * np.cumsum(95 + 35 * np.exp(-t * 18)) / SR) * np.exp(-t * 7) + 0.4 * bp(noise(0.6), 200, 800) * np.exp(-t * 60)
def reverse_snap():
    return (hp(noise(0.3), 1000) * np.exp(-t_(0.3) * 40))[::-1]
def metal_ring():
    t = t_(1.2); return np.sin(2 * np.pi * 440 * t + 3 * np.exp(-t * 4) * np.sin(2 * np.pi * 616 * t)) * np.exp(-t * 3) * np.minimum(1, t / 0.002)
def vault_thunk():
    t = t_(0.8); return np.sin(2 * np.pi * 48 * t) * np.exp(-t * 5) * 1.3 + bp(noise(0.8), 400, 1200) * np.exp(-t * 25) + ring(2300, 0.8, 90) * 0.3
def warm_pad(d=1.3):
    t = t_(d); x = sum(sg.sawtooth(2 * np.pi * f * t) for f in (146.83, 220, 293.66, 369.99))
    return lp(x, 1200) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
def twinkle():
    return mix(*[at(np.sin(2 * np.pi * f * t_(0.25) + 1.2 * np.exp(-t_(0.25) * 20) * np.sin(2 * np.pi * 2 * f * t_(0.25))) * np.exp(-t_(0.25) * 14), 0.6, i * 0.05)
                 for i, f in enumerate((1568, 1975.5, 2349.3, 2637, 3136))])
def bwom():
    t = t_(0.6); return np.sin(2 * np.pi * np.cumsum(220 * 0.5 ** (t / 0.6)) / SR + 0.8 * np.sin(2 * np.pi * 110 * t)) * np.exp(-t * 4)
def ui_toggle():
    tri = lambda f, d: sg.sawtooth(2 * np.pi * f * t_(d), 0.5) * np.exp(-t_(d) * 25)
    return mix(tri(659.25, 0.15), at(tri(880, 0.18), 0.3, 0.07))
def keyboard():
    out = np.zeros(int(SR * 0.4)); st = 0
    for k in range(4):
        st += rng.uniform(0.06, 0.1); c = bp(noise(0.03), 2000, 6000) * np.exp(-t_(0.03) * 300) + ring(rng.uniform(260, 340), 0.03, 120) * 0.6
        out += at(c, 0.4, min(st, 0.36))
    return out
def thock():
    t = t_(0.12); return lp(np.r_[np.ones(48), np.zeros(len(t) - 48)], 200) * 6 * np.exp(-t * 40) + ring(600, 0.12, 70) * 0.5
def msg_send():
    a = sweep(500, 1600, 0.18) * np.sin(np.pi * t_(0.18) / 0.18); tail = hp(noise(0.3), 4000) * np.exp(-t_(0.3) * 12) * 0.25
    return mix(a, at(tail, 0.5, 0.12))
def kalimba(f=1046.5):
    t = t_(0.8); return (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * 5.9 * f * t) * np.exp(-t * 30)) * np.exp(-t * 6) + 0.15 * hp(noise(0.8), 5000) * np.exp(-t * 600)

used = set()
def put(name, start, x, db, pan=0.0, rev=0.18, peak_at=None, end_at=None):
    assert name not in used, name; used.add(name)
    x = np.asarray(x, float); x = x / (np.abs(x).max() + 1e-9)
    if x.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4); x = np.stack([x * l * 1.414, x * r * 1.414], 1)
    if peak_at is not None: start = peak_at - np.argmax(np.abs(x).sum(1)) / SR
    if end_at is not None: start = end_at - len(x) / SR
    g = 10 ** (db / 20); i = int(round(start * SR))
    if i < 0: x = x[-i:]; i = 0
    x = x[:max(0, N - i)]
    dry[i:i + len(x)] += x * g * (1 - rev * 0.5); wet[i:i + len(x)] += x * g * rev
    log.append((round(start, 2), name, db))


# ---------- recipes added for this ad ----------
def curtain_swish(d=0.45):
    t = t_(d); x = bp(noise(d), 400, 3500) * (0.7 + 0.3 * np.sin(2 * np.pi * 6 * t)); return x * np.sin(np.pi * t / d) ** 2
def mirror_glint():
    t = t_(0.7); return sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) * np.minimum(1, t / 0.002) for f, a, k in ((2900, 1, 9), (4400, .6, 12), (6600, .35, 16)))
def pull_chain():
    beads = mix(*[at(hp(noise(0.006), 4000) * np.exp(-t_(0.006) * 800), 0.12, i * 0.011 + rng.uniform(0, 0.004)) for i in range(5)])
    return mix(beads, at(ring(1600, 0.12, 60) + 0.5 * ring(95, 0.12, 50), 0.3, 0.08))
def tap_pour(d=0.5):
    t = t_(d); flow = bp(noise(d), 800, 3000) * np.sin(np.pi * t / d) ** 0.8 * 0.6
    bub = mix(*[at(sweep(f, f * 1.6, 0.03) * np.hanning(int(SR * 0.03)), d, rng.uniform(0.02, d - 0.05)) for f in rng.uniform(600, 1400, 9)])
    return mix(flow, bub)
def braam(d=1.4):
    t = t_(d); x = sum(sg.sawtooth(2 * np.pi * f * t) for f in (55, 82.41, 110, 164.8))
    y = np.zeros_like(x); fc = 200 + 1000 * np.sin(np.pi * np.clip(t / (d * 0.6), 0, 1)); lo = bd = 0.0
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * fc[i] / SR); hi = x[i] - lo - 0.5 * bd; bd += f * hi; lo += f * bd; y[i] = lo
    return np.tanh(y * 1.5) * np.minimum(1, t / 0.01) * np.exp(-t * 1.6)
def grid_fill(d=0.6):
    out = np.zeros(int(SR * d)); k = 0; st = 0.0
    while st < d - 0.02:
        f = 1000 * 4 ** (st / d); out += at(ring(f, 0.02, 220) * 0.8, d, st); k += 1; st += 0.05 * (1 - 0.8 * st / d)
    return out
def phone_ring():
    t = t_(0.26); tone = (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * t)))
    tone *= np.minimum(1, t / 0.01) * np.minimum(1, (0.26 - t) / 0.02); return mix(tone, at(tone, 0.62, 0.36))

BEAT = 0.6835; D1 = 2.00; Bn = lambda n: D1 + n * 4 * BEAT; b = lambda n, k: Bn(n) + k * BEAT
D2 = Bn(4); W0 = b(2, 2)

# hook: blueprint
put('pen plotter', 0.05, plotter(), -20, 0.1, 0.1)
put('breath', 0.12, breath(), -23, -0.2)
put('laser measure', 1.25, laser_measure(), -19, 0.5)
put('reverse cymbal', 0, reverse_cymbal(), -16, end_at=D1)
put('materialise', D1 - 0.35, glass_shimmer(), -20, 0.0, 0.3)
# drop 1: villa
put('metal impact', D1, fm_impact(), -11, 0, 0.25)
put('doppler pass', D1, doppler(), -18, rev=0.15)
put('bell chord', D1 + 0.32, fm_bell_chord(), -16, -0.1, 0.35)
put('logo pluck', b(0, 2) - 0.1, pluck_arp(), -14, 0.1, 0.3)
put('felt mallet', b(0, 3), felt_mallet(), -16, 0.0, 0.2)
# hotel tour foley
put('blinds', Bn(1) - 0.1, blinds_rattle(), -9, 0, 0.12)
put('curtain', b(1, 0) + 0.12, curtain_swish(), -14, -0.4, 0.15)
put('mirror glint', b(1, 1), mirror_glint(), -11, 0.3, 0.35)
put('pull chain', b(1, 2), pull_chain(), -10, -0.2, 0.15)
put('tap pour', b(1, 3), tap_pour(), -11, 0.2, 0.25)
# before / after
put('page turn', b(2, 0) - 0.22, page_turn(), -13, 0.4)
put('card slap', b(2, 0) + 0.18, card_slap(), -13, 0.0, 0.15)
put('muted pluck', b(2, 1), muted_pluck(), -13, -0.4, 0.2)
put('sparkle sweep', W0, sparkle_sweep(), -15, 0.0, 0.35)
put('glass ping', W0 + 0.18, glass_ping(), -15, 0.5, 0.35)
put('marimba', b(2, 3), marimba3(), -14, -0.2, 0.25)
# grid, then dive into it
put('harp cascade', Bn(3) + 0.06, harp_cascade(), -14, 0.1, 0.3)
put('dive flanger', b(3, 3) - 0.12, tape_flanger(0.8), -15)
put('shepard riser', 0, shepard_riser(0.9), -16, end_at=D2)
# drop 2: montage
put('braam', D2, braam(), -12, 0, 0.2)
put('low tom', D2, low_tom(), -12, 0, 0.15)
put('photos click', D2 + 0.03, mirror_slap(), -14, 0.3, 0.1)
put('video tours', b(4, 1), film_ratchet(), -11, -0.3, 0.1)
put('reels', b(4, 2), ui_toggle(), -13, 0.3, 0.15)
put('quote', b(4, 3), kalimba(), -11, -0.2, 0.35)
# CTA
put('grid fill', Bn(5) - 0.42, grid_fill(), -15, 0.0, 0.2)
put('warm pad', Bn(5) + 0.05, warm_pad(), -20, 0, 0.3)
put('twinkle', Bn(5) + 0.1, twinkle(), -17, 0.3, 0.4)
put('bwom', b(5, 2) - 0.04, bwom(), -13, 0, 0.2)
put('whatsapp in', b(5, 3) - 0.04, msg_send(), -12, 0.3, 0.25)
put('call in', Bn(6) - 0.04, thock(), -9, -0.2, 0.1)
put('phone ring', b(6, 1), phone_ring(), -12, -0.3, 0.2)

# small plate reverb shared by everything
L = int(SR * 1.8); tt = np.arange(L) / SR
ir = np.stack([lp(rng.standard_normal(L), 6000) * np.exp(-tt * 3.6), lp(rng.standard_normal(L), 6000) * np.exp(-tt * 3.6)], 1)
ir[:int(SR * 0.012)] = 0; ir /= np.sqrt((ir ** 2).sum(0))
rv = np.stack([sg.fftconvolve(wet[:, c], ir[:, c])[:N] for c in range(2)], 1)
bus = dry + rv * 0.9
pk = np.abs(bus).max(); print('sfx bus peak %.2f dBFS' % (20 * np.log10(pk)))
bus = np.tanh(bus * 1.2) / np.tanh(1.2); pk = np.abs(bus).max()
if pk > 0.89: bus *= 0.89 / pk
wavfile.write('sfx.wav', SR, (bus * 32767).astype(np.int16))
print(len(log), 'unique sounds placed')
for l in sorted(log): print('%6.2fs  %-16s %4d dB' % l)
