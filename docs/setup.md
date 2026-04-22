# Setup

This repo is a starting point for building an OpenClaw-based chess coach locally.

It assumes you already have OpenClaw installed. If not, start here:
- <https://docs.openclaw.ai>

## What you need
- Python 3
- OpenClaw workspace capable of running skill scripts
- your own PGN corpus if you want to go beyond the included sample data
- your own study/source lists if you want to use the sync workflows seriously

## Minimum setup path

1. clone the repo
2. install Python dependencies with `pip install -r requirements.txt`
3. read `docs/workflows.md`
4. inspect the sample files in `examples/`
5. replace the sample data with your own corpus and source lists

## What works from this repo alone
- reading the docs
- inspecting the public skills and reusable tooling
- experimenting with the minimal example data in `examples/`

## What you add for real use
- a larger working `games.pgn`
- the source lists you actually want to maintain
- your own target openings, concepts, and study priorities
