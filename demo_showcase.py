"""
EAM Agentic AI Demo Showcase
═══════════════════════════════════════════════════════════════════
"A Day in the Life of an AI-Powered City"

5-act demo that flows seamlessly from one agent to the next,
telling a continuous story of AI-powered enterprise asset management.

Acts:
  1. THE EARLY WARNING (6:00 AM) , IoT Anomaly Detection
  2. THE SMART DISPATCHER (7:00 AM), GIS Route Optimization
  3. THE STRATEGIC ADVISOR (9:00 AM), Budget Scenario Planning
  4. THE COMMUNICATOR (10:00 AM), Citizen Communication
  5. THE BIG PICTURE (4:00 PM), Executive Summary

Usage:
  python demo_showcase.py                     # Full 5-act demo
  python demo_showcase.py --condensed         # Acts 1 + 2 + 5 (12 min)
  python demo_showcase.py --act 3             # Single act
  python demo_showcase.py --audience executive # Audience-tuned language
  python demo_showcase.py --list-acts         # Show available acts
  python demo_showcase.py --record FILE       # Live run, save model responses
  python demo_showcase.py --replay FILE       # Offline run from a saved file
  python demo_showcase.py --ui PORT           # Live view at http://127.0.0.1:PORT

Designed for live presentations to the platform CTO and stakeholders.
═══════════════════════════════════════════════════════════════════
"""

import argparse
import errno
import http.server
import json
import os
import queue
import sys
import threading
import time
from datetime import date, datetime
from urllib.parse import urlparse

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from agent import (
    get_agent,
    get_demo_prompt,
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance,
    optimize_field_routes,
    plan_capital_strategy,
)

# ── Tool Registry ─────────────────────────────────────────────
# Must include ALL tools bound to the agent (currently 7)
TOOL_MAP = {
    "query_assets": query_assets,
    "analyze_asset_health": analyze_asset_health,
    "predict_failures": predict_failures,
    "calculate_tco": calculate_tco,
    "track_compliance": track_compliance,
    "optimize_field_routes": optimize_field_routes,
    "plan_capital_strategy": plan_capital_strategy,
}


# ── Act Definitions ───────────────────────────────────────────

ACTS = [
    {
        "number": 1,
        "title": "THE EARLY WARNING",
        "time": "6:00 AM",
        "agent": "IoT Anomaly Detection Agent",
        "query": (
            "A vibration sensor on Pump Station #7 (Sacramento River intake) spiked "
            "overnight. Analyze the asset health of pumps in the fleet and predict "
            "which assets are at highest risk of failure. Diagnose the anomaly, is this "
            "bearing degradation, seal failure, or cavitation? Estimate a failure window "
            "and generate a prioritized work order recommendation."
        ),
        "transition": (
            "\n    That work order just hit the queue. Now let's see what "
            "happens when the morning shift starts and the optimization kicks in..."
        ),
    },
    {
        "number": 2,
        "title": "THE SMART DISPATCHER",
        "time": "7:00 AM",
        "agent": "GIS Route Optimization Agent",
        "query": (
            "Morning shift begins. There are 48 work orders in the queue including "
            "the urgent Priority 2 pump station repair from overnight. Query the full "
            "asset portfolio to understand the geographic distribution and asset types. "
            "Analyze which assets need attention and help plan optimized field operations "
            ", the goal is to reduce total drive time by matching skills to jobs and "
            "routing the closest qualified technician to the critical pump repair."
        ),
        "transition": (
            "\n    Routes are set, crews are rolling. But the Operations Director "
            "just walked in, can we afford to replace that pump, or do we keep repairing it?"
        ),
    },
    {
        "number": 3,
        "title": "THE STRATEGIC ADVISOR",
        "time": "9:00 AM",
        "agent": "Budget Scenario Planning Agent",
        "query": (
            "The Operations Director asks: Pump Station #7 has had 4 repairs in 18 months. "
            "Should we replace it ($180K) or keep repairing ($12K per incident)? "
            "Calculate the total cost of ownership for all pumps over 5 years. "
            "Also analyze health trends to understand if this is an isolated issue or "
            "part of a fleet-wide pattern. Present a recommendation with financial scenarios."
        ),
        "transition": (
            "\n    The director approves the replacement for Q3 budget. But that pump "
            "station serves 2,400 homes, those residents need to know what's coming..."
        ),
    },
    {
        "number": 4,
        "title": "THE COMMUNICATOR",
        "time": "10:00 AM",
        "agent": "Citizen Communication Agent",
        "query": (
            "The pump station replacement is approved for Q3. Query the asset portfolio "
            "to understand the service territory and check compliance status for the "
            "affected infrastructure. How many assets are in the service area? What's "
            "the compliance status? Generate a proactive communication plan, classify "
            "residents by impact tier and outline a multi-channel notification strategy "
            "(30-day notice, 7-day reminder, day-of alert)."
        ),
        "transition": (
            "\n    Citizens are informed, crews are optimized, the pump is scheduled. "
            "Let's zoom out, what did all of this look like across the whole system?"
        ),
    },
    {
        "number": 5,
        "title": "THE BIG PICTURE",
        "time": "4:00 PM",
        "agent": "Predictive Maintenance / Asset Intelligence Agent",
        "query": (
            "End of day. Generate a comprehensive executive summary of today's AI-powered "
            "operations. Query the full asset portfolio, analyze fleet-wide health trends, "
            "predict failures over the next 90 days, calculate total cost of ownership "
            "across the fleet, and check compliance status for all assets. "
            "Synthesize everything into a boardroom-ready dashboard: what was prevented, "
            "what was optimized, what was planned, and what's on the horizon."
        ),
        "transition": None,  # Final act, no transition
    },
]

# Condensed demo: Acts 1, 2, 5 (detection to action to results)
CONDENSED_ACTS = [1, 2, 5]


# ── Display Helpers ───────────────────────────────────────────

def print_banner() -> None:
    """Print the opening demo banner."""
    today = date.today().strftime("%B %d, %Y")
    print()
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 70 + "║")
    print("║" + "  EAM AGENTIC AI DEMO SHOWCASE".center(70) + "║")
    print("║" + '  "A Day in the Life of an AI-Powered City"'.center(70) + "║")
    print("║" + f"  {today}".center(70) + "║")
    print("║" + " " * 70 + "║")
    print("╚" + "═" * 70 + "╝")
    print()
    print('  "What you\'re about to see isn\'t five separate products.')
    print("   It's one intelligent layer that sits on top of the platform")
    print('   your customers already run, amplifying what they already have."')
    print()


