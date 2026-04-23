# Opponent report

## What it does

This workflow downloads an opponent's public games and turns them into a scouting report.

Typical report contents:
- opening tendencies
- time-control breakdown
- castling and king-safety patterns
- rating-band performance

## Main file

- `skills/chess-opponent-scout/scripts/analyze_player.py`

## How it works

1. download a player's games from chess.com or lichess
2. build analysis data from those games
3. feed that data into a report-rendering layer
4. review the resulting tendencies and weaknesses

## Example command

```bash
python3 skills/chess-opponent-scout/scripts/analyze_player.py <username> tmp/<username> --platform chesscom
```

## Current state

- the data-extraction engine is already generic
- the remaining cleanup target is a generic report-rendering path that does not depend on staged or personalized sample artifacts

This means the underlying analysis capability is reusable now, but the final packaging can still be improved.
