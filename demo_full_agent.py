"""
Full 5-Tool Asset Management Agent Demo

Demonstrates comprehensive workflow: 
Query Assets → Analyze Health → Predict Failures → Calculate TCO → Track Compliance

Showcases the agent's ability to perform multi-step analysis and synthesize
insights across all asset management domains.
"""
from agent import (
    get_agent,
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance,
)
from langchain_core.messages import HumanMessage, ToolMessage


def run_full_demo():
    """Demonstrate all 5 asset management tools in a comprehensive analysis."""
    print("\n" + "="*80)
    print("🚀 FULL 5-TOOL ASSET MANAGEMENT AGENT DEMO")
    print("="*80)
    
    agent_llm = get_agent()
    tool_map = {
        "query_assets": query_assets,
        "analyze_asset_health": analyze_asset_health,
        "predict_failures": predict_failures,
        "calculate_tco": calculate_tco,
        "track_compliance": track_compliance,
    }
    
    # Complex query that exercises multiple tools
    query = (
        "Perform a comprehensive asset portfolio analysis: "
        "query all assets, analyze health trends, predict failures for the next quarter, "
        "calculate total cost of ownership over 5 years, and check compliance status."
    )
    
    print(f"\n🤖 Query:\n{query}\n")
    print("="*80)
    
    messages = [HumanMessage(content=query)]
    response = agent_llm.invoke(messages)
    
    iteration = 0
    max_iterations = 10  # Allow multiple tool rounds for comprehensive analysis
    
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
            
            print(f"  📤 Result: {result[:200]}..." if len(result) > 200 else f"  📤 Result: {result}")
            
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        response = agent_llm.invoke(messages)
    
    # Show final comprehensive analysis
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE ANALYSIS COMPLETE")
    print("="*80)
    print(response.content if response.content else "[No final response]")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    try:
        run_full_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Exiting.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Ensure OPENAI_API_KEY is set in .env and asset_data.csv exists.\n")
