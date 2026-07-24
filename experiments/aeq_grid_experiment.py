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
# v1.1 amendment: haiku judge produced arithmetically false rejections of
# correct frontier answers in the v1.0 run; upgraded to opus per author approval.
JUDGE_MODEL = "claude-opus-4-8"

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
    JUDGE_MODEL:    (5.00, 25.00),
}
PRICING_VERIFIED = False  # flip to True after checking official pricing pages

# v1.1 amendment: 600 was consumed entirely by gpt-5-mini/nano reasoning
# tokens, returning empty answers; raised to 4000 per author approval.
MAX_OUTPUT_TOKENS = 4000
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

