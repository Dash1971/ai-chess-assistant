#!/usr/bin/env python3
"""
Deterministically crop a 2-column x 3-row puzzle page into numbered board images.

This is for clean book pages like the Counting Problems sample where board order
must come from page layout, not detector/discovery order from earlier artifacts.

Usage:
  python recrop_page_grid.py --page page-2.png --labels 1-7,1-10,1-8,1-11,1-9,1-12 --out-dir out/page-2

The script finds 6 board-like squares on the page, sorts them top-to-bottom then
left-to-right, pads each crop to include coordinate labels, and writes numbered crops.
"""

import argparse
from pathlib import Path

import cv2
from PIL import Image
import numpy as np


def find_boxes(page_path: Path):
    img = cv2.imread(str(page_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"Could not read page: {page_path}")
    _, th = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)
    th = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=1)
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = img.shape
    boxes = []
    for c in contours:
        x, y, bw, bh = cv2.boundingRect(c)
        area = bw * bh
        if bw < 300 or bh < 300:
            continue
        aspect = bw / bh
        if not (0.75 < aspect < 1.25):
            continue
        if area >= 0.3 * w * h:
            continue
        boxes.append((x, y, bw, bh))
    if len(boxes) != 6:
        raise SystemExit(f"Expected 6 board boxes, found {len(boxes)} on {page_path}")

    # Robust reading order: cluster into 3 rows by y-center, then sort left-to-right within each row.
    centers = sorted(((y + bh / 2), i) for i, (x, y, bw, bh) in enumerate(boxes))
    rows = []
    row_threshold = 80
    for cy, idx in centers:
        placed = False
        for row in rows:
            if abs(cy - row['avg']) <= row_threshold:
                row['items'].append((cy, idx))
                row['avg'] = sum(v for v, _ in row['items']) / len(row['items'])
                placed = True
                break
        if not placed:
            rows.append({'avg': cy, 'items': [(cy, idx)]})
    rows.sort(key=lambda r: r['avg'])
    if len(rows) != 3 or any(len(r['items']) != 2 for r in rows):
        raise SystemExit(f"Could not form 3 rows of 2 boards on {page_path}: {rows}")
    ordered = []
    for row in rows:
        row_boxes = [boxes[idx] for _, idx in row['items']]
        row_boxes.sort(key=lambda b: b[0])
        ordered.extend(row_boxes)
    return ordered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", type=Path, required=True)
    ap.add_argument("--labels", required=True, help="Comma-separated labels in reading order")
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--pad-left", type=int, default=70)
    ap.add_argument("--pad-top", type=int, default=30)
    ap.add_argument("--pad-right", type=int, default=25)
    ap.add_argument("--pad-bottom", type=int, default=80)
    args = ap.parse_args()

    labels = [x.strip() for x in args.labels.split(",") if x.strip()]
    if len(labels) != 6:
        raise SystemExit("--labels must contain exactly 6 labels")

    boxes = find_boxes(args.page)
    page = Image.open(args.page).convert("RGB")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for (x, y, w, h), label in zip(boxes, labels):
        l = max(0, x - args.pad_left)
        t = max(0, y - args.pad_top)
        r = min(page.width, x + w + args.pad_right)
        b = min(page.height, y + h + args.pad_bottom)
        crop = page.crop((l, t, r, b))
        crop.save(args.out_dir / f"{label}.png")
        print(f"{label}: {x},{y},{w},{h} -> {args.out_dir / (label + '.png')}")


if __name__ == "__main__":
    main()
