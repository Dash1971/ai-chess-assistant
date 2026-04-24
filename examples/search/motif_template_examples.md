# chess-db motif template examples

These are the first reusable positional motifs wired into the NL layer.

## Open-file rook

```bash
python3 chess_tools/query_nl.py "show me exact wonestall white games with a rook on open e-file" --compile-only
```

Compiles to a predicate like:

```json
{"type": "rook_on_open_file", "phase": "before", "color": "any", "file": "e"}
```

## Bishop pointed at h7

```bash
python3 chess_tools/query_nl.py "show me similar stonewall games where my bishop pointed at h7" --compile-only
```

Compiles to:

```json
{"type": "piece_attacks_square", "phase": "before", "color": "self", "piece": "B", "target_square": "h7"}
```

## Knight outpost

```bash
python3 chess_tools/query_nl.py "show me exact black games with a knight outpost on e4" --compile-only
```

Compiles to:

```json
{"type": "knight_outpost", "phase": "before", "color": "any", "square": "e4"}
```

## Important limit

These templates are narrow by design. They are meant to capture common chess concepts in a deterministic way, not fake broad positional understanding.
