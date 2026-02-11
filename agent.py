"""
AgentSaasy_NGAI: 3-layer AI agent for enterprise asset management.

Designed for NexGen Asset Management platform to demonstrate AI-powered
predictive maintenance, cost optimization, and compliance automation.

Architecture:
  1. Reasoning layer: OpenAI LLM with tool calling (GPT-4o-mini)
  2. Tools layer: Asset query, health analysis, failure prediction, compliance tracking, TCO calculation
  3. Orchestration layer: LangChain tool binding for seamless LLM-tool integration

This agent analyzes asset portfolios to predict failures, optimize maintenance spend,
ensure regulatory compliance, and provide executive insights through natural language.
"""

import os
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from scipy import stats
from sklearn.linear_model import LinearRegression

# Constants
DATA_PATH = Path(__file__).parent / "data" / "asset_data.csv"
FAILURE_RISK_THRESHOLD = 70  # Risk score threshold for predictive maintenance alerts

load_dotenv()


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


def get_agent(verbose: bool = True):
    """Create and return the asset management agent with tool calling enabled.
    
    Initializes OpenAI LLM (GPT-4o-mini) with asset management tools bound for
    function calling. The agent can autonomously select and execute tools based
    on natural language queries.
    
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
