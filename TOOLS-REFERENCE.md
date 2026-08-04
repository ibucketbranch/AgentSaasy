# AgentSaaSy_EAM - Tools Reference

## Overview

AgentSaaSy_EAM provides 6 specialized tools for enterprise asset management and field service optimization. Each tool is designed to address specific operational challenges faced by asset-intensive organizations.

## The 6 Tools

### 1. Query Assets
**Purpose:** Filter and search asset data by type, location, health status, or time period

**Use Cases:**
- Find all critical assets in a specific building
- List pumps with warning status
- Identify assets serviced in the last quarter
- Get asset counts by location or type

**Example Queries:**
```
"Show me all critical assets in Building A"
"List all pumps with warnings"
"Find assets serviced last quarter"
```

**Returns:**
- Asset count
- Total acquisition value
- Average health score
- Critical asset count

---

### 2. Analyze Asset Health
**Purpose:** Analyze health trends and identify deteriorating assets

**Use Cases:**
- Detect assets with declining health scores
- Identify overdue maintenance
- Calculate health statistics across portfolio
- Flag assets approaching failure thresholds

**Example Queries:**
```
"Analyze asset health trends"
"Which assets have declining health?"
"Show me overdue maintenance"
```

**Returns:**
- Average health score
- Critical/Warning/Healthy asset counts
- Overdue maintenance count
- Health score distribution

---

### 3. Predict Failures
**Purpose:** Identify at-risk assets 60-90 days ahead using statistical analysis

**Use Cases:**
- Proactive maintenance planning
- Budget forecasting for repairs
- Risk mitigation strategies
- Preventive maintenance scheduling

**Example Queries:**
```
"Which assets are at risk of failure in the next quarter?"
"Predict failures for critical equipment"
"Show me high-risk assets"
```

**Returns:**
- Risk scores for each asset
- Top 5 at-risk assets with details
- Statistical outlier detection
- Maintenance recommendations

**Algorithm:**
- Health score analysis (50% weight)
- Time since last maintenance (30% weight)
- Asset age (20% weight)
- Z-score outlier detection

---

### 4. Calculate TCO (Total Cost of Ownership)
**Purpose:** Financial analysis of asset lifecycle costs

**Use Cases:**
- Budget planning
- Asset replacement decisions
- ROI analysis
- Cost-benefit comparisons

**Example Queries:**
```
"Calculate TCO for all pumps over 5 years"
"What's the total cost of ownership for PUMP-001?"
"Show me 10-year TCO for critical assets"
```

**Returns:**
- Acquisition costs
- Maintenance costs (actual + projected)
- Downtime costs
- Disposal costs
- Total TCO
- ROI percentage
- Cost per asset

**Time Horizons:** 1-10 years (default: 5 years)

---

### 5. Track Compliance
**Purpose:** Monitor regulatory compliance for inspections and certifications

**Use Cases:**
- Regulatory audit preparation
- Inspection scheduling
- Compliance reporting
- Risk management

**Example Queries:**
```
"Check compliance status for all assets"
"Which inspections are overdue?"
"Show me upcoming compliance deadlines"
```

**Returns:**
- Compliant asset count
- Upcoming inspections (60-day window)
- Overdue inspections
- Critical non-compliance alerts
- Overall compliance rate

**Thresholds:**
- Annual inspection requirement: 365 days
- Critical assets: 180 days (semi-annual)

---

### 6. Optimize Field Routes (NEW)
**Purpose:** Spatial intelligence scenario model for field service optimization (simulated, see Phase 2 note)

**Use Cases:**
- Daily route planning
- Emergency response optimization
- Cost reduction initiatives
- Capacity planning
- Territory management

**Example Queries:**
```
"Optimize routes for 30 work orders across 8 technicians"
"Plan field service routes for north territory"
"Balance workload across 12 technicians"
```

**Parameters:**
- `work_order_count`: Number of jobs to optimize (default: 20)
- `technician_count`: Available field crew (default: 5)
- `service_territory`: Geographic filter ('all', 'north', 'south', 'east', 'west')
- `optimization_goal`: Objective ('minimize_drive_time', 'balance_workload', 'prioritize_urgent')

**Returns:**
- Baseline vs optimized drive time comparison
- Cost savings (labor + fuel)
- Daily and annual savings projections
- Capacity improvement analysis
- Technician assignments
- Priority work order handling
- Business impact metrics
- ROI analysis

**Modeled Benefits** (scenario output, not measured field data)**:**
- 20-40% drive time reduction
- $100K-150K annual savings (typical 20-person crew)
- 15-25% capacity increase
- Improved customer response times
- Reduced fuel consumption

**Technology:**
- Geographic clustering (DBSCAN)
- Route optimization (OR-Tools VRP solver)
- Real-world routing (OSRM)
- Constraint satisfaction (skills, time windows, priorities)

---

## Tool Selection Guide

### When to Use Each Tool

| Scenario | Recommended Tool |
|----------|------------------|
| Find specific assets | `query_assets` |
| Understand asset condition | `analyze_asset_health` |
| Plan preventive maintenance | `predict_failures` |
| Budget planning | `calculate_tco` |
| Regulatory audit prep | `track_compliance` |
| Daily route planning | `optimize_field_routes` |
| Emergency response | `optimize_field_routes` (prioritize_urgent) |
| Cost reduction initiative | `calculate_tco` + `optimize_field_routes` |

