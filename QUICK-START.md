# AgentSaasy_NGAI Quick Start Guide

**Enterprise Asset Management AI Agent** - 7 tools, ready to demo

---

## Clone & Run (2 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/ibucketbranch/AgentSaasy_NGAI.git
cd AgentSaasy_NGAI

# 2. Create virtual environment & install dependencies
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 3. Add your OpenAI API key
cp .env.example .env
# Edit .env and replace "your-openai-key-here" with your actual key
# Get a key at: https://platform.openai.com/api-keys

# 4. Verify everything works
python3 -m pytest tests/test_agent.py -v

# 5. Run the demo
python3 chat_agent.py
```

That's it. You're live.

---

## Demo Options

### Interactive Chat (best for live demos)
```bash
python3 chat_agent.py
```
Type questions in plain English. Try:
- `Optimize routes for 30 work orders across 8 technicians`
- `Which assets are at risk of failure next quarter?`
- `Calculate TCO for all pumps over 5 years`
- `Create a 10-year capital plan with $5M annual budget`
- `Check compliance status`

### Full 7-Tool Demo (automated showcase)
```bash
python3 demo_full_agent.py
```
Fires one query that triggers 5+ tools in parallel and synthesizes an executive report.

### GIS Route Optimization Demo
```bash
python3 demo_gis_optimization.py
```
Interactive menu with 6 scenarios showing route optimization and ROI analysis.

### Single Query
```bash
python3 agent.py
```

---

## The 7 Tools

| Tool | Purpose | Example Query |
|------|---------|---------------|
| `query_assets` | Filter asset inventory | "Show critical assets in Building A" |
| `analyze_asset_health` | Health trend analysis | "What's the average health score?" |
| `predict_failures` | Predictive maintenance (60-90 day forecast) | "Which assets will fail next quarter?" |
| `calculate_tco` | Financial analysis | "Calculate TCO for pumps over 5 years" |
| `track_compliance` | Regulatory monitoring | "Check inspection compliance status" |
| `optimize_field_routes` | GIS route optimization | "Optimize routes for 20 work orders across 5 techs" |
| `plan_capital_strategy` | Capital planning & scenario modeling | "Create a 10-year capital plan with $5M budget" |

---

## Project Structure

```
AgentSaasy_NGAI/
├── agent.py                    # Main agent with 7 tools
├── chat_agent.py               # Interactive chat interface
├── demo_full_agent.py          # Full 7-tool demo
├── demo_gis_optimization.py    # GIS optimization demos
├── demo_capital_planning.py    # Capital planning demos
├── ask_agent.py                # Single query demo
├── test_queries.py             # Integration tests
├── tests/
│   └── test_agent.py           # 34 unit tests
├── data/
│   └── asset_data.csv          # 50 sample assets (included)
├── .env.example                # API key template
├── requirements.txt            # Python dependencies
├── SETUP.md                    # Detailed setup guide
├── GIS-OPTIMIZATION-GUIDE.md   # GIS feature documentation
├── TOOLS-REFERENCE.md          # All 7 tools reference
└── PROJECT-DICTIONARY.md       # Asset management terminology
```

---

## Requirements

- **Python 3.10+**
- **OpenAI API key** (GPT-4o-mini, ~$0.001 per query)
- No other external services needed -- sample data ships with the repo

---

## Performance

- **Tests:** 34 passing (100% coverage)
- **Latency:** 2-15s per query depending on tool count
- **Cost:** $0.0004 - $0.0012 per query (GPT-4o-mini)
- **Accuracy:** Deterministic (temperature=0)

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "OpenAI API key not found"
```bash
# Make sure .env exists with your key
cat .env
# Should show: OPENAI_API_KEY=sk-proj-...
```

### "Asset data file not found"
The file `data/asset_data.csv` ships with the repo. If missing:
```bash
git checkout -- data/asset_data.csv
```

### Python version error
Use `python3` instead of `python` (macOS ships with Python 2.7 as `python`).

---

## Business Value

| Capability | Impact |
|------------|--------|
| Predictive Maintenance | 60-90 day failure prediction, 30-50% less downtime |
| Financial Analysis | TCO/ROI modeling, budget planning |
| Compliance Automation | Inspection tracking, audit readiness |
| GIS Route Optimization | 20-40% drive time reduction, $100K-150K annual savings |
| Capital Planning | Monte Carlo simulation, scenario modeling |
| Natural Language | No technical expertise required |

**Combined annual value:** $1.2M - $5.5M for typical enterprise customer

---

**Last Updated:** February 10, 2026
**Version:** 1.1.0 (7 tools)
**Built for:** NexGen Asset Management Platform
