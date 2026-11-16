"""Small helpers that write Lottie (Bodymovin) JSON: Sunroom's own animated stickers and titles.

Everything here is drawn from shapes and text, so the animations are ours to ship. Used by
make_lottie.py (the ones inside the app) and make_packs.py (the downloadable template packs).
"""
import json, math

FPS = 30

def static(v):
    return {"a": 0, "k": v}

def anim(keys, dims=None):
    """keys: [(frame, value), ...] with an ease-out-back feel by default. value is a number or a list."""
    out = []
    for i, (t, v) in enumerate(keys):
        val = v if isinstance(v, list) else [v]
        n = len(val)
        k = {"t": t, "s": val}
        if i < len(keys) - 1:
            k["i"] = {"x": [0.25] * n, "y": [1] * n}
            k["o"] = {"x": [0.45] * n, "y": [0] * n}
        out.append(k)
    return {"a": 1, "k": out}

def ease(keys, ix=0.25, iy=1.0, ox=0.45, oy=0.0):
    out = []
    for i, (t, v) in enumerate(keys):
        val = v if isinstance(v, list) else [v]
        n = len(val)
        k = {"t": t, "s": val}
        if i < len(keys) - 1:
            k["i"] = {"x": [ix] * n, "y": [iy] * n}
            k["o"] = {"x": [ox] * n, "y": [oy] * n}
        out.append(k)
    return {"a": 1, "k": out}

def transform(p=(0, 0), a=(0, 0), s=100, r=0, o=100):
    def val(x, dims):
        if isinstance(x, dict):
            return x
        if dims == 3 and isinstance(x, (int, float)):
            return static([x, x, 100])
        if dims == 3:
            return static(list(x) + [0] if len(x) == 2 else list(x))
        return static(x)
    return {"p": val(p, 3) if not isinstance(p, dict) else p, "a": val(a, 3), "s": val(s, 3) if not isinstance(s, dict) else s,
            "r": val(r, 1), "o": val(o, 1)}

def group_tr(p=(0, 0), s=100, r=0, o=100):
    t = transform(p, (0, 0), s, r, o)
    t["ty"] = "tr"
    return t

def fill(rgb, o=100):
    return {"ty": "fl", "c": static([rgb[0], rgb[1], rgb[2], 1]), "o": static(o) if not isinstance(o, dict) else o, "r": 1}

def stroke(rgb, w=8, o=100):
    return {"ty": "st", "c": static([rgb[0], rgb[1], rgb[2], 1]), "o": static(o), "w": static(w), "lc": 2, "lj": 2}

def ellipse(w, h, p=(0, 0)):
    return {"ty": "el", "p": static(list(p)), "s": static([w, h]) if not isinstance(w, dict) else w}

def rect(w, h, r=0, p=(0, 0)):
    return {"ty": "rc", "p": static(list(p)), "s": static([w, h]), "r": static(r)}

def star(points, outer, inner, p=(0, 0)):
    return {"ty": "sr", "sy": 1, "d": 1, "pt": static(points), "p": static(list(p)), "r": static(0),
            "ir": static(inner), "is": static(0), "or": static(outer), "os": static(0)}

def path(vertices, closed=False, ins=None, outs=None):
    n = len(vertices)
    return {"ty": "sh", "ks": static({"i": ins or [[0, 0]] * n, "o": outs or [[0, 0]] * n,
                                      "v": [list(v) for v in vertices], "c": closed})}

def smooth_path(vertices, closed=False, k=0.33):
    """A Catmull-Rom-ish smooth curve through the points."""
    n = len(vertices)
    ins, outs = [], []
    for i in range(n):
        prev = vertices[i - 1] if (i > 0 or closed) else vertices[i]
        nxt = vertices[(i + 1) % n] if (i < n - 1 or closed) else vertices[i]
        dx, dy = (nxt[0] - prev[0]) * k, (nxt[1] - prev[1]) * k
        ins.append([-dx, -dy]); outs.append([dx, dy])
    return path(vertices, closed, ins, outs)

