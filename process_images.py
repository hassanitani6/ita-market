"""
Remove backgrounds from product photos and save as 400x400 transparent PNGs
for the market-app tile previews.
Run once: python3 process_images.py PHOTOS_DIR
"""

import io, os, sys
from pathlib import Path

try:
    from rembg import remove
    from PIL import Image
except ImportError:
    sys.exit("Missing deps — run: pip3 install rembg onnxruntime Pillow")

# Folder holding the product photo folders; pass it on the command line: python3 process_images.py PHOTOS_DIR
PHOTOS  = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path("photos")
OUTPUT  = Path(__file__).parent / "images"
OUTPUT.mkdir(exist_ok=True)

PHOTOS = {
    'leather-keychain':       PHOTOS / "Small leather keychains/IMG_1138.JPG",
    'custom-leather-keychain':PHOTOS / "Leather Keychain/IMG_3191.jpg",
    'heart-keychain':         PHOTOS / "Heart Mirrors/IMG_4705.jpg",
    'mini-heart-keychain':    PHOTOS / "Heart Mirrors/IMG_4733.JPG",
    'circle-keychain':        PHOTOS / "Circle Mirrors/IMG_5119.JPG",
    'cat-paw-organizer':      PHOTOS / "Cable Holders/Closer up.jpg",
    'heart-lip-balm':         PHOTOS / "Lip palm holder/IMG_4903.JPG",
    'lip-balm-bag-charm':     PHOTOS / "Lip palm holder/IMG_4915.JPG",
    'slim-wallet':            PHOTOS / "Wallets/IMG_4792.JPG",
    'luggage-tag':            PHOTOS / "Luggage tags/IMG_4571.jpg",
    'slate-coaster':          PHOTOS / "Coasters/Slate Coasters.jpg",
    'square-slate-coaster':   PHOTOS / "Coasters/Aquare Coaster.jpg",
    'cork-coaster':           PHOTOS / "Coasters/Cork Coaster.jpg",
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
