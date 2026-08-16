# ChiefOS Telemetry / Instrumentation Spec for AEQ Evaluation

**Written 2026-08-16. Status: DESIGN. Companion to `README.md` in this directory.**

Design stance in one paragraph: one append-only event stream, six event types, one correlation spine (`cycle_id -> task_id -> call_id`), captured at exactly two choke points (the LLM client and the orchestrator dispatch loop) plus three narrow tap-ins (fork decisions, OCR cascade, outcome resolution). Storage is dual-written: a single JSONB table in the existing PostgreSQL plus a daily-rotated JSONL file. Public output is produced by a whitelist projector - a public event is constructed from named fields, never by redacting a private one. Field names reuse the phase0_raw.json vocabulary (`tokens_in`, `tokens_out`, `latency_s`, `cost_usd`, `tier`, `model`, `pass`, `error`) so ChiefOS run data and AEQ Grid run data can be joined in the same analysis code.

## 1. Event Schema

### 1.1 Common envelope (every event)

```json
{
  "schema_ver": "chiefos-telemetry/1",
  "event_id": "01J5Y8...",
  "event_type": "llm_call",
  "ts": "2026-08-16T14:00:03.412Z",
  "cycle_id": "c-2026-08-16T14",
  "task_id": "t-01J5Y8...",
  "parent_id": null,
  "agent": "filing_clerk",
  "doc_ref": "d-a1b2c3",
  "dry_run": false
}
```

Rules: `event_id` is a ULID (sortable, unique, no coordination needed). `cycle_id` is one per orchestrator wake, the AEQ-L "run" unit. `agent` is a closed enum matching the eight published agents (orchestrator, filing_clerk, lost_found, dedup_hunter, student, profiler, auditor, keeper). `doc_ref` is an opaque internal surrogate key ChiefOS already has; the raw event never contains a filesystem path - that constraint is applied at capture, not at sanitization, so a leak of the raw log is survivable.

### 1.2 `cycle` - one per orchestrator wake (emitted twice: start, end)

```json
{
  "event_type": "cycle",
  "phase": "end",
  "trigger": "scheduled",
  "docs_pending": 14,
  "tasks_dispatched": 9,
  "tasks_by_agent": {"filing_clerk": 6, "lost_found": 2, "dedup_hunter": 1},
  "latency_s": 212.4,
  "degraded_mode": null,
  "error": null
}
```

`trigger`: scheduled | manual | catchup. `docs_pending` is the in-box depth at wake - this is the "minimum work" anchor for Layer 2. `degraded_mode`: null | "rule_based_all" | "local_only" (cloud gate closed).

### 1.3 `agent_task` - one per dispatch (emitted at task end)

```json
{
  "event_type": "agent_task",
  "task_kind": "classify_and_file",
  "pass": true,
  "outcome_code": "filed",
  "llm_calls": 2,
  "tool_calls": 3,
  "tokens_in": 1412,
  "tokens_out": 96,
  "latency_s": 8.9,
  "cost_usd": 0.0,
  "error": null,
  "retries": 0
}
```

`task_kind`: classify_and_file | second_opinion | dedup_scan | learn_rule | profile_extract | code_audit | health_check. `outcome_code`: filed | routed_review | dedup_proposed | rule_learned | no_action | error. Token fields are rollups of child llm_call events, denormalized for cheap queries.

### 1.4 `llm_call` - one per model invocation (the workhorse event)

```json
{
  "event_type": "llm_call",
  "tier": "local_fast",
  "model": "qwen2.5:7b-instruct",
  "purpose": "classify",
  "tokens_in": 812,
  "tokens_out": 44,
  "system_prompt_tokens": 291,
  "tokens_src": "ollama",
  "latency_s": 1.84,
  "cost_usd": 0.0,
  "error": null,
  "retries": 0,
  "cache_hit": false
}
```

`tier`: local_fast | local_analyst | cloud (rule_based never emits llm_call). `purpose`: classify | second_opinion | extract_obligation | profile_entities | summarize | audit | route. `system_prompt_tokens` is the tokenizer count on the system prompt string BEFORE the call (AEQ Layer 1). `tokens_src`: ollama | api_usage | tiktoken | estimate - the spec 6.7 measured-vs-estimated disclosure per record.

Token accounting, exact where available:

- Ollama: `prompt_eval_count` -> tokens_in, `eval_count` -> tokens_out from the response body; `tokens_src: "ollama"`. Ollama omits `prompt_eval_count` on a fully cached prompt; when absent, fall back to a tokenizer count and mark `tokens_src: "estimate"`.
- Anthropic: `response.usage.input_tokens` / `output_tokens` (plus `cache_read_input_tokens` in an optional `tokens_in_cached` field). `tokens_src: "api_usage"`.
- OpenAI-compatible cloud: `usage.prompt_tokens` / `completion_tokens` when returned; tiktoken locally otherwise.
- `system_prompt_tokens` is always computed locally before the call, per spec section 4 Layer 1 - the only per-call field needing new computation, cheap and cacheable per (agent, prompt-version).

### 1.5 `fork_decision` - one per gated branch (spec 9.6: fork = validation call site)

```json
{
  "event_type": "fork_decision",
  "fork": "routing_tier",
  "branch_taken": "local_analyst",
  "reason_code": "low_confidence_escalation",
  "validator_kind": "rule",
  "validator_tokens": 0,
  "confidence": 0.71,
  "alternatives_considered": ["local_fast"]
}
```

`fork`: routing_tier | confidence_gate | dedup_accept | cloud_budget_gate | degradation | halt. `branch_taken` for routing_tier: rule_based | local_fast | local_analyst | cloud | human_review. `validator_kind`: rule | small_model | large_model | human (spec 9.6 rule 1: gates must be cheap). `validator_tokens` is the cost of the gate itself, 0 for deterministic rules. `confidence` is a PRIVATE-ONLY field: raw score kept for tuning, stripped by the projector - the public feed carries only the `reason_code` enum, never the numeric threshold.

Reason-code enum (closed, extend deliberately): high_confidence_rule_match, low_confidence_escalation, second_opinion_disagreement, budget_gate_closed, budget_gate_open, models_offline_fallback, operator_forced, novel_doc_type.

Every tier choice, every review-queue routing, every dedup accept/reject, and every graceful-degradation fallback emits one of these. This is the event that makes spec 9.6 gate A/B testing possible: `validator_tokens` is the gate's overhead, and joining fork decisions to downstream `outcome` events tells you whether the gate earned it.

### 1.6 `ocr_extraction` - one per document read

```json
{
  "event_type": "ocr_extraction",
  "cascade": ["native_text", "pdf_text_layer", "vision_ocr"],
  "stage_succeeded": "vision_ocr",
  "pages": 3,
  "chars_extracted": 4210,
  "latency_s": 6.1,
  "error": null
}
```

`stage_succeeded`: native_text | pdf_text_layer | office_extract | vision_ocr | failed. No tokens here, but it feeds AEQ-L causally: a document that needed the deep cascade correlates with downstream tier escalation, and the extraction cascade is itself a fork family worth cost-accounting (Vision OCR wall-clock is the "token" analog for the Swift side).

### 1.7 `outcome` - the AEQ-L numerator resolver (emitted at action time AND at correction time)

```json
{
  "event_type": "outcome",
  "outcome_kind": "filing",
  "verdict": "provisional_pass",
  "verdict_src": "system",
  "ref_task_id": "t-01J5Y8...",
  "days_to_verdict": 0
}
```

`outcome_kind`: filing | review_routing | dedup_proposal | rule_update | audit_finding. `verdict`: provisional_pass | confirmed_pass | corrected_fail | correct_refusal | incorrect_refusal. `verdict_src`: system | human_correction | human_approval | validation_window_expiry.

The novel design element, built on ground truth ChiefOS already has: the Student consumes human corrections. A filing is `provisional_pass` when made; when the human corrects it, emit a second `outcome` event with `verdict: "corrected_fail"` pointing at the same `ref_task_id`; when a validation window (default 14 days, to be replaced by the measured 95th-percentile correction latency from Phase B0) passes with no correction, a nightly job emits `confirmed_pass`. Review-queue routing that the human confirms was warranted emits `correct_refusal` - the AEQ-L "correct halt counts as value" clause (spec 9.2) made operational.

## 2. Capture and Storage

### 2.1 Where events live

Decision: dual-write, JSONL first, PostgreSQL second, both local.

