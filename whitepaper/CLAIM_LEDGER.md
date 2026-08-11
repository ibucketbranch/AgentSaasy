# CLAIM LEDGER — The Cost of a Question
*(paper retitled 2026-08-07; formerly "The Agentic Substitution")*
**Michael Valderrama | AI Agent Architect | Independent R&D © 2026**
**Created:** 2026-08-06 | **Locked before drafting begins. No row, no sentence.**

**The rule:** every factual assertion the paper makes must have a row here with a green-enough status. A sentence with no row gets a row (and evidence) or gets cut. This ledger is the skeleton of the paper; sorted by status, it is also the to-do list.

**Status legend:**
- **REPRODUCIBLE** — evidence file exists in this repo; a reader can verify.
- **NEEDS RE-VERIFY** — evidence exists; a dated input (price, link) must be re-checked at publish time.
- **NEEDS RE-RUN / RE-PIN** — evidence exists but rests on a deprecated model or unjustified pin.
- **UNSUPPORTED-PENDING-SCRUB** — suspected harness artifact; publish nothing until the scrub verdict.
- **EMBARGOED** — evidence exists but is private until 2026-08-10 (routing study submission).
- **RETIRED** — true as a historical record, no longer the basis of any argument.
- **HYPOTHESIS** — no data; publishable only labeled as falsifiable prediction with its instrument named.
- **CONTEXT** — third-party citation; framing only, never evidence.

---

## A. Case study (Section 2)

| # | Claim | Evidence | Status |
|---|---|---|---|
| A1 | Seven tools implement the commercial EAM module list | `agent.py` (7 `@tool` decorators, verified at lines 149–652, AUDIT-2026-08-03) | REPRODUCIBLE |
| A2 | Test suite 59/59 passing (37 tool + 22 capital planning) | `tests/`, reproduced twice in AUDIT-2026-08-03 | REPRODUCIBLE |
| A3 | Latency 1.35 s single-tool / 8.70 s multi-tool | TECHNICAL-WHITE-PAPER.md §9, §11 | NEEDS RE-RUN — measured early 2026 on a since-retired model; either re-measure on the certified tier or label as dated measurement with model named |
| A4 | $0.0009 average cost per query | TECHNICAL-WHITE-PAPER.md §11 | RETIRED as economic basis (Blocker 1: uncertified model). Reportable only as what v2.1.0 recorded. Known internal inconsistency: $288/yr implies $0.0008 and a 360-day year — fix in v2.1.1 |
| A5 | ~$288/yr model spend at 1,000 q/day | derived from A4 | RETIRED — replaced by C2-derived $1,095/yr |
| A6 | Demo is 50 synthetic assets; route optimizer measured against simulation, not live roads | `data/asset_data.csv` (50 records verified), AUDIT-2026-08-03 | REPRODUCIBLE (disclosed caveat — keep beside the table, not in §7) |

## B. Architecture efficiency (AEQ metric)

| # | Claim | Evidence | Status |
|---|---|---|---|
| B1 | Same model, same query, equal value: 4.68x token / 5.04x cost spread across architectures (simulated); live dual-vendor measured range 2.04x–5.51x tokens with the simulation inside it | `experiments/aeq_dual_results.txt` (2026-07-23 real-API, two vendors, N=5, temp 0), `experiments/aeq_experiment_results.txt`, `experiments/STUDY-DESIGN.md`, spec §8 | REPRODUCIBLE — dual-provider run is the primary real-API evidence: moderate 1.15x/1.26x, severe 5.51x/4.97x/2.6x (OpenAI) and 2.04x/2.61x/1.81x (Anthropic); severe consistency 3/5 on Anthropic vs optimized 5/5 both vendors. Amended 2026-08-07 |
| B2 | Forced multi-tool orchestration: 3x cost, 3.6x latency, identical answers | same files, spec §8 | REPRODUCIBLE (same disclosure regime as B1) |
| B3 | Prompt overhead 13.9% optimized vs 29.4% severe bloat | same files, spec §4 | REPRODUCIBLE |

