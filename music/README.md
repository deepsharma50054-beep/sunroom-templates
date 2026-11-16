# Sunroom Music

28 songs by Kevin MacLeod (incompetech.com), licensed under Creative Commons:
By Attribution 4.0 (http://creativecommons.org/licenses/by/4.0/).

These files are no longer packed inside the app. Sunroom downloads them once, when the
user asks, from the `music/` folder of the sunroom-templates repository:

    https://cdn.jsdelivr.net/gh/deepsharma50054-beep/sunroom-templates@main/music/<name>.m4a
    (fallback) https://raw.githubusercontent.com/deepsharma50054-beep/sunroom-templates/main/music/<name>.m4a

Upload all 28 `.m4a` files from this folder, unchanged, into `music/` in that repository.
The app checks each file's size and SHA-256 (listed in `Sources/iUtility/Video/MusicPack.swift`)
and rejects anything else, so if a song is ever replaced, update the list there too.
