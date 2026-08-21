# Agentic Substitution v3 — Blocker 1 & 2 Corrections

**Purpose:** drop-in replacement text for the two publication blockers.
**Blocker 1:** the ledger priced an uncertified model. Fixed by moving to the certified $0.0030 figure.
**Blocker 2:** implementation labor was acknowledged but never quantified. Fixed by a new Section 6.3 with a break-even derivation.

Every number below is recomputed and stated with its assumption. Items marked **[SUPPLY]** are ones only you can fill — placeholders are defensible but they are not your data.

---

## Before you paste: what actually changed

| | v3 draft | corrected |
|---|---|---|
| Cost per query in the ledger | $0.0009 (GPT-4o-mini, early 2026, $0.15/MTok — **never certified**) | $0.0030 (gpt-5.6-luna, AEQ refresh 2026-07-24, $1/MTok — **the certified tier**) |
| Annual model spend, 1,000 q/day | ~$288 | $1,095 |
| Agent spend as % of Premium seat bill | 2.2% | 8.3% |
| Cost advantage vs Premium | ~46× | **~12×** |
| Implementation labor | one clause | Section 6.3, with break-even |

You lose the 46× headline. You gain a paper that cannot be dismissed in one sentence. Take the trade.

---

## REPLACEMENT — Section 2 case-study table

Replace the two cost rows and add the third caveat paragraph.

| Measure | Value |
|---|---|
| Tools implemented | 7 |
| Test suite | 37/37 passing |
| End-to-end latency, single-tool query | 1.35 s |
| End-to-end latency, complex multi-tool query | 8.70 s |
| Average cost per query (GPT-4o-mini, early 2026, $0.15/$0.60 per MTok) | $0.0009 |
| Average cost per query (gpt-5.6-luna, certified, 2026-07-24, $1/$6 per MTok) | **$0.0030** |
| Memory per stateless instance | ~250 MB |

> Three caveats belong next to that table rather than buried in a limitations section. The demo dataset is 50 synthetic assets, not a live customer portfolio. The route optimizer was measured against statistical simulation rather than a live road network. And the two cost figures are not interchangeable: the first was measured in early 2026 on a model this program never certified, and is reported here only because it is what the v2.1.0 reference recorded. **Every economic argument in this paper uses the second figure**, the one measured on the tier that passed certification. A paper that argues for certifying before deploying does not get to price an uncertified model.

---

## REPLACEMENT — Section 6, opening through the arithmetic

> ### 6. The Economics Against Per-Seat Pricing
>
> The compute side of the ledger is measured, and it is measured on the model the certification program actually cleared. The AEQ refresh run of July 24, 2026 recorded **$0.0030 per query** on gpt-5.6-luna at $1.00/$6.00 per million tokens, the cheapest tier that passed every non-trap class of the hardened rubric. That is the number used throughout this section.
>
> It is not the cheapest number available. The v2.1.0 reference recorded $0.0009 per query on GPT-4o-mini in early 2026, and prior drafts of this paper used it. That figure is retired here for a reason the paper's own thesis demands: GPT-4o-mini was never put through the certification program described in Section 3. Pricing an uncertified model in a paper arguing for certification-first deployment would be an unforced contradiction, and a reader would be right to treat it as one. The correction costs the argument a factor of three and buys it internal consistency.
>
> The incumbent side of the ledger requires sourced, dated public prices, and estimates are not acceptable here because this is the table a skeptical reader checks first.
>
> *[incumbent pricing table unchanged — UpKeep / Limble / IBM Maximo, captured 2026-07-24]*
>
> Two observations before the arithmetic. Only one of the three vendors still publishes a list price at all; price opacity is itself part of the per-seat model this paper is examining. And the published prices are per human seat, a unit that has no relationship to the marginal cost of answering a maintenance question.
>
> **The arithmetic, with assumptions stated.** A 20-technician maintenance team on UpKeep Premium pays 20 × $55 = $1,100 per month, **$13,200 per year**, for the module list of Section 2. The AgentSaaSy_EAM stack answering 1,000 queries per day — 365,000 queries a year, roughly one query per technician every ten minutes of a working day — costs **$1,095 per year** in model spend at the certified $0.0030 per query. That is **8.3 percent of the seat bill, a cost advantage of roughly twelve to one**. On the Essential tier the same comparison is $5,760 against $1,095, or 19 percent. Seat prices for the quote-only vendors are, by construction, not comparable here, which is the point of recording them as quote-only rather than estimating.
>
> | Strategy | Annual model spend, 1,000 q/day | Share of Premium seat bill |
> |---|---|---|
> | UpKeep Premium, 20 seats | $13,200 | — |
> | UpKeep Essential, 20 seats | $5,760 | — |
> | Agent stack, **certified** tier ($0.0030/query) | **$1,095** | 8.3% |
> | Agent stack, frontier tier ($0.0152/query) | $5,548 | 42.0% |
>
> **The last row is the finding.** Running the same workload on the uncertified frontier model costs $5,548 a year — 42 percent of the Premium seat bill, and within four percent of the entire Essential seat bill. Against Essential, the substitution argument on the frontier model *disappears*. Certification is not a governance nicety layered on top of the economics; **certification is what produces the economics.** An operator who skips it and defaults to the biggest available model has, on this workload, spent away most of the advantage the substitution thesis depends on.

