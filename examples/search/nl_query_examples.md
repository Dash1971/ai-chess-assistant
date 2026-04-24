# chess-db natural-language wrapper

`query_nl.py` is the rule-first entry point for plain-English chess searches.

It does five things:
1. parse the prompt
2. decide `exact` vs `fuzzy`
3. compile JSON for the deterministic engine
4. run the search
5. return results plus the compiled query

## Basic usage

```bash
python3 chess_tools/query_nl.py "show me exact wonestall black games where Qc7 came before Nbd7 with a white knight on e5" --pretty
```

## Parse only

```bash
python3 chess_tools/query_nl.py "similar wonestall black games where Qc7 stabilized the bishop before Nbd7" --parse-only
```

## Compile only

```bash
python3 chess_tools/query_nl.py "similar wonestall black games where Qc7 stabilized the bishop before Nbd7 with a bishop on d6" --compile-only
```

## What it understands today

### Search mode
- exact cues: `exact`, `literally`, `where exactly`, `only true examples`
- fuzzy cues: `similar`, `closest`, `analogous`, `same idea`, `like this`, `motif`, `pattern`

### Players
- `wonestall`
- `sterkurstrakur`
- `habitual`
- `Aman` + opening hint
  - `Aman` + `stonewall` -> `wonestall`
  - `Aman` + `french` -> `sterkurstrakur`
  - `Aman` + `habits` -> `habitual`

### Colors
- `as white`
- `as black`
- `white games`
- `black games`

### Study/opening filters
- `stonewall`
- `french`
- `habits`
- `london`

### Concrete anchors
- SAN moves like `Qc7`, `Nbd7`, `Bxh7+`, `O-O`
- board facts like `white knight on e5`, `bishop on d6`, `their rook on e-file` (square facts only today)
- timing hints like `before`, `after`, `then`, `followed by`, `within 4 plies`, `within 2 moves`

### Motif hints
- `battery`
- `defend`, `protect`, `stabilize`, `support`
- `rook on open e-file`
- `rook on semi-open c-file`
- `bishop pointed at h7`
- `queen-bishop battery toward h7`
- `knight outpost on e5`
- `knight pinned to king on f6`
- `opposite-side castling`
- `pawn storm against kingside castled king`
- `rook lift`
- `rook swing to g3`
- `bishop sac on h7`

### Composed sequence templates
- `rook lift then rook swing within 8 plies`
- `bishop sac on h7 and attacking continuation within 6 plies`
- `opposite-side castling, pawn storm, and heavy-piece follow-up`

These expand into normal query steps; they are not opaque engine-side macros.

## Current limits

This wrapper is intentionally narrow. It will **not** pretend to understand everything.

It is good at:
- anchor-move searches
- square occupancy facts
- short tactical/strategic sequences
- exact vs fuzzy selection
- a growing motif library (open/semi-open file rooks, bishop pressure on a square, batteries toward a target, knight outposts, simple pins, opposite-side castling, pawn-storm attack shapes, rook lifts/swings, simple sac patterns, and a few deterministic composed attack templates)

It is not yet good at:
- full positional prose without anchors
- semantic opening descriptions with no move or square hook
- abstract plan descriptions like `improve the bad bishop and then squeeze`
- piece relations without explicit squares

If the prompt is too vague, it should return `needs_clarification`.
