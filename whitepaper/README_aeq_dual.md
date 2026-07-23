# AEQ Dual-Provider Experiment — Run Guide

`aeq_experiment_dual.py` — vendor-neutral version of your AEQ rig. Runs all three
architectures (optimized / moderate_bloat / severe_bloat) against **OpenAI and
Anthropic**, capturing measured tokens, cost, **latency**, and **cross-run reliability**.

## Why two providers
If the efficiency pattern (optimized << moderate << severe) holds on *both* vendors,
the waste is **architectural, not a model quirk**. That kills the "you just picked a
bad config on one model" rebuttal — the strongest framing for a GTC stage.

## Setup (one time)
```bash
pip install tiktoken langchain-openai langchain-anthropic langchain-core python-dotenv
```
Create a `.env` file in this folder. You set these; they stay on your machine and never
pass through Claude:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```
A provider with no key is **skipped** (not an error), so you can run one vendor at a time.

## Run
```bash
# No keys needed — exact input tokens, estimated outputs (reproduces your published sim)
python aeq_experiment_dual.py --mode simulate

# Real measurement, both vendors, 5 runs each per architecture
python aeq_experiment_dual.py --mode validate --providers openai anthropic --runs 5

# Both phases
python aeq_experiment_dual.py --mode both --providers openai anthropic --runs 5
```
Results write to `experiments/aeq_dual_results.txt`.

## What you get that the old script didn't
- **Measured latency** per architecture — the number that does *not* deflate as tokens get cheaper. This is the missing proof at the center of the AEQ thesis.
- **Reliability score** — across N runs, how many agree on the same critical-asset set. A bloated prompt that drifts is your reliability argument, made visible.
- **All three architectures** in the real-API path (the old script only ran two live).
- **Cross-vendor verdict** — a one-line "pattern holds on all vendors: True/False".

## Integrity rules baked in
- Every number is tagged `[MEASURED]` or `[EST]`. Inputs (tiktoken) are exact; simulation outputs are estimates, disclosed. Real-API numbers are all measured.
- Pricing constants are at the top of the script (`PRICES`). **Verify before publishing:**
  OpenAI gpt-4o-mini `$0.15 / $0.60` per M; Anthropic claude-haiku-4.5 `$1.00 / $5.00` per M (checked June 2026).
- Your three system prompts are copied verbatim — they're the independent variable, do not edit them.

## Note on the headline number
Your published 4.68x tokens / 5.04x cost comes from the *severe_bloat* case, which
forces 3 tool calls — a deliberately extreme strawman. The realistic case (moderate_bloat,
which nothing forces) is ~1.45x / 1.79x. Lead with the honest realistic delta plus the
measured latency/reliability story; keep severe_bloat labeled as the extreme bound.
