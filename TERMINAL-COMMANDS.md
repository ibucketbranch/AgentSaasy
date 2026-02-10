# Terminal Commands – Copy and run these only

Use these when you need to run commands manually. One command per line.

```bash
# Setup (one-time)
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements-working.txt

# Run Agent
python3 agent.py

# Run Full 5-Tool Demo
python3 demo_full_agent.py

# Test New Tools
python3 test_new_tools.py

# Run Tests
python3 -m pytest tests/test_agent.py -v

# Run Integration Tests
python3 test_queries.py

# Development
python3 -m pytest tests/test_agent.py::TestQueryData::test_query_all_data -v
```
