# AgentSaasy_NGAI Setup Guide

**Enterprise Asset Management AI Agent** - Installation and Configuration

> ⚠️ **Do not paste this entire document into the terminal.**  
> Follow these instructions step-by-step. For command reference only, see `TERMINAL-COMMANDS.md`.

---

## API Keys Setup

### Required: OpenAI API Key

**This project uses GPT-4o-mini for cost-effective enterprise analysis:**

```bash
OPENAI_API_KEY=sk-proj-...  # Required for agent operation
```

**Important: API Usage Costs**
- **claude.ai subscription** ($20/month Pro) = Chat interface only
- **OpenAI API access** = Pay-per-use (separate billing, requires payment method)

### API Pricing

**OpenAI GPT-4o-mini** (optimized for this project):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- Free tier: $5 credit on signup
- **Typical asset query cost: ~$0.0006** (very affordable for enterprise)

**Cost estimates for asset management:**
| Usage | Queries | Estimated Cost |
|-------|---------|---------------|
| Development/Testing | 100 | $0.06 |
| Small deployment | 1,000 | $0.60 |
| Medium deployment | 10,000 | $6.00 |
| Enterprise monthly | 50,000 | $30.00 |

### Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy key to `.env` file: `OPENAI_API_KEY=sk-proj-...`
5. Add payment method after free $5 credit expires

### Alternative: Using Claude API (Optional)

To switch from OpenAI to Claude Sonnet 4, modify `agent.py`:

```python
# Replace in agent.py (line ~225):
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# With:
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

And install: `pip install langchain-anthropic`

**Note:** Claude is ~20x more expensive but may provide better reasoning for complex queries.

---

## Environment Setup

### 1. Create Virtual Environment

```bash
cd /path/to/AgentSaasy_NGAI
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies:**
- `langchain` - Agent framework
- `langchain-openai` - OpenAI integration
- `langchain-core` - Core LangChain components
- `pandas` - Data analysis
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning (forecasting)
- `scipy` - Statistical analysis
- `python-dotenv` - Environment variable management
- `pytest` - Testing framework

### 3. Configure API Keys

Create `.env` file in project root:

```bash
OPENAI_API_KEY=sk-proj-your-key-here
```

**Security best practices:**
- ✅ `.env` is in `.gitignore` (never committed)
- ✅ Use environment variables, not hardcoded keys
- ✅ Rotate keys periodically
- ❌ Never share API keys
- ❌ Never commit `.env` to git

### 4. Verify Installation

```bash
# Test imports
python3 -c "import langchain; import pandas; print('✅ All dependencies installed')"

# Run tests
python3 -m pytest tests/test_agent.py -v

# Expected: All tests pass
```

---

## Data Setup

### Asset Data Configuration

The agent requires asset portfolio data in CSV format:

**Required structure** (`data/asset_data.csv`):
```csv
asset_id,asset_type,location,health_score,health_status,last_maintenance,acquisition_cost,annual_maintenance_cost,last_inspection
PUMP-001,Pump,Building A,85,Good,2024-01-15,25000,1250,2024-02-01
HVAC-012,HVAC,Building B,42,Critical,2023-06-20,150000,7500,2023-12-15
...
```

**Required columns:**
- `asset_id` - Unique identifier
- `asset_type` - Pump, HVAC, Conveyor, Generator, Compressor, Boiler
- `location` - Building/Zone identifier
- `health_score` - Integer 0-100
- `health_status` - Good, Warning, Critical
- `last_maintenance` - ISO date format (YYYY-MM-DD)
- `acquisition_cost` - Numeric (dollars)
- `annual_maintenance_cost` - Numeric (dollars)
- `last_inspection` - ISO date format (YYYY-MM-DD)

**Data generation:**
```python
# If you need sample data, create data generation script:
python3 generate_sample_data.py
```

---

## Cursor IDE Configuration (Optional)

**For AI-assisted development in Cursor:**

### Cursor Settings

**Go to:** `Cursor` → `Settings` → `Cursor Settings` → `Features`

| Setting | Recommended Value |
|---------|-------------------|
| Codebase Indexing | ON |
| Auto-import detection | ON |
| Symbol search | ON |
| Terminal integration | ON |

**Privacy Settings:** `Cursor Settings` → `Privacy`
- Enable Cursor to read your codebase (needed for context)
- `.env` files are automatically excluded (safe)

### Disable Python Virtual Environment Auto-Activation

**We've already configured this:**
```json
"python.terminal.activateEnvironment": false,
"python.terminal.activateEnvInCurrentTerminal": false
```

