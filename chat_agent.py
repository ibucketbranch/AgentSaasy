"""
Interactive AgentSaasy - Chat with the 5-Tool Agent
Run this to have a conversation with the agent!
"""
from agent import get_agent, query_data, analyze_trends, detect_anomalies, generate_forecast, summarize_insights
from langchain_core.messages import HumanMessage, ToolMessage

def chat_with_agent():
    """Interactive chat session with the agent."""
    print("\n" + "="*80)
    print("💬 INTERACTIVE AGENTSAASY - 5-TOOL ENTERPRISE AGENT")
    print("="*80)
    print("\nAvailable capabilities:")
    print("  • Query sales data (by product, region, date)")
    print("  • Analyze trends and growth rates")
    print("  • Detect anomalies in data")
    print("  • Generate forecasts (weekly predictions)")
    print("  • Create executive summaries")
    print("\nExample questions:")
    print("  - 'Show me all Widget A sales'")
    print("  - 'What are the sales trends?'")
    print("  - 'Forecast the next 8 weeks'")
    print("  - 'Give me an executive summary'")
    print("  - 'Analyze Q1 sales and detect anomalies'")
    print("\nType 'quit' or 'exit' to end the conversation")
    print("="*80 + "\n")
    
    # Initialize agent
    agent_llm = get_agent()
    tool_map = {
        "query_data": query_data,
        "analyze_trends": analyze_trends,
        "detect_anomalies": detect_anomalies,
        "generate_forecast": generate_forecast,
        "summarize_insights": summarize_insights,
    }
    
    # Chat loop
    while True:
        # Get user input
        user_input = input("🧑 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Thanks for chatting! Goodbye!\n")
            break
        
        print(f"\n🤖 Agent: Processing your request...\n")
        
        # Process query
        messages = [HumanMessage(content=user_input)]
        response = agent_llm.invoke(messages)
        
        # Handle tool calls
        iteration = 0
        max_iterations = 5
        
        while response.tool_calls and iteration < max_iterations:
            iteration += 1
            messages.append(response)
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                print(f"   🔧 Using tool: {tool_name}")
                
                tool_func = tool_map[tool_name]
                result = tool_func.invoke(tool_args)
                
                messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
            
            response = agent_llm.invoke(messages)
        
        # Show final answer
        print(f"\n📊 Answer:\n{response.content if response.content else '[No response]'}\n")
        print("-"*80 + "\n")


if __name__ == "__main__":
    try:
        chat_with_agent()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
