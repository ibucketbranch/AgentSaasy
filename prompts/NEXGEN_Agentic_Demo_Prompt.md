# NEXGEN AI Agent Demo Showcase — Master Prompt Template

## PURPOSE
Generate a seamless, impressive live demo that showcases AI Agent capabilities applied to enterprise asset management. The demo tells ONE continuous story through multiple agent types, with each agent naturally handing off to the next — creating a "day in the life" narrative that NEXGEN's CTO (Gaja Naik) and stakeholders can immediately connect to their platform and customer base.

---

## THE NARRATIVE: "A Day in the Life of an AI-Powered City"

### Story Arc
We follow the City of Sacramento's Public Works department through a single day — from 6 AM to 5 PM — where five AI Agents work together to prevent failures, optimize operations, save money, and keep citizens informed. Each agent is autonomous but interconnected, demonstrating how AI Agents transform reactive asset management into proactive infrastructure intelligence.

**Key Framing for Audience:**
> "What you're about to see isn't five separate products. It's one intelligent layer that sits on top of NEXGEN's existing platform — amplifying what your customers already have."

---

## DEMO FLOW: 5 ACTS, ONE STORY

### ═══ ACT 1: THE EARLY WARNING (6:00 AM) ═══
**Agent: IoT Anomaly Detection Agent**
**Transition In:** Cold open — a sensor fires before anyone's at their desk.
**Demo Beat:**

```
SCENARIO:
A vibration sensor on Pump Station #7 (Sacramento River intake) spikes 
overnight. The IoT Anomaly Agent detects it in real-time against historical 
baselines, classifies it as a bearing degradation pattern (not a one-off 
spike), predicts 72-hour failure window, and auto-creates a PRIORITY 2 
work order in the NEXGEN system — all before a single human clocks in.

SHOW:
1. Live sensor stream dashboard (Streamlit) — vibration spike visualized
2. Agent reasoning trace — "Compared to 90-day baseline... pattern matches 
   bearing wear signature with 87% confidence... escalating to work order"
3. Auto-generated work order with: asset ID, failure prediction, 
   recommended parts, estimated repair time
4. SMS/email alert sent to on-call maintenance supervisor

KEY TALKING POINT:
"This agent doesn't just alert — it diagnoses, predicts, and acts. 
Your customers go from 'something beeped' to 'here's exactly what's 
failing, when, and what to do about it.'"
```

**Transition Out →** "That work order just hit the queue. Now let's see what happens when the morning shift starts and the GIS Optimization Agent picks it up..."

---

### ═══ ACT 2: THE SMART DISPATCHER (7:00 AM) ═══
**Agent: GIS Optimization Agent**
**Tool: `optimize_field_routes`**
**Transition In:** Seamless — the work order from Act 1 is now in the routing queue alongside 47 other work orders for the day.
**Demo Beat:**

```
SCENARIO:
Morning shift begins. The GIS Optimization Agent ingests all 48 work 
orders (including the urgent pump station repair from Act 1), evaluates 
12 field technicians' skill sets and locations, and generates optimized 
routes using PostGIS spatial analysis and OR-Tools.

The CRITICAL pump station repair gets assigned to the closest qualified 
technician — rerouting them from a lower-priority inspection. Other 
routes dynamically adjust to compensate.

SHOW:
1. Folium/Leaflet map — Sacramento with all 48 work orders plotted
2. Before/After route comparison:
   - BEFORE (manual dispatch): 312 total miles, 6.2 hrs drive time
   - AFTER (AI-optimized): 218 total miles, 4.1 hrs drive time
   → 30% reduction in drive time, $847 saved TODAY
3. Technician skill matching — "Tech Martinez: pump certified, 
   2.3 miles from station, rerouted from low-priority fence inspection"
4. Priority override logic — agent reasoning for bumping the pump job

KEY TALKING POINT:
"Notice what just happened — the anomaly agent's work order flowed 
directly into route optimization. No dispatcher had to triage. The 
system understood urgency, matched skills, and optimized the entire 
day's routes in seconds. For a city with 20 field techs, this saves 
$100-150K annually in reduced windshield time alone."
```

**Transition Out →** "Routes are set, crews are rolling. But the Operations Director just walked in and wants to know: can we afford to replace that pump, or do we keep repairing it? Let's ask the Budget Agent..."

---

### ═══ ACT 3: THE STRATEGIC ADVISOR (9:00 AM) ═══
**Agent: Budget Scenario Planning Agent**
**Tool: `plan_capital_strategy`**
**Transition In:** Natural — the Operations Director sees the work order and asks a strategic question the other agents can't answer.
**Demo Beat:**