def print_act_header(act: dict) -> None:
    """Print a formatted act header with timestamp."""
    print()
    print("  " + "═" * 66)
    print(f"  ═══ ACT {act['number']}: {act['title']} ({act['time']}) ═══")
    print(f"  Agent: {act['agent']}")
    print("  " + "═" * 66)
    print()


def print_transition(text: str | None) -> None:
    """Print an inter-act transition with visual separator."""
    if text is None:
        return
    print()
    print("  " + "─" * 66)
    print(f"  {text.strip()}")
    print("  " + "─" * 66)


def print_tool_call(tool_name: str, tool_args: dict) -> None:
    """Print tool execution info during the demo."""
    print(f"    [Agent reasoning] Calling: {tool_name}")
    _emit("tool_call", tool=tool_name, args=tool_args)


def print_closing() -> None:
    """Print the closing statement."""
    print()
    print("  " + "═" * 66)
    print("  ═══ DEMO COMPLETE ═══")
    print("  " + "═" * 66)
    print()
    print('  "Everything you just saw runs on data that already exists in')
    print("   the platform, asset records, work orders, maintenance")
    print("   history, GIS coordinates, sensor feeds.")
    print()
    print("   We're not asking your customers to change anything about how")
    print("   they use the platform. We're adding an intelligence layer that makes")
    print('   their existing investment exponentially more valuable.')
    print()
    print("   NAMI AI helps users navigate the platform.")
    print('   These agents help the platform think for itself."')
    print()
    print("  " + "═" * 66)
    print()


# -- Record / Replay ------------------------------------------
# A recording is a JSON object, not a bare array, so it can grow new
# top-level metadata (and new per-call fields such as token usage)
# without breaking readers of an older file.
#
#   {
#     "schema_version": 2,
#     "recorded_at": "2026-08-25T09:00:00",
#     "acts": [1, 2, 3, 4, 5],
#     "audience": "technical",
#     "city": "Sacramento",
#     "model": "gpt-4o-mini",
#     "calls": [
#       {"act": 1, "content": "...", "tool_calls": [{"name": ..., "args": {...}, "id": "..."}],
#        "input_tokens": 1234, "output_tokens": 56},
#       ...
#     ]
#   }
#
# "calls" is in the order the model was actually invoked. Each entry carries
# only the fields execute_act() reads off a response (content, tool_calls),
# since a langchain AIMessage does not serialize to JSON directly, plus the
# token usage the provider reported for that call.
#
# Schema history:
#   1 - content and tool_calls only, no token usage, no model id.
#   2 - adds input_tokens/output_tokens per call and a top-level "model", so a
#       replay reports the same cost summary the live run printed.
# Version 1 files still replay: they simply have no usage to report.

RECORDING_SCHEMA_VERSION = 2


class RecordingError(Exception):
    """Raised when a recording file cannot be read or does not cover a run."""


class RecordedResponse:
    """Stand-in for an AIMessage during replay.

    Exposes exactly what execute_act() reads: .content and .tool_calls.
    """

    def __init__(self, content, tool_calls: list[dict]):
        self.content = content
        self.tool_calls = tool_calls


def _extract_call(response) -> dict:
    """Reduce a model response to the plain-dict form we can serialize."""
    return {
        "content": response.content,
        "tool_calls": [
            {
                "name": tool_call["name"],
                "args": tool_call["args"],
                "id": tool_call.get("id"),
            }
            for tool_call in (response.tool_calls or [])
        ],
    }


# -- Token usage and cost -------------------------------------
# Counts come from the provider, never from counting characters. LangChain
# normalizes them onto AIMessage.usage_metadata; older/other integrations
# only populate response_metadata['token_usage'], so both are read.


