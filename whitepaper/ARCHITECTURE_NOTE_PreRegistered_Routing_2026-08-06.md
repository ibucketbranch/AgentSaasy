# Architecture Note — Pre-Registered Workflow Routing and the Four-Layer Stack
**Michael Valderrama | AI Agent Architect | Independent R&D © 2026**
**Date:** 2026-08-06
**Status:** DRAFT — brainstorm capture from working session. Not paper text. Claims marked [MEASURED] trace to existing experiment reports; claims marked [HYPOTHESIS] have no data yet and must not be published as findings.

---

## 1. The four layers, one job each

| Layer | Job | Status |
|---|---|---|
| **AEQ** | The metric. Business value delivered ÷ tokens consumed; latency reported alongside. Architecture quality, not cost. | Canonical (AEQ_Specification_v1.0) |
| **AEQ Grid** | The certification program. Pre-registered model × query-class runs against a locked bar; records tokens AND latency per cell. | Built, run (grid2q harness) |
| **Agent_AEQ** | The operator. An agent that ingests pre-registered workflows, runs the Grid on triggers (new workflow, model version bump), and emits the routing policy table. Absorbs the certification-as-CI/CD idea (~$0.02/cell). | Proposed — new |
| **Execution layer** | Certified narrow agents (or a swarm of them) running the workload. Consults the policy table; contains no routing intelligence. | Demo built (7 tools, 59 tests) |

Naming discipline: one name, one job. The certification program is never called "AEQ." The metric is never called a certifier. (This resolves the collision flagged 2026-07-28; the consulting handoff prompt still contains the merged definition and needs the fix.)

## 2. The core design move

**All intelligence runs offline in a slow loop; the runtime is a straight line.**

- **Registration time (Agent_AEQ):** Workflow Registry (machine-readable: class name, example queries, tools, equivalence rubric, locked pass bar) → Grid certification → **Routing Policy Table** (versioned, signed by the Grid run that produced it).
- **Execution time:** query → cheap in-taxonomy filter → policy lookup (class + mode tag) → certified agent → answer. Unmatched queries exit via the **escape hatch**: logged refusal, human hand-off. No model makes a routing decision at request time.

Rationale [MEASURED]: the routing study found a fixed cheap model rivaled trained per-request routers — runtime routing cleverness did not pay for itself. The policy table is static routing with more columns, not dynamic routing.

## 3. Multi-objective routing without runtime cleverness

Certification emits a small Pareto set per query class: **cost-mode** (cheapest adequate), **speed-mode** (fastest adequate), and the minimum tier that passes at all. Requests carry an objective tag set by channel/SLA (field-tech UI defaults speed-mode; batch planning defaults cost-mode). Trade-offs are resolved at certification time; runtime is a table lookup.

"Validated" is precise: a path that matches the goal with fewer tokens AND less time Pareto-dominates → unambiguous row. Faster-but-costlier is not a validation; it is a trade-off and lives in the speed-mode row.

Latency data already exists in Grid runs [MEASURED: 1.35 s single-tool, 8.70 s multi-tool, case-study table]. On simple classes the cheap tier is both cheapest and fastest, so most rows collapse.

## 4. Bounded domain: pre-registration fits EAM

Maintenance work is already procedural (work orders, PM schedules, inspections, capital planning); a CMMS is a registry of workflows. Pre-defining all workflows at registration is the domain's native shape, not a constraint.

- **Coverage ratio [HYPOTHESIS]:** share of real inbound queries landing inside registered classes. Never measured. Stated as a hypothesis with an instrument: the escape-hatch log. Every refusal is a candidate registration.
- **Escape-hatch accounting:** a correct refusal counts as value delivered (AEQ-L design decision), not waste. The in-taxonomy filter must itself be cheap and certified.

## 5. Loop taxonomy (what is and isn't loop engineering here)

| Loop | Timescale | Nature |
|---|---|---|
| Runtime dispatch | per query | **Not a loop.** Straight line by design; every runtime iteration is drift risk against the certificate. |
| Inside a certified agent | ms–s | Bounded ReAct loop, capped by the workflow definition. Single-turn AEQ covers it [MEASURED]. |
| Registration cycle | days–weeks | Control-systems feedback loop with a human gate: logs → coverage → new registrations → re-cert → new table. No unsupervised LLM inside. |

One sentence: **a slow smart loop wrapped around a fast dumb line.** VLIW analogy holds (scheduling decided offline by the smart thing, executed by the fast predictable thing) and is consistent with the LEOPARD framing fix of 2026-07-28: ARD = executing a pre-certified static routing policy.

## 6. Frame observation (possible resolution of the two-paper question)

The two candidate theses may be one causal chain, not competitors:

> Certification produces the economics [MEASURED: certified $0.0030/query vs frontier $0.0152 — the substitution advantage exists only on the certified tier] → the economics undercut per-seat pricing [consequence].

Adequacy measurement is the mechanism; SaaS substitution is the consequence. Substitution arrives as **scenario-assembled fleets of certified narrow agents** — faster to production than a platform release, priced by workload instead of by seat. Per-seat pricing dies because the unit of delivery changed, not because agents are cheap.

## 7. The only unmeasured load-bearing claims

1. **Coverage ratio** (§4) — instrument: escape-hatch log in deployment.
2. **Swarm coordination overhead [HYPOTHESIS]** — spec §11.5 gap. Three-arm experiment: (a) one frontier agent, (b) one certified cheap agent with all tools, (c) N certified narrow agents coordinating. Same scenario, equivalence rubric, cumulative tokens + wall-clock. If the swarm wins, thesis graduates; if it loses, the break-even is itself a finding.

Everything else in this note traces to existing runs or is a design decision, not a claim.

## 8. Build deltas (small; certification machinery already exists)

- Registry file format (YAML/JSON) — machine-readable version of the existing pre-registrations.
- Policy-table emitter on top of the grid2q harness.
- Dispatch loop (~50 lines) + in-taxonomy filter + escape-hatch logging.

---
*Session capture, Cowork 2026-08-06. Supersedes nothing; feeds the claim ledger.*
