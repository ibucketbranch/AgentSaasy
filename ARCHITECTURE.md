# AgentSaaSy_EAM Architecture

> **Technical architecture and system design for enterprise asset management AI agent**

Built for asset management platform.

---

## System Overview

AgentSaaSy_EAM is a 3-layer AI agent architecture combining LLM reasoning with specialized tools for asset management, predictive maintenance, and compliance automation.

```
┌─────────────────────────────────────────────────────────┐
│               1. Reasoning Layer                         │
│          LLM: GPT-4o-mini (OpenAI)                      │
│        ReAct pattern + Chain-of-Thought                 │
│     Temperature: 0 (deterministic responses)            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  2. Tools Layer                          │
│  • query_assets - Asset retrieval & filtering           │
│  • analyze_asset_health - Health trend analysis         │
│  • predict_failures - Predictive maintenance            │
│  • calculate_tco - Financial analysis                   │
│  • track_compliance - Regulatory monitoring             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│            3. Orchestration Layer                        │
│         LangChain tool binding pattern                  │
│     Multi-turn conversation support                     │
│     Automatic tool selection based on query             │
└─────────────────────────────────────────────────────────┘
```

---

## Layer 1: Reasoning (LLM)

### Model: GPT-4o-mini
- **Context window**: 128k tokens (~96k words)
- **Cost**: $0.15/1M input tokens, $0.60/1M output tokens
- **Latency**: 1-3 seconds typical response time
- **Temperature**: 0 (deterministic, reproducible outputs)

### Why GPT-4o-mini?
1. **Cost-effective**: 20x cheaper than GPT-4o
2. **Fast**: Lower latency for production applications
3. **Capable**: Strong reasoning for structured tasks
4. **Tool calling**: Native function calling support

### Reasoning Pattern: ReAct
```
User Query
    ↓
LLM Thinks: "I need to check asset health first"
    ↓
LLM Acts: Calls analyze_asset_health()
    ↓
LLM Observes: "12 critical assets found"
    ↓
LLM Thinks: "Now I should predict failure risk"
    ↓
LLM Acts: Calls predict_failures()
    ↓
LLM Observes: "Top 5 assets at extreme risk"
    ↓
LLM Synthesizes: Final answer combining both insights
```

---

## Layer 2: Tools

### Tool Design Principles
1. **Single responsibility**: Each tool does one thing well
2. **Clear docstrings**: LLM uses these to decide when to call
3. **Structured outputs**: JSON-compatible return values
4. **Error handling**: Graceful failures with meaningful messages
5. **Type hints**: Enable static analysis and IDE support

### Tool 1: query_assets
**Purpose**: Filter and retrieve asset data

**Implementation**:
```python
@tool
def query_assets(query: str) -> str:
    """Query asset data. Use for filtering by asset type, location, 
    health status, or time period."""
    
    df = pd.read_csv('data/asset_data.csv')
    
    # Parse natural language query
    # Filter DataFrame
    # Return formatted results
```

**Data operations**:
- CSV loading with pandas
- String matching and filtering
- Aggregations (count, sum, mean)
- Date-based filtering

---

### Tool 2: analyze_asset_health
**Purpose**: Calculate health trends and identify deteriorating assets

**Implementation**:
```python
@tool
def analyze_asset_health(asset_filter: str = "all") -> str:
    """Analyze asset health trends. Calculates statistics and 
    identifies assets requiring attention."""
    
    df = pd.read_csv('data/asset_data.csv')
    
    # Calculate health score statistics
    # Group by asset type
    # Identify critical assets
    # Return analysis report
```

**Calculations**:
- Mean, median, min, max health scores
- Standard deviation and variance
- Percentage in each health category
- Trend analysis over time

---

### Tool 3: predict_failures
**Purpose**: Predictive maintenance - identify assets at failure risk

**Implementation**:
```python
@tool
def predict_failures(days_ahead: int = 90) -> str:
    """Predict which assets are at risk of failure in next 60-90 days."""
    
    df = pd.read_csv('data/asset_data.csv')
    
    # Calculate days since last maintenance
    # Compute failure risk score
    # Rank assets by risk
    # Return prioritized list
```

