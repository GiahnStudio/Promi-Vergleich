"""Race-Charts: Linien über die Zeit, Comic-Köpfe an der Spitze, Überhol-Momente.
Bewegung ab Frame 0, Headline als Hook oben, Callouts bei Schlüsselmomenten, Frage am Ende."""
import os, sys, math, wave, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import data_videos as dv
from data_videos import W, H, FPS, font, ease, ease_io, layer_text, wrap
import cartoon

BG = (6, 6, 10); GRID = (34, 36, 46); FG = (248, 246, 240); MUTED = (150, 152, 168)
def fD(s): return font("InterDisplay-Bold.otf", int(s))
fHead = fD(66); fKick = font("Inter-Bold.otf", 34); fAxis = font("Inter-SemiBold.otf", 30)
fLab = font("Inter-Bold.otf", 34); fVal = fD(46); fYear = fD(120); fCall = fD(50); fTiny = font("Inter-Medium.otf", 26)
fBrand = font("Inter-Bold.otf", 28); fQ = fD(64); fBody = font("Inter-Medium.otf", 40)

L, R, T, B = 130, 820, 600, 1290   # Chart-Fläche (rechts Platz für Köpfe + Labels)

def series_value(p, x):
    if "events" in p:  # Stufen: jedes Event +1 (oder (x, delta))
        v = p.get("start", 0)
        for e in p["events"]:
            ex, dvv = (e if isinstance(e, tuple) else (e, 1))
            if ex <= x: v += dvv
        return v
    pts = p["points"]
    if x <= pts[0][0]: return pts[0][1]
    for (x0, v0), (x1, v1) in zip(pts, pts[1:]):
        if x <= x1: return v0 + (v1 - v0) * (x - x0) / (x1 - x0)
    return pts[-1][1]

def path(p, x0, xc, X, Y):
    if "events" in p:
        v = p.get("start", 0); pts = [(X(x0), Y(v))]
        for e in p["events"]:
            ex, dvv = (e if isinstance(e, tuple) else (e, 1))
            if ex > xc: break
            if ex < x0: v += dvv; continue
            pts += [(X(ex), Y(v))]; v += dvv; pts += [(X(ex), Y(v))]
        return pts + [(X(xc), Y(v))]
    pts = [(X(x), Y(v)) for x, v in p["points"] if x <= xc]
    return pts + [(X(xc), Y(series_value(p, xc)))]

class Clock:
    """Zeit → x mit Zeitlupe in 'slow'-Abschnitten."""
    def __init__(self, r):
        self.x0, self.x1 = r["xrange"]; self.dur = r["race_dur"]; self.slow = r.get("slow", [])
        xs = np.linspace(self.x0, self.x1, 2000)
        w = np.array([max([f for a, b, f in self.slow if a <= x <= b] + [1.0]) for x in xs])
        self.cum = np.concatenate([[0], np.cumsum(w[1:] * np.diff(xs))]); self.cum /= self.cum[-1]; self.xs = xs
    def x(self, t):
        u = ease_io(t / self.dur) * 0.15 + (min(max(t / self.dur, 0), 1)) * 0.85
        return float(np.interp(u, self.cum, self.xs))

