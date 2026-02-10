# Terminal Commands – Copy and run these only

Use these when you need to run commands manually. One command per line.

```bash
# Setup (one-time)
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements-working.txt

# ═══════════════════════════════════════════════════════════
# INTERACTIVE MODE - Chat with the Agent!
# ═══════════════════════════════════════════════════════════

# Interactive Chat (ask multiple questions)
python3 chat_agent.py

# Single Question (see step-by-step)
python3 ask_agent.py "your question here"

# Single Question Examples:
python3 ask_agent.py "Forecast the next 8 weeks"
python3 ask_agent.py "Show me Widget A sales"
python3 ask_agent.py "Give me an executive summary"
python3 ask_agent.py "Analyze trends and detect anomalies"

# ═══════════════════════════════════════════════════════════
# DEMOS & TESTING
# ═══════════════════════════════════════════════════════════

# Run Full 5-Tool Demo
python3 demo_full_agent.py

# Test New Tools
python3 test_new_tools.py

# Quick Verification
python3 verify_tools.py

# Run Tests
python3 -m pytest tests/test_agent.py -v

# Run Integration Tests
python3 test_queries.py

# Development - Single Test
python3 -m pytest tests/test_agent.py::TestQueryData::test_query_all_data -v
```
