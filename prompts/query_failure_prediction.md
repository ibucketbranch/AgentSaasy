# Query Template: Failure Prediction

> **ID:** `query-failure-prediction` | **Version:** 2.0.0 | **Category:** query

## Variables

| Variable | Default |
|----------|---------|
| `{{time_horizon}}` | next quarter |

## Prompt

<instructions>
Which assets are at risk of failure in the {{time_horizon}}? For each at-risk asset:
1. Current health score and failure risk score
2. Primary risk factors (age, maintenance gap, health trend)
3. Estimated time-to-failure window
4. Recommended preventive action and estimated cost
5. Cost of inaction (emergency repair + downtime)

Rank by urgency.
</instructions>

<output_format>
Include total portfolio risk exposure in dollars at the end. Present each asset with its ID, risk score, and recommended action in a prioritized list.
</output_format>

## Usage

```python
from prompt_library import PromptLibrary
lib = PromptLibrary()
prompt = lib.render("query-failure-prediction", time_horizon="next 60 days")
```
