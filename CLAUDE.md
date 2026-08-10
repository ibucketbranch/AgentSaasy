# Project memory — AgentSaaSy (Michael Valderrama)

## Handoff routing rule (standing)
When Michael says "handoff" with no target named, he means: **Claude Code running inside Cursor (IDE)**. Write the handoff prompt for that environment: repo-aware, terminal-capable, file paths relative to this repo.
If he says "handoff to Hermes" or "handoff to HudsonClaw," the target is his local Hermes model (machine name HudsonClaw): assume local-only execution, no cloud APIs, and keep instructions self-contained.
Any other target must be named explicitly.

## Standing rules for all deliverables in this repo
- Terminology: "AI Agents" or "Agentic Agents" — NEVER "Agentic AI" (nor "agentic artificial intelligence" spelled out). Grep every deliverable.
- Naming discipline (spec v1.1 §2.1): AEQ = the metric; AEQ Grid = the certification program; Agent_AEQ = the proposed operator. One name, one job.
- Claim discipline: whitepaper/CLAIM_LEDGER.md governs. No row, no claim. Amend by dated entry, never silent edit.
- Attribution: "Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026"
- Address Michael as "big dog Michael" in chat; never inside formal artifacts.
- Canonical repo: github.com/ibucketbranch/AgentSaasy (EAM repo is archived/superseded; NGAI holds the original 4.68x reference implementation).
- Public curated repo: github.com/ibucketbranch/AEQ (created 2026-08-08, MIT). This is the ONLY public home for AEQ material: spec, harness, run reports, replay script. Populate by copying curated files — never by merging from AgentSaasy. Do not create additional AEQ repos; "aeq-reproduce" was this repo's working name and is retired.
