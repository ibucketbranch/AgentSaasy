# Query Template: Full Portfolio Analysis

> **ID:** `query-portfolio-analysis` | **Version:** 2.0.0 | **Category:** query

## Variables

None — runs against entire asset portfolio.

## Prompt

<instructions>
Perform a comprehensive asset portfolio analysis:
1. Query all assets and summarize by type, location, and health status
2. Analyze health trends — identify deteriorating assets and patterns
3. Predict failures for the next 90 days — which assets are at risk?
4. Calculate total cost of ownership over 5 years for the full portfolio
5. Check compliance status — any overdue inspections or certifications?
</instructions>

<output_format>
Synthesize findings into an executive summary with:
- Top 3 risks requiring immediate action
- Estimated financial impact of inaction
- Recommended prioritized action plan
</output_format>

## Usage

```python
from prompt_library import PromptLibrary
lib = PromptLibrary()
prompt = lib.render("query-portfolio-analysis")
```
