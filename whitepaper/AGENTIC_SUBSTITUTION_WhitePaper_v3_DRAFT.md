# The Agentic Substitution: What a Small Agent Stack and a Certified Cheap Model Mean for Per-Seat SaaS

**A White Paper**

**AgentSaasy_NGAI | NexGen Asset Management Platform**

---

**Author:** Michael Valderrama
**Date:** July 24, 2026 (working draft)
**Version:** 3.0.0-draft
**Supersedes:** none; the v2.1.0 technical reference (TECHNICAL-WHITE-PAPER.md) remains the canonical architecture document. This paper argues a thesis; that one specifies a system.
**Repository:** github.com/ibucketbranch/AgentSaasy_NGAI

> DRAFT STATUS: the incumbent pricing table in Section 6 was captured from vendor pages on July 24, 2026 and must be re-verified at publish time. The routing study citation in Section 4 links to a repository that goes public after the study's academic submission (August 10, 2026). Nothing in this draft publishes before that date.

---

## Abstract

Workflow SaaS is priced per seat. The marginal cost of replicating a workflow SaaS product's core functions with LLM agents is priced per token, and the token side has collapsed. This paper argues, with measurements rather than projection, that the technical moat of workflow SaaS is gone and that what remains is organizational: integrations, data custody, compliance certifications, and sales relationships. The evidence is one case study and two measurement studies. The case study is AgentSaasy_NGAI, an enterprise asset management (EAM) agent stack that reimplements the module list of a commercial EAM product in seven Python tools behind one language model, at a measured $0.0009 average cost per query. The first study, AEQ, is a pre-registered evaluation program that certifies whether cheap model tiers hold up on the actual workload: on the four non-trap query classes of its hardened rubric, a $1.00-per-million-token model matched a $5.00-per-million-token frontier model 12 cells to 12, at one fifth the measured cost per query. The second study, a cost-aware routing experiment on 2,434 held-out benchmark prompts, found that one cheap fixed model rivaled every trained router and beat the commercial routing product on both cost and quality. Together they support a deployment rule that undercuts both per-seat pricing and per-request routing complexity: certify a small menu of models against your workload, default to the cheapest certified one. The paper closes with what the evidence does not prove, and with a prediction about which SaaS categories are exposed first.

---

## 1. The Claim, Stated Carefully

The strong version of the claim circulating in 2026 is "AI agents will kill SaaS." That version is unfalsifiable and mostly marketing. The version this paper defends is narrower and has numbers attached:

1. For a workflow SaaS product, defined as one whose value is dominated by rules, CRUD operations, reporting, and scheduled checks over customer data, the compute cost of replicating the product's core functions with an agent stack is now negligible relative to the product's per-seat price.
2. The models required to run that stack acceptably are not the expensive ones. Whether a cheap tier holds up is an empirical, per-workload question, and it can be answered cheaply and rigorously before deployment.
3. The remaining defensible value of the incumbent is organizational, not technical: integrations, data gravity, compliance certifications, SLAs, and the sales relationship. None of those are measured here, and Section 7 says so plainly.

Point 1 rests on the NGAI case study (Section 2) and the pricing comparison (Section 6). Point 2 rests on the AEQ certification program (Section 3) and the routing study (Section 4). Point 3 is the concession the argument needs, and it does predictive work: it identifies which categories fall first (Section 8).

## 2. The Case Study: a Platform's Worth of Workflows in Seven Tools

A commercial EAM/CMMS product sells, roughly, this module list: asset registry and search, condition monitoring, predictive maintenance, cost and TCO reporting, compliance and inspection tracking, field service dispatch, and capital planning. These are sold as product tiers and priced per user per month.

AgentSaasy_NGAI implements that module list as seven Python tools bound to one language model through LangChain: asset query, health analysis, failure prediction (composite risk scoring with z-score anomaly detection), TCO calculation, compliance tracking, field route optimization, and Monte Carlo capital planning (1,000-iteration, four-strategy comparison with P10/P50/P90 bounds). The full formal specification, test inventory, and simulation methodology are in the v2.1.0 technical reference and are not repeated here.

