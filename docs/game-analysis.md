# Game analysis

## What it does

This workflow analyzes a game against a local opening corpus and produces a coach-style explanation.

Current example opening families:
- Stonewall
- French Defense

## How it works today

The current implementation is a workflow rather than a single standalone CLI.

Typical sequence:

1. parse the input game reliably
2. detect which opening family applies
3. compare the game against the local opening database
4. retrieve matching examples or recurring themes
5. write an explanation or report card from the retrieved evidence

## Main building blocks

- `chess_tools/parse_pgn.py`
- search/query tooling in `chess_tools/`
- opening-specific tagging / comparison logic in the current skills and helper scripts

## Current state

Already implemented:
- opening-oriented comparison against a study database
- Stonewall/French example workflows
- structured prompting and grading logic in the current OpenClaw skills

Not yet fully cleaned up:
- a single reusable CLI that takes a PGN and emits the final report directly

## Practical use

Today the cleanest way to use this feature is:

1. make sure your local study DB is current
2. search or tag comparable examples
3. write the final analysis from the retrieved evidence

This is one of the likely candidates for a cleaner public feature once the workflow is packaged more generically.
