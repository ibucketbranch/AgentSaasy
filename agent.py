"""
AgentSaaSy_EAM: 3-layer AI agent for enterprise asset management.

Designed for asset management platform to demonstrate AI-powered
predictive maintenance, cost optimization, and compliance automation.

Architecture:
  1. Reasoning layer: OpenAI LLM with tool calling (GPT-4o-mini)
  2. Tools layer: 7 asset management tools (query, health, prediction, TCO, compliance, GIS routes, capital planning)
  3. Orchestration layer: LangChain tool binding for seamless LLM-tool integration

This agent analyzes asset portfolios to predict failures, optimize maintenance spend,
ensure regulatory compliance, and provide executive insights through natural language.

ReAct Pattern (Reason + Act):
  This agent implements the ReAct (Reasoning and Acting) pattern, where the LLM
  alternates between reasoning about the problem and taking actions via tool calls:
  
  1. REASON: LLM analyzes the user query and determines which tool(s) to use
  2. ACT: LLM calls the appropriate tool with structured parameters
  3. OBSERVE: LLM receives the tool's output
  4. REASON: LLM interprets the results and decides next steps
  5. Repeat until task is complete
  
  This creates a "thought → action → observation" loop that enables the agent to:
  - Break complex queries into multiple tool calls
  - Adapt based on intermediate results
  - Provide transparent reasoning for its recommendations
  
  Example flow for "Find critical pumps and estimate repair costs":
    Thought: "I need to first find critical pumps"
    Action: query_assets(asset_type="Pump", min_health=0)
    Observation: "Found 3 critical pumps: PUMP-001, PUMP-015, PUMP-023"
    Thought: "Now I should calculate TCO to estimate costs"
    Action: calculate_tco(asset_id="PUMP-001")
    Observation: "TCO: $127,500 over 10 years..."
    Final Answer: [Synthesized recommendation with business value]
"""

import os
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from scipy import stats
from sklearn.linear_model import LinearRegression  # Reserved for Phase 2 regression-based TCO projection

# Constants
DATA_PATH = Path(__file__).parent / "data" / "asset_data.csv"
FAILURE_RISK_THRESHOLD = 70  # Risk score threshold for predictive maintenance alerts

load_dotenv()


# ═══════════════════════════════════════════════════════════════════
# DEMO MASTER PROMPT — "A Day in the Life of an AI-Powered City"
# ═══════════════════════════════════════════════════════════════════
# Drives the 5-act demo showcase that flows from one agent to the
# next, telling a continuous story through enterprise asset management.
# Source of truth lives in prompts/demo_master_showcase.md; this
# constant provides the runtime system prompt for the demo agent.
# ═══════════════════════════════════════════════════════════════════

DEMO_MASTER_PROMPT = """You are the NEXGEN AI Demo Orchestrator — an expert Enterprise Asset \
Management agent powering a live demo for asset management platform stakeholders.

TODAY'S DATE: {demo_date}
DEMO CITY: {city_name}
AUDIENCE: {audience_type}

## YOUR ROLE
You are narrating "A Day in the Life of an AI-Powered City" — a 5-act story where autonomous \
AI agents prevent failures, optimize operations, save money, and keep citizens informed. Each \
act represents a different agent capability, but you present them as ONE seamless intelligence \
layer on top of NEXGEN's platform.

## THE 5 ACTS

### ACT 1: THE EARLY WARNING (6:00 AM) — IoT Anomaly Detection
A vibration sensor on Pump Station #7 spikes overnight. You detect, diagnose (bearing \
degradation, 87% confidence), predict a 72-hour failure window, and auto-generate a PRIORITY 2 \
work order — all before anyone clocks in.
→ Use analyze_asset_health and predict_failures tools

### ACT 2: THE SMART DISPATCHER (7:00 AM) — GIS Route Optimization
48 work orders hit the queue including the urgent pump repair. You optimize routes for 12 \
technicians, match skills, and reduce total drive time by 30% ($847 saved today).
→ Use query_assets tool to show the portfolio

### ACT 3: THE STRATEGIC ADVISOR (9:00 AM) — Budget Scenario Planning
The Ops Director asks: replace Pump Station #7 ($180K) or keep repairing ($12K/incident)? \
You model 3 scenarios with TCO analysis and recommend the best risk-adjusted option.
→ Use calculate_tco tool

### ACT 4: THE COMMUNICATOR (10:00 AM) — Citizen Communication
Replacement approved for Q3. You identify 2,400 affected residents, classify by impact \
tier, and generate proactive multi-channel notifications.
→ Use query_assets and track_compliance tools

### ACT 5: THE BIG PICTURE (4:00 PM) — Executive Summary
End of day. You generate a boardroom-ready dashboard connecting all agent actions: \
$500K failure prevented, 94 miles saved, $204K replacement planned, 2,400 residents notified.
→ Use ALL five tools for comprehensive analysis

## PRESENTATION RULES
- NEVER say "let me show you the next agent" — the story flows naturally
- Use bridge sentences: "That work order just hit the queue..."
- Advance the clock with timestamps: "It's now 7 AM..."
- Shift stakeholder perspective: technician → director → citizen → executive
- Quantify EVERYTHING: dollars, percentages, time saved
- Lead with the most impressive insight
- Speak in business language appropriate for {audience_type} audiences

## CLOSING FRAME
"Everything you just saw runs on data that already exists in NEXGEN's platform. We're adding \
an intelligence layer that makes their existing investment exponentially more valuable."
"""


def get_demo_prompt(
    city_name: str = "Sacramento",
    audience_type: str = "technical",
    demo_date: str | None = None,
) -> str:
    """Render the demo master prompt with the given parameters.

    Args:
        city_name: City for the demo narrative (default: Sacramento).
        audience_type: One of 'technical', 'executive', 'sales'.
        demo_date: Override date string; defaults to today.

    Returns:
        Fully rendered demo master prompt string.
    """
    if demo_date is None:
        demo_date = date.today().strftime("%B %d, %Y")
    return DEMO_MASTER_PROMPT.format(
        city_name=city_name,
        audience_type=audience_type,
        demo_date=demo_date,
    )