1. JSONL append log - `telemetry/events-YYYY-MM-DD.jsonl`, one JSON object per line, written synchronously by a single background writer thread with a bounded in-memory queue. This is the durability layer and what the AEQ analysis scripts read (identical posture to phase0_raw.json: a flat record list). Survives DB migrations, trivially rsync-able, matches existing AEQ tooling.
2. One PostgreSQL table in the existing database - envelope columns promoted (event_id, ts, cycle_id, task_id, event_type, agent), everything else in a `payload JSONB` column, indexed on (cycle_id), (event_type, ts), (task_id). One table, not six - event types evolve faster than migrations should. Powers dashboard queries and the outcome-resolver job.

Writes are fail-open: if the queue is full or the DB is down, drop the Postgres write, keep the JSONL write; if both fail, increment a counter and continue. Telemetry must never block a filing operation - the zero-deletion safety contract outranks observability.

### 2.2 Where events are captured (minimal invasiveness into 26K lines)

1. The LLM client wrapper. ChiefOS necessarily has a small number of call sites (probably one client class) for Ollama and the cloud tier. Wrap it once; every llm_call event flows from there with zero per-agent changes. This is where system_prompt_tokens, tokens_src, retries, and latency are measured.
2. The orchestrator dispatch loop. One `cycle` context manager around the hourly wake; one `agent_task` context manager around each dispatch. Two edits in one file.
3. Explicit `emit()` calls at fork sites, the OCR cascade return, and the correction handler - the only places requiring surgical edits, each one line.

### 2.3 Suggested Python module interface (`chiefos/telemetry.py`)

```python
"""Telemetry for AEQ instrumentation. Fail-open: never raises into caller code."""
import json, queue, threading, time, contextlib
from ulid import ULID

SCHEMA_VER = "chiefos-telemetry/1"
_q: "queue.Queue[dict]" = queue.Queue(maxsize=10_000)
_ctx = threading.local()  # holds current cycle_id / task_id / parent_id


def emit(event_type: str, **fields) -> str:
    """Fire-and-forget. Returns event_id. Drops (with counter) if queue full."""
    ev = {
        "schema_ver": SCHEMA_VER, "event_id": str(ULID()),
        "event_type": event_type, "ts": _utcnow_iso(),
        "cycle_id": getattr(_ctx, "cycle_id", None),
        "task_id": getattr(_ctx, "task_id", None),
        "parent_id": getattr(_ctx, "parent_id", None),
        **fields,
    }
    try:
        _q.put_nowait(ev)
    except queue.Full:
        _dropped_inc()
    return ev["event_id"]


@contextlib.contextmanager
def cycle(trigger="scheduled", docs_pending=0):
    _ctx.cycle_id = f"c-{_utcnow_iso()[:13]}"
    emit("cycle", phase="start", trigger=trigger, docs_pending=docs_pending)
    t0 = time.monotonic()
    try:
        yield _ctx.cycle_id
    finally:
        emit("cycle", phase="end", latency_s=round(time.monotonic() - t0, 2))
        _ctx.cycle_id = None


@contextlib.contextmanager
def task(agent: str, task_kind: str, doc_ref=None, dry_run=False):
    _ctx.task_id = f"t-{ULID()}"
    t0, rollup = time.monotonic(), {"llm_calls": 0, "tokens_in": 0, "tokens_out": 0}
    _ctx.rollup = rollup
    try:
        yield rollup  # caller may set rollup["outcome_code"], rollup["pass"]
    finally:
        emit("agent_task", agent=agent, task_kind=task_kind, doc_ref=doc_ref,
             dry_run=dry_run, latency_s=round(time.monotonic() - t0, 2), **rollup)
        _ctx.task_id = None


def record_llm_call(tier, model, purpose, tokens_in, tokens_out,
                    system_prompt_tokens, tokens_src, latency_s,
                    cost_usd=0.0, error=None, retries=0):
    r = getattr(_ctx, "rollup", None)
    if r is not None:
        r["llm_calls"] += 1; r["tokens_in"] += tokens_in; r["tokens_out"] += tokens_out
    emit("llm_call", tier=tier, model=model, purpose=purpose, tokens_in=tokens_in,
         tokens_out=tokens_out, system_prompt_tokens=system_prompt_tokens,
         tokens_src=tokens_src, latency_s=latency_s, cost_usd=cost_usd,
         error=error, retries=retries)


def record_fork(fork, branch_taken, reason_code, validator_kind="rule",
                validator_tokens=0, confidence=None):
    emit("fork_decision", fork=fork, branch_taken=branch_taken,
         reason_code=reason_code, validator_kind=validator_kind,
         validator_tokens=validator_tokens, confidence=confidence)

# _writer(): daemon thread - drains _q, appends JSONL line, best-effort INSERT
# to Postgres. Started lazily on first emit(). Flush-on-exit via atexit.
```

