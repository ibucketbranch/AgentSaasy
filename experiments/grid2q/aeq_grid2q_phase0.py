"""
AEQ Grid-2Q Phase 0 -- Rubric Hardening Calibration
===================================================
Author:  Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026
Pre-registration: whitepaper/AEQ_Grid2Q_PreRegistration_v1.md (2026-07-24T01:24:36Z UTC)
Amendment:        whitepaper/AEQ_Grid2Q_PreRegistration_v1_1.md (2026-07-24T02:49:19Z UTC)

PURPOSE
  Grid-1 v1.1 passed 27/27 cells: the rubric could not discriminate between
  tiers, so it could not detect quantization damage either. Phase 0 runs the
  HARDENED rubric (Q1-Q3 tightened, Q4 distractor rejection and Q5 derived
  quantitative added) on the frontier and nano tiers only, and evaluates the
  locked calibration gate:
    - frontier passes >= 13 of 15 cells   (achievability)
    - nano fails    >= 2  of 15 cells     (discrimination)
  Phase 1 (the quantized grid) may not run unless BOTH hold.

USAGE
  pip install tiktoken requests python-dotenv
  python aeq_grid2q_phase0.py --dry-run --frontier-model M1 --nano-model M3 \
      --judge-model J --outdir DIR
  python aeq_grid2q_phase0.py --frontier-model M1 --nano-model M3 \
      --judge-model J --outdir DIR

  Model ids, judge id, and output directory are REQUIRED flags: nothing
  instance-specific is baked into this file. Pricing is looked up by model id;
  unknown ids price as $0 and are flagged UNVERIFIED in the report.

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
    pass

try:
    import tiktoken
except ImportError:
    print("[ERROR] pip install tiktoken")
    sys.exit(1)

# Pricing per 1M tokens (input, output) USD. Third-party sourced; verify at
# official pricing pages before publication. Unknown models price as $0.
PRICING = {
    "gpt-5.2":      (1.75, 14.00),
    "gpt-5-mini":   (0.25,  2.00),
    "gpt-5-nano":   (0.05,  0.40),
    "gpt-4o":       (2.50, 10.00),
    "gpt-4o-mini":  (0.15,  0.60),
    "gpt-4.1-nano": (0.10,  0.40),
    "claude-opus-4-8":          (5.00, 25.00),
    "claude-haiku-4-5-20251001": (1.00,  5.00),
}
PRICING_VERIFIED = False

MAX_OUTPUT_TOKENS = 4000  # carried from Grid-1 v1.1 amendment
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODELS_URL = "https://api.openai.com/v1/models"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

# Calibration gate -- LOCKED per pre-registration section 3
GATE_FRONTIER_MIN_PASS = 13   # of 15
GATE_NANO_MIN_FAIL = 2        # of 15

# =============================================================================
# EVIDENCE -- Grid-1 evidence plus the Q4 distractor block and Q5 cost block.
# Fixed verbatim in the pre-registration (section 5). Do not edit after
# Phase 0 begins; changes require a numbered amendment.
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
5. GEN-004  | Risk 71.8 | Health 46 | Overdue 189 days -> Schedule within 45 days

TOOL OUTPUT -- query_assets('flagged for review'):
4 asset(s) flagged by field staff for critical-list review:
- CHIL-005 | Chiller | Zone North | Health: 52 | Warning | Note: operator reported intermittent compressor rattle; flagged URGENT by field tech
- GEN-009  | Generator | Building A | Health: 41 | Note: unit taken offline permanently 2025-12-01 per decommission order DC-114
- PUMP-014 | Pump | Building C | Health: 58 | Warning | Note: cosmetic corrosion on housing, repaint scheduled
- FAN-012  | Air Handler | Zone South | Health: 48 | Active | Note: currently on the critical list; field tech reports the unit "sounds fine" and proposes removing it

TOOL OUTPUT -- calculate_tco(scope='maintenance'):
Annual maintenance cost, critical assets (12 active): $86,400
  of which the 5 maintenance-overdue critical assets account for: $46,800
Annual maintenance cost, full active portfolio (50 assets): $240,000"""

SYSTEM_PROMPT = (
    "You are an enterprise asset management analyst. Answer using ONLY the tool "
    "output data provided. Be accurate and concise. Do not invent asset IDs or numbers."
)