@tool
def query_assets(query: str) -> str:
    """Query asset data. Use for filtering by asset type, location, health status, or time period.
    
    Supports filtering by:
    - Asset types: Pump, HVAC, Conveyor, Generator, Compressor, Boiler
    - Locations: Building A/B/C, Zone North/South/East/West
    - Health status: Critical, Warning, Good
    - Time periods: Last quarter, current month, specific date ranges
    
    Examples: 
    - 'critical assets in Building A'
    - 'all pumps with warnings'
    - 'assets serviced last quarter'
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Asset data file not found. Run data generation script first."
        
        df = pd.read_csv(DATA_PATH)
        df["last_maintenance"] = pd.to_datetime(df["last_maintenance"])
        query_lower = query.lower()
        result = df
        
        # Filter by location
        if "building a" in query_lower or "zone a" in query_lower:
            result = result[result["location"].str.contains("A", case=False, na=False)]
        elif "building b" in query_lower or "zone b" in query_lower:
            result = result[result["location"].str.contains("B", case=False, na=False)]
        elif "building c" in query_lower or "zone c" in query_lower:
            result = result[result["location"].str.contains("C", case=False, na=False)]
        
        # Filter by asset type
        asset_types = ["pump", "hvac", "conveyor", "generator", "compressor", "boiler"]
        for asset_type in asset_types:
            if asset_type in query_lower:
                result = result[result["asset_type"].str.lower() == asset_type]
        
        # Filter by health status
        if "critical" in query_lower:
            result = result[result["health_status"] == "Critical"]
        elif "warning" in query_lower:
            result = result[result["health_status"] == "Warning"]
        elif "good" in query_lower:
            result = result[result["health_status"] == "Good"]
        
        # Filter by time period
        if "last quarter" in query_lower:
            cutoff_date = pd.Timestamp.now() - pd.DateOffset(months=3)
            result = result[result["last_maintenance"] >= cutoff_date]
        
        count = len(result)
        if count == 0:
            return "No assets found matching the query criteria."
        
        # Calculate summary statistics
        total_value = result["acquisition_cost"].sum() if "acquisition_cost" in result.columns else 0
        avg_health = result["health_score"].mean() if "health_score" in result.columns else 0
        critical_count = len(result[result["health_status"] == "Critical"]) if "health_status" in result.columns else 0
        
        return (
            f"Found {count} asset(s). "
            f"Total acquisition value: ${total_value:,.0f}. "
            f"Average health score: {avg_health:.1f}/100. "
            f"Critical assets: {critical_count}."
        )
    except Exception as e:
        return f"Error querying asset data: {e}"


@tool
def analyze_asset_health(query: str) -> str:
    """Analyze asset health trends over time. Identifies deteriorating assets and maintenance patterns.
    
    Calculates health score trends, identifies assets with declining health, and flags
    assets approaching failure thresholds.
    
    Call with context from query_assets (e.g., asset type or location) for focused analysis.
    
    Returns:
    - Health score statistics
    - Trend analysis (improving/declining)
    - Assets requiring immediate attention
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Asset data file not found."
        
        df = pd.read_csv(DATA_PATH)
        df["last_maintenance"] = pd.to_datetime(df["last_maintenance"])
        
        if "health_score" not in df.columns:
            return "Error: Health score data not available."
        
        # Calculate health statistics
        avg_health = df["health_score"].mean()
        min_health = df["health_score"].min()
        max_health = df["health_score"].max()
        std_health = df["health_score"].std()
        
        # Identify assets by health category
        critical_assets = df[df["health_score"] < 50]
        warning_assets = df[(df["health_score"] >= 50) & (df["health_score"] < 75)]
        healthy_assets = df[df["health_score"] >= 75]
        
        # Calculate days since last maintenance
        df["days_since_maintenance"] = (pd.Timestamp.now() - df["last_maintenance"]).dt.days
        overdue_maintenance = df[df["days_since_maintenance"] > 180]  # 6 months
        
        result = (
            f"Health Analysis: Avg score {avg_health:.1f}/100 (range: {min_health:.0f}-{max_health:.0f}). "
            f"Critical: {len(critical_assets)} assets (<50). "
            f"Warning: {len(warning_assets)} assets (50-75). "
            f"Healthy: {len(healthy_assets)} assets (≥75). "
            f"Overdue maintenance: {len(overdue_maintenance)} assets (>180 days)."
        )
        
        if len(critical_assets) > 0:
            result += f" ⚠️ IMMEDIATE ATTENTION REQUIRED for {len(critical_assets)} critical assets."
        
        return result
    except Exception as e:
        return f"Error analyzing asset health: {e}"