def trim(end_keys, start=0):
    return {"ty": "tm", "s": static(start), "e": ease(end_keys) if isinstance(end_keys, list) else static(end_keys), "o": static(0), "m": 1}

def group(items, tr=None):
    return {"ty": "gr", "it": list(items) + [tr or group_tr()]}

def shape_layer(name, shapes, ks, ip=0, op=60, ind=1):
    return {"ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1, "ks": ks, "ao": 0, "shapes": shapes,
            "ip": ip, "op": op, "st": 0, "bm": 0}

FONTS = {
    "AvenirNext-Heavy": ("Avenir Next", "Heavy"),
    "Futura-Bold": ("Futura", "Bold"),
    "Didot-Bold": ("Didot", "Bold"),
    "MarkerFelt-Wide": ("Marker Felt", "Wide"),
    "SnellRoundhand-Bold": ("Snell Roundhand", "Bold"),
    "AvenirNext-DemiBold": ("Avenir Next", "Demi Bold"),
}

def text_layer(name, words, font="AvenirNext-Heavy", size=72, rgb=(1, 1, 1), ks=None, ip=0, op=60, ind=1, tracking=0):
    return {"ddd": 0, "ind": ind, "ty": 5, "nm": name, "sr": 1, "ks": ks or transform(), "ao": 0,
            "t": {"d": {"k": [{"s": {"s": size, "f": font, "t": words, "j": 2, "tr": tracking, "lh": size * 1.2, "ls": 0,
                                      "fc": [rgb[0], rgb[1], rgb[2]]}, "t": 0}]},
                  "p": {}, "m": {"g": 1, "a": static([0, 0])}, "a": []},
            "ip": ip, "op": op, "st": 0, "bm": 0}

def animation(name, w, h, frames, layers):
    # Lottie draws the first layer on top: callers list back to front, so reverse here.
    layers = list(reversed(layers))
    for i, l in enumerate(layers):
        l["ind"] = i + 1
        l.setdefault("op", frames)
    used = sorted({l["t"]["d"]["k"][0]["s"]["f"] for l in layers if l["ty"] == 5})
    out = {"v": "5.7.4", "fr": FPS, "ip": 0, "op": frames, "w": w, "h": h, "nm": name, "ddd": 0, "assets": [], "layers": layers}
    if used:
        out["fonts"] = {"list": [{"fName": f, "fFamily": FONTS.get(f, (f, "Regular"))[0], "fStyle": FONTS.get(f, (f, "Regular"))[1], "ascent": 75} for f in used]}
    return out

def dumps(a):
    return json.dumps(a, separators=(",", ":"))

# ---------------------------------------------------------------------------------------------
# Building blocks: each returns a whole animation.

def pop_in_out(frames, hold_from=10, out_at=None, overshoot=115):
    """Scale keys: pop in with an overshoot, hold, then shrink away."""
    out_at = out_at or frames - 8
    return ease([(0, [0, 0, 100]), (hold_from - 3, [overshoot, overshoot, 100]), (hold_from, [100, 100, 100]),
                 (out_at, [100, 100, 100]), (frames - 1, [0, 0, 100])])

def fade_keys(frames, fin=6, fout=6):
    return ease([(0, 0), (fin, 100), (frames - fout, 100), (frames - 1, 0)])

def pop_title(name, words, rgb=(1, 1, 1), shadow=(0, 0, 0), font="AvenirNext-Heavy", size=110, frames=75, w=900, h=360):
    ks = transform(p=(w / 2, h / 2 + size * 0.35), s=pop_in_out(frames), o=fade_keys(frames, 3, 6))
    back = transform(p=(w / 2 + 6, h / 2 + size * 0.35 + 8), s=pop_in_out(frames), o=ease([(0, 0), (4, 55), (frames - 6, 55), (frames - 1, 0)]))
    return animation(name, w, h, frames, [
        text_layer("Shadow", words, font, size, shadow, back),
        text_layer("Words", words, font, size, rgb, ks),
    ])