```
SCENARIO:
The Operations Director asks: "Pump Station #7 has had 4 repairs in 18 
months. Should we replace it ($180K) or keep repairing ($12K per incident)?"

The Budget Scenario Agent pulls maintenance history from NEXGEN, models 
three scenarios with different assumptions, and presents a recommendation 
with confidence intervals using Monte Carlo simulation.

SHOW:
1. Chat interface — natural language query from the director
2. Agent pulling historical data: "Analyzing 18 months of maintenance 
   records for Pump Station #7..."
3. Three scenario cards:
   
   SCENARIO A: Continue Repairs
   → Expected cost over 5 years: $340K (increasing failure frequency)
   → Risk: 23% chance of catastrophic failure (est. $500K+ emergency)
   
   SCENARIO B: Planned Replacement (Q3 2026)
   → Total cost: $180K + $24K installation
   → 5-year savings vs repairs: $136K
   → Eliminates catastrophic failure risk
   
   SCENARIO C: Refurbish + Extended Monitoring
   → Cost: $65K refurb + $8K enhanced IoT sensors
   → Extends useful life 3-5 years
   → 5-year cost: $73K + potential future replacement

4. Agent recommendation with reasoning:
   "Based on failure acceleration pattern and TCO analysis, Scenario B 
   (planned replacement) offers the best risk-adjusted return. However, 
   if Q3 capital budget is constrained, Scenario C buys time with 
   acceptable risk."

KEY TALKING POINT:
"This isn't a chatbot — it's a strategic advisor. It pulled real 
maintenance data, modeled financial scenarios, and gave an actionable 
recommendation. Your customers' CFOs and City Managers will love this 
because it speaks their language: dollars, risk, and trade-offs."
```

**Transition Out →** "Great — the director approves the replacement for Q3 budget. But here's the thing: that pump station serves 2,400 homes. When we schedule the replacement, those residents need to know. That's where the next agent takes over..."

---

### ═══ ACT 4: THE COMMUNICATOR (10:00 AM) ═══
**Agent: Citizen Communication Agent**
**Transition In:** Direct consequence of the budget decision — replacement is approved, citizens need notification.
**Demo Beat:**

```
SCENARIO:
The pump station replacement is scheduled for Q3. The Citizen 
Communication Agent identifies the service area using GIS data, 
generates personalized notifications based on impact level and 
resident preferences, and schedules a multi-channel communication 
campaign.

SHOW:
1. GIS service area identification — map highlighting 2,400 affected 
   addresses in the pump station's service territory
2. Impact classification:
   - 340 homes: Direct service interruption (8 hours)
   - 1,200 homes: Reduced pressure (2-3 days)
   - 860 homes: No impact (informational only)
3. Auto-generated notifications (3 versions based on impact tier):
   - HIGH IMPACT: "Water service interruption scheduled..."
   - MEDIUM IMPACT: "You may experience reduced water pressure..."
   - LOW IMPACT: "Infrastructure improvement in your area..."
4. Multi-channel delivery: SMS, email, 311 portal, push notification
5. Communication timeline: 30-day notice → 7-day reminder → day-of alert

KEY TALKING POINT:
"Most municipalities communicate reactively — AFTER the outage, AFTER 
the complaints flood 311. This agent flips that completely. Proactive 
communication reduces 311 call volume by 40-60% and transforms citizen 
satisfaction scores. And it's triggered automatically — no PR team 
needed."
```

**Transition Out →** "Citizens are informed, crews are optimized, the pump is scheduled for replacement. But let's zoom out — what did all of this actually look like across the whole system? The Asset Intelligence Agent ties it all together..."

---

### ═══ ACT 5: THE BIG PICTURE (4:00 PM) ═══
**Agent: Predictive Maintenance / Asset Intelligence Agent**
**Transition In:** End-of-day executive summary — pulling insights from ALL the other agents' actions.
**Demo Beat:**

