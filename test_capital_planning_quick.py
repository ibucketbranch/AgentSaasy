#!/usr/bin/env python3
"""
Quick test of Capital Planning feature with reduced iterations.
"""

from agent import plan_capital_strategy

# Test with just 100 iterations for speed
print("Testing Capital Planning with 100 Monte Carlo iterations...\n")

result = plan_capital_strategy.invoke({
    "planning_horizon_years": 10,
    "annual_budget": 5000000,
    "strategy_preference": "balanced",
    "monte_carlo_iterations": 100  # Reduced for quick test
})

print(result)
print("\n✅ Capital Planning feature test complete!")