def sparkle_burst(name, rgb=(1, 0.86, 0.3), frames=45, w=512, h=512, count=6):
    layers = []
    for i in range(count):
        ang = i / count * math.tau
        dist = 150 + (i % 2) * 40
        x, y = w / 2 + math.cos(ang) * dist, h / 2 + math.sin(ang) * dist
        delay = (i % 3) * 3
        size = 70 if i % 2 == 0 else 44
        sc = ease([(delay, [0, 0, 100]), (delay + 9, [120, 120, 100]), (delay + 16, [90, 90, 100]), (frames - 1, [0, 0, 100])])
        rot = ease([(delay, 0), (frames - 1, 90)])
        layers.append(shape_layer(f"Spark {i}", [group([star(4, size, size * 0.28), fill(rgb)])],
                                  transform(p=(x, y), s=sc, r=rot)))
    core = ease([(0, [0, 0, 100]), (8, [130, 130, 100]), (14, [100, 100, 100]), (frames - 1, [0, 0, 100])])
    layers.append(shape_layer("Core", [group([star(4, 120, 30), fill((1, 1, 1))])], transform(p=(w / 2, h / 2), s=core, r=ease([(0, 0), (frames - 1, 45)]))))
    return animation(name, w, h, frames, layers)

HEART = [(0, 60), (-70, -10), (-40, -70), (0, -40), (40, -70), (70, -10)]

def heart_shape(scale=1.0):
    v = [(0, 95), (-100, -15), (-52, -82), (0, -48), (52, -82), (100, -15)]
    i = [(20, -20), (0, 45), (-30, 0), (-4, -22), (-28, 0), (0, -35)]
    o = [(-20, -20), (0, -35), (28, 0), (4, -22), (30, 0), (0, 45)]
    sc = lambda pts: [[x * scale, y * scale] for x, y in pts]
    return path(sc(v), True, sc(i), sc(o))

def heart_pop(name, rgb=(1, 0.27, 0.45), frames=60, w=512, h=512):
    layers = [shape_layer("Heart", [group([heart_shape(1.6), fill(rgb)])],
                          transform(p=(w / 2, h / 2 + 10), s=ease([(0, [0, 0, 100]), (8, [125, 125, 100]), (13, [95, 95, 100]), (18, [105, 105, 100]),
                                                                   (24, [100, 100, 100]), (frames - 8, [100, 100, 100]), (frames - 1, [0, 0, 100])])))]
    for i, (dx, delay) in enumerate([(-150, 6), (150, 10), (-90, 16), (110, 20)]):
        y0 = h / 2 + 40
        p = ease([(delay, [w / 2 + dx * 0.4, y0]), (frames - 1, [w / 2 + dx, y0 - 260])])
        layers.append(shape_layer(f"Little {i}", [group([heart_shape(0.45), fill(rgb)])],
                                  transform(p=p, s=ease([(delay, [0, 0, 100]), (delay + 8, [100, 100, 100]), (frames - 1, [60, 60, 100])]),
                                            o=ease([(delay, 0), (delay + 4, 100), (frames - 6, 100), (frames - 1, 0)]))))
    return animation(name, w, h, frames, layers)

def underline(name, rgb=(1, 0.55, 0.1), frames=45, w=800, h=200):
    pts = [(-330, 10), (-150, -12), (40, 6), (200, -10), (330, 4)]
    return animation(name, w, h, frames, [shape_layer("Swoosh", [group([smooth_path(pts), stroke(rgb, 22), trim([(0, 0), (16, 100)])])],
                                                       transform(p=(w / 2, h / 2), o=ease([(0, 100), (frames - 8, 100), (frames - 1, 0)])))])

