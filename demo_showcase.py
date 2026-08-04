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

Designed for live presentations to the platform CTO and stakeholders.
═══════════════════════════════════════════════════════════════════
"""

import argparse
import sys
import time
from datetime import date

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
) -> None:
    """Run the full demo showcase.

    Args:
        acts_to_run: List of act numbers to run (default: all 5).
        audience: Audience type — 'technical', 'executive', or 'sales'.
        city: Demo city name.
        pause: Seconds to pause between acts for pacing.
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
    agent_llm = get_agent(demo_mode=True)
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
        execute_act(act, agent_llm, system_msg, pause=pause)

        # Transition to next act (skip for last act)
        if i < len(selected_acts) - 1:
            print_transition(act["transition"])
            time.sleep(pause)

    # Closing
    print_closing()


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

    args = parser.parse_args()

    if args.list_acts:
        list_acts()
        return

    # Determine which acts to run
    if args.act:
        acts_to_run = [args.act]
    elif args.condensed:
        acts_to_run = CONDENSED_ACTS
    else:
        acts_to_run = None  # All acts

    run_demo(
        acts_to_run=acts_to_run,
        audience=args.audience,
        city=args.city,
        pause=args.pause,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Demo paused. Exiting gracefully.\n")
    except Exception as e:
        print(f"\n  Error: {e}\n")
        print("  Ensure OPENAI_API_KEY is set in .env and asset_data.csv exists.\n")