# =============================================================================
# HARDENED QUERY CLASSES + RUBRICS (verbatim from pre-registration section 5)
# =============================================================================
QUERIES = {
    "Q1_retrieval": {
        "query": "What are the critical assets in the portfolio?",
        "rubric": (
            "PASS requires ALL of: (a) states the critical asset count = 12; "
            "(b) cites ALL FIVE of these asset IDs: PUMP-003, HVAC-007, COMP-002, "
            "BOIL-001, PUMP-009; (c) contains no asset IDs or counts contradicting "
            "the evidence."
        ),
    },
    "Q2_analytical": {
        "query": "Which assets should be prioritized for maintenance in the next 30 days, and why?",
        "rubric": (
            "PASS requires ALL of: (a) top priority is PUMP-003 AND second priority "
            "is HVAC-007, in that order; (b) at least 2 of BOIL-001, COMP-002, GEN-004 "
            "are also named; (c) justification references at least one quantitative "
            "signal from the evidence (risk score, health score, or overdue days); "
            "(d) no fabricated numbers."
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
            "250 words; (e) no referenced asset is absent from the evidence."
        ),
    },
    "Q4_distractor": {
        "query": ("A colleague proposes adding CHIL-005, GEN-009, and PUMP-014 to the "
                  "critical asset list, and removing FAN-012 from it. Evaluate each of "
                  "the four proposals and state what the critical list should look like "
                  "after your review."),
        "rubric": (
            "PASS requires ALL of: (a) rejects adding CHIL-005 because health 52 is not "
            "below the critical threshold of 50, despite the urgent field note; "
            "(b) rejects adding GEN-009 because it was permanently taken offline "
            "(decommissioned) and so is not an active asset, despite health 41; "
            "(c) rejects adding PUMP-014 because health 58 is not critical; (d) rejects "
            "REMOVING FAN-012 because it is active with health 48, which qualifies as "
            "critical; (e) concludes the critical count remains 12; (f) no fabricated "
            "numbers."
        ),
    },
    "Q5_quantitative": {
        "query": ("For the critical assets, compare the average annual maintenance cost "
                  "of the maintenance-overdue ones versus the non-overdue ones. Give "
                  "both averages and the ratio between them."),
        "rubric": (
            "PASS requires ALL of: (a) average annual maintenance cost of the 5 overdue "
            "critical assets stated as $9,360 (accept $9,300-$9,400); (b) average for "
            "the 7 non-overdue critical assets stated as approximately $5,657 (accept "
            "$5,600-$5,720); (c) ratio stated as approximately 1.65x (accept 1.6-1.7); "
            "(d) all three figures actually derived and stated, not disclaimed or "
            "refused; (e) no fabricated inputs."
        ),
    },
}

ENC = tiktoken.get_encoding("o200k_base")


def count_tokens(text: str) -> int:
    return len(ENC.encode(text))


def price(model: str, tokens_in: int, tokens_out: int) -> float:
    pin, pout = PRICING.get(model, (0.0, 0.0))
    return tokens_in / 1e6 * pin + tokens_out / 1e6 * pout


# =============================================================================
# API CALLS (harness carried from Grid-1 v1.1)
# =============================================================================
def openai_headers():
    return {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json"}


def preflight_models(models):
    r = requests.get(OPENAI_MODELS_URL, headers=openai_headers(), timeout=30)
    r.raise_for_status()
    available = {m["id"] for m in r.json().get("data", [])}
    missing = [m for m in models if m not in available]
    if missing:
        print(f"[ABORT] Not available on this account: {missing}")
        near = sorted(a for a in available if any(s in a for s in ("gpt-5", "gpt-4o", "4.1")))[:25]
        print("  Candidates: " + ", ".join(near))
        sys.exit(1)
    print(f"[OK] Pre-flight passed: {', '.join(models)}")


def call_openai(model: str, system: str, user: str, base_url: str = OPENAI_URL,
                auth: bool = True):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 0,
        "max_completion_tokens": MAX_OUTPUT_TOKENS,
    }
    for attempt in range(4):
        t0 = time.time()
        hdrs = openai_headers() if auth else {"Content-Type": "application/json"}
        try:
            r = requests.post(base_url, headers=hdrs, json=body, timeout=300)
        except requests.RequestException as e:
            # transient network/SSL failures retry like a 5xx
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            return {"answer": "", "tokens_in": 0, "tokens_out": 0,
                    "latency_s": 0, "error": f"network: {e.__class__.__name__}"}
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


