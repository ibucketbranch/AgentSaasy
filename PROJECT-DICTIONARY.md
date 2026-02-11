# AgentSaasy_NGAI Project Dictionary

> **Quick reference guide for enterprise asset management and AI terminology**

Built for NexGen Asset Management platform demonstrations.

---

## Enterprise Asset Management (EAM) Terms

### Asset
Physical equipment or infrastructure owned and operated by an organization. In this project: 
Pumps, HVAC systems, Conveyors, Generators, Compressors, and Boilers.

### Asset Health Score
Numerical metric (0-100) indicating overall condition and operational reliability of an asset.
- 0-49: Critical (immediate attention required)
- 50-74: Warning (schedule maintenance)
- 75-100: Healthy (normal operation)

### Predictive Maintenance (PdM)
Maintenance strategy using data analysis and AI to predict equipment failures before they occur,
enabling proactive intervention 60-90 days ahead of failure.

**Benefits:**
- Reduce unplanned downtime by 30-50%
- Lower maintenance costs by 20-40%
- Extend asset lifespan by 20-30%

### Total Cost of Ownership (TCO)
Comprehensive financial analysis including acquisition, operation, maintenance, downtime, and
disposal costs over an asset's entire lifecycle (typically 5-10 years).

**Components:**
- Acquisition cost (initial purchase)
- Annual maintenance cost (labor + parts)
- Downtime cost (lost productivity)
- Energy/operational costs
- Disposal/replacement cost

### MTBF (Mean Time Between Failures)
Average time an asset operates between breakdowns. Higher MTBF = more reliable equipment.

**Example:** MTBF of 2,000 hours means asset runs ~2,000 hours between failures on average.

### MTTR (Mean Time To Repair)
Average time required to repair an asset and return it to operational status.
Lower MTTR = faster recovery from failures.

### Compliance
Adherence to regulatory requirements for inspections, certifications, and safety audits.
Critical for avoiding penalties and ensuring operational safety.

**Regulatory areas:**
- Safety inspections (OSHA)
- Environmental compliance (EPA)
- Industry-specific certifications
- Insurance requirements

### Failure Risk Score
Calculated metric (0-100) predicting likelihood of asset failure based on:
- Current health score
- Time since last maintenance
- Asset age
- Historical failure patterns

Scores above 70 trigger predictive maintenance alerts.

### Asset Lifecycle Management
Managing assets from acquisition through operation, maintenance, and eventual disposal.

**Phases:**
1. Planning & Acquisition
2. Installation & Commissioning
3. Operation & Maintenance
4. Monitoring & Optimization
5. Decommissioning & Replacement

### GIS Route Optimization
Spatial intelligence for field service operations. Uses geographic information systems (GIS) 
to optimize technician routes, reducing drive time, fuel costs, and improving response times.

**Benefits:**
- 20-40% reduction in drive time
- $100K-150K annual savings for 20-person crews
- Improved first-time fix rates
- Better work-life balance for field technicians

### Monte Carlo Simulation
Statistical technique that runs thousands of scenarios with randomized variables to quantify 
uncertainty in complex decisions. Used in capital planning to model different replacement 
strategies and provide confidence intervals (P10/P50/P90).

**In this project:**
- Simulates 1,000+ iterations per capital strategy
- Models cost inflation, maintenance variation, failure probabilities
- Provides defensible recommendations for city councils and boards

### Capital Planning
Strategic multi-year budgeting for asset replacement and major maintenance. Balances cost, 
risk, and service levels across planning horizons (typically 5-10 years).

**Strategies:**
- Aggressive Preventive: Replace at 80% of useful life
- Balanced Risk-Based: Replace based on risk score + condition
- Conservative Run-to-Failure: Replace only at 100% life or after failure
- Budget-Constrained Priority: Maximize value within budget limits

---

## AI Agent & LLM Terms

### AI Agent / Agentic Agent
Autonomous AI systems that perceive, reason, plan, use tools, and act to achieve goals.
Unlike generative AI (which only outputs text), agents take actions and adapt.

**In this project:** The asset management agent autonomously selects tools, analyzes data,
and synthesizes insights based on natural language queries.

### ReAct (Reason + Act)
Agent pattern alternating between reasoning (thinking step-by-step) and acting (calling tools),
then observing results and repeating until task completion.

**Pattern:**
```
Thought → Action (Tool Call) → Observation → Thought → Action → ... → Final Answer
```

### Chain-of-Thought (CoT)
Prompting technique instructing the LLM to "think step by step" before answering.
Improves planning, decision quality, and complex reasoning.

### Tool Calling / Function Calling
Mechanism where LLM invokes external functions (tools) instead of just generating text.
Model outputs structured call (JSON), framework executes it, and result is returned.

