#!/usr/bin/env python3
"""
Demo script for Capital Planning & Scenario Modeling feature.

This demonstrates the strategic AI capability for municipal finance teams
to perform multi-year capital planning with Monte Carlo simulation.
"""

from langchain_core.messages import HumanMessage, ToolMessage
from agent import get_agent

def demo_capital_planning():
    """Run capital planning demo scenarios."""
    
    agent_llm = get_agent()
    
    # Demo Scenario 1: Basic 10-year capital plan
    print("=" * 80)
    print("DEMO SCENARIO 1: 10-Year Capital Plan with $5M Annual Budget")
    print("=" * 80)
    
    query1 = """Create a comprehensive 10-year capital replacement plan with a $5 million 
    annual budget. Compare different strategies and recommend the optimal approach 
    for our municipal asset portfolio."""
    
    print(f"\n🤖 Query: {query1}\n")
    
    messages = [HumanMessage(content=query1)]
    response = agent_llm.invoke(messages)
    
    if response.tool_calls:
        print(f"🔧 Agent selected tool: {response.tool_calls[0]['name']}\n")
        
        tool_map = {
            "plan_capital_strategy": __import__('agent').plan_capital_strategy,
        }
        
        messages.append(response)
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"📊 Executing: {tool_name}({tool_args})\n")
            
            tool_func = tool_map.get(tool_name, lambda x: "Tool not found")
            result = tool_func.invoke(tool_args)
            print(result)
            print("\n")
            
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        # Get final synthesized response
        final_response = agent_llm.invoke(messages)
        print(f"\n📋 AI Executive Summary:\n{final_response.content}\n")
    else:
        print(f"📊 Response:\n{response.content}")
    
    # Demo Scenario 2: Budget-constrained scenario
    print("\n" + "=" * 80)
    print("DEMO SCENARIO 2: Budget-Constrained Scenario ($3M Annual Budget)")
    print("=" * 80)
    
    query2 = """Our city council reduced the capital budget to $3 million per year. 
    Run a capital planning analysis showing how we can optimize our replacement 
    strategy within this tighter budget constraint."""
    
    print(f"\n🤖 Query: {query2}\n")
    
    messages2 = [HumanMessage(content=query2)]
    response2 = agent_llm.invoke(messages2)
    
    if response2.tool_calls:
        messages2.append(response2)
        
        for tool_call in response2.tool_calls:
            tool_func = tool_map.get(tool_call["name"], lambda x: "Tool not found")
            result = tool_func.invoke(tool_call["args"])
            print(result)
            print("\n")
            
            messages2.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        final_response2 = agent_llm.invoke(messages2)
        print(f"\n📋 AI Executive Summary:\n{final_response2.content}\n")
    
    # Demo Scenario 3: Aggressive preventive strategy
    print("\n" + "=" * 80)
    print("DEMO SCENARIO 3: Aggressive Preventive Strategy Analysis")
    print("=" * 80)
    
    query3 = """The city council wants to minimize failure risk after last year's 
    emergency repairs. Analyze an aggressive preventive replacement strategy 
    over 10 years and show the cost-benefit trade-offs."""
    
    print(f"\n🤖 Query: {query3}\n")
    
    messages3 = [HumanMessage(content=query3)]
    response3 = agent_llm.invoke(messages3)
    
    if response3.tool_calls:
        messages3.append(response3)
        
        for tool_call in response3.tool_calls:
            tool_func = tool_map.get(tool_call["name"], lambda x: "Tool not found")
            result = tool_func.invoke(tool_call["args"])
            print(result)
            print("\n")
            
            messages3.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        
        final_response3 = agent_llm.invoke(messages3)
        print(f"\n📋 AI Executive Summary:\n{final_response3.content}\n")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE - Capital Planning & Scenario Modeling")
    print("=" * 80)
    print("\n💡 Key Capabilities Demonstrated:")
    print("  ✓ Monte Carlo simulation (1000 iterations per strategy)")
    print("  ✓ Multi-strategy comparison (4 scenarios)")
    print("  ✓ Uncertainty quantification (P10/P50/P90 distributions)")
    print("  ✓ Risk-based asset prioritization")
    print("  ✓ Budget constraint optimization")
    print("  ✓ Executive-level recommendations")
    print("  ✓ Multi-year replacement schedules")
    print("  ✓ ROI and business impact analysis")
    print("\n🎯 Business Value:")
    print("  • CFO/Finance Director decision support")
    print("  • Data-driven recommendations for city council")
    print("  • Quantified uncertainty (not just point estimates)")
    print("  • Defensible methodology for audits")
    print("  • $1M-5M annual savings for typical municipal customers")
    print("\n🏛️ NexGen Positioning:")
    print("  • Elevates NexGen from tactical CMMS to strategic planning tool")
    print("  • Complements existing Capital Planning module with AI scenarios")
    print("  • Differentiates from IBM Maximo, SAP (no AI scenario modeling)")
    print("  • Targets executive buyers (Finance Directors, City Managers)")
    print()

if __name__ == "__main__":
    demo_capital_planning()
