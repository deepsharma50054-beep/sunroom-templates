#!/usr/bin/env python3
"""Writes catalog.json: Sunroom's online Reel templates.

Each template is a small recipe (rhythm, moves, transitions, look, words) that Sunroom draws with
its own engine. Edit the lists below, run `python3 make_catalog.py`, and publish catalog.json.
Fields Sunroom doesn't know are ignored; numbers are limited by the app when it reads them.
"""
import json, datetime, os

def text(label, placeholder, font="Avenir Next", size=0.1, y=0.5, color=(1, 1, 1), motion="none",
         start=0, beats=8, step=1, bold=True, outline=0.0, shadow=0.5, glow=0.0, glow_color=None,
         gradient=None, tracking=0.0, italic=False, depth=0.0, depth_color=None):
    layer = {"text": placeholder, "fontFamily": font, "bold": bold, "italic": italic, "size": size,
             "color": {"r": color[0], "g": color[1], "b": color[2]}, "center": {"x": 0.5, "y": y},
             "outline": outline, "outlineColor": {"r": 0, "g": 0, "b": 0}, "shadow": shadow, "glow": glow,
             "tracking": tracking, "depth": depth}
    if glow_color: layer["glowColor"] = {"r": glow_color[0], "g": glow_color[1], "b": glow_color[2]}
    if gradient: layer["gradient"] = {"r": gradient[0], "g": gradient[1], "b": gradient[2]}
    if depth_color: layer["depthColor"] = {"r": depth_color[0], "g": depth_color[1], "b": depth_color[2]}
    return {"label": label, "placeholder": placeholder, "layer": layer, "startBeats": start, "beats": beats,
            "motion": motion, "stepBeats": step}

def slots(beats, effects, transitions):
    n = max(len(beats), len(effects), len(transitions))
    return [{"beats": beats[i % len(beats)], "effect": effects[i % len(effects)],
             "transition": transitions[i % len(transitions)]} for i in range(n)]

def template(key, name, category, family="classic", symbol="sparkles", hue=0.6, bpm=120, length=15,
             beats=(2,), effects=("none",), transitions=("none",), tsec=0.3, look="none", look_amount=1.0,
             texts=(), captions=None, card=None, labels=None, notes=""):
    t = {"key": key, "name": name, "category": category, "family": family, "symbol": symbol, "hue": hue,
         "bpm": bpm, "length": length, "loops": True, "slots": slots(list(beats), list(effects), list(transitions)),
         "transitionSeconds": tsec, "look": look, "lookAmount": look_amount, "texts": list(texts), "notes": notes}
    if captions: t["captions"] = captions
    if card: t["card"] = card
    if labels: t["labels"] = labels
    return t

def card(tilt=4, width=0.8, border=0.045, bottom=0.2, paper=(0.98, 0.97, 0.95), backdrop=(0.93, 0.89, 0.84)):
    return {"tilt": tilt, "width": width, "border": border, "bottom": bottom,
            "paper": {"r": paper[0], "g": paper[1], "b": paper[2]}, "backdrop": {"r": backdrop[0], "g": backdrop[1], "b": backdrop[2]}}

YELLOW = (1, 0.88, 0.15); PINK = (1, 0.35, 0.7); CYAN = (0.2, 0.85, 1); RED = (1, 0.25, 0.2); GOLD = (1, 0.8, 0.35)
K, P, B, S = "Kinetic Text", "Photo Dump", "Before & After", "Seasonal"