**Risk formula**:
```python
risk_score = (
    (100 - health_score) * 0.4 +  # Health weight
    (days_since_maintenance / 365) * 100 * 0.4 +  # Maintenance delay
    (asset_age_years / 10) * 100 * 0.2  # Age factor
)
```

**Thresholds**:
- **Critical risk (>90)**: Immediate intervention required
- **High risk (70-90)**: Schedule maintenance within 30 days
- **Moderate risk (50-70)**: Monitor closely, plan ahead
- **Low risk (<50)**: Normal operations

---

### Tool 4: calculate_tco
**Purpose**: Total Cost of Ownership financial analysis

**Implementation**:
```python
@tool
def calculate_tco(asset_filter: str, years: int = 5) -> str:
    """Calculate Total Cost of Ownership over specified time horizon."""
    
    df = pd.read_csv('data/asset_data.csv')
    
    # Project maintenance costs
    # Estimate downtime costs
    # Calculate disposal/replacement costs
    # Return financial breakdown + ROI
```

**TCO components**:
```python
tco = (
    acquisition_cost +
    (annual_maintenance * years) +
    estimated_downtime_cost +
    disposal_cost
)

roi_percentage = (
    (savings_from_predictive_maintenance / tco) * 100
)
```

**Uses scikit-learn**:
- LinearRegression for cost forecasting
- R² score for prediction accuracy

---

### Tool 5: track_compliance
**Purpose**: Monitor regulatory inspections and certifications

**Implementation**:
```python
@tool
def track_compliance(asset_filter: str = "all") -> str:
    """Track compliance status for inspections and certifications."""
    
    df = pd.read_csv('data/asset_data.csv')
    
    # Calculate days since last inspection
    # Identify overdue inspections
    # Flag critical non-compliance
    # Return compliance report
```

**Compliance rules**:
- ✅ Compliant: Inspected within 365 days
- ⚠️ Warning: 30-60 days until inspection due
- 🚨 Critical: Overdue inspection (>365 days)

**Uses scipy**:
- Z-score analysis for outlier detection
- Statistical anomaly identification

---

## Layer 3: Orchestration (LangChain)

### Tool Binding Pattern
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Initialize LLM with tool calling
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Bind tools to LLM
tools = [
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance
]

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### Execution Flow
1. **User sends query** → Converted to HumanMessage
2. **Agent reasons** → LLM generates thought process
3. **Agent acts** → Selects and calls appropriate tool(s)
4. **Tool executes** → Returns result as ToolMessage
5. **Agent observes** → Processes tool output
6. **Loop or finish** → Continues until answer is complete
7. **Final response** → Synthesized insight to user

### Multi-Tool Orchestration
Agent automatically chains tools when needed:

**Example query**: "Find critical assets and calculate their TCO"

**Agent execution**:
```
Step 1: Call query_assets("critical")
Result: 12 critical assets found

Step 2: Call calculate_tco("critical assets", 5)
Result: $2.4M projected TCO

Step 3: Synthesize answer combining both results
```

---

## Data Model

### Asset CSV Schema
**File**: `data/asset_data.csv`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `asset_id` | String | Unique identifier | PUMP-001 |
| `asset_type` | String | Equipment category | Pump, HVAC, Conveyor |
| `location` | String | Physical location | Building A-1, Zone North |
| `health_score` | Integer (0-100) | Overall condition | 85 |
| `health_status` | String | Status category | Good, Warning, Critical |
| `last_maintenance` | Date (YYYY-MM-DD) | Last service date | 2024-01-15 |
| `acquisition_cost` | Integer | Purchase price | 25000 |
| `annual_maintenance_cost` | Integer | Yearly maintenance | 1250 |
| `last_inspection` | Date (YYYY-MM-DD) | Last inspection | 2024-02-01 |
| `install_date` | Date (YYYY-MM-DD) | Installation date | 2020-03-15 |

**Sample record**:
```csv
PUMP-001,Pump,Building A-1,85,Good,2024-01-15,25000,1250,2024-02-01,2020-03-15
```