```
SCENARIO:
End of day. The Asset Intelligence Agent generates an executive 
dashboard summarizing everything that happened — connecting the dots 
between the morning's sensor alert, the optimized field operations, 
the capital planning decision, and the citizen communications.

SHOW:
1. Executive Summary Dashboard:
   "Today's AI-Powered Operations Summary — February 11, 2026"
   
   ┌─ PREVENTED ──────────────────────────────┐
   │ 1 potential pump failure (est. $500K)     │
   │ Detected 72 hours before failure          │
   └───────────────────────────────────────────┘
   
   ┌─ OPTIMIZED ──────────────────────────────┐
   │ 48 work orders across 12 technicians     │
   │ 94 miles saved | $847 in fuel/labor      │
   │ Avg response time: 34 min (vs 52 min)    │
   └───────────────────────────────────────────┘
   
   ┌─ PLANNED ────────────────────────────────┐
   │ 1 capital replacement approved ($204K)   │
   │ 5-year savings: $136K vs continued repair│
   └───────────────────────────────────────────┘
   
   ┌─ COMMUNICATED ───────────────────────────┐
   │ 2,400 residents notified proactively     │
   │ 0 complaint calls (vs avg 47 for outages)│
   └───────────────────────────────────────────┘

2. Predictive maintenance horizon — fleet-wide view:
   "3 additional assets trending toward failure in the next 90 days..."
   
3. Monthly trend: "AI-assisted operations have reduced emergency work 
   orders by 34% and improved first-time fix rate to 91%"

KEY TALKING POINT:
"This is where the story comes together. Each agent handled its piece 
autonomously, but the real value is the SYSTEM — prevention, optimization, 
planning, and communication working as one intelligence layer on top 
of NEXGEN's platform. Your customers don't buy agents — they buy outcomes. 
And this is the outcome: a city that runs smarter every single day."
```

---

## DEMO EXECUTION GUIDELINES

### Setup & Environment
```
TECHNICAL REQUIREMENTS:
- Terminal/IDE visible for agent reasoning traces (shows the "brain")
- Streamlit dashboards for each agent (visual impact)
- Folium maps for GIS visualization
- Split screen recommended: left = agent terminal, right = dashboard output
- Browser tabs pre-loaded in demo order for smooth transitions

DEMO DATA:
- All agents use Sacramento, CA as the demo city
- Consistent asset IDs across agents (Pump Station #7 = PS-007)
- Realistic but impressive numbers (30% savings, not 90%)
- Date-stamped to TODAY for immediacy
```

### Transition Techniques
```
BETWEEN EACH ACT:
1. BRIDGE SENTENCE: Connect the previous agent's output to the next 
   agent's trigger ("That work order just entered the queue...")
2. TIME STAMP: Advance the clock ("It's now 7 AM, shift change...")
3. STAKEHOLDER SHIFT: Change whose perspective we're seeing 
   (technician → director → citizen → executive)
4. NEVER say "Next, let me show you another agent" — the story flows, 
   the agents don't announce themselves
```

### Pacing & Timing
```
TARGET: 20-25 minutes total
- Act 1 (IoT Anomaly):        3-4 minutes
- Transition:                  30 seconds
- Act 2 (GIS Optimization):   4-5 minutes  
- Transition:                  30 seconds
- Act 3 (Budget Scenario):    4-5 minutes
- Transition:                  30 seconds
- Act 4 (Citizen Comms):      3-4 minutes
- Transition:                  30 seconds
- Act 5 (Executive Summary):  3-4 minutes
- Q&A Buffer:                 5-10 minutes
```

### Failure Modes & Recovery
```
IF A DEMO BREAKS:
- Have screenshot/recording backup for each act
- Each act is INDEPENDENT — skip one and the story still works
- "Let me show you the output" (switch to pre-built dashboard)
- The narrative carries even if the live code stumbles

MINIMUM VIABLE DEMO (if pressed for time):
- Act 1 (IoT) + Act 2 (GIS) + Act 5 (Summary) = 12 minutes
- This shows: detection → action → results
```

---

## CLOSING STATEMENT

```
"Everything you just saw runs on data that already exists in NEXGEN's 
platform — asset records, work orders, maintenance history, GIS 
coordinates, sensor feeds. We're not asking your customers to change 
anything about how they use NEXGEN. We're adding an intelligence layer 
that makes their existing investment exponentially more valuable.

NAMI AI helps users navigate the platform. These agents help the 
platform think for itself.

The question isn't whether your customers need this — it's whether 
NEXGEN delivers it first, or a competitor does."
```

---

## CUSTOMIZATION NOTES

```
FOR DIFFERENT AUDIENCES:
- Technical (Gaja/Engineering): Emphasize architecture, reasoning traces, 
  API integration points
- Executive (CEO/Board): Emphasize ROI numbers, competitive differentiation, 
  customer retention
- Sales/Customer-facing: Emphasize the story, citizen impact, 
  "what your customers will see"

FOR DIFFERENT TIME SLOTS:
- 10 min: Acts 1 + 2 + 5 (detect → optimize → results)
- 20 min: Full 5-act demo
- 45 min: Full demo + deep dive on any 2 agents + architecture discussion
```
