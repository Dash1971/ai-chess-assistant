# chess-db opposite-side castling examples

## Opposite-side castling

```bash
python3 chess_tools/query_nl.py "show me similar stonewall games with opposite-side castling" --compile-only
```

Compiles to:

```json
{"type": "opposite_side_castling", "phase": "before"}
```

## Pawn storm against kingside castled king

```bash
python3 chess_tools/query_nl.py "show me similar stonewall games with pawn storm against kingside castled king" --compile-only
```

Compiles to:

```json
{"type": "pawn_storm_against_castled_king", "phase": "before", "color": "any", "target_side": "king"}
```

## Combined shape

```bash
python3 chess_tools/query_answer.py "show me similar stonewall games with opposite-side castling and pawn storm against kingside castled king"
```

This is intentionally narrow. It checks for the structural shape, not full strategic evaluation.