**In this project - 7 tools:**
- `query_assets` - Filter and retrieve asset data
- `analyze_asset_health` - Calculate health trends
- `predict_failures` - Identify at-risk assets
- `calculate_tco` - Financial analysis
- `track_compliance` - Regulatory status
- `optimize_field_routes` - GIS-powered field service routing
- `plan_capital_strategy` - Monte Carlo capital planning simulation

**Cost consideration:** Each tool call = 1 LLM API request. Complex queries using multiple
tools cost more but provide richer analysis.

### Orchestration
Control layer managing workflow: deciding when to reason, call tools, loop, handle errors,
or stop. In this project, LangChain's tool binding provides orchestration.

### Token
Unit of text an LLM processes (roughly ¾ of a word in English).
Critical for understanding API costs and context limits.

**Examples:**
- "predictive maintenance" ≈ 3 tokens
- "asset health score" ≈ 4 tokens
- 1,000 words ≈ 1,333 tokens

**Why it matters:** OpenAI pricing is per token, not per word.

### Context Window
Maximum amount of text (in tokens) an LLM can process at once, including prompt,
conversation history, tool outputs, and response.

**Model limits:**
- GPT-4o-mini: 128k tokens (~96k words)
- GPT-4o: 128k tokens

---

## LangChain Framework Terms

### LangChain
Open-source Python framework for building LLM applications. Provides building blocks
for prompts, tools, agents, memory, and integrations.

**This project uses:** Tool binding pattern with GPT-4o-mini for efficient asset analysis.

**Website:** https://langchain.com

### Tool
Function wrapped with metadata (name, description, args schema) enabling LLM to understand
when and how to call it. Defined with `@tool` decorator.

**Example:**
```python
@tool
def query_assets(query: str) -> str:
    """Query asset data by type, location, or health status."""
    # Implementation
```

### ChatOpenAI
LangChain wrapper for OpenAI's chat models. Handles API authentication, rate limiting,
retries, and tool binding.

### Message Types
Structured classes representing conversation components:
- **HumanMessage**: User input
- **AIMessage**: LLM response (with optional tool calls)
- **ToolMessage**: Tool execution results

---

## Python Libraries & Dependencies

### pandas
Powerful data manipulation library providing DataFrame objects for structured data
operations (filtering, grouping, aggregating, transforming).

**In this project:**
- Load and query `asset_data.csv`
- Filter assets by type, location, health status
- Calculate aggregations and statistics
- Time-series analysis for maintenance patterns

### numpy
Fundamental numerical computing library providing array operations and mathematical
functions. Foundation for pandas, scipy, and scikit-learn.

**In this project:**
- Array operations for predictions
- Statistical computations
- Risk score calculations

### scikit-learn
Most popular machine learning library for Python. Provides tools for classification,
regression, clustering, and preprocessing.

**In this project:**
- `LinearRegression` for TCO forecasting
- Predictive modeling for failure analysis
- R² score calculation for model quality

### scipy
Scientific Python library providing algorithms for optimization, linear algebra,
statistics, and more.

**In this project:**
- `stats.zscore()` for anomaly detection
- Statistical analysis for compliance tracking
- Outlier identification in asset health data

### python-dotenv
Loads environment variables from `.env` file for secure configuration management.

**In this project:**
- Loads `OPENAI_API_KEY` securely
- Prevents hardcoding secrets in code
- Essential for security best practices

### pytest
Python's most popular testing framework for unit and integration testing.

**In this project:**
- Comprehensive test suite in `tests/test_agent.py`
- Tests all 5 asset management tools
- Ensures production reliability

---

## Quick Tool Reference

| Tool | Purpose | Example Query |
|------|---------|---------------|
| `query_assets` | Filter assets by type, location, health status | "Show critical assets in Building A" |
| `analyze_asset_health` | Calculate health trends, identify deteriorating assets | "Analyze health trends for all pumps" |
| `predict_failures` | Identify assets at risk 60-90 days ahead | "Which assets will fail next quarter?" |
| `calculate_tco` | Total cost of ownership over time horizon | "Calculate TCO for HVAC over 5 years" |
| `track_compliance` | Monitor inspections, certifications, regulatory status | "Check compliance for pressure vessels" |
| `optimize_field_routes` | GIS optimization for field technician routing | "Optimize routes for 30 work orders across 8 technicians" |
| `plan_capital_strategy` | Multi-year capital planning with Monte Carlo simulation | "Create a 10-year capital plan with $5M annual budget" |

---

## Additional Resources

- **LangChain Documentation**: https://python.langchain.com/docs/
- **OpenAI API Reference**: https://platform.openai.com/docs/
- **ReAct Paper**: https://arxiv.org/abs/2210.03629
- **ISO 55000 (Asset Management)**: International standard for asset management
- **NexGen Asset Management**: Target platform for this demonstration

---

**For detailed examples, see:** `DEMO-RESULTS.md`  
**For architecture details, see:** `ARCHITECTURE.md`  
**For performance metrics, see:** `PERFORMANCE.md`
