#!/usr/bin/env python3
"""
Automate the front half of the puzzle-book workflow:
- rasterize a PDF into page images (optional)
- detect likely board regions on those pages
- crop them into a review directory
- build a JSON manifest for the remaining human verification steps

USAGE:
    python automate_book.py --pdf input.pdf --output-dir out/book
    python automate_book.py --pages-dir out/book/pages --output-dir out/book
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from extract_boards import crop_candidates, find_board_candidates


IMAGE_EXTS = {".png", ".jpg", ".jpeg"}


def rasterize_pdf(pdf_path, pages_dir, dpi=250, fmt="png"):
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm not found. Install poppler-utils or pass --pages-dir.")

    pages_dir.mkdir(parents=True, exist_ok=True)
    prefix = pages_dir / "page"
    cmd = [pdftoppm, f"-{fmt}", "-r", str(dpi), str(pdf_path), str(prefix)]
    subprocess.run(cmd, check=True)


def sorted_page_images(pages_dir):
    return sorted(
        p for p in pages_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )


def build_summary(manifest_rows):
    by_page = {}
    for row in manifest_rows:
        by_page.setdefault(row["source_page"], 0)
        by_page[row["source_page"]] += 1
    return {
        "page_count": len(by_page),
        "candidate_count": len(manifest_rows),
        "pages": [{"page": page, "candidates": count} for page, count in sorted(by_page.items())],
    }


def main():
    parser = argparse.ArgumentParser(description="Rasterize a puzzle book and extract likely chess-board crops.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf", type=Path, help="Source puzzle-book PDF.")
    group.add_argument("--pages-dir", type=Path, help="Pre-rendered page-image directory.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Working directory for pages/crops/manifest.")
    parser.add_argument("--dpi", type=int, default=250, help="Rasterization DPI when using --pdf.")
    parser.add_argument("--format", choices=("png", "jpeg"), default="png", help="Page image format when rasterizing.")
    parser.add_argument("--min-size", type=int, default=110, help="Minimum candidate board size on the detection image.")
    parser.add_argument("--max-dim", type=int, default=1600, help="Downsample long edge to this many pixels for detection.")
    parser.add_argument("--annotate", action="store_true", help="Save page images with candidate boxes drawn.")
    args = parser.parse_args()

    output_dir = args.output_dir
    pages_dir = args.pages_dir or (output_dir / "pages")
    crops_dir = output_dir / "crops"
    manifest_path = output_dir / "manifest.json"
    summary_path = output_dir / "summary.json"

    output_dir.mkdir(parents=True, exist_ok=True)

    if args.pdf:
        if not args.pdf.exists():
            raise SystemExit(f"Missing PDF: {args.pdf}")
        rasterize_pdf(args.pdf, pages_dir, dpi=args.dpi, fmt=args.format)

    if not pages_dir.exists():
        raise SystemExit(f"Pages directory does not exist: {pages_dir}")

    page_images = sorted_page_images(pages_dir)
    if not page_images:
        raise SystemExit(f"No page images found in {pages_dir}")

    all_rows = []
    for page_image in page_images:
        candidates = find_board_candidates(page_image, min_size=args.min_size, max_dim=args.max_dim)
        rows, annotated = crop_candidates(page_image, candidates, crops_dir, annotate=args.annotate)
        all_rows.extend(rows)
        print(f"{page_image.name}: {len(rows)} candidate board(s)")
        if annotated:
            print(f"  annotated: {annotated}")

    manifest_path.write_text(json.dumps(all_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary_path.write_text(json.dumps(build_summary(all_rows), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nManifest -> {manifest_path}")
    print(f"Summary  -> {summary_path}")
    print(f"Crops    -> {crops_dir}")
    print("\nNext step: review the crops, fill in diagram ids / side to move, then transcribe and validate FENs.")


if __name__ == "__main__":
    main()
