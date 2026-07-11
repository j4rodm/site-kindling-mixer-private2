#!/usr/bin/env python3
"""
Build script for Kindling Frequency Mixer.
Scans pieces/ directories, reads manifests, generates index.json,
and copies everything into docs/ for GitHub Pages.
"""

import json
import os
import shutil
import yaml
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_DIR = os.path.join(ROOT, "pieces")
SETS_FILE = os.path.join(ROOT, "sets", "sets.yaml")
DOCS_DIR = os.path.join(ROOT, "docs")
STATIC_DIR = os.path.join(ROOT, "static")


def load_manifest(piece_dir):
    manifest_path = os.path.join(piece_dir, "manifest.yaml")
    if not os.path.exists(manifest_path):
        return None
    with open(manifest_path, "r") as f:
        return yaml.safe_load(f)


def build():
    # Clean docs/pieces only, preserve docs/index.html etc.
    docs_pieces = os.path.join(DOCS_DIR, "pieces")
    if os.path.exists(docs_pieces):
        shutil.rmtree(docs_pieces)

    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(docs_pieces, exist_ok=True)

    pieces = []

    # Scan piece directories
    if not os.path.exists(PIECES_DIR):
        print("No pieces/ directory found.")
        sys.exit(1)

    for slug in sorted(os.listdir(PIECES_DIR)):
        piece_path = os.path.join(PIECES_DIR, slug)
        if not os.path.isdir(piece_path):
            continue

        manifest = load_manifest(piece_path)
        if manifest is None:
            print(f"  Skipping {slug}: no manifest.yaml")
            continue

        print(f"  Processing: {slug}")

        # Build piece entry
        entry = {
            "slug": slug,
            "title": manifest.get("title", slug),
            "date": str(manifest.get("date", "")),
            "tags": manifest.get("tags", []),
            "description": manifest.get("description", ""),
            "images": [f"pieces/{slug}/{img}" for img in manifest.get("images", [])],
            "audio": f"pieces/{slug}/{manifest['audio']}" if manifest.get("audio") else None,
        }

        # Include private fields (encrypted values pass through as-is)
        if "private" in manifest:
            entry["private"] = manifest["private"]

        pieces.append(entry)

        # Copy media files to docs/pieces/slug/
        dest_dir = os.path.join(docs_pieces, slug)
        os.makedirs(dest_dir, exist_ok=True)

        for fname in os.listdir(piece_path):
            if fname == "manifest.yaml":
                continue
            src = os.path.join(piece_path, fname)
            dst = os.path.join(dest_dir, fname)
            if os.path.isfile(src):
                shutil.copy2(src, dst)

    # Load curated sets
    sets = []
    if os.path.exists(SETS_FILE):
        with open(SETS_FILE, "r") as f:
            sets = yaml.safe_load(f) or []

    # Write index.json
    index = {
        "pieces": pieces,
        "sets": sets,
    }
    index_path = os.path.join(DOCS_DIR, "index.json")
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
    print(f"\n  Written {len(pieces)} pieces and {len(sets)} sets to index.json")

    # Copy static files (index.html, css, js) into docs/
    if os.path.exists(STATIC_DIR):
        for fname in os.listdir(STATIC_DIR):
            src = os.path.join(STATIC_DIR, fname)
            dst = os.path.join(DOCS_DIR, fname)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        print("  Copied static files to docs/")

    print("\nBuild complete!")


if __name__ == "__main__":
    build()
