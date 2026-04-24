# NL wrapper test prompts

## Exact

```bash
python3 chess_tools/query_nl.py "show me exact wonestall black games where Qc7 came before Nbd7 with a white knight on e5" --pretty
```

```bash
python3 chess_tools/query_nl.py "find exact stonewall black examples with Qc7 then Nbd7 within 4 plies and a white knight on e5" --compile-only
```

## Fuzzy

```bash
python3 chess_tools/query_nl.py "show me similar wonestall black games where Qc7 stabilized the bishop before Nbd7 with a bishop on d6" --compile-only
```

```bash
python3 chess_tools/query_nl.py "closest stonewall black examples where Aman used Qc7 in a battery idea before Nbd7" --parse-only
```

## Clarification expected

```bash
python3 chess_tools/query_nl.py "show me games where the position just feels harmonious"
```

## White-side analogue

```bash
python3 chess_tools/query_nl.py "show me exact wonestall white games where Qc2 came before Nd2 with a black knight on e4" --pretty
```