## C. AEQ Grid certification (Section 3)

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Cheap tier matched frontier 12/12 on non-trap classes | `experiments/grid2q/refresh_gpt56_2026-07-24/phase0_report.md` | REPRODUCIBLE |
| C2 | Certified tier $0.0030/query; frontier $0.0152/query (prices verified 2026-07-24) | same report | RE-VERIFIED 2026-08-07 — frontier unchanged ($5/$30); certified tier REPRICED to $0.20/$1.20 (5x cut). Paper states run-date figures as upper bounds with a dated postscript (~$219/yr at new price). Harness price constants in aeq_experiment.py need the same update before next run |
| C3 | Trap class: frontier failed 3/3; cheap tier 1/3 pass | same report + `multimodel_2026-07-24/phase0_report.md` | REPRODUCIBLE |
| C4 | Every model family and size fell for the trap at least once | `multimodel_2026-07-24/phase0_report.md` | REPRODUCIBLE — confirm the report states it across all families before citing |
| C5 | First rubric saturated and was discarded (calibration gate) | pre-registration series v1.0–v1.4.2, `AEQ_Lessons_Ledger.md` | REPRODUCIBLE (documented process) |
| C6 | Judge spend ~$0.02/cell | grid2q run reports | REPRODUCIBLE — confirm figure appears in report, not memory |
| C7 | Pre-registered prior confirmed (cheap tier failed exactly 2, both trap) | refresh report + pre-registration | REPRODUCIBLE |
| C8 | Judge: claude-opus-4-8, cross-family | run reports | RESOLVED 2026-08-07 — pin-justification paragraph added to §3.2 (fixed instrument for verdict comparability; re-evaluated per program, not per run) |
| C9 | Harness `aeq_experiment.py` model pin and pricing | `experiments/aeq_experiment.py` | RESOLVED 2026-08-07 — re-pinned to gpt-5.6-luna with explicit $1/$6 price constants (verified 2026-07-24, re-verify at publish); cost computed from constants, not the callback table; tokenizer falls back to o200k_base |

## D. Quantization and open-weight (Sections 3.3–3.4)

| # | Claim | Evidence | Status |
|---|---|---|---|
| D1 | 4-bit Q4 3B passed 3 cells where its fp16 parent passed 0, identical rubric | `experiments/grid2q/phase1_2026-07-24/phase0_report.md` + `SCRUB_REPORT.md` | REPRODUCIBLE — SCRUBBED 2026-08-09. All four suspects cleared with artifact evidence: identical per-class tokens_in across tiers (template), explicit temp 0 same body (sampling), zero template artifacts + complete answers (EOS), same endpoint/code path (stack). Inversion concentrated in Q5: Q4 derived correctly 3/3, fp16 confabulated a fake tool-output block 3/3. CLOSED 2026-08-09: templates verified identical by direct inspection AND inversion reproduced live on freshly pulled weights (Q4 answer character-identical to July run 3/3; fp16 confabulated structurally identical fake tool-output 3/3; tokens_in=832 both tags). Digests on file in SCRUB_REPORT Addendum 3 |
| D2 | 7B fabricated internally consistent numbers where 3B computed correctly | multimodel/localmodels runs | PENDING-SCRUB — separate evidence base; give it the D1 treatment before citing beyond the paper's current careful phrasing |
| D3 | qwen3.5 (9.7B Q4) certified 3/5 classes at zero marginal compute; gemma4 (12B) only 2/5 | `localmodels_2026-07-29/phase0_report.md` + `readjudication_2026-07-30.md` | REPRODUCIBLE — exploratory label mandatory; outside calibration gate |
| D4 | Thinking-model silent failure: entire output budget spent reasoning, no answer | same reports | REPRODUCIBLE (exploratory) |
| D5 | Local latency 280–335 s vs 4–8 s API (upper bound, shared host) | same reports | REPRODUCIBLE (exploratory, bounded) |
| D6 | Cheap API tier produced a retrieval failure on re-run it did not produce 5 days earlier (re-certification evidence) | same reports | REPRODUCIBLE |
| D7 | Registered prior for local run partly missed (quantitative predicted to fail; analytical/retrieval failed instead) | same reports + pre-reg v1.4.x | REPRODUCIBLE (honest-miss disclosure) |

