#!/usr/bin/env python3
"""
Generate deterministic board crops and labeled square contact sheets for manual audit.

Purpose:
- stabilize board order (reading order, not detector order)
- make square-by-square verification fast
- provide a fail-closed review artifact before PGN delivery

Usage examples:
  python generate_audit_sheets.py \
    --page page-1.png \
    --box 411,536,479,487,1-1 \
    --box 1173,535,479,487,1-4 \
    --out-dir out

  python generate_audit_sheets.py \
    --crop page-2-board-01.png,1-7 \
    --crop page-2-board-02.png,1-8 \
    --out-dir out
"""

import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw


def parse_box(text):
    x, y, w, h, label = text.split(",", 4)
    return int(x), int(y), int(w), int(h), label


def parse_crop(text):
    path, label = text.rsplit(",", 1)
    return Path(path), label


def save_contact_sheet(crop, out_path):
    w, h = crop.size
    sqw = w / 8
    sqh = h / 8
    files = "abcdefgh"
    ranks = "87654321"
    contact = Image.new("RGB", (4 * 180, 16 * 120), "white")
    k = 0
    for r in range(8):
        for c in range(8):
            left = int(round(c * sqw))
            top = int(round(r * sqh))
            right = int(round((c + 1) * sqw))
            bottom = int(round((r + 1) * sqh))
            cell = crop.crop((left, top, right, bottom))
            cell = ImageOps.contain(cell, (150, 90))
            canvas = Image.new("RGB", (180, 120), "white")
            canvas.paste(cell, ((180 - cell.width) // 2, 20))
            draw = ImageDraw.Draw(canvas)
            draw.text((8, 5), f"{files[c]}{ranks[r]}", fill="red")
            x0 = (k % 4) * 180
            y0 = (k // 4) * 120
            contact.paste(canvas, (x0, y0))
            k += 1
    contact.save(out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", type=Path, help="Source page image for --box entries")
    parser.add_argument("--box", action="append", default=[], help="x,y,w,h,label")
    parser.add_argument("--crop", action="append", default=[], help="crop_path,label")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--pad-left", type=int, default=70)
    parser.add_argument("--pad-top", type=int, default=30)
    parser.add_argument("--pad-right", type=int, default=25)
    parser.add_argument("--pad-bottom", type=int, default=80)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    page_img = Image.open(args.page).convert("RGB") if args.page else None

    for box_text in args.box:
        if page_img is None:
            raise SystemExit("--page is required when using --box")
        x, y, w, h, label = parse_box(box_text)
        l = max(0, x - args.pad_left)
        t = max(0, y - args.pad_top)
        r = min(page_img.width, x + w + args.pad_right)
        b = min(page_img.height, y + h + args.pad_bottom)
        crop = page_img.crop((l, t, r, b))
        crop.save(args.out_dir / f"{label}.png")
        save_contact_sheet(crop, args.out_dir / f"{label}-squares.png")

    for crop_text in args.crop:
        path, label = parse_crop(crop_text)
        crop = Image.open(path).convert("RGB")
        crop.save(args.out_dir / f"{label}.png")
        save_contact_sheet(crop, args.out_dir / f"{label}-squares.png")


if __name__ == "__main__":
    main()
