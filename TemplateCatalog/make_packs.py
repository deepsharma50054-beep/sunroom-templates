#!/usr/bin/env python3
"""Writes the downloadable template packs: packs.json and packs/<id>/ (templates.json + anim/*.json).

Each pack is a set of Reel templates (Sunroom recipes, see make_catalog.py) and animated stickers
(Lottie, see lottie_kit.py), all Sunroom's own. Run `python3 make_packs.py`, then upload packs.json
and the packs/ folder to the sunroom-templates repository. Every file is listed in packs.json with
its size and SHA-256; the app checks them after downloading.
"""
import json, os, hashlib, datetime, shutil
from make_catalog import template, text, card
from lottie_kit import *

WHITE = (1, 1, 1); BLACK = (0.08, 0.08, 0.08); GOLD = (1, 0.8, 0.35); PINK = (1, 0.35, 0.7)
SKY = (0.55, 0.85, 1); CORAL = (1, 0.45, 0.4); MINT = (0.4, 0.95, 0.7); LIME = (0.75, 1, 0.2)
BA = dict(beats=(4, 4), effects=("none", "push"), transitions=("flash", "splitReveal"), tsec=1.2)

PACKS = []
def pack(id_, title, detail, symbol, hue, templates, animations):
    PACKS.append(dict(id=id_, title=title, detail=detail, symbol=symbol, hue=hue, templates=templates, animations=animations))

pack("travel", "Travel", "Trips, cities and road days: maps-and-postcards feel, quick cuts on the move.", "airplane", 0.55, [
    template("travel-postcard", "Postcard From", "Travel", "photoDump", "envelope", 0.55, 112, 18, (3,), ("drop",), ("none",), 0, "kodachrome",
             card=card(4, 0.8, 0.05, 0.2, (1, 0.98, 0.94), (0.75, 0.86, 0.95)),
             texts=[text("Place", "greetings from lisbon", "American Typewriter", 0.05, 0.9, (0.15, 0.25, 0.4), "typewriter", 0, 12, 1, False, 0, 0)]),
    template("travel-passport", "Passport Stamps", "Travel", "classic", "globe.europe.africa", 0.58, 124, 15, (2, 1, 1), ("punch", "push", "shake"), ("whip", "flash", "none"), 0.25, "tealOrange",
             texts=[text("Title", "PASSPORT FULL", "Futura", 0.12, 0.45, WHITE, "slam", 0, 6, 1, True, 0.35),
                    text("Count", "6 countries · 21 days", "Avenir Next", 0.045, 0.58, WHITE, "pop", 4, 16)]),
    template("travel-road-trip", "Road Trip", "Travel", "classic", "car", 0.1, 118, 20, (2, 2, 4), ("push", "drift", "pull"), ("slideLeft", "whip", "dissolve"), 0.3, "goldenHour",
             texts=[text("Title", "road trip diaries", "Marker Felt", 0.08, 0.2, (1, 0.95, 0.85), "typewriter", 0, 10, 1, True, 0.3)]),
    template("travel-city-lights", "City Lights", "Travel", "classic", "building.2", 0.72, 128, 15, (1, 1, 2), ("punch", "shake"), ("glitch", "flash", "zoom"), 0.2, "neonNight",
             texts=[text("City", "TOKYO NIGHTS", "Futura", 0.12, 0.5, (1, 0.4, 0.8), "slam", 0, 6, 1, True, 0.3, 0.3, 0.7, (0.3, 0.8, 1))]),
    template("travel-beach-day", "Beach Day", "Travel", "classic", "beach.umbrella", 0.5, 104, 18, (4,), ("drift", "push"), ("softSwipe", "dissolve"), 0.6, "pastelDream",
             texts=[text("Title", "salt water therapy", "Snell Roundhand", 0.09, 0.5, WHITE, "pop", 0, 10, 1, True, 0, 0.4)]),
    template("travel-mountains", "Mountain Air", "Travel", "classic", "mountain.2", 0.4, 90, 20, (4, 8), ("drift", "pull"), ("dissolve", "blurZoom"), 0.8, "arctic",
             texts=[text("Title", "above the clouds", "Didot", 0.08, 0.45, WHITE, "typewriter", 0, 14, 1, False, 0, 0.6),
                    text("Height", "3,200 m", "Avenir Next", 0.045, 0.56, WHITE, "pop", 6, 16)]),
    template("travel-itinerary", "Itinerary", "Travel", "kinetic", "list.bullet", 0.6, 116, 18, (4,), ("push", "pull"), ("whip",), 0.3, "cleanBright",
             texts=[text("Plan", "day 1  arrive\nday 2  explore\nday 3  eat everything", "Avenir Next", 0.06, 0.5, WHITE, "stack", 0, 16, 3, True, 0.25)]),
    template("travel-then-there", "Here vs There", "Travel", "beforeAfter", "arrow.left.arrow.right", 0.55, 110, 16, look="kodachrome", **BA, labels=["MONDAY", "FRIDAY"]),
], [
    ("plane", "Plane Trail", "airplane", plane("Plane Trail")),
    ("pin", "Map Pin", "mappin.and.ellipse", pin_drop("Map Pin")),
    ("wanderlust", "Wanderlust", "textformat", pop_title("Wanderlust", "WANDERLUST", (1, 1, 1), (0.1, 0.3, 0.5), "Futura-Bold", 96)),
])

