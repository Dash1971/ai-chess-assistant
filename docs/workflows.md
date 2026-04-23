# Workflows

## Main workflows in this repo

- study sync and source-list maintenance
- search/query across a chess corpus
- opponent/account scouting
- opening-study extraction from public accounts
- opening concept and study-output generation
- chess.com speedrun PGN extraction for later study ingestion

## Typical study flow

The usual operating sequence is:

1. pull games from a public account or archive
2. import them into Lichess studies
3. annotate and organize them in Lichess
4. add the study URLs to a source list
5. sync the studies into a local PGN corpus
6. run search, coaching, or document-generation workflows against that local corpus

This repo ships the generic tooling and a minimal example layer.