What matters for the thesis is the size and the cost of the build, measured in early 2026 on the demo portfolio:

| Measure | Value |
|---|---|
| Tools implemented | 7 |
| Test suite | 37/37 passing |
| End-to-end latency, single-tool query | 1.35 s |
| End-to-end latency, complex multi-tool query | 8.70 s |
| Average cost per query | $0.0009 |
| Annual API cost at 1,000 queries/day | ~$288 |
| Memory per stateless instance | ~250 MB |

Two caveats belong next to that table rather than buried in a limitations section. The demo dataset is 50 synthetic assets, not a live customer portfolio, and the route optimizer was measured against statistical simulation rather than a live road network. The case study shows how little engineering the module list requires; it is not a production deployment report.

The architecture is deliberately boring: a reasoning layer (one chat model, temperature 0), a tool layer (seven functions over a DataFrame), an orchestration layer (standard tool binding). The interesting question was never whether this could be built. It is whether it holds up on a cheap model, and what that does to the economics. That is what the two studies measure.

## 3. Study One: Does the Cheap Model Hold Up? (AEQ)

### 3.1 Method

AEQ (Agent Efficiency Quotient) is a pre-registered evaluation program run against the NGAI workload. Its discipline, developed across four runs and recorded in an append-only lessons ledger, is the part most evaluation efforts skip:

- **Pre-registration before execution.** Query classes, rubrics, gates, and priors were registered before each run (versions 1.0 through 1.3); every amendment was recorded before the run it governs. Improvements never touched a live run.
- **A calibration gate.** No rubric certifies anything until it has demonstrably failed a weaker system. The first rubric saturated (every tier passed everything) and was therefore discarded as certifying nothing.
- **Five query classes** drawn from the workload: retrieval, analytical ranking, synthesis, a distractor trap, and quantitative derivation.
- **Cross-family judging.** An Anthropic judge scores OpenAI candidates and vice versa, never same-family. Every FAIL verdict is independently re-adjudicated; a judge is a measurement device and gets its own error model.
- **Temperature 0, three runs per cell.** Failures proved stable: every failing model failed the same way three out of three times, which makes a certification durable until a model version changes.
- **Deprecation and pricing hygiene.** A pre-publication check found the original test models deprecated with unlisted prices; the program re-ran on current models with prices verified against official pages the same day. A result on a model a reader cannot access or price is a demo, not evidence.

### 3.2 Results (refresh run, July 24, 2026, prices verified same day)

Frontier reference: gpt-5.6-sol at $5.00 / $30.00 per million tokens (input/output). Cheap tier: gpt-5.6-luna at $1.00 / $6.00. Judge: claude-opus-4-8, cross-family for all OpenAI cells.

| Query class | Frontier ($5/MTok) | Cheap tier ($1/MTok) |
|---|---|---|
| Retrieval | 3/3 | 3/3 |
| Analytical | 3/3 | 3/3 |
| Synthesis | 3/3 | 3/3 |
| Quantitative | 3/3 | 3/3 |
| Distractor trap | 0/3 | 1/3 |
| **Non-trap total** | **12/12** | **12/12** |
| Measured cost per query | $0.0152 | $0.0030 |

![AEQ pass matrix: cheap tier vs frontier across the five query classes](figures/aeq_pass_matrix.png)

On every non-trap class, the cheap tier was indistinguishable from the frontier reference, at one fifth the measured cost per query. On the trap class it did slightly better than the frontier. The pre-registered prior for this run (cheap tier fails 2 to 6 of 15 with failures concentrating in the hard classes) was confirmed: it failed exactly 2, both in the trap class.

### 3.3 The two findings that were not supposed to happen

**The trap catches the frontier.** The distractor class centers on an asset with a health score of 52, two points above the explicit critical threshold of 50, described in an urgent-sounding field note. The rule is stated in the evidence; the urgency is noise. The frontier model added the asset to the critical list 3 out of 3 times. Across the program's runs, every model family and size fell for this at least once. Models over-weight emotionally salient text against numeric thresholds, and that is precisely the class of error that costs money in a production agent. Two implications: rubrics without a trap class overstate every model, and "use the biggest model" is not a control for this failure mode, since the biggest model failed it most consistently.

