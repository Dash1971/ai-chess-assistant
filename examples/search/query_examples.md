# Query engine examples

The model should use `query_cli.py` for structural/pattern searches instead of reading PGN text directly.

There are now two modes:
- **exact queries** for literal matches
- **fuzzy queries** for similar ideas scored by optional motifs

See also:
- `fuzzy_query_examples.md`
- `query_translation_prompt.md`
- `nl_query_examples.md`
- `nl_query_test_prompts.md`
- `assistant_query_workflow.md`

## Example: queen defends bishop before Nd2

```json
{
  "player": "wonestall",
  "color": "white",
  "limit": 10,
  "context_window": 2,
  "sequence": [
    {
      "move": "Qc2",
      "move_by": "self",
      "predicates": [
        {"type": "piece_on_square", "phase": "before", "color": "opponent", "piece": "N", "square": "e4"},
        {"type": "move_adds_defender_to_piece", "color": "self", "defender_color": "self", "defender_piece": "Q", "piece": "B", "square": "d3"}
      ]
    },
    {
      "move": "Nd2",
      "move_by": "self",
      "within_plies": 4
    }
  ]
}
```

Run:

```bash
python3 chess_tools/query_cli.py --query-file examples/search/examples-queen-battery.json --pretty
```

## Supported step fields

- `move`: exact SAN match, e.g. `Qc2`, `Nd7`, `Bxh7+`
- `move_mode`: `exact` (default) or `regex` — useful for SAN disambiguation like `N.?d7` matching `Nd7` or `Nbd7`
- `uci`: exact UCI move, e.g. `d2f3`
- `move_by`: `self`, `opponent`, `white`, `black`, `any`
- `within_plies`: max distance from the previous matched step
- `predicates`: list of board-state checks

## Supported predicates

### `piece_on_square`
Check whether a square contains a given piece.

```json
{"type": "piece_on_square", "phase": "before", "color": "opponent", "piece": "N", "square": "e4"}
```

### `piece_count`
Count pieces by type and color.

```json
{"type": "piece_count", "phase": "before", "color": "self", "piece": "R", "min": 2}
```

### `piece_defended`
Check whether a piece on a square is defended.

```json
{"type": "piece_defended", "phase": "after", "color": "self", "piece": "B", "square": "d3", "defender_color": "self", "defender_piece": "Q"}
```

### `move_adds_defender_to_square`
Check if the just-played move increases defenders of a square.

```json
{"type": "move_adds_defender_to_square", "square": "e4", "color": "self", "piece": "Q"}
```

### `move_adds_defender_to_piece`
Check if the just-played move increases defense of the piece on a square.

```json
{"type": "move_adds_defender_to_piece", "color": "self", "defender_color": "self", "defender_piece": "Q", "piece": "B", "square": "d3"}
```

### `battery`
Loose same-line battery detection.

```json
{"type": "battery", "phase": "after", "color": "self", "back_piece": "Q", "front_piece": "B"}
```

### `piece_attacks_square`
Check whether a piece attacks a target square.

```json
{"type": "piece_attacks_square", "phase": "before", "color": "self", "piece": "B", "target_square": "h7"}
```

### `rook_on_open_file`
Check whether a rook sits on an open file.

```json
{"type": "rook_on_open_file", "phase": "before", "color": "self", "file": "e"}
```

### `rook_on_semi_open_file`
Check whether a rook sits on a semi-open file (no own pawn, at least one enemy pawn on that file).

```json
{"type": "rook_on_semi_open_file", "phase": "before", "color": "self", "file": "c"}
```

### `knight_outpost`
Check whether a knight is on a true outpost square: occupied by a knight, defended by a pawn, and not attackable by enemy pawns.

```json
{"type": "knight_outpost", "phase": "before", "color": "self", "square": "e5"}
```

### `battery_toward_square`
Check for a battery whose front piece attacks a target square.

```json
{"type": "battery_toward_square", "phase": "before", "color": "self", "back_piece": "Q", "front_piece": "B", "target_square": "h7"}
```

### `piece_pinned_to_target`
Check whether a piece on a square is pinned to its king or queen.

```json
{"type": "piece_pinned_to_target", "phase": "before", "pinned_color": "opponent", "piece": "N", "square": "f6", "target_piece": "K"}
```

### `opposite_side_castling`
Check whether White and Black have castled to opposite wings.

```json
{"type": "opposite_side_castling", "phase": "before"}
```

### `pawn_storm_against_castled_king`
Check whether a side has a real pawn storm against a castled king wing.

```json
{"type": "pawn_storm_against_castled_king", "phase": "before", "color": "self", "target_side": "king", "min_count": 2, "min_advance": 2}
```

### `rook_lifted`
Check whether a rook has been materially lifted off the back rank.

```json
{"type": "rook_lifted", "phase": "before", "color": "self", "min_advance": 2}
```

## Design rule

Use Python for retrieval. Use the model only to:
1. translate the user’s natural-language motif into JSON
2. inspect the returned candidates
3. explain which are pure examples vs loose analogues