pack("love", "Wedding & Love", "Weddings, anniversaries and couples: slow dissolves, soft light, elegant words.", "heart.circle", 0.95, [
    template("love-vows", "The Vows", "Wedding & Love", "classic", "heart.text.square", 0.08, 80, 25, (4, 8), ("drift", "pull"), ("dissolve", "dipToBlack"), 0.9, "portra",
             texts=[text("Names", "Maya & Leo", "Didot", 0.09, 0.48, WHITE, "pop", 0, 14, 1, False, 0, 0.5),
                    text("Date", "forever starts today", "Snell Roundhand", 0.06, 0.58, WHITE, "typewriter", 4, 16, 1, True, 0, 0.5)]),
    template("love-save-date", "Save the Date", "Wedding & Love", "photoDump", "calendar.badge.clock", 0.95, 100, 15, (3,), ("drop",), ("none",), 0, "pastelDream",
             card=card(3, 0.78, 0.045, 0.22, (1, 0.99, 0.97), (0.96, 0.88, 0.88)),
             texts=[text("Title", "save the date", "Snell Roundhand", 0.08, 0.1, (0.6, 0.3, 0.35), "pop", 0, 10),
                    text("Date", "06 · 14 · 2027", "Didot", 0.05, 0.9, (0.45, 0.3, 0.3), "typewriter", 2, 14, 1, False, 0, 0)]),
    template("love-anniversary", "Anniversary", "Wedding & Love", "classic", "sparkles", 0.1, 92, 18, (4,), ("drift", "push"), ("blurZoom", "dissolve"), 0.7, "goldenHour",
             texts=[text("Years", "5 years of us", "Didot", 0.09, 0.5, (1, 0.92, 0.8), "pop", 0, 12, 1, False, 0, 0.5, 0.5, GOLD)]),
    template("love-how-we-met", "How We Met", "Wedding & Love", "kinetic", "quote.bubble", 0.92, 96, 18, (4,), ("drift",), ("dissolve",), 0.6, "matte",
             texts=[text("Story", "it started with\na wrong number", "Georgia", 0.07, 0.5, WHITE, "stack", 0, 16, 4, False, 0, 0.6)]),
    template("love-first-dance", "First Dance", "Wedding & Love", "classic", "figure.socialdance", 0.85, 84, 20, (8,), ("drift", "pull"), ("dissolve",), 1.0, "noir",
             texts=[text("Title", "our first dance", "Snell Roundhand", 0.09, 0.85, WHITE, "pop", 0, 14)]),
    template("love-proposal", "She Said Yes", "Wedding & Love", "kinetic", "heart.circle.fill", 0.12, 120, 12, (2, 1, 1), ("push", "punch"), ("flash", "zoom"), 0.25, "naturalPop",
             texts=[text("Words", "SHE SAID YES!", "Futura", 0.14, 0.5, WHITE, "slam", 0, 8, 1, True, 0.35, 0.4, 0.6, PINK)]),
    template("love-polaroids", "Love Polaroids", "Wedding & Love", "photoDump", "heart", 0.97, 112, 15, (2,), ("drop",), ("none",), 0, "fadedFilm",
             card=card(6, 0.72, backdrop=(0.98, 0.9, 0.92)),
             texts=[text("Title", "us", "Snell Roundhand", 0.1, 0.9, (0.75, 0.2, 0.35), "pop", 0, 8)]),
    template("love-then-now", "Then & Now (Us)", "Wedding & Love", "beforeAfter", "clock.arrow.circlepath", 0.95, 92, 16, look="portra", **BA, labels=["2019", "2026"]),
], [
    ("rings", "Rings", "circle.circle", rings("Rings")),
    ("hearts", "Floating Hearts", "heart.fill", heart_pop("Floating Hearts", (1, 0.5, 0.6))),
    ("just-married", "Just Married", "textformat", pop_title("Just Married", "Just Married", (1, 1, 1), (0.6, 0.3, 0.4), "SnellRoundhand-Bold", 110)),
])