**Quantization did not order capability.** In a paired run on pinned local weights, a 4-bit quantized 3B model passed 3 cells where its own fp16 parent passed 0, on the identical rubric. Between separate runs, a 7B model failed a quantitative class by fabricating internally consistent numbers while a 3B model pulled the correct inputs and divided them correctly. Capability is per-class and per-workload, not per-parameter-count or per-precision. The only way to know what a given model does on a given workload is to measure that pair.

The general lesson of Section 3 is not "cheap models are good." It is that the question "is the cheap tier good enough here" has a cheap, rigorous, repeatable answer, and the answer in this workload was yes for four of five classes, with the fifth failing for everyone including the frontier.

## 4. Study Two: Do You Even Need to Be Clever About Choosing? (Routing)

The author's separate academic study (Valderrama, 2026, University of San Diego; conducted independently of this paper, full citation in References; its repository remains private until the August 2026 submission) asked the complementary question: given recorded outcomes for many models on many prompts, can a learned router predict, per request, the cheapest capable model, and is per-request prediction even worth it?

The study ran on LLMRouterBench (Findings of ACL 2026), evaluating on 2,434 held-out prompts with a leakage-safe prompt-level split. Measured results:

| Strategy | Mean cost/query | Mean quality |
|---|---|---|
| Always-strongest (gemini-2.5-pro) | $0.0615 | 0.597 |
| Oracle (per-prompt perfect choice) | $0.0055 | 0.822 |
| Logistic-regression router | $0.0115 | 0.564 |
| Random-forest router | $0.0073 | 0.536 |
| Cost-regressor-driven router | $0.0006 | 0.513 |
| Best fixed single model (qwen3-235b) | $0.0009 | 0.538 |
| Commercial router (OpenRouter reference) | $0.0225 | 0.495 |

![Routing strategies: mean cost per query (log scale) against mean quality](figures/routing_cost_quality.png)

Four findings matter here. The learned router captured 94 percent of always-strongest quality at 19 percent of its cost, so routing works. A single cheap fixed model rivaled every trained router, reproducing the benchmark's own published finding that most routers fail to beat the best single model. The commercial routing product lost to every trained approach in the study on both cost and quality. And an LLM-as-router experiment (prompting a model to choose from the menu per request) converged on the same answer by itself, sending 95 percent of traffic to that same fixed model.

The study's thesis, in its own words: the hard part of routing turned out to be knowing the menu, not picking per request. The gap between the fixed-model strategy and the oracle is informational (knowing which prompts are the exceptions), not economic (the money is already saved).

## 5. The Playbook: Certify a Menu, Default to the Cheapest Certified Model

The two studies compose into a deployment rule.

1. **Extract query classes from the real workload.** Five classes covered the EAM workload: retrieval, ranking, synthesis, trap, derivation.
2. **Write a rubric and make it fail someone.** Include at least one just-above-threshold trap dressed in urgent language. Run the calibration gate: if a weak model passes everything, the rubric is measuring nothing; harden it and re-register.
3. **Judge cross-family, re-adjudicate every FAIL, temperature 0, three runs per cell.** The whole certification of a five-model panel cost roughly $0.02 of judge spend per cell.
4. **Certify the cheapest tier that passes each class.** In the NGAI workload that was the $1/MTok tier for four of five classes.
5. **Default all traffic to the cheapest certified model.** Per-request routing earned its complexity in neither study; add it only if certification produces a genuinely split menu across classes.
6. **Guard the class that failed everyone.** Where no tier passes (the trap class), the mitigation is a deterministic check in the tool layer, not a bigger model. A threshold comparison does not need a language model.
7. **Re-certify on version bumps and watch deprecation calendars.** Temperature-0 failures are stable, so certification holds between versions; hosted models rot on a schedule the vendor publishes.

This is the AEQ Verify service pattern in seven steps, and it is what replaces both "pay for the frontier everywhere" and "buy a routing product."