---

## NEW — Section 6.3, Total Cost of Ownership and the Break-Even Seat Count

This is the section that was missing. Paste after the arithmetic, before the accounting notes.

> ### 6.3 What the Model Spend Leaves Out
>
> Model spend is the smallest line on the agent side of the ledger, and a comparison that stops there is not an honest one. The incumbent's $13,200 buys hosting, support, an upgrade path, and somebody else's on-call rotation. The agent stack buys none of those. They have to be built and staffed, and that cost is large enough to reverse the conclusion at small seat counts.
>
> The assumptions below are stated so they can be argued with. They are drawn from **[SUPPLY: your actual build hours / your rate assumption]** and should be replaced with an operator's own figures before the conclusion is relied on.
>
> | Line item | Assumption | Annual |
> |---|---|---|
> | Production build, amortized | **[SUPPLY]** ~$150,000 over 3 years — data integration (PostgreSQL, ESRI, sensor feeds), auth, logging, deployment, hardening. *Not* the demo build. | $50,000 |
> | Maintenance and on-call | 0.15 FTE at $250,000 fully loaded | $37,500 |
> | Re-certification | ~1 engineer-day per vendor version bump, 4×/year. Judge spend itself is ~$0.02/cell and rounds to zero. | $4,000 |
> | Hosting | Two stateless instances (~250 MB each) plus load balancer | $1,800 |
> | Model spend, 20 seats | $0.0030 × 365,000 queries | $1,095 |
> | **Total, year one at 20 seats** | | **$94,395** |
>
> Against $13,200. **At twenty seats the agent stack loses by roughly seven to one**, and it loses for three years running. The compute was never the constraint. The engineering was.
>
> **Break-even.** Model spend scales with seats; the rest does not. At 50 queries per technician per day, compute runs $54.75 per seat per year against a Premium list price of $660 per seat per year, so each additional seat closes the gap by $605. With the fixed run cost of $43,300 and the build amortized over three years:
>
> | Comparison | Break-even seat count |
> |---|---|
> | vs UpKeep Premium ($660/seat/yr), build excluded | ~72 seats |
> | vs UpKeep Premium, 3-year amortized build | **~154 seats** |
> | vs UpKeep Essential ($288/seat/yr), 3-year amortized build | ~400 seats |
>
> Two things follow, and neither is comfortable for the strong version of the substitution thesis.
>
> First, **the twenty-technician team in the arithmetic above should keep buying the SaaS.** The per-seat license is, for them, a good deal — they are renting engineering they cannot justify hiring. The substitution argument is not an argument about small teams, and this paper should not be read as making one.
>
> Second, the break-even is a seat count, not a date, and that is what makes the prediction in Section 8 falsifiable. Substitution bites where the seat count is large enough to clear the fixed cost of building — and it bites at the margin, one module and one cohort of seats at a time, rather than as a platform replacement. A 400-seat customer who moves 250 seats' worth of inspection tracking to an internal agent stack has not churned. They have renewed smaller. That is the observable.
>
> The break-even figures are conservative in the incumbent's favour in one respect worth naming: they assign zero cost to the incumbent side beyond the license. Real deployments carry administration, configuration, integration, and training labour on the SaaS side too, none of which is counted here. Counting it would move break-even down. It was left out because this paper measured the agent side and did not measure the incumbent's, and an unmeasured adjustment in the direction of one's own thesis is exactly the move the rest of this paper is written to avoid.

