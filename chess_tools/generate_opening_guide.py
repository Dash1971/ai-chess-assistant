#!/usr/bin/env python3
"""Generic opening guide generator.

Dispatches to the current opening-specific guide generators via a shared config
layer, so callers can use one stable CLI while the underlying rendering logic
is still being generalized.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from opening_configs import get_opening_config, list_openings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an opening guide for a configured opening.")
    parser.add_argument("opening", nargs="?", help="Opening id, e.g. stonewall or french")
    parser.add_argument("--input", dest="input_json", help="Path to the tagged JSON input")
    parser.add_argument("--output", dest="output", help="Path to the generated PDF output")
    parser.add_argument("--html-debug", dest="html_debug", help="Path to write the debug HTML")
    parser.add_argument("--list-openings", action="store_true", help="List supported opening ids and exit")
    parser.add_argument("--quiet", action="store_true", help="Reduce wrapper-level status output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_openings:
        for cfg in list_openings():
            print(f"{cfg['id']}: {cfg['description']}")
        return 0

    if not args.opening:
        parser.error("opening is required unless --list-openings is used")

    cfg = get_opening_config(args.opening)
    env = os.environ.copy()
    if args.input_json:
        env["OPENING_GUIDE_INPUT"] = str(Path(args.input_json).resolve())
    if args.output:
        env["OPENING_GUIDE_OUTPUT"] = str(Path(args.output).resolve())
    if args.html_debug:
        env["OPENING_GUIDE_HTML"] = str(Path(args.html_debug).resolve())

    cmd = [sys.executable, str(cfg["guide_script"])]
    if not args.quiet:
        output_path = args.output or cfg["default_pdf_output"]
        print(f"[generate_opening_guide] opening={cfg['id']} output={output_path}")
    completed = subprocess.run(cmd, env=env)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

