"""
AgentSaasy: 3-layer AI agent for enterprise data analysis.

Architecture:
  1. Reasoning layer: OpenAI LLM with tool calling
  2. Tools layer: query_data, analyze_trends, detect_anomalies
  3. Orchestration layer: LangChain tool binding
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
DATA_PATH = Path(__file__).parent / "data" / "sales_data.csv"

load_dotenv()


@tool
def query_data(query: str) -> str:
    """Query sales data. Use for filtering by product, region, date range, or quarter.
    Examples: 'last quarter', 'Widget A', 'North region', 'Q1 2024'.
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Sales data file not found."
        df = pd.read_csv(DATA_PATH)
        df["date"] = pd.to_datetime(df["date"])
        query_lower = query.lower()
        result = df
        if "north" in query_lower or "north region" in query_lower:
            result = result[result["region"] == "North"]
        elif "south" in query_lower or "south region" in query_lower:
            result = result[result["region"] == "South"]
        if "widget a" in query_lower or "product a" in query_lower:
            result = result[result["product"] == "Widget A"]
        elif "widget b" in query_lower or "product b" in query_lower:
            result = result[result["product"] == "Widget B"]
        if "q1" in query_lower or "quarter 1" in query_lower:
            result = result[result["date"].dt.month <= 3]
        elif "q2" in query_lower or "quarter 2" in query_lower:
            result = result[(result["date"].dt.month >= 4) & (result["date"].dt.month <= 6)]
        if "last quarter" in query_lower:
            result = result[result["date"].dt.month >= 4]
        total = result["amount"].sum()
        count = len(result)
        return f"Found {count} records. Total amount: ${total:,.2f}."
    except Exception as e:
        return f"Error querying data: {e}"


@tool
def analyze_trends(query: str) -> str:
    """Analyze sales trends. Call with context from query_data (e.g. product/region).
    Returns summary of growth, comparisons, and key metrics."""
    try:
        if not DATA_PATH.exists():
            return "Error: Sales data file not found."
        df = pd.read_csv(DATA_PATH)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M")
        monthly = df.groupby("month").agg({"amount": "sum", "quantity": "sum"}).reset_index()
        if len(monthly) < 2:
            return "Insufficient data for trend analysis."
        first_val = monthly["amount"].iloc[0]
        last_val = monthly["amount"].iloc[-1]
        growth_pct = ((last_val - first_val) / first_val * 100) if first_val else 0
        avg_monthly = monthly["amount"].mean()
        return (
            f"Trends: First month ${first_val:,.0f}, last ${last_val:,.0f}. "
            f"Growth: {growth_pct:.1f}%. Avg monthly: ${avg_monthly:,.0f}."
        )
    except Exception as e:
        return f"Error analyzing trends: {e}"


@tool
def detect_anomalies(query: str) -> str:
    """Detect anomalies in sales data. Uses statistical outlier detection.
    Call after query_data to analyze a subset, or use 'all' for full dataset."""
    try:
        if not DATA_PATH.exists():
            return "Error: Sales data file not found."
        df = pd.read_csv(DATA_PATH)
        amounts = df["amount"]
        mean_val = amounts.mean()
        std_val = amounts.std()
        if std_val == 0:
            return "No variance in data; no anomalies detected."
        threshold = 2.0
        outliers = df[(amounts - mean_val).abs() > threshold * std_val]
        if outliers.empty:
            return f"No anomalies (threshold {threshold} std). Mean: ${mean_val:,.0f}."
        return (
            f"Found {len(outliers)} anomaly/outliers. "
            f"Mean: ${mean_val:,.0f}, Std: ${std_val:,.0f}. "
            f"Outlier rows: {outliers[['date', 'product', 'amount']].to_dict('records')}."
        )
    except Exception as e:
        return f"Error detecting anomalies: {e}"