def frame(r, t, clock):
    img = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(img)
    x0, x1 = r["xrange"]; ymax = r["ymax"]
    X = lambda x: L + (x - x0) / (x1 - x0) * (R - L)
    Y = lambda v: B - v / ymax * (B - T)
    xc = clock.x(min(t, r["race_dur"]))
    # Kopfzeile
    layer_text(img, (W / 2, 190), r["kicker"], fKick, r.get("acc", (255, 200, 60)), 1, "ma")
    for i, ln in enumerate(wrap(d, r["headline"], fHead, W - 140)):
        layer_text(img, (W / 2, 250 + i * 78), ln, fHead, FG, 1, "ma")
    layer_text(img, (W / 2, 250 + 78 * len(wrap(d, r["headline"], fHead, W - 140)) + 10), r["unit"], fBody, MUTED, 1, "ma")
    # Raster
    for g in r["grid"]:
        d.line([L, Y(g), R + 40, Y(g)], fill=GRID, width=2)
        d.text((L - 18, Y(g)), r.get("gfmt", str)(g), font=fAxis, fill=MUTED, anchor="rm")
    for yt in r["ticks"]:
        d.text((X(yt), B + 22), str(yt), font=fAxis, fill=MUTED, anchor="ma")
    # Linien (Glow + Linie)
    glow = Image.new("RGBA", img.size); gd = ImageDraw.Draw(glow)
    paths = [path(p, x0, xc, X, Y) for p in r["people"]]
    for p, pts in zip(r["people"], paths): gd.line(pts, fill=p["col"] + (140,), width=20, joint="curve")
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(img)
    for p, pts in zip(r["people"], paths): d.line(pts, fill=p["col"], width=8, joint="curve")
    # Köpfe mit Mindestabstand
    vals = [series_value(p, xc) for p in r["people"]]
    lead = max(vals)
    heads = sorted([(Y(v), i) for i, v in enumerate(vals)])
    ys, minsp = [], 104
    for y, i in heads:
        if ys and y - ys[-1][0] < minsp: y = ys[-1][0] + minsp
        ys.append((y, i))
    shift = max(0, ys[-1][0] - (B - 20)) if ys else 0
    for y, i in ys:
        p = r["people"][i]; hx, hy = paths[i][-1]; y -= shift
        d.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=p["col"])
        cx = hx + 58
        if abs(y - hy) > 4: d.line([hx, hy, cx - 40, y], fill=p["col"], width=3)
        av = cartoon.rendered(cartoon.look_key(p["look"], tuple(int(c * 0.55) for c in p["col"])), 92).copy()
        img.alpha_composite(av, (int(cx - 46), int(y - 46))); d = ImageDraw.Draw(img)
        ring = (255, 210, 70) if vals[i] == lead and vals.count(lead) == 1 and lead > 0 else p["col"]
        d.ellipse([cx - 50, y - 50, cx + 50, y + 50], outline=ring, width=6)
        lx = cx + 62
        d.text((lx, y - 34), p["short"], font=fLab, fill=FG)
        d.text((lx, y + 2), r.get("vfmt", lambda v: str(int(round(v))))(vals[i]), font=fVal, fill=p["col"])
    # Jahr
    layer_text(img, (W / 2, B + 80), r.get("xfmt", lambda x: str(int(x)))(xc), fYear, FG, 1, "ma")
    # Callouts
    for c in r["callouts"]:
        cx_, txt = c[0], c[1]; dur = c[2] if len(c) > 2 else 1.8
        tc = next((tt / FPS for tt in range(int(r["race_dur"] * FPS) + 1) if clock.x(tt / FPS) >= cx_), None)
        if tc is None or not (tc <= t < tc + dur): continue
        a = ease((t - tc) / 0.2) * (1 - ease((t - tc - dur + 0.25) / 0.25)); sc = 1 + 0.15 * (1 - ease((t - tc) / 0.25))
        P = Image.new("RGBA", img.size); pd = ImageDraw.Draw(P); f = fD(50 * sc)
        tw = pd.textlength(txt, font=f); bx0, bx1 = W / 2 - tw / 2 - 34, W / 2 + tw / 2 + 34
        pd.rounded_rectangle([bx0, 1495, bx1, 1595], radius=50, fill=(255, 210, 70, int(240 * a)))
        img.alpha_composite(P); layer_text(img, (W / 2, 1545), txt, f, BG, a, "mm")
    # Ende: Frage
    te = r["race_dur"] + 0.5
    if t > te:
        a = ease((t - te) / 0.4)
        for i, ln in enumerate(wrap(d, r["end_q"], fQ, W - 140)):
            layer_text(img, (W / 2, 1480 + i * 76), ln, fQ, FG, a, "ma")
        layer_text(img, (W / 2, 1480 + 76 * len(wrap(d, r["end_q"], fQ, W - 140)) + 20), "Comment below 👇".replace(" 👇", ""), fBody, MUTED, ease((t - te - 0.4) / 0.4), "ma")
    # Rahmen
    d = ImageDraw.Draw(img); total = r["race_dur"] + r["end_dur"]
    d.rectangle([0, 0, W, 8], fill=(30, 30, 40)); d.rectangle([0, 0, int(W * min(t / total, 1)), 8], fill=(255, 210, 70))
    w = d.textlength("WHO HAS MORE?", font=fBrand); d.text(((W - w) / 2, 120), "WHO HAS MORE?", font=fBrand, fill=(110, 110, 125))
    src = "Source: " + r["source"]
    for i, ln in enumerate(wrap(d, src, fTiny, W - 180)):
        lw = d.textlength(ln, font=fTiny); d.text(((W - lw) / 2, H - 170 + i * 34), ln, font=fTiny, fill=(100, 100, 115))
    return img.convert("RGB")

def audio(r, clock, path):
    total = r["race_dur"] + r["end_dur"]
    dv.audio({"scenes": [{"type": "hook", "dur": total}]}, path)
    with wave.open(path) as w: sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32767
    a *= 0.75
    ts = np.arange(int(r["race_dur"] * FPS) + 1) / FPS; xs = np.array([clock.x(t) for t in ts])
    for p in r["people"]:  # „Plopp“ bei jedem Titel
        for e in p.get("events", []):
            ex = e[0] if isinstance(e, tuple) else e
            k = np.searchsorted(xs, ex)
            if k >= len(ts): continue
            st = int(ts[k] * sr); ln = int(0.12 * sr); lo = np.arange(ln) / sr
            if st + ln < len(a): a[st:st + ln] += np.sin(2 * np.pi * (660 + 40 * (hash(p["short"]) % 5)) * lo) * np.exp(-lo * 30) * 0.18
    for c in r["callouts"]:  # Akzent bei Callouts
        k = np.searchsorted(xs, c[0])
        if k >= len(ts): continue
        st = int(ts[k] * sr); ln = int(0.4 * sr); lo = np.arange(ln) / sr
        if st + ln < len(a): a[st:st + ln] += (np.sin(2 * np.pi * 880 * lo) + 0.5 * np.sin(2 * np.pi * 1320 * lo)) * np.exp(-lo * 9) * 0.22
    a = a / np.max(np.abs(a)) * 0.85
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a * 32767).astype(np.int16).tobytes())

def render(r, out_dir):
    os.makedirs(out_dir, exist_ok=True); os.makedirs(dv.SCR, exist_ok=True)
    clock = Clock(r); total = r["race_dur"] + r["end_dur"]
    wav = f"{dv.SCR}/{r['slug']}.wav"; audio(r, clock, wav)
    out = f"{out_dir}/{r['slug']}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)): p.stdin.write(frame(r, i / FPS, clock).tobytes())
    p.stdin.close(); p.wait()
    return out, total
