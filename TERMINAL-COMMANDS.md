# Terminal Commands – Copy and run these only

**AgentSaaSy_EAM - Enterprise Asset Management AI Agent**

Use these commands when you need to run operations manually. One command per line.

---

## Setup (One-Time)

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ═══════════════════════════════════════════════════════════
## INTERACTIVE MODE - Chat with the Agent!
## ═══════════════════════════════════════════════════════════

```bash
# Interactive Chat (ask multiple questions, explore assets)
python3 chat_agent.py

# Single Question (see step-by-step tool execution)
python3 ask_agent.py "your question here"
```

### Single Question Examples:

```bash
# Predictive Maintenance
python3 ask_agent.py "Which assets are at risk of failure?"
python3 ask_agent.py "Predict failures for the next quarter"
python3 ask_agent.py "Show me high-risk equipment"

# Asset Health
python3 ask_agent.py "What is the average health score?"
python3 ask_agent.py "Show critical assets requiring attention"
python3 ask_agent.py "Analyze health trends for all pumps"

# Financial Analysis
python3 ask_agent.py "Calculate TCO for all HVAC systems over 5 years"
python3 ask_agent.py "What's the total maintenance cost projection?"
python3 ask_agent.py "Estimate ROI for equipment replacement"

# Compliance
python3 ask_agent.py "Are we compliant with inspection requirements?"
python3 ask_agent.py "Show assets with overdue inspections"
python3 ask_agent.py "Check certification status"

# Location-Based
python3 ask_agent.py "Show all equipment in Building A"
python3 ask_agent.py "What's the health of Zone North assets?"

# Complex Multi-Tool
python3 ask_agent.py "Analyze health trends, predict failures, and calculate costs"
python3 ask_agent.py "Check compliance and identify high-risk assets"
```

---

## ═══════════════════════════════════════════════════════════
## DEMOS & TESTING
## ═══════════════════════════════════════════════════════════

```bash
# Run Full 5-Tool Demo (comprehensive portfolio analysis)
python3 demo_full_agent.py

# Quick Tool Verification
python3 verify_tools.py

# Run All Unit Tests
python3 -m pytest tests/test_agent.py -v

# Run Integration Tests
python3 test_queries.py

# Test Specific Tool
python3 -m pytest tests/test_agent.py::TestPredictFailures -v
python3 -m pytest tests/test_agent.py::TestCalculateTCO -v
python3 -m pytest tests/test_agent.py::TestTrackCompliance -v
```

---

## ═══════════════════════════════════════════════════════════
## PRODUCTION OPERATIONS
## ═══════════════════════════════════════════════════════════

```bash
# Run agent with default query
python3 agent.py

# Check test coverage
python3 -m pytest tests/test_agent.py --cov=agent --cov-report=term-missing

# Verify dependencies
pip list | grep -E "langchain|pandas|openai"

# Update dependencies
pip install --upgrade langchain langchain-openai

# Check environment variables
cat .env | grep OPENAI_API_KEY
```

---

## ═══════════════════════════════════════════════════════════
## DEVELOPMENT & DEBUGGING
## ═══════════════════════════════════════════════════════════

```bash
# Run single test with verbose output
python3 -m pytest tests/test_agent.py::TestQueryAssets::test_query_all_assets -vv

# Run with debug output
python3 -m pytest tests/test_agent.py -v --tb=short

# Check code quality (if installed)
python3 -m pylint agent.py
python3 -m mypy agent.py --ignore-missing-imports

# Profile performance
python3 -m cProfile -o profile.stats agent.py
```

---

## ═══════════════════════════════════════════════════════════
## GIT OPERATIONS
## ═══════════════════════════════════════════════════════════

```bash
# Check status
git status

# Stage changes
git add agent.py tests/ *.md

# Commit
git commit -m "Update: Asset management agent implementation"

# Push to remote
git push origin main

# View commit history
git log --oneline -10
```

---

## ═══════════════════════════════════════════════════════════
## DATA OPERATIONS
## ═══════════════════════════════════════════════════════════

```bash
# Check data file exists
ls -lh data/asset_data.csv

# View first few lines
head -20 data/asset_data.csv

# Count assets
wc -l data/asset_data.csv

# Search for specific assets
grep "PUMP" data/asset_data.csv
grep "Critical" data/asset_data.csv
```

---

## ═══════════════════════════════════════════════════════════
## CLEANUP OPERATIONS
## ═══════════════════════════════════════════════════════════

```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove test artifacts
rm -rf .pytest_cache/
rm -f .coverage

# Remove macOS junk
find . -name ".DS_Store" -delete

# Deactivate virtual environment
deactivate
```

---

## ═══════════════════════════════════════════════════════════
## ENVIRONMENT VERIFICATION
## ═══════════════════════════════════════════════════════════

```bash
# Check Python version
python3 --version

# Check if venv is activated
which python3

# List installed packages
pip list

# Check API key is set
echo $OPENAI_API_KEY

# Verify all imports work
python3 -c "import langchain; import pandas; import numpy; print('✅ All dependencies OK')"
```

---

## ═══════════════════════════════════════════════════════════
## QUICK REFERENCE
## ═══════════════════════════════════════════════════════════

| Task | Command |
|------|---------|
| **Start chat** | `python3 chat_agent.py` |
| **Single query** | `python3 ask_agent.py "your question"` |
| **Run demo** | `python3 demo_full_agent.py` |
| **Run tests** | `python3 -m pytest tests/test_agent.py -v` |
| **Verify setup** | `python3 verify_tools.py` |
| **Check status** | `git status` |
| **Activate env** | `source venv/bin/activate` |

---

**Last Updated:** February 10, 2026  
**Version:** 1.0.0  
**Built for:** AgentSaaSy Asset Management Platform
