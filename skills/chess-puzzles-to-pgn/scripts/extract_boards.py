#!/usr/bin/env python3
"""
Find likely chess-board regions on page images and crop them for verification.

This is a candidate finder, not a final truth machine.
It speeds up the workflow by extracting likely board crops plus a JSON manifest,
so the user can verify/transcribe instead of hunting through full pages manually.

USAGE:
    python extract_boards.py page.jpg --output-dir out/crops
    python extract_boards.py pages/*.jpg --output-dir out/crops --manifest out/boards.json
"""

import argparse
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


DARK_THRESHOLD = 80


def dilate(mask, steps=2):
    out = mask.copy()
    for _ in range(steps):
        padded = np.pad(out, 1, mode="constant", constant_values=False)
        out = (
            padded[1:-1, 1:-1]
            | padded[:-2, 1:-1]
            | padded[2:, 1:-1]
            | padded[1:-1, :-2]
            | padded[1:-1, 2:]
            | padded[:-2, :-2]
            | padded[:-2, 2:]
            | padded[2:, :-2]
            | padded[2:, 2:]
        )
    return out


def load_grayscale(path, max_dim=1600):
    img = Image.open(path).convert("L")
    scale = 1.0
    if max(img.size) > max_dim:
        scale = max_dim / max(img.size)
        new_size = (max(1, int(img.size[0] * scale)), max(1, int(img.size[1] * scale)))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    return img, scale


def connected_components(mask):
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=bool)
    components = []

    for r in range(h):
        for c in range(w):
            if not mask[r, c] or seen[r, c]:
                continue
            q = deque([(r, c)])
            seen[r, c] = True
            min_r = max_r = r
            min_c = max_c = c
            area = 0

            while q:
                rr, cc = q.popleft()
                area += 1
                if rr < min_r:
                    min_r = rr
                if rr > max_r:
                    max_r = rr
                if cc < min_c:
                    min_c = cc
                if cc > max_c:
                    max_c = cc

                for nr, nc in ((rr - 1, cc), (rr + 1, cc), (rr, cc - 1), (rr, cc + 1)):
                    if 0 <= nr < h and 0 <= nc < w and mask[nr, nc] and not seen[nr, nc]:
                        seen[nr, nc] = True
                        q.append((nr, nc))

            components.append({
                "top": min_r,
                "bottom": max_r,
                "left": min_c,
                "right": max_c,
                "area": area,
            })
    return components


