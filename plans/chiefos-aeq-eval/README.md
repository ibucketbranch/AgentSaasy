# ChiefOS Swarm Evaluation Program - Master Plan

**Written 2026-08-16. Status: DESIGN. Nothing here is pre-registered until timestamped per Grid-2Q practice.**

Measure the ChiefOS agent swarm (the production document-intelligence system: orchestrator plus seven specialists, two local model tiers, budget-gated cloud fallback, on-device OCR, human review queue) with the AEQ methodology, and surface the results as a real-data visualization on bucketbranch.ai.

## Why this program matters to the AEQ body of work

AEQ Specification v1.1 section 11.5 names multi-agent attribution - how AEQ decomposes across orchestrator/worker teams - as an open limitation, and names the swarm coordination-overhead experiment (ARCHITECTURE_NOTE_PreRegistered_Routing_2026-08-06 section 7) as the designated instrument. ChiefOS is a production swarm already generating labeled ground truth (every human correction is a gold label; every review-queue resolution adjudicates halt-correctness). This program is that designated experiment, realized on real workload data. It is also the validation deployment AEQ-L (spec section 9, PROPOSED) needs before it can graduate.

## The three workstreams

Each has a full design document in this directory. They share one event vocabulary and one correlation spine (`cycle_id -> task_id -> call_id`), field-aligned with the existing `phase0_raw.json` record schema so swarm telemetry and Grid run records join in the same analysis code.

### 1. Telemetry (`01-telemetry-spec.md`) - implemented by the ChiefOS session

One append-only event stream, six event types (`cycle`, `agent_task`, `llm_call`, `fork_decision`, `ocr_extraction`, `outcome`), captured at two choke points (LLM client wrapper, orchestrator dispatch loop) plus three narrow tap-ins. Dual-written to JSONL and one JSONB table in the existing PostgreSQL. Fail-open: telemetry never blocks a filing operation.

Two load-bearing ideas:

- The `outcome` event turns the correction history into the AEQ-L numerator for free: a filing is `provisional_pass` at action time, `confirmed_pass` after a 14-day uncorrected window, `corrected_fail` when the human fixes it, and routing to review that the human validates is a `correct_refusal` (the spec 9.2 "correct halt counts as value" clause, made operational).
- Publishing is whitelist projection, not redaction: a public event is constructed from named fields (enums, counts, hashes) and free text does not exist in the public schema, so the site's do-not-publish list (no paths, no document data, no schema names, no ports, no prompts, no routing thresholds) is enforced by type, not by review.

Effort: 2-3 focused days for a session that knows the codebase; the first half day (LLM wrapper) already yields per-agent AEQ layer metrics.

### 2. Evaluation program (`02-evaluation-program.md`) - the AEQ side

Unit of certification is one document-task, not one orchestrator cycle: each dispatched job is single-turn-shaped, which keeps most of the program inside validated AEQ Grid machinery. Seven ChiefOS-native query classes (C-series), analogous to Q1-Q5 but grown from the real workload, including two trap classes: C5 urgency trap (the health-52 analog: urgent-sounding documents that require no action, plus one bland document hiding a real statutory deadline) and C6 correct refusal (routing to human review IS the pass, with one only-looks-hard item so blanket refusal fails). Ground truth comes from the corrections history; gold labels only back published rates.

Three tracks:

- **Track A - offline Grid certification** of the four tiers (frontier/cloud, local analyst, local fast, weak probe) against C1-C7. Direct reuse of the grid2q harness; the one required harness change is per-class evidence (today `EVIDENCE` is a single module-level constant). Output: the pass matrix that IS the routing policy table for ChiefOS's tier ladder.
- **Track B - live AEQ-L** from telemetry, with a locked outcome taxonomy (S1 auto-processed uncorrected, S2 correct refusal, F1 silent failure, F2 incorrect halt, F3 mechanical), a correction-latency window W pinned from the measured distribution (not guessed), and weekly GREEN/YELLOW/RED gates per class with a RED action of falling back one tier until re-certification. All AEQ-L values carry the spec section 9 PROPOSED label.
- **Track C - the coordination-overhead experiment** (the section 11.5 instrument): three arms on one frozen 100-document batch - one frontier agent, one certified cheap agent, the production swarm - measuring pass counts, cumulative tokens, and the orchestration-tax decomposition (orchestrator + handoff + duplicated-context tokens over total). Gates and priors declared before the run; if the swarm loses, the break-even is itself the finding.

Judging: Anthropic judge over qwen/gemma/OpenAI SUTs (cross-family rule), deterministic checks first wherever gold labels exist, 100% judging of refusals and corrections, 5% audit sampling of successes, fail re-adjudication carried verbatim from v1.1 practice. Judge COGS for the whole program: under $10/month.

The Student agent makes the SUT non-stationary: frozen (snapshot hash pinned) for Tracks A and C, covariate-and-rebaseline for Track B.

### 3. Live visualization (`03-live-visualization.md`) - the website side

