<div align="center">

# NaiWa Wallpaper · Asset Warehouse

**406 assets, 15 categories, one machine-readable manifest. The single source of supply for the museum and the browser extension.**

[![Stars](https://img.shields.io/github/stars/Nailong-Studio/NaiWa-Wallpaper?style=for-the-badge&label=Star&color=FFD700&logo=github)](https://github.com/Nailong-Studio/NaiWa-Wallpaper/stargazers)
[![Live index](https://img.shields.io/badge/live%20index-nailoong--wallpaper.pages.dev-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://nailoong-wallpaper.pages.dev/)
[![Manifest](https://img.shields.io/badge/manifest-assets.json-gold?style=for-the-badge)](assets.json)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

[English](README.md) · [简体中文](README.zh-CN.md)

</div>

---

## What this is

A warehouse with a map at the door. This repository stores the raw NaiWa assets —
paintings, stickers, 3D poses, animated frames, wallpapers, short films — with a
licence record for every single file. Curation, storytelling and presentation
happen in the museum repository, [NaiLoong-Universe](https://github.com/Nailong-Studio/NaiLoong-Universe).

The split is deliberate: **this repo registers and delivers, that repo narrates.** The
live index is now a nine-settlement island over the same 406 files — browse, read a
label, then take the file.

A separate [NaiWa Chronicle](https://nailoong-wallpaper.pages.dev/history.html) records
how the character spread from an AI accident to an internet folk university. It is an
annex to the warehouse, not a change to its cataloguing job.

The landing page stays cheap on purpose: one 56 KB display-font subset served from
`fonts/`, system fonts for body copy, no third-party font CDN; the first four
thumbnails load eager, the rest are lazy; media URLs carry the release version and
`_headers` caches media for a week with background revalidation while HTML and
`assets.json` revalidate on every visit.

## Desktop client

`desktop/` contains **NaiWa Wallpaper v0.0.3**, a Windows 10/11 and Linux desktop
client for the 205 curated wallpapers in this warehouse. It is separate from the
website and the browser extension: no account, no network calls, no telemetry.

Download the portable Windows / Linux builds from the
[desktop-v0.0.3 release](https://github.com/Nailong-Studio/NaiWa-Wallpaper/releases/tag/desktop-v0.0.3).

## Take what you need

Three ways in, pick whichever fits:

```bash
# 1. The whole manifest, then fetch only what you want
curl -s https://raw.githubusercontent.com/Nailong-Studio/NaiWa-Wallpaper/main/assets.json

# 2. Direct file access through the CDN
https://nailoong-wallpaper.pages.dev/<category>/<filename>

# 3. Browse the index as a world map
open https://nailoong-wallpaper.pages.dev/
```

Every manifest entry carries `id`, `category`, `title`, `file`, `raw`, `thumb`,
`type`, `bytes`, `width`, `height`, `narrative`, `license`, `source` and `form`. That is
enough to build a gallery, a wallpaper rotation, or a download client without
touching this repository at all.

## Categories

| Directory | Contents | Count |
| --- | --- | --- |
| `classic/` | World masterpieces re-signed by NaiWa | 62 |
| `laugh-gallery/` | Laughing variants collected from across the web | 22 |
| `emotes/` | Sticker packs, official poses, animated emotes | 70 |
| `poses/` | 3D costume poses — professions, props, expressions | 24 |
| `poses-wall/` | 1080×1920 vertical wallpapers composed from those poses | 24 |
| `mobile/` | 1080×1936 vertical scenes | 6 |
| `pet/` | Desktop-pet loops and 3D frame-by-frame animation | 79 |
| `art/` | Generated scenes and art experiments | 46 |
| `hd/` | Desktop wallpapers | 22 |
| `4k/` | 4K originals | 5 |
| `frames/` | Frames extracted from the short films | 35 |
| `videos/` | Official short films | 6 |
| `fan-videos/` | Fan-made scene animations | 2 |
| `audio/` | Laughs, voice clips, usable sound effects | 2 |
| `assets/` | Brand marks and logos | 1 |

`poses/` and `poses-wall/` carry an anthropomorphic costume variant (`form: anthro`);
every other category uses the frog-form character (`form: naiwa`).

Each asset sits beside a `.txt` record with its narrative, source, licence,
credit and takedown statement. Assets without a complete record do not ship.

## What counts as a wallpaper

Bitmaps with a short edge ≥ 720 px, grouped by aspect: landscape (≥1.5:1),
portrait (≤0.72:1) and near-square. Pure emote thumbnails, desktop-pet frame
sequences, audio and video are excluded from the wallpaper pack.

The browser extension [NaiWa-NewTab](https://github.com/Nailong-Studio/NaiWa-NewTab)
takes 206 of these (v1.7.4) — 73 landscape, 69 portrait,
35 square, 5 4K, 24 pose wallpapers. Change the art here; the extension only displays it.

## Manifest and records

| File | Purpose |
| --- | --- |
| `assets.json` | The machine-readable inventory: category, title, narrative, type, size, dimensions, raw URL, thumbnail path |
| `thumbs/` | 480 px WebP thumbnails, one per asset; audio gets a waveform instead |
| `SOURCES.md` | Sources, licences and the exclusion list, batch by batch |
| `DUPLICATES.md` | Known near-duplicate groups (38 groups / 98 images at v3.2.1), all intentional derivations |
| `scripts/build_assets.py` | Regenerates the manifest and thumbnails; validates the inventory |
| `scripts/build_site.py` | Builds the portal home, zones directory, today page, collection page and take page |
| `scripts/world_pages.py` | Templates and page shell for the four inner pages |
| `scripts/duplicates.py` | Read-only near-duplicate scan (dHash + SHA-256) |

```bash
python3 scripts/build_assets.py            # regenerate everything
python3 scripts/build_assets.py --check    # verify only, no writes
python3 scripts/build_site.py              # rebuild the portal and four inner pages
python3 scripts/build_assets.py --site ../NaiLoong-Universe/docs   # push to the museum
```

The `Assets Check` workflow runs `--check` whenever assets, the manifest or the
script change, and fails on count or category drift, missing thumbnails, orphan files, stale
dimensions, or records without `license` / `source`.

## Naming

Every file uses the `奶蛙-` prefix with a Chinese semantic name, so a filename
tells you what the picture is. The legacy name 奶龙 is normalised to 奶蛙
throughout; third-party repository names are never altered, because renaming
them would break links.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). In short: one asset per pull request,
a complete `.txt` record, a licence that permits redistribution, and a thumbnail
generated by the script rather than by hand. Site copy follows [VOICE.md](VOICE.md): short, concrete, no slogan voice.

If you are a rights holder and believe an asset should not be here, open an
issue — it will be removed after verification.

## Licence

Repository code is MIT. Each asset carries its own licence in its `.txt` record;
anything that cannot be redistributed is excluded, and the exclusion list in
`SOURCES.md` is the authoritative record of what was rejected and why.

NaiWa is a fan-made derivative character; original character rights stay with
their holders.
