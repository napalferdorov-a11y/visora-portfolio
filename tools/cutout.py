#!/usr/bin/env python3
"""
Cut a portrait out of its background -> transparent PNG for the VISORA hero.

Usage:
    pip install rembg onnxruntime pillow
    python tools/cutout.py assets/images/portrait-raw.jpg assets/images/portrait.png

Uses AI subject segmentation (rembg / U2Net), so light clothing on a white
background (e.g. white trousers) is preserved instead of being erased.
"""
import sys
from PIL import Image
from rembg import remove

src = sys.argv[1] if len(sys.argv) > 1 else "assets/images/portrait-raw.jpg"
dst = sys.argv[2] if len(sys.argv) > 2 else "assets/images/portrait.png"

img = Image.open(src).convert("RGB")
cut = remove(img)                      # RGBA with subject isolated
cut.save(dst)
print(f"Saved cut-out -> {dst}  ({cut.size[0]}x{cut.size[1]})")