def circle_highlight(name, rgb=(1, 0.3, 0.3), frames=45, w=600, h=420):
    pts = [(-220, 0), (-150, -150), (40, -175), (230, -60), (200, 120), (0, 165), (-200, 110), (-235, -20), (-180, -120)]
    return animation(name, w, h, frames, [shape_layer("Circle", [group([smooth_path(pts), stroke(rgb, 14), trim([(0, 0), (18, 100)])])],
                                                       transform(p=(w / 2, h / 2), r=-4, o=ease([(0, 100), (frames - 8, 100), (frames - 1, 0)])))])

def arrow(name, rgb=(1, 1, 1), frames=60, w=400, h=400):
    shaft = path([(0, -130), (0, 90)])
    head = path([(-70, 30), (0, 110), (70, 30)])
    bob = ease([(0, [w / 2, h / 2 - 30]), (15, [w / 2, h / 2 + 10]), (30, [w / 2, h / 2 - 30]), (45, [w / 2, h / 2 + 10]), (frames - 1, [w / 2, h / 2 - 30])])
    return animation(name, w, h, frames, [shape_layer("Arrow", [group([shaft, head, stroke(rgb, 26)])],
                                                       transform(p=bob, o=ease([(0, 0), (5, 100), (frames - 6, 100), (frames - 1, 0)])))])

def confetti(name, colors=((1, 0.3, 0.4), (1, 0.85, 0.2), (0.2, 0.75, 1), (0.4, 0.9, 0.5), (0.8, 0.4, 1)), frames=75, w=720, h=720, count=18):
    layers = []
    for i in range(count):
        x = 40 + (i * 397 % (w - 80))
        delay = (i * 7) % 20
        drift = ((i * 53) % 120) - 60
        p = ease([(delay, [x, -30]), (frames - 1, [x + drift, h + 30])], ix=0.5, iy=0.5, ox=0.5, oy=0.5)
        r = ease([(delay, (i * 37) % 360), (frames - 1, (i * 37) % 360 + 360 * (1 if i % 2 else -1))], ix=0.5, iy=0.5, ox=0.5, oy=0.5)
        c = colors[i % len(colors)]
        shape = rect(18, 30, 3) if i % 3 else ellipse(20, 20)
        layers.append(shape_layer(f"Bit {i}", [group([shape, fill(c)])], transform(p=p, r=r)))
    return animation(name, w, h, frames, layers)

def badge(name, words, bg=(1, 0.25, 0.3), fg=(1, 1, 1), font="AvenirNext-Heavy", size=78, frames=75, w=640, h=280, pulse=True):
    sc = ease([(0, [0, 0, 100]), (8, [112, 112, 100]), (13, [100, 100, 100])] +
              ([(28, [100, 100, 100]), (34, [106, 106, 100]), (40, [100, 100, 100])] if pulse else []) +
              [(frames - 8, [100, 100, 100]), (frames - 1, [0, 0, 100])])
    tw = max(260, len(words) * size * 0.62 + 90)
    pill = shape_layer("Pill", [group([rect(tw, size * 1.55, size * 0.78), fill(bg)])], transform(p=(w / 2, h / 2), s=sc))
    txt = text_layer("Words", words, font, size, fg, transform(p=(w / 2, h / 2 + size * 0.36), s=sc))
    return animation(name, w, h, frames, [pill, txt])

