# HANDOFF PROMPT — bucketbranch.ai: add Case Studies section + Papers restructure

Paste everything below this line into the session that has the bucketbranch.ai site repo.

---

You are working on the bucketbranch.ai website. Before changing anything, inspect the repo to learn the stack and conventions (static site generator, templating, how /papers/ pages are built, nav structure). Match the existing dark-navy theme (#0a1628) and the existing paper-page template style. Do not invent a new design language.

## Terminology and voice rules (hard requirements)

- NEVER write "Agentic AI" or "agentic artificial intelligence." Use "AI agents," "AI agent architecture," or "agentic architecture." Run a case-insensitive grep for both banned forms on every file you touch before finishing.
- Plain ASCII in all copy: straight quotes, regular hyphens, no em dashes, no curly quotes, no emoji.
- Attribution where the template shows an author: "Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026"
- Do not soften numbers or add marketing superlatives. The copy below is final; typographic fitting only.

## Publication constraint

Do NOT publish any content from the v3 white paper ("The Cost of a Question") or any mention of the routing study before 2026-08-10. Task 2 builds the slug and template for it but leaves it unpublished/hidden until told.

## Task 1 — New section: /case-studies/

Create a Case Studies index page and the first entry at /case-studies/agentsaasy-eam/. Add "Case Studies" to the site nav after "Papers."

Page copy (use verbatim; headings may adapt to the template):

---

# Case Study: A Platform's Worth of EAM Workflows in Seven Tools

**Client:** Internal R&D build (AgentSaaSy_EAM)
**Domain:** Enterprise asset management for utility-grade operations
**Stack:** Python, LangChain, one certified language model, seven domain tools

## The problem

Commercial EAM/CMMS platforms sell asset registry, condition monitoring, predictive maintenance, TCO reporting, compliance tracking, field dispatch, and capital planning as per-seat licenses. A 20-technician team on a mid-market Premium tier pays about $13,200 a year for that module list. The question this build set out to answer: how much engineering does that module list actually require, and what does it cost to run once built?

## The build

Seven Python tools behind one language model: asset query, health analysis, failure prediction with composite risk scoring, TCO calculation, compliance tracking, field route optimization, and Monte Carlo capital planning with 1,000-iteration convergence. Orchestration is standard LangChain tool binding at temperature 0. The architecture is deliberately boring, and that is the point: the module list of a licensed platform fits in a reasoning layer, a tool layer, and an orchestration layer.

The AI-assisted demo build took roughly 40 to 80 engineer-hours, verifiable in the repository's commit history.

## The measurements

- 59 of 59 unit and integration tests passing (37 tool tests, 22 capital-planning tests)
- End-to-end latency: 1.35 s single-tool, 8.70 s multi-tool (measured early 2026)
- Cost per query on the certified model tier: $0.0030 (AEQ Grid certification run, July 2026)
- The certified $1/MTok tier matched a $5/MTok frontier model 12 cells to 12 on the workload's non-trap query classes

## The honest limits

The demo runs on a 50-asset synthetic portfolio, not a live customer deployment, and the route optimizer was measured against statistical simulation rather than a live road network. Total cost of ownership matters: with build and maintenance labor counted, the agent stack does not beat the per-seat license below roughly 130 seats. Small teams should keep their SaaS. The full accounting, including the assumptions an operator should replace with their own, is in the white paper.

## Read the engineering

The complete formal specification, test inventory, and simulation methodology: [Agentic Architecture for Enterprise Asset Management](/papers/agentic-architecture-enterprise-eam/) (technical reference, v2.1.0).

**Want this measured against your workflow?** A bake-off engagement runs your workload against your incumbent path under a pre-registered rubric and reports the same numbers you see above: tokens, cost, latency, and whether the answers hold up. [Contact](/contact/) to scope one.

---

## Task 2 — Papers index restructure

1. Keep /papers/agentic-architecture-enterprise-eam/ exactly where it is.
2. On the /papers/ index, give each paper a one-line role description:
   - "Agentic Architecture for Enterprise Asset Management (v2.1.0) - Technical reference: design, testing, validation, and simulation of the AgentSaaSy_EAM system."
   - Prepare (unpublished) "The Cost of a Question: The Measured Economics of Certified AI Agents vs. Per-Seat SaaS (v3) - The economics thesis: certified cheap models against per-seat pricing, with a break-even accounting." Slug: /papers/cost-of-a-question/. Leave hidden until instructed.
3. When the v3 paper publishes, each paper's page links to the other: v2.1.0 gets "For the economics argument built on this system, see The Cost of a Question." The v3 page gets "For the system's formal specification, see the technical reference."

## Task 3 — v2.1.1 edit set on the live technical reference page

Three small corrections to /papers/agentic-architecture-enterprise-eam/, bumping the displayed version to v2.1.1:

1. Abstract: replace "an agentic artificial intelligence architecture" with "an AI agent architecture." (Terminology rule above.)
2. Abstract cost sentence: replace "sub-$0.002 measured cost per inference (about $288 per year of model spend at 1,000 queries per day)" with "a measured $0.0009 per query on the early-2026 test model, about $328 per year of model spend at 1,000 queries per day; the certified-tier economics used for any substitution argument are in the v3 white paper." (Fixes an internal inconsistency: the old $288 figure implied $0.0008/query and a 360-day year.)
3. Add a version-history note if the template supports one: "v2.1.1 - terminology and cost-figure consistency corrections; economics accounting moved to the v3 white paper."

## Acceptance checks before you finish

- Case-insensitive grep across changed files: zero hits for "agentic ai" and "agentic artificial intelligence" (nav/title uses "Agentic Architecture," which is allowed).
- All internal links resolve; the hidden v3 slug returns no public link anywhere yet.
- Numbers in the case study match this list exactly: $13,200 / 59 of 59 / 1.35 s / 8.70 s / $0.0030 / 12 to 12 / 40 to 80 hours / ~130 seats / 50 assets.
- Mobile rendering checked on the case study page.
