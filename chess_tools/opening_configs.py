#!/usr/bin/env python3
"""Opening guide registry for generic opening-tag/guide commands."""

from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OPENING_CONFIGS = {
    "stonewall": {
        "id": "stonewall",
        "title": "Stonewall",
        "description": "Stonewall guide/tag pipeline built from wonestall games.",
        "tag_script": BASE_DIR / "tag_games.py",
        "guide_script": BASE_DIR / "generate_pdf.py",
        "default_tag_output": Path("/tmp/sw_data.json"),
        "default_pdf_output": BASE_DIR / "stonewall-cheatsheet.pdf",
        "default_html_debug": Path("/tmp/stonewall_cheatsheet.html"),
    },
    "french": {
        "id": "french",
        "title": "French Defense",
        "description": "French guide/tag pipeline built from sterkurstrakur games.",
        "tag_script": BASE_DIR / "tag_french.py",
        "guide_script": BASE_DIR / "generate_french_pdf.py",
        "default_tag_output": Path("/tmp/french_data.json"),
        "default_pdf_output": BASE_DIR / "french-cheatsheet.pdf",
        "default_html_debug": Path("/tmp/french_cheatsheet.html"),
    },
}


def get_opening_config(opening: str) -> dict:
    key = opening.strip().lower()
    if key not in OPENING_CONFIGS:
        valid = ", ".join(sorted(OPENING_CONFIGS))
        raise KeyError(f"Unknown opening '{opening}'. Valid openings: {valid}")
    return OPENING_CONFIGS[key]


def list_openings() -> list[dict]:
    return [OPENING_CONFIGS[k] for k in sorted(OPENING_CONFIGS)]