@tool
def generate_forecast(periods: int = 4) -> str:
    """Generate linear regression forecast for next N periods (weeks).
    
    Args:
        periods: Number of future periods to predict (default: 4 weeks)
    
    Returns:
        Formatted string with predictions, R² score, and average forecast
    
    Example: 'Forecast next quarter's revenue'
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Sales data file not found."
        
        df = pd.read_csv(DATA_PATH)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        
        # Create day index for regression
        min_date = df["date"].min()
        df["day_index"] = (df["date"] - min_date).dt.days
        
        # Prepare data for regression
        X = df[["day_index"]].values
        y = df["amount"].values
        
        # Train linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate R² score
        r2_score = model.score(X, y)
        
        # Generate future predictions
        last_day = df["day_index"].max()
        last_date = df["date"].max()
        predictions = []
        
        for i in range(1, periods + 1):
            future_day = last_day + (7 * i)  # Weekly predictions
            future_date = last_date + timedelta(weeks=i)
            pred_amount = model.predict([[future_day]])[0]
            predictions.append(f"  • Week {i} ({future_date.strftime('%Y-%m-%d')}): ${pred_amount:,.0f}")
        
        avg_forecast = sum(model.predict([[last_day + (7 * i)]]) for i in range(1, periods + 1))[0] / periods
        
        result = f"🔮 Forecast (Linear Regression, R²={r2_score:.3f}):\n"
        result += "\n".join(predictions)
        result += f"\n\n📊 Avg Forecast: ${avg_forecast:,.0f}"
        
        return result
    except Exception as e:
        return f"Error generating forecast: {e}"


@tool
def summarize_insights(context: str = "") -> str:
    """Generate executive summary with key metrics and insights.
    
    Args:
        context: Optional context to include in summary
    
    Returns:
        Formatted executive summary with key business metrics
    
    Example: 'Summarize the analysis findings'
    """
    try:
        if not DATA_PATH.exists():
            return "Error: Sales data file not found."
        
        df = pd.read_csv(DATA_PATH)
        df["date"] = pd.to_datetime(df["date"])
        
        # Calculate key metrics
        total_revenue = df["amount"].sum()
        avg_revenue = df["amount"].mean()
        
        # Top product and region
        top_product = df.groupby("product")["amount"].sum().idxmax()
        top_region = df.groupby("region")["amount"].sum().idxmax()
        
        # Date range
        date_range = f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"
        total_records = len(df)
        
        # Detect anomalies using z-score
        z_scores = np.abs(stats.zscore(df["amount"]))
        anomalies = (z_scores > 3).sum()
        
        # Format executive summary
        result = "📋 EXECUTIVE SUMMARY\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"💰 Total Revenue: ${total_revenue:,.0f}\n"
        result += f"📊 Average Revenue: ${avg_revenue:,.0f}\n"
        result += f"🏆 Top Product: {top_product}\n"
        result += f"🌍 Top Region: {top_region}\n"
        result += f"⚠️  Anomalies Detected: {anomalies} records (z-score > 3)\n"
        result += f"📅 Date Range: {date_range}\n"
        result += f"📈 Total Records: {total_records}\n"
        
        if context:
            result += f"\n💡 Context: {context}\n"
        
        result += "\n✓ Analysis complete"
        
        return result
    except Exception as e:
        return f"Error generating summary: {e}"


def get_agent(verbose: bool = True):
    """Create and return the agent with tool calling."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    tools = [query_data, analyze_trends, detect_anomalies, generate_forecast, summarize_insights]
    # Bind tools to LLM for function calling
    return llm.bind_tools(tools)


def main() -> None:
    """Run the agent with a sample query."""
    from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
    
    agent_llm = get_agent()
    
    # Create a simple agent loop
    query = "Analyze last quarter's sales trends and summarize key insights."
    print(f"\n🤖 Query: {query}\n")
    
    messages = [HumanMessage(content=query)]
    response = agent_llm.invoke(messages)
    
    # Check if tools were called
    if response.tool_calls:
        print(f"🔧 Agent wants to use {len(response.tool_calls)} tool(s):\n")
        
        tool_map = {
            "query_data": query_data,
            "analyze_trends": analyze_trends,
            "detect_anomalies": detect_anomalies,
            "generate_forecast": generate_forecast,
            "summarize_insights": summarize_insights,
        }
        
        # Add AI response to messages
        messages.append(response)
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"  - {tool_name}({tool_args})")
            
            # Execute the tool
            tool_func = tool_map[tool_name]
            result = tool_func.invoke(tool_args)
            print(f"    Result: {result}\n")
            
            # Add tool result to messages
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        # Get final response
        final_response = agent_llm.invoke(messages)
        print(f"📊 Final Answer:\n{final_response.content if final_response.content else '[No content - checking tool calls again]'}")
        
        # If still calling tools, run one more iteration
        if final_response.tool_calls:
            print(f"\n🔧 Agent wants more tools: {[tc['name'] for tc in final_response.tool_calls]}\n")
            messages.append(final_response)
            for tool_call in final_response.tool_calls:
                tool_func = tool_map[tool_call["name"]]
                result = tool_func.invoke(tool_call["args"])
                print(f"  - {tool_call['name']}: {result}")
                messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
            
            # Final final response
            final_final = agent_llm.invoke(messages)
            print(f"\n📊 Final Answer:\n{final_final.content}")
    else:
        print(f"📊 Answer:\n{response.content}")


if __name__ == "__main__":
    main()
