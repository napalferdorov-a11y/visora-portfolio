"""Synthesised sound effects for the VISORA 30 s "stop the scroll" ad, placed on the same timeline as the animation."""
import numpy as np, scipy.signal as sg, os, subprocess
from scipy.io import wavfile
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR = 48000; DUR = 30.0; N = int(SR * DUR)
rng = np.random.default_rng(7)
bus = np.zeros((N, 2), np.float64)
log = []

def bp(x, lo, hi, order=2):
    return sg.sosfilt(sg.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sg.sosfilt(sg.butter(order, f, 'highpass', fs=SR, output='sos'), x)
def lp(x, f, order=2): return sg.sosfilt(sg.butter(order, f, 'lowpass', fs=SR, output='sos'), x)
def t_(d): return np.arange(int(SR * d)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)

def whoosh(d=0.55, peak=0.7, lo=250, hi=6000, layers=7, sharp=5.0):
    """noise swept through a bank of band-pass layers, loudest at `peak` (0..1)"""
    t = t_(d); n = len(t); out = np.zeros(n)
    fs = np.geomspace(lo, hi, layers)
    for k, f in enumerate(fs):
        pos = peak * (k / (layers - 1))           # low bands first, high bands at the peak
        env = np.exp(-((t / d - pos) ** 2) * sharp * 6)
        out += bp(rng.standard_normal(n), f * 0.75, min(f * 1.35, SR / 2 - 100)) * env
    g = np.where(t / d < peak, (t / d / peak) ** 2, np.exp(-(t / d - peak) * 9))
    return norm(out * g)
def swish(d=0.38, f=3500):
    t = t_(d); x = hp(rng.standard_normal(len(t)), f)
    return norm(x * np.sin(np.pi * t / d) ** 2)
def tick(f=1900):
    t = t_(0.06); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 90)
    c = hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 900)
    return norm(x + 0.6 * c)
def pop(f0=560, f1=190, d=0.09):
    t = t_(d); f = f0 * (f1 / f0) ** (t / d)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38))
def thud(d=0.5, f0=95, f1=42):
    t = t_(d); f = f1 + (f0 - f1) * np.exp(-t * 22)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    return norm(x + 0.25 * lp(rng.standard_normal(len(t)), 400) * np.exp(-t * 60))
def boom(d=1.3):
    t = t_(d); f = 38 + 50 * np.exp(-t * 14)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.6)
    return norm(x + 0.35 * lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 35))
def shutter(double=True):
    d = 0.20; t = t_(d); x = np.zeros(len(t))
    def burst(at, amp):
        tt = t - at; m = tt >= 0
        y = np.zeros(len(t)); y[m] = np.exp(-tt[m] * 260)
        return amp * bp(rng.standard_normal(len(t)), 1800, 9000) * y + amp * 0.7 * np.sin(2 * np.pi * 210 * t) * np.where(m, np.exp(-np.maximum(tt, 0) * 120), 0)
    x += burst(0.0, 1.0)
    if double: x += burst(0.072, 0.75)
    return norm(x)
def riser(d=0.78):
    t = t_(d); n = len(t); out = np.zeros(n)
    for k, f in enumerate(np.geomspace(500, 9000, 8)):
        env = np.exp(-((t / d - k / 7) ** 2) * 14)
        out += bp(rng.standard_normal(n), f * 0.8, min(f * 1.3, 22000)) * env
    gl = np.sin(2 * np.pi * np.cumsum(260 * (5.0) ** (t / d)) / SR) * 0.12
    return norm((out + gl) * (t / d) ** 2.4)
def chime(notes=(1318.5, 1760.0), gap=0.11, d=0.9):
    t = t_(d + gap * len(notes)); x = np.zeros(len(t))
    for i, f in enumerate(notes):
        tt = t - i * gap; m = tt >= 0
        x += np.where(m, (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-np.maximum(tt, 0) * 6.5) * np.minimum(1, np.maximum(tt, 0) / 0.004), 0)
    return norm(x)
def blip(f=1750):
    t = t_(0.22); x = np.zeros(len(t))
    for at in (0.0, 0.095):
        tt = t - at; m = (tt >= 0) & (tt < 0.055)
        x += np.where(m, np.sin(2 * np.pi * f * tt) * np.sin(np.pi * np.clip(tt / 0.055, 0, 1)) ** 0.5, 0)
    return norm(x)