T = []
# --- Kinetic text: words land on the beat ---------------------------------------------------
T += [
    template("kinetic-say-it-loud", "Say It Loud", K, "kinetic", "megaphone", 0.02, 128, 15, (2,), ("punch", "none"), ("flash", "none"),
             0.2, "naturalPop", texts=[text("Words", "SAY IT LOUD AND PROUD", "Impact", 0.16, 0.5, YELLOW, "slam", 0, 10, 1, False, 0.5)],
             notes="Big words slam in one at a time on the beat."),
    template("kinetic-hot-take", "Hot Take", K, "kinetic", "flame", 0.03, 140, 12, (1,), ("shake", "punch"), ("flash",), 0.15, "cyberpunk",
             texts=[text("Words", "HOT TAKE INCOMING", "Futura", 0.14, 0.45, RED, "slam", 0, 6, 1, True, 0.4),
                    text("Under", "hear me out", "Avenir Next", 0.05, 0.62, (1, 1, 1), "pop", 6, 18)],
             notes="Fast shakes and a red slam for opinions."),
    template("kinetic-pov", "POV", K, "kinetic", "eye", 0.75, 110, 15, (4,), ("push",), ("dissolve",), 0.5, "moody",
             texts=[text("Words", "POV: you finally did it", "Avenir Next", 0.07, 0.3, (1, 1, 1), "typewriter", 0, 16)],
             notes="Typewriter words over slow pushes."),
    template("kinetic-three-things", "3 Things", K, "kinetic", "list.number", 0.55, 120, 18, (4,), ("push", "pull"), ("whip",), 0.35, "cleanBright",
             texts=[text("List", "Three things\nthat changed\nmy life", "Avenir Next", 0.08, 0.5, (1, 1, 1), "stack", 0, 12, 2, True, 0.3)],
             notes="Lines build up one at a time."),
    template("kinetic-motivation", "Monday Motivation", K, "kinetic", "bolt.heart", 0.08, 124, 15, (2,), ("punch", "push"), ("zoom", "flash"), 0.25, "goldenHour",
             texts=[text("Words", "WAKE UP. SHOW UP. NEVER GIVE UP.", "Futura", 0.13, 0.5, GOLD, "slam", 0, 14, 1, True, 0.35)]),
    template("kinetic-quote", "Quote of the Day", K, "kinetic", "quote.opening", 0.62, 90, 15, (8,), ("drift",), ("dissolve",), 0.8, "matte",
             texts=[text("Quote", "Small steps every day", "Didot", 0.08, 0.45, (1, 1, 1), "typewriter", 0, 20, 1, False, 0, 0.6),
                    text("Author", "— you", "Didot", 0.045, 0.6, (1, 1, 1), "pop", 12, 20, 1, False)],
             notes="Calm typewriter quote with a credit."),
    template("kinetic-countdown", "3, 2, 1 Go", K, "kinetic", "timer", 0.0, 128, 12, (1, 1, 1, 4), ("punch", "punch", "punch", "push"), ("flash",), 0.15, "neonNight",
             texts=[text("Count", "3 2 1 GO!", "Impact", 0.3, 0.5, (1, 1, 1), "slam", 0, 6, 1, False, 0.4, 0.4, 0.8, CYAN)],
             notes="A countdown that lands on the drop."),
    template("kinetic-announcement", "Big News", K, "kinetic", "sparkles", 0.85, 120, 15, (2,), ("push", "punch"), ("glitch", "none"), 0.25, "pastelDream",
             texts=[text("Words", "WE HAVE BIG NEWS", "Avenir Next", 0.14, 0.5, PINK, "slam", 0, 8, 1, True, 0.3, 0.4, 0, None, (1, 0.75, 0.3))],
             notes="Gradient words for launches and reveals."),
    template("kinetic-lyrics", "Lyric Drop", K, "kinetic", "music.mic", 0.7, 100, 20, (4,), ("drift", "push"), ("dissolve",), 0.5, "moody",
             texts=[text("Lyrics", "and I keep coming back\nto this feeling", "Snell Roundhand", 0.09, 0.55, (1, 1, 1), "stack", 0, 16, 4, True, 0, 0.5, 0.5, (1, 0.85, 0.9))]),
    template("kinetic-day-in-life", "Day in My Life", K, "kinetic", "sun.max", 0.12, 118, 20, (2, 2, 4), ("push", "drift", "pull"), ("slideLeft", "none"), 0.3, "naturalPop",
             texts=[text("Title", "a day in my life", "American Typewriter", 0.07, 0.2, (1, 1, 1), "typewriter", 0, 12, 1, False, 0, 0.6)]),
    template("kinetic-glitch-words", "Glitch Words", K, "kinetic", "waveform.path.ecg", 0.5, 140, 12, (1,), ("shake", "none"), ("glitch",), 0.2, "cyberpunk",
             texts=[text("Words", "ERROR 404 SLEEP NOT FOUND", "Menlo", 0.09, 0.5, (0.3, 1, 0.45), "slam", 0, 10, 1, True, 0, 0.3, 0.7, (0.1, 0.9, 0.3))]),
    template("kinetic-rules", "Rules I Live By", K, "kinetic", "checklist", 0.35, 112, 18, (4,), ("pull", "push"), ("whip",), 0.3, "fadedFilm",
             texts=[text("Rules", "1. drink water\n2. go outside\n3. call your mom", "Avenir Next", 0.065, 0.5, (1, 1, 1), "stack", 0, 16, 3, True, 0.25)]),
]
# --- Photo dump: printed photos dropped on a table --------------------------------------------
T += [
    template("dump-classic", "Photo Dump", P, "photoDump", "photo.stack", 0.08, 120, 15, (2,), ("drop",), ("none",), 0, "fadedFilm",
             card=card(), texts=[text("Title", "photo dump", "Snell Roundhand", 0.06, 0.9, (0.25, 0.2, 0.18), "pop", 0, 8, 1, True, 0, 0)],
             notes="Each shot drops in as a printed photo."),
    template("dump-summer", "Summer Dump", P, "photoDump", "sun.max", 0.12, 126, 15, (2,), ("drop",), ("none",), 0, "goldenHour",
             card=card(5, backdrop=(1, 0.85, 0.6)), texts=[text("Title", "summer '26", "Marker Felt", 0.07, 0.9, (0.6, 0.25, 0.1), "pop", 0, 8, 1, True, 0, 0)]),
    template("dump-film-roll", "Film Roll", P, "photoDump", "film", 0.6, 100, 18, (3,), ("drop",), ("none",), 0, "portra",
             card=card(3, 0.82, 0.04, 0.04, (0.08, 0.08, 0.08), (0.12, 0.12, 0.13)), notes="Dark frames on a dark table."),
    template("dump-scrapbook", "Scrapbook", P, "photoDump", "book", 0.95, 110, 18, (3,), ("drop",), ("none",), 0, "vintage70s",
             card=card(7, 0.74, 0.05, 0.22, (1, 0.98, 0.92), (0.82, 0.88, 0.8)),
             texts=[text("Title", "our little scrapbook", "Bradley Hand", 0.055, 0.1, (0.2, 0.3, 0.25), "typewriter", 0, 10, 1, True, 0, 0)]),
    template("dump-travel", "Travel Diary", P, "photoDump", "airplane", 0.55, 116, 20, (2, 3), ("drop",), ("none",), 0, "kodachrome",
             card=card(4, backdrop=(0.78, 0.86, 0.92)), texts=[text("Place", "where to next?", "American Typewriter", 0.05, 0.9, (0.15, 0.2, 0.3), "typewriter", 0, 12, 1, False, 0, 0)]),
    template("dump-besties", "Besties", P, "photoDump", "heart", 0.92, 124, 15, (2,), ("drop",), ("none",), 0, "pastelDream",
             card=card(6, backdrop=(1, 0.86, 0.9)), texts=[text("Title", "my people", "Marker Felt", 0.07, 0.9, (0.8, 0.2, 0.45), "pop", 0, 8)]),
    template("dump-birthday", "Birthday Dump", P, "photoDump", "gift", 0.88, 128, 15, (2,), ("drop",), ("none",), 0, "naturalPop",
             card=card(5, backdrop=(1, 0.92, 0.6)), texts=[text("Title", "happy birthday!", "Marker Felt", 0.075, 0.1, (0.85, 0.25, 0.4), "slam", 0, 6, 1, True)]),
    template("dump-recap", "Month Recap", P, "photoDump", "calendar", 0.3, 120, 20, (2,), ("drop",), ("none",), 0, "matte",
             card=card(3, 0.78, backdrop=(0.9, 0.9, 0.88)), texts=[text("Month", "november recap", "Futura", 0.05, 0.92, (0.2, 0.2, 0.2), "typewriter", 0, 10, 1, True, 0, 0, tracking=0.15)]),
    template("dump-cozy", "Cozy Season", P, "photoDump", "cup.and.saucer", 0.07, 96, 18, (3,), ("drop",), ("none",), 0, "vintage70s",
             card=card(4, backdrop=(0.55, 0.38, 0.28)), texts=[text("Title", "cozy season", "Snell Roundhand", 0.07, 0.9, (1, 0.95, 0.88), "pop", 0, 8)]),
    template("dump-polaroid-wall", "Polaroid Wall", P, "photoDump", "square.grid.2x2", 0.0, 132, 12, (1,), ("drop",), ("none",), 0, "cleanBright",
             card=card(8, 0.7, backdrop=(0.96, 0.96, 0.96)), notes="Quick drops on every beat."),
]
# --- Before & after: the second shot wipes over the first -------------------------------------
BA = dict(beats=(4, 4), effects=("none", "push"), transitions=("flash", "splitReveal"), tsec=1.2)
T += [
    template("reveal-glow-up", "Glow Up", B, "beforeAfter", "sparkles", 0.85, 110, 16, look="naturalPop", **BA, notes="Pairs: before, then after wipes over it."),
    template("reveal-room", "Room Makeover", B, "beforeAfter", "sofa", 0.1, 100, 16, look="cleanBright", **BA, labels=["BEFORE", "AFTER"]),
    template("reveal-then-now", "Then & Now", B, "beforeAfter", "clock.arrow.circlepath", 0.08, 96, 16, look="fadedFilm", **BA, labels=["THEN", "NOW"]),
    template("reveal-edit", "Edit Reveal", B, "beforeAfter", "wand.and.stars", 0.6, 120, 12, look="tealOrange", **BA, labels=["RAW", "EDITED"]),
    template("reveal-fitness", "Fitness Journey", B, "beforeAfter", "figure.run", 0.02, 128, 16, look="moody", **BA, labels=["DAY 1", "DAY 90"]),
    template("reveal-recipe", "Recipe Result", B, "beforeAfter", "fork.knife", 0.1, 110, 16, look="goldenHour", **BA, labels=["INGREDIENTS", "RESULT"]),
    template("reveal-clean", "Clean With Me", B, "beforeAfter", "bubbles.and.sparkles", 0.5, 118, 16, look="arctic", **BA, labels=["MESSY", "CLEAN"]),
    template("reveal-hair", "New Look", B, "beforeAfter", "scissors", 0.9, 120, 16, look="pastelDream", **BA, labels=["BEFORE", "AFTER"]),
]
# --- Seasonal: beat cuts with themed words ----------------------------------------------------
T += [
    template("season-halloween", "Spooky Season", S, "classic", "moon.stars", 0.07, 120, 15, (2, 1, 1), ("shake", "punch", "push"), ("glitch", "flash", "dipToBlack"),
             0.25, "noir", texts=[text("Title", "SPOOKY SEASON", "Impact", 0.13, 0.5, (1, 0.5, 0.1), "slam", 0, 6, 1, False, 0.4, 0.4, 0.6, (1, 0.4, 0))],
             notes="Glitches and flashes for Halloween."),
    template("season-birthday", "Happy Birthday", S, "classic", "birthday.cake", 0.9, 124, 15, (2,), ("punch", "push"), ("flash", "circle"), 0.3, "pastelDream",
             texts=[text("Name", "Happy Birthday!", "Marker Felt", 0.1, 0.45, PINK, "slam", 0, 6, 1, True, 0.3)]),
    template("season-christmas", "Holiday Lights", S, "classic", "snowflake", 0.35, 108, 18, (4,), ("drift", "push"), ("blurZoom", "dissolve"), 0.6, "goldenHour",
             texts=[text("Title", "Merry & Bright", "Snell Roundhand", 0.1, 0.5, (1, 0.92, 0.75), "pop", 0, 10, 1, True, 0, 0.4, 0.7, (1, 0.8, 0.4))]),
    template("season-new-year", "New Year", S, "classic", "party.popper", 0.12, 128, 15, (1, 1, 2), ("punch",), ("flash", "spin"), 0.25, "neonNight",
             texts=[text("Count", "5 4 3 2 1 HAPPY NEW YEAR", "Futura", 0.14, 0.5, GOLD, "slam", 0, 10, 1, True, 0.3, 0.3, 0.6, (1, 0.7, 0.2))]),
    template("season-diwali", "Diwali Glow", S, "classic", "flame", 0.1, 110, 15, (2, 4), ("push", "drift"), ("blurZoom", "dissolve"), 0.5, "goldenHour",
             texts=[text("Title", "Happy Diwali", "Didot", 0.1, 0.5, (1, 0.82, 0.4), "pop", 0, 10, 1, True, 0, 0.4, 0.8, (1, 0.6, 0.1))]),
    template("season-holi", "Holi Colors", S, "classic", "paintpalette", 0.85, 128, 15, (1, 2), ("punch", "shake"), ("whip", "flash"), 0.25, "naturalPop",
             texts=[text("Title", "HAPPY HOLI", "Futura", 0.13, 0.5, (1, 0.3, 0.6), "slam", 0, 6, 1, True, 0.3, 0.3, 0, None, (1, 0.85, 0.2))]),
    template("season-eid", "Eid Mubarak", S, "classic", "moon.stars", 0.45, 96, 15, (4,), ("drift", "push"), ("dissolve",), 0.7, "goldenHour",
             texts=[text("Title", "Eid Mubarak", "Snell Roundhand", 0.1, 0.5, (1, 0.9, 0.7), "pop", 0, 10, 1, True, 0, 0.4, 0.5, (1, 0.85, 0.5))]),
    template("season-valentine", "Valentine", S, "classic", "heart.fill", 0.95, 100, 15, (4,), ("drift", "push"), ("circle", "dissolve"), 0.6, "pastelDream",
             texts=[text("Title", "you & me", "Snell Roundhand", 0.1, 0.5, (1, 0.85, 0.9), "typewriter", 0, 12, 1, True, 0, 0.4, 0.5, PINK)]),
    template("season-wedding", "Wedding Highlights", S, "classic", "heart.circle", 0.1, 84, 25, (4, 8), ("drift", "pull", "push"), ("dissolve", "dipToBlack"), 0.9, "portra",
             texts=[text("Names", "Anna & Sam", "Didot", 0.08, 0.5, (1, 1, 1), "pop", 0, 12, 1, False, 0, 0.5),
                    text("Date", "11.14.2026", "Didot", 0.04, 0.58, (1, 1, 1), "typewriter", 4, 12, 1, False, 0, 0.5)]),
    template("season-graduation", "Graduation", S, "classic", "graduationcap", 0.6, 122, 15, (2,), ("punch", "push"), ("whip", "flash"), 0.3, "cleanBright",
             texts=[text("Title", "CLASS OF 2026", "Futura", 0.11, 0.5, GOLD, "slam", 0, 8, 1, True, 0.3)]),
    template("season-back-to-school", "Back to School", S, "classic", "backpack", 0.15, 120, 15, (2,), ("push", "punch"), ("slideLeft", "flash"), 0.3, "naturalPop",
             texts=[text("Title", "back to school", "Chalkboard SE", 0.08, 0.5, (1, 1, 1), "typewriter", 0, 10, 1, True, 0.2)]),
    template("season-spring", "Spring Bloom", S, "classic", "leaf", 0.3, 104, 15, (4,), ("drift", "push"), ("softSwipe", "dissolve"), 0.6, "pastelDream",
             texts=[text("Title", "hello spring", "Snell Roundhand", 0.1, 0.5, (1, 1, 1), "pop", 0, 10)]),
    template("season-summer", "Summer Vibes", S, "classic", "beach.umbrella", 0.12, 126, 15, (2, 1, 1), ("push", "punch", "shake"), ("whip", "flash", "none"), 0.25, "goldenHour",
             texts=[text("Title", "SUMMER VIBES", "Futura", 0.12, 0.5, (1, 0.9, 0.3), "slam", 0, 6, 1, True, 0.3)]),
    template("season-thanksgiving", "Grateful", S, "classic", "leaf.fill", 0.08, 96, 18, (4,), ("drift", "pull"), ("dissolve",), 0.7, "vintage70s",
             texts=[text("Words", "grateful for\nthese moments", "Georgia", 0.07, 0.5, (1, 0.95, 0.85), "stack", 0, 12, 3, False, 0, 0.5)]),
]

