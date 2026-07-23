# AEQ 3×3×3 GRID — CLAUDE CODE EXECUTION HANDOFF
*Paste everything below this line into Claude Code in Cursor.*

---

## CONTEXT

You are executing a pre-registered experiment. Two files are already in this repo (or I am adding them now):

- `AEQ_Grid_PreRegistration_v1.md` — the locked experimental protocol, timestamped 2026-07-22T08:49:29Z UTC
- `aeq_grid_experiment.py` — the runnable grid script

The experiment tests whether cheaper model tiers (mid, nano) deliver rubric-equivalent answers to a frontier tier when given identical evidence. 3 query classes × 3 model tiers × 3 runs, judged by a cross-family validator (Anthropic Claude judging OpenAI outputs). The script auto-evaluates a GREEN/YELLOW/RED gate verdict against locked thresholds.

Your job is to EXECUTE it, not redesign it.

## NON-NEGOTIABLE RULES

1. **DO NOT modify** the gates, rubrics, query texts, evidence block, or anything in `AEQ_Grid_PreRegistration_v1.md`. The pre-registration is locked. If something in the protocol seems wrong, STOP and report it to me — do not fix it yourself.
2. **DO NOT modify** any existing files in this repo. The only files you may edit are the two experiment files listed above, and only in the ways permitted below.
3. The ONLY permitted edits to `aeq_grid_experiment.py` are inside the CONFIG block:
   - `TIERS` model-name strings (if pre-flight fails — see Step 3)
   - `PRICING` values (only to correct them against official pricing pages)
   - `PRICING_VERIFIED` flag (only after actually verifying)
4. **Never fabricate, estimate, or "fill in" any result.** Every number in the final report must come from the script's actual output. If a run fails, it stays failed in the log.
5. API keys are in `.env` at the project root (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). Do not print, log, or echo them anywhere.

## EXECUTION STEPS

### Step 1 — Environment
```
pip install tiktoken requests python-dotenv
```
Confirm both API keys are present in `.env` (check existence only — do not display values).

### Step 2 — Verify pricing (BEFORE running)
Open `aeq_grid_experiment.py` CONFIG block. The `PRICING` dict contains PLACEHOLDER values from third-party sources. Verify each model's current per-1M-token input/output pricing against the official pages:
- OpenAI: https://platform.openai.com/docs/pricing
- Anthropic: https://www.anthropic.com/pricing

Correct any values that differ, then set `PRICING_VERIFIED = True`. Record what you changed (old → new) for the final report. If you cannot access the pricing pages, leave `PRICING_VERIFIED = False`, note it, and proceed — cost figures will be flagged as unverified.

### Step 3 — Dry run
```
python aeq_grid_experiment.py --dry-run
```
Confirm the cost estimate is under $1. Report the estimate.

### Step 4 — Full grid
```
python aeq_grid_experiment.py
```
The script pre-flights the configured model names against `/v1/models`. If it aborts because a `TIERS` name is unavailable on this account, choose the closest equivalent from the candidates it prints, keeping the tier ordering intact (T1 = most capable/expensive, T2 = mid, T3 = cheapest). Preferred fallback set: `gpt-4o` / `gpt-4o-mini` / `gpt-4.1-nano`. Record any substitution (configured → actual) for the final report, then re-run.

Expected wall time: 10–20 minutes. If individual runs error, let the script's retry logic handle it; do not intervene mid-run.

### Step 5 — Integrity checks on the output
Open `experiments/grid/aeq_grid_report.md` and verify:
- Frontier reference self-pass is ≥ 8/9. If it is NOT, STOP — per the pre-registration, the rubric is defective. Report the failed criteria verbatim and take no further action. Do not "fix" the rubric.
- Every cell in the pass-rate matrix has 3 runs (or failures are explicitly logged).
- The gate verdict (GREEN/YELLOW/RED) is present.

### Step 6 — Report back to me
Produce a summary containing, in this order:
1. Gate verdict: GREEN / YELLOW / RED
2. Aggregate SUT pass rate vs. the declared prior (75–80%)
3. The full pass-rate matrix (query class × tier)
4. Cost deltas (T1/T2 and T1/T3) and verification overhead per query
5. Any model substitutions made (configured → actual)
6. Any pricing corrections made (old → new) and the `PRICING_VERIFIED` status
7. Every failed cell with its failed criteria, verbatim from the report
8. Paths to `aeq_grid_report.md` and `aeq_grid_raw.json`

Do not editorialize the result. Do not soften a RED. Do not inflate a YELLOW. The verdict is the verdict.

## WHAT THIS IS FOR

This experiment is the single cheapest de-risking step for a product concept (AEQ Verify) whose load-bearing assumption — cheap tiers passing pre-registered equivalence rubrics — has never been measured. The result gets scored against a prior declared in writing before the run. A RED result is as publishable as a GREEN one. The numbers must be REAL — measured from actual API calls, never estimated, never fabricated.

---
Michael Valderrama | AI Agent Architect | Independent R&D © 2026
