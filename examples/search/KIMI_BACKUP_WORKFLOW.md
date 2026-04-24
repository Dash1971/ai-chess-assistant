# Kimi Backup Workflow for search stack

Use this when the backup model needs to answer a chess-db question without a stronger orchestrator guiding every step.

## Goal

Reduce model discretion.
Do **not** ask Kimi to invent the whole search plan from scratch.

Instead, use the procedural wrapper first.

## Primary command

```bash
python3 chess_tools/query_backup.py "<natural language chess question>"
```

This forces a fixed ladder:
1. normalize fuzzy attack wording when possible
2. parse prompt
3. compile normal chess-db query
4. if the wording matches a known attack shape, run the deterministic backup sequence
5. if still empty, retry forced fuzzy mode
6. return interpretation + best link + summary

## Why this exists

The raw stack is powerful, but backup models can fail when asked to:
- interpret a messy query
- choose exact vs fuzzy
- invent the search path
- rank candidates
- summarize all in one hop

`query_backup.py` narrows the job.

## Rules for Kimi

1. **Use `query_backup.py` first** for normal chess-db questions.
2. If it returns a result, use that result directly.
3. If it returns `Need clarification`, ask for:
   - one anchor move, or
   - one target square, or
   - one follow-up move
4. If it returns `No matches found`, restate the interpretation it used and then optionally inspect:
   ```bash
   python3 chess_tools/query_nl.py "<question>" --compile-only
   ```
5. Remember the backup wrapper now canonicalizes:
   - `rook uplift` / `rook uplifted` / `lifted rook` -> `rook lift`
   - `queen rook battery` / `queen+rook battery` / `heavy-piece battery` -> `queen-rook battery`
   - `leading to checkmate` / `mate` / `mating finish` -> `mate finish`
6. Do not default to Stonewall. Only narrow when the prompt explicitly says Stonewall, French, or Habits.

## Good usage examples

```bash
python3 chess_tools/query_backup.py "find a game with bishop sac on h7 and attacking continuation"
```

```bash
python3 chess_tools/query_backup.py "show me games with rook lift then rook swing within 8 plies"
```

```bash
python3 chess_tools/query_backup.py "find a game with opposite-side castling, pawn storm, and heavy-piece follow-up"
```

```bash
python3 chess_tools/query_backup.py "find me a game with a rook uplift which resulted in a queen rook battery leading to a checkmate"
```

## Debug path if needed

If output looks weak:

```bash
python3 chess_tools/query_nl.py "<question>" --parse-only
python3 chess_tools/query_nl.py "<question>" --compile-only
python3 chess_tools/query_answer.py "<question>"
```

## Key principle

Kimi should not act like the search engine.
Python retrieves. The model interprets and reports.
