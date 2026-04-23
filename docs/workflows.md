# Workflows

## Main workflows in this repo

- study sync and source-list maintenance
- search/query across a chess corpus
- opponent/account scouting
- opening-study extraction from public accounts
- opening concept and study-output generation
- chess.com speedrun PGN extraction for later study ingestion

## Generic opening-guide pipeline

The repo now exposes a generic opening pipeline layer in `chess_tools/`:

- `opening_configs.py` — opening registry/configuration
- `tag_opening.py` — generic opening tagger entry point
- `generate_opening_guide.py` — generic guide generator entry point

Current configured openings:
- `stonewall`
- `french`

The older opening-specific scripts still work, but they are no longer the only interface.

Example usage:

```bash
python3 chess_tools/tag_opening.py stonewall --db <games.pgn> --output /tmp/stonewall.json
python3 chess_tools/generate_opening_guide.py stonewall --input /tmp/stonewall.json --output stonewall-cheatsheet.pdf
```

```bash
python3 chess_tools/tag_opening.py french --db <games.pgn> --output /tmp/french.json
python3 chess_tools/generate_opening_guide.py french --input /tmp/french.json --output french-cheatsheet.pdf
```

## Typical study flow

The usual operating sequence is:

1. pull games from a public account or archive
2. import them into Lichess studies
3. annotate and organize them in Lichess
4. add the study URLs to a source list
5. sync the studies into a local PGN corpus
6. run search, coaching, or document-generation workflows against that local corpus

This repo ships the generic tooling and a minimal example layer.
