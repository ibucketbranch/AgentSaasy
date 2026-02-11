"""
Single Query Demo - Asset Management Agent in Action
Ask one question and watch the agent analyze assets step-by-step.

Demonstrates agent reasoning, tool selection, and synthesized insights
for enterprise asset management scenarios.
"""
import sys
from agent import (
    get_agent,
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance,
)
from langchain_core.messages import HumanMessage, ToolMessage


def ask_agent(query: str):
    """Ask the agent a single asset management question with detailed output.
    
    Args:
        query: Natural language question about assets, maintenance, or compliance
    
    Shows step-by-step tool execution and reasoning process.
    """
    print("\n" + "="*80)
    print("🤖 AGENTSAASY_NGAI - SINGLE QUERY DEMO")
    print("="*80)
    print(f"\n🧑 Your Question:")
    print(f"   {query}")
    print("\n" + "-"*80)
    
    # Initialize asset management agent
    agent_llm = get_agent()
    tool_map = {
        "query_assets": query_assets,
        "analyze_asset_health": analyze_asset_health,
        "predict_failures": predict_failures,
        "calculate_tco": calculate_tco,
        "track_compliance": track_compliance,
    }
    
    print("\n🤖 Agent: Analyzing your request...\n")
    
    # Process query
    messages = [HumanMessage(content=query)]
    response = agent_llm.invoke(messages)
    
    # Handle tool execution with detailed output
    iteration = 0
    max_iterations = 5
    
    while response.tool_calls and iteration < max_iterations:
        iteration += 1
        print(f"💭 Step {iteration}: Agent selected {len(response.tool_calls)} tool(s):\n")
        
        messages.append(response)
        
        for i, tool_call in enumerate(response.tool_calls, 1):
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            print(f"   🔧 Tool {i}: {tool_name}")
            print(f"   📥 Input: {tool_args}")
            
            tool_func = tool_map[tool_name]
            result = tool_func.invoke(tool_args)
            
            print(f"   📤 Output: {result}\n")
            
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        response = agent_llm.invoke(messages)
    
    # Show final synthesized answer
    print("="*80)
    print("\n📊 Final Analysis:")
    print(response.content if response.content else "[No response generated]")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    # Default demo query
    default_query = "Which assets are at risk of failure in the next quarter?"
    
    # Allow custom query from command line
    query = sys.argv[1] if len(sys.argv) > 1 else default_query
    
    try:
        ask_agent(query)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Exiting.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Ensure OPENAI_API_KEY is set in .env and asset_data.csv exists.\n")
