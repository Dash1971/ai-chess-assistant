# chess-db relation template examples

## Queen-bishop battery toward h7

```bash
python3 chess_tools/query_nl.py "show me similar stonewall games with a queen-bishop battery toward h7" --compile-only
```

Compiles to:

```json
{"type": "battery_toward_square", "phase": "before", "color": "any", "back_piece": "Q", "front_piece": "B", "target_square": "h7"}
```

## Rook on semi-open c-file

```bash
python3 chess_tools/query_nl.py "show me exact black games with a rook on semi-open c-file" --compile-only
```

Compiles to:

```json
{"type": "rook_on_semi_open_file", "phase": "before", "color": "any", "file": "c"}
```

## Knight pinned to king on f6

```bash
python3 chess_tools/query_nl.py "show me exact games with a knight pinned to king on f6" --compile-only
```

Compiles to:

```json
{"type": "piece_pinned_to_target", "phase": "before", "pinned_color": "any", "piece": "N", "square": "f6", "target_piece": "K"}
```
