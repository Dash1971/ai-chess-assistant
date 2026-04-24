# chess-db fuzzy query examples

Use fuzzy queries when the user asks for **similar ideas**, not just literal matches.

## Design rule

- **Required steps** = hard constraints
- **Optional steps** = ranking signals
- Steps are evaluated in order; `within_plies` is measured from the previous matched step
- The model should keep the sequence small and meaningful
- If the question is crisp, prefer exact queries
- If the question says *like this*, *similar*, *analogous*, *same idea*, or *closest examples*, prefer fuzzy queries

## Fuzzy schema

```json
{
  "player": "wonestall",
  "color": "black",
  "limit": 10,
  "context_window": 2,
  "sequence": [
    {
      "move": "Qc7",
      "move_by": "self",
      "required": true,
      "predicates": [
        {"type": "piece_on_square", "phase": "before", "color": "opponent", "piece": "N", "square": "e5"}
      ]
    },
    {
      "label": "queen-bishop battery right after queen move",
      "move_by": "self",
      "within_plies": 0,
      "required": false,
      "weight": 2.5,
      "predicates": [
        {"type": "battery", "phase": "after", "color": "self", "back_piece": "Q", "front_piece": "B"}
      ]
    },
    {
      "label": "queen adds defense to bishop on d6",
      "move": "Qc7",
      "move_by": "self",
      "required": false,
      "weight": 3.0,
      "predicates": [
        {"type": "move_adds_defender_to_piece", "color": "self", "defender_color": "self", "defender_piece": "Q", "piece": "B", "square": "d6"}
      ]
    },
    {
      "move": "N.?d7",
      "move_mode": "regex",
      "move_by": "self",
      "within_plies": 4,
      "required": true
    }
  ]
}
```

## Run fuzzy search

```bash
python3 chess_tools/query_cli.py --fuzzy-file examples/search/examples-fuzzy-queen-battery-black.json --pretty
```

## Compile only

Useful for debugging the model’s JSON output.

```bash
python3 chess_tools/query_cli.py --fuzzy-file examples/search/examples-fuzzy-queen-battery-black.json --compile-only
```

## Translation guidance for the model

### If the user asks:
- “show me exact examples”
- “only true examples”
- “where exactly this happened”

Use **exact** query JSON.

### If the user asks:
- “show me similar ideas”
- “closest examples”
- “same concept in a different position”
- “analogous pattern”

Use **fuzzy** query JSON.

### Good fuzzy behavior

- make the anchor move or anchor position **required**
- make motif-strengthening details **optional** with weights
- use regex when SAN disambiguation may vary (`N.?d7`, `R.?e1`)
- use small windows (`within_plies`) when the concept depends on timing

### Bad fuzzy behavior

- turning every detail into `required: true`
- leaving out the anchor move entirely
- producing 10 optional steps with tiny weights
- relying on prose instead of predicates