### Multi-Tool Workflows

**Workflow 1: Comprehensive Asset Analysis**
```
1. query_assets → Find critical assets
2. analyze_asset_health → Assess health trends
3. predict_failures → Identify at-risk assets
4. calculate_tco → Estimate repair/replacement costs
```

**Workflow 2: Compliance & Maintenance Planning**
```
1. track_compliance → Identify overdue inspections
2. query_assets → Filter by location/type
3. optimize_field_routes → Plan inspection routes
```

**Workflow 3: Cost Optimization**
```
1. calculate_tco → Analyze current costs
2. predict_failures → Identify upcoming expenses
3. optimize_field_routes → Reduce operational costs
```

**Workflow 4: Emergency Response**
```
1. query_assets → Find critical/urgent assets
2. optimize_field_routes → Prioritize urgent jobs
3. track_compliance → Ensure regulatory requirements met
```

## Usage Examples

### Python API

```python
from agent import (
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance,
    optimize_field_routes
)

# Direct tool invocation
result = query_assets.invoke({"query": "critical assets in Building A"})
print(result)

# Route optimization
route_result = optimize_field_routes.invoke({
    "work_order_count": 30,
    "technician_count": 8,
    "service_territory": "north",
    "optimization_goal": "minimize_drive_time"
})
print(route_result)
```

### Natural Language (via Agent)

```python
from agent import get_agent
from langchain_core.messages import HumanMessage

agent = get_agent()

# Single query
response = agent.invoke([HumanMessage(
    content="Find critical pumps and predict which will fail next quarter"
)])

# The agent automatically selects and chains appropriate tools
```

### Command Line

```bash
# Activate environment
source venv/bin/activate

# Run interactive agent
python chat_agent.py

# Run specific demo
python demo_gis_optimization.py

# Test single tool
python -c "from agent import optimize_field_routes; \
    print(optimize_field_routes.invoke({'work_order_count': 20}))"
```

## Performance Characteristics

| Tool | Typical Response Time | Data Dependencies |
|------|----------------------|-------------------|
| query_assets | < 100ms | asset_data.csv |
| analyze_asset_health | < 200ms | asset_data.csv |
| predict_failures | < 300ms | asset_data.csv |
| calculate_tco | < 100ms | asset_data.csv |
| track_compliance | < 200ms | asset_data.csv |
| optimize_field_routes | < 2s | asset_data.csv + GIS data |

## Business Impact Summary

> Every figure in this section is an unvalidated scenario model. The values come
> from industry-standard cost multipliers applied to a baseline, not from
> measured deployments. No customer has run this system. The white paper
> retires ROI multiples for this reason and keeps projections only as labeled
> scenario modeling; treat the numbers below the same way.

### Predictive Maintenance (Tools 1-4)
- **Value:** $1.1M - $5.4M annually (typical enterprise)
- **ROI:** 16,000% - 70,000%
- **Payback:** Immediate (uses existing data)

### Field Service Optimization (Tool 6)
- **Value:** $100K - $150K annually (20-person crew)
- **ROI:** 50x - 100x
- **Payback:** 1-2 weeks
- **Scalability:** Linear with crew size

### Combined Impact
- **Total Annual Value:** $1.2M - $5.5M (typical organization)
- **Operational Improvements:** 
  - 20-40% drive time reduction
  - 15-25% capacity increase
  - 60-90 day failure prediction
  - 95%+ compliance rate

## Integration Points

### Current (Demo Mode)
- Uses sample asset data (50 assets)
- Simulates GIS optimization
- Demonstrates full functionality

### Production Integration
- **the EAM platform API:** Work orders, asset locations, technician data
- **PostGIS Database:** Spatial queries and analysis
- **OSRM/Google Maps:** Real-world routing
- **the platform mobile app:** Route sheet delivery
- **Document Management:** PDF route sheets

## Future Enhancements

### Planned Features
1. **Real-time re-optimization** (dynamic route updates)
2. **Traffic-aware routing** (live traffic data)
3. **Machine learning** (predictive job duration)
4. **Advanced constraints** (customer time windows, multi-day scheduling)
5. **Extended use cases** (fleet routing, emergency response, meter reading)

### Additional Tools (Roadmap)
- **Energy Optimization:** Analyze energy consumption patterns
- **Inventory Management:** Parts availability and procurement
- **Workforce Planning:** Skill gap analysis and training recommendations
- **Sustainability Metrics:** Carbon footprint and environmental impact

## Support

### Documentation
- **Main README:** README.md
- **Architecture Guide:** ARCHITECTURE.md
- **GIS Optimization Guide:** GIS-OPTIMIZATION-GUIDE.md
- **Demo Results:** DEMO-RESULTS.md
- **Quick Start:** QUICK-START.md

### Demo Scripts
- `demo_full_agent.py` - All 6 tools demonstration
- `demo_gis_optimization.py` - GIS-specific demos
- `chat_agent.py` - Interactive chat interface
- `test_queries.py` - Tool testing

### Getting Help
- Review documentation in docs/ folder
- Run demos to see tools in action
- Check test files for usage examples
- Contact: [Your support email]

---

**Last Updated:** February 2024  
**Version:** 1.1.0 (6 tools)  
**License:** MIT