pack("party", "Birthday & Party", "Birthdays, parties and celebrations: confetti, big words, fast fun cuts.", "birthday.cake", 0.88, [
    template("party-its-my-birthday", "It's My Birthday", "Birthday & Party", "kinetic", "gift", 0.9, 128, 12, (1, 1, 2), ("punch", "shake"), ("flash", "spin"), 0.2, "naturalPop",
             texts=[text("Words", "IT'S MY BIRTHDAY", "Futura", 0.14, 0.5, (1, 0.9, 0.2), "slam", 0, 8, 1, True, 0.35, 0.4, 0, None, PINK)]),
    template("party-turning", "Turning 30", "Birthday & Party", "classic", "number", 0.12, 124, 15, (2,), ("punch", "push"), ("zoom", "flash"), 0.25, "goldenHour",
             texts=[text("Age", "30", "Impact", 0.32, 0.45, GOLD, "slam", 0, 6, 1, False, 0.4, 0.4, 0.8, (1, 0.6, 0.2)),
                    text("Words", "and thriving", "Snell Roundhand", 0.07, 0.62, WHITE, "pop", 4, 16)]),
    template("party-night", "Party Night", "Birthday & Party", "classic", "music.note", 0.78, 132, 12, (1,), ("shake", "punch"), ("glitch", "flash"), 0.15, "neonNight",
             texts=[text("Title", "PARTY MODE", "Futura", 0.13, 0.5, (0.4, 1, 0.9), "slam", 0, 6, 1, True, 0.3, 0.3, 0.8, (0.2, 0.9, 1))]),
    template("party-dump", "Party Dump", "Birthday & Party", "photoDump", "photo.stack", 0.9, 128, 15, (2,), ("drop",), ("none",), 0, "fadedFilm",
             card=card(7, 0.72, backdrop=(1, 0.86, 0.5)),
             texts=[text("Title", "last night", "Marker Felt", 0.08, 0.9, (0.8, 0.2, 0.4), "pop", 0, 8)]),
    template("party-wish", "Make a Wish", "Birthday & Party", "classic", "sparkles", 0.1, 96, 15, (4,), ("drift", "push"), ("blurZoom", "dissolve"), 0.6, "goldenHour",
             texts=[text("Words", "make a wish", "Snell Roundhand", 0.1, 0.5, (1, 0.92, 0.75), "typewriter", 0, 12, 1, True, 0, 0.4, 0.7, GOLD)]),
    template("party-kids", "Little One Turns 1", "Birthday & Party", "classic", "teddybear", 0.12, 112, 15, (2, 4), ("push", "drift"), ("circle", "dissolve"), 0.4, "pastelDream",
             texts=[text("Title", "one year of you", "Marker Felt", 0.08, 0.5, WHITE, "pop", 0, 10, 1, True, 0.3)]),
    template("party-countdown", "Party Countdown", "Birthday & Party", "kinetic", "timer", 0.0, 128, 12, (1, 1, 1, 4), ("punch", "punch", "punch", "push"), ("flash",), 0.15, "naturalPop",
             texts=[text("Count", "3 2 1 PARTY!", "Impact", 0.28, 0.5, WHITE, "slam", 0, 6, 1, False, 0.4, 0.4, 0.8, PINK)]),
    template("party-squad", "The Squad", "Birthday & Party", "classic", "person.3", 0.85, 124, 15, (2,), ("push", "punch"), ("whip", "slideLeft"), 0.3, "naturalPop",
             texts=[text("Title", "the whole squad", "Futura", 0.09, 0.2, WHITE, "slam", 0, 6, 1, True, 0.3)]),
], [
    ("balloons", "Balloons", "balloon.2.fill", balloons("Balloons")),
    ("party-confetti", "Party Confetti", "party.popper", confetti("Party Confetti", frames=90, count=24)),
    ("happy-birthday", "Happy Birthday", "textformat", pop_title("Happy Birthday", "Happy Birthday!", (1, 0.85, 0.2), (0.7, 0.2, 0.4), "MarkerFelt-Wide", 96)),
])