# --- Marketing: products, sales and launches ------------------------------------------------
M = "Marketing"
WHITE = (1, 1, 1); BLACK = (0.08, 0.08, 0.08)
T += [
    template("mkt-product-spotlight", "Product Spotlight", M, "photoDump", "bag", 0.58, 110, 15, (3,), ("drop",), ("none",), 0, "cleanBright",
             card=card(0, 0.78, 0.0, 0.0, (1, 1, 1), (0.95, 0.95, 0.96)),
             texts=[text("Product", "THE NEW ESSENTIAL", "Futura", 0.06, 0.1, BLACK, "typewriter", 0, 10, 1, True, 0, 0, tracking=0.12),
                    text("Price", "$49", "Avenir Next", 0.09, 0.88, BLACK, "pop", 4, 20, 1, True, 0, 0)],
             notes="Your product on a clean card, name and price."),
    template("mkt-flash-sale", "Flash Sale", M, "kinetic", "bolt.fill", 0.0, 140, 10, (1,), ("punch", "shake"), ("flash",), 0.15, "naturalPop",
             texts=[text("Sale", "FLASH SALE 50% OFF TODAY ONLY", "Impact", 0.15, 0.45, (1, 0.9, 0.1), "slam", 0, 12, 1, False, 0.5),
                    text("Shop", "shop now • link in bio", "Avenir Next", 0.045, 0.85, WHITE, "pop", 8, 20)],
             notes="Fast, loud and on the beat."),
    template("mkt-new-arrival", "New Arrival", M, "classic", "sparkles", 0.62, 116, 15, (2, 2, 4), ("push", "punch", "pull"), ("whip", "flash", "blurZoom"), 0.3, "tealOrange",
             texts=[text("Title", "NEW IN", "Futura", 0.16, 0.45, WHITE, "slam", 0, 4, 1, True, 0.3),
                    text("Name", "the summer collection", "Didot", 0.06, 0.58, WHITE, "typewriter", 2, 12, 1, False, 0, 0.5)]),
    template("mkt-price-drop", "Price Drop", M, "kinetic", "tag", 0.98, 128, 12, (2,), ("punch", "push"), ("glitch", "flash"), 0.2, "neonNight",
             texts=[text("Was", "WAS $99", "Futura", 0.08, 0.38, (1, 1, 1), "pop", 0, 4, 1, True, 0.3),
                    text("Now", "NOW $59", "Impact", 0.16, 0.52, (1, 0.3, 0.4), "slam", 4, 12, 1, False, 0.4, 0.3, 0.6, (1, 0.2, 0.4))]),
    template("mkt-before-after-product", "Product Before & After", M, "beforeAfter", "rectangle.split.2x1", 0.45, 110, 16,
             beats=(4, 4), effects=("none", "push"), transitions=("flash", "splitReveal"), tsec=1.2, look="cleanBright", labels=["WITHOUT", "WITH"]),
    template("mkt-testimonial", "Customer Love", M, "classic", "quote.bubble", 0.9, 96, 15, (4,), ("drift", "push"), ("dissolve",), 0.6, "portra",
             texts=[text("Quote", "\u201cI use it every single day\u201d", "Georgia", 0.065, 0.45, WHITE, "typewriter", 0, 12, 1, False, 0, 0.6),
                    text("Name", "— Priya, verified buyer", "Avenir Next", 0.04, 0.58, WHITE, "pop", 6, 16, 1, True, 0, 0.5)]),
    template("mkt-menu-special", "Menu Special", M, "classic", "fork.knife", 0.07, 118, 15, (2, 2, 4), ("push", "punch", "pull"), ("slideLeft", "flash", "dissolve"), 0.3, "goldenHour",
             texts=[text("Dish", "TODAY'S SPECIAL", "Futura", 0.09, 0.2, WHITE, "slam", 0, 6, 1, True, 0.3),
                    text("Price", "only $12", "Marker Felt", 0.08, 0.82, (1, 0.85, 0.3), "pop", 4, 16, 1, True, 0.3)]),
    template("mkt-grand-opening", "Grand Opening", M, "kinetic", "party.popper", 0.12, 124, 12, (1, 1, 2), ("punch", "push"), ("flash", "spin"), 0.25, "naturalPop",
             texts=[text("Words", "GRAND OPENING THIS SATURDAY", "Futura", 0.12, 0.45, GOLD, "slam", 0, 10, 1, True, 0.3),
                    text("Where", "see you there", "Snell Roundhand", 0.07, 0.62, WHITE, "pop", 8, 16)]),
]

if __name__ == "__main__":
    out = {"schema": 1, "updated": datetime.date.today().isoformat(), "revision": int(datetime.datetime.now().timestamp()), "templates": T}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "catalog.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"{len(T)} templates, {os.path.getsize(os.path.join(here, 'catalog.json')) // 1024} KB")