## E. Routing study (Section 4)

| # | Claim | Evidence | Status |
|---|---|---|---|
| E1 | Full results table (oracle, routers, fixed model, commercial router) on 2,434 held-out prompts | routing study repo (USD AAI-501) | EMBARGOED until 2026-08-10 — verify link resolves and title matches at publish |
| E2 | Single cheap fixed model rivaled every trained router | same | EMBARGOED |
| E3 | Commercial router lost to every trained approach on cost and quality | same | EMBARGOED |
| E4 | LLM-as-router converged on the same fixed model (95% of traffic) | same | EMBARGOED |

## F. Economics (Section 6, corrected per Blocker 1 & 2)

| # | Claim | Evidence | Status |
|---|---|---|---|
| F1 | UpKeep $24 / $55 per user/mo; Limble and IBM Maximo quote-only (captured 2026-07-24) | vendor pricing pages, dated capture | RE-VERIFIED 2026-08-07 against upkeep.com/pricing — unchanged. Bonus: UpKeep's own implementation add-ons list at $500–$5,000+, supporting 6.3's zero-incumbent-setup-cost conservatism note |
| F2 | 20 seats Premium = $13,200/yr vs $1,095/yr certified model spend → 8.3%, ~12x advantage | derived: F1 × C2 × 365,000 q/yr | REPRODUCIBLE once C2 re-verified — corrections doc text pending merge into draft |
| F3 | Frontier tier same workload = $5,548/yr = 42% of Premium; substitution vs Essential disappears → certification produces the economics | derived: F1 × C2 frontier price | REPRODUCIBLE once C2 re-verified — this is the finding; keep it the finding |
| F4 | TCO year one at 20 seats ≈ $77,728; agent stack loses ~6:1 at small scale | §6.3 (merged 2026-08-07) + SUPPLY_Research_Memo_2026-08-05.md | ASSUMPTION-BASED — build $100k central over 3 yrs (git-history-derived 40–80h demo, 3–10x production multiplier), $250k loaded rate (sourced in memo). Assumptions stated in-text; operator invited to substitute |
| F5 | Break-even vs Premium ≈ 127 seats ($100k build; sensitivity ~105 at $60k / ~154 at $150k); ≈ 72 excluding build; ≈ 329 vs Essential | same derivation | ASSUMPTION-BASED — merged 2026-08-07. Volume direction stated correctly in-text: lower query volume LOWERS break-even (~72→~67); break-even is build-cost-dominated |
| F6 | "Seat bill runs 20 to 45 times measured compute" (current §6 accounting note) | derived from RETIRED A5 | RETIRED — recompute on certified basis: ~5x (Essential) to ~12x (Premium). Downstream edit required |
| F7 | Certified-cheap adequate capability got MORE expensive 2026 ($0.15 → $1.00/MTok); what falls is price of given capability, not price of adequacy | corrections doc replacement note; C2 vs A4 record | REPRODUCIBLE from own two data points — replaces the "prices are falling" note |
| F8 | Zero-marginal-compute floor under 3 of 5 classes (open-weight) | D3 | REPRODUCIBLE (exploratory label travels with it) |

## G. Predictions and hypotheses (Section 8 + architecture note)

| # | Claim | Instrument | Status |
|---|---|---|---|
| G1 | Substitution shows up as seat-count shrinkage at renewal, single-workflow tools first | renewal seat counts, category order | HYPOTHESIS (falsifiable, labeled — keep) |
| G2 | Coverage ratio: bounded EAM domain means most real queries land in registered classes | escape-hatch refusal log in deployment | HYPOTHESIS |
| G3 | Swarm of certified narrow agents beats both one frontier agent and one certified generalist on cumulative tokens at equal outcome | three-arm experiment (ARCHITECTURE_NOTE §7) | HYPOTHESIS — not in this paper except as designed future experiment |
| G4 | Static pre-certified routing policy with cost/speed rows serves multi-objective needs without runtime routing | ARCHITECTURE_NOTE_PreRegistered_Routing_2026-08-06.md | DESIGN CLAIM — grounded in E2 + C-series; publishable as architecture, not as measured outcome |

