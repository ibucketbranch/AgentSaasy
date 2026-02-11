"""
Comprehensive Testing - Various Asset Management Query Scenarios

Manual testing suite for validating agent responses across different
asset management use cases and query patterns.
"""
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from agent import (
    get_agent,
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance,
)

load_dotenv()


def run_query(agent_llm, query: str, tool_map: dict) -> None:
    """Run a single query and display detailed results.
    
    Args:
        agent_llm: Initialized agent with tools bound
        query: Natural language query to test
        tool_map: Mapping of tool names to tool functions
    """
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
    """Run comprehensive test queries covering all asset management scenarios."""
    print("\n" + "="*80)
    print("🚀 COMPREHENSIVE ASSET MANAGEMENT AGENT TESTING")
    print("="*80)
    
    agent_llm = get_agent()
    tool_map = {
        "query_assets": query_assets,
        "analyze_asset_health": analyze_asset_health,
        "predict_failures": predict_failures,
        "calculate_tco": calculate_tco,
        "track_compliance": track_compliance,
    }
    
    # Test scenarios covering different use cases
    test_queries = [
        # Asset querying
        "Show me all critical assets in Building A",
        
        # Health analysis
        "What is the average health score of our pumps?",
        
        # Predictive maintenance
        "Which assets are likely to fail in the next 60 days?",
        
        # Financial analysis
        "Calculate the total cost of ownership for all HVAC systems over 5 years",
        
        # Compliance monitoring
        "Are we compliant with inspection requirements?",
        
        # Complex multi-tool query
        "Analyze high-risk assets, predict failures, and recommend maintenance priorities",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'#'*80}")
        print(f"TEST {i}/{len(test_queries)}")
        print('#'*80)
        run_query(agent_llm, query, tool_map)
    
    print("\n\n" + "="*80)
    print("✅ ALL TESTS COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted. Exiting.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Ensure OPENAI_API_KEY is set in .env and asset_data.csv exists.\n")
