"""
Phase 2 Manual Testing - Various Query Scenarios
"""
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from agent import get_agent, query_data, analyze_trends, detect_anomalies, generate_forecast, summarize_insights

load_dotenv()

def run_query(agent_llm, query: str, tool_map: dict) -> None:
    """Run a single query and display results."""
    print(f"\n{'='*80}")
    print(f"🤖 Query: {query}")
    print('='*80)
    
    messages = [HumanMessage(content=query)]
    response = agent_llm.invoke(messages)
    
    iteration = 0
    max_iterations = 5
    
    while response.tool_calls and iteration < max_iterations:
        iteration += 1
        print(f"\n🔧 Iteration {iteration} - Agent calling {len(response.tool_calls)} tool(s):")
        
        messages.append(response)
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"  - {tool_name}({tool_args})")
            
            tool_func = tool_map[tool_name]
            result = tool_func.invoke(tool_args)
            print(f"    ✓ Result: {result}")
            
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        response = agent_llm.invoke(messages)
    
    print(f"\n📊 Final Answer:")
    print(response.content if response.content else "[No content generated]")


def main():
    """Run comprehensive test queries."""
    print("\n" + "="*80)
    print("🚀 PHASE 2: COMPREHENSIVE AGENT TESTING")
    print("="*80)
    
    agent_llm = get_agent()
    tool_map = {
        "query_data": query_data,
        "analyze_trends": analyze_trends,
        "detect_anomalies": detect_anomalies,
        "generate_forecast": generate_forecast,
        "summarize_insights": summarize_insights,
    }
    
    # Test 1: Simple query
    run_query(agent_llm, "What's the total sales for Widget A?", tool_map)
    
    # Test 2: Regional analysis
    run_query(agent_llm, "Compare sales between North and South regions", tool_map)
    
    # Test 3: Trend analysis
    run_query(agent_llm, "Show me the sales trends over time", tool_map)
    
    # Test 4: Anomaly detection
    run_query(agent_llm, "Are there any unusual sales patterns or outliers?", tool_map)
    
    # Test 5: Complex multi-tool query
    run_query(agent_llm, "Analyze Q2 sales, identify trends, and check for anomalies", tool_map)
    
    # Test 6: Forecast future sales
    run_query(agent_llm, "Generate a forecast for the next 4 weeks", tool_map)
    
    # Test 7: Executive summary
    run_query(agent_llm, "Provide an executive summary of all sales data", tool_map)
    
    # Test 8: Full workflow - All 5 tools
    run_query(agent_llm, "Analyze all sales data: query the data, analyze trends, detect anomalies, forecast next month, and provide an executive summary", tool_map)
    
    print("\n" + "="*80)
    print("✅ PHASE 2 TESTING COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