def lower_third(name, words, sub, bar=(1, 0.55, 0.1), frames=90, w=900, h=300):
    slide = ease([(0, [-w / 2, h / 2]), (12, [w / 2, h / 2]), (frames - 12, [w / 2, h / 2]), (frames - 1, [-w / 2, h / 2])])
    bar_l = shape_layer("Bar", [group([rect(16, 170, 0, (-w * 0.41 + 8, 0)), fill(bar)]), group([rect(w * 0.82, 170, 18), fill((0.06, 0.06, 0.08))])], transform(p=slide))
    t1 = text_layer("Name", words, "AvenirNext-Heavy", 64, (1, 1, 1), transform(p=ease([(4, [-w / 2, h / 2 - 2]), (16, [w / 2, h / 2 - 2]), (frames - 12, [w / 2, h / 2 - 2]), (frames - 1, [-w / 2, h / 2 - 2])])))
    t2 = text_layer("Title", sub, "AvenirNext-DemiBold", 34, bar, transform(p=ease([(6, [-w / 2, h / 2 + 48]), (18, [w / 2, h / 2 + 48]), (frames - 12, [w / 2, h / 2 + 48]), (frames - 1, [-w / 2, h / 2 + 48])])))
    return animation(name, w, h, frames, [bar_l, t1, t2])

def pin_drop(name, rgb=(1, 0.3, 0.3), frames=60, w=400, h=480):
    pin = path([[0, 150], [-95, -45], [0, -150], [95, -45]], True,
               [[25, -45], [0, 50], [-52, 0], [0, -58]], [[-25, -45], [0, -58], [52, 0], [0, 50]])
    drop = ease([(0, [w / 2, -150]), (12, [w / 2, h / 2 + 10]), (16, [w / 2, h / 2 - 15]), (20, [w / 2, h / 2]), (frames - 8, [w / 2, h / 2]), (frames - 1, [w / 2, h / 2])])
    squash = ease([(11, [100, 100, 100]), (13, [115, 85, 100]), (17, [95, 105, 100]), (21, [100, 100, 100])])
    return animation(name, w, h, frames, [
        shape_layer("Shadow", [group([ellipse(120, 26), fill((0, 0, 0), 35)])], transform(p=(w / 2, h / 2 + 160), s=ease([(0, [20, 20, 100]), (12, [100, 100, 100])]), o=fade_keys(frames, 10, 6))),
        shape_layer("Pin", [group([ellipse(70, 70, (0, -50)), fill((1, 1, 1))]), group([pin, fill(rgb)])], transform(p=drop, s=squash, o=ease([(0, 100), (frames - 6, 100), (frames - 1, 0)]))),
    ])

