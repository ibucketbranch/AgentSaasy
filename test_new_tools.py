"""Test new tools: generate_forecast and summarize_insights"""
from agent import generate_forecast, summarize_insights

print("="*80)
print("🧪 TESTING NEW TOOLS")
print("="*80)

print("\n1️⃣ Testing generate_forecast (4 weeks):")
print("-"*80)
result1 = generate_forecast.invoke({"periods": 4})
print(result1)

print("\n2️⃣ Testing summarize_insights:")
print("-"*80)
result2 = summarize_insights.invoke({"context": "Full data analysis"})
print(result2)

print("\n3️⃣ Testing generate_forecast (8 weeks):")
print("-"*80)
result3 = generate_forecast.invoke({"periods": 8})
print(result3)

print("\n" + "="*80)
print("✅ ALL NEW TOOLS WORKING!")
print("="*80)
