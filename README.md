# AgentSaasy - 5-Tool Enterprise Analytics Agent

> **ARCHIVED.** This project continued as [AgentSaasy_NGAI](https://github.com/ibucketbranch/AgentSaasy_NGAI), an enterprise asset management agent built on this codebase. All active development, including the 7-tool agent, GIS route optimization, capital planning, and the AEQ experiments, lives there. This repo is kept read-only for reference.

**A production-ready AI agent for enterprise data analysis with forecasting and executive reporting.**

---

## ✨ What It Does

Natural language queries powered by 5 specialized tools:
- 📊 **Query Data** - Filter sales by product, region, or date
- 📈 **Analyze Trends** - Calculate growth rates and patterns
- ⚠️ **Detect Anomalies** - Find unusual data points (z-score)
- 🔮 **Generate Forecasts** - Predict future sales (LinearRegression)
- 📋 **Summarize Insights** - Create executive summaries

---

## 🚀 Quick Start

```bash
# Setup
source venv/bin/activate
pip install -r requirements-working.txt

# Try it!
python3 chat_agent.py                              # Interactive chat
python3 ask_agent.py "forecast next 4 weeks"       # Single question
python3 demo_full_agent.py                         # Full demo
```

---

## 📚 Documentation

| Guide | Purpose |
|-------|---------|
| **HOW-TO-USE.md** | 3 ways to interact with the agent |
| **README-5-TOOLS.md** | Complete feature guide |
| **TERMINAL-COMMANDS.md** | Quick command reference |
| **PROJECT-DICTIONARY.md** | 60+ terms explained |
| **SETUP.md** | API keys & Cursor configuration |

---

## ✅ Status

- **Tools:** 5/5 implemented ✅
- **Tests:** 22/22 passing ✅
- **Documentation:** Complete ✅
- **Repository:** https://github.com/ibucketbranch/AgentSaasy

---

**Get started:** See [HOW-TO-USE.md](./HOW-TO-USE.md) for interactive examples!