---

## REPLACEMENT — Section 6 accounting notes, second note only

The current second note claims cheap-tier prices are falling. **Your own two data points say the opposite** and a reviewer will catch it: GPT-4o-mini was $0.15/MTok in early 2026; the cheapest tier you were willing to certify in July 2026 is $1.00/MTok. That is a 6.7× increase in the price of adequate capability.

> Second, the token side of this ledger has a direction, but not the simple one. The certified-cheap price used here ($1/MTok in, $6/MTok out) is higher per token than the $0.15/MTok model this project ran in early 2026. What falls across vendor generations is the price of a *given capability*, not the price of the cheapest tier on the menu — new budget tiers arrive priced against the capability they deliver, not against last year's floor. The operator-relevant quantity is the price of the cheapest tier that passes certification on the workload, and that quantity has to be re-measured on each generation rather than assumed to fall. Per-seat list prices, meanwhile, have not moved at all.

---

## Downstream edits — these will contradict you if you skip them

| Location | Current | Change to |
|---|---|---|
| **Abstract** | "at a measured $0.0009 average cost per query" | "at a measured $0.0030 average cost per query on the certified tier" |
| **Abstract** | "at one fifth the measured cost per query" | unchanged — correct ($0.0030 vs $0.0152) |
| **Section 1, point 1** | no figure cited | unchanged |
| **Section 9 conclusion** | "fit in seven tools behind one model at $0.0009 a query" | "at $0.0030 a query on a certified $1/MTok tier" |
| **Section 9 conclusion** | add after the deployment rule | one sentence carrying the break-even: "The rule pays for itself above roughly 150 seats and not below it." |
| **Figure: annual cost comparison** | bars at $13,200 / $5,760 / $288 | $13,200 / $5,760 / **$1,095**, plus a fourth bar at $5,548 for the frontier tier. Caption: "Agent figures are model spend only; see 6.3 for total cost of ownership." |
| **Section 7** | does not list TCO as unmeasured | now partly measured — add: "The total-cost figures in 6.3 rest on assumed labour rates, not on a recorded production build." |
| **Appendix: Where the Evidence Lives** | no row for the ledger | add row: "Certified cost per query → experiments/grid2q/refresh_gpt56_2026-07-24/phase0_report.md" |

---

## Bonus catch while I was in the numbers

The v2.1.0 reference is internally inconsistent on its own figure. Line 146 states cost per query as **$0.0009**. The annualized table at 11.3 derives **$288/year** from 1,000 queries/day — but $288 implies **$0.0008** and a 360-day year (30,000/month × 12). At a true 365 days and $0.0009 the figure is $328.

It does not matter once you move to the certified number, and I have used 365 days throughout above. But it is the kind of thing a reviewer finds while checking something else, and it is worth cleaning in v2.1.1 so the two documents agree.

---

## What I need from you to finish this properly

1. **Actual build hours** for the demo stack, and your estimate for a production build. The $150,000 is a placeholder. Your real number changes the break-even by a lot — at $60,000 the Premium break-even drops to about 105 seats; at $300,000 it climbs past 250.
2. **Loaded rate assumption.** I used $250,000/yr fully loaded. If you would rather state it as a contractor day rate, the table restructures.
3. **Whether 50 queries/technician/day survives contact with reality.** Lower it and compute drops, which raises break-even, because the fixed cost stays put.
