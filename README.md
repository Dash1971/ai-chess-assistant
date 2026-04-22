# OpenClaw AI Chess Coach

OpenClaw AI Chess Coach is a practical template for using **OpenClaw** as a chess study and training assistant.

It shows how to combine:
- reusable OpenClaw skills
- local chess tooling
- a PGN corpus
- study-source sync scripts
- example workflows for coaching, scouting, and opening prep

If you want to build your own agent-backed chess coach, this repo is meant to give you a clean starting point.

---

## What you can do with it

This repo is built around a few concrete workflows:

- **Sync an opening database** from study/source lists into a local PGN corpus
- **Search that corpus** by move order, structure, theme, or natural-language question
- **Analyze games** against an opening-specific reference database
- **Scout opponents** from public chess accounts
- **Extract opening study material** from public player histories
- **Generate concept sheets and opening cheat sheets** from recurring patterns in the corpus
- **Pull and chunk speedrun PGNs** from chess.com for later study import

The included opening families — **Stonewall**, **French**, and **Habits** — are examples. The same structure can be adapted to any repertoire you want to study.

---

## Who this is for

This repo is for people who want to:
- use OpenClaw for a serious personal chess workflow
- keep their own study corpus locally
- build reproducible chess-analysis pipelines instead of one-off chat prompts
- adapt a working system rather than start from scratch

---

## How to use this repo

### 1. Read the docs
Start with:
- `docs/setup.md`
- `docs/workflows.md`
- `docs/search-system.md`
- `docs/opening-families.md`

### 2. Explore the example layer
The `examples/` directory gives you a small sample PGN, a sample source list, and example queries so you can see the structure without needing a full corpus first.

### 3. Point the tooling at your own data
For real use, replace the sample inputs with your own:
- PGN corpus
- source/study lists
- target openings
- generated documents or reports

### 4. Wire the skills into OpenClaw
The `skills/` directory shows how the agent-facing layer is organized, while `chess_tools/` contains the reusable code those workflows depend on.

---

## Repository layout

```text
README.md
LICENSE
requirements.txt
docs/
skills/
chess_tools/
examples/
scripts/
```

### `docs/`
Readable documentation for setup, architecture, workflows, search, limitations, and data model.

### `skills/`
OpenClaw skills for chess coaching, scouting, study extraction, concept generation, database sync, and speedrun PGN extraction.

### `chess_tools/`
The reusable Python layer: PGN parsing, search/query logic, sync/update scripts, tagging helpers, diagram helpers, and document-generation utilities.

### `examples/`
Minimal sample inputs for understanding the workflow and testing the structure.

### `scripts/`
Thin repo-level helpers and notes.

---

## What this repo is

This is not a polished chess product or a hosted service.

It is a **working public toolkit** for people who want to replicate an OpenClaw-based chess coach locally, study how the pieces fit together, and adapt the approach to their own opening systems and game database.

---

## Quick starting point

If you only want the shortest path:

1. install the requirements
2. read `docs/setup.md`
3. inspect `examples/`
4. run the search and parsing tools in `chess_tools/`
5. adapt the source lists and skills to your own repertoire

That is enough to understand the architecture and begin building your own version.