## H. Context citations (framing only, never evidence)

| # | Citation | Use |
|---|---|---|
| H1 | Blundin 40x deflation — Moonshots EP #208 (dated); quantization background EP #197 | CONTEXT for "why adequacy must be re-measured each generation." Never evidence for D1 |
| H2 | Goldberg, C. (2026-07-31), CIO Dive, cost-per-token breaks down per workload | CONTEXT — external support for thesis; verified link |
| H3 | Torres, R. (2026-07-30), CIO Dive, EY: 4 in 5 firms concerned about token costs | CONTEXT — verified link |
| H4 | LLMRouterBench (ACL 2026 Findings), RouteLLM, FrugalGPT, ReAct, Huang et al. ICLR 2024 | CONTEXT / related work as already cited in draft |

---

## Downstream edits the ledger forces (do these during the draft merge)

1. **Abstract + §2 + §6 + §9:** economic basis moves from $0.0009/$288 (RETIRED) to $0.0030/$1,095 per corrections doc. A4 stays only as the disclosed historical record beside the table.
2. **§6 accounting note:** "20 to 45 times" → recomputed ~5–12x (F6). "Token prices falling" note → F7 replacement text.
3. **§3.1:** "AEQ is an evaluation method" → the certification program is **AEQ Grid**; the metric is AEQ (spec v1.1 §2.1 governs). Sweep the whole draft.
4. **Repo pointers:** `AgentSaaSy_EAM` → `AgentSaasy` everywhere (title block, references, appendix) now that consolidation is done.
5. **§3.3:** quantization inversion text gets published only per D1's scrub verdict; if the scrub kills it, the section reports two findings and the scrub itself.
6. **Figures:** annual-cost bars re-drawn at $13,200 / $5,760 / $1,095 / $5,548 with TCO caption (corrections doc).
7. **Appendix:** add row for certified cost per query → `experiments/grid2q/refresh_gpt56_2026-07-24/phase0_report.md`; update routing row when repo flips public.
8. **v2.1.1 of TECHNICAL-WHITE-PAPER.md:** fix the $288/$0.0008/360-day inconsistency (A4).

## Launch notes (post-embargo, from WhitePaper_v3_Plan Workstream 5)

- Launch post tags: **Dave Blundin** (deflation context, H1) and **Chen Goldberg** (CoreWeave EVP, H2 author; warm contact via Michael's 2026-08-04 LinkedIn comment on her post).
- **Publishing rule (no gates, one principle):** a post ships when its links resolve and its claims have ledger rows. E-series links resolve when the routing repo flips public (2026-08-10, the USD submission date); paper/repo links resolve when the draft merge lands and `aeq-reproduce` goes public. Coursework posts inside the LMS need no public links and ship anytime.

## Dated amendments

- **2026-08-10 (2)** — Reference 2 restated (paper v3.1.2): the routing study repository is private and contains team coursework, so the citation now states the private status plainly and points readers to the Section 4 reproduction instead of a URL. E1-E4 remain EMBARGOED pending Michael's decision on a public carve-out of his own routing artifacts (candidate home: github.com/ibucketbranch/AEQ).

- **2026-08-10** — Harness reprice applied (closes the C2 "pending in the harness" note). `experiments/aeq_experiment.py`: pinned constants updated to gpt-5.6-luna $0.20 in / $1.20 out per MTok, verified 2026-08-07 (capture: `whitepaper/PRICE_CHECK_2026-08-07.md`); commit also lands the C9 re-pin (model pin, o200k_base tokenizer fallback, cost computed from constants). `experiments/grid2q/aeq_grid2q_phase0.py`: PRICING luna row updated likewise. `aeq_grid_experiment.py` carries only legacy-model rows and its PRICING_VERIFIED flag is already False; unchanged. No recorded result files touched.

---
*No report, no claim. Lock this file before drafting; amend by dated entry, never by silent edit.*
