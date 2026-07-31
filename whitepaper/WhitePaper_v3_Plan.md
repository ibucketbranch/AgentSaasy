# White Paper v3 Plan: Agentic Substitution of Workflow SaaS

**Overview:** Restructure the technical white paper (v2.1.0, TECHNICAL-WHITE-PAPER.md) around the substitution thesis: workflow SaaS is priced per seat while the marginal compute to replicate its core workflows with agents is near zero. AgentSaaSy_EAM is the case study, AEQ and the routing study are the measured evidence. v2.1.0 stays untouched; v3 is a new draft alongside it.

**The thesis, stated carefully:** the technical moat of workflow SaaS is gone (measured), the remaining moat is organizational (integrations, data gravity, compliance, SLAs, sales relationships), and that predicts which categories get eaten first. The paper concedes what it did not measure, out loud.

## Workstream 1: Restructure the draft

- [ ] 1.1 Create the v3 draft file (new title, keeps v2.1.0 intact). Working title direction: "The Agentic Substitution: What a Few Agents and a Certified Cheap Model Do to Per-Seat SaaS."
- [ ] 1.2 New abstract and Section 1 carrying the substitution thesis. The current abstract sells the platform; the new one argues the thesis with AgentSaaSy_EAM as evidence.
- [ ] 1.3 Compress architecture material (current sections 4-8) into a "how few parts this took" chapter. Formal tool specs move to an appendix. The point becomes the smallness of the build, not its sophistication.
- [ ] 1.4 Rework the business value section (current 13). Remove marketing-grade claims (the 16,000% ROI line does not survive). Replace with: what incumbents charge vs measured agent compute cost per equivalent workflow.
- [ ] 1.5 Rewrite limitations (current 14) as the moat concession: switching costs, integrations, data custody, compliance, SLAs were not measured. Include the CHIL-005 boundary-trap finding as a real substitution risk: even frontier models let narrative pressure override a stated numeric policy 3 of 3 times, which is exactly why certification gates precede deployment.
- [ ] 1.6 Refresh stale facts from the Feb 2026 draft: deprecated model names, quoted prices, latency/cost figures re-verified against current official pages at publish time (AEQ v1.3 already pinned the gpt-5.6 family with verified prices, reuse that discipline).

## Workstream 2: The economics evidence section (new)

- [ ] 2.1 Write the AEQ program summary: pre-registration v1.0 to v1.3, locked gates, cross-family judging, calibration pass (frontier 12/12 non-trap, cheap tier failing 2/15 where predicted), the quantized-beats-fp16 result, the 11-lesson ledger distilled to the 3-4 lessons a reader needs.
- [ ] 2.2 Write the routing findings summary from the class study's measured results: logistic router at 94% of always-strongest quality for 19% of cost, one fixed cheap model rivaling every trained router, commercial OpenRouter beaten by all of them, LLM-as-router rediscovering the same fixed model with 95% of its picks.
- [ ] 2.3 Land the combined playbook: certify a small menu with AEQ-style gates, default to the cheapest certified model, skip per-request routing complexity until the menu itself is the bottleneck.
- [ ] 2.4 Build the consolidated results table and figures: AEQ pass matrix, routing cost-vs-quality chart, one cost-per-workflow figure. Source data lives in experiments/grid2q/ dashboards and the class repo notebooks (figures rebuilt, not copied).

## Workstream 3: Incumbent pricing comparison (new, load-bearing)

- [ ] 3.1 Research real public pricing for EAM/CMMS incumbents (candidates: IBM Maximo, Fiix, UpKeep, Limble, eMaint). Record price, unit (per seat/asset/site), tier, source URL, and capture date for each. No estimates; skip vendors whose pricing is quote-only and say so.
- [ ] 3.2 Build the comparison table: incumbent monthly cost for a reference org size vs measured agent compute cost for the equivalent workflow set. State assumptions explicitly (org size, request volume).
- [ ] 3.3 Skeptic pass on the table: this is the section a hostile reader checks first. Every number gets a source and date.

## Workstream 4: Citation and boundary hygiene

- [ ] 4.1 Cite the routing study as Michael's own measured work with a link to the class repo once it flips public (after Aug 10). Findings cross, text does not: no prose reuse from the student paper. No implication of USD endorsement.
- [ ] 4.2 Cite AEQ via the pre-registration documents and run reports in this repo (already public on GitHub).
- [ ] 4.3 Gate check before publishing: nothing that cites the class study goes public before the Aug 10 submission and the repo flip.

## Workstream 5: Polish and publication

- [ ] 5.1 Full AI-fingerprint scrub and professional-register pass on the v3 draft (plain ASCII, no em dashes, past tense for completed work).
- [ ] 5.2 Produce the publishable artifacts: PDF, and a refreshed one-pager (agent_loop_economics_onepager.html can be updated to the new thesis).
- [ ] 5.3 Draft the launch post and the provocative-questions thread, each question paired with the number that backs it (what is the per-seat license paying for; which SaaS categories survive a prompt library; why did a logistic regression beat the commercial router).
- [ ] 5.4 Optional follow-on experiment: pre-register a Grid-2Q arm testing "certified cheapest fixed model" against the platform's current model choice, using the existing harness and the v1.3 discipline. Strengthens the playbook claim with a purpose-built result.

## Order and gates

Start now, no dependencies: 1.1-1.6, 2.1, 2.4 (AEQ side), 3.1-3.3, 5.4 registration draft.
Needs the class numbers finalized (they are, in the milestone doc): 2.2, 2.3.
Gated on Aug 10 submission + repo flip: 4.1 link, 5.2 publish, 5.3 post.
Last before publish: 5.1 scrub, 4.3 gate check, 1.6 price re-verification.