## 6. The Economics Against Per-Seat Pricing

The compute side of the ledger is measured. The NGAI stack averaged $0.0009 per query in benchmark use; at 1,000 queries per day that is roughly $288 per year of model spend for a workload that spans the incumbent module list. The AEQ certification that de-risked the cheap tier cost about $0.02 per cell of judge spend, a one-time cost per model version.

The incumbent side of the ledger requires sourced, dated public prices, and estimates are not acceptable here because this is the table a skeptical reader checks first. Three representative vendors were checked directly on their own pricing pages on July 24, 2026: one mid-market vendor that publishes list prices, one that recently stopped publishing them, and the enterprise anchor.

| Vendor / product | Public list price (captured 2026-07-24) | Notes | Source |
|---|---|---|---|
| UpKeep, Essential tier | $24 per user per month | Monthly billing as shown; unlimited view-only and requester users free | upkeep.com/pricing |
| UpKeep, Premium tier | $55 per user per month | Monthly billing as shown; Professional and Enterprise tiers are quote-only | upkeep.com/pricing |
| Limble CMMS (Standard, Premium+, Enterprise) | No public list price | All three tiers route to a "Calculate my price" flow; no dollar amounts on the page | limble.com/pricing |
| IBM Maximo Application Suite | Quote-only | Page offers "Request a quote," a price estimator, and a demo; no dollar amounts | ibm.com/products/maximo/pricing |

Two observations before the arithmetic. Only one of the three vendors still publishes a list price at all; price opacity is itself part of the per-seat model this paper is examining. And the published prices are per human seat, a unit that has no relationship to the marginal cost of answering a maintenance question.

The arithmetic, with assumptions stated: a 20-technician maintenance team on UpKeep Premium pays 20 x $55 = $1,100 per month, $13,200 per year, for the module list of Section 2. The NGAI stack answering 1,000 queries per day, roughly one query per technician every 10 minutes of a working day, costs about $288 per year in model spend at the measured $0.0009 per query. That is 2.2 percent of the seat bill. On the Essential tier the same comparison is $5,760 per year against $288, or 5 percent. The certification that de-risked the cheap model adds a one-time cost of a few dollars per model version. Seat prices for the quote-only vendors are, by construction, not comparable here, which is the point of recording them as quote-only rather than estimating.

![Annual cost comparison: UpKeep seat licenses against NGAI agent compute](figures/annual_cost_bars.png)

Two accounting notes. First, prior versions of this document quoted a marginal ROI figure computed as operational value over API cost; that framing is retired. API cost is the wrong denominator for a substitution argument, and projected operational value is the wrong numerator for a skeptical audience. The comparison that matters is what the incumbent charges versus what the workflow costs to run, with implementation labor acknowledged as the real upfront cost on the agent side. Second, the token side of this ledger has a direction: the certified-cheap price used here ($1/MTok in, $6/MTok out) is itself a market price that has been falling across vendor generations, while per-seat list prices have not.

## 7. What This Does Not Prove

The measurements establish that the compute is cheap and that cheap models hold up on this workload under a hardened rubric. They do not establish that an incumbent's customers will move. Specifically not measured: migration and switching costs, integration surface (ERP, SCADA, GIS, procurement), data custody and residency requirements, compliance certifications (SOC 2, FedRAMP and their industry equivalents), contractual SLAs, and the enterprise sales relationship. For a municipal utility, several of those are the purchase decision.

The trap finding cuts against the substitution thesis too, and belongs in this section as much as in Section 3. An agent that lets an urgent-sounding note override a stated numeric policy is exactly the failure a buyer fears, and the frontier model committed it 3 out of 3 times. The honest conclusion is not "agents are ready everywhere" but "agents are ready where the workload has been certified and the known failure classes are guarded deterministically." That is a real engineering bar, and it is the reason certification-first deployment is the paper's recommendation rather than a nice-to-have.

Finally, the case study runs on a 50-asset synthetic portfolio. The database scaling projections in the v2.1.0 reference cover the data layer, but no claim here extends to a live 500,000-asset deployment.