def scribble(d=0.9):
    t = t_(d); x = bp(rng.standard_normal(len(t)), 1400, 5200)
    trem = 0.55 + 0.45 * np.sin(2 * np.pi * 17 * t + 2 * np.sin(2 * np.pi * 3 * t))
    return norm(x * trem * np.sin(np.pi * t / d) ** 1.2)
def click():
    t = t_(0.08); f = 330 * (0.45) ** (t / 0.08)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 60) + 0.5 * tick(2400)[:len(t)] if len(tick(2400)) >= len(t) else np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 60))

def put(name, at, x, db, pan=0.0, peak_at=None):
    """place mono sound x so that it starts at `at` (or its loudest point lands on `peak_at`)"""
    if peak_at is not None: at = peak_at - np.argmax(np.abs(x)) / SR
    g = 10 ** (db / 20); i = int(round(at * SR));
    if i < 0: x = x[-i:]; i = 0
    x = x[:max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    bus[i:i + len(x), 0] += x * g * l * 1.414; bus[i:i + len(x), 1] += x * g * r * 1.414
    log.append((round(at, 2), name, db))

DROP, S3, S4, S5, S6, S7, S8 = 2.02, 6.03, 10.03, 14.02, 18.01, 22.02, 26.01
H = lambda d, k: d + [0, 1.0, 1.75, 2.5, 3.25][k]

# --- hook: boring feed flicks past and decays to a stop on the drop
put('hook 1', 0.10, swish(0.42, 2600), -18, -0.3)
put('hook 2', 0.30, swish(0.42, 2900), -19, 0.3)
put('hook 3', 0.50, swish(0.42, 2700), -19, 0.0)
put('underline', 1.02, swish(0.34, 3600), -20, 0.4)
for k in np.arange(0.5, 5.0, 0.5):
    tk = DROP * (1 - (1 - k * 1040 / 5200) ** (1 / 3))
    put('scroll tick', tk, tick(1500 + 120 * k), -15 if k % 1 == 0 else -21, 0.15 * (-1) ** int(k * 2))
put('riser', 0, riser(0.9), -12, peak_at=DROP - 0.015)
put('hook out', DROP - 0.32, swish(0.3, 2200), -18)
put('finger in', DROP - 0.42, swish(0.3, 2400), -21, 0.2)
put('stop tap', DROP - 0.14, click(), -5)
# --- the stop
put('shutter', DROP - 0.005, shutter(), -6)
put('boom', DROP, boom(), -6)
put('burst open', DROP, whoosh(0.7, 0.25, 400, 7000), -13)
put('they 1', DROP + 0.42, swish(0.42, 2600), -19, -0.2)
put('they 2', H(DROP, 1) - 0.06, swish(0.42, 2900), -19, 0.2)
put('logo draw', H(DROP, 2) - 0.08, swish(0.75, 3200), -14, -0.2)
put('aperture', H(DROP, 2) - 0.08 + 0.95 / 1.15, pop(900, 420, 0.07), -19)
put('subtitle', H(DROP, 3) - 0.06, chime((1568.0, 2093.0), 0.09, 0.7), -11)
put('cities', H(DROP, 4) - 0.04, pop(520, 300, 0.07), -17)
# --- swipes between posts
for name, t, pan in (('p1', S3, -0.2), ('p2', S4, 0.2), ('p3', S5, -0.2), ('p4', S6, 0.2), ('p5', S7, 0.0)):
    put('swipe ' + name, 0, whoosh(0.5, 0.72, 220, 6500), -11, pan, peak_at=t - 0.03)
    put('land ' + name, t, thud(), -9)
    put('caption ' + name, t + 0.06, swish(0.38, 2700), -21, -0.3)
# P1 business
put('panel A', S3 - 0.12, swish(0.5, 2000), -16, 0.5)
put('panel B', H(S3, 1) - 0.12, swish(0.5, 2200), -16, -0.5)
put('chip A', S3 + 0.42, pop(520, 300, 0.07), -18, -0.4)
put('chip B', H(S3, 1) + 0.42, pop(520, 300, 0.07), -18, -0.4)
put('sell hit', H(S3, 2) - 0.02, pop(700, 260, 0.1), -9)
for i, t in enumerate((H(S3, 2) + 0.12, H(S3, 3) - 0.02, H(S3, 4) - 0.02)):
    put('platform', t, pop(420 + 90 * i, 700 + 90 * i, 0.08), -14, -0.4 + 0.4 * i)
# P2 real estate
put('pill re', S4 + 0.55, pop(), -16, -0.4)
put('space hit', H(S4, 1) - 0.02, pop(700, 260, 0.1), -9)
put('defocus', H(S4, 2) - 0.08, whoosh(0.5, 0.3, 300, 3000), -15)
for k, pan in ((2, -0.4), (3, 0.4), (4, 0.0)):
    put('photo fly', H(S4, k) - 0.02, swish(0.3, 2100), -17, pan)
    put('photo slap', H(S4, k) + 0.2, thud(0.18, 160, 90), -11, pan)
    put('photo snap', H(S4, k) + 0.2, shutter(False), -15, pan)
# P3 social
put('phone up', S5 - 0.12, swish(0.5, 2000), -16)
put('fan out', H(S5, 1) - 0.04, whoosh(0.4, 0.4, 600, 7000), -14)
put('fan land L', H(S5, 1) + 0.18, pop(380, 640, 0.09), -15, -0.6)
put('fan land R', H(S5, 1) + 0.2, pop(400, 680, 0.09), -15, 0.6)
put('like 1', H(S5, 2), blip(2100), -16, 0.4); put('like 2', H(S5, 3), blip(2300), -16, 0.4); put('like 3', H(S5, 3) + 0.18, blip(2500), -18, 0.4)
for b, h in enumerate((H(S5, 2), H(S5, 3), H(S5, 4))):
    for i in range(4):
        put('count', h + i * 0.06, tick(1700 + 140 * (b * 4 + i)), -12 if i == 3 else -16)
# P4 private
put('focus beep', S6 + 0.48, blip(), -12, 0.1)
for t in (H(S6, 1), H(S6, 2)): put('portrait cut', t - 0.005, shutter(), -5)
for i in range(4): put('readout', S6 + 0.55 + 0.07 * i, tick(2600 + 200 * i), -22, -0.5)
put('film hit', H(S6, 3) - 0.02, pop(700, 260, 0.1), -9)
put('pill private', H(S6, 4) - 0.02, pop(), -15, -0.4)
# P5 one team
put('team 2', H(S7, 1) - 0.08, swish(0.38, 2900), -20, 0.3)
put('team 3', H(S7, 1) + 0.18, swish(0.38, 2600), -20, -0.3)
put('frame in', S7 + 0.5, pop(380, 640, 0.1), -14)
put('files hit', H(S7, 2) + 0.02, pop(700, 260, 0.1), -9)
put('morph 9:16', H(S7, 2) - 0.02, whoosh(0.45, 0.6, 500, 5000), -17, 0.2)
put('morph 1:1', H(S7, 3) - 0.02, whoosh(0.45, 0.6, 500, 5000), -17, -0.2)
for i, t in enumerate((H(S7, 3) + 0.12, H(S7, 3) + 0.28, H(S7, 4) - 0.02)):
    put('stat', t, pop(), -14, -0.4 + 0.4 * i)
# --- call to action
TAP, BLINK = H(S8, 2), H(S8, 4)
put('iris close', 0, whoosh(0.42, 0.85, 300, 6000), -11, peak_at=S8 - 0.03)
put('shutter cta', S8 - 0.005, shutter(), -6)
put('boom cta', S8, boom(1.1), -8)
put('iris open cta', S8, whoosh(0.7, 0.25, 500, 8000), -15)
put('logo draw 2', S8 + 0.16, swish(0.6, 3200), -14)
put('cta line 1', S8 + 0.42, swish(0.4, 2600), -19, -0.2)
put('cta line 2', S8 + 0.53, swish(0.4, 2900), -20, 0.2)
put('stop hit', H(S8, 1) - 0.1, pop(700, 260, 0.1), -9)
put('button in', H(S8, 1) - 0.02, pop(380, 640, 0.1), -10)
put('finger', TAP - 0.42, swish(0.36, 2400), -20, 0.4)
put('tap', TAP, click(), -4)
put('message chime', TAP + 0.07, chime(), -8)
put('number in', TAP + 0.16, swish(0.4, 2800), -20)
put('site', H(S8, 3) - 0.02, pop(520, 300, 0.07), -17)
put('logo blink', BLINK - 0.02, shutter(), -4)

pk = np.abs(bus).max(); print('sfx bus peak %.2f dBFS' % (20 * np.log10(pk)))
bus = np.tanh(bus * 1.0) ; pk = np.abs(bus).max()
if pk > 0.89: bus *= 0.89 / pk
wavfile.write('sfx.wav', SR, (bus * 32767).astype(np.int16))
print(len(log), 'sounds placed')