def _as_int(value) -> int:
    """Coerce a reported token count to int, treating anything odd as 0."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def extract_usage(response) -> dict | None:
    """Pull input/output token counts off a model response.

    Returns None when the response carried no usage at all, which is
    different from a response that reported zero.
    """
    usage_metadata = getattr(response, "usage_metadata", None)
    if isinstance(usage_metadata, dict) and usage_metadata:
        return {
            "input_tokens": _as_int(usage_metadata.get("input_tokens")),
            "output_tokens": _as_int(usage_metadata.get("output_tokens")),
        }

    metadata = getattr(response, "response_metadata", None) or {}
    token_usage = metadata.get("token_usage") or {}
    if token_usage:
        return {
            "input_tokens": _as_int(
                token_usage.get("prompt_tokens", token_usage.get("input_tokens"))
            ),
            "output_tokens": _as_int(
                token_usage.get("completion_tokens", token_usage.get("output_tokens"))
            ),
        }
    return None


def extract_model_name(response) -> str | None:
    """Read the model id the provider says answered this call."""
    metadata = getattr(response, "response_metadata", None) or {}
    model = metadata.get("model_name") or metadata.get("model")
    return model or None


class UsageMeter:
    """Running totals for one demo run: calls, tokens, and the model used."""

    def __init__(self):
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.calls_without_usage = 0
        self.model: str | None = None

    def add(self, usage: dict | None, model: str | None = None) -> None:
        self.calls += 1
        if usage is None:
            self.calls_without_usage += 1
        else:
            self.input_tokens += usage["input_tokens"]
            self.output_tokens += usage["output_tokens"]
        if model and self.model is None:
            self.model = model
        self._emit_totals()

    def _emit_totals(self) -> None:
        """Push the running totals to the UI. Skipped entirely without --ui.

        The cost is priced here rather than only at the end so the page can
        show it climbing, and it is only computed when someone is watching:
        estimate_cost() reads the rate file on every call.
        """
        if _UI is None:
            return
        cost, reason = estimate_cost(self)
        _emit(
            "usage",
            calls=self.calls,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            total_tokens=self.total_tokens,
            model=self.model,
            cost=cost,
            cost_reason=reason,
        )

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class MeteredLLM:
    """Wraps the live LLM and totals token usage across every invoke()."""

    def __init__(self, agent_llm):
        self._agent_llm = agent_llm
        self.current_act: int | None = None
        self.meter = UsageMeter()

    def invoke(self, messages):
        response = self._agent_llm.invoke(messages)
        usage = extract_usage(response)
        self.meter.add(usage, extract_model_name(response))
        self._on_response(response, usage)
        return response

    def _on_response(self, response, usage: dict | None) -> None:
        """Hook for subclasses. The plain metered wrapper keeps nothing."""


class RecordingLLM(MeteredLLM):
    """Meters the live LLM and also keeps every response, in order."""

    def __init__(self, agent_llm):
        super().__init__(agent_llm)
        self.calls: list[dict] = []

    def _on_response(self, response, usage: dict | None) -> None:
        entry = {"act": self.current_act}
        entry.update(_extract_call(response))
        if usage is not None:
            entry.update(usage)
        self.calls.append(entry)


class ReplayLLM:
    """Plays recorded responses back, one per invoke(), per act.

    Makes no network calls and builds no LLM client, so replay needs
    no API key. Token usage stored with each recorded call is metered
    back so a replay reports the cost of the run that produced it.
    """

    def __init__(self, calls_by_act: dict[int, list[dict]], model: str | None = None):
        self._calls_by_act = calls_by_act
        self._cursors: dict[int, int] = {}
        self.current_act: int | None = None
        self.meter = UsageMeter()
        self.meter.model = model

    def invoke(self, messages):
        act = self.current_act
        queue = self._calls_by_act.get(act, [])
        position = self._cursors.get(act, 0)
        if position >= len(queue):
            raise RecordingError(
                f"Recording ran out of responses for act {act} "
                f"(it holds {len(queue)}). Re-record with --record."
            )
        self._cursors[act] = position + 1
        call = queue[position]
        if "input_tokens" in call or "output_tokens" in call:
            usage = {
                "input_tokens": _as_int(call.get("input_tokens")),
                "output_tokens": _as_int(call.get("output_tokens")),
            }
        else:
            usage = None  # schema_version 1 recording: no usage was captured
        self.meter.add(usage)
        return RecordedResponse(call.get("content", ""), call.get("tool_calls") or [])


def set_current_act(agent_llm, act_number: int) -> None:
    """Tell a recording or replay wrapper which act is executing."""
    if isinstance(agent_llm, (MeteredLLM, ReplayLLM)):
        agent_llm.current_act = act_number


def load_recording(path: str) -> dict:
    """Read and shape-check a recording file. Raises RecordingError.

    Older files are accepted as they are: a schema_version 1 recording has
    no per-call token usage and no model id, so a replay of it reports the
    acts fine and reports usage as unavailable rather than failing.
    """
    if not os.path.isfile(path):
        raise RecordingError(f"Recording file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise RecordingError(f"Recording file is not valid JSON: {path} ({exc})")
    except OSError as exc:
        raise RecordingError(f"Cannot read recording file: {path} ({exc})")

    if not isinstance(data, dict) or not isinstance(data.get("calls"), list):
        raise RecordingError(
            f"Recording file has no 'calls' list: {path}. "
            "Re-record with --record."
        )
    return data


def index_calls_by_act(recording: dict) -> dict[int, list[dict]]:
    """Group recorded calls by act number, preserving call order."""
    calls_by_act: dict[int, list[dict]] = {}
    for call in recording["calls"]:
        calls_by_act.setdefault(call.get("act"), []).append(call)
    return calls_by_act


def recording_model(recording: dict) -> str | None:
    """Model id a recording was made with, if it recorded one."""
    model = recording.get("model")
    return model or None


def write_recording(path: str, calls: list[dict], metadata: dict) -> None:
    """Write the recording file as a JSON object with metadata plus calls."""
    payload = {"schema_version": RECORDING_SCHEMA_VERSION}
    payload.update(metadata)
    payload["calls"] = calls
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


# -- Pricing --------------------------------------------------
# Rates live in a JSON file, not in this code, because per-token prices go
# stale and a wrong dollar figure quoted to a customer is worse than no
# figure. If the file is missing, has no entry for the model, or has an
# entry nobody has filled in yet, the run prints token counts and says
# pricing is unavailable. There is no built-in fallback rate on purpose.

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PRICING_PATH = os.path.join(REPO_ROOT, "pricing", "model_rates.json")


def _short_path(path: str) -> str:
    """Repo-relative path when possible, for stable printed output."""
    try:
        return os.path.relpath(path, REPO_ROOT)
    except ValueError:
        return path


def load_model_rates(path: str) -> tuple[dict | None, str | None]:
    """Read the rate table.

    Returns (rates_by_model_id, reason_it_is_unavailable). Exactly one of
    the two is None.
    """
    shown = _short_path(path)
    if not os.path.isfile(path):
        return None, f"rates file {shown} is missing"
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        return None, f"rates file {shown} is not valid JSON ({exc})"
    except OSError as exc:
        return None, f"rates file {shown} cannot be read ({exc})"

    if not isinstance(data, dict):
        return None, f"rates file {shown} is not a JSON object"
    if isinstance(data.get("models"), dict):
        return data["models"], None
    return {k: v for k, v in data.items() if not k.startswith("_")}, None


def _rate(entry: dict, key: str) -> float | None:
    """A filled-in numeric rate, or None if it is null/blank/not a number."""
    value = entry.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def estimate_cost(meter: UsageMeter, pricing_path: str = PRICING_PATH):
    """Price a run's tokens.

    Returns (cost_in_usd, reason_it_is_unavailable). Exactly one is None.
    Never guesses a rate.
    """
    if meter.calls_without_usage and meter.total_tokens == 0:
        return None, "token usage was not reported for this run"
    if not meter.model:
        return None, "the model id for this run is unknown"

    rates, reason = load_model_rates(pricing_path)
    if rates is None:
        return None, reason

    entry = rates.get(meter.model)
    if not isinstance(entry, dict):
        shown = _short_path(pricing_path)
        return None, f"{shown} has no entry for {meter.model}"

    input_rate = _rate(entry, "input_per_million")
    output_rate = _rate(entry, "output_per_million")
    if input_rate is None or output_rate is None:
        shown = _short_path(pricing_path)
        return None, (
            f"rates for {meter.model} in {shown} are not filled in yet "
            "(a human must enter them from the provider's pricing page)"
        )

    cost = (
        meter.input_tokens / 1_000_000 * input_rate
        + meter.output_tokens / 1_000_000 * output_rate
    )
    return cost, None


def print_usage_summary(meter: UsageMeter, pricing_path: str = PRICING_PATH) -> None:
    """Print what the run consumed: calls, tokens, and cost if it is known."""
    print("  " + "=" * 66)
    print("  === RUN COST ===")
    print("  " + "=" * 66)
    print(f"  Model:           {meter.model or 'unknown'}")
    print(f"  Model calls:     {meter.calls:,}")
    print(f"  Input tokens:    {meter.input_tokens:,}")
    print(f"  Output tokens:   {meter.output_tokens:,}")
    print(f"  Total tokens:    {meter.total_tokens:,}")
    if meter.calls_without_usage:
        print(
            f"  Note:            {meter.calls_without_usage} of {meter.calls} calls "
            "reported no token usage (older recording, or the provider sent none)"
        )

    cost, reason = estimate_cost(meter, pricing_path)
    if cost is None:
        print(f"  Estimated cost:  not available: {reason}")
    else:
        rates, _ = load_model_rates(pricing_path)
        entry = (rates or {}).get(meter.model, {})
        verified_on = entry.get("verified_on") or "unknown date"
        print(f"  Estimated cost:  ${cost:,.4f} USD")
        print(f"  Rates verified:  {verified_on} ({_short_path(pricing_path)})")
    print("  " + "=" * 66)
    print()


# -- Live UI (--ui PORT) --------------------------------------
# Optional. Serves one self-contained page on 127.0.0.1 and streams run
# events to it over Server-Sent Events. Standard library only: http.server
# plus a thread, no new dependency and no websockets.
#
# Everything here is additive. With no --ui the module-level _UI stays None,
# _emit() returns immediately, and console output is exactly what it was.
# The hooks fire from print_tool_call(), UsageMeter.add(), execute_act() and
# run_demo(), all of which sit on the path a live run and a replayed run
# share, so --ui works the same either way (a replay needs no API key and
# makes no network call, and the UI does not change that).
#
# A slow or absent reader must never slow the demo down, so each connected
# client gets its own bounded queue and a full queue drops the event rather
# than blocking the act loop.

UI_LINGER_SECONDS = 3.0     # keep serving after the run so the last frame lands
UI_CLIENT_QUEUE_SIZE = 256  # per-client backlog before events are dropped
UI_HISTORY_LIMIT = 1000     # events replayed to a browser that connects late

UI_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AgentSaaSy Demo Showcase | Live Run</title>
<style>
  :root {
    --bg: #0a0e14;
    --bg2: #0f1420;
    --panel: #131a28;
    --panel2: #1a2336;
    --line: #24304a;
    --text: #e8edf5;
    --muted: #8b98b0;
    --accent: #4fd1c5;     /* teal - harness */
    --accent2: #7c9bff;    /* blue - agents */
    --accent3: #f6ad55;    /* amber - meters */
    --green: #48bb78;
    --yellow: #ecc94b;
    --red: #f56565;
    --mono: "SF Mono", "Fira Code", Consolas, monospace;
    --sans: -apple-system, "Segoe UI", Inter, Roboto, sans-serif;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background: var(--bg); color: var(--text); font-family: var(--sans); }
  .wrap { max-width: 1180px; margin: 0 auto; padding: 0 24px 40px; }

  /* ---------- NAV ---------- */
  nav {
    display:flex; align-items:center; justify-content:space-between;
    padding: 18px 0; border-bottom: 1px solid var(--line);
  }
  .logo { font-family: var(--mono); font-weight: 700; font-size: 18px; letter-spacing: .5px; }
  .logo span { color: var(--accent); }
  .status {
    font-family: var(--mono); font-size: 11px; letter-spacing: 1.5px;
    text-transform: uppercase; padding: 5px 12px; border-radius: 6px;
    border: 1px solid var(--line); color: var(--muted);
  }
  .status.ok { color: var(--green); border-color: var(--green); background: rgba(72,187,120,.12); }
  .status.warn { color: var(--yellow); border-color: var(--yellow); background: rgba(236,201,75,.12); }
  .status.done { color: var(--accent3); border-color: var(--accent3); background: rgba(246,173,85,.12); }

  /* ---------- HEADER ---------- */
  header { padding: 40px 0 26px; }
  .kicker {
    font-family: var(--mono); font-size: 12px; letter-spacing: 2px;
    color: var(--accent); text-transform: uppercase; margin-bottom: 12px;
  }
  h1 { font-size: clamp(26px, 4vw, 40px); line-height: 1.15; font-weight: 800; }
  h1 .grad {
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  .runmeta { margin-top: 14px; color: var(--muted); font-family: var(--mono); font-size: 13px; }

  /* ---------- LAYOUT ---------- */
  .grid { display:grid; grid-template-columns: 1fr 380px; gap: 18px; align-items:start; }
  @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
  .col { display:flex; flex-direction:column; gap: 14px; }
  .card { background: var(--panel); border:1px solid var(--line); border-radius:12px; padding:16px; }
  .card h3 {
    font-size: 12px; font-family: var(--mono); letter-spacing: 1.5px;
    text-transform: uppercase; color: var(--muted); margin-bottom: 12px;
  }
  .empty { font-size: 13px; color: #55637f; }

  /* ---------- ACTS ---------- */
  .act {
    border:1px solid var(--line); border-radius:10px; padding:12px 14px;
    margin-bottom:10px; background: var(--bg2); transition: all .25s;
  }
  .act:last-child { margin-bottom:0; }
  .act .top { display:flex; align-items:center; gap:10px; }
  .act .dot { width:9px; height:9px; border-radius:50%; background: var(--line); flex:none; }
  .act .no {
    font-family: var(--mono); font-size: 11px; color: var(--muted);
    border:1px solid var(--line); border-radius:5px; padding:2px 7px;
  }
  .act .name { font-size: 14px; font-weight: 700; }
  .act .clock { margin-left:auto; font-family: var(--mono); font-size: 11px; color: var(--muted); }
  .act .who { font-size: 12px; color: var(--muted); margin-top:6px; padding-left: 19px; }
  .act.running { border-color: var(--accent2); box-shadow: 0 0 0 1px rgba(124,155,255,.25); }
  .act.running .dot { background: var(--accent2); animation: blink 1.1s ease-in-out infinite; }
  .act.running .name { color: var(--accent2); }
  .act.done { border-color: var(--green); }
  .act.done .dot { background: var(--green); }
  @keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: .25; } }

  /* ---------- TOOLS ---------- */
  .tools { display:flex; flex-direction:column; gap:8px; }
  .tool {
    border:1px solid var(--line); border-radius:8px; padding:8px 10px;
    background: var(--bg2); transition: all .25s;
  }
  .tool .tn {
    font-family: var(--mono); font-size: 12px; color: var(--muted);
    display:flex; gap:8px; align-items:center;
  }
  .tool .count { margin-left:auto; font-size: 10.5px; color: var(--muted); }
  .tool .args {
    font-family: var(--mono); font-size: 10.5px; color: #55637f;
    margin-top:5px; word-break: break-word; display:none;
  }
  .tool.fired { border-color: var(--accent2); }
  .tool.fired .tn { color: var(--accent2); }
  .tool.fired .args { display:block; }
  .tool.lit { border-color: var(--accent); background: rgba(79,209,197,.14); }
  .tool.lit .tn { color: var(--accent); }

  /* ---------- METERS ---------- */
  .stats { display:grid; grid-template-columns: 1fr 1fr; gap:10px; }
  .stat { background: var(--bg2); border-radius:8px; padding:10px; }
  .stat .n { font-family: var(--mono); font-size: 20px; font-weight:700; color: var(--accent3); }
  .stat .l { font-size: 11px; color: var(--muted); margin-top:2px; }
  .modelline { margin-top:12px; font-family: var(--mono); font-size: 12px; color: var(--muted); }
  .modelline span { color: var(--text); }
  .costnote { margin-top:6px; font-size: 11.5px; color: #55637f; line-height:1.5; }

  /* ---------- LOG ---------- */
  #log {
    font-family: var(--mono); font-size: 11.5px; line-height: 1.7; height: 240px;
    overflow-y: auto; color: var(--muted);
  }
  #log .t { color: #55637f; }
  #log .ev-run { color: var(--accent); }
  #log .ev-act { color: var(--accent2); }
  #log .ev-tool { color: var(--accent3); }

  footer {
    border-top: 1px solid var(--line); padding: 24px 0 0; margin-top: 22px;
    color: var(--muted); font-size: 12.5px; display:flex;
    justify-content:space-between; flex-wrap:wrap; gap:12px;
  }
</style>
</head>
<body>

<div class="wrap">
  <nav>
    <div class="logo">bucketbranch<span>.ai</span></div>
    <div class="status" id="status">connecting</div>
  </nav>

  <header>
    <div class="kicker">EAM Agentic AI Demo Showcase</div>
    <h1>A Day in the Life of an <span class="grad">AI-Powered City</span></h1>
    <div class="runmeta" id="runmeta">waiting for the run to start</div>
  </header>

  <div class="grid">
    <div class="col">
      <div class="card">
        <h3>Acts</h3>
        <div id="acts"><div class="empty">The act list appears when the run starts.</div></div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <h3>Run Totals</h3>
        <div class="stats">
          <div class="stat"><div class="n" id="st-calls">0</div><div class="l">model calls</div></div>
          <div class="stat"><div class="n" id="st-cost">--</div><div class="l">estimated cost</div></div>
          <div class="stat"><div class="n" id="st-in">0</div><div class="l">input tokens</div></div>
          <div class="stat"><div class="n" id="st-out">0</div><div class="l">output tokens</div></div>
        </div>
        <div class="modelline">model: <span id="st-model">unknown</span></div>
        <div class="costnote" id="costnote"></div>
      </div>
      <div class="card">
        <h3>Tools</h3>
        <div id="tools" class="tools"><div class="empty">The tool registry appears when the run starts.</div></div>
      </div>
      <div class="card">
        <h3>Event Log</h3>
        <div id="log"></div>
      </div>
    </div>
  </div>

  <footer>
    <div>AgentSaaSy - Michael Valderrama | AI Agent Architect | Independent R&amp;D (c) 2026</div>
    <div>Served from this machine only. This page makes no outbound requests.</div>
  </footer>
</div>

<script>
/* =========================================================
   LIVE RUN VIEW
   One EventSource against /events. Every value on the page
   comes from the demo process, nothing is simulated here.
   ========================================================= */
(function () {
  var byId = function (id) { return document.getElementById(id); };
  var statusEl = byId('status');
  var logEl = byId('log');
  var actsEl = byId('acts');
  var toolsEl = byId('tools');
  var actRows = {};
  var toolRows = {};
  var toolCounts = {};
  var finished = false;
  var src;

  function setStatus(text, cls) {
    statusEl.textContent = text;
    statusEl.className = 'status' + (cls ? ' ' + cls : '');
  }

  function stamp() {
    return new Date().toTimeString().slice(0, 8);
  }

  function logLine(text, cls) {
    var row = document.createElement('div');
    var when = document.createElement('span');
    when.className = 't';
    when.textContent = stamp();
    var msg = document.createElement('span');
    msg.className = cls || '';
    msg.textContent = ' ' + text;
    row.appendChild(when);
    row.appendChild(msg);
    logEl.appendChild(row);
    while (logEl.children.length > 200) { logEl.removeChild(logEl.firstChild); }
    logEl.scrollTop = logEl.scrollHeight;
  }

  function num(value) {
    return Number(value || 0).toLocaleString();
  }

  /* Tool arguments are model output, so they are written with textContent
     and never as markup. */
  function argsText(args) {
    if (args === null || args === undefined) { return '(no arguments)'; }
    if (typeof args !== 'object') { return String(args); }
    var keys = Object.keys(args);
    if (!keys.length) { return '(no arguments)'; }
    var parts = keys.map(function (k) {
      var v = args[k];
      return k + '=' + (typeof v === 'string' ? v : JSON.stringify(v));
    });
    return parts.join('   ');
  }

  function renderActs(list) {
    actsEl.textContent = '';
    actRows = {};
    (list || []).forEach(function (a) {
      var row = document.createElement('div');
      row.className = 'act';
      var top = document.createElement('div');
      top.className = 'top';
      var dot = document.createElement('span');
      dot.className = 'dot';
      var no = document.createElement('span');
      no.className = 'no';
      no.textContent = 'ACT ' + a.number;
      var name = document.createElement('span');
      name.className = 'name';
      name.textContent = a.title;
      var clock = document.createElement('span');
      clock.className = 'clock';
      clock.textContent = a.time;
      top.appendChild(dot);
      top.appendChild(no);
      top.appendChild(name);
      top.appendChild(clock);
      var who = document.createElement('div');
      who.className = 'who';
      who.textContent = a.agent;
      row.appendChild(top);
      row.appendChild(who);
      actsEl.appendChild(row);
      actRows[a.number] = row;
    });
  }

  function renderTools(names) {
    toolsEl.textContent = '';
    toolRows = {};
    toolCounts = {};
    (names || []).forEach(function (n) {
      var row = document.createElement('div');
      row.className = 'tool';
      var tn = document.createElement('div');
      tn.className = 'tn';
      var label = document.createElement('span');
      label.textContent = n;
      var count = document.createElement('span');
      count.className = 'count';
      count.textContent = '0 calls';
      tn.appendChild(label);
      tn.appendChild(count);
      var args = document.createElement('div');
      args.className = 'args';
      row.appendChild(tn);
      row.appendChild(args);
      toolsEl.appendChild(row);
      toolRows[n] = { row: row, count: count, args: args };
      toolCounts[n] = 0;
    });
  }

  function setCost(cost, reason) {
    var value = byId('st-cost');
    var note = byId('costnote');
    if (cost === null || cost === undefined) {
      value.textContent = '--';
      note.textContent = reason ? 'estimated cost not available: ' + reason : '';
    } else {
      value.textContent = '$' + Number(cost).toFixed(4);
      note.textContent = '';
    }
  }

  var handlers = {
    run_start: function (e) {
      renderActs(e.acts);
      renderTools(e.tools);
      byId('runmeta').textContent =
        e.source + ' run   |   ' + e.mode + '   |   audience ' + e.audience +
        '   |   city ' + e.city + '   |   ' + ((e.acts || []).length) + ' act(s)';
      if (e.model) { byId('st-model').textContent = e.model; }
      setStatus(e.source === 'replay' ? 'replay running' : 'live run', 'ok');
      logLine('run started (' + e.source + ')', 'ev-run');
    },

    act_start: function (e) {
      var row = actRows[e.number];
      if (row) {
        row.classList.remove('done');
        row.classList.add('running');
      }
      logLine('act ' + e.number + ' ' + e.title + ' (' + e.time + ') - ' + e.agent, 'ev-act');
    },

    act_end: function (e) {
      var row = actRows[e.number];
      if (row) {
        row.classList.remove('running');
        row.classList.add('done');
      }
      logLine('act ' + e.number + ' complete', 'ev-act');
    },

    tool_call: function (e) {
      var text = argsText(e.args);
      var entry = toolRows[e.tool];
      if (entry) {
        toolCounts[e.tool] += 1;
        entry.count.textContent = toolCounts[e.tool] +
          (toolCounts[e.tool] === 1 ? ' call' : ' calls');
        entry.args.textContent = text;
        entry.row.classList.add('fired');
        entry.row.classList.add('lit');
        window.setTimeout(function () { entry.row.classList.remove('lit'); }, 900);
      }
      logLine(e.tool + '  ' + text, 'ev-tool');
    },

    usage: function (e) {
      byId('st-calls').textContent = num(e.calls);
      byId('st-in').textContent = num(e.input_tokens);
      byId('st-out').textContent = num(e.output_tokens);
      if (e.model) { byId('st-model').textContent = e.model; }
      setCost(e.cost, e.cost_reason);
    },

    run_end: function (e) {
      Object.keys(actRows).forEach(function (k) {
        actRows[k].classList.remove('running');
        actRows[k].classList.add('done');
      });
      if (e.model) { byId('st-model').textContent = e.model; }
      setCost(e.cost, e.cost_reason);
      setStatus('run complete', 'done');
      logLine('demo complete', 'ev-run');
      finished = true;
      if (src) { src.close(); }
    }
  };

  setStatus('connecting', '');
  src = new EventSource('/events');
  src.onopen = function () {
    if (!finished) { setStatus('connected', 'ok'); }
  };
  src.onerror = function () {
    if (!finished) { setStatus('waiting for the demo', 'warn'); }
  };
  src.onmessage = function (message) {
    var event;
    try {
      event = JSON.parse(message.data);
    } catch (err) {
      return;
    }
    var handler = handlers[event.type];
    if (handler) { handler(event); }
  };
})();
</script>
</body>
</html>
"""


