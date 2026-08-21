# Contributing

Thanks for the interest. Two things live in this repo, and they have different rules.

## The agent (AgentSaaSy_EAM)

Issues and pull requests are welcome for the agent code, tools, tests, and docs.

- Open an issue before a large PR so we agree on direction first.
- All 59+ tests must pass. New tools need new tests.
- Keep tool functions deterministic. No LLM calls inside tool implementations.
- Match the existing code style. Plain, readable Python over clever Python.

## The AEQ program (whitepaper/, experiments/)

The measurement side is governed by a pre-registration discipline, so contributions
work differently here:

- The canonical metric definition lives in `whitepaper/AEQ_Specification_v1.1.md`.
  PRs that redefine AEQ will be closed. Proposals for spec changes go through an
  issue first and, if accepted, produce a new spec version.
- Experiment results are only accepted with a dated pre-registration committed
  before the runs it governs. That is the whole point of the method.
- Found a defect in the method itself? That is the most valuable contribution
  there is. Open an issue titled `[Lessons]` and it will be evaluated for the
  `AEQ_Lessons_Ledger.md`.

## Terminology (enforced in review)

- The metric is **AEQ** (Agent Efficiency Quotient). Never "AQE."
- Say "AI Agents" or "Agentic Agents." Never "Agentic AI."

## Questions

Open an issue, or reach out via bucketbranch.ai.
