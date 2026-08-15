<div align="center">

# AgentSaaSy

**A working enterprise asset management agent, and the measurement program built to audit it.**

[![Spec](https://img.shields.io/badge/AEQ_spec-v1.1-3FD0C9?style=flat-square)](whitepaper/AEQ_Specification_v1.1.md)
[![Method](https://img.shields.io/badge/method-pre--registered-6BA5E7?style=flat-square)](whitepaper/)
[![Tests](https://img.shields.io/badge/tests-59_passing-E8B54D?style=flat-square)](tests/)
[![Tools](https://img.shields.io/badge/tools-7-8FA3B8?style=flat-square)](#architecture)
[![Paper](https://img.shields.io/badge/paper-The_Cost_of_a_Question-0E1620?style=flat-square)](https://bucketbranch.ai/papers/cost-of-a-question/)

</div>

![Same answer, 4.68x the tokens: three builds of one agent, optimized 345 tokens, moderate bloat 499, severe bloat 1,615](whitepaper/figures/token_spread_468.png)

---

## Two things live here

**1. AgentSaaSy_EAM**, a working enterprise asset management agent: seven Python tools behind
one language model, covering asset query, health analysis, failure prediction, TCO, compliance
tracking, field routing, and Monte Carlo capital planning. 59 tests passing.

**2. The AEQ program**, a pre-registered evaluation method that measures whether an agent
architecture wastes tokens, and whether a cheap model tier holds up on a specific workload.
The agent above is the workload it was measured against.

If you arrived from the article on token waste, part 2 is what you are looking for.

---

## Start here

| If you want | Go to |
|---|---|
| The AEQ definition and method | [`whitepaper/AEQ_Specification_v1.1.md`](whitepaper/AEQ_Specification_v1.1.md) |
| The measured results | [`experiments/aeq_dual_results.txt`](experiments/aeq_dual_results.txt), [`experiments/aeq_experiment_results.txt`](experiments/aeq_experiment_results.txt) |
| The experiment design | [`experiments/STUDY-DESIGN.md`](experiments/STUDY-DESIGN.md) |
| Pre-registrations, dated before the runs they govern | [`whitepaper/`](whitepaper/): `AEQ_Grid_PreRegistration_*`, `AEQ_Grid2Q_PreRegistration_*`, `AEQ_DualProvider_PreRegistration_*` |
| Every defect the method caught in itself | [`whitepaper/AEQ_Lessons_Ledger.md`](whitepaper/AEQ_Lessons_Ledger.md) |
| Run records and dashboards | [`experiments/grid2q/`](experiments/grid2q/) |
| The thesis white paper | [`whitepaper/AGENTIC_SUBSTITUTION_WhitePaper_v3_DRAFT.md`](whitepaper/AGENTIC_SUBSTITUTION_WhitePaper_v3_DRAFT.md) |
| The system architecture reference | [`TECHNICAL-WHITE-PAPER.md`](TECHNICAL-WHITE-PAPER.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Setup and troubleshooting | [`docs/SETUP.md`](docs/SETUP.md) |

---

## AEQ: Agent Efficiency Quotient

```
AEQ  =  Business Value Delivered  /  Tokens Consumed
```

An architecture quality metric, not a cost metric. The numerator is held constant by an
equivalence rubric: two runs are compared only when they deliver the same substantive answer.
When value is equal, the token delta between architectures is architectural waste by
construction.

Read across three independently addressable layers: **prompt** (system-prompt tokens as a
share of total), **orchestration** (calls and retries versus the minimum the query required),
and **output** (verbosity beyond what the answer requires).

### What was measured

Same model, pinned version, temperature 0, same query, three architectures that all returned
the same substantive answer:

| | Optimized | Moderate | Severe |
|---|---:|---:|---:|
| System prompt tokens | 48 | 87 | 475 |
| Total tokens | 345 | 499 | 1,615 |
| Tool calls | 1 | 1 | 3 |
| Prompt overhead | 13.9% | 17.4% | 29.4% |
| **Token ratio** | **1.0x** | **1.45x** | **4.68x** |

Validated live on two vendors, five runs per architecture at temperature 0:

| Vendor | Tokens | Cost | Latency |
|---|---:|---:|---:|
| OpenAI | 5.51x | 4.97x | 2.6x |
| Anthropic | 2.04x | 2.61x | 1.81x |

The pattern holding on **both** vendors is what makes it a property of the architecture rather
than a quirk of one model.

Reliability moved too. Across five identical calls at temperature 0, the severe build agreed
with itself on the critical-asset list **3 of 5 times**. The optimized build agreed **5 of 5**
on both vendors. A padded prompt is not a safety blanket. It is a place to hide the
instruction that mattered.

### Method discipline

- **Pre-registration before execution.** Query classes, rubrics, gates, and priors registered
  before each run; every amendment dated before the run it governs.
- **A calibration gate.** No rubric certifies anything until it has demonstrably failed a
  weaker system. The first rubric passed everything and was discarded for that reason.
- **Cross-family judging.** An Anthropic judge scores OpenAI candidates and vice versa, never
  same-family. Every FAIL verdict is independently re-adjudicated.
- **Deprecation and pricing hygiene.** Models and prices re-verified against official pages
  before publication. A result on a model a reader cannot access or price is a demo, not
  evidence.
- **An append-only lessons ledger.** Eleven entries, each a defect the method caught in itself,
  with detection, fix, and the verifying run. The dates run in that order on purpose.

---

## Quick start

```bash
git clone https://github.com/ibucketbranch/AgentSaasy.git
cd AgentSaasy
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # add your OpenAI API key
python3 -m pytest tests/ -q   # 59 tests
python3 chat_agent.py
```

Requirements: Python 3.10+, an OpenAI API key. Sample data (50 synthetic assets) ships with the
repo; no database or external data needed.

Sample queries: `Show me all critical assets in Building A` · `Which assets are at risk of
failure this quarter?` · `Calculate TCO for all pumps over 5 years` · `Create a 10-year capital
plan with $5M annual budget`

---

## Architecture

![The three-layer system: one certified model, standard orchestration, seven tools, with AEQ Grid certifying offline](whitepaper/figures/system_three_layers.png)

```
Layer 1: Reasoning     -> one chat model, temperature 0, ReAct pattern
Layer 2: Tools         -> 7 Python functions over a DataFrame
Layer 3: Orchestration -> LangChain tool binding
```

| Tool | Purpose |
|------|---------|
| `query_assets` | Filter assets by type, location, health status |
| `analyze_asset_health` | Health trends and risk analysis |
| `predict_failures` | Composite risk scoring with z-score anomaly detection |
| `calculate_tco` | Total cost of ownership analysis |
| `track_compliance` | Inspection and certification tracking |
| `optimize_field_routes` | Field service routing scenario model |
| `plan_capital_strategy` | Monte Carlo capital planning, 1,000 iterations, P10/P50/P90 |

The architecture is deliberately boring. The interesting question was never whether this could
be built, but what it costs to run and whether a cheap model holds up on it.

---

## Scope and limits, stated up front

- The demo portfolio is **50 synthetic assets**, not a live customer dataset.
- `optimize_field_routes` is a **scenario model** against statistical simulation, not a solved
  road network. Drive-time reductions come from industry-standard multipliers applied to a
  baseline.
- The AEQ evidence base is five query classes, one registered query per class, three runs per
  cell at temperature 0. That is an existence proof about this workload, not a population
  statistic. What makes it evidence is the pre-registered bar and the calibration gate.
- AEQ was validated on **single-turn** interactions, where the minimum necessary work is
  knowable in advance. The loop-native adaptation is stated as a proposal awaiting measurement,
  not a finding.

---

## What's here and what isn't

This is the working repository: the agent, every experiment, the white paper, and the claim
ledger that governs what any of it is allowed to assert.

Not published anywhere: the rubric authoring used in client engagements, and the Agent_AEQ
operator design. If you want AEQ run against your own workload, or want the harness rather than
the method, reach out on [LinkedIn](https://www.linkedin.com/in/m-valderrama/) or via
[bucketbranch.ai](https://bucketbranch.ai).

---

## Citing this work

AEQ (Agent Efficiency Quotient) is a framework by Michael Valderrama. Cite the public
repository, not this one:

> Valderrama, M. (2026). *AEQ: Agent Efficiency Quotient, specification, pre-registration
> series, and run reports.* https://github.com/ibucketbranch/AEQ

- Plain-language writeup: [Same Model, Same Question, 4.68x the Tokens](https://medium.com/@michael_valderrama/same-model-same-question-4-68x-the-tokens-455725b06add)
- Full methodology and white paper: [The Cost of a Question](https://bucketbranch.ai/papers/cost-of-a-question/)
- System architecture reference (v2.1.0): [Agentic Architecture for Enterprise Asset Management](https://bucketbranch.ai/papers/agentic-architecture-enterprise-eam/)

---

<div align="center">

### Part of one body of work

| Repository | What it holds | |
|---|---|---|
| [**AEQ**](https://github.com/ibucketbranch/AEQ) | The specification, pre-registrations, and every run record | public |
| **AgentSaaSy** | The agent under test, the experiments, and the white paper | you are here |
| **quantized-agent-grid** | The open-weight findings, packaged on their own | private |

**Michael Valderrama** · AI Agent Architect · Independent R&D © 2026

[bucketbranch.ai](https://bucketbranch.ai) · [Medium](https://medium.com/@michael_valderrama) · [LinkedIn](https://www.linkedin.com/in/m-valderrama/) · [X](https://x.com/mikevalderrama)

</div>
