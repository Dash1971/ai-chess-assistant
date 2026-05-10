# Opponent report

## What it does

This workflow downloads an opponent's public games and turns them into a scouting report.

Typical report contents:
- opening tendencies
- time-control breakdown
- castling and king-safety patterns
- rating-band performance
- improvement trajectory by pool (bullet/blitz/rapid/classical where available)
- PDF dossier output plus machine-readable `analysis.json`

## Main file

- `skills/chess-opponent-scout/scripts/analyze_player.py`
- `skills/chess-opponent-scout/scripts/build_pdf.py`

## How it works

1. download a player's games from chess.com or lichess
2. build analysis data from those games
3. generate a polished PDF dossier from the analysis layer
4. review the resulting tendencies, weaknesses, and improvement trajectory

## Example command

```bash
python3 skills/chess-opponent-scout/scripts/analyze_player.py <username> tmp/<username> --platform chesscom
python3 skills/chess-opponent-scout/scripts/build_pdf.py tmp/<username>/analysis.json tmp/<username>/<username>-scouting-report.pdf
```

## Improvement model note

The improver-tier / percentile section is informed by public large-scale Lichess research from:
- <https://github.com/jcw024/lichess_database_ETL>

The scout uses that work as an anchor for approximate benchmarking. Direct-fit confidence is highest for Lichess blitz; other pools and platforms should be treated as proxy estimates.

## Current state

- the data-extraction engine is generic
- the PDF dossier path is now generic
- the improvement-trajectory section is embedded in the reusable analysis output
