"""
EAM Agentic AI Demo Showcase
═══════════════════════════════════════════════════════════════════
"A Day in the Life of an AI-Powered City"

5-act demo that flows seamlessly from one agent to the next,
telling a continuous story of AI-powered enterprise asset management.

Acts:
  1. THE EARLY WARNING (6:00 AM)  — IoT Anomaly Detection
  2. THE SMART DISPATCHER (7:00 AM) — GIS Route Optimization
  3. THE STRATEGIC ADVISOR (9:00 AM) — Budget Scenario Planning
  4. THE COMMUNICATOR (10:00 AM) — Citizen Communication
  5. THE BIG PICTURE (4:00 PM) — Executive Summary

Usage:
  python demo_showcase.py                     # Full 5-act demo
  python demo_showcase.py --condensed         # Acts 1 + 2 + 5 (12 min)
  python demo_showcase.py --act 3             # Single act
  python demo_showcase.py --audience executive # Audience-tuned language
  python demo_showcase.py --list-acts         # Show available acts
  python demo_showcase.py --record FILE       # Live run, save model responses
  python demo_showcase.py --replay FILE       # Offline run from a saved file

Designed for live presentations to the platform CTO and stakeholders.
═══════════════════════════════════════════════════════════════════
"""

import argparse
import json
import os
import sys
import time
from datetime import date, datetime

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
            "which assets are at highest risk of failure. Diagnose the anomaly — is this "
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
            "— the goal is to reduce total drive time by matching skills to jobs and "
            "routing the closest qualified technician to the critical pump repair."
        ),
        "transition": (
            "\n    Routes are set, crews are rolling. But the Operations Director "
            "just walked in — can we afford to replace that pump, or do we keep repairing it?"
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
            "station serves 2,400 homes — those residents need to know what's coming..."
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
            "the compliance status? Generate a proactive communication plan — classify "
            "residents by impact tier and outline a multi-channel notification strategy "
            "(30-day notice, 7-day reminder, day-of alert)."
        ),
        "transition": (
            "\n    Citizens are informed, crews are optimized, the pump is scheduled. "
            "Let's zoom out — what did all of this look like across the whole system?"
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
        "transition": None,  # Final act — no transition
    },
]

# Condensed demo: Acts 1, 2, 5 (detection → action → results)
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
    print("   It's one intelligent layer that sits on top of the platform's")
    print('   existing platform — amplifying what your customers already have."')
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


def print_closing() -> None:
    """Print the closing statement."""
    print()
    print("  " + "═" * 66)
    print("  ═══ DEMO COMPLETE ═══")
    print("  " + "═" * 66)
    print()
    print('  "Everything you just saw runs on data that already exists in')
    print("   the platform — asset records, work orders, maintenance")
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
        audience: Audience type — 'technical', 'executive', or 'sales'.
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
    print(f"  Mode: {mode} ({act_count} acts) | Audience: {audience.upper()}")
    print(f"  City: {city}")
    print()

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
        ),
    )
    parser.add_argument(
        "--condensed", action="store_true",
        help="Run condensed demo (Acts 1, 2, 5 — 12 minutes)",
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

    run_demo(
        acts_to_run=acts_to_run,
        audience=args.audience,
        city=args.city,
        pause=args.pause,
        record_path=args.record,
        recording=recording,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Demo paused. Exiting gracefully.\n")
    except RecordingError as e:
        print(f"\n  Error: {e}\n", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"\n  Error: {e}\n")
        print("  Ensure OPENAI_API_KEY is set in .env and asset_data.csv exists.\n")