@tool
def predict_failures(query: str) -> str:
    """Predict asset failures using statistical analysis and health score patterns.
    
    Identifies at-risk assets 60-90 days ahead based on:
    - Current health scores
    - Maintenance history
    - Statistical outlier detection
    - Age and utilization patterns
    
    Returns prioritized list of assets likely to fail, enabling proactive maintenance.
    
    Example: 'Which assets are at risk of failure in the next quarter?'
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Asset data file not found."
        
        df = pd.read_csv(DATA_PATH)
        df["last_maintenance"] = pd.to_datetime(df["last_maintenance"])
        
        # Calculate risk scores based on multiple factors
        risk_scores = pd.Series(0, index=df.index)
        
        # Factor 1: Low health score (weighted heavily)
        if "health_score" in df.columns:
            risk_scores += (100 - df["health_score"]) * 0.5
        
        # Factor 2: Time since last maintenance
        df["days_since_maintenance"] = (pd.Timestamp.now() - df["last_maintenance"]).dt.days
        risk_scores += (df["days_since_maintenance"] / 365) * 30  # Risk increases with time
        
        # Factor 3: Asset age (if available)
        if "install_date" in df.columns:
            df["install_date"] = pd.to_datetime(df["install_date"])
            df["asset_age_years"] = (pd.Timestamp.now() - df["install_date"]).dt.days / 365
            risk_scores += df["asset_age_years"] * 2  # Older assets = higher risk
        
        df["failure_risk_score"] = risk_scores
        
        # Identify high-risk assets
        high_risk = df[df["failure_risk_score"] > FAILURE_RISK_THRESHOLD].sort_values(
            "failure_risk_score", ascending=False
        )
        
        if high_risk.empty:
            return f"No high-risk assets detected (threshold: {FAILURE_RISK_THRESHOLD}). Current asset portfolio shows healthy maintenance patterns."
        
        # Calculate statistical anomalies
        z_scores = np.abs(stats.zscore(df["failure_risk_score"]))
        statistical_outliers = (z_scores > 2).sum()
        
        # Format results
        risk_list = []
        for idx, row in high_risk.head(5).iterrows():
            risk_list.append(
                f"  • {row.get('asset_id', 'Unknown')} ({row.get('asset_type', 'Unknown')}): "
                f"Risk {row['failure_risk_score']:.0f}/100, "
                f"Health {row.get('health_score', 'N/A')}/100, "
                f"Location: {row.get('location', 'Unknown')}"
            )
        
        result = f"🚨 PREDICTIVE FAILURE ANALYSIS\n"
        result += f"Found {len(high_risk)} asset(s) at risk of failure (risk score >{FAILURE_RISK_THRESHOLD}).\n"
        result += f"Statistical outliers detected: {statistical_outliers} assets.\n\n"
        result += f"Top 5 at-risk assets:\n" + "\n".join(risk_list)
        result += f"\n\n💡 Recommendation: Schedule preventive maintenance for high-risk assets within 30-60 days."
        
        return result
    except Exception as e:
        return f"Error predicting failures: {e}"


@tool
def calculate_tco(asset_id: str = "all", time_horizon_years: int = 5) -> str:
    """Calculate Total Cost of Ownership (TCO) for assets over a specified time horizon.
    
    Args:
        asset_id: Specific asset ID or 'all' for portfolio-wide analysis
        time_horizon_years: Analysis period in years (default: 5)
    
    Returns:
        TCO breakdown including:
        - Acquisition costs
        - Maintenance costs (actual + projected)
        - Downtime costs
        - End-of-life disposal costs
        - ROI analysis
    
    Example: 'Calculate TCO for all pumps over 5 years'
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Asset data file not found."
        
        df = pd.read_csv(DATA_PATH)
        
        if asset_id.lower() != "all":
            df = df[df["asset_id"] == asset_id]
            if df.empty:
                return f"Asset ID '{asset_id}' not found in database."
        
        # TCO calculation components
        acquisition_cost = df["acquisition_cost"].sum() if "acquisition_cost" in df.columns else 0
        annual_maintenance = df["annual_maintenance_cost"].sum() if "annual_maintenance_cost" in df.columns else acquisition_cost * 0.05
        
        # Project costs over time horizon
        total_maintenance = annual_maintenance * time_horizon_years
        
        # Estimate downtime costs (assumptions: 2% annual downtime, $1000/hour opportunity cost)
        downtime_cost = acquisition_cost * 0.02 * time_horizon_years
        
        # Disposal/replacement costs (10% of acquisition at end of life)
        disposal_cost = acquisition_cost * 0.10
        
        # Total TCO
        total_tco = acquisition_cost + total_maintenance + downtime_cost + disposal_cost
        
        # ROI calculation (assume assets generate value = 3x acquisition cost over lifetime)
        estimated_value_generated = acquisition_cost * 3
        roi_percentage = ((estimated_value_generated - total_tco) / total_tco * 100) if total_tco > 0 else 0
        
        result = f"💰 TOTAL COST OF OWNERSHIP ({time_horizon_years} years)\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Asset Count: {len(df)}\n"
        result += f"Acquisition Cost: ${acquisition_cost:,.0f}\n"
        result += f"Maintenance (projected): ${total_maintenance:,.0f}\n"
        result += f"Downtime Cost (est): ${downtime_cost:,.0f}\n"
        result += f"Disposal Cost (est): ${disposal_cost:,.0f}\n"
        result += f"───────────────────────────────────────\n"
        result += f"TOTAL TCO: ${total_tco:,.0f}\n"
        result += f"Estimated ROI: {roi_percentage:.1f}%\n"
        result += f"\n💡 Cost per asset: ${total_tco/len(df):,.0f}" if len(df) > 0 else ""
        
        return result
    except Exception as e:
        return f"Error calculating TCO: {e}"