**Data quality requirements**:
- All dates in ISO format (YYYY-MM-DD)
- Health scores must be 0-100
- Health status must match score ranges
- No missing values in required fields
- Asset IDs must be unique

---

## Technology Stack

### Core Dependencies
```
langchain==0.3.18
langchain-openai==0.2.14
openai==1.59.2
pandas==2.2.3
numpy==2.2.2
scikit-learn==1.6.1
scipy==1.15.1
python-dotenv==1.0.1
pytest==8.3.4
```

### Python Version
**Minimum**: Python 3.10+  
**Recommended**: Python 3.11 or 3.12  
**Tested on**: Python 3.14 (preview)

---

## Security Considerations

### API Key Management
- Stored in `.env` file (never committed to git)
- Loaded via `python-dotenv`
- Environment-based configuration

### Data Privacy
- CSV data stored locally
- No sensitive PII in demo data
- Production: Encrypt data at rest

### Rate Limiting
- OpenAI API: 10k TPM (tokens per minute) on free tier
- Production: Use tiered pricing for higher limits

---

## Scalability

### Horizontal Scaling
Agent is **stateless** - each query is independent:
- Deploy multiple instances behind load balancer
- No session state to manage
- Scales linearly with traffic

### Vertical Scaling
For large datasets:
- Optimize pandas operations (vectorization)
- Cache frequent queries (Redis/Memcached)
- Use Parquet instead of CSV for faster I/O

### Production Deployment
```
Load Balancer
     ↓
┌────────┬────────┬────────┐
│ Agent 1│ Agent 2│ Agent 3│  → Multiple stateless instances
└────────┴────────┴────────┘
     ↓
┌─────────────────────────┐
│  Shared Data Storage    │  → S3, PostgreSQL, or Data Lake
└─────────────────────────┘
```

---

## Monitoring & Observability

### Metrics to Track
1. **Latency**: Response time per query
2. **Tool usage**: Which tools called most frequently
3. **Error rate**: Failed tool executions
4. **Cost**: API usage in tokens and dollars
5. **User queries**: Most common request patterns

### Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log every tool execution
logger.info(f"Tool called: {tool_name}, Args: {args}")
logger.info(f"Tool result: {result}")
```

### LangSmith Integration (Optional)
LangChain's observability platform:
- Trace agent execution step-by-step
- Debug reasoning and tool selection
- Monitor production performance
- Track costs per query

---

## Testing Strategy

### Unit Tests
**File**: `tests/test_agent.py`

Tests for each tool:
- Valid inputs
- Edge cases
- Error handling
- Output format validation

### Integration Tests
**File**: `test_queries.py`

End-to-end agent execution:
- Single-tool queries
- Multi-tool orchestration
- Complex analysis scenarios

### Performance Tests
Benchmark tool execution time:
- query_assets: <100ms
- analyze_asset_health: <200ms
- predict_failures: <300ms
- calculate_tco: <250ms
- track_compliance: <150ms

---

## Future Enhancements

### Phase 2 (AgentSaaSy Production)
1. **Real-time data**: Connect to live asset sensors
2. **Database integration**: PostgreSQL for asset records
3. **Authentication**: User-based access control
4. **Web UI**: React dashboard for queries
5. **Email alerts**: Automated notifications for critical assets

### Phase 3 (Advanced AI)
1. **Fine-tuned model**: Custom LLM for asset management
2. **Embeddings**: Semantic search over asset documentation
3. **Image analysis**: CV for equipment condition assessment
4. **Multi-agent**: Specialized agents for different asset types

---

## Additional Resources

- **LangChain Docs**: https://python.langchain.com/docs/
- **OpenAI Platform**: https://platform.openai.com/
- **pandas Documentation**: https://pandas.pydata.org/docs/
- **ReAct Paper**: https://arxiv.org/abs/2210.03629

---

**For demo results, see:** `DEMO-RESULTS.md`  
**For terminology, see:** `PROJECT-DICTIONARY.md`  
**For performance metrics, see:** `PERFORMANCE.md`