## 8. Which Categories Are Exposed First

If the moat is organizational rather than technical, the substitution order follows from where the organizational moat is thinnest:

- **Exposed first:** single-workflow tools priced per seat with light integration surface: inspection trackers, report generators, scheduling and dispatch tools, form-driven compliance products. Their feature list is a prompt library, their data is already the customer's, and their integrations are shallow.
- **Exposed next:** module-tier platforms like mid-market CMMS, where each module is separable and an agent stack can eat one module at a time from the inside of an existing customer relationship.
- **Defended, for now:** products whose value is network effects (marketplaces), regulated data custody, or being the system of record that many other systems integrate against. The moat there was never the workflow logic.

The prediction is testable: substitution shows up first as seat-count shrinkage at renewal in the first category, not as dramatic platform rip-outs.

## 9. Conclusion

A platform's worth of EAM workflows fit in seven tools behind one model at $0.0009 a query. A pre-registered certification program showed a $1/MTok model matching a $5/MTok frontier on every non-trap class of that workload at one fifth the cost, and showed the frontier failing the one class everyone failed. A routing study evaluated on 2,434 held-out benchmark prompts showed that a single well-chosen cheap model rivals learned routers and beats the commercial one. The deployment rule that falls out is short: certify a small menu against your own workload, default to the cheapest certified model, guard the failure classes with deterministic checks, and re-certify on the vendor's calendar.

The questions this leaves for the reader are the uncomfortable ones. If the compute to replicate a workflow product costs a fraction of a cent per decision, what is the per-seat license paying for? Which parts of your product would survive your customer running this certification against it? And if a logistic regression beat the commercial router, how much of the current AI-infrastructure layer is solving a problem that a certified menu makes disappear?

---

## References

1. Valderrama, M. (2026). AEQ Grid-2Q pre-registration series v1.0-v1.3, lessons ledger, and run reports. AgentSaasy_NGAI repository, whitepaper/ and experiments/grid2q/. github.com/ibucketbranch/AgentSaasy_NGAI
2. Valderrama, M. (2026). Cost-Aware Routing of Large Language Models: Predicting the Cheapest Capable Model for Each Request. University of San Diego, AAI-501 final project. github.com/ibucketbranch/MS-AAI-501-Final_Project_IntroAI [Repository is private until the August 2026 submission; before publication, verify the link resolves and the final title matches the submitted paper.]
3. LLMRouterBench: a massive benchmark and unified framework for LLM routing. (2026). Findings of the Association for Computational Linguistics: ACL 2026. arxiv.org/abs/2601.07206
4. Ong, I., et al. (2024). RouteLLM: learning to route LLMs with preference data. arxiv.org/abs/2406.18665
5. Chen, L., Zaharia, M., & Zou, J. (2024). FrugalGPT: how to use large language models while reducing cost and improving performance. TMLR.
6. Yao, S., et al. (2022). ReAct: synergizing reasoning and acting in language models. arxiv.org/abs/2210.03629
7. Valderrama, M. (2026). Agentic architecture for enterprise asset management (v2.1.0). TECHNICAL-WHITE-PAPER.md, this repository. The canonical architecture, testing, and simulation reference for the NGAI system.

## Appendix: Where the Evidence Lives

| Claim | Source in this repository |
|---|---|
| Case-study latency, cost, test results | TECHNICAL-WHITE-PAPER.md sections 9, 11 |
| AEQ method and gates | whitepaper/AEQ_Grid2Q_PreRegistration_v1.md through v1_3.md |
| AEQ refresh results (verified pricing) | experiments/grid2q/refresh_gpt56_2026-07-24/phase0_report.md |
| Five-model comparison | experiments/grid2q/multimodel_2026-07-24/phase0_report.md |
| Quantization result (fp16 vs Q4) | experiments/grid2q/phase1_2026-07-24/phase0_report.md |
| Methodology lessons L1-L11 | whitepaper/AEQ_Lessons_Ledger.md |
| Routing study | [public repository link after August 2026 submission] |