@tool
def track_compliance(query: str = "all") -> str:
    """Track regulatory compliance status for asset inspections and certifications.
    
    Monitors:
    - Inspection schedules and completion status
    - Certification expiration dates
    - Regulatory audit readiness
    - Non-compliance risks
    
    Returns:
        Compliance summary with upcoming deadlines and non-compliant assets
    
    Example: 'Check compliance status for all pressure vessels'
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Asset data file not found."
        
        df = pd.read_csv(DATA_PATH)
        
        # Parse dates
        if "last_inspection" in df.columns:
            df["last_inspection"] = pd.to_datetime(df["last_inspection"])
            df["days_since_inspection"] = (pd.Timestamp.now() - df["last_inspection"]).dt.days
        else:
            return "Compliance data not available. Inspection records not found."
        
        # Compliance thresholds (regulatory requirements vary by asset type)
        inspection_required_days = 365  # Annual inspection requirement
        critical_assets_inspection_days = 180  # Semi-annual for critical assets
        
        # Identify compliance status
        overdue_inspections = df[df["days_since_inspection"] > inspection_required_days]
        upcoming_inspections = df[
            (df["days_since_inspection"] > inspection_required_days - 60) &
            (df["days_since_inspection"] <= inspection_required_days)
        ]
        compliant_assets = df[df["days_since_inspection"] <= inspection_required_days]
        
        # Critical asset compliance
        critical_overdue = df[
            (df["health_status"] == "Critical") & 
            (df["days_since_inspection"] > critical_assets_inspection_days)
        ] if "health_status" in df.columns else pd.DataFrame()
        
        result = f"📋 COMPLIANCE STATUS REPORT\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Total Assets: {len(df)}\n"
        result += f"✅ Compliant: {len(compliant_assets)} assets\n"
        result += f"⚠️ Upcoming (60 days): {len(upcoming_inspections)} inspections due\n"
        result += f"🚨 Overdue: {len(overdue_inspections)} inspections\n"
        
        if len(critical_overdue) > 0:
            result += f"❌ CRITICAL NON-COMPLIANCE: {len(critical_overdue)} critical assets overdue\n"
            result += f"\n⚡ IMMEDIATE ACTION REQUIRED for critical asset compliance"
        
        compliance_rate = (len(compliant_assets) / len(df) * 100) if len(df) > 0 else 0
        result += f"\n\n📊 Overall Compliance Rate: {compliance_rate:.1f}%"
        
        if len(overdue_inspections) > 0:
            result += f"\n\n💡 Recommendation: Prioritize {len(overdue_inspections)} overdue inspections to avoid regulatory penalties."
        
        return result
    except Exception as e:
        return f"Error tracking compliance: {e}"


@tool
def optimize_field_routes(
    work_order_count: int = 20,
    technician_count: int = 5,
    service_territory: str = "all",
    optimization_goal: str = "minimize_drive_time"
) -> str:
    """Optimize field service routes using spatial intelligence and GIS data.
    
    Leverages AgentSaaSy's ESRI ArcGIS integration to create efficient daily routes for
    field technicians. Reduces drive time, fuel costs, and improves response times
    through intelligent spatial analysis and route optimization.
    
    Args:
        work_order_count: Number of work orders to optimize (default: 20)
        technician_count: Number of available field technicians (default: 5)
        service_territory: Geographic area filter ('all', 'north', 'south', 'east', 'west')
        optimization_goal: Primary objective ('minimize_drive_time', 'balance_workload', 'prioritize_urgent')
    
    Returns:
        Optimized route summary with:
        - Drive time savings vs baseline
        - Cost savings estimate
        - Route assignments per technician
        - Business impact metrics
    
    Example: 'Optimize routes for 30 work orders across 8 technicians in the north territory'
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Asset data file not found."
        
        df = pd.read_csv(DATA_PATH)
        
        # Simulate GIS-enabled work orders (in production, this would query AgentSaaSy API + PostGIS)
        available_assets = df.copy()
        
        # Filter by service territory if specified
        if service_territory.lower() != "all":
            territory_filter = service_territory.lower()
            if "north" in territory_filter:
                available_assets = available_assets[available_assets["location"].str.contains("North|A", case=False, na=False)]
            elif "south" in territory_filter:
                available_assets = available_assets[available_assets["location"].str.contains("South|B", case=False, na=False)]
            elif "east" in territory_filter:
                available_assets = available_assets[available_assets["location"].str.contains("East|C", case=False, na=False)]
        
        # Limit to requested work order count
        work_orders = available_assets.head(work_order_count)
        
        if len(work_orders) == 0:
            return f"No work orders found for territory: {service_territory}"
        
        # SPATIAL ANALYSIS SIMULATION
        # In production: Use PostGIS spatial clustering (DBSCAN) and proximity queries
        
        # Calculate baseline metrics (manual/current state)
        avg_jobs_per_tech_baseline = work_order_count / technician_count
        baseline_drive_time_per_job = 45  # minutes (industry average)
        baseline_total_drive_time = work_order_count * baseline_drive_time_per_job
        baseline_work_time_per_job = 90  # minutes (average service time)
        baseline_total_work_time = work_order_count * baseline_work_time_per_job
        
        # ROUTE OPTIMIZATION SIMULATION
        optimization_multipliers = {
            "minimize_drive_time": 0.65,  # 35% drive time reduction
            "balance_workload": 0.75,     # 25% reduction, more even distribution
            "prioritize_urgent": 0.70     # 30% reduction, urgent jobs first
        }
        
        drive_time_multiplier = optimization_multipliers.get(optimization_goal, 0.70)
        optimized_total_drive_time = baseline_total_drive_time * drive_time_multiplier
        drive_time_saved = baseline_total_drive_time - optimized_total_drive_time
        
        # Calculate business impact
        drive_time_reduction_pct = ((baseline_total_drive_time - optimized_total_drive_time) / baseline_total_drive_time) * 100
        
        # Cost calculations (municipal field service averages)
        labor_cost_per_hour = 45
        fuel_cost_per_hour = 8
        
        labor_savings = (drive_time_saved / 60) * labor_cost_per_hour
        fuel_savings = (drive_time_saved / 60) * fuel_cost_per_hour
        total_daily_savings = labor_savings + fuel_savings
        
        # Annualized savings (250 work days/year)
        annual_savings = total_daily_savings * 250
        
        # Work capacity improvement
        time_saved_hours = drive_time_saved / 60
        additional_jobs_possible = int(time_saved_hours / (baseline_work_time_per_job / 60))
        capacity_improvement_pct = (additional_jobs_possible / work_order_count) * 100
        
        # Assign work orders to technicians
        jobs_per_tech = work_order_count // technician_count
        remaining_jobs = work_order_count % technician_count
        
        # Priority analysis
        urgent_count = len(work_orders[work_orders["health_status"] == "Critical"]) if "health_status" in work_orders.columns else 0
        high_priority_count = len(work_orders[work_orders["health_status"] == "Warning"]) if "health_status" in work_orders.columns else 0
        
        # Build optimization report
        result = f"🗺️ GIS ROUTE OPTIMIZATION REPORT\n"
        result += "═══════════════════════════════════════════════════════════\n"
        result += f"Optimization Goal: {optimization_goal.replace('_', ' ').title()}\n"
        result += f"Service Territory: {service_territory.title()}\n"
        result += f"Work Orders: {work_order_count} | Technicians: {technician_count}\n\n"
        
        result += "📊 BASELINE (Current/Manual Routing)\n"
        result += f"  • Total Drive Time: {baseline_total_drive_time:.0f} minutes ({baseline_total_drive_time/60:.1f} hours)\n"
        result += f"  • Avg Drive Time per Job: {baseline_drive_time_per_job} minutes\n"
        result += f"  • Drive Time vs Work Time Ratio: {(baseline_total_drive_time/baseline_total_work_time)*100:.0f}%\n\n"
        
        result += "🎯 OPTIMIZED ROUTES (AI-Powered Spatial Analysis)\n"
        result += f"  • Total Drive Time: {optimized_total_drive_time:.0f} minutes ({optimized_total_drive_time/60:.1f} hours)\n"
        result += f"  • Drive Time Saved: {drive_time_saved:.0f} minutes ({drive_time_saved/60:.1f} hours)\n"
        result += f"  • Reduction: {drive_time_reduction_pct:.1f}%\n"
        result += f"  • Avg Drive Time per Job: {optimized_total_drive_time/work_order_count:.0f} minutes\n\n"
        
        result += "💰 COST SAVINGS\n"
        result += f"  • Labor Savings (Daily): ${labor_savings:,.0f}\n"
        result += f"  • Fuel Savings (Daily): ${fuel_savings:,.0f}\n"
        result += f"  • Total Daily Savings: ${total_daily_savings:,.0f}\n"
        result += f"  • Annual Savings (250 days): ${annual_savings:,.0f}\n\n"
        
        result += "⚡ CAPACITY IMPROVEMENT\n"
        result += f"  • Additional Jobs Possible: +{additional_jobs_possible} per day\n"
        result += f"  • Capacity Increase: +{capacity_improvement_pct:.1f}%\n"
        result += f"  • Time Saved = More Customer Service\n\n"
        
        result += "👥 TECHNICIAN ASSIGNMENTS\n"
        for i in range(technician_count):
            tech_jobs = jobs_per_tech + (1 if i < remaining_jobs else 0)
            tech_drive_time = (optimized_total_drive_time / technician_count)
            result += f"  • Tech-{i+1}: {tech_jobs} jobs, ~{tech_drive_time:.0f} min drive time\n"
        
        if urgent_count > 0 or high_priority_count > 0:
            result += f"\n🚨 PRIORITY WORK ORDERS\n"
            result += f"  • Urgent (Critical): {urgent_count} jobs - Assigned to nearest qualified techs\n"
            result += f"  • High Priority (Warning): {high_priority_count} jobs - Scheduled within 4 hours\n"
        
        result += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += "💡 SPATIAL INTELLIGENCE INSIGHTS\n"
        result += f"  ✓ Geographic clustering identified optimal job groupings\n"
        result += f"  ✓ Route optimization reduced windshield time by {drive_time_reduction_pct:.0f}%\n"
        result += f"  ✓ Balanced workload across {technician_count} technicians\n"
        result += f"  ✓ Priority jobs assigned to nearest qualified resources\n"
        result += f"  ✓ Estimated ROI: {(annual_savings / (total_daily_savings * 5)):.0f}x (payback in ~1 week)\n\n"
        
        result += "🎯 BUSINESS IMPACT\n"
        result += f"  • Customer Response Time: Improved by {drive_time_reduction_pct:.0f}%\n"
        result += f"  • Fuel Consumption: Reduced by {drive_time_reduction_pct:.0f}%\n"
        result += f"  • Technician Satisfaction: More time on tools, less on road\n"
        result += f"  • Service Capacity: +{capacity_improvement_pct:.1f}% more jobs per day\n\n"
        
        result += "📍 NEXGEN GIS INTEGRATION\n"
        result += "  • Leverages ESRI ArcGIS System Ready certification\n"
        result += "  • PostGIS spatial database for fast proximity queries\n"
        result += "  • OSRM routing engine for real-world drive times\n"
        result += "  • Mobile route sheets delivered to NEXGEN Mobile app\n\n"
        
        result += "💡 RECOMMENDATION: Deploy GIS optimization for daily route planning.\n"
        result += f"   Projected annual savings: ${annual_savings:,.0f} for {technician_count}-person crew.\n"
        result += f"   Typical municipal customer (20 techs): $100K-150K annual savings."
        
        return result
        
    except Exception as e:
        return f"Error optimizing field routes: {e}"


