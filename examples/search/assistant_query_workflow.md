# Assistant-facing query workflow

Use `query_answer.py` when the goal is to answer a chess question in a human-readable way.

## Purpose

`query_nl.py` is the compiler/orchestrator.
`query_answer.py` is the presentation layer.

So the stack is:

1. user asks normal chess question
2. `query_answer.py` parses it via `query_nl.py`
3. exact/fuzzy engine runs
4. output comes back as a compact answer instead of raw JSON

## Example

```bash
python3 chess_tools/query_answer.py "show me exact wonestall black games where Qc7 came before Nbd7 with a white knight on e5"
```

## Fuzzy example

```bash
python3 chess_tools/query_answer.py "show me similar wonestall black games where Qc7 stabilized the bishop before Nbd7 with a bishop on d6"
```

## When to use which file

- `query_engine.py` — low-level exact retrieval
- `query_fuzzy.py` — low-level fuzzy ranking
- `query_cli.py` — raw structured JSON execution
- `query_nl.py` — natural language to compiled query JSON
- `query_answer.py` — final human-facing answer format

## Chat-agent pattern

For a chess-db question in chat:
1. call `query_answer.py` first
2. if it returns `Need clarification`, ask the user for one anchor move or board fact
3. if it returns weak/no matches, retry with fuzzier wording or forced `--mode fuzzy`
4. if needed, inspect `query_nl.py --compile-only` to debug translation
