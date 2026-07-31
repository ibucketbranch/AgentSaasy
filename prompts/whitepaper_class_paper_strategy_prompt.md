# Strategy prompt: fold the routing-project findings and AEQ into the AgentSaaSy_EAM white paper (professional track)

Copy everything below the line into a Claude chat. Attach the files listed at the end (Claude chat cannot read your disk), including the context package, which is the authoritative briefing on the class project and its boundaries.

Status this prompt assumes: the AAI-501 class project is complete on the analysis side (notebooks executed, draft report written and built); only polish and logistics remain, owned elsewhere, due Aug 10. Its scope is closed. This conversation is the professional track and must not write into the school deliverable or its repo.

---

I am an AI engineer with two connected bodies of work and one theme: pick the cheapest model that is still capable. I need a strategy for unifying them into a single professional research arc with the AgentSaaSy_EAM white paper as the flagship document. One of the two is graded academic work whose scope is closed; read the attached context package first, it states the commitments, results, and boundaries, and it wins over anything else here if they conflict.

Track 1, closed and measured (the class project): cost-aware LLM routing on LLMRouterBench, solo, University of San Diego AAI-501, submission Aug 10. Key results on 2,434 held-out test prompts: a logistic-regression router reached 94 percent of always-strongest quality at 19 percent of its cost ($0.0115 / 0.564 vs $0.0615 / 0.597); a random forest came in at $0.0073 / 0.536; a cost-regressor-driven router at $0.0006 / 0.513; the best fixed single model (qwen3-235b-a22b-2507) at $0.0009 / 0.538; the commercial OpenRouter reference at $0.0225 / 0.495, beaten by every trained approach; the oracle ceiling at $0.0055 / 0.822. An LLM-as-router experiment (claude-haiku-4-5 choosing from a model menu, 300 prompts) sent 95 percent of traffic to that same fixed qwen model. The paper's thesis: the hard part of routing turned out to be knowing the menu, not picking per request. The gap to the oracle is informational, not economic.

Track 2, ongoing and mine to shape (the professional work): the AgentSaasy AgentSaaSy_EAM platform white paper (v2.1.0 draft, enterprise asset management agents) and the AEQ evaluation program inside it. AEQ ran a pre-registered five-query-class grid (retrieval, analytical, synthesis, a boundary-trap distractor, quantitative) across model tiers at temperature 0 with cross-family LLM judging. Pre-registration v1.0 to v1.3, each amendment recorded before the runs it governs. Results: calibration passed on current models (frontier 12/12 non-trap cells, cheap tier failing 2/15 where predicted); a boundary trap that catches even the frontier model 3 of 3 times (narrative urgency overriding a stated numeric threshold); a 4-bit quantized 3B model beating its fp16 parent 3-0; an 11-lesson methodology ledger.

The two tracks answer complementary halves of the same question. AEQ asks: does a cheap tier actually hold up on my workload? The routing project asks: given recorded outcomes, can you predict per request which model is the cheapest capable one, and is per-request prediction even worth it over picking one good cheap model?

## What I want from you

1. The unified arc. Propose the storyline that presents AEQ and the routing findings as one research program in the white paper. My starting intuition: AEQ certifies tiers on a specific workload, the routing study shows menu knowledge dominates per-request cleverness, and together they argue for "certify a small menu, default to the cheapest certified model" over both flat frontier-everything deployment and complex per-request routers. Pressure-test that framing against the actual numbers and tell me where it overreaches.

2. White paper surgery. Where does this land in the existing draft? Name the sections to add or rewrite (the draft currently has architecture, testing, Monte Carlo simulation, business value), what gets displaced, and roughly how many pages. The white paper's model-economics story is currently thin; AEQ plus routing could become its strongest section.

3. AEQ program extension. Does a learned or fixed-menu router earn a place as a new arm in the AEQ study design (the study compares agent architectures on value per token)? If yes, sketch the smallest pre-registerable experiment that tests "certified cheapest fixed model" against the platform's current model choice on the existing Grid-2Q harness, consistent with the discipline in the pre-registrations (declared priors, locked gates, cross-family judging).

4. Citation and boundary hygiene. The routing numbers come from graded coursework under an honor code. How do I cite my own class project in a professional white paper cleanly (format, attribution, timing relative to the Aug 10 submission), and what must I avoid (copying prose from the student paper, implying USD endorsement, reopening its scope)? The student paper stays in its voice and repo; the white paper reuses findings, not text.

5. Sequencing. What can start now without touching the class deliverable, and what waits until after Aug 10? Give an ordered plan.

## Boundaries (from the context package, non-negotiable)

- The class project's commitments are closed; do not propose reopening them before Aug 10.
- Complementary work must not write into the school deliverable or its private repo.
- The student paper keeps its academic register; the white paper keeps its professional register; findings cross, text does not.

## Attachments I am providing

- Complementary_Conversation_Context_Package.md (authoritative class-project briefing)
- TECHNICAL-WHITE-PAPER.md (the white paper draft, v2.1.0)
- AEQ_Lessons_Ledger.md and AEQ_Grid2Q_PreRegistration_v1_3.md (the AEQ program)
- phase0_report.md from the 2026-07-24 refresh run (latest AEQ results)

Formatting for anything you draft: plain ASCII, no em dashes, past tense for work already done.
