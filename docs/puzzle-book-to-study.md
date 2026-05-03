# Puzzle-book to Lichess-study workflow

This workflow is for turning a scanned chess puzzle workbook into a Lichess-importable PGN, with one diagram per chapter.

It is meant for books where the source is a PDF scan rather than structured PGN, including older grayscale books and non-English books.

## What it does

The workflow helps you:
- rasterize a workbook PDF into high-resolution page images
- crop individual diagrams for verification
- measure square occupancy instead of trusting eyesight alone
- build structurally valid FENs
- assemble a multi-chapter PGN for Lichess study import

The public skill for this lives at:

- `skills/chess-puzzles-to-pgn/`

## Why this workflow exists

Scanned diagrams are easy to misread by one file or one rank.

That is enough to break the entire puzzle.

The key safeguard in this workflow is square-measurement:
- crop the board with rank/file labels visible
- run occupancy measurement on the crop
- compare the measurement grid with the visual transcription before finalizing the FEN

This is especially useful for:
- edge files (`a/b`, `g/h`)
- crowded positions
- noisy grayscale scans
- older instructional books with weak print quality

## Non-English books

This workflow is designed to handle non-English books too.

For Russian sources, the skill includes a reference for common chess notation and phrases:

- `skills/chess-puzzles-to-pgn/references/russian_chess_notation.md`

Typical examples:
- `Ход белых` = White to move
- `Ход чёрных` = Black to move
- `Кр` = king, `Ф` = queen, `Л` = rook, `С` = bishop, `К` = knight

The board glyphs are still standard chess pieces; the translation issue is usually in the surrounding puzzle text.

## Included scripts

- `scripts/automate_book.py` — rasterize a PDF, detect likely boards, export crops, and build a review manifest
- `scripts/extract_boards.py` — detect likely board regions from existing page images
- `scripts/detect_occupancy.py` — measure ink density per square on a board crop
- `scripts/check_fens.py` — validate structural FEN correctness
- `scripts/build_pgn.py` — template for assembling a Lichess-ready multi-chapter PGN

## Recommended setup

```bash
cd skills/chess-puzzles-to-pgn
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Dependencies:
- `numpy`
- `Pillow`

Recommended external tool:
- `pdftoppm` for rasterizing source PDFs into page images

## Basic operating flow

1. Run `scripts/automate_book.py` on the workbook PDF at about 250 DPI.
2. Review the generated candidate crops and manifest.
3. Catalog the diagrams and side-to-move prompts before transcribing.
4. Confirm or tighten each crop so rank/file labels are still visible.
5. Do a visual transcription of pieces and squares.
6. Run occupancy measurement on the crop and reconcile any disagreements.
7. Build a full FEN for each diagram.
8. Validate every FEN.
9. Assemble a multi-chapter PGN and import it into a Lichess study.

## Lichess output model

The intended output is a PGN where each diagram becomes one study chapter.

Key headers:
- `[SetUp "1"]`
- `[FEN "..."]`
- a descriptive `[Event]`
- a useful `[White]` label for the Lichess chapter sidebar

See also:
- `skills/chess-puzzles-to-pgn/references/lichess_pgn_format.md`

## Important limitation

This is still not a one-click OCR pipeline.

What is now automated:
- PDF rasterization
- likely-board detection
- initial crop export
- manifest generation

What remains verification-first:
- confirming which candidates are real diagrams
- reading the surrounding puzzle text
- identifying piece types and colors
- setting side to move and writing final FENs

That tradeoff is deliberate: for scanned chess books, measured semi-manual transcription is much more reliable than pretending full automation is already solved.
