"""Synthesised sound effects for the VISORA 20 s ad, placed on the same timeline as the animation."""
import numpy as np, scipy.signal as sg, os, subprocess
from scipy.io import wavfile
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR = 48000; DUR = 20.0; N = int(SR * DUR)
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

DROP, S3A, S3B, S3C, S4, HL, S5, TAP, BLINK = 3.30, 6.78, 8.38, 10.26, 11.86, 13.72, 15.32, 17.20, 18.80

# --- hook
put('line 1 in', 0.26, swish(0.42, 2600), -19, -0.3)
put('line 2 in', 0.50, swish(0.42, 3000), -20, 0.3)
put('count 3', 1.25, tick(1500), -9); put('count 2', 1.95, tick(1800), -9); put('count 1', 2.65, tick(2150), -8)
put('riser', 0, riser(0.80), -12, peak_at=DROP - 0.015)
put('text out', 2.98, swish(0.3, 2200), -18)
# --- drop: shutter opens on the footage
put('shutter', DROP - 0.005, shutter(), -6)
put('boom', DROP, boom(), -7)
put('iris open', DROP, whoosh(0.7, 0.25, 400, 7000), -15)
put('logo draw', DROP + 0.12, swish(0.75, 3200), -14, -0.2)
put('aperture', DROP + 0.95, pop(900, 420, 0.07), -20)
put('subtitle', 4.88, chime((1568.0, 2093.0), 0.09, 0.7), -11)
# --- services
for name, t, pan in (('to 01', S3A, -0.25), ('to 02', S3B, 0.25), ('to 03', S3C, -0.25), ('to tagline', S4, 0.0)):
    put('whoosh ' + name, 0, whoosh(0.5, 0.72, 220, 6500), -11, pan, peak_at=t - 0.03)
    put('thud ' + name, t, thud(), -9)
put('focus beep', S3A + 0.50, blip(), -12, 0.1)
put('pill 01', S3A + 0.40, pop(), -18, -0.4)
put('arches draw', S3B + 0.12, scribble(0.95), -14)
put('sun', S3B + 0.42, pop(420, 620, 0.09), -19, 0.4)
put('pill 02', S3B + 0.42 + 0.3, pop(), -18, -0.4)
for i, f in enumerate((520, 660, 820)): put('format %d' % (i + 1), S3C + 0.18 + i * 0.13, pop(f, f * 0.55, 0.08), -10, (-0.4, 0.3, 0.1)[i])
put('timeline', S3C + 0.44, scribble(0.5), -17)
put('pill 03', S3C + 0.74, pop(), -18, -0.4)
# --- tagline
put('strip open', S4, whoosh(0.6, 0.2, 180, 4500), -10)
put('tag line 1', S4 + 0.30, swish(0.4, 2600), -19, -0.3)
put('tag line 2', S4 + 0.62, swish(0.4, 2900), -19, 0.3)
put('highlight', 0, whoosh(0.34, 0.6, 900, 9000), -12, peak_at=HL + 0.08)
put('highlight hit', HL, pop(700, 260, 0.1), -9)
# --- call to action
put('iris close', 0, whoosh(0.42, 0.85, 300, 6000), -11, peak_at=S5 - 0.03)
put('shutter cta', S5 - 0.005, shutter(), -6)
put('boom cta', S5, boom(1.1), -9)
put('iris open cta', S5, whoosh(0.7, 0.25, 500, 8000), -15)
put('logo draw 2', S5 + 0.16, swish(0.6, 3200), -14)
put('cta line 1', S5 + 0.42, swish(0.4, 2600), -19, -0.2)
put('cta line 2', S5 + 0.53, swish(0.4, 2900), -20, 0.2)
put('button in', S5 + 1.07, pop(380, 640, 0.1), -9)
put('finger', TAP - 0.42, swish(0.36, 2400), -20, 0.4)
put('tap', TAP, click(), -4)
put('message chime', TAP + 0.07, chime(), -8)
put('number in', TAP + 0.16, swish(0.4, 2800), -20)
put('logo blink', BLINK - 0.02, shutter(), -3)

pk = np.abs(bus).max(); print('sfx bus peak %.2f dBFS' % (20 * np.log10(pk)))
bus = np.tanh(bus * 1.0) ; pk = np.abs(bus).max()
if pk > 0.89: bus *= 0.89 / pk
wavfile.write('sfx.wav', SR, (bus * 32767).astype(np.int16))
for l in sorted(log): print('%6.2fs  %-18s %4d dB' % l)