pack("business", "Business & Sales", "Shops, launches and offers: bold prices, clean product shots, clear calls to action.", "briefcase", 0.6, [
    template("biz-launch", "Launch Day", "Business & Sales", "kinetic", "paperplane", 0.6, 128, 12, (1, 1, 2), ("punch", "push"), ("flash", "zoom"), 0.2, "cleanBright",
             texts=[text("Words", "IT'S FINALLY HERE", "Futura", 0.13, 0.45, BLACK, "slam", 0, 8, 1, True, 0, 0.2),
                    text("Shop", "available now", "Avenir Next", 0.05, 0.6, BLACK, "pop", 6, 16, 1, True, 0, 0)]),
    template("biz-bogo", "Buy One Get One", "Business & Sales", "kinetic", "tag", 0.98, 136, 10, (1,), ("punch", "shake"), ("flash",), 0.15, "naturalPop",
             texts=[text("Deal", "BUY 1 GET 1 FREE", "Impact", 0.15, 0.45, (1, 0.9, 0.1), "slam", 0, 10, 1, False, 0.5),
                    text("When", "this weekend only", "Avenir Next", 0.045, 0.85, WHITE, "pop", 6, 20)]),
    template("biz-behind", "Behind the Scenes", "Business & Sales", "classic", "camera", 0.08, 108, 18, (2, 4), ("drift", "push"), ("slideLeft", "dissolve"), 0.4, "fadedFilm",
             texts=[text("Title", "how we make it", "American Typewriter", 0.07, 0.15, WHITE, "typewriter", 0, 12, 1, False, 0, 0.6)]),
    template("biz-three-reasons", "3 Reasons", "Business & Sales", "kinetic", "list.number", 0.55, 116, 18, (4,), ("push", "pull"), ("whip",), 0.3, "cleanBright",
             texts=[text("List", "1. made by hand\n2. ships in 24h\n3. loved by 10k+", "Avenir Next", 0.06, 0.5, WHITE, "stack", 0, 16, 3, True, 0.3)]),
    template("biz-review", "5-Star Review", "Business & Sales", "classic", "star.fill", 0.12, 96, 15, (4,), ("drift", "push"), ("dissolve",), 0.6, "goldenHour",
             texts=[text("Quote", "\u201cbest purchase this year\u201d", "Georgia", 0.065, 0.45, WHITE, "typewriter", 0, 12, 1, False, 0, 0.6),
                    text("Who", "— a happy customer", "Avenir Next", 0.04, 0.58, WHITE, "pop", 6, 16, 1, True, 0, 0.5)]),
    template("biz-unboxing", "Unboxing", "Business & Sales", "classic", "shippingbox", 0.1, 120, 15, (2, 2, 4), ("push", "punch", "pull"), ("zoom", "flash", "dissolve"), 0.3, "naturalPop",
             texts=[text("Title", "unboxing time", "Futura", 0.09, 0.2, WHITE, "slam", 0, 6, 1, True, 0.3)]),
    template("biz-catalog", "Product Lineup", "Business & Sales", "photoDump", "square.grid.2x2", 0.58, 120, 15, (2,), ("drop",), ("none",), 0, "cleanBright",
             card=card(0, 0.8, 0.0, 0.0, WHITE, (0.94, 0.95, 0.97)),
             texts=[text("Title", "THE COLLECTION", "Futura", 0.055, 0.08, BLACK, "typewriter", 0, 10, 1, True, 0, 0, tracking=0.15)]),
    template("biz-results", "Real Results", "Business & Sales", "beforeAfter", "chart.line.uptrend.xyaxis", 0.4, 110, 16, look="cleanBright", **BA, labels=["BEFORE", "AFTER"]),
], [
    ("sale-badge", "Sale Badge", "tag.fill", badge("Sale Badge", "SALE -50%", (1, 0.2, 0.25))),
    ("new-badge", "New Badge", "sparkle", badge("New Badge", "NEW", (0.15, 0.5, 1))),
    ("shop-now", "Shop Now", "cart.fill", badge("Shop Now", "SHOP NOW", (0.08, 0.08, 0.1), (1, 0.85, 0.2), "Futura-Bold")),
])

