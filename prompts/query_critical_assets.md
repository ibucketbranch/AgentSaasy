# Query Template: Critical Asset Identification

> **ID:** `query-critical-assets` | **Version:** 2.0.0 | **Category:** query

## Variables

| Variable | Default |
|----------|---------|
| `{{location}}` | (all locations) |
| `{{asset_type}}` | (all types) |

## Prompt

<instructions>
Identify all critical assets{{" in " + location if location else ""}}{{" of type " + asset_type if asset_type else ""}} that require immediate attention. For each critical asset, provide:
1. Current health score and trend direction
2. Days since last maintenance
3. Estimated failure risk score
4. Recommended immediate action

Prioritize by risk score (highest first).
</instructions>

<output_format>
Return findings as a prioritized list with specific asset IDs, metrics, and recommended actions. Include total portfolio risk exposure in dollars at the end.
</output_format>

## Usage

```python
from prompt_library import PromptLibrary
lib = PromptLibrary()
prompt = lib.render("query-critical-assets", location="Building A", asset_type="Pump")
```
