# chess-db translation prompt notes

Use this when converting a user’s natural-language chess question into JSON for `query_cli.py`.

## Output choice

### Output EXACT query JSON when:
- user wants literal matches
- user says “exact”, “only true examples”, “same position”, “where this actually happened”

### Output FUZZY query JSON when:
- user wants similar ideas
- user says “closest examples”, “same concept”, “analogous”, “like this”

## Translation priorities

1. Identify the **anchor** first
   - a move (`Qc7`, `Ne5`, `Bxh7+`)
   - or a position fact (opponent knight on e5, same-side castling, rook on open file)
2. Identify the **timing relation**
   - before / after / within N plies
3. Separate **hard constraints** from **ranking signals**
4. Keep the JSON compact

## Good pattern

User:
> show me similar cases where Black played a queen move to stabilize the bishop before rerouting the knight

Good fuzzy JSON:
- required: queen move anchor
- required: knight reroute within 2-4 plies
- optional: battery exists after queen move
- optional: queen adds defense to bishop
- optional: opponent knight occupies the critical outpost

## Bad pattern

- describing the idea in prose instead of predicates
- making every nuance required
- omitting move timing
- using huge windows unless the user explicitly wants broad analogies
