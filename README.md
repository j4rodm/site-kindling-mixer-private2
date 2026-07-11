# Kindling Frequency Mixer

A static gallery + audio mixer for [Kindling by Stacey](https://www.kindlingbystacey.com/). Visitors browse art pieces, select several, and mix their audio loops together to discover evolving sonic combinations.
Fun 1
## Quick Start

1. **Add a piece:** Create a directory under `pieces/` with a `manifest.yaml` and media files.
2. **Build:** Run `python scripts/build.py` (or let GitHub Actions do it on push).
3. **Deploy:** Push to `main` — GitHub Pages serves the `docs/` folder.

## Directory Structure

```
pieces/
  aurora-drift/
    manifest.yaml
    image-1.jpg
    audio.mp3
  tidal-hum/
    ...
sets/
  sets.yaml          # Curated combinations
scripts/
  build.py           # Generates index.json + copies assets to docs/
  encrypt_field.py   # Encrypts private field values
docs/                # Built output served by GitHub Pages
```

## Manifest Format

```yaml
title: "Aurora Drift"
date: 2025-06-15
tags: ["ambient", "warm"]
images:
  - image-1.jpg
  - image-2.jpg
audio: audio.mp3
description: "Inspired by northern lights."

private:
  notes: "ENCRYPTED_STRING_HERE"
  price: "ENCRYPTED_STRING_HERE"
```

## Private Fields

Encrypt values before committing:

```bash
python scripts/encrypt_field.py "This is a secret note"
# Enter passphrase when prompted
# Paste the output into your manifest.yaml
```

Visitors click the lock icon and enter the passphrase to decrypt private fields in-browser.

## Curated Sets

Edit `sets/sets.yaml`:

```yaml
- name: "Ocean Series"
  description: "Best experienced together"
  pieces: ["tidal-hum", "crystal-resonance", "aurora-drift"]
```

## Audio Recommendations

- **Format:** MP3 at 128-192kbps (universal support)
- **Lengths:** Can vary — tracks loop independently, creating evolving phase relationships
- **Content:** Each piece gets one audio file
