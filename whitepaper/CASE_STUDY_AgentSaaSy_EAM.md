# Case Study: A Platform's Worth of EAM Workflows in Seven Tools

**Kind:** Case study
**Version:** 1.1
**Date:** 2026-08-31 (v1.0 published 2026-08-07)
**Author:** Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026

**Client:** Internal R&D build (AgentSaaSy_EAM)
**Domain:** Enterprise asset management for utility-grade operations
**Stack:** Python, LangChain, one certified language model, seven domain tools

## The problem

Commercial EAM/CMMS platforms sell asset registry, condition monitoring, predictive maintenance, TCO reporting, compliance tracking, field dispatch, and capital planning as per-seat licenses. A 20-technician team on a mid-market Premium tier pays about $13,200 a year for that module list. The question this build set out to answer: how much engineering does that module list actually require, and what does it cost to run once built?

## The build

Seven Python tools behind one language model: asset query, health analysis, failure prediction with composite risk scoring, TCO calculation, compliance tracking, field route optimization, and Monte Carlo capital planning with 1,000-iteration convergence. Orchestration is standard LangChain tool binding at temperature 0. The architecture is deliberately boring, and that is the point: the module list of a licensed platform fits in a reasoning layer, a tool layer, and an orchestration layer.

The AI-assisted demo build took roughly 40 to 80 engineer-hours, verifiable in the repository's commit history.

## The measurements

- 59 of 59 unit and integration tests passing (37 tool tests, 22 capital-planning tests)
- End-to-end latency: 1.35 s single-tool, 8.70 s multi-tool (measured early 2026)
- Cost per query on the certified model tier: $0.0030 (AEQ Grid certification run, July 2026)
- The certified $1/MTok tier matched a $5/MTok frontier model 12 cells to 12 on the workload's non-trap query classes

**Pricing note (added 2026-08-31):** the certified-tier prices behind the $0.0030 figure were verified 2026-07-24 for the July 2026 certification run. On 2026-08-07 the vendor repriced the certified tier to $0.20 per million input tokens and $1.20 per million output tokens, roughly a 5x cut, so the run-date figure stands as an upper bound. The white paper's dated pricing postscript carries the full accounting.

## The honest limits

The demo runs on a 50-asset synthetic portfolio, not a live customer deployment, and the route optimizer was measured against statistical simulation rather than a live road network. Total cost of ownership matters: with build and maintenance labor counted, the agent stack does not beat the per-seat license below roughly 130 seats. Small teams should keep their SaaS. The full accounting, including the assumptions an operator should replace with their own, is in the white paper.

## Read the engineering

The complete formal specification, test inventory, and simulation methodology: [Agentic Architecture for Enterprise Asset Management](/papers/agentic-architecture-enterprise-eam/) (technical reference, v2.1.1).

**Want this measured against your workflow?** A bake-off engagement runs your workload against your incumbent path under a pre-registered rubric and reports the same numbers you see above: tokens, cost, latency, and whether the answers hold up. [Contact](/contact/) to scope one.

---

## Version history

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Initial publication via prompts/Website_CaseStudy_Papers_Handoff.md |
| 1.1 | 2026-08-31 | Dated pricing note added under the measurements (2026-08-07 certified-tier reprice makes $0.0030 a run-date upper bound); technical-reference citation bumped to v2.1.1; copy extracted from the handoff prompt into this canonical source file |