This prevents automatic activation of virtual environments when opening terminals.

---

## Verify Complete Setup

### Test Suite

Run comprehensive tests to verify everything works:

```bash
# Activate environment
source venv/bin/activate

# Run unit tests
python3 -m pytest tests/test_agent.py -v

# Expected output:
# tests/test_agent.py::TestQueryAssets::test_query_all_assets PASSED
# tests/test_agent.py::TestAnalyzeAssetHealth::test_analyze_returns_health_summary PASSED
# ...
# ======================== X passed in Y.XXs =========================
```

### Interactive Test

```bash
# Run the agent with default query
python3 agent.py

# Should see:
# 🤖 Query: Analyze asset health trends and identify which assets are at risk...
# 🔧 Agent selected 2 tool(s)...
# 📊 Final Analysis: ...
```

### Chat Interface Test

```bash
python3 chat_agent.py

# Should see interactive prompt:
# 💬 AGENTSAASY_NGAI - ENTERPRISE ASSET MANAGEMENT AI AGENT
# 🧑 You: _

# Type: "show all critical assets"
# Agent should respond with asset analysis
# Type: "quit" to exit
```

---

## Cursor AI-Assisted Development

### Using Cursor Features

#### A) Composer (Multi-file editing) - `Cmd + I`

**When to use:**
- Adding new asset management tools
- Refactoring across agent.py, tests, and docs
- Building new features that span multiple files

**Example prompt:**
```
Add a new tool called "optimize_maintenance_schedule" that analyzes 
asset health scores and recommends optimal maintenance timing.
Update agent.py, add tests, and document in HOW-TO-USE.md.
```

#### B) Chat - `Cmd + L`

**When to use:**
- Understanding asset management algorithms
- Debugging tool execution
- Explaining predictive maintenance logic

**Example prompts:**
```
@Sonnet Explain how the failure risk score is calculated in predict_failures

Debug the TCO calculation - ROI seems incorrect

How does the agent select which tools to use for a query?
```

#### C) Inline Edit - `Cmd + K`

**When to use:**
- Quick function modifications
- Adding error handling
- Refining docstrings

**Example:**
```
# Highlight predict_failures function, then Cmd + K:
Add z-score anomaly detection to risk scoring
```

---

## Keyboard Shortcuts (Mac)

**Essential for AI-assisted development:**
```
Cmd + L          → Open Chat with AI
Cmd + I          → Open Composer (multi-file)
Cmd + K          → Inline edit (on highlighted code)
Cmd + `          → Toggle terminal
Cmd + Shift + P  → Command palette
Cmd + /          → Toggle comment

# During chat:
Cmd + Enter      → Send message
Esc              → Close chat
@ + Sonnet       → Use Claude Sonnet 4
@ + GPT4         → Use GPT-4
```

---

## Production Deployment Considerations

### Security
- Store API keys in secure secrets management (AWS Secrets Manager, Azure Key Vault)
- Use IAM roles instead of hardcoded credentials
- Enable API rate limiting
- Implement request authentication

### Scalability
- Deploy agent as stateless microservice
- Use connection pooling for database access
- Implement caching for frequent queries
- Consider horizontal scaling with load balancer

### Monitoring
- Track API usage and costs
- Monitor response times
- Log tool execution patterns
- Set up alerts for errors and anomalies

### Cost Optimization
- Use GPT-4o-mini (20x cheaper than GPT-4o)
- Implement query caching
- Limit max_iterations in agent loop
- Batch similar queries when possible

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Error: Asset data file not found"
```bash
# Create data directory
mkdir -p data

# Add asset_data.csv or run data generation script
```

### "OpenAI API key not found"
```bash
# Check .env file exists and has correct format
cat .env

# Should show:
# OPENAI_API_KEY=sk-proj-...

# If missing, create it:
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Tests failing
```bash
# Run tests with verbose output
python3 -m pytest tests/test_agent.py -v --tb=short

# Check specific failing test
python3 -m pytest tests/test_agent.py::TestQueryAssets::test_query_all_assets -v
```

---

## Next Steps

1. ✅ Verify all tests pass
2. ✅ Run interactive chat to explore capabilities
3. ✅ Try sample queries from HOW-TO-USE.md
4. ✅ Review PROJECT-DICTIONARY.md for terminology
5. ✅ Customize for your asset portfolio

---

**Setup Complete!** 🎉

Start using the agent:
```bash
python3 chat_agent.py
```

---

**Last Updated:** February 10, 2026  
**Version:** 1.0.0  
**Built for:** NexGen Asset Management Platform  
**Target:** Enterprise Operations Teams