pack("fitness", "Fitness", "Workouts, progress and routines: punchy cuts, counters and high-energy words.", "figure.run", 0.3, [
    template("fit-workout", "Workout of the Day", "Fitness", "kinetic", "dumbbell", 0.3, 136, 15, (1, 1, 2), ("punch", "shake"), ("flash", "whip"), 0.15, "moody",
             texts=[text("Title", "WORKOUT OF THE DAY", "Impact", 0.12, 0.15, LIME, "slam", 0, 8, 1, False, 0.4)]),
    template("fit-day-one", "Day 1 vs Day 100", "Fitness", "beforeAfter", "figure.strengthtraining.traditional", 0.3, 128, 16, look="moody", **BA, labels=["DAY 1", "DAY 100"]),
    template("fit-reps", "Count the Reps", "Fitness", "kinetic", "number", 0.32, 140, 12, (1,), ("punch",), ("flash",), 0.1, "noir",
             texts=[text("Count", "1 2 3 4 5 6 7 8 9 10", "Impact", 0.25, 0.5, WHITE, "slam", 0, 10, 1, False, 0.4)]),
    template("fit-morning-run", "Morning Run", "Fitness", "classic", "sunrise", 0.1, 124, 18, (2, 2, 4), ("push", "drift", "pull"), ("whip", "slideLeft", "dissolve"), 0.3, "goldenHour",
             texts=[text("Title", "5 km before 6 am", "Futura", 0.08, 0.2, WHITE, "typewriter", 0, 10, 1, True, 0.3)]),
    template("fit-no-excuses", "No Excuses", "Fitness", "kinetic", "flame", 0.02, 140, 10, (1,), ("shake", "punch"), ("glitch", "flash"), 0.15, "cyberpunk",
             texts=[text("Words", "NO EXCUSES. JUST RESULTS.", "Futura", 0.12, 0.5, (1, 0.35, 0.2), "slam", 0, 10, 1, True, 0.4)]),
    template("fit-yoga", "Yoga Flow", "Fitness", "classic", "figure.yoga", 0.45, 84, 20, (8,), ("drift",), ("dissolve",), 1.0, "pastelDream",
             texts=[text("Title", "breathe in, breathe out", "Snell Roundhand", 0.08, 0.5, WHITE, "typewriter", 0, 16, 1, True, 0, 0.4)]),
    template("fit-meal-prep", "Meal Prep Sunday", "Fitness", "photoDump", "takeoutbag.and.cup.and.straw", 0.3, 118, 15, (2,), ("drop",), ("none",), 0, "cleanBright",
             card=card(3, 0.78, backdrop=(0.85, 0.95, 0.85)),
             texts=[text("Title", "meal prep sunday", "Marker Felt", 0.07, 0.9, (0.2, 0.45, 0.25), "pop", 0, 8)]),
    template("fit-progress", "Progress Check", "Fitness", "classic", "chart.bar", 0.33, 120, 15, (2,), ("push", "punch"), ("zoom", "flash"), 0.25, "tealOrange",
             texts=[text("Title", "MONTH 3 CHECK-IN", "Futura", 0.1, 0.2, WHITE, "slam", 0, 6, 1, True, 0.3)]),
], [
    ("bolt", "Lightning", "bolt.fill", bolt("Lightning")),
    ("day-counter", "Day Counter", "calendar", counter_badge("Day Counter", "DAY 1")),
    ("lets-go", "Let's Go", "textformat", pop_title("Let's Go", "LET'S GO!", LIME, (0, 0, 0), "Futura-Bold", 120)),
])

