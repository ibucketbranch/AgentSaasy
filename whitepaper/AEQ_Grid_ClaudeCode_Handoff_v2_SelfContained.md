# AEQ 3×3×3 GRID — SELF-CONTAINED CLAUDE CODE HANDOFF v2
*Paste everything below this line into Claude Code in Cursor. It creates all files itself and executes the full experiment. Your only prerequisite: `.env` at the project root with `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`.*

---

## CONTEXT

You are executing a pre-registered experiment testing whether cheaper model tiers (mid, nano) deliver rubric-equivalent answers to a frontier tier when given identical evidence. 3 query classes × 3 model tiers × 3 runs, cross-family judged (Anthropic Claude judging OpenAI outputs), with an automatic GREEN/YELLOW/RED gate verdict against locked thresholds.

Both required files are embedded verbatim in this prompt. You will create them, then execute. Your job is to EXECUTE the protocol, not redesign it.

## NON-NEGOTIABLE RULES

1. Create the two embedded files EXACTLY as given — byte-for-byte, no reformatting, no "improvements," no added comments.
2. **DO NOT modify** the gates, rubrics, query texts, or evidence block anywhere. The pre-registration is locked (timestamped 2026-07-22T08:49:29Z UTC). If something seems wrong, STOP and report to me — do not fix it yourself.
3. **DO NOT modify** any pre-existing files in this repo.
4. After creation, the ONLY permitted edits to `aeq_grid_experiment.py` are inside the CONFIG block:
   - `TIERS` model-name strings (only if pre-flight fails — see Step 5)
   - `PRICING` values (only to correct them against official pricing pages)
   - `PRICING_VERIFIED` flag (only after actually verifying)
5. **Never fabricate, estimate, or "fill in" any result.** Every number in the final report must come from the script's actual output. Failed runs stay failed in the log.
6. API keys live in `.env`. Verify they EXIST — never print, log, or echo their values.

## EXECUTION STEPS