The LLM client change is ~6 lines inside the existing client: extract usage counts, call record_llm_call(...). The Swift OCR helper writes a JSON line to a named pipe or stdout that the Python caller forwards via emit("ocr_extraction", ...) - do not build a second telemetry stack in Swift.

## 3. Deriving AEQ Quantities from the Events

All derivations are SQL/pandas over the events; nothing needs re-instrumenting later.

**Per-agent / per-cycle token totals.** Sum llm_call tokens grouped by agent (via task join) and by cycle_id. The agent_task rollups give the cheap version; the llm_call events are the auditable version - they should reconcile, and a nightly reconciliation check is itself a data-quality gate.

**Layer 1 - prompt overhead ratio.** Sum(system_prompt_tokens) / Sum(tokens_in + tokens_out) per agent per week. Measured pre-call with a tokenizer, this is the spec's exact section 4 measurement, per agent, continuously. The Orchestrator and Auditor will have legitimately different profiles (spec section 7: track per agent against its own baseline).

**Layer 2 - orchestration efficiency.** The minimum-work anchor is cycle.docs_pending: each pending document needs at most one classify task; anything above that is coordination. Metrics: tasks_dispatched / docs_pending (dispatch amplification), llm_calls per filed document (the ChiefOS analog of tool-calls-vs-minimum: a doc filed by rules = 0 calls, by fast tier = 1, escalated = 2+), retries summed per cycle. Second-opinion calls (Lost and Found) are deliberately extra calls - the fork events separate designed redundancy from waste.

**Layer 3 - output efficiency.** tokens_out per purpose. Classification calls should emit tens of tokens; upward drift on purpose "classify" is a Layer-3 regression alarm.

**AEQ-L (spec 9), per rolling window (default 30 days):**

```
numerator   = count(outcome.verdict IN ('confirmed_pass', 'correct_refusal'))
              + count(dedup proposals with human_approval)
denominator = Sum tokens_in + tokens_out over ALL llm_calls in the window
              - including retries, tasks that ended corrected_fail, and
                validator_tokens from model-backed gates (cumulative and
                honest, spec 9.3)
```

corrected_fail and incorrect_refusal subtract nothing from the denominator and add nothing to the numerator - failures pay full token freight. The validation window means AEQ-L is provisional for the trailing window and final behind it; the dashboard shows both.

**Coordination overhead - the section 11.5 experiment feed:**

```
coordination_overhead = (orchestrator tokens + gate/validator tokens
                         + second-opinion tokens on docs the first
                           classifier already got right)
                        / (worker tokens on tasks that produced outcomes)
```

Every term is directly computable: orchestrator tokens by agent = 'orchestrator'; gate tokens from fork_decision.validator_tokens; the second-opinion-on-correct term by joining Lost and Found tasks to outcomes where the first classification would have been confirmed. Report per-cycle and as a distribution, not just a mean.

**Gate break-even (spec 9.6 rule 2).** For each fork value: Sum(validator_tokens) (gate cost) vs token-cost of the failures the gate caught (join fork_decision -> downstream outcome). A gate whose caught-failure value is below its cumulative overhead is a candidate for removal - and that comparison is a publishable AEQ-L result on its own.

## 4. The Sanitization Boundary

Principle: whitelist projection, not redaction. A public event is constructed from an explicit field list; any field not named in the projector never leaves the machine. The do-not-publish list (no paths, no real document data, no schema/table names, no ports, no prompt contents, no routing thresholds) is satisfied structurally, not by review.