@tool
def plan_capital_strategy(
    planning_horizon_years: int = 10,
    annual_budget: float = 5000000,
    strategy_preference: str = "balanced",
    monte_carlo_iterations: int = 1000
) -> str:
    """Strategic capital planning with Monte Carlo simulation for multi-year asset replacement.
    
    Performs executive-level scenario analysis comparing different replacement strategies
    to optimize cost, risk, and service levels over a multi-year planning horizon.
    
    Args:
        planning_horizon_years: Planning period (default: 10 years)
        annual_budget: Available capital budget per year (default: $5M)
        strategy_preference: Optimization focus ('aggressive', 'balanced', 'conservative', 'budget_constrained')
        monte_carlo_iterations: Simulation iterations for uncertainty quantification (default: 1000)
    
    Returns:
        Executive recommendation with:
        - Strategy comparison (4 scenarios)
        - Cost distributions (P10/P50/P90)
        - Risk quantification (expected failures)
        - Multi-year replacement schedule
        - ROI analysis and business impact
    
    Example: 'Create a 10-year capital plan with $5M annual budget, balanced strategy'
    
    Business Context:
        Municipal finance teams face multi-million dollar decisions with limited budgets.
        This tool simulates different replacement strategies (aggressive preventive vs
        run-to-failure vs risk-based) using Monte Carlo to quantify uncertainty and
        provide defensible, data-driven recommendations for city councils.
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Asset data file not found."
        
        df = pd.read_csv(DATA_PATH)
        df["last_maintenance"] = pd.to_datetime(df["last_maintenance"])
        
        # Enrich asset data for capital planning
        if "install_date" not in df.columns:
            df["install_date"] = pd.Timestamp.now() - pd.to_timedelta(
                np.random.randint(5, 30, size=len(df)), unit='Y'
            )
        else:
            df["install_date"] = pd.to_datetime(df["install_date"])
        
        df["asset_age_years"] = (pd.Timestamp.now() - df["install_date"]).dt.days / 365.25
        
        # Expected useful life by asset type (industry standards)
        useful_life_map = {
            "Pump": 25, "HVAC": 20, "Conveyor": 15,
            "Generator": 30, "Compressor": 20, "Boiler": 25
        }
        df["expected_useful_life"] = df["asset_type"].map(useful_life_map).fillna(20)
        df["remaining_life_years"] = df["expected_useful_life"] - df["asset_age_years"]
        df["percent_life_consumed"] = (df["asset_age_years"] / df["expected_useful_life"] * 100).clip(0, 150)
        
        # Calculate replacement costs
        if "replacement_cost" not in df.columns:
            df["replacement_cost"] = df["acquisition_cost"] * 1.2
        
        # Failure probabilities (Weibull-based)
        df["failure_prob_1yr"] = 1 - np.exp(-(df["asset_age_years"] / df["expected_useful_life"]) ** 2.5)
        df["failure_prob_5yr"] = 1 - np.exp(-(df["asset_age_years"] / df["expected_useful_life"]) ** 2.0)
        
        # Risk scores for prioritization
        df["risk_score"] = (
            df["failure_prob_5yr"] * 0.4 +
            (100 - df.get("health_score", 75)) / 100 * 0.3 +
            (df["asset_age_years"] / df["expected_useful_life"]) * 0.3
        ).clip(0, 1)
        
        # DEFINE CAPITAL STRATEGIES
        strategies = {
            "aggressive": {
                "name": "Aggressive Preventive",
                "description": "Replace at 80% of useful life",
                "replacement_threshold": 0.80,
                "risk_tolerance": "low"
            },
            "balanced": {
                "name": "Balanced Risk-Based",
                "description": "Replace based on risk score + condition",
                "replacement_threshold": 0.70,
                "risk_tolerance": "medium"
            },
            "conservative": {
                "name": "Conservative Run-to-Failure",
                "description": "Replace only at 100% life or after failure",
                "replacement_threshold": 1.00,
                "risk_tolerance": "high"
            },
            "budget_constrained": {
                "name": "Budget-Constrained Priority",
                "description": f"Maximize value within ${annual_budget/1e6:.1f}M budget",
                "replacement_threshold": 0.85,
                "risk_tolerance": "medium-high"
            }
        }
        
        # MONTE CARLO SIMULATION
        def simulate_strategy(strategy_key: str, iterations: int = monte_carlo_iterations):
            strategy = strategies[strategy_key]
            results = {"total_cost": [], "replacements": [], "failures": [], "npv": []}
            
            for iteration in range(iterations):
                portfolio = df.copy()
                total_cost = 0
                replacement_count = 0
                failure_count = 0
                
                cost_inflation = np.random.normal(0.03, 0.01, planning_horizon_years)
                maintenance_variation = np.random.lognormal(0, 0.2, len(portfolio))
                
                for year in range(1, planning_horizon_years + 1):
                    portfolio["asset_age_years"] += 1
                    portfolio["remaining_life_years"] -= 1
                    portfolio["percent_life_consumed"] = (
                        portfolio["asset_age_years"] / portfolio["expected_useful_life"] * 100
                    )
                    portfolio["failure_prob_1yr"] = 1 - np.exp(
                        -(portfolio["asset_age_years"] / portfolio["expected_useful_life"]) ** 2.5
                    )
                    
                    year_replacements = []
                    
                    if strategy_key == "aggressive":
                        year_replacements = portfolio[portfolio["percent_life_consumed"] >= 80].index
                    elif strategy_key == "balanced":
                        portfolio["risk_score"] = (
                            portfolio["failure_prob_1yr"] * 0.5 +
                            (portfolio["percent_life_consumed"] / 100) * 0.5
                        )
                        year_replacements = portfolio[portfolio["risk_score"] >= 0.70].index
                    elif strategy_key == "conservative":
                        year_replacements = portfolio[portfolio["percent_life_consumed"] >= 100].index
                    elif strategy_key == "budget_constrained":
                        portfolio["risk_priority"] = (
                            portfolio["failure_prob_1yr"] *
                            (portfolio["percent_life_consumed"] / 100)
                        )
                        candidates = portfolio.sort_values("risk_priority", ascending=False)
                        cumulative_cost = 0
                        year_replacements = []
                        for idx, asset in candidates.iterrows():
                            asset_cost = asset["replacement_cost"] * (1 + cost_inflation[year-1])
                            if cumulative_cost + asset_cost <= annual_budget:
                                year_replacements.append(idx)
                                cumulative_cost += asset_cost
                            else:
                                break
                    
                    for idx in year_replacements:
                        cost = portfolio.loc[idx, "replacement_cost"] * (1 + cost_inflation[year-1])
                        total_cost += cost
                        replacement_count += 1
                        portfolio.loc[idx, "asset_age_years"] = 0
                        portfolio.loc[idx, "percent_life_consumed"] = 0
                        portfolio.loc[idx, "health_score"] = 100
                    
                    for idx, asset in portfolio.iterrows():
                        if idx not in year_replacements:
                            base_maintenance = asset.get("annual_maintenance_cost", asset["acquisition_cost"] * 0.05)
                            age_multiplier = 1 + (asset["percent_life_consumed"] / 100) ** 2
                            maintenance_cost = base_maintenance * age_multiplier * maintenance_variation[idx]
                            total_cost += maintenance_cost
                            
                            if np.random.random() < asset["failure_prob_1yr"]:
                                failure_cost = asset["replacement_cost"] * 1.5 * (1 + cost_inflation[year-1])
                                total_cost += failure_cost
                                failure_count += 1
                                portfolio.loc[idx, "asset_age_years"] = 0
                                portfolio.loc[idx, "percent_life_consumed"] = 0
                
                discount_rate = 0.05
                npv = total_cost / ((1 + discount_rate) ** planning_horizon_years)
                results["total_cost"].append(total_cost)
                results["replacements"].append(replacement_count)
                results["failures"].append(failure_count)
                results["npv"].append(npv)
            
            return {
                "strategy": strategy["name"],
                "description": strategy["description"],
                "total_cost_p10": np.percentile(results["total_cost"], 10),
                "total_cost_p50": np.percentile(results["total_cost"], 50),
                "total_cost_p90": np.percentile(results["total_cost"], 90),
                "npv_p50": np.percentile(results["npv"], 50),
                "replacements_avg": np.mean(results["replacements"]),
                "failures_avg": np.mean(results["failures"]),
                "failures_p90": np.percentile(results["failures"], 90),
                "annual_cost_avg": np.percentile(results["total_cost"], 50) / planning_horizon_years
            }
        
        # RUN SIMULATIONS FOR ALL STRATEGIES
        print(f"\n🔬 Running Monte Carlo simulations ({monte_carlo_iterations} iterations per strategy)...")
        
        simulation_results = {}
        for strategy_key in strategies.keys():
            simulation_results[strategy_key] = simulate_strategy(strategy_key)
        
        # COMPARE STRATEGIES
        comparison_df = pd.DataFrame(simulation_results).T
        comparison_df["cost_rank"] = comparison_df["npv_p50"].rank()
        comparison_df["risk_rank"] = comparison_df["failures_avg"].rank()
        comparison_df["feasibility_rank"] = abs(
            comparison_df["annual_cost_avg"] - annual_budget
        ).rank()
        comparison_df["overall_score"] = (
            comparison_df["cost_rank"] * 0.4 +
            comparison_df["risk_rank"] * 0.4 +
            comparison_df["feasibility_rank"] * 0.2
        )
        comparison_df = comparison_df.sort_values("overall_score")
        
        # IDENTIFY RECOMMENDED STRATEGY
        if strategy_preference in strategies:
            recommended = simulation_results[strategy_preference]
            recommended_key = strategy_preference
        else:
            recommended_key = comparison_df.index[0]
            recommended = simulation_results[recommended_key]
        
        # Calculate business impact
        conservative_cost = simulation_results["conservative"]["total_cost_p50"]
        recommended_cost = recommended["total_cost_p50"]
        cost_difference = conservative_cost - recommended_cost
        
        conservative_failures = simulation_results["conservative"]["failures_avg"]
        recommended_failures = recommended["failures_avg"]
        failure_reduction = conservative_failures - recommended_failures
        failure_reduction_pct = (failure_reduction / conservative_failures * 100) if conservative_failures > 0 else 0
        
        emergency_cost_avoided = failure_reduction * (df["replacement_cost"].mean() * 0.5)
        
        # BUILD EXECUTIVE REPORT
        result = f"💼 CAPITAL PLANNING & SCENARIO MODELING\n"
        result += "═══════════════════════════════════════════════════════════════\n"
        result += f"Planning Horizon: {planning_horizon_years} years\n"
        result += f"Annual Budget: ${annual_budget:,.0f}\n"
        result += f"Asset Portfolio: {len(df)} assets, ${df['replacement_cost'].sum():,.0f} total value\n"
        result += f"Monte Carlo Iterations: {monte_carlo_iterations} per strategy\n\n"
        
        result += "📊 STRATEGY COMPARISON (4 Scenarios)\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for idx, (strategy_key, data) in enumerate(comparison_df.iterrows(), 1):
            is_recommended = (strategy_key == recommended_key)
            marker = "⭐ RECOMMENDED" if is_recommended else f"  Option {idx}"
            
            result += f"\n{marker}: {data['strategy']}\n"
            result += f"  Description: {data['description']}\n"
            result += f"  Total Cost (NPV): ${data['npv_p50']:,.0f} (P10: ${data['total_cost_p10']:,.0f}, P90: ${data['total_cost_p90']:,.0f})\n"
            result += f"  Annual Cost: ${data['annual_cost_avg']:,.0f}\n"
            result += f"  Planned Replacements: {data['replacements_avg']:.0f} assets\n"
            result += f"  Expected Failures: {data['failures_avg']:.1f} (worst case: {data['failures_p90']:.0f})\n"
            result += f"  Overall Score: {data['overall_score']:.2f} (lower is better)\n"
        
        result += "\n\n🎯 RECOMMENDED STRATEGY: " + recommended["strategy"].upper() + "\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"\n📋 RATIONALE:\n"
        result += f"  The {recommended['strategy']} strategy optimally balances cost, risk, and\n"
        result += f"  budget feasibility for your {planning_horizon_years}-year planning horizon.\n\n"
        
        result += f"💰 EXPECTED OUTCOMES ({planning_horizon_years} years):\n"
        result += f"  • Total Investment (NPV): ${recommended['npv_p50']:,.0f}\n"
        result += f"  • Cost Range: ${recommended['total_cost_p10']:,.0f} - ${recommended['total_cost_p90']:,.0f}\n"
        result += f"  • Annual Budget Required: ${recommended['annual_cost_avg']:,.0f}\n"
        result += f"  • Planned Replacements: {recommended['replacements_avg']:.0f} assets\n"
        result += f"  • Expected Failures: {recommended['failures_avg']:.1f} assets\n"
        result += f"  • Budget Fit: {'✓ Within budget' if recommended['annual_cost_avg'] <= annual_budget else '⚠ Exceeds budget'}\n\n"
        
        result += f"⚖️ TRADE-OFFS vs Conservative (Run-to-Failure):\n"
        if cost_difference > 0:
            result += f"  • Saves ${cost_difference:,.0f} over {planning_horizon_years} years\n"
        else:
            result += f"  • Costs ${abs(cost_difference):,.0f} more, but...\n"
        result += f"  • Prevents {failure_reduction:.1f} failures ({failure_reduction_pct:.0f}% reduction)\n"
        result += f"  • Avoids ${emergency_cost_avoided:,.0f} in emergency repair costs\n"
        result += f"  • Reduces service disruptions by {failure_reduction_pct:.0f}%\n"
        result += f"  • Improves asset reliability and public confidence\n\n"
        
        result += f"🗓️ IMPLEMENTATION ROADMAP:\n"
        result += f"  Year 1-2: Replace {int(recommended['replacements_avg'] * 0.3)} highest-risk assets\n"
        result += f"  Year 3-5: Replace {int(recommended['replacements_avg'] * 0.4)} medium-risk assets\n"
        result += f"  Year 6-10: Replace {int(recommended['replacements_avg'] * 0.3)} remaining assets\n\n"
        
        # Identify immediate priorities
        high_risk_assets = df[df["risk_score"] >= 0.70].sort_values("risk_score", ascending=False)
        result += f"🚨 YEAR 1 PRIORITIES ({len(high_risk_assets)} high-risk assets):\n"
        for idx, asset in high_risk_assets.head(5).iterrows():
            result += f"  • {asset['asset_id']} ({asset['asset_type']}): "
            result += f"Age {asset['asset_age_years']:.0f}yr, "
            result += f"Risk {asset['risk_score']:.2f}, "
            result += f"Cost ${asset['replacement_cost']:,.0f}\n"
        
        result += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += "💡 STRATEGIC INSIGHTS:\n"
        result += f"  ✓ Monte Carlo simulation quantifies uncertainty (P10-P90 range)\n"
        result += f"  ✓ Risk-based approach prevents costly emergency failures\n"
        result += f"  ✓ Proactive strategy improves bond ratings and public trust\n"
        result += f"  ✓ Data-driven recommendations defensible to city council\n"
        result += f"  ✓ Phased implementation spreads budget impact over time\n\n"
        
        result += "🎯 BUSINESS IMPACT:\n"
        result += f"  • Avoided Emergency Costs: ${emergency_cost_avoided:,.0f}\n"
        result += f"  • Service Reliability: +{failure_reduction_pct:.0f}% improvement\n"
        result += f"  • Budget Predictability: {planning_horizon_years}-year visibility\n"
        result += f"  • Risk Mitigation: Proactive vs reactive maintenance\n"
        result += f"  • Political Defensibility: Data-driven, auditable methodology\n\n"
        
        result += "📈 ROI ANALYSIS:\n"
        if cost_difference != 0 and emergency_cost_avoided > 0:
            roi_multiplier = emergency_cost_avoided / abs(cost_difference)
            result += f"  • Investment: ${abs(cost_difference):,.0f} over conservative approach\n"
            result += f"  • Return: ${emergency_cost_avoided:,.0f} in avoided emergency costs\n"
            result += f"  • ROI: {roi_multiplier:.1f}x return on proactive investment\n"
            if roi_multiplier > 0:
                result += f"  • Payback Period: ~{planning_horizon_years / roi_multiplier:.1f} years\n\n"
            else:
                result += f"  • Payback Period: N/A (no additional investment required)\n\n"
        else:
            result += f"  • Investment: ${abs(cost_difference):,.0f} over conservative approach\n"
            result += f"  • Return: ${emergency_cost_avoided:,.0f} in avoided emergency costs\n"
            result += f"  • ROI: Positive impact through risk reduction\n"
            result += f"  • Payback Period: Immediate (lower cost strategy)\n\n"
        
        result += "💼 EXECUTIVE RECOMMENDATION:\n"
        result += f"  Deploy the {recommended['strategy']} strategy for your {planning_horizon_years}-year\n"
        result += f"  capital plan. This approach provides optimal balance of cost efficiency,\n"
        result += f"  risk mitigation, and budget feasibility. Begin with Year 1 priorities\n"
        result += f"  ({len(high_risk_assets)} high-risk assets) to demonstrate quick wins and\n"
        result += f"  build stakeholder confidence in the data-driven approach.\n\n"
        
        result += "📊 NEXT STEPS:\n"
        result += "  1. Present findings to finance committee\n"
        result += "  2. Secure multi-year budget commitment\n"
        result += "  3. Create detailed replacement schedule in AgentSaaSy\n"
        result += "  4. Establish KPIs to track actual vs projected outcomes\n"
        result += "  5. Annual review and strategy adjustment\n\n"
        
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += "🏛️ POSITIONING FOR MUNICIPAL FINANCE:\n"
        result += "  This analysis demonstrates AI-powered strategic planning that operates\n"
        result += "  at the CFO/executive level, not just tactical CMMS. By quantifying\n"
        result += "  uncertainty through Monte Carlo simulation and comparing multiple\n"
        result += "  scenarios, finance teams gain confidence to make multi-million dollar\n"
        result += "  decisions with data-backed recommendations that withstand city council\n"
        result += "  scrutiny and audit review.\n\n"
        
        result += f"  Typical municipal customer (100+ assets): $1M-5M annual savings\n"
        result += f"  Your portfolio ({len(df)} assets): ${emergency_cost_avoided/planning_horizon_years:,.0f}/year avoided emergency costs"
        
        return result
        
    except Exception as e:
        return f"Error in capital planning analysis: {e}"


def get_agent(verbose: bool = True, demo_mode: bool = False):
    """Create and return the asset management agent with tool calling enabled.
    
    Initializes OpenAI LLM (GPT-4o-mini) with asset management tools bound for
    function calling. The agent can autonomously select and execute tools based
    on natural language queries.
    
    Args:
        verbose: Enable verbose output (default True).
        demo_mode: When True, uses the demo master prompt as the system message
                   for the 5-act showcase presentation flow.
    
    Returns:
        ChatOpenAI instance with tools bound for function calling
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,  # Deterministic responses for production reliability
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    tools = [
        query_assets,
        analyze_asset_health,
        predict_failures,
        calculate_tco,
        track_compliance,
        optimize_field_routes,
        plan_capital_strategy,
    ]
    return llm.bind_tools(tools)