### Step 1 — Create the experiment directory and files
Create `experiments/grid/` if it does not exist. Then create the two files below at the repo root (or the project's standard experiments location if one exists — your choice, but record where).

**FILE 1 of 2 — create as `AEQ_Grid_PreRegistration_v1.md`:**

<<<FILE_START:AEQ_Grid_PreRegistration_v1.md>>>
# AEQ 3×3×3 GRID EXPERIMENT — PRE-REGISTRATION v1.0

**Pre-registered:** 2026-07-22T08:49:29Z (UTC)
**Author:** Michael Valderrama | AI Agent Architect | Independent R&D © 2026
**Status:** REGISTERED — NOT YET RUN. This document is written and timestamped BEFORE the experiment executes. Gates below may not be modified after the run begins.

---

## 1. The Question

Does a cheaper model tier deliver a rubric-equivalent answer when given the same query and the same evidence as a frontier tier — and at what pass rate, per query class?

This is the load-bearing assumption of the AEQ Verify concept. The published routing literature suggests high pass rates on benchmark traffic (RouteLLM: 95% of GPT-4 quality with 14–26% strong-model calls, ICLR 2025; FrugalGPT: up to 98% cost reduction at matched performance, Chen et al. 2023, arXiv:2305.05176). None of that literature uses pre-registered equivalence rubrics or cross-family adjudication on enterprise-agent-style queries. This experiment does.

## 2. Stated Prior (declared before run)

**Founder prior: 75–80% aggregate rubric pass rate** for the mid tier, lower for nano. Declared here so the result can be scored against the prediction, not fitted to it.

## 3. Design — 3 × 3 × 3

| Dimension | Levels |
|---|---|
| **Query class** | Q1 Simple retrieval · Q2 Analytical multi-signal · Q3 Judgment/synthesis |
| **Model tier** | T1 Frontier (reference) · T2 Mid · T3 Nano — pinned versions recorded at run time |
| **Runs per cell** | N = 3 (temperature 0; latency and minor variance still averaged) |

**Replay semantics (deliberate design choice):** All tiers receive identical evidence — the same deterministic tool outputs injected as context. This isolates the tier-equivalence variable and mirrors the AEQ Verify shadow-lane mechanism (replay same query + same retrieved data on a cheaper configuration).

**Declared limitation:** This design does NOT test tool-selection ability across tiers. Whether a nano-tier model *chooses* the right tools is a separate experiment (Grid-2, future). Do not generalize Grid-1 results to full autonomous orchestration.

**Adjudication:** Cross-family validator (Anthropic Claude judging OpenAI system-under-test outputs). No self-grading — the same independence rule AEQ v1.0 imposes on customers is imposed here. Judge renders a structured verdict against the rubric plus the frontier reference answer. Judge model version pinned at run time.

**Judge cost is recorded separately** as "verification overhead per verified query" — this is the COGS of certification and a product-relevant number in its own right.

## 4. Equivalence Rubrics (pre-registered per query class)

**Q1 — Simple retrieval.** "What are the critical assets in the portfolio?"
PASS requires: (a) states the critical asset count = 12; (b) cites at least 3 of the 5 named critical asset IDs present in the evidence (PUMP-003, HVAC-007, COMP-002, BOIL-001, PUMP-009); (c) contains no asset IDs or counts that contradict the evidence.

**Q2 — Analytical multi-signal.** "Which assets should be prioritized for maintenance in the next 30 days, and why?"
PASS requires: (a) top priority is PUMP-003 (highest risk score 91.2 in evidence); (b) at least 2 of the remaining top-5 risk assets named (HVAC-007, BOIL-001, COMP-002, GEN-004); (c) justification references at least one quantitative signal from the evidence (risk score, health score, or overdue days); (d) no fabricated numbers.

**Q3 — Judgment/synthesis.** "Draft a one-paragraph recommendation for leadership on the state of the asset portfolio and the single most important action to take."
PASS requires: (a) portfolio characterized as declining or at-risk (consistent with 24% critical, −3.2 pt 90-day trend in evidence); (b) recommended action addresses the highest-risk asset(s) or the overdue-maintenance backlog; (c) no fabricated statistics; (d) length ≤ 250 words (leadership-appropriate).

A response FAILS if any required element is absent or contradicted. The judge must return structured JSON: `{pass, failed_criteria, notes}`.

## 5. Go / No-Go Gates (LOCKED)

| Gate | Condition | Consequence for AEQ Verify |
|---|---|---|
| **GREEN** | Aggregate pass rate (T2+T3 vs rubric) ≥ 70% AND effective cost delta ≥ 5x AND Q3 (hardest class) pass ≥ 50% | Full pitch stands. "Certified verified savings" story proceeds to design-partner outreach. |
| **YELLOW** | Aggregate 40–70%, or GREEN numbers but Q3 < 50% | Company exists but repositions: "auditable routing with a billing-grade ledger," differentiation shifts to certification, not savings magnitude. |
| **RED** | Aggregate < 40%, OR passes concentrated only in Q1 | Savings pool does not support gainshare at target ICP. Pivot AEQ IP toward consulting / benchmark tooling. |

Secondary integrity checks (reported, not gated): frontier reference must itself pass its own rubric ≥ 8/9 runs (else rubric is defective — fix rubric, re-register as v1.1, re-run); any judge JSON parse failure is logged and re-adjudicated once, never silently dropped.

## 6. Measurement & Integrity Rules (inherited from AEQ Spec v1.0 §6)

1. Pin everything: model versions, temperature 0, pricing at run date (verify at platform.openai.com and anthropic.com pricing pages before publication — defaults in the script are placeholders from third-party sources and MUST be re-verified).
2. Input tokens measured exactly (tiktoken); output tokens from API usage fields. All numbers in publication labeled measured vs. estimated.
3. N=3 per cell; failed runs logged, not dropped.
4. Full answer text captured for every cell for qualitative audit.
5. Results published regardless of outcome. A RED result is publishable — "we pre-registered, we ran it, here is what the rubric actually says" is itself a credibility asset.

## 7. Run Instructions

```
# In the AgentSaasy_NGAI repo (or standalone dir), with .env containing:
#   OPENAI_API_KEY=...
#   ANTHROPIC_API_KEY=...
pip install tiktoken requests python-dotenv
python aeq_grid_experiment.py                # full grid
python aeq_grid_experiment.py --dry-run      # token/cost estimate only, no API calls
```

Estimated total API cost: **under $5** (27 execution calls on small prompts + ≤ 60 judge calls). Estimated wall time: 10–20 minutes.

## 8. What Gets Reported

Per-cell: pass/fail, tokens, cost, latency, full answer. Aggregate: pass-rate matrix (class × tier), cost-delta matrix, gate verdict (GREEN/YELLOW/RED) computed automatically against §5, verification overhead per query, and a comparison of the measured pass rate against the §2 declared prior.

---
*Terminology compliance: this document uses "AI agent(s)" exclusively.*

<<<FILE_END:AEQ_Grid_PreRegistration_v1.md>>>

**FILE 2 of 2 — create as `aeq_grid_experiment.py`:**

<<<FILE_START:aeq_grid_experiment.py>>>
"""
AEQ 3x3x3 Grid Experiment -- Tier Equivalence Under Pre-Registered Rubrics
==========================================================================
Author:  Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026
Version: 1.0.0
Pre-registration: AEQ_Grid_PreRegistration_v1.md (2026-07-22T08:49:29Z UTC)

THE QUESTION
  Does a cheaper model tier deliver a rubric-equivalent answer when given
  the same query and the same evidence as a frontier tier?

DESIGN
  3 query classes x 3 model tiers x 3 runs = 27 execution cells.
  Replay semantics: identical evidence (deterministic tool outputs) injected
  as context for every tier. Cross-family judge (Anthropic Claude) adjudicates
  each candidate against the pre-registered rubric + frontier reference.
  Gates (LOCKED in pre-registration -- do not edit after run begins):
    GREEN : aggregate pass >= 70% AND cost delta >= 5x AND Q3 pass >= 50%
    YELLOW: aggregate 40-70%, or GREEN numbers with Q3 < 50%
    RED   : aggregate < 40%, or passes only in Q1

USAGE
  pip install tiktoken requests python-dotenv
  python aeq_grid_experiment.py --dry-run     # cost/token estimate, no API calls
  python aeq_grid_experiment.py               # full grid
  python aeq_grid_experiment.py --runs 3      # runs per cell (default 3)

Requires .env (or exported env vars):
  OPENAI_API_KEY=...        # system under test
  ANTHROPIC_API_KEY=...     # cross-family judge
"""

import os
import sys
import json
import time
import argparse
import statistics
from datetime import datetime, timezone
from pathlib import Path

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # env vars may be exported directly

try:
    import tiktoken
except ImportError:
    print("[ERROR] pip install tiktoken")
    sys.exit(1)

# =============================================================================
# CONFIG -- SET THESE BEFORE RUNNING
# =============================================================================
# Model tiers (OpenAI, system under test). The script pre-flights these names
# against /v1/models and aborts with suggestions if a name is unavailable.
# Fallback set if GPT-5.x names differ on your account:
#   T1 "gpt-4o"  T2 "gpt-4o-mini"  T3 "gpt-4.1-nano"
TIERS = {
    "T1_frontier": "gpt-5.2",
    "T2_mid":      "gpt-5-mini",
    "T3_nano":     "gpt-5-nano",
}

# Cross-family judge (Anthropic). Pinned version per AEQ independence rule.
JUDGE_MODEL = "claude-haiku-4-5-20251001"

# Pricing per 1M tokens (input, output) in USD.
# !! PLACEHOLDERS from third-party sources (Jan 2026). VERIFY at
# !! platform.openai.com/docs/pricing and anthropic.com/pricing BEFORE
# !! publication. The report flags these as UNVERIFIED until you edit
# !! PRICING_VERIFIED = True.
PRICING = {
    "gpt-5.2":      (1.75, 14.00),
    "gpt-5-mini":   (0.25,  2.00),
    "gpt-5-nano":   (0.05,  0.40),
    "gpt-4o":       (2.50, 10.00),
    "gpt-4o-mini":  (0.15,  0.60),
    "gpt-4.1-nano": (0.10,  0.40),
    JUDGE_MODEL:    (1.00,  5.00),
}
PRICING_VERIFIED = False  # flip to True after checking official pricing pages

MAX_OUTPUT_TOKENS = 600
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODELS_URL = "https://api.openai.com/v1/models"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

# =============================================================================
# EVIDENCE -- deterministic tool outputs (identical for every tier; replay
# semantics per pre-registration section 3). Reused from AgentSaasy_NGAI stubs.
# =============================================================================
EVIDENCE = """TOOL OUTPUT -- query_assets('critical'):
Found 12 asset(s) matching 'critical'.
Total acquisition value: $485,000 | Average health score: 41.3 | Critical assets: 12
Top results:
- PUMP-003 | Pump | Building A | Health: 37 | Critical | Last maint: 2025-06-12
- HVAC-007 | HVAC | Zone North | Health: 39 | Critical | Last maint: 2025-04-18
- COMP-002 | Compressor | Building B | Health: 42 | Critical | Last maint: 2025-07-01
- BOIL-001 | Boiler | Zone South | Health: 43 | Critical | Last maint: 2025-05-20
- PUMP-009 | Pump | Building C | Health: 44 | Critical | Last maint: 2025-08-10
[7 more assets not shown]

TOOL OUTPUT -- analyze_asset_health():
Total assets analyzed: 50 | Mean health: 67.5 (sigma 18.2) | Min 37 | Max 93
Critical (h<50): 12 (24.0%) | Warning (50<=h<75): 18 (36.0%) | Healthy (h>=75): 20 (40.0%)
Maintenance overdue (>180 days): 8 assets -- PUMP-003, HVAC-007, BOIL-001, COMP-002,
GEN-004, CONV-006, PUMP-011, HVAC-015
TREND: Portfolio health declined 3.2 points over 90-day period.

TOOL OUTPUT -- predict_failures():
60-90 day horizon, alert threshold risk > 70. HIGH RISK (top 5):
1. PUMP-003 | Risk 91.2 | Health 37 | Overdue 247 days -> Immediate inspection + bearing replacement
2. HVAC-007 | Risk 84.6 | Health 39 | Overdue 318 days -> Schedule within 2 weeks
3. BOIL-001 | Risk 79.3 | Health 43 | Overdue 258 days -> Schedule within 30 days
4. COMP-002 | Risk 73.1 | Health 42 | Overdue 216 days -> Enhanced monitoring + schedule
5. GEN-004  | Risk 71.8 | Health 46 | Overdue 189 days -> Schedule within 45 days"""

SYSTEM_PROMPT = (
    "You are an enterprise asset management analyst. Answer using ONLY the tool "
    "output data provided. Be accurate and concise. Do not invent asset IDs or numbers."
)

# =============================================================================
# QUERY CLASSES + PRE-REGISTERED RUBRICS (verbatim from pre-registration sec 4)
# =============================================================================
QUERIES = {
    "Q1_retrieval": {
        "query": "What are the critical assets in the portfolio?",
        "rubric": (
            "PASS requires ALL of: (a) states the critical asset count = 12; "
            "(b) cites at least 3 of these asset IDs: PUMP-003, HVAC-007, COMP-002, "
            "BOIL-001, PUMP-009; (c) contains no asset IDs or counts contradicting "
            "the evidence."
        ),
    },
    "Q2_analytical": {
        "query": "Which assets should be prioritized for maintenance in the next 30 days, and why?",
        "rubric": (
            "PASS requires ALL of: (a) top priority is PUMP-003; (b) at least 2 of "
            "HVAC-007, BOIL-001, COMP-002, GEN-004 are also named; (c) justification "
            "references at least one quantitative signal from the evidence (risk score, "
            "health score, or overdue days); (d) no fabricated numbers."
        ),
    },
    "Q3_synthesis": {
        "query": ("Draft a one-paragraph recommendation for leadership on the state of "
                  "the asset portfolio and the single most important action to take."),
        "rubric": (
            "PASS requires ALL of: (a) portfolio characterized as declining or at-risk, "
            "consistent with 24% critical and a 3.2-point 90-day decline; (b) the "
            "recommended action addresses the highest-risk asset(s) or the overdue-"
            "maintenance backlog; (c) no fabricated statistics; (d) response is at most "
            "250 words."
        ),
    },
}

# Gates -- LOCKED per pre-registration section 5
GATE_GREEN_AGG = 0.70
GATE_GREEN_Q3 = 0.50
GATE_GREEN_COSTX = 5.0
GATE_RED_AGG = 0.40

ENC = tiktoken.get_encoding("o200k_base")


def count_tokens(text: str) -> int:
    return len(ENC.encode(text))


def price(model: str, tokens_in: int, tokens_out: int) -> float:
    pin, pout = PRICING.get(model, (0.0, 0.0))
    return tokens_in / 1e6 * pin + tokens_out / 1e6 * pout


# =============================================================================
# API CALLS
# =============================================================================
def openai_headers():
    return {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json"}


def preflight_models():
    """Verify configured tier names exist on this account before burning the grid."""
    r = requests.get(OPENAI_MODELS_URL, headers=openai_headers(), timeout=30)
    r.raise_for_status()
    available = {m["id"] for m in r.json().get("data", [])}
    missing = [(k, v) for k, v in TIERS.items() if v not in available]
    if missing:
        print("[ABORT] These configured models are not available on your account:")
        for k, v in missing:
            print(f"  {k}: '{v}'")
        near = sorted(a for a in available if any(s in a for s in ("gpt-5", "gpt-4o", "4.1")))[:25]
        print("  Available candidates on your account:")
        for a in near:
            print(f"    {a}")
        print("  Edit TIERS in the CONFIG block and re-run.")
        sys.exit(1)
    print(f"[OK] Pre-flight passed: {', '.join(TIERS.values())}")


def call_openai(model: str, system: str, user: str):
    """Chat completion with graceful retry when a param is unsupported
    (e.g., some reasoning-tier models reject temperature/max_tokens)."""
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 0,
        "max_completion_tokens": MAX_OUTPUT_TOKENS,
    }
    for attempt in range(4):
        t0 = time.time()
        r = requests.post(OPENAI_URL, headers=openai_headers(), json=body, timeout=180)
        latency = time.time() - t0
        if r.status_code == 200:
            data = r.json()
            usage = data.get("usage", {})
            return {
                "answer": data["choices"][0]["message"]["content"] or "",
                "tokens_in": usage.get("prompt_tokens", 0),
                "tokens_out": usage.get("completion_tokens", 0),
                "latency_s": round(latency, 2),
                "error": None,
            }
        # Strip unsupported params and retry
        err = r.text.lower()
        changed = False
        for p in ("temperature", "max_completion_tokens", "max_tokens"):
            if p in body and p in err and ("unsupported" in err or "not supported" in err
                                           or "unknown" in err or "invalid" in err):
                body.pop(p)
                changed = True
        if "max_completion_tokens" in err and "max_tokens" not in body and not changed:
            body["max_tokens"] = body.pop("max_completion_tokens", MAX_OUTPUT_TOKENS)
            changed = True
        if not changed:
            if r.status_code in (429, 500, 502, 503):
                time.sleep(5 * (attempt + 1))
                continue
            return {"answer": "", "tokens_in": 0, "tokens_out": 0,
                    "latency_s": 0, "error": f"HTTP {r.status_code}: {r.text[:300]}"}
    return {"answer": "", "tokens_in": 0, "tokens_out": 0,
            "latency_s": 0, "error": "retries exhausted"}


def call_judge(rubric: str, query: str, reference: str, candidate: str):
    """Cross-family adjudication. Returns dict {pass, failed_criteria, notes} + usage."""
    prompt = f"""You are an independent equivalence adjudicator for AI agent outputs.
Judge the CANDIDATE answer against the pre-registered RUBRIC. The REFERENCE answer
from a frontier model is provided as context only -- the RUBRIC is the sole standard.
Judge strictly: every rubric element must be satisfied.

QUERY: {query}

EVIDENCE the models were given:
{EVIDENCE}

RUBRIC:
{rubric}

REFERENCE ANSWER (frontier tier, context only):
{reference}

CANDIDATE ANSWER (under test):
{candidate}

Respond with ONLY a JSON object, no markdown fences, no preamble:
{{"pass": true/false, "failed_criteria": ["..."], "notes": "one sentence"}}"""
    body = {
        "model": JUDGE_MODEL,
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
               "anthropic-version": ANTHROPIC_VERSION,
               "Content-Type": "application/json"}
    for attempt in range(3):
        r = requests.post(ANTHROPIC_URL, headers=headers, json=body, timeout=120)
        if r.status_code == 200:
            data = r.json()
            text = "".join(b.get("text", "") for b in data.get("content", []))
            usage = data.get("usage", {})
            cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            try:
                verdict = json.loads(cleaned)
            except json.JSONDecodeError:
                if attempt < 2:
                    continue  # re-adjudicate once per integrity rules
                verdict = {"pass": False, "failed_criteria": ["judge_parse_failure"],
                           "notes": text[:200]}
            verdict["judge_tokens_in"] = usage.get("input_tokens", 0)
            verdict["judge_tokens_out"] = usage.get("output_tokens", 0)
            return verdict
        if r.status_code in (429, 500, 529):
            time.sleep(5 * (attempt + 1))
            continue
        return {"pass": False, "failed_criteria": [f"judge_http_{r.status_code}"],
                "notes": r.text[:200], "judge_tokens_in": 0, "judge_tokens_out": 0}
    return {"pass": False, "failed_criteria": ["judge_retries_exhausted"],
            "notes": "", "judge_tokens_in": 0, "judge_tokens_out": 0}


# =============================================================================
# EXPERIMENT
# =============================================================================
def build_user_message(query: str) -> str:
    return f"{EVIDENCE}\n\nQUESTION: {query}"


def dry_run(runs: int):
    sys_toks = count_tokens(SYSTEM_PROMPT)
    total_cost = 0.0
    print(f"\nDRY RUN -- no API calls. System prompt: {sys_toks} tokens.")
    for qk, q in QUERIES.items():
        in_toks = sys_toks + count_tokens(build_user_message(q["query"]))
        for tk, model in TIERS.items():
            est = price(model, in_toks, 350) * runs
            total_cost += est
            print(f"  {qk} x {tk} ({model}): ~{in_toks} in-tokens/run, est ${est:.4f} for {runs} runs")
    judge_est = 9 * runs * price(JUDGE_MODEL, 1600, 150)  # every cell judged
    print(f"  Judge ({JUDGE_MODEL}): est ${judge_est:.4f}")
    print(f"  ESTIMATED TOTAL: ${total_cost + judge_est:.2f}")


def run_grid(runs: int, outdir: Path):
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if not os.environ.get(key):
            print(f"[ERROR] {key} not set (check .env)")
            sys.exit(1)
    preflight_models()

    results = []
    references = {}

    # Pass 1 -- frontier reference answers (also judged, per integrity rule)
    frontier = TIERS["T1_frontier"]
    for qk, q in QUERIES.items():
        print(f"\n[REF] {qk} on {frontier} ...")
        user_msg = build_user_message(q["query"])
        cell_runs = []
        for i in range(runs):
            res = call_openai(frontier, SYSTEM_PROMPT, user_msg)
            if res["error"]:
                print(f"  run {i+1}: ERROR {res['error']}")
            else:
                print(f"  run {i+1}: {res['tokens_out']} out-tokens, {res['latency_s']}s")
            cell_runs.append(res)
        ok = [r for r in cell_runs if not r["error"] and r["answer"]]
        references[qk] = ok[0]["answer"] if ok else "(reference unavailable)"
        for i, res in enumerate(cell_runs):
            verdict = (call_judge(q["rubric"], q["query"], references[qk], res["answer"])
                       if res["answer"] else
                       {"pass": False, "failed_criteria": ["no_answer"], "notes": "",
                        "judge_tokens_in": 0, "judge_tokens_out": 0})
            results.append(make_row(qk, "T1_frontier", frontier, i, res, verdict))

    # Pass 2 -- cheap tiers judged against rubric + reference
    for tk in ("T2_mid", "T3_nano"):
        model = TIERS[tk]
        for qk, q in QUERIES.items():
            print(f"\n[SUT] {qk} on {model} ...")
            user_msg = build_user_message(q["query"])
            for i in range(runs):
                res = call_openai(model, SYSTEM_PROMPT, user_msg)
                verdict = (call_judge(q["rubric"], q["query"], references[qk], res["answer"])
                           if res["answer"] else
                           {"pass": False, "failed_criteria": ["no_answer"], "notes": "",
                            "judge_tokens_in": 0, "judge_tokens_out": 0})
                mark = "PASS" if verdict.get("pass") else "FAIL"
                print(f"  run {i+1}: {mark} ({res['tokens_out']} out-tokens, {res['latency_s']}s)")
                results.append(make_row(qk, tk, model, i, res, verdict))

    write_outputs(results, outdir, runs)


def make_row(qk, tk, model, run_i, res, verdict):
    cost = price(model, res["tokens_in"], res["tokens_out"])
    jcost = price(JUDGE_MODEL, verdict.get("judge_tokens_in", 0), verdict.get("judge_tokens_out", 0))
    return {
        "query_class": qk, "tier": tk, "model": model, "run": run_i + 1,
        "pass": bool(verdict.get("pass")),
        "failed_criteria": verdict.get("failed_criteria", []),
        "judge_notes": verdict.get("notes", ""),
        "tokens_in": res["tokens_in"], "tokens_out": res["tokens_out"],
        "latency_s": res["latency_s"], "cost_usd": round(cost, 6),
        "judge_cost_usd": round(jcost, 6),
        "error": res["error"], "answer": res["answer"],
    }


# =============================================================================
# REPORTING + GATE EVALUATION
# =============================================================================
def write_outputs(results, outdir: Path, runs: int):
    outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (outdir / "aeq_grid_raw.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    sut = [r for r in results if r["tier"] in ("T2_mid", "T3_nano") and not r["error"]]
    ref = [r for r in results if r["tier"] == "T1_frontier" and not r["error"]]

    agg_pass = sum(r["pass"] for r in sut) / len(sut) if sut else 0.0
    q3 = [r for r in sut if r["query_class"] == "Q3_synthesis"]
    q3_pass = sum(r["pass"] for r in q3) / len(q3) if q3 else 0.0
    q1_only = all(not r["pass"] for r in sut if r["query_class"] != "Q1_retrieval") if sut else True
    ref_pass = sum(r["pass"] for r in ref) / len(ref) if ref else 0.0

    def mean_cost(tier):
        vals = [r["cost_usd"] for r in results if r["tier"] == tier and not r["error"]]
        return statistics.mean(vals) if vals else 0.0

    c1, c2, c3 = mean_cost("T1_frontier"), mean_cost("T2_mid"), mean_cost("T3_nano")
    delta_mid = c1 / c2 if c2 else 0.0
    delta_nano = c1 / c3 if c3 else 0.0
    best_delta = max(delta_mid, delta_nano)

    if agg_pass >= GATE_GREEN_AGG and best_delta >= GATE_GREEN_COSTX and q3_pass >= GATE_GREEN_Q3:
        gate = "GREEN"
    elif agg_pass < GATE_RED_AGG or q1_only:
        gate = "RED"
    else:
        gate = "YELLOW"

    verification_overhead = statistics.mean([r["judge_cost_usd"] for r in sut]) if sut else 0.0

    lines = [
        "# AEQ 3x3x3 GRID -- RESULTS",
        f"Run completed: {ts} | Runs per cell: {runs}",
        f"Models: {TIERS} | Judge: {JUDGE_MODEL}",
        f"Pricing verified against official pages: {PRICING_VERIFIED}"
        + ("" if PRICING_VERIFIED else "  << VERIFY BEFORE PUBLICATION"),
        "",
        "## PASS-RATE MATRIX (query class x tier)",
    ]
    for qk in QUERIES:
        row = [qk.ljust(14)]
        for tk in TIERS:
            cell = [r for r in results if r["query_class"] == qk and r["tier"] == tk and not r["error"]]
            p = sum(r["pass"] for r in cell)
            row.append(f"{tk}: {p}/{len(cell)}")
        lines.append("  " + " | ".join(row))

    lines += [
        "",
        "## AGGREGATES",
        f"  Frontier reference self-pass : {ref_pass:.0%}  (integrity check; must be >= ~89%)",
        f"  Aggregate SUT pass (T2+T3)   : {agg_pass:.0%}   (declared prior: 75-80%)",
        f"  Q3 (hardest) SUT pass        : {q3_pass:.0%}",
        f"  Mean cost/query  T1: ${c1:.6f}  T2: ${c2:.6f}  T3: ${c3:.6f}",
        f"  Cost delta  T1/T2: {delta_mid:.1f}x   T1/T3: {delta_nano:.1f}x",
        f"  Verification overhead per verified query (judge COGS): ${verification_overhead:.6f}",
        "",
        "## GATE VERDICT (locked thresholds -- pre-registration section 5)",
        f"  >>> {gate} <<<",
        "  GREEN : agg >= 70% AND cost delta >= 5x AND Q3 >= 50%",
        "  YELLOW: agg 40-70%, or GREEN numbers with Q3 < 50%",
        "  RED   : agg < 40%, or passes confined to Q1",
        "",
        "## FAILED CELLS",
    ]
    fails = [r for r in sut if not r["pass"]]
    if not fails:
        lines.append("  (none)")
    for r in fails:
        lines.append(f"  {r['query_class']} x {r['tier']} run {r['run']}: "
                     f"{', '.join(r['failed_criteria'])} -- {r['judge_notes'][:120]}")
    if ref_pass < 8 / 9:
        lines += ["", "  [!] INTEGRITY FLAG: frontier reference failed its own rubric too often.",
                  "      Per pre-registration: fix rubric, re-register as v1.1, re-run."]
    lines += ["", "Full answers and per-cell data: aeq_grid_raw.json",
              "Author: Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026"]

    report = "\n".join(lines)
    (outdir / "aeq_grid_report.md").write_text(report, encoding="utf-8")
    print("\n" + report)
    print(f"\n[OK] Saved: {outdir/'aeq_grid_report.md'} and aeq_grid_raw.json")


def main():
    ap = argparse.ArgumentParser(description="AEQ 3x3x3 grid experiment")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--outdir", type=str, default="experiments/grid")
    args = ap.parse_args()
    if args.dry_run:
        dry_run(args.runs)
    else:
        run_grid(args.runs, Path(args.outdir))


if __name__ == "__main__":
    main()

<<<FILE_END:aeq_grid_experiment.py>>>

After creating both, run `python -m py_compile aeq_grid_experiment.py` to confirm a clean transcription. If it does not compile, you transcribed it wrong — re-create it exactly, do not patch it.

### Step 2 — Environment
```
pip install tiktoken requests python-dotenv
```
Confirm `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` exist in `.env` (existence check only). If either is missing, STOP and tell me — do not proceed and do not create placeholder keys.

### Step 3 — Verify pricing (BEFORE running)
The `PRICING` dict in the CONFIG block contains PLACEHOLDER values. Verify each model's current per-1M-token input/output pricing against the official pages:
- OpenAI: https://platform.openai.com/docs/pricing
- Anthropic: https://www.anthropic.com/pricing

Correct any values that differ, then set `PRICING_VERIFIED = True`. Record every change (old → new) for the final report. If you cannot access the pages, leave the flag `False`, note it, and proceed — cost figures will carry an unverified flag.

### Step 4 — Dry run
```
python aeq_grid_experiment.py --dry-run
```
Confirm the estimate is under $1 and report it.

### Step 5 — Full grid
```
python aeq_grid_experiment.py
```
The script pre-flights configured model names against `/v1/models`. If it aborts on an unavailable name, choose the closest equivalent from the candidates it prints, keeping tier ordering intact (T1 = most capable, T2 = mid, T3 = cheapest). Preferred fallback set: `gpt-4o` / `gpt-4o-mini` / `gpt-4.1-nano`. Record any substitution (configured → actual), then re-run. Expected wall time: 10–20 minutes. Let the script's retry logic handle individual run errors — do not intervene mid-run.

### Step 6 — Integrity checks
Open `experiments/grid/aeq_grid_report.md` and verify:
- Frontier reference self-pass ≥ 8/9. If NOT: STOP — the rubric is defective per the pre-registration. Report the failed criteria verbatim and take no further action. Do not "fix" the rubric.
- Every cell has 3 runs, or failures are explicitly logged.
- The gate verdict (GREEN/YELLOW/RED) is present.

### Step 7 — Report back to me
Summary in this exact order:
1. Gate verdict: GREEN / YELLOW / RED
2. Aggregate SUT pass rate vs. the declared prior (75–80%)
3. Full pass-rate matrix (query class × tier)
4. Cost deltas (T1/T2, T1/T3) and verification overhead per query
5. Where you created the files, and any model substitutions (configured → actual)
6. Pricing corrections (old → new) and `PRICING_VERIFIED` status
7. Every failed cell with failed criteria, verbatim
8. Paths to `aeq_grid_report.md` and `aeq_grid_raw.json`

Do not editorialize. Do not soften a RED. Do not inflate a YELLOW. The verdict is the verdict.

## WHAT THIS IS FOR

This is the single cheapest de-risking step for a product concept (AEQ Verify) whose load-bearing assumption — cheap tiers passing pre-registered equivalence rubrics — has never been measured. The result is scored against a prior declared in writing before the run. A RED result is as publishable as a GREEN one. Numbers must be REAL — measured from actual API calls, never estimated, never fabricated.

---
Michael Valderrama | AI Agent Architect | Independent R&D © 2026
