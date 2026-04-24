# chess-db attack-shape examples

## Rook lift

```bash
python3 chess_tools/query_nl.py "show me similar stonewall games with rook lift" --compile-only
```

Compiles to:

```json
{"type": "rook_lifted", "phase": "before", "color": "any", "min_advance": 2}
```

Note: this is intentionally broad. It detects a materially advanced rook, not only a textbook third-rank lift.

## Rook swing to g3

```bash
python3 chess_tools/query_answer.py "show me similar stonewall games with rook swing to g3"
```

Compiles to a move regex like:

```json
{"move": "R.?g3[+#]?", "move_mode": "regex", "move_by": "any"}
```

## Bishop sac on h7

```bash
python3 chess_tools/query_answer.py "show me similar stonewall games with bishop sac on h7"
```

Compiles to:

```json
{"move": "Bxh7[+#]?", "move_mode": "regex", "move_by": "any"}
```

## Rook lift -> rook swing within N plies

```bash
python3 chess_tools/query_answer.py "show me exact games with rook lift then rook swing within 8 plies"
```

Compiles to ordinary sequence steps:
1. a predicate step requiring `rook_lifted`
2. a follow-up rook-move regex step within the requested ply window

Current default swing regex is intentionally broad when no destination square is given:
```json
{"move": "R[a-h1-8x]*[a-h][3-6][+#]?", "move_mode": "regex"}
```

## Bishop sac -> attacking continuation

```bash
python3 chess_tools/query_answer.py "show me exact games with bishop sac on h7 and attacking continuation within 6 plies"
```

Compiles to:
1. `Bxh7[+#]?`
2. a follow-up attacking move regex within the ply window

Current continuation rule is deliberately broad: if the prompt does not specify `check`, `queen`, `rook`, or `heavy-piece`, the continuation step accepts a generic attacking follow-up rather than pretending to know a richer tactical definition.

## Opposite-side castling + pawn storm + heavy-piece follow-up

```bash
python3 chess_tools/query_answer.py "show me exact games with opposite-side castling, pawn storm, and heavy-piece follow-up"
```

Compiles to:
1. an `opposite_side_castling` predicate step
2. a `pawn_storm_against_castled_king` predicate step
3. a heavy-piece move regex step (`Q...` or `R...` family by default)

## Future refinement

If these composed results prove too broad, refine with additional constraints:
- target file / destination square
- explicit attacker color when a player anchor exists
- `check` / `mate` / `queen follow-up` / `rook follow-up` wording
- castled-king target side (`kingside` / `queenside`)