class EventBus:
    """Fans run events out to every connected SSE client.

    Publishing never blocks: a client that is not draining its queue loses
    events instead of holding up the demo.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._clients: list[queue.Queue] = []
        self._history: list[dict] = []
        self.closed = False

    def subscribe(self):
        """Register a client. Returns its queue plus the events it missed."""
        client: queue.Queue = queue.Queue(maxsize=UI_CLIENT_QUEUE_SIZE)
        with self._lock:
            backlog = list(self._history)
            self._clients.append(client)
        return client, backlog

    def unsubscribe(self, client) -> None:
        with self._lock:
            if client in self._clients:
                self._clients.remove(client)

    def publish(self, event: dict) -> None:
        with self._lock:
            self._history.append(event)
            overflow = len(self._history) - UI_HISTORY_LIMIT
            if overflow > 0:
                del self._history[:overflow]
            clients = list(self._clients)
        for client in clients:
            try:
                client.put_nowait(event)
            except queue.Full:
                pass  # a stalled browser must not back-pressure the run


class _UIServer(http.server.ThreadingHTTPServer):
    """Threaded server whose handler threads never keep the process alive."""

    daemon_threads = True


def make_ui_handler(bus: EventBus):
    """Build a request handler bound to one event bus."""

    class UIRequestHandler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self):
            path = urlparse(self.path).path
            if path in ("/", "/index.html"):
                self._serve_page()
            elif path == "/events":
                self._serve_events()
            else:
                self._serve_missing()

        def log_message(self, fmt, *args):
            """Silence the stdlib access log. The demo owns the terminal."""

        def _serve_page(self):
            body = UI_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                self.wfile.write(body)
            except OSError:
                pass  # reader went away mid-write

        def _serve_missing(self):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def _serve_events(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True

            client, backlog = bus.subscribe()
            try:
                for event in backlog:
                    self._write_event(event)
                while True:
                    try:
                        event = client.get(timeout=1.0)
                    except queue.Empty:
                        # Comment frame: keeps the connection warm and gives
                        # the loop a chance to notice the run is over.
                        self.wfile.write(b": keep-alive\n\n")
                        self.wfile.flush()
                        if bus.closed:
                            break
                        continue
                    self._write_event(event)
            except (OSError, ValueError):
                pass  # tab closed, or the server is shutting down
            finally:
                bus.unsubscribe(client)

        def _write_event(self, event: dict) -> None:
            payload = json.dumps(event, default=str)
            self.wfile.write(("data: " + payload + "\n\n").encode("utf-8"))
            self.wfile.flush()

    return UIRequestHandler


class DemoUI:
    """Background HTTP server streaming one run to one local page."""

    def __init__(self, port: int):
        self.port = port
        self.bus = EventBus()
        self._server = _UIServer(("127.0.0.1", port), make_ui_handler(self.bus))
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name="demo-ui",
            daemon=True,
        )

    def start(self) -> None:
        self._thread.start()

    def emit(self, event_type: str, **fields) -> None:
        event = {"type": event_type}
        event.update(fields)
        self.bus.publish(event)

    def close(self, linger: float = UI_LINGER_SECONDS) -> None:
        """Stop serving. Lingers first so the last events reach the page."""
        if linger > 0:
            time.sleep(linger)
        self.bus.closed = True
        self._server.shutdown()
        self._server.server_close()


# Set by main() when --ui is passed, and left None otherwise. A module-level
# handle keeps the hooks free of plumbing: print_tool_call() and
# UsageMeter.add() are called from places that cannot grow a new argument
# without changing behavior for callers that never asked for a UI.
_UI: DemoUI | None = None


def _emit(event_type: str, **fields) -> None:
    """Publish one run event to the UI. Does nothing unless --ui is on."""
    if _UI is not None:
        _UI.emit(event_type, **fields)


def start_ui(port: int) -> DemoUI | None:
    """Start the UI server, or report why it could not start and carry on.

    Never raises: a demo in front of an audience does not stop because a
    port is busy.
    """
    try:
        ui = DemoUI(port)
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            detail = f"port {port} is in use"
        else:
            detail = f"port {port} could not be bound ({exc})"
        print(f"  UI unavailable: {detail}. Continuing without the UI.")
        return None
    except (OverflowError, ValueError) as exc:
        print(f"  UI unavailable: port {port} is not usable ({exc}). "
              "Continuing without the UI.")
        return None

    ui.start()
    print(f"  UI live at http://127.0.0.1:{port}")
    return ui


# ── Core Demo Engine ──────────────────────────────────────────

def execute_act(
    act: dict,
    agent_llm,
    system_msg: SystemMessage,
    pause: float = 1.0,
) -> None:
    """Execute a single act of the demo showcase.

    Args:
        act: Act definition dict from ACTS list.
        agent_llm: LLM with bound tools.
        system_msg: System message with demo master prompt.
        pause: Seconds to pause between steps for dramatic pacing.
    """
    print_act_header(act)
    _emit(
        "act_start",
        number=act["number"],
        title=act["title"],
        time=act["time"],
        agent=act["agent"],
    )

    # Build message chain for this act
    messages = [system_msg, HumanMessage(content=act["query"])]
    response = agent_llm.invoke(messages)

    iteration = 0
    max_iterations = 5

    while response.tool_calls and iteration < max_iterations:
        iteration += 1
        messages.append(response)

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print_tool_call(tool_name, tool_args)
            time.sleep(pause * 0.3)  # Brief pause for readability

            tool_func = TOOL_MAP[tool_name]
            result = tool_func.invoke(tool_args)

            messages.append(
                ToolMessage(content=result, tool_call_id=tool_call["id"])
            )

        response = agent_llm.invoke(messages)

    # Display the agent's synthesized response
    if response.content:
        print()
        print(response.content)

    _emit("act_end", number=act["number"])
    time.sleep(pause)


def run_demo(
    acts_to_run: list[int] | None = None,
    audience: str = "technical",
    city: str = "Sacramento",
    pause: float = 1.5,
    record_path: str | None = None,
    recording: dict | None = None,
) -> None:
    """Run the full demo showcase.

    Args:
        acts_to_run: List of act numbers to run (default: all 5).
        audience: Audience type, 'technical', 'executive', or 'sales'.
        city: Demo city name.
        pause: Seconds to pause between acts for pacing.
        record_path: If set, run live and write every model response here.
        recording: If set, replay from this loaded recording instead of
            calling a model. No LLM client is built.
    """
    # Filter acts
    if acts_to_run is None:
        selected_acts = ACTS
    else:
        selected_acts = [a for a in ACTS if a["number"] in acts_to_run]
        if not selected_acts:
            print(f"No acts found matching: {acts_to_run}")
            return

    # Initialize
    if recording is not None:
        calls_by_act = index_calls_by_act(recording)
        missing = [a["number"] for a in selected_acts if not calls_by_act.get(a["number"])]
        if missing:
            raise RecordingError(
                "Recording holds no responses for act(s): "
                + ", ".join(str(n) for n in missing)
                + ". Re-record with --record, or run the acts it covers: "
                + ", ".join(str(n) for n in sorted(k for k in calls_by_act if k is not None))
            )
        agent_llm = ReplayLLM(calls_by_act, model=recording_model(recording))
    else:
        live_llm = get_agent(demo_mode=True)
        if record_path is not None:
            agent_llm = RecordingLLM(live_llm)
        else:
            agent_llm = MeteredLLM(live_llm)

    demo_prompt = get_demo_prompt(
        city_name=city,
        audience_type=audience,
    )
    system_msg = SystemMessage(content=demo_prompt)

    # Opening
    print_banner()

    act_count = len(selected_acts)
    mode = "CONDENSED" if act_count < 5 else "FULL"
    print(f"  Mode: {mode} ({act_count} act{'' if act_count == 1 else 's'})"
          f" | Audience: {audience.upper()}")
    print(f"  City: {city}")
    print()

    _emit(
        "run_start",
        acts=[
            {key: act[key] for key in ("number", "title", "time", "agent")}
            for act in selected_acts
        ],
        tools=list(TOOL_MAP),
        mode=mode,
        audience=audience,
        city=city,
        source="replay" if recording is not None else "live",
        model=agent_llm.meter.model,
    )

    # Execute each act
    for i, act in enumerate(selected_acts):
        set_current_act(agent_llm, act["number"])
        execute_act(act, agent_llm, system_msg, pause=pause)

        # Transition to next act (skip for last act)
        if i < len(selected_acts) - 1:
            print_transition(act["transition"])
            time.sleep(pause)

    # Closing
    print_closing()
    print_usage_summary(agent_llm.meter)

    if _UI is not None:
        cost, cost_reason = estimate_cost(agent_llm.meter)
        _emit(
            "run_end",
            calls=agent_llm.meter.calls,
            input_tokens=agent_llm.meter.input_tokens,
            output_tokens=agent_llm.meter.output_tokens,
            total_tokens=agent_llm.meter.total_tokens,
            model=agent_llm.meter.model,
            cost=cost,
            cost_reason=cost_reason,
        )

    if record_path is not None:
        write_recording(
            record_path,
            agent_llm.calls,
            {
                "recorded_at": datetime.now().isoformat(timespec="seconds"),
                "acts": [a["number"] for a in selected_acts],
                "audience": audience,
                "city": city,
                "model": agent_llm.meter.model,
            },
        )
        print(f"  Recorded {len(agent_llm.calls)} model responses to {record_path}")
        print()


def list_acts() -> None:
    """Print available acts and their descriptions."""
    print()
    print("  Available Demo Acts:")
    print("  " + "─" * 50)
    for act in ACTS:
        print(f"    Act {act['number']}: {act['title']} ({act['time']})")
        print(f"           {act['agent']}")
    print()
    print("  Run options:")
    print("    --condensed      Acts 1, 2, 5 (12 min)")
    print("    --act N          Single act")
    print("    (default)        Full 5-act demo (20-25 min)")
    print()


# ── CLI ───────────────────────────────────────────────────────

def main() -> None:
    """CLI entry point for the demo showcase."""
    parser = argparse.ArgumentParser(
        description="EAM Agentic AI Demo Showcase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python demo_showcase.py                      # Full demo\n"
            "  python demo_showcase.py --condensed          # Quick demo\n"
            "  python demo_showcase.py --act 3              # Budget scenario only\n"
            "  python demo_showcase.py --audience executive  # Executive language\n"
            "  python demo_showcase.py --record take1.json  # Live run, saved\n"
            "  python demo_showcase.py --replay take1.json  # Offline, no API key\n"
            "  python demo_showcase.py --ui 8765            # Live view in a browser\n"
        ),
    )
    parser.add_argument(
        "--condensed", action="store_true",
        help="Run condensed demo (Acts 1, 2, 5, 12 minutes)",
    )
    parser.add_argument(
        "--act", type=int, choices=[1, 2, 3, 4, 5],
        help="Run a single act (1-5)",
    )
    parser.add_argument(
        "--audience", default="technical",
        choices=["technical", "executive", "sales"],
        help="Audience type for language tuning (default: technical)",
    )
    parser.add_argument(
        "--city", default="Sacramento",
        help="Demo city name (default: Sacramento)",
    )
    parser.add_argument(
        "--pause", type=float, default=1.5,
        help="Pause between acts in seconds (default: 1.5)",
    )
    parser.add_argument(
        "--list-acts", action="store_true",
        help="List available acts and exit",
    )
    parser.add_argument(
        "--record", type=str, metavar="PATH",
        help="Run live and write every model response to PATH (JSON)",
    )
    parser.add_argument(
        "--replay", type=str, metavar="PATH",
        help="Replay a recorded run from PATH: no network, no API key",
    )
    parser.add_argument(
        "--ui", type=int, metavar="PORT",
        help=(
            "Serve a live view of the run at http://127.0.0.1:PORT. "
            "PORT is required; there is no default. Works with --replay."
        ),
    )

    args = parser.parse_args()

    if args.list_acts:
        list_acts()
        return

    if args.record and args.replay:
        print(
            "  Error: --record and --replay cannot be used together. "
            "Pick one: record a live run, or replay a recorded one.",
            file=sys.stderr,
        )
        sys.exit(2)

    recording = None
    if args.replay:
        try:
            recording = load_recording(args.replay)
        except RecordingError as exc:
            print(f"  Error: {exc}", file=sys.stderr)
            sys.exit(2)

    # Determine which acts to run
    if args.act:
        acts_to_run = [args.act]
    elif args.condensed:
        acts_to_run = CONDENSED_ACTS
    elif recording is not None and isinstance(recording.get("acts"), list) and recording["acts"]:
        # A bare --replay runs exactly the acts the recording covers, so a
        # one-act take does not fail asking for the other four.
        acts_to_run = list(recording["acts"])
    else:
        acts_to_run = None  # All acts

    global _UI
    if args.ui is not None:
        _UI = start_ui(args.ui)

    completed = False
    try:
        run_demo(
            acts_to_run=acts_to_run,
            audience=args.audience,
            city=args.city,
            pause=args.pause,
            record_path=args.record,
            recording=recording,
        )
        completed = True
    finally:
        if _UI is not None:
            # Linger only on a clean finish: on the way out of an error the
            # page has nothing left to receive.
            _UI.close(UI_LINGER_SECONDS if completed else 0.0)
            _UI = None


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Demo paused. Exiting gracefully.\n")
    except RecordingError as e:
        print(f"\n  Error: {e}\n", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        # Exit non-zero so a run that died partway cannot be mistaken for a
        # success. write_recording() is only reached after every selected act
        # finishes, so a run that lands here leaves no --record file behind: a
        # partial recording would replay later as though it were a real run.
        print(f"\n  Error: {e}\n", file=sys.stderr)
        print("  Ensure OPENAI_API_KEY is set in .env and asset_data.csv exists.\n",
              file=sys.stderr)
        sys.exit(1)