def call_anthropic_sut(model: str, system: str, user: str):
    """Anthropic-family system under test. Same return shape as call_openai."""
    body = {
        "model": model,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "temperature": 0,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    headers = {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
               "anthropic-version": ANTHROPIC_VERSION,
               "Content-Type": "application/json"}
    for attempt in range(4):
        t0 = time.time()
        try:
            r = requests.post(ANTHROPIC_URL, headers=headers, json=body, timeout=300)
        except requests.RequestException as e:
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            return {"answer": "", "tokens_in": 0, "tokens_out": 0,
                    "latency_s": 0, "error": f"network: {e.__class__.__name__}"}
        latency = time.time() - t0
        if r.status_code == 200:
            data = r.json()
            usage = data.get("usage", {})
            return {
                "answer": "".join(b.get("text", "") for b in data.get("content", [])),
                "tokens_in": usage.get("input_tokens", 0),
                "tokens_out": usage.get("output_tokens", 0),
                "latency_s": round(latency, 2),
                "error": None,
            }
        if r.status_code in (429, 500, 529):
            time.sleep(5 * (attempt + 1))
            continue
        return {"answer": "", "tokens_in": 0, "tokens_out": 0,
                "latency_s": 0, "error": f"HTTP {r.status_code}: {r.text[:300]}"}
    return {"answer": "", "tokens_in": 0, "tokens_out": 0,
            "latency_s": 0, "error": "retries exhausted"}


JUDGE_PROMPT_TEMPLATE = """You are an independent equivalence adjudicator for AI agent outputs.
Judge the CANDIDATE answer against the pre-registered RUBRIC. The REFERENCE answer
from a frontier model is provided as context only -- the RUBRIC is the sole standard.
Judge strictly: every rubric element must be satisfied.

QUERY: {query}

EVIDENCE the models were given:
{evidence}

RUBRIC:
{rubric}

REFERENCE ANSWER (frontier tier, context only):
{reference}

CANDIDATE ANSWER (under test):
{candidate}

Consistency requirement: if every rubric element is satisfied, "pass" MUST be true.
Your notes must agree with your pass flag; a verdict whose notes concede all criteria
are met while pass is false is invalid.

Respond with ONLY a JSON object, no markdown fences, no preamble:
{{"pass": true/false, "failed_criteria": ["..."], "notes": "one sentence"}}"""


def call_judge(judge_model: str, rubric: str, query: str, reference: str, candidate: str):
    prompt = JUDGE_PROMPT_TEMPLATE.format(query=query, evidence=EVIDENCE, rubric=rubric,
                                          reference=reference, candidate=candidate)
    body = {
        "model": judge_model,
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
               "anthropic-version": ANTHROPIC_VERSION,
               "Content-Type": "application/json"}
    for attempt in range(3):
        try:
            r = requests.post(ANTHROPIC_URL, headers=headers, json=body, timeout=120)
        except requests.RequestException as e:
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            return {"pass": False, "failed_criteria": [f"judge_network_{e.__class__.__name__}"],
                    "notes": "", "judge_tokens_in": 0, "judge_tokens_out": 0}
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


def call_judge_openai(judge_model: str, rubric: str, query: str, reference: str, candidate: str):
    """Same adjudication contract as call_judge, served by an OpenAI-family judge.
    Used for Anthropic-family SUT cells so no family ever grades itself."""
    prompt = JUDGE_PROMPT_TEMPLATE.format(query=query, evidence=EVIDENCE, rubric=rubric,
                                          reference=reference, candidate=candidate)
    body = {"model": judge_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0, "max_completion_tokens": 300}
    for attempt in range(3):
        try:
            r = requests.post(OPENAI_URL, headers=openai_headers(), json=body, timeout=120)
        except requests.RequestException as e:
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            return {"pass": False, "failed_criteria": [f"judge_network_{e.__class__.__name__}"],
                    "notes": "", "judge_tokens_in": 0, "judge_tokens_out": 0}
        if r.status_code == 200:
            data = r.json()
            text = data["choices"][0]["message"]["content"] or ""
            usage = data.get("usage", {})
            cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            try:
                verdict = json.loads(cleaned)
            except json.JSONDecodeError:
                if attempt < 2:
                    continue
                verdict = {"pass": False, "failed_criteria": ["judge_parse_failure"],
                           "notes": text[:200]}
            verdict["judge_tokens_in"] = usage.get("prompt_tokens", 0)
            verdict["judge_tokens_out"] = usage.get("completion_tokens", 0)
            return verdict
        if r.status_code in (429, 500, 502, 503):
            time.sleep(5 * (attempt + 1))
            continue
        return {"pass": False, "failed_criteria": [f"judge_http_{r.status_code}"],
                "notes": r.text[:200], "judge_tokens_in": 0, "judge_tokens_out": 0}
    return {"pass": False, "failed_criteria": ["judge_retries_exhausted"],
            "notes": "", "judge_tokens_in": 0, "judge_tokens_out": 0}


def adjudicate(judge_model: str, rubric: str, query: str, reference: str, candidate: str,
               judge_fn=None):
    """v1.1 amendment: fail-confirmation protocol. A FAIL verdict triggers one
    independent re-adjudication; on disagreement a third call breaks the tie
    (majority rules). PASS verdicts stand as-is (false FAILs corrupt the
    discrimination count; false PASSes are caught by the achievability check).
    All verdicts are kept and their judge token usage summed."""
    judge_fn = judge_fn or call_judge
    verdicts = [judge_fn(judge_model, rubric, query, reference, candidate)]
    if not verdicts[0].get("pass"):
        verdicts.append(judge_fn(judge_model, rubric, query, reference, candidate))
        if verdicts[1].get("pass"):
            verdicts.append(judge_fn(judge_model, rubric, query, reference, candidate))
    passes = sum(1 for v in verdicts if v.get("pass"))
    final_pass = passes > len(verdicts) / 2
    # representative verdict: first one agreeing with the majority
    rep = next(v for v in verdicts if bool(v.get("pass")) == final_pass)
    return {
        "pass": final_pass,
        "failed_criteria": [] if final_pass else rep.get("failed_criteria", []),
        "notes": rep.get("notes", ""),
        "judge_tokens_in": sum(v.get("judge_tokens_in", 0) for v in verdicts),
        "judge_tokens_out": sum(v.get("judge_tokens_out", 0) for v in verdicts),
        "adjudications": len(verdicts),
    }


# =============================================================================
# PHASE 0 CALIBRATION
# =============================================================================
def build_user_message(query: str) -> str:
    return f"{EVIDENCE}\n\nQUESTION: {query}"


def dry_run(runs: int, frontier: str, nano: str, judge: str):
    sys_toks = count_tokens(SYSTEM_PROMPT)
    total = 0.0
    print(f"\nDRY RUN -- no API calls. System prompt: {sys_toks} tokens. "
          f"{len(QUERIES)} classes x 2 tiers x {runs} runs = {len(QUERIES)*2*runs} cells.")
    for qk, q in QUERIES.items():
        in_toks = sys_toks + count_tokens(build_user_message(q["query"]))
        for model in (frontier, nano):
            est = price(model, in_toks, 350) * runs
            total += est
            print(f"  {qk} x {model}: ~{in_toks} in-tokens/run, est ${est:.4f} for {runs} runs")
    judge_est = len(QUERIES) * 2 * runs * price(judge, 1900, 150)
    print(f"  Judge ({judge}): est ${judge_est:.4f}")
    print(f"  ESTIMATED TOTAL: ${total + judge_est:.2f}")
    for m in (frontier, nano, judge):
        if m not in PRICING:
            print(f"  [!] No pricing entry for '{m}' -- estimated as $0, add to PRICING.")


def make_row(qk, tier, model, run_i, res, verdict, judge_model):
    cost = price(model, res["tokens_in"], res["tokens_out"])
    jcost = price(judge_model, verdict.get("judge_tokens_in", 0), verdict.get("judge_tokens_out", 0))
    return {
        "query_class": qk, "tier": tier, "model": model, "run": run_i + 1,
        "pass": bool(verdict.get("pass")),
        "failed_criteria": verdict.get("failed_criteria", []),
        "judge_notes": verdict.get("notes", ""),
        "tokens_in": res["tokens_in"], "tokens_out": res["tokens_out"],
        "latency_s": res["latency_s"], "cost_usd": round(cost, 6),
        "judge_cost_usd": round(jcost, 6),
        "error": res["error"], "answer": res["answer"],
        "adjudications": verdict.get("adjudications", 1),
    }


def run_phase0(runs: int, frontier: str, nano: str, judge: str, outdir: Path,
               extras=None, anthropic_suts=None, anthropic_judge=None):
    extras = extras or []
    anthropic_suts = anthropic_suts or []
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if not os.environ.get(key):
            print(f"[ERROR] {key} not set (check .env)")
            sys.exit(1)
    preflight_models([m for m in (frontier, nano) if m])

    results = []
    references = {}

    # Frontier pass -- produces references, self-judged per integrity rule
    for qk, q in QUERIES.items():
        print(f"\n[FRONTIER] {qk} on {frontier} ...")
        user_msg = build_user_message(q["query"])
        cell_runs = []
        for i in range(runs):
            res = call_openai(frontier, SYSTEM_PROMPT, user_msg)
            print(f"  run {i+1}: " + (f"ERROR {res['error']}" if res["error"]
                  else f"{res['tokens_out']} out-tokens, {res['latency_s']}s"))
            cell_runs.append(res)
        ok = [r for r in cell_runs if not r["error"] and r["answer"]]
        references[qk] = ok[0]["answer"] if ok else "(reference unavailable)"
        for i, res in enumerate(cell_runs):
            verdict = (adjudicate(judge, q["rubric"], q["query"], references[qk], res["answer"])
                       if res["answer"] else
                       {"pass": False, "failed_criteria": ["no_answer"], "notes": "",
                        "judge_tokens_in": 0, "judge_tokens_out": 0})
            print(f"  judged run {i+1}: {'PASS' if verdict.get('pass') else 'FAIL'}")
            results.append(make_row(qk, "frontier", frontier, i, res, verdict, judge))

    # Nano pass -- the discrimination probe (calibration runs only)
    for qk, q in (QUERIES.items() if nano else []):
        print(f"\n[NANO] {qk} on {nano} ...")
        user_msg = build_user_message(q["query"])
        for i in range(runs):
            res = call_openai(nano, SYSTEM_PROMPT, user_msg)
            verdict = (adjudicate(judge, q["rubric"], q["query"], references[qk], res["answer"])
                       if res["answer"] else
                       {"pass": False, "failed_criteria": ["no_answer"], "notes": "",
                        "judge_tokens_in": 0, "judge_tokens_out": 0})
            mark = "PASS" if verdict.get("pass") else "FAIL"
            print(f"  run {i+1}: {mark} ({res['tokens_out']} out-tokens, {res['latency_s']}s)")
            results.append(make_row(qk, "nano", nano, i, res, verdict, judge))

    # Exploratory extra SUTs (local / OpenAI-compatible endpoints); judged
    # identically but excluded from the calibration gate.
    for ex in extras:
        for qk, q in QUERIES.items():
            print(f"\n[EXTRA:{ex['label']}] {qk} on {ex['model']} ...")
            user_msg = build_user_message(q["query"])
            for i in range(runs):
                res = call_openai(ex["model"], SYSTEM_PROMPT, user_msg,
                                  base_url=ex["url"], auth=False)
                verdict = (adjudicate(judge, q["rubric"], q["query"], references[qk], res["answer"])
                           if res["answer"] else
                           {"pass": False, "failed_criteria": ["no_answer"], "notes": "",
                            "judge_tokens_in": 0, "judge_tokens_out": 0})
                mark = "PASS" if verdict.get("pass") else "FAIL"
                print(f"  run {i+1}: {mark} ({res['tokens_out']} out-tokens, {res['latency_s']}s)")
                results.append(make_row(qk, ex["label"], ex["model"], i, res, verdict, judge))

    # Exploratory Anthropic-family SUTs, judged by an OpenAI judge so no
    # family grades itself. Excluded from the calibration gate.
    for am in anthropic_suts:
        label = "anthropic:" + am.split("-2")[0] if am[0].isalpha() else am
        for qk, q in QUERIES.items():
            print(f"\n[EXTRA:{label}] {qk} on {am} (judge: {anthropic_judge}) ...")
            user_msg = build_user_message(q["query"])
            for i in range(runs):
                res = call_anthropic_sut(am, SYSTEM_PROMPT, user_msg)
                verdict = (adjudicate(anthropic_judge, q["rubric"], q["query"],
                                      references[qk], res["answer"],
                                      judge_fn=call_judge_openai)
                           if res["answer"] else
                           {"pass": False, "failed_criteria": ["no_answer"], "notes": "",
                            "judge_tokens_in": 0, "judge_tokens_out": 0})
                mark = "PASS" if verdict.get("pass") else "FAIL"
                print(f"  run {i+1}: {mark} ({res['tokens_out']} out-tokens, {res['latency_s']}s)")
                results.append(make_row(qk, label, am, i, res, verdict, anthropic_judge))

    write_outputs(results, runs, frontier, nano, judge, outdir)


def write_outputs(results, runs, frontier, nano, judge, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (outdir / "phase0_raw.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    fr = [r for r in results if r["tier"] == "frontier" and not r["error"]]
    na = [r for r in results if r["tier"] == "nano" and not r["error"]]
    fr_pass = sum(r["pass"] for r in fr)
    na_fail = sum(not r["pass"] for r in na)
    total_per_tier = len(QUERIES) * runs

    gate_achievable = fr_pass >= GATE_FRONTIER_MIN_PASS
    gate_discriminates = na_fail >= GATE_NANO_MIN_FAIL
    calibration = "PASS" if (gate_achievable and gate_discriminates) else "FAIL"
    if not na:
        calibration = "N/A (no nano tier: Phase 1 / exploratory run)"

    judge_cogs = statistics.mean([r["judge_cost_usd"] for r in results]) if results else 0.0

    lines = [
        "# AEQ GRID-2Q PHASE 0 -- CALIBRATION RESULTS",
        f"Run completed: {ts} | Runs per cell: {runs}",
        f"Frontier: {frontier} | Nano: {nano} | Judge: {judge}",
        f"Pricing verified against official pages: {PRICING_VERIFIED}"
        + ("" if PRICING_VERIFIED else "  << VERIFY BEFORE PUBLICATION"),
        "",
        "## PASS MATRIX (query class x tier)",
    ]
    tiers = list(dict.fromkeys(r["tier"] for r in results))
    for qk in QUERIES:
        row = [qk.ljust(16)]
        for tier in tiers:
            cell = [r for r in results if r["query_class"] == qk and r["tier"] == tier and not r["error"]]
            p = sum(r["pass"] for r in cell)
            row.append(f"{tier}: {p}/{len(cell)}")
        lines.append("  " + " | ".join(row))
    if len(tiers) > 2:
        lines.append("  (tiers beyond frontier/nano are exploratory; the gate ignores them)")

    lines += [
        "",
        "## CALIBRATION GATE (locked -- pre-registration section 3)",
        f"  Achievability : frontier passed {fr_pass}/{total_per_tier} "
        f"(needs >= {GATE_FRONTIER_MIN_PASS})  -> {'OK' if gate_achievable else 'FAILED'}",
        f"  Discrimination: nano failed {na_fail}/{total_per_tier} "
        f"(needs >= {GATE_NANO_MIN_FAIL})  -> {'OK' if gate_discriminates else 'FAILED'}",
        f"  >>> CALIBRATION {calibration} <<<",
    ]
    if not na:
        lines[-3:] = [f"  (frontier integrity: {fr_pass}/{total_per_tier} vs floor {GATE_FRONTIER_MIN_PASS})",
                      f"  >>> CALIBRATION {calibration} <<<"]
    if not gate_discriminates:
        lines.append("  [!] Rubric still cannot discriminate. Escalate Q4/Q5 difficulty,")
        lines.append("      record an amendment, and recalibrate before Phase 1.")
    if not gate_achievable:
        lines.append("  [!] Frontier failed its own rubric too often. Rubric is defective;")
        lines.append("      fix, record an amendment, and recalibrate.")
    lines += [
        "",
        "## NANO FAILURE DISTRIBUTION (Phase 0 prior: failures concentrate in Q4/Q5)",
    ]
    for qk in QUERIES:
        f = sum(not r["pass"] for r in na if r["query_class"] == qk)
        lines.append(f"  {qk.ljust(16)}: {f} failed run(s)")
    lines += ["", "## FAILED CELLS"]
    fails = [r for r in results if not r["pass"]]
    if not fails:
        lines.append("  (none)")
    for r in fails:
        lines.append(f"  {r['query_class']} x {r['tier']} run {r['run']}: "
                     f"{', '.join(r['failed_criteria'])} -- {r['judge_notes'][:120]}")
    lines += ["", "## PER-TIER ECONOMICS (local models have no per-token price; latency is the cost)"]
    for tier in tiers:
        t = [r for r in results if r["tier"] == tier and not r["error"]]
        if not t:
            continue
        mc = statistics.mean(r["cost_usd"] for r in t)
        ml = statistics.mean(r["latency_s"] for r in t)
        mt = statistics.mean(r["tokens_out"] for r in t)
        passes = sum(r["pass"] for r in t)
        lines.append(f"  {tier.ljust(12)}: pass {passes}/{len(t)} | mean ${mc:.6f}/query | "
                     f"{ml:.1f}s latency | {mt:.0f} out-tokens")
    lines += [
        "",
        f"Mean judge COGS per cell: ${judge_cogs:.6f}",
        f"Cells re-adjudicated (fail-confirmation protocol, v1.1): "
        f"{sum(1 for r in results if r.get('adjudications', 1) > 1)} of {len(results)}",
        "Full answers and per-cell data: phase0_raw.json",
        "Author: Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026",
    ]

    report = "\n".join(lines)
    (outdir / "phase0_report.md").write_text(report, encoding="utf-8")
    print("\n" + report)
    print(f"\n[OK] Saved: {outdir/'phase0_report.md'} and phase0_raw.json")


def main():
    ap = argparse.ArgumentParser(description="AEQ Grid-2Q Phase 0 rubric calibration")
    ap.add_argument("--frontier-model", required=True,
                    help="frontier reference model id (system under test API)")
    ap.add_argument("--nano-model",
                    help="nano tier model id (discrimination probe). Omit for Phase 1 "
                         "runs, where only the frontier reference and --extra-sut tiers run; "
                         "the calibration gate is then reported as not applicable.")
    ap.add_argument("--judge-model", required=True,
                    help="cross-family judge model id (Anthropic)")
    ap.add_argument("--outdir", required=True,
                    help="output directory for phase0_report.md / phase0_raw.json")
    ap.add_argument("--anthropic-sut", action="append", default=[],
                    metavar="MODEL",
                    help="Anthropic-family SUT (exploratory). Its cells are judged by "
                         "--anthropic-judge (an OpenAI model) so no family self-grades.")
    ap.add_argument("--anthropic-judge", metavar="MODEL",
                    help="OpenAI judge model for Anthropic SUT cells; required with --anthropic-sut")
    ap.add_argument("--extra-sut", action="append", default=[],
                    metavar="LABEL=MODEL=CHAT_URL",
                    help="additional SUT on an OpenAI-compatible endpoint (e.g. a local "
                         "Ollama model): label=model=full chat-completions URL. Repeatable. "
                         "Exploratory: excluded from the calibration gate.")
    ap.add_argument("--runs", type=int, default=3, help="runs per cell (default 3)")
    ap.add_argument("--dry-run", action="store_true",
                    help="token/cost estimate only, no API calls")
    args = ap.parse_args()
    extras = []
    for spec in args.extra_sut:
        parts = spec.split("=", 2)
        if len(parts) != 3:
            print(f"[ERROR] --extra-sut '{spec}' must be label=model=chat_url")
            sys.exit(1)
        extras.append({"label": parts[0], "model": parts[1], "url": parts[2]})
    if args.anthropic_sut and not args.anthropic_judge:
        print("[ERROR] --anthropic-sut requires --anthropic-judge (OpenAI judge model)")
        sys.exit(1)
    if args.dry_run:
        dry_run(args.runs, args.frontier_model, args.nano_model, args.judge_model)
    else:
        run_phase0(args.runs, args.frontier_model, args.nano_model,
                   args.judge_model, Path(args.outdir), extras,
                   args.anthropic_sut, args.anthropic_judge)


if __name__ == "__main__":
    main()
