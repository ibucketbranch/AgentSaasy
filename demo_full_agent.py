"""
Full 5-Tool Enterprise Agent Demo
Shows complete workflow: Query → Analyze → Detect → Forecast → Summarize
"""
from agent import get_agent, query_data, analyze_trends, detect_anomalies, generate_forecast, summarize_insights
from langchain_core.messages import HumanMessage, ToolMessage

def run_full_demo():
    """Demonstrate all 5 tools in a comprehensive analysis."""
    print("\n" + "="*80)
    print("🚀 FULL 5-TOOL ENTERPRISE AGENT DEMO")
    print("="*80)
    
    agent_llm = get_agent()
    tool_map = {
        "query_data": query_data,
        "analyze_trends": analyze_trends,
        "detect_anomalies": detect_anomalies,
        "generate_forecast": generate_forecast,
        "summarize_insights": summarize_insights,
    }
    
    # Complex query that should use multiple tools
    query = "Perform a comprehensive analysis: query all sales data, analyze trends, check for anomalies, forecast the next 4 weeks, and provide an executive summary"
    
    print(f"\n🤖 Query:\n{query}\n")
    print("="*80)
    
    messages = [HumanMessage(content=query)]
    response = agent_llm.invoke(messages)
    
    iteration = 0
    max_iterations = 10
    
    while response.tool_calls and iteration < max_iterations:
        iteration += 1
        print(f"\n🔧 Iteration {iteration} - Calling {len(response.tool_calls)} tool(s):")
        print("-"*80)
        
        messages.append(response)
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"\n  📌 Tool: {tool_name}")
            print(f"  📥 Args: {tool_args}")
            
            tool_func = tool_map[tool_name]
            result = tool_func.invoke(tool_args)
            
            print(f"  📤 Result:\n")
            # Indent the result for readability
            for line in result.split('\n'):
                print(f"     {line}")
            
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        response = agent_llm.invoke(messages)
    
    print("\n" + "="*80)
    print("📊 FINAL ANSWER:")
    print("="*80)
    print(response.content if response.content else "[No content generated]")
    print("\n" + "="*80)
    print(f"✅ DEMO COMPLETE - {iteration} iterations, {iteration * len(response.tool_calls) if iteration > 0 else 0} tool calls")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_full_demo()
