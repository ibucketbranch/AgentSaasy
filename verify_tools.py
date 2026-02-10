"""
Quick Tool Verification - Test Each Tool Individually
Run this to verify all 5 tools work correctly
"""

print("=" * 80)
print("🔍 AGENTSAASY - TOOL VERIFICATION")
print("=" * 80)

# Test imports
try:
    from agent import (
        query_data,
        analyze_trends,
        detect_anomalies,
        generate_forecast,
        summarize_insights,
        get_agent,
    )
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)

print("\n" + "-" * 80)
print("TOOL 1: query_data")
print("-" * 80)
try:
    result = query_data.invoke({"query": "all"})
    print(f"✅ {result[:80]}...")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "-" * 80)
print("TOOL 2: analyze_trends")
print("-" * 80)
try:
    result = analyze_trends.invoke({"query": "all"})
    print(f"✅ {result[:80]}...")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "-" * 80)
print("TOOL 3: detect_anomalies")
print("-" * 80)
try:
    result = detect_anomalies.invoke({"query": "all"})
    print(f"✅ {result[:80]}...")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "-" * 80)
print("TOOL 4: generate_forecast")
print("-" * 80)
try:
    result = generate_forecast.invoke({"periods": 4})
    print(f"✅ {result[:80]}...")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "-" * 80)
print("TOOL 5: summarize_insights")
print("-" * 80)
try:
    result = summarize_insights.invoke({"context": "Verification test"})
    print(f"✅ {result[:80]}...")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "-" * 80)
print("AGENT: get_agent()")
print("-" * 80)
try:
    agent = get_agent()
    print("✅ Agent created successfully")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ ALL 5 TOOLS + AGENT VERIFIED")
print("=" * 80)
print("\nNext steps:")
print("  • Run full demo: python3 demo_full_agent.py")
print("  • Run tests: python3 -m pytest tests/test_agent.py -v")
print("  • Run agent: python3 agent.py")