- **Transport:** Mac mini pushes sanitized events outbound (solves home NAT) to Supabase via an authenticated Edge Function; the page reads a snapshot and subscribes to Realtime with the anon key. The site stays literally static - the data plane is external, same pattern as the existing analytics beacon. Permanent fallback shipped from day one: committed recordings of real sanitized cycles, played back under a "RECORDED RUN - REAL DATA" badge, so the page never depends on the mini being awake.
- **Page:** new `/projects/chiefos-live/`, copy-adapting the agentsaasy canvas engine with a ChiefOS topology: drop folder -> orchestrator -> seven specialists, a dashed tier rail (rules -> local fast -> local analyst -> cloud) that escalations visibly climb, review queue, filed. The existing agentsaasy demo page stays untouched and permanently SIMULATED; the chiefos page gets one static status chip linking over.
- **Honesty model:** a badge state machine - LIVE (realtime connected, cycle in progress), CONNECTED - SWARM IDLE (replaying last cycle between hourly wakes), LATEST CYCLE (snapshot, with age), RECORDED RUN (committed real recording). States only degrade downward. Replay defaults to labeled 60x compression with a 1x toggle.
- **Thresholds:** the page shows gate verdicts (GREEN/YELLOW/RED chips) and the AEQ-L reading, never the pre-registered threshold numbers, which stay on the do-not-publish list. The demo page's simulated threshold line is not copied over.
- **Meters:** AEQ-L card (labeled as an evaluation result with date), tokens this cycle, tier distribution (the thesis-carrying meter: local-first economics made visible), review-queue rate, coordination-overhead share, cycle counters.

Delivery respects the site coordination contract: the ChiefOS session queues work via its publish queue and messages the website session; nobody upstream edits the website repo.

## Phasing (merged across workstreams)

| Phase | What | Cost | Output |
|---|---|---|---|
| 0 (day 1, free) | B0: SQL over existing corrections history (correction-latency distribution pins window W; class mix pins Track C stratification). Telemetry phases 1-2 (LLM wrapper + cycle/task context managers). | $0 | Two registration parameters measured, not guessed; per-agent token/layer metrics flowing |
| 1 (week 1) | Finish telemetry (forks, outcomes, projector). Grid Phase A0: build C1-C7 corpus (synthetic/redacted, seeded from real failure patterns), register, run calibration (frontier + weak probe). Website v0: recorded-cycle page with RECORDED badge. | ~$3 | First publishable number: a calibrated, discriminating rubric for a personal-document workload; frontier C5 trap performance as the hook finding. Live page exists. |
| 2 (weeks 2-3) | Track A full grid (7 classes x 4 tiers x 3 runs). Website v1: Supabase provisioned, snapshot mode, staleness fallback. | ~$5 | The pass matrix / routing policy table: which classes certify onto $0-marginal local models. Page auto-updates. |
| 3 (one weekend) | Track C: the three-arm coordination-overhead experiment on the frozen batch. | ~$15 | The first measured number against spec 11.5. Headline result either way. |
| 4 (4-week window) | Track B live AEQ-L with weekly gates. Website v2: true realtime (LIVE badge). | ~$1.50/wk judge | Finalized outcome rates (measured) + AEQ-L readings (PROPOSED label) = section 11.3 graduation evidence for spec v1.2 |
| 5 (ongoing) | Fork-gated A/B: one fork at a time (cloud budget gate, degradation ladder, review threshold), each judged by AEQ-L delta. | ~$2/experiment | The steady-state program; section 9.6 rule 2 made empirical |

## What can be claimed when (house rule: published claims use real API results only)

- MEASURED and publishable: Track A matrices, tokens, latencies, calibration outcomes (including a failed calibration); Track C arm totals and the orchestration-tax decomposition; Track B finalized outcome rates; frontier trap performance on C5.
- ESTIMATED or caveated: local-inference $/query (no per-token price; label amortization); every AEQ-L value (always "AEQ-L [PROPOSED, per AEQ Spec v1.1 s9]"); anything on the synthetic corpus ("synthetic documents modeled on the production correction history").
- Never: absolute cross-domain AEQ scores; "the swarm is efficient" as a general claim. Only: for this workload, this batch, this configuration, the measured tax was X%.
- Internal only: provisional (pre-window-W) rates; raw confidences; anything outside the public-event whitelist.

## Who does what

| Actor | Work |
|---|---|
| ChiefOS session (on the Mac mini, owns the private codebase) | Implements `01-telemetry-spec.md`; runs B0 SQL; builds the C-series corpus from corrections history; runs the harness locally against Ollama tiers; exports sanitized recordings; queues website work per the coordination contract |
| This repo (AgentSaasy) | Harness change (per-class evidence field), C-series queries JSON, pre-registration documents (one per track, Grid-2Q format), analysis scripts |
| Website session (owns bucketbranch.ai repo) | Builds `/projects/chiefos-live/` (v0 recorded -> v1 snapshot -> v2 realtime), badge machine, chiefos status chip; verifies nginx CSP allows the Supabase origin |
| Supabase (provisioned once) | `swarm_events` / `swarm_cycles` tables, RLS read-only anon, ingest Edge Function with bearer secret, snapshot Storage object, retention cron |

## Open items the user should confirm

1. "AIOrganizer" appears nowhere in the site repo or these four repos; this plan treats ChiefOS as the swarm under test. If AIOrganizer is a distinct system, it becomes a second instrumented target using the same event schema.
2. Track C arm gates and priors are proposed in `02-evaluation-program.md` and need Michael's sign-off before registration (they are his priors to declare, not the assistant's).
3. The 14-day validation window default is a placeholder until Phase B0 measures the real correction-latency distribution.
