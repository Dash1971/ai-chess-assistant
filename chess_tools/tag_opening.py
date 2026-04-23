#!/usr/bin/env python3
"""Generic opening tagger.

Dispatches to the current opening-specific taggers via a shared config layer,
so callers can use one stable CLI while the underlying tagging logic is still
being generalized.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from opening_configs import get_opening_config, list_openings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tag games for a configured opening.")
    parser.add_argument("opening", nargs="?", help="Opening id, e.g. stonewall or french")
    parser.add_argument("--db", dest="db", help="Path to the PGN database")
    parser.add_argument("--output", dest="output", help="Path to the tagged JSON output")
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
    if args.db:
        env["OPENING_PGN_PATH"] = str(Path(args.db).resolve())
    if args.output:
        env["OPENING_TAG_OUTPUT"] = str(Path(args.output).resolve())

    cmd = [sys.executable, str(cfg["tag_script"])]
    if not args.quiet:
        output_path = args.output or cfg["default_tag_output"]
        print(f"[tag_opening] opening={cfg['id']} output={output_path}")
    completed = subprocess.run(cmd, env=env)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