def balloons(name, colors=((1, 0.3, 0.45), (0.25, 0.7, 1), (1, 0.8, 0.2)), frames=90, w=600, h=800):
    layers = []
    for i, c in enumerate(colors):
        x = w * (0.25 + 0.25 * i)
        delay = i * 6
        rise = ease([(delay, [x, h + 200]), (frames - 1, [x + (i - 1) * 30, -120])], ix=0.4, iy=0.6, ox=0.4, oy=0.4)
        sway = ease([(0, -6), (frames // 2, 6), (frames - 1, -6)], ix=0.5, iy=0.5, ox=0.5, oy=0.5)
        layers.append(shape_layer(f"Balloon {i}", [
            # Shape groups draw first-on-top.
            group([ellipse(30, 50, (-35, -40)), fill((1, 1, 1), 45)]),
            group([ellipse(150, 180), fill(c)]),
            group([path([(0, 85), (8, 160), (-6, 210), (4, 260)]), stroke((0.9, 0.9, 0.9), 3)]),
        ], transform(p=rise, r=sway)))
    return animation(name, w, h, frames, layers)

def stars_rating(name, rgb=(1, 0.8, 0.15), frames=70, w=700, h=220):
    layers = []
    for i in range(5):
        d = i * 4
        layers.append(shape_layer(f"Star {i}", [group([star(5, 54, 24), fill(rgb)])],
                                  transform(p=(w / 2 + (i - 2) * 125, h / 2), s=ease([(d, [0, 0, 100]), (d + 7, [125, 125, 100]), (d + 12, [100, 100, 100]), (frames - 8, [100, 100, 100]), (frames - 1, [0, 0, 100])]),
                                            r=ease([(d, -40), (d + 12, 0)]))))
    return animation(name, w, h, frames, layers)

def steam(name, rgb=(1, 1, 1), frames=75, w=400, h=500):
    layers = []
    for i, x in enumerate((-80, 0, 80)):
        d = i * 8
        curve = smooth_path([(x, 180), (x - 30, 90), (x + 30, 0), (x - 25, -90), (x + 20, -180)])
        layers.append(shape_layer(f"Wisp {i}", [group([curve, stroke(rgb, 16, 70), trim([(d, 0), (d + 30, 100)])])],
                                  transform(p=ease([(0, [w / 2, h / 2 + 20]), (frames - 1, [w / 2, h / 2 - 30])]), o=ease([(d, 0), (d + 8, 80), (frames - 10, 60), (frames - 1, 0)]))))
    return animation(name, w, h, frames, layers)

def bolt(name, rgb=(1, 0.85, 0.1), frames=50, w=360, h=480):
    pts = [(30, -200), (-90, 20), (-10, 20), (-40, 200), (90, -30), (10, -30)]
    flick = ease([(0, 0), (3, 100), (6, 30), (9, 100), (frames - 8, 100), (frames - 1, 0)])
    return animation(name, w, h, frames, [shape_layer("Bolt", [group([path(pts, True), fill(rgb)])], transform(p=(w / 2, h / 2), s=ease([(0, [60, 60, 100]), (8, [110, 110, 100]), (12, [100, 100, 100])]), o=flick))])

def rings(name, rgb=(1, 0.82, 0.35), frames=75, w=520, h=400):
    a = ease([(0, [w / 2 - 260, h / 2]), (16, [w / 2 - 55, h / 2]), (frames - 1, [w / 2 - 55, h / 2])])
    b = ease([(0, [w / 2 + 260, h / 2]), (16, [w / 2 + 55, h / 2]), (frames - 1, [w / 2 + 55, h / 2])])
    ring = lambda: [group([ellipse(170, 170), stroke(rgb, 22)])]
    return animation(name, w, h, frames, [
        shape_layer("Left", ring(), transform(p=a, o=fade_keys(frames, 6, 8))),
        shape_layer("Right", ring(), transform(p=b, o=fade_keys(frames, 6, 8))),
        shape_layer("Spark", [group([star(4, 40, 10), fill((1, 1, 1))])], transform(p=(w / 2, h / 2 - 95), s=ease([(16, [0, 0, 100]), (22, [140, 140, 100]), (30, [0, 0, 100])]))),
    ])

def plane(name, rgb=(1, 1, 1), frames=90, w=900, h=500):
    trail = smooth_path([(-400, 150), (-200, 40), (0, 90), (200, -40), (400, -150)])
    body = path([(-50, -12), (40, -6), (60, 0), (40, 6), (-50, 12)], True)
    wing = path([(-5, 0), (-30, -55), (-12, -55), (25, 0), (-12, 55), (-30, 55)], True)
    fly = ease([(0, [w / 2 - 420, h / 2 + 160]), (frames - 1, [w / 2 + 420, h / 2 - 160])], ix=0.4, iy=0.6, ox=0.4, oy=0.4)
    return animation(name, w, h, frames, [
        shape_layer("Trail", [group([trail, {"ty": "st", "c": static([rgb[0], rgb[1], rgb[2], 1]), "o": static(80), "w": static(6), "lc": 2, "lj": 2, "d": [{"n": "d", "nm": "dash", "v": static(18)}, {"n": "g", "nm": "gap", "v": static(16)}]},
                                     trim([(0, 0), (frames - 1, 100)])])], transform(p=(w / 2, h / 2))),
        shape_layer("Plane", [group([body, wing, fill(rgb)])], transform(p=fly, r=-17)),
    ])

def counter_badge(name, words, bg=(0.15, 0.85, 0.5), frames=60, w=520, h=260):
    return badge(name, words, bg, (0.05, 0.05, 0.05), "Futura-Bold", 84, frames, w, h)
