"""
Remove backgrounds from product photos and save as 400x400 transparent PNGs
for the market-app tile previews.
Run once: python3 process_images.py
"""

import io, os, sys
from pathlib import Path

try:
    from rembg import remove
    from PIL import Image
except ImportError:
    sys.exit("Missing deps — run: pip3 install rembg onnxruntime Pillow")

ICLOUD  = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/ITA Prints/Photos"
KARIM   = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/ITA Prints/Karim/Photos"
OUTPUT  = Path(__file__).parent / "images"
OUTPUT.mkdir(exist_ok=True)

PHOTOS = {
    'leather-keychain':       ICLOUD / "Small leather keychains/IMG_1138.JPG",
    'custom-leather-keychain':KARIM  / "Leather Keychain/IMG_3191.jpg",
    'heart-keychain':         ICLOUD / "Heart Mirrors/IMG_4705.jpg",
    'mini-heart-keychain':    ICLOUD / "Heart Mirrors/IMG_4733.JPG",
    'circle-keychain':        ICLOUD / "Circle Mirrors/IMG_5119.JPG",
    'cat-paw-organizer':      ICLOUD / "Cable Holders/Closer up.jpg",
    'heart-lip-balm':         ICLOUD / "Lip palm holder/IMG_4903.JPG",
    'lip-balm-bag-charm':     ICLOUD / "Lip palm holder/IMG_4915.JPG",
    'slim-wallet':            ICLOUD / "Wallets/IMG_4792.JPG",
    'luggage-tag':            ICLOUD / "Luggage tags/IMG_4571.jpg",
    'slate-coaster':          ICLOUD / "Coasters/Slate Coasters.jpg",
    'square-slate-coaster':   ICLOUD / "Coasters/Aquare Coaster.jpg",
    'cork-coaster':           ICLOUD / "Coasters/Cork Coaster.jpg",
    # wood-bottle-opener: no photo — SVG fallback used in index.html
}

TARGET  = 400   # output px per side
PADDING = 0.08  # fraction of longest edge added as transparent padding


def process(product_id: str, src: Path) -> None:
    if not src.exists():
        print(f"  SKIP  {product_id}: not found")
        return

    print(f"  {product_id}...", end=" ", flush=True)
    out_bytes = remove(src.read_bytes())      # rembg → RGBA PNG bytes

    img = Image.open(io.BytesIO(out_bytes)).convert("RGBA")

    # Trim transparent border
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Centre on a square canvas with padding
    w, h    = img.size
    long    = max(w, h)
    pad     = int(long * PADDING)
    size    = long + 2 * pad
    canvas  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(img, (pad + (long - w) // 2, pad + (long - h) // 2))

    final = canvas.resize((TARGET, TARGET), Image.LANCZOS)
    dest  = OUTPUT / f"{product_id}.png"
    final.save(dest, "PNG", optimize=True)
    print(f"done  ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    print(f"Output → {OUTPUT}\n")
    for pid, path in PHOTOS.items():
        process(pid, path)
    print("\nAll done.")
