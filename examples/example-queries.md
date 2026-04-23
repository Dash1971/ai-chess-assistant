# Example commands and prompts

## Study DB sync + search

Sync a study list into a local database:

```bash
python3 chess_tools/update_db.py
```

Search a local PGN corpus:

```bash
python3 chess_tools/search.py --db examples/sample_games.pgn d4 d5 e3 e6 Bd3
```

## Typical workflow prompts

> Sync my Lichess study list and show me the newest Stonewall examples with a black knight on e4.

> Search the corpus for opposite-side castling plus a kingside pawn storm.

## AI coach game analysis

Typical prompt:

> Analyze this game against the Stonewall corpus and tell me the single biggest mistake in the opening plan.

Typical prompt:

> Analyze this game against the French corpus and grade the opening decisions.

## Opponent report

Download a chess.com player:

```bash
python3 chess_tools/analyze_player.py <username> tmp/<username> --platform chesscom
```

Typical prompt:

> Build a scouting report for this opponent and summarize the biggest exploitable opening patterns.

## Speedrun-study pipeline

Typical sequence:

1. pull games from a public chess.com speedrun account
2. import them into Lichess studies
3. annotate the studies
4. sync the study URLs into a local PGN corpus
5. search that corpus or generate study outputs from it
