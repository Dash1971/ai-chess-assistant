---
name: chess-improvement-analyzer
description: Answer questions about chess improvement timelines, odds, percentiles, ceilings, and adult-improver expectations using published research. Use when the user asks things like "how long does it take to gain 100 points", "what are the odds an adult reaches 1800 lichess", "is this progress normal", "what percentile improver is this", or asks to interpret chess-improvement studies in plain language. Also use when adding new chess-improvement research sources or comparing multiple research findings.
---

# chess-improvement-analyzer

Answer chess-improvement questions in plain language from published research.

## Core rule

Default to the **published findings as source of truth**.

Do **not** clone, run, or replicate an external research repo unless one of these is true:
- the user explicitly asks for replication or audit
- the published writeup is too incomplete to answer the question responsibly
- two sources materially conflict and the conflict matters to the answer
- the user wants a new estimate that cannot be supported from the published results alone

For the current `jcw024/lichess_database_ETL` source, the published README is good enough for most plain-language answers.

## First read

When this skill triggers:
1. Read `references/api_reference.md` for the research policy and answer style.
2. Read the specific source note you need, starting with `references/jcw024-lichess-etl.md`.
3. Answer from the research directly.

## Answer style

Give:
- a short direct answer first
- then the reasoning in plain English
- then caveats only if they actually matter

Prefer wording like:
- "roughly"
- "ballpark"
- "based on this dataset"
- "the average player in this sample"
- "this is possible, but rare"

Avoid fake precision when the research does not support it.

## Required distinctions

Always distinguish between:
- **what the source directly shows**
- **what you are inferring from the source**
- **what the source does not let you answer confidently**

If a user asks a question beyond the data, say so plainly and give the nearest supported answer.

## Current source base

Start with:
- `references/jcw024-lichess-etl.md`

That source is strongest for:
- lichess improvement rate
- rating-gain timelines
- improver percentiles
- how unusual large gains are
- whether playing more games alone predicts faster improvement

It is weaker for:
- exact odds of reaching a specific final rating by a specific deadline
- adult-only causal claims
- rapid-specific claims when the published analysis is mostly blitz
- OTB/tournament equivalence

## Estimation policy

If the user asks something like:
- "what are the odds an adult reaches 1800 lichess rapid in 5 years?"
- "how long will the average learner take to get there?"

then:
1. State whether the source directly answers it.
2. If not, give a **bounded estimate** or **qualitative estimate** derived from the nearest evidence.
3. Explain the bridge:
   - blitz vs rapid
   - beginner vs already-intermediate
   - adult assumption vs general population sample
   - rating gain vs target-rating attainment
4. Label the estimate as an approximation.

## Good answer template

Use this shape when it fits:

1. **Short answer**
2. **What the research actually says**
3. **What that implies for your question**
4. **Main caveats**

## Adding future research

When a new chess-improvement source is added:
1. Create a new note under `references/` named for the source.
2. Capture:
   - source link
   - population
   - time controls
   - sample size
   - what the source directly supports
   - what it does *not* support
   - strongest headline findings
   - known caveats
3. Update `references/api_reference.md` to include it in the source list.
4. Do not merge claims from multiple sources casually; note when they align vs conflict.

## Default posture on the ETL repo itself

Right now, prefer **analysis of the published results** over local replication.

Replication can come later if Dash asks for one of these:
- confidence audit
- methodological critique
- custom estimates beyond the README
- updated reproduction from raw data
- extension to rapid/classical/adult-only subsets
