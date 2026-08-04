# AgentSaaSy_EAM
AI-powered Agent for an asset intelligence platform showcasing predictive maintenance, cost optimization, and compliance automation for enterprise operations. 

## Repo - https://github.com/ibucketbranch/AgentSaaSy_EAM

> **Enterprise Asset Management AI Agent**  
> Demonstrating predictive maintenance, cost optimization, and compliance automation through intelligent analytics

AgentSaaSy_EAM is a proof-of-concept showcasing how enterprise asset management platforms can leverage AI to deliver measurable business value.

Designed specifically for the asset management domain, this intelligent agent demonstrates what's possible when you combine deep domain expertise, modern AI capabilities (GPT-4o), production-grade engineering, and focus on real business outcomes.

## What It Does

The agent analyzes asset portfolios to predict failures, optimize maintenance spend, ensure regulatory compliance, and provide executive insights - all through natural language conversation.

## Why It Matters

Asset-intensive industries spend 15-40% of operational budgets on maintenance. Even small improvements in prediction accuracy or scheduling efficiency translate to significant cost savings. This agent demonstrates how AI can augment human expertise with data-driven insights at scale.

## Key Capabilities

- **Predictive Failure Analysis** - Identify at-risk assets 60-90 days ahead
- **Financial Impact Modeling** - Calculate TCO, ROI, and cost avoidance scenarios
- **Compliance Automation** - Track inspections, certifications, and regulatory requirements
- **GIS Route Optimization** - Field service routing scenario model. Drive time reduction of 20-40% comes from industry-standard multipliers applied to a baseline, not from solving a real road network. See Section 6.7 of the technical white paper.
- **Capital Planning & Scenario Modeling** - Strategic AI for multi-year asset replacement planning with Monte Carlo simulation (NEW)
- **Natural Language Interface** - Query complex asset data using plain English
- **Multi-Asset Intelligence** - Analyze patterns across asset types, locations, and lifecycles

## Quick Start

```bash
# 1. Clone & setup
git clone https://github.com/ibucketbranch/AgentSaaSy_EAM.git
cd AgentSaaSy_EAM
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Add your API key
cp .env.example .env
# Edit .env -> paste your OpenAI API key (get one at https://platform.openai.com/api-keys)

# 3. Verify everything works
python3 -m pytest tests/ -q          # 56 tests, all should pass

# 4. Launch the interactive agent
python3 chat_agent.py
```

**Sample queries to try in the chat:**
- `Show me all critical assets in Building A`
- `Which assets are at risk of failure this quarter?`
- `Calculate TCO for all pumps over 5 years`
- `Optimize routes for 30 work orders across 8 technicians`
- `Create a 10-year capital plan with $5M annual budget`

> **Requirements:** Python 3.10+, OpenAI API key (GPT-4o-mini, ~$0.001/query).  
> Sample data (50 assets) ships with the repo, no database or external data needed.

See [SETUP.md](SETUP.md) for detailed configuration, Cursor IDE tips, and troubleshooting.

## Architecture

```
Layer 1: Reasoning     -> GPT-4o-mini with ReAct pattern
Layer 2: Tools         -> 7 specialized asset management tools
Layer 3: Orchestration -> LangChain tool binding
```

| Tool | Purpose |
|------|---------|
| `query_assets` | Filter assets by type, location, health status |
| `analyze_asset_health` | Health trends and risk analysis |
| `predict_failures` | 60-90 day failure forecasting |
| `calculate_tco` | Total Cost of Ownership financial analysis |
| `track_compliance` | Regulatory inspection tracking |
| `optimize_field_routes` | Field service routing scenario model (simulated, not live spatial solving) |
| `plan_capital_strategy` | Monte Carlo capital planning simulation |

Modular 3-layer architecture separates reasoning (AI decision-making), tools (domain-specific analytics), and orchestration (workflow management). This design enables rapid customization while maintaining stability, critical for R&D initiatives that need to prove value quickly.

**Built for:** R&D teams evaluating AI integration strategies, operations leaders seeking competitive advantage through technology, and organizations ready to move beyond basic dashboards into predictive intelligence.
