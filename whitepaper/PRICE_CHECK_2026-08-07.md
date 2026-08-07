# Price re-verification, captured 2026-08-07

Same-day captures for the publish checklist (ledger rows F1, C2). Sources fetched directly today.

## UpKeep (upkeep.com/pricing)

Unchanged from the 2026-07-24 capture.

| Tier | Price |
|---|---|
| Essential | $24/user/mo |
| Premium | $55/user/mo |
| Professional | Custom pricing |
| Enterprise | Custom pricing |

F1 re-verified. No downstream edits from this row.

## OpenAI (developers.openai.com/api/docs/pricing, confirmed on the gpt-5.6-luna model page)

| Model | Input /MTok | Output /MTok | vs 2026-07-24 capture |
|---|---|---|---|
| gpt-5.6-sol | $5.00 | $30.00 | unchanged |
| gpt-5.6-luna | $0.20 | $1.20 | CUT from $1.00 / $6.00 (5x) |

Cached input for luna: $0.02/MTok.

## Downstream impact of the luna cut

- C2: the certified-tier $0.0030/query was computed at $1/$6. At $0.20/$1.20 the same token mix lands near a fifth of that. Recompute from the grid2q run's token counts, do not scale by eyeball.
- F2: $1,095/yr certified spend and the ~12x Premium advantage both move by the same factor. The substitution case strengthens.
- F3: the "substitution vs Essential disappears at frontier pricing" finding is unaffected (sol unchanged), but the cheap-tier margin against Essential widens.
- F7: the claim "adequate capability got MORE expensive in 2026 ($0.15 to $1.00/MTok)" is falsified as of today. The series is now $0.15 to $1.00 to $0.20. The defensible replacement claim: the price of adequacy is volatile in both directions, which is the argument for dated captures and re-certification, not a monotonic story.
- Launch post draft: the line "the $1-per-million-token model matched the $5 frontier model" must carry the price current on posting day.
- Medium article: cites ratios only, no absolute prices. Unaffected.
- AEQ harness (experiments/aeq_experiment.py): pinned price constants for luna are now stale; update the constants and their verified-on date before any run whose dollar figures publish.

Prices in the paper are captures, not estimates; whichever day the paper publishes, re-pull both sources that day and update this note by dated entry rather than editing this one.