pack("food", "Food & Café", "Recipes, cafés and restaurants: warm looks, steam and star ratings.", "fork.knife", 0.08, [
    template("food-recipe", "Quick Recipe", "Food & Café", "kinetic", "list.bullet.clipboard", 0.08, 116, 18, (2,), ("push", "pull"), ("whip", "slideLeft"), 0.3, "goldenHour",
             texts=[text("Title", "15-minute pasta", "Futura", 0.08, 0.15, WHITE, "slam", 0, 6, 1, True, 0.3),
                    text("Steps", "boil\ntoss\nenjoy", "Avenir Next", 0.06, 0.8, WHITE, "stack", 4, 16, 3, True, 0.3)]),
    template("food-cafe", "Café Vibes", "Food & Café", "classic", "cup.and.saucer", 0.07, 92, 18, (4,), ("drift", "push"), ("dissolve", "softSwipe"), 0.6, "vintage70s",
             texts=[text("Title", "slow mornings", "Snell Roundhand", 0.09, 0.5, (1, 0.95, 0.88), "pop", 0, 12)]),
    template("food-review", "Rate This Dish", "Food & Café", "classic", "star.leadinghalf.filled", 0.1, 120, 15, (2, 2, 4), ("push", "punch", "pull"), ("zoom", "flash", "dissolve"), 0.3, "naturalPop",
             texts=[text("Dish", "worth the hype?", "Futura", 0.09, 0.2, WHITE, "slam", 0, 6, 1, True, 0.3),
                    text("Score", "9/10", "Impact", 0.14, 0.82, GOLD, "slam", 8, 16, 1, False, 0.4)]),
    template("food-what-i-eat", "What I Eat in a Day", "Food & Café", "photoDump", "fork.knife", 0.08, 120, 18, (3,), ("drop",), ("none",), 0, "fadedFilm",
             card=card(4, 0.78, backdrop=(0.95, 0.9, 0.82)),
             texts=[text("Title", "what i eat in a day", "Marker Felt", 0.06, 0.9, (0.45, 0.25, 0.15), "typewriter", 0, 10)]),
    template("food-street", "Street Food Tour", "Food & Café", "classic", "takeoutbag.and.cup.and.straw", 0.05, 128, 15, (1, 1, 2), ("punch", "shake", "push"), ("whip", "flash"), 0.2, "tealOrange",
             texts=[text("Title", "STREET FOOD TOUR", "Futura", 0.11, 0.2, (1, 0.85, 0.3), "slam", 0, 6, 1, True, 0.35)]),
    template("food-bake", "Bake With Me", "Food & Café", "classic", "birthday.cake", 0.95, 100, 18, (4,), ("drift", "push"), ("dissolve",), 0.5, "pastelDream",
             texts=[text("Title", "bake with me", "Snell Roundhand", 0.09, 0.15, WHITE, "pop", 0, 10)]),
    template("food-menu", "Today's Menu", "Food & Café", "kinetic", "menucard", 0.07, 110, 15, (4,), ("push",), ("slideLeft",), 0.3, "goldenHour",
             texts=[text("Menu", "soup  $6\nsalad  $8\npasta  $12", "American Typewriter", 0.06, 0.5, WHITE, "stack", 0, 14, 3, False, 0.25)]),
    template("food-raw-cooked", "Raw to Ready", "Food & Café", "beforeAfter", "flame", 0.08, 110, 16, look="goldenHour", **BA, labels=["RAW", "READY"]),
], [
    ("steam", "Steam", "cloud", steam("Steam")),
    ("rating", "Star Rating", "star.fill", stars_rating("Star Rating")),
    ("yummy", "Yummy", "textformat", pop_title("Yummy", "YUMMY!", (1, 0.75, 0.2), (0.5, 0.2, 0.1), "MarkerFelt-Wide", 120)),
])

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, "packs")
shutil.rmtree(root, ignore_errors=True)
index = []
def write(rel, data):
    p = os.path.join(here, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(data)
    return {"path": rel, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
for p in PACKS:
    files = []
    envelope = {"schema": 1, "templates": p["templates"]}
    files.append(write(f"packs/{p['id']}/templates.json", json.dumps(envelope, indent=1, ensure_ascii=False).encode()))
    anims = []
    for aid, title, symbol, a in p["animations"]:
        f = write(f"packs/{p['id']}/anim/{aid}.json", dumps(a).encode())
        f.update({"title": title, "symbol": symbol})
        files.append(f)
    index.append({"id": p["id"], "title": p["title"], "detail": p["detail"], "symbol": p["symbol"], "hue": p["hue"],
                  "templates": len(p["templates"]), "animations": len(p["animations"]), "files": files})
out = {"schema": 1, "updated": datetime.date.today().isoformat(), "revision": int(datetime.datetime.now().timestamp()), "packs": index}
open(os.path.join(here, "packs.json"), "w").write(json.dumps(out, indent=1, ensure_ascii=False))
total = sum(f["size"] for p in index for f in p["files"])
print(f"{len(index)} packs, {sum(p['templates'] for p in index)} templates, {sum(p['animations'] for p in index)} animations, {total // 1024} KB")
