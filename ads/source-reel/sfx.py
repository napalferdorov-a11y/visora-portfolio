"""Synthesised sound effects for the VISORA 20 s ad, placed on the same timeline as the animation."""
import numpy as np, scipy.signal as sg, os, subprocess
from scipy.io import wavfile
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR = 48000; DUR = 20.3; N = int(SR * DUR)
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


def imp(t,db=-7): put('impact',t,boom(1.0),db); put('imp click',t-0.004,thud(0.3,140,60),db-3)
def cam(t,db=-8,pan=0.0): put('shutter',t-0.004,shutter(),db,pan)
def wh(peak,db=-11,d=0.42,pan=0.0,lo=260,hi=7000): put('whoosh',0,whoosh(d,0.72,lo,hi),db,pan,peak_at=peak)
def sw(t,db=-19,pan=0.0,f=2800): put('swish',t,swish(0.4,f),db,pan)
# hook
wh(0.04,-13,0.3); imp(0.44,-6); cam(0.44,-7); imp(0.82,-8); cam(0.82,-8,0.2)
sw(0.86,-18,-0.3); sw(1.60,-18,0.3); put('riser',0,riser(0.8),-11,peak_at=3.57); sw(2.94,-19)
# the idea
put('cut',3.18,tick(1700),-11,-0.3); put('cut',3.37,tick(2000),-12,0.3)
imp(3.59,-6); wh(3.60,-13,0.3); put('thud',3.96,thud(),-8)
put('pen',4.02,scribble(0.7),-13,0.2); put('pop',4.77,pop(520,300,0.08),-12); sw(4.78,-18)
# the shoot
put('thud',5.55,thud(0.6,80,38),-8); sw(5.60,-19); put('cut',6.33,tick(1800),-13); put('thud',6.73,thud(0.5,90,42),-10)
wh(7.12,-8,0.46,0.3,300,8000); put('thud',7.10,thud(),-8); put('pop',7.92,pop(300,160,0.1),-15); put('pop',8.69,pop(300,160,0.1),-15)
# the result: camera shutters on the photos
imp(9.47,-8); cam(9.47,-5,-0.3); cam(9.69,-7,0.3); cam(9.88,-6,0.0)
sw(9.90,-18); cam(10.25,-7,0.2); put('thud',10.25,thud(),-9); wh(11.05,-15,0.3); wh(11.82,-15,0.3)
# tagline
put('riser',0,riser(0.6),-12,peak_at=12.61); imp(12.62,-6)
sw(12.66,-18,-0.3); sw(13.38,-18,0.3); sw(14.18,-18); put('hl',0,whoosh(0.34,0.6,900,9000),-12,peak_at=14.32); put('hl hit',14.24,pop(700,260,0.1),-11)
# call to action
wh(15.75,-10,0.5); imp(15.77,-6); cam(15.77,-8)
sw(15.86,-15,0.0,3200); sw(16.50,-18); put('btn',17.33,pop(380,640,0.1),-10); sw(17.72,-19); put('pop',18.12,pop(520,300,0.07),-15)
put('tap',18.90,click(),-5); put('chime',18.97,chime(),-9)
cam(19.66,-4); put('end hit',19.68,boom(0.6),-9)

pk=np.abs(bus).max(); bus=np.tanh(bus); pk=np.abs(bus).max()
if pk>0.89: bus*=0.89/pk
wavfile.write('sfx.wav',SR,(bus*32767).astype(np.int16)); print('events',len(log),'peak',round(20*np.log10(pk),1))