def edge_score(mask, top, bottom, left, right):
    height = bottom - top + 1
    width = right - left + 1
    if height < 8 or width < 8:
        return 0.0
    band_h = max(2, height // 25)
    band_w = max(2, width // 25)

    top_band = mask[top:top + band_h, left:right + 1].mean()
    bottom_band = mask[bottom - band_h + 1:bottom + 1, left:right + 1].mean()
    left_band = mask[top:bottom + 1, left:left + band_w].mean()
    right_band = mask[top:bottom + 1, right - band_w + 1:right + 1].mean()
    return float((top_band + bottom_band + left_band + right_band) / 4.0)


def interior_density(mask, top, bottom, left, right):
    height = bottom - top + 1
    width = right - left + 1
    inset_h = max(2, height // 12)
    inset_w = max(2, width // 12)
    if height <= 2 * inset_h or width <= 2 * inset_w:
        return 0.0
    inner = mask[top + inset_h:bottom - inset_h + 1, left + inset_w:right - inset_w + 1]
    if inner.size == 0:
        return 0.0
    return float(inner.mean())


def expand_bbox(top, bottom, left, right, width, height,
                left_pad=0.14, right_pad=0.05, top_pad=0.05, bottom_pad=0.16):
    box_w = right - left + 1
    box_h = bottom - top + 1
    new_left = max(0, int(round(left - box_w * left_pad)))
    new_right = min(width - 1, int(round(right + box_w * right_pad)))
    new_top = max(0, int(round(top - box_h * top_pad)))
    new_bottom = min(height - 1, int(round(bottom + box_h * bottom_pad)))
    return new_top, new_bottom, new_left, new_right


def find_board_candidates(image_path, min_size=110, max_dim=1600):
    img, scale = load_grayscale(image_path, max_dim=max_dim)
    arr = np.array(img)
    dark = arr < DARK_THRESHOLD
    search_mask = dilate(dark, steps=2)
    comps = connected_components(search_mask)

    page_h, page_w = dark.shape
    candidates = []
    for comp in comps:
        top = comp["top"]
        bottom = comp["bottom"]
        left = comp["left"]
        right = comp["right"]
        width = right - left + 1
        height = bottom - top + 1

        if width < min_size or height < min_size:
            continue
        aspect = width / height
        if not 0.82 <= aspect <= 1.18:
            continue
        if width > page_w * 0.95 or height > page_h * 0.95:
            continue

        border = edge_score(dark, top, bottom, left, right)
        inner = interior_density(dark, top, bottom, left, right)
        if border < 0.35:
            continue
        if inner < 0.002:
            continue

        full_top = int(round(top / scale))
        full_bottom = int(round(bottom / scale))
        full_left = int(round(left / scale))
        full_right = int(round(right / scale))

        candidates.append({
            "top": full_top,
            "bottom": full_bottom,
            "left": full_left,
            "right": full_right,
            "width": full_right - full_left + 1,
            "height": full_bottom - full_top + 1,
            "aspect": round(aspect, 3),
            "border_score": round(border, 3),
            "inner_density": round(inner, 3),
            "area": comp["area"],
        })

    candidates.sort(key=lambda c: (-c["width"] * c["height"], c["top"], c["left"]))
    deduped = []
    for cand in candidates:
        keep = True
        for prior in deduped:
            dx = abs(cand["left"] - prior["left"]) + abs(cand["right"] - prior["right"])
            dy = abs(cand["top"] - prior["top"]) + abs(cand["bottom"] - prior["bottom"])
            if dx < 20 and dy < 20:
                keep = False
                break
        if keep:
            deduped.append(cand)
    return deduped


def crop_candidates(image_path, candidates, output_dir, prefix=None, annotate=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    stem = prefix or Path(image_path).stem
    manifest_rows = []

    annotated = img.copy() if annotate else None
    draw = ImageDraw.Draw(annotated) if annotate else None

    for idx, cand in enumerate(sorted(candidates, key=lambda c: (c["top"], c["left"])), start=1):
        top, bottom, left, right = expand_bbox(
            cand["top"], cand["bottom"], cand["left"], cand["right"], width, height
        )
        crop = img.crop((left, top, right + 1, bottom + 1))
        out_name = f"{stem}-board-{idx:02d}.png"
        out_path = output_dir / out_name
        crop.save(out_path)

        row = {
            "source_page": str(image_path),
            "crop_path": str(out_path),
            "candidate_index": idx,
            "board_bbox": {
                "top": cand["top"],
                "bottom": cand["bottom"],
                "left": cand["left"],
                "right": cand["right"],
            },
            "crop_bbox": {
                "top": top,
                "bottom": bottom,
                "left": left,
                "right": right,
            },
            "border_score": cand["border_score"],
            "inner_density": cand["inner_density"],
            "status": "needs_review",
            "diagram_id": "",
            "side_to_move": "",
            "comment": "",
        }
        manifest_rows.append(row)

        if annotate:
            draw.rectangle((cand["left"], cand["top"], cand["right"], cand["bottom"]), outline=(255, 0, 0), width=4)
            draw.text((cand["left"], max(0, cand["top"] - 20)), str(idx), fill=(255, 0, 0))

    annotated_path = None
    if annotate and annotated is not None:
        annotated_path = output_dir / f"{stem}-annotated.png"
        annotated.save(annotated_path)

    return manifest_rows, annotated_path


def main():
    parser = argparse.ArgumentParser(description="Extract likely chess-board crops from page images.")
    parser.add_argument("images", nargs="+", type=Path, help="Page image(s) to scan.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for cropped board images.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON manifest path.")
    parser.add_argument("--min-size", type=int, default=110, help="Minimum board width/height on the working image.")
    parser.add_argument("--max-dim", type=int, default=1600, help="Downsample long edge to this many pixels for detection.")
    parser.add_argument("--annotate", action="store_true", help="Also save page images with candidate boxes drawn.")
    args = parser.parse_args()

    all_rows = []
    for image_path in args.images:
        if not image_path.exists():
            raise SystemExit(f"Missing image: {image_path}")
        candidates = find_board_candidates(image_path, min_size=args.min_size, max_dim=args.max_dim)
        rows, annotated_path = crop_candidates(
            image_path, candidates, args.output_dir, annotate=args.annotate
        )
        all_rows.extend(rows)
        print(f"{image_path}: found {len(rows)} candidate board(s)")
        if annotated_path:
            print(f"  annotated: {annotated_path}")

    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(all_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Manifest -> {args.manifest}")


if __name__ == "__main__":
    main()
