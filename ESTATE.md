# ESTATE.md, where the AEQ program lives

> Read this BEFORE proposing repos, benchmarks, specs, or plans in any session.
> The program is further along than a fresh session assumes. Maintained by hand;
> update when a repo is added, moved, or retired. Last updated: 2026-08-27.

## The map

| Location | What it is | Remote |
|---|---|---|
| `~/Projects/AgentSaaSy` | **Canonical research home.** Claim ledger, experiments, publish queue, standing rules in its `CLAUDE.md` (terminology, naming, claim discipline). | `ibucketbranch/AgentSaasy` |
| `~/Projects/AEQ` | **Public curated method repo.** Spec (v1.2 current + layer-independence amendment), pre-registrations, runs, results, `AEQ_Lessons_Ledger.md` (append-only; it gets longer, which is the point). | `ibucketbranch/AEQ` (MIT) |
| `~/Projects/Blueberry` | **Private showcase + harness.** builder-gauge, token ledger, price table. Blueberry AEQ Showcase ran 2026-08-25: 180 cells, two arms, pre-registration frozen before the first cell (ledger L12 through L15). | `ibucketbranch/Blueberry` (private) |
| `~/Projects/loop-bench` | **Neutral target for builder-gauge** (MyRalphy vs. Ruflo two-arm build benchmark). Skeleton on `main`; tasks on `task/small` and `task/complex`; held-out tests live with the grader, not here. | local only |
| `~/HudsonClaw/repos/MyRaphy` | **The MyRalphy arm / driver.** Fork of michaelshimeles/ralphy (loop, engines, prompts, R-Minions PRD). *Pending move to `~/Projects/`.* | `ibucketbranch/MyRalphy` (renamed from `MyRaphy` 2026-08-25; the old URL still redirects, the local folder name was not changed) |

Adjacent, not part of the program: `~/Websites/*` (older web projects, incl. archives
and duplicates), `~/Developer/usd-aai-500-final` (USD capstone), HudsonClaw/Hermes
agent stack (its own world).

## Session rules

1. Orient first: read this file and `AgentSaaSy/CLAUDE.md` before planning anything.
2. One bench. Builder work continues **builder-gauge** (in Blueberry, target =
   loop-bench). Do not create new bench repos, ledgers, or metric definitions.
3. The spec is versioned. Current: **AEQ v1.2** in `AEQ/spec/`. Proposals go through
   amendments, not fresh definitions.
4. Check `AEQ_Lessons_Ledger.md` before designing measurement. Most mistakes have
   already been made once, on purpose or otherwise.
5. Claims follow the claim ledger discipline in AgentSaaSy. No ledger row, no claim.

## Why this file exists

2026-08-27: a Cowork session that could not see `~/Projects` spent a day re-designing
the benchmark program from scratch: duplicate protocol, duplicate bench plan, a
mission prompt one paste away from building a third harness (now superseded, see
`~/HudsonClaw/repos/AEQ_BENCH_PROMPT.md`). Two sessions, no shared state, one
re-derived estate. This file is the fix: the cost of a question includes the cost of
re-asking answered ones.
