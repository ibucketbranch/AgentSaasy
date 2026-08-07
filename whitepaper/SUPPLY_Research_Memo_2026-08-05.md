# [SUPPLY] Research Memo — Section 6.3 Inputs
**Michael Valderrama | AI Agent Architect | Independent R&D © 2026**
Prepared 2026-08-05. Evidence sources: local repo `~/Projects/AgentSaaSy` (git history at commit b194306), `AUDIT-2026-08-03.md`, NEXGEN project knowledge, and dated web sources cited inline.

**Frame dependency reminder:** these numbers only matter if the SaaS-substitution frame survives. If the paper moves to the "specs don't predict adequacy" thesis, Section 6.3 is moot (per Cowork handoff, Part 4). Numbers gathered anyway, as requested.

---

## 1. Actual build hours (demo) + production estimate

### Measured, from your own git history
- **60 commits over 11 active days**: Feb 10–11 (20 commits — the AgentSaasy → EAM transform), Mar 3 (AEQ study), Jul 23 – Aug 3 (39 commits — AEQ Grid, white paper, GIS, capital planning hardening).
- **Commit-spacing floor: ~31 active hours.** (Sum of gaps under 3h between consecutive commits, +30 min per session start.) This is a floor — design work, reading, and Cursor sessions that didn't end in a commit are invisible to it.
- **Defensible demo figure: 40–80 hours**, AI-assisted (Cursor + Claude Code). Codebase verified in AUDIT-2026-08-03: 5,590 LOC, 59 passing tests, 7 tools.
- **Recommended paper language:** "the demo stack was built in roughly 40–80 engineer-hours with AI-assisted tooling" — cite the commit history in the reproduction repo as the evidence trail.

### Production estimate
The corrections doc's $150,000 placeholder implies ~600 hours at ~$250/hr equivalent. Using a demo→production multiplier of 3–10× (data integration, auth, logging, deployment, hardening) on the 40–80h demo:
- **Range: 240–800 hours.** At the fully loaded senior rate below (~$137/hr effective), that is **$33k–$110k**, not $150k.
- **Recommendation:** state $100,000 over 3 years as the central estimate with the $60k–$150k sensitivity the corrections doc already computed (break-even ~105 → ~154 seats). This keeps the placeholder honest and moves break-even in your favor without you supplying anything unmeasured.
- **Caveat to carry:** the AI-assisted labor multiplier is itself one of the paper's themes (the "20–45×" labor bound in Section 6, accounting note 1). A production estimate assuming traditional dev hours would be higher; say which assumption you're making.

## 2. Loaded rate assumption

Your $250,000/yr fully loaded is **in range and citable**:
- Fully loaded = 1.25–1.4× base salary (benefits 15–20%, payroll tax 7.65%, equipment, recruiting) — [Arc.dev](https://arc.dev/employer-blog/software-developer-freelance-vs-full-time-costs/), [Glencoyne](https://www.glencoyne.com/guides/fully-loaded-cost-us-employee)
- US senior engineers: **$250k–$350k+ fully loaded** — [DontHireDevs 2026](https://www.donthiredevs.com/blog/the-real-cost-of-hiring-a-software-engineer-in-2026); average **$285k** across 60+ tech companies — [Full Scale](https://wp.fullscale.io/blog/software-developer-salary-2026/)
- AI-specialized engineers run **$300k–$460k** fully loaded — [AY Automate](https://www.ayautomate.com/blog/hire-ai-engineers-cost-guide)

**Recommendation: keep $250,000/yr fully loaded.** It's the conservative end of the senior range, so 0.15 FTE = $37,500/yr stands. If you prefer contractor framing: senior US contractor rates run ~$110–175/hr; 0.15 FTE ≈ 310 hr/yr ≈ $34k–$54k — same neighborhood, so the table doesn't need restructuring.

## 3. Queries/technician/day (the 50/day assumption)

**No public source measures "queries per technician per day" on a CMMS.** Closest measured proxies:
- Work orders completed per technician per day: **3.2 → 5.8** after CMMS adoption (municipal water utility case) — [OxMaint](https://oxmaint.com/article/mobile-cmms-field-technicians-manage-work-orders)
- Mobile CMMS saves ~58 min/user/day on admin; techs interact with the system well beyond one touch per work order (status checks, parts lookups, closeouts) — [eWorkOrders](https://eworkorders.com/how-maintenance-teams-use-cmms-every-day/)

A tech completing ~5 work orders/day with ~5–10 system interactions each lands at **25–50 interactions/day**. So 50/day is the **top of the defensible band**, not the middle.

**Recommendation:** present 50/day as the upper-bound assumption and state the band (10–50). Label it a hypothesis to be measured in deployment — consistent with how the Gemini-review taxonomy item was handled.

### ⚠ Error in the corrections doc, found while checking sensitivity
The doc's item 3 says lowering queries/day *raises* break-even. **The direction is backwards.** Break-even s = F ÷ (p − c), where c is per-seat compute. Lower query volume → lower c → larger denominator → **lower** break-even:
- At 50 q/tech/day: c = $54.75 → 43,300 ÷ 605.25 ≈ **72 seats** (build excluded)
- At 10 q/tech/day: c = $10.95 → 43,300 ÷ 649.05 ≈ **67 seats**
Fixed cost doesn't move, but compute is a *variable* cost — cutting it helps the agent side. The effect is small (±5 seats) but a reviewer running the algebra will catch the stated direction. Fix the sentence in "What I need from you" item 3 logic if it migrated into any draft text.

---

## Repo situation (the mistake you flagged)

Confirmed from the mounted local repo:
- `origin` now points at `git@github.com:ibucketbranch/AgentSaaSy_EAM.git` — the newer repo.
- Your original v1 material is preserved locally in `.archive-agentsaasy-v1/` (not git-tracked).
- **Full history is intact locally** — 60 commits back to the 2026-02-10 initial commit, including the original AgentSaasy → EAM transform. Nothing is lost; the question is only which GitHub remote is canonical.
- I **cannot verify or unarchive** the original `AgentSasy` GitHub repo from here: it's private (API returns only `claudeskills` + public repos) and the GitHub connector isn't authorized in this session.

**To fix the archive:** either (a) you do it in the browser — repo → Settings → Danger Zone → Unarchive, ~30 seconds; or (b) authorize the GitHub connector in claude.ai connector settings and I can unarchive, and if you want, consolidate the two repos (e.g., push the full local history to whichever name you keep and archive the other *deliberately* this time).

**Security note:** `.archive-agentsaasy-v1/API-Keys.txt` is plaintext API keys on disk. Not git-tracked, so not exposed — but if any of those keys were ever pushed to the old repo, rotate them before making anything public.

## Bonus: handoff open question #2 answered
`experiments/grid2q/` **is a runnable harness**, not just result files: `aeq_grid2q_phase0.py`, `grid_watchdog.sh`, plus dated result dirs (`phase0`, `phase0_v1_1`, `phase1_2026-07-24`, `refresh_gpt56_2026-07-24`, `localmodels_2026-07-29`, `multimodel_2026-07-24`). The `aeq-reproduce` public repo is a **packaging job, not a build**.
