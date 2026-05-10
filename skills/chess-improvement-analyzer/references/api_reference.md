# Chess Improvement Research Index

## Purpose

This skill answers chess-improvement questions from published research, with plain-language output and explicit limits.

## Current operating model

Use published findings as the default evidence base.

That means:
- read the public writeup first
- answer from what it directly supports
- estimate carefully only when necessary
- avoid pretending the source proves more than it does

Do not recommend cloning or reproducing a research repo unless the user actually needs that extra rigor.

## Current sources

### 1. `jcw024-lichess-etl.md`
Use for:
- typical time to gain 100 lichess points
- improvement pace by starting strength
- how rare major rating gains are
- improver percentile framing
- whether heavy game volume alone predicts faster improvement

## Output standard

Every answer should separate:
- **direct evidence**
- **reasonable inference**
- **uncertain / unsupported territory**

## Preferred phrasing

Good:
- "Based on this dataset..."
- "The nearest supported answer is..."
- "Roughly..."
- "This looks possible but uncommon..."
- "The source is stronger on X than Y..."

Bad:
- "The odds are exactly..." when no exact odds exist
- "Adults usually..." when the source is not adult-only
- "Rapid players will..." when the source is mainly blitz

## When to escalate to replication

Replication or local setup is worth doing only when:
- Dash asks for an audit or reproduction
- you need subgroup estimates the public writeup does not provide
- you need exact counts / probabilities from the underlying dataset
- multiple sources conflict and the conflict matters
- the published methodology is too vague for the question at hand
