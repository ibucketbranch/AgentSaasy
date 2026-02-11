"""
Interactive AgentSaasy_NGAI - Chat with the Asset Management Agent

Real-time conversational interface for enterprise asset management analysis.
Demonstrates natural language interaction with predictive maintenance, compliance,
TCO analysis, GIS route optimization, and strategic capital planning capabilities.

Designed for NexGen Asset Management platform demonstrations.
"""
from agent import (
    get_agent,
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance,
    optimize_field_routes,
    plan_capital_strategy,
)
from langchain_core.messages import HumanMessage, ToolMessage


def chat_with_agent():
    """Interactive chat session with the asset management agent.
    
    Enables natural language queries for:
    - Asset portfolio analysis
    - Predictive maintenance insights
    - Compliance monitoring
    - TCO calculations
    - GIS route optimization
    - Capital planning & scenario modeling
    - Executive reporting
    """
    print("\n" + "="*80)
    print("💬 AGENTSAASY_NGAI - ENTERPRISE ASSET MANAGEMENT AI AGENT")
    print("="*80)
    print("\nCapabilities:")
    print("  • Query assets (by type, location, health status)")
    print("  • Analyze health trends and deterioration patterns")
    print("  • Predict failures 60-90 days ahead")
    print("  • Calculate Total Cost of Ownership (TCO)")
    print("  • Track regulatory compliance status")
    print("  • Optimize field service routes (GIS-powered)")
    print("  • Capital planning with Monte Carlo simulation (NEW)")
    print("\nExample questions:")
    print("  - 'Show me all critical assets in Building A'")
    print("  - 'What assets are at risk of failure?'")
    print("  - 'Calculate TCO for all pumps over 5 years'")
    print("  - 'Check compliance status for pressure vessels'")
    print("  - 'Optimize routes for 30 work orders across 8 technicians'")
    print("  - 'Create a 10-year capital plan with $5M annual budget'")
    print("  - 'Compare replacement strategies for our aging infrastructure'")
    print("\nType 'quit' or 'exit' to end the conversation")
    print("="*80 + "\n")
    
    # Initialize agent with all asset management tools
    agent_llm = get_agent()
    tool_map = {
        "query_assets": query_assets,
        "analyze_asset_health": analyze_asset_health,
        "predict_failures": predict_failures,
        "calculate_tco": calculate_tco,
        "track_compliance": track_compliance,
        "optimize_field_routes": optimize_field_routes,
        "plan_capital_strategy": plan_capital_strategy,
    }
    
    # Interactive chat loop
    while True:
        # Get user input
        user_input = input("🧑 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Thank you for using AgentSaasy_NGAI. Goodbye!\n")
            break
        
        print(f"\n🤖 Agent: Analyzing your request...\n")
        
        # Process natural language query
        messages = [HumanMessage(content=user_input)]
        response = agent_llm.invoke(messages)
        
        # Handle multi-turn tool execution
        iteration = 0
        max_iterations = 5  # Prevent infinite loops
        
        while response.tool_calls and iteration < max_iterations:
            iteration += 1
            messages.append(response)
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                print(f"   🔧 Executing: {tool_name}")
                
                tool_func = tool_map[tool_name]
                result = tool_func.invoke(tool_args)
                
                messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
            
            # Get next response (may call more tools or provide final answer)
            response = agent_llm.invoke(messages)
        
        # Display final synthesized answer
        print(f"\n📊 Analysis:\n{response.content if response.content else '[No response generated]'}\n")
        print("-"*80 + "\n")


if __name__ == "__main__":
    try:
        chat_with_agent()
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Ensure OPENAI_API_KEY is set in .env file and asset_data.csv exists.\n")
