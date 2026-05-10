# jcw024 / lichess_database_ETL

## Source

- Repo: <https://github.com/jcw024/lichess_database_ETL>
- Main writeup used here: `README.md`
- Title: **How Long Does It Take Ordinary People To "Get Good" At Chess?**

## What the source is

A public analysis of large-scale Lichess game data focused on improvement rate rather than absolute chess strength.

## Dataset described in the README

- about **5.5 years** of data
- about **450 million games**
- about **2.3 million players**
- roughly **100 GB** loaded into PostgreSQL
- primary improvement analysis discussed in terms of **monthly average rating**
- strongest discussion is around **Lichess blitz**

## Why this source is useful

It is unusually valuable because it tries to answer the question most ordinary learners actually care about:
- how fast do people usually improve?
- how rare are major jumps?
- is my pace normal?

## Headline findings to use

### 1. Beginners improve much faster than intermediate players

The README says:
- most players in the **800-1000** range gain **100 lichess points in 3-6 months**
- in some filtered views, strong improvers in that range can gain 100 points in **1-2 months**
- most players in the **1600-2000** range take around **3-4 years** to gain 100 points

Core implication:
- improvement slows sharply as current strength rises

### 2. Most players do not improve that much

The README says:
- only about the **top 10%** achieve clearly meaningful long-run improvement (roughly >100 points)
- only about **1%** break past **200+ points** within a few years
- the majority of players hover near their starting rating even across long periods

Core implication:
- large gains are possible, but they are not normal

### 3. Big jumps happen, but they are outliers

The README reports:
- from the **800-1200** starting range, there are players who improved **500+** or even **800+** points
- these big improvers appear to have made those gains in a little under **2 years** on average
- but they are a small minority of the total sample

Core implication:
- dramatic adult-improver stories are plausible, but should be framed as outlier outcomes, not baseline expectations

### 4. Playing more games alone does not strongly predict faster improvement

The README says there is:
- no clear 1:1 linear relationship between number of games played and improvement
- maybe a weak sweet spot around **100-300 games per month**
- but no evidence that brute-force bingeing games is the main driver

Core implication:
- study quality and training likely matter more than raw game volume alone

## What this source directly supports

Use it confidently for questions like:
- "How long does 100 lichess points usually take?"
- "Do beginners improve faster than stronger players?"
- "How rare is a 200-point jump?"
- "Is playing tons of games enough by itself?"
- "Is this rate of improvement normal or unusually fast?"

## What this source does NOT directly support

Be careful with questions like:
- exact probability of reaching a specific final rating such as **1800 rapid** by a deadline
- adult-only outcomes specifically
- rapid/classical-specific outcomes when the published discussion is mainly blitz
- causal claims about what training method works best
- exact conversion to OTB ratings or FIDE ratings

## Best way to answer target-rating questions

For questions like:
- "What are the odds an adult reaches 1800 lichess rapid in 5 years?"

use this approach:
1. say the source does **not** directly give exact odds for that target
2. translate the question into the nearest supported form:
   - starting range
   - approximate rating gain needed
   - how unusual that size of gain is in the source
3. give a plain-language estimate like:
   - common
   - plausible
   - uncommon
   - rare
   - outlier-level
4. explain the caveats:
   - blitz vs rapid mismatch
   - adults not isolated as a subgroup
   - target rating ≠ net gain alone

## Recommended plain-language bands

When an exact probability is not supported, use qualitative odds bands such as:
- **common**
- **plausible**
- **uncommon**
- **rare**
- **outlier-level**

Only use numeric odds if a future source actually gives them.

## Good example answer shape

> Short answer: reaching 1800 lichess rapid within 5 years as an adult looks possible, but probably uncommon rather than normal.
>
> Why: this source shows that big gains do happen, especially from beginner starting points, but the majority of players do not make massive long-run jumps. The people who gain several hundred points quickly are real, but they are the minority, not the baseline.
>
> Caveat: that is an inference from mostly blitz-focused Lichess data, not a direct adult-only rapid estimate.

## Bottom line

Treat this source as:
- **strong** on broad improvement-rate expectations
- **strong** on rarity / percentile framing
- **moderate** on extrapolating to ambitious target-rating questions
- **weak** on exact target-specific odds without further modeling
