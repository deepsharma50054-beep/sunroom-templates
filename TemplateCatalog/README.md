# Sunroom Reel templates

`catalog.json` is the list of online Reel templates Sunroom shows in the template feed and on the
Reels page. Each template is a small recipe (rhythm, camera moves, transitions, look and words)
that Sunroom draws with its own engine, so a template is a few KB and nothing heavy is downloaded.

## Where it lives

Repository: https://github.com/deepsharma50054-beep/sunroom-templates (public).
Sunroom reads
`https://cdn.jsdelivr.net/gh/deepsharma50054-beep/sunroom-templates@main/catalog.json`
(set in `Sources/iUtility/Video/OnlineTemplates.swift`, `defaultURL`).

## Add or change templates

1. Edit the lists in `make_catalog.py`.
2. Run `python3 make_catalog.py`; it writes `catalog.json` with a new revision number (Sunroom always shows the newest revision it has).
3. Upload the new `catalog.json` to the repository (replace the old one).

Sunroom checks for changes at most every 6 hours (or from the feed's ••• menu, Check for new
templates). jsDelivr can take up to 12 hours to pick up a change on `@main`; to make it
immediate, open `https://purge.jsdelivr.net/gh/deepsharma50054-beep/sunroom-templates@main/catalog.json`.

## What a template can say

- `family`: `classic` (beat cuts), `kinetic` (words land on the beat), `photoDump` (printed
  photos dropped on a table) or `beforeAfter` (pairs, the second wipes over the first).
- `slots`: shot lengths in beats, a move (`none push pull punch shake drift drop`) and the
  transition into it (`none dissolve dipToBlack wipeLeft wipeUp slideLeft zoom flash blurZoom
  spin glitch whip circle pixelate softSwipe splitReveal`).
- `texts`: words with a font, size, colour and place, and a `motion` (`none pop slam typewriter
  stack`) with `stepBeats` (beats per word or line).
- `look`: one of Sunroom's film looks. `card` and `labels` style Photo Dump and Before & After.

Sunroom checks everything it reads: unknown or broken templates are skipped and numbers are kept
within safe limits. A template's `key` must be unique; Sunroom adds `online.` in front of it.

## Template packs (downloaded once, on request)
`packs.json` lists the packs; `packs/<id>/` holds each pack's `templates.json` (same format as
`catalog.json`) and `anim/*.json` (Lottie animations, Sunroom's own, drawn by `lottie_kit.py`).
1. Edit `make_packs.py` (and `lottie_kit.py` for new animation shapes).
2. Run `python3 make_packs.py`. It rewrites `packs.json` (with each file's size and SHA-256) and `packs/`.
3. Upload `packs.json` and the whole `packs/` folder to the repository root, next to `catalog.json`.
Sunroom checks every file against `packs.json` and refuses the pack if any file differs, so always
upload `packs.json` together with the files it lists.

The animations inside the app come from `make_lottie.py`, which writes
`Sources/iUtility/Video/LottieBuiltIn.swift`.