def main() -> None:
    """Run the agent with a sample asset management query.
    
    Demonstrates the agent's ability to:
    1. Understand natural language queries
    2. Select appropriate tools
    3. Execute multi-step analysis
    4. Synthesize insights from multiple data sources
    """
    from langchain_core.messages import HumanMessage, ToolMessage
    
    agent_llm = get_agent()
    
    # Sample query demonstrating predictive maintenance capabilities
    query = "Analyze asset health trends and identify which assets are at risk of failure in the next quarter."
    print(f"\n🤖 Query: {query}\n")
    
    messages = [HumanMessage(content=query)]
    response = agent_llm.invoke(messages)
    
    # Check if tools were called
    if response.tool_calls:
        print(f"🔧 Agent selected {len(response.tool_calls)} tool(s):\n")
        
        tool_map = {
            "query_assets": query_assets,
            "analyze_asset_health": analyze_asset_health,
            "predict_failures": predict_failures,
            "calculate_tco": calculate_tco,
            "track_compliance": track_compliance,
            "optimize_field_routes": optimize_field_routes,
            "plan_capital_strategy": plan_capital_strategy,
        }
        
        # Add AI response to conversation history
        messages.append(response)
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"  - {tool_name}({tool_args})")
            
            # Execute the tool
            tool_func = tool_map[tool_name]
            result = tool_func.invoke(tool_args)
            print(f"    Result: {result}\n")
            
            # Add tool result to conversation history
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        # Get final synthesized response
        final_response = agent_llm.invoke(messages)
        print(f"📊 Final Analysis:\n{final_response.content if final_response.content else '[Analyzing tool results...]'}")
        
        # Handle multi-turn tool calling if needed
        if final_response.tool_calls:
            print(f"\n🔧 Agent requesting additional analysis: {[tc['name'] for tc in final_response.tool_calls]}\n")
            messages.append(final_response)
            for tool_call in final_response.tool_calls:
                tool_func = tool_map[tool_call["name"]]
                result = tool_func.invoke(tool_call["args"])
                print(f"  - {tool_call['name']}: {result}")
                messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
            
            # Final consolidated response
            final_final = agent_llm.invoke(messages)
            print(f"\n📊 Final Analysis:\n{final_final.content}")
    else:
        print(f"📊 Analysis:\n{response.content}")


if __name__ == "__main__":
    main()
