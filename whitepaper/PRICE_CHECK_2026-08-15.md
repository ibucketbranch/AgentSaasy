# Price re-verification, 2026-08-15

Run before the second-wave LinkedIn post, which leads with dollar figures. Prior capture:
`PRICE_CHECK_2026-08-07.md`. Sources fetched directly from the vendors' own pricing pages.

## Seat prices, upkeep.com/pricing

| Tier | 2026-07-24 | 2026-08-07 | 2026-08-15 | Change |
|---|---|---|---|---|
| Essential | $24/user/mo | $24 | **$24** | none |
| Premium | $55/user/mo | $55 | **$55** | none |
| Professional | quote-only | quote-only | **quote-only** | none |
| Enterprise | quote-only | quote-only | **quote-only** | none |

Derived annual figures for the 20-technician comparison are therefore unchanged:
Essential 20 x $24 x 12 = **$5,760**, Premium 20 x $55 x 12 = **$13,200**.

## Model prices, developers.openai.com/api/docs/pricing (standard tier, per MTok)

| Model | Role in the study | 2026-07-24 | 2026-08-07 | 2026-08-15 | Change |
|---|---|---|---|---|---|
| gpt-5.6-sol | frontier reference | $5.00 / $30.00 | $5.00 / $30.00 | **$5.00 / $30.00** | none |
| gpt-5.6-luna | certified tier | $1.00 / $6.00 | $0.20 / $1.20 | **$0.20 / $1.20** | none since 08-07 |
| gpt-5.6-terra | not used in any run | $2.50 / $15.00 | not checked | **$2.00 / $12.00** | repriced down |

## What this changes

Nothing in the paper, the post, or any published figure. Every dollar amount the second-wave
post depends on ($5,760, $13,200, $5/MTok frontier, $0.20/MTok certified) is unchanged from the
figures already published, so the post is clear to run as written.

One correction landed in the harness: `experiments/grid2q/aeq_grid2q_phase0.py` had
gpt-5.6-terra pinned at $2.50/$15.00. Terra was never used as a system under test and appears in
no run record or claim, so no result is affected, but the constant would have produced wrong
costs on the next run and is now $2.00/$12.00.

The luna repricing captured on 2026-08-07 (5x down, $1.00/$6.00 to $0.20/$1.20) still holds
eight days later, which strengthens rather than weakens the paper's pricing-note argument that
cost-per-query figures in the paper are upper bounds.

Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026