| Concern | Raw (private, never leaves the Mac mini) | Public feed |
|---|---|---|
| Document identity | doc_ref internal surrogate key | doc_hash = first 12 hex of HMAC-SHA256(doc_ref, per-install secret). Unlinkable without the key; stable across events so flows are traceable |
| Document class | real bin taxonomy label | fixed 8-value public enum: financial, medical, legal, correspondence, records, media, technical, other (static mapping kept privately) |
| Paths / filenames | never captured, even in raw | n/a |
| Prompts / answers | never captured (production docs are not benchmark queries; log token counts, not text) | n/a |
| Routing thresholds | confidence numeric | dropped; only reason_code enum and branch_taken survive |
| Model identity | exact Ollama tag / API model id | tier only (local_fast, local_analyst, cloud, rule_based) |
| Schema/table/ports | never in events | n/a |
| Timestamps | ms precision | truncated to the hour |
| Errors | full message string | boolean plus coarse class (timeout, model_error, other) |

Public event example (what the site's live viz consumes):

```json
{"schema_ver": "chiefos-public/1", "event_type": "agent_task", "ts": "2026-08-16T14:00Z",
 "cycle_id": "c-2026-08-16T14", "agent": "filing_clerk", "doc_hash": "9f3a1c07b2d4",
 "doc_class": "financial", "tier": "local_fast", "outcome_code": "filed",
 "tokens_in": 812, "tokens_out": 44, "latency_s": 1.8, "verdict": "provisional_pass"}
```

The projector is a ~150-line standalone script: reads the JSONL, applies the field whitelist + hash + enum map + time truncation, writes public-YYYY-MM-DD.jsonl, and pushes to the site's data pipeline (the publish-queue contract governs the site side). It must carry a unit test asserting that no output field outside the whitelist can ever appear - that test IS the pre-scrub the coordination contract demands. Aggregates for the viz can be computed site-side from the public feed or exported pre-aggregated; start with pre-aggregated daily rollups.

## 5. Effort and Rollout Order

| Phase | Work | Effort | Signal unlocked |
|---|---|---|---|
| 1. LLM call wrapper + JSONL writer | telemetry.py, wrap the LLM client(s), token extraction, system_prompt_tokens | ~half a day | Per-tier/per-purpose token totals, Layer 1, Layer 3 - most of AEQ's raw material from one choke point |
| 2. Cycle + task context managers | Two context managers into the orchestrator; docs_pending capture | ~2 hours | Per-agent/per-cycle attribution, Layer 2, first cut of coordination overhead |
| 3. Fork decisions | record_fork() at tier router, confidence gate, budget gate, degradation fallback, dedup accept | ~half a day | Spec 9.6 gate accounting, tier-mix analytics, the fork half of AEQ-L |
| 4. Outcome resolution | Emit at file/route/propose; hook the correction handler (piggyback on the Student); nightly confirmed_pass expiry job | ~half a day | The AEQ-L numerator. Without this everything else is denominator-only |
| 5. Postgres table + reconciliation | One migration, dual-write, nightly rollup-vs-events check | ~2 hours | Dashboard queries, durability redundancy |
| 6. OCR cascade events | JSON line from the Swift helper, forwarded by Python | ~2 hours | Cascade-stage economics; lowest AEQ urgency, hence last |
| 7. Public projector + rollups | Whitelist script + never-leak unit test + daily aggregate export | ~half a day | The bucketbranch.ai feed |

Total: roughly 2-3 focused days for a session that knows the codebase; phases 1-2 alone (under a day) already produce per-agent AEQ layer metrics worth publishing. Run phases 1-4 for two full weeks before trusting any AEQ-L number - the validation window makes the first fortnight's numerator structurally provisional. First publishable artifact: a phase0_raw.json-style flat export of one week of agent_task records (public projection), which existing AEQ tooling can consume nearly unmodified.

Caution for the implementing session: dry_run events are excluded from the AEQ-L numerator AND denominator by default (rehearsals are not outcomes; their tokens are safety spend, not architecture spend) - but keep them in the stream, because dry-run token cost is exactly the kind of spec 9.6 gate-overhead question AEQ-L exists to answer later.

## References

- AEQ/spec/AEQ_Specification_v1.1.md - canonical definitions (s4 layers, s9 AEQ-L, s9.6 forks, s11.5 gap)
- AEQ/runs/phase1_2026-07-24/phase0_raw.json - the record vocabulary this schema aligns with
- bucketbranch docs/SITE-COORDINATION-CONTRACT.md - the do-not-publish list the sanitization boundary is built against
- AgentSaaSy_EAM/whitepaper/ARCHITECTURE_NOTE_PreRegistered_Routing_2026-08-06.md - s7 defines the coordination-overhead experiment this telemetry must feed
