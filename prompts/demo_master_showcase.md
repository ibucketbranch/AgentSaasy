# Demo Master Prompt: EAM AI Agent Showcase

> **ID:** `demo-master-showcase` | **Version:** 2.0.0 | **Category:** demo

## Purpose

Generate a seamless, impressive live demo that showcases AI Agent capabilities applied to enterprise asset management. The demo tells ONE continuous story through five agent types, with each agent naturally handing off to the next — creating a "day in the life" narrative.

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `{{city_name}}` | Demo city | Sacramento |
| `{{demo_date}}` | Today's date | (auto-filled) |
| `{{audience_type}}` | technical / executive / sales | technical |

## Prompt

<narrative>
We follow {{city_name}}'s Public Works department through a single day — from 6 AM to 5 PM — where five AI Agents work together to prevent failures, optimize operations, save money, and keep citizens informed.

Opening frame:
"What you're about to see isn't five separate products. It's one intelligent layer that sits on top of the existing platform — amplifying what your customers already have."
</narrative>

<acts>
| Act | Time | Agent | Core Action |
|-----|------|-------|-------------|
| 1 | 6:00 AM | IoT Anomaly Detection | Sensor spike → diagnosis → auto work order |
| 2 | 7:00 AM | GIS Route Optimization | 48 work orders → optimized routes → skill matching |
| 3 | 9:00 AM | Budget Scenario Planning | Replace vs repair → 3 scenarios → recommendation |
| 4 | 10:00 AM | Citizen Communication | Service area → impact tiers → multi-channel alerts |
| 5 | 4:00 PM | Executive Summary | Day's results → ROI dashboard → fleet-wide view |
</acts>

<transitions>
1. Bridge Sentence — Connect previous output to next trigger
2. Time Stamp — Advance the clock naturally
3. Stakeholder Shift — Change perspective (tech → director → citizen → exec)
4. Never announce agents — The story flows, agents don't introduce themselves
</transitions>

<pacing>
- Full demo: 20-25 minutes
- Condensed: Acts 1 + 2 + 5 = 12 minutes
- Extended: Full + architecture deep-dive = 45 minutes
</pacing>

<closing>
"Everything you just saw runs on data that already exists in the platform. We're not asking your customers to change anything. We're adding an intelligence layer that makes their existing investment exponentially more valuable."
</closing>

## Usage

```python
from prompt_library import PromptLibrary
lib = PromptLibrary()
prompt = lib.render("demo-master-showcase", city_name="Sacramento", demo_date="February 11, 2026")
```
