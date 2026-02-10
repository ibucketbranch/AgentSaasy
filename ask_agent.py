"""
Single Query Demo - See the Agent Work Step-by-Step
Ask one question and watch the agent think and use tools!
"""
import sys
from agent import get_agent, query_data, analyze_trends, detect_anomalies, generate_forecast, summarize_insights
from langchain_core.messages import HumanMessage, ToolMessage

def ask_agent(query: str):
    """Ask the agent a single question with detailed output."""
    print("\n" + "="*80)
    print("🤖 AGENTSAASY - SINGLE QUERY DEMO")
    print("="*80)
    print(f"\n🧑 Your Question:")
    print(f"   {query}")
    print("\n" + "-"*80)
    
    # Initialize agent
    agent_llm = get_agent()
    tool_map = {
        "query_data": query_data,
        "analyze_trends": analyze_trends,
        "detect_anomalies": detect_anomalies,
        "generate_forecast": generate_forecast,
        "summarize_insights": summarize_insights,
    }
    
    print("\n🤖 Agent: Let me process that...\n")
    
    # Process query
    messages = [HumanMessage(content=query)]
    response = agent_llm.invoke(messages)
    
    # Handle tool calls
    iteration = 0
    max_iterations = 5
    
    while response.tool_calls and iteration < max_iterations:
        iteration += 1
        print(f"💭 Step {iteration}: Agent is using {len(response.tool_calls)} tool(s):\n")
        
        messages.append(response)
        
        for i, tool_call in enumerate(response.tool_calls, 1):
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            print(f"   🔧 Tool {i}: {tool_name}")
            print(f"   📥 Input: {tool_args}")
            
            tool_func = tool_map[tool_name]
            result = tool_func.invoke(tool_args)
            
            # Show first 150 chars of result
            result_preview = result[:150] + "..." if len(result) > 150 else result
            print(f"   📤 Output: {result_preview}\n")
            
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        response = agent_llm.invoke(messages)
    
    # Show final answer
    print("="*80)
    print("📊 FINAL ANSWER:")
    print("="*80)
    print(response.content if response.content else '[No response generated]')
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    # Check if query provided as command line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        # Default queries to try
        queries = [
            "Show me Widget A sales in the North region",
            "What are the sales trends?",
            "Forecast the next 6 weeks",
            "Give me an executive summary",
            "Analyze all sales and check for anomalies",
        ]
        
        print("\n" + "="*80)
        print("📋 EXAMPLE QUERIES YOU CAN TRY:")
        print("="*80)
        for i, q in enumerate(queries, 1):
            print(f"   {i}. {q}")
        print("\nUsage: python3 ask_agent.py 'your question here'")
        print("Or just run: python3 ask_agent.py (uses default query)")
        print("="*80 + "\n")
        
        # Use first query as default
        query = queries[0]
        print(f"Using default query: '{query}'\n")
    
    try:
        ask_agent(query)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
