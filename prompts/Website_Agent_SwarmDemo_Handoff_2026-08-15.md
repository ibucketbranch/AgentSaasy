# HANDOFF - Website agent: publish the AgentSaaSy Swarm Demo project page to bucketbranch.ai

**Written 2026-08-15. Paste into the session that maintains ~/Projects/Bucketbranch-ai.**

You are integrating a finished, self-contained project page into bucketbranch.ai. The page is done and verified. Your job is integration, not redesign. Do not rewrite the copy, rename the concepts, or restyle the animation.

---

## 1. THE DELIVERABLE

One file, stored in the AgentSaaSy repo: `~/Projects/AgentSaaSy/prompts/assets/agentsaasy-swarm-demo.html`

- Fully self-contained: all CSS and JS inline, zero external dependencies, no build step, no CDN calls.
- Canvas-based animation, vanilla JS, ~30KB. Verified in headless Chromium: zero console errors, animation and all interactions work.
- Responsive: side panels collapse to single column below 900px.

## 2. BACKGROUND AND CONTEXT (read before touching anything)

This page illustrates the three projects that make up the AEQ body of work, operating together on one simple workflow:

1. **AEQ (Agent Efficiency Quotient)** = Business Value Delivered / Tokens Consumed. An ARCHITECTURE QUALITY metric (signal-to-noise ratio of an agent design), NOT a cost-savings tool. Never frame it as cost savings. On the page it is the cross-cutting measurement plane and the live gate monitor.
2. **The harness**: the orchestration and test layer. Routes requests, fans out parallel work to agents, enforces pre-registered gate thresholds (GREEN/YELLOW/RED declared before any data exists), and coordinates cross-family judging (the judge model never shares a family with the workers it reviews). On the page it is the L3 layer and the central "HARNESS" node in the animation.
3. **AgentSaaSy**: the flagship R&D platform for enterprise AI Agent stacks and SaaS substitution economics. On the page it is the L4 application layer and the project title.

- Site owner: Michael Valderrama, independent AI agent architect (GitHub: `ibucketbranch`, Medium: @michael_valderrama).
- **Core thesis** (appears in the hero, keep it intact): a model's specs do not predict whether it is adequate for a workload; only measuring the model-workload pair does.
- The page shows ONE simple workflow on purpose. Complexity gets added later (multi-workflow swarms, then full AEQ Grid 3x3x3 certification). The roadmap section reflects this.

## 3. HARD RULES (non-negotiable)

1. **Terminology:** NEVER use the phrase "Agentic AI" anywhere: page, card, meta tags, alt text, URLs. Use "AI Agents" or "Agentic Agents" only.
2. **Simulated data:** every number in the demo is simulated. The page carries a "SIMULATED DATA - DEMO" badge on the canvas and a footer disclaimer ("All meters on this page run on simulated demo data. Published claims use real API results only."). Do not remove, hide, or soften either one.
3. **Character hygiene:** no em dashes, en dashes, or curly quotes in any copy you write (card blurb, meta description, etc.). Plain ASCII: hyphens and straight quotes.
4. **Do not mention** LEOpard or any chip/hardware concept anywhere on this page or card. It is deliberately excluded.
5. **AEQ vs AEQ Grid:** AEQ is the metric; AEQ Grid is the certification program. Do not conflate them. The page uses them correctly; keep it that way.

## 4. INTEGRATION PLAN

### A. Project index card
On the projects/work listing page, add a card for this project:

- **Title:** AgentSaaSy: The Swarm, Measured
- **Blurb (use as-is):** "A live look at an enterprise AI Agent stack: harness orchestration, cross-family judging, and AEQ scoring on every run."
- **Tags:** AI Agents, AEQ, Orchestration, R&D
- **Thumbnail:** preferred option is a mini looping version of the swarm animation (the canvas code is data-driven and lightweight; a cropped, non-interactive instance works). Fallback: a static dark screenshot of the swarm canvas.
- Card links to the full page.

### B. Full project page
- Route: `/projects/agentsaasy` (or the site's equivalent pattern). Rename the file as needed; nothing inside depends on the filename.
- Page structure (already built, in this order):
  1. **Hero** (semi-marketing): "Watch the swarm work. Then measure it." + AEQ formula rendered as a fraction + two CTAs that smooth-scroll to sections.
  2. **01 The Swarm, Live:** animated canvas. Workflow: intake -> harness -> planner -> parallel fan-out (retriever, worker A, worker B) -> cross-family judge -> AEQ gate -> output. Side panel: live AEQ meter with GREEN/YELLOW/RED gate chips, run counters, scrolling harness log. User controls: pause, inject request, speed slider.
  3. **02 Architecture Layers** (technical): L4 AgentSaaSy Application Layer, L3 Harness and Orchestration Layer, L2 Agent Layer, L1 Model Layer, plus a vertical amber "AEQ Measurement Plane" cutting across all four with an animated scanline. Hover/tap a layer to populate the detail panel.
  4. **03 The Stack:** Python, Anthropic API, OpenAI API, tiktoken, pre-registration docs, AEQ Grid, GitHub (ibucketbranch), canvas + vanilla JS.
  5. **04 Roadmap:** NOW (one metered workflow) -> NEXT (multi-workflow swarms, tiered model routing) -> LATER (AEQ Grid 3x3x3 certification).
  6. **Footer** with the simulated-data disclaimer.

### C. Navigation handling
- The file ships with its own top nav (logo + four in-page anchor links: Live Swarm, Architecture, Stack, Roadmap).
- If the site has a global nav, REMOVE the demo page's `<nav>` block and keep the four anchor links as a slim sub-nav under the global header. Anchor IDs are: `#demo`, `#architecture`, `#stack`, `#roadmap`.
- If the site has no global nav on project pages, leave the built-in nav as-is.

### D. Meta / SEO
- Title tag: `AgentSaaSy | The Swarm, Measured | bucketbranch.ai`
- Meta description (use as-is): "A live, animated demo of an enterprise AI Agent stack: a harness orchestrating a swarm of AI Agents through a metered workflow, scored by AEQ (Business Value Delivered per token)."
- OG image: screenshot of the swarm canvas on the dark background.

## 5. TECHNICAL NOTES FOR FUTURE EDITS (do not act on these now)

- The animation is data-driven. Agents live in a `NODES` object (unit coordinates), connections in `EDGES`, and the workflow in `STAGES`. Adding an agent or a second concurrent workflow is a config edit, not a renderer rewrite.
- Gate thresholds in the sim: GREEN >= 0.90, YELLOW >= 0.50 (BVD units per 1K tokens). These mirror the pre-registration pattern; they are demo values.
- Color system via CSS variables at the top of the file: teal = harness, blue = agents, amber = AEQ, purple = judge, green = output.

## 6. ACCEPTANCE CHECKLIST (verify before calling it done)

- [ ] Card renders on the project index and links to the page
- [ ] Page loads with zero console errors
- [ ] Animation runs; pause / inject / speed controls work
- [ ] Gate chips light up and the harness log scrolls as requests complete
- [ ] Architecture layer hover/tap updates the detail panel
- [ ] No double nav bars
- [ ] "SIMULATED DATA - DEMO" badge and footer disclaimer present
- [ ] Zero occurrences of "Agentic AI" in rendered output and meta tags
- [ ] Mobile: single-column layout below 900px, canvas still animates
