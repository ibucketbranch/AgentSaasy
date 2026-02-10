# 🗣️ HOW TO INTERACT WITH AGENTSAASY

## 3 Ways to Use the Agent

---

## 🎯 Method 1: Interactive Chat (RECOMMENDED)

**Best for:** Having a conversation, asking multiple questions

```bash
python3 chat_agent.py
```

### What You'll See:
```
💬 INTERACTIVE AGENTSAASY - 5-TOOL ENTERPRISE AGENT

Available capabilities:
  • Query sales data (by product, region, date)
  • Analyze trends and growth rates
  • Detect anomalies in data
  • Generate forecasts (weekly predictions)
  • Create executive summaries

🧑 You: _
```

### Example Conversation:
```
🧑 You: Show me Widget A sales

🤖 Agent: Processing your request...
   🔧 Using tool: query_data

📊 Answer:
Found 12 records for Widget A. Total amount: $18,810.00.

🧑 You: Now forecast the next 4 weeks

🤖 Agent: Processing your request...
   🔧 Using tool: generate_forecast

📊 Answer:
🔮 Forecast (Linear Regression, R²=0.368):
  • Week 1: $1,642
  • Week 2: $1,687
  ...

🧑 You: quit

👋 Thanks for chatting! Goodbye!
```

---

## 🎯 Method 2: Single Question (Step-by-Step)

**Best for:** Seeing exactly what the agent does, debugging

```bash
python3 ask_agent.py "your question here"
```

### What You'll See:
```
🤖 AGENTSAASY - SINGLE QUERY DEMO

🧑 Your Question:
   Forecast the next 4 weeks and summarize key insights

🤖 Agent: Let me process that...

💭 Step 1: Agent is using 2 tool(s):

   🔧 Tool 1: generate_forecast
   📥 Input: {'periods': 4}
   📤 Output: 🔮 Forecast (Linear Regression, R²=0.368)...

   🔧 Tool 2: summarize_insights
   📥 Input: {}
   📤 Output: 📋 EXECUTIVE SUMMARY...

📊 FINAL ANSWER:
[Complete formatted answer with all insights]
```

### Example Questions:
```bash
# Forecasting
python3 ask_agent.py "Forecast the next 8 weeks"
python3 ask_agent.py "Predict next month's revenue"

# Querying
python3 ask_agent.py "Show me Widget A sales"
python3 ask_agent.py "What are North region sales?"
python3 ask_agent.py "Show Q1 2024 sales"

# Analysis
python3 ask_agent.py "What are the sales trends?"
python3 ask_agent.py "Analyze growth rates"

# Anomalies
python3 ask_agent.py "Check for anomalies"
python3 ask_agent.py "Find unusual sales patterns"

# Summaries
python3 ask_agent.py "Give me an executive summary"
python3 ask_agent.py "Summarize all sales data"

# Complex Queries
python3 ask_agent.py "Analyze trends, detect anomalies, and forecast next quarter"
python3 ask_agent.py "Compare regions and predict future sales"
```

---

## 🎯 Method 3: Full Automated Demo

**Best for:** Seeing the complete workflow with all 5 tools

```bash
python3 demo_full_agent.py
```

### What It Does:
Runs a comprehensive analysis automatically:
1. Queries all sales data
2. Analyzes trends
3. Detects anomalies
4. Generates forecasts
5. Creates executive summary
6. Produces complete markdown report

**No input required** - just watch it work!

---

## 📝 What Questions Can You Ask?

### Data Queries
- "Show me all Widget A sales"
- "What are North region sales?"
- "Display Q1 2024 data"
- "Find sales for Product X in Region Y"

### Trend Analysis
- "What are the sales trends?"
- "Calculate growth rates"
- "Show monthly averages"
- "How is revenue trending?"

### Anomaly Detection
- "Check for anomalies"
- "Find unusual sales patterns"
- "Are there any outliers?"
- "Detect irregular data"

### Forecasting
- "Forecast the next 4 weeks"
- "Predict next month's sales"
- "Project Q2 revenue"
- "Generate 8-week forecast"

### Summaries
- "Give me an executive summary"
- "Summarize all data"
- "Show key metrics"
- "Create a business report"

### Complex Multi-Tool Queries
- "Analyze Q1 sales, detect anomalies, and forecast Q2"
- "Compare all regions and predict next quarter"
- "Show trends, check for outliers, and summarize findings"
- "Full analysis with forecast and executive summary"

---

## 🎮 Try It Now!

### Quick Start (Interactive):
```bash
cd /path/to/AgentSaasy
source venv/bin/activate
python3 chat_agent.py
```

Then type any question!

### Quick Start (Single Query):
```bash
python3 ask_agent.py "Forecast the next 4 weeks"
```

### Quick Start (Full Demo):
```bash
python3 demo_full_agent.py
```

---

## 🔧 Behind the Scenes

When you ask a question, the agent:

1. **Understands** your natural language query
2. **Decides** which tools to use
3. **Calls** the appropriate tools
4. **Chains** multiple tools if needed
5. **Synthesizes** results into a coherent answer

### Example Flow:
```
You: "Analyze sales and forecast next month"
  ↓
Agent thinks: "I need to query data, analyze trends, and forecast"
  ↓
Step 1: Calls query_data → Gets sales data
Step 2: Calls analyze_trends → Calculates growth
Step 3: Calls generate_forecast → Predicts future
  ↓
Agent: [Comprehensive answer with all insights]
```

---

## 🎯 Use Cases

### Sales Team
```bash
python3 ask_agent.py "Show this month's top products"
python3 ask_agent.py "Forecast next quarter's revenue"
```

### Management
```bash
python3 ask_agent.py "Give me an executive summary"
python3 ask_agent.py "Analyze performance and predict trends"
```

### Data Analysis
```bash
python3 chat_agent.py
# Then explore interactively:
# - "Show regional breakdown"
# - "Find anomalies"
# - "Compare products"
```

### Reporting
```bash
python3 demo_full_agent.py > report.txt
# Generates complete analysis report
```

---

## ✅ Tips for Best Results

### ✅ DO:
- Ask clear, specific questions
- Use natural language
- Request multiple analyses in one query
- Try the interactive mode for exploration

### ❌ DON'T:
- Don't ask questions about data you don't have
- Don't expect the agent to modify data (read-only)
- Don't use technical jargon unnecessarily

---

## 🎉 You're Ready!

Start chatting with your AI agent:
```bash
python3 chat_agent.py
```

Or try a quick question:
```bash
python3 ask_agent.py "What are the sales trends?"
```

**Have fun exploring your data with AI! 🚀**
