# Strategy prompt: can the NGAI white paper double as my final class paper?

Copy everything below the line into a Claude chat. Attach or paste the files it names (Claude chat cannot read your disk). Fill in the two placeholders first.

---

I am a master's student in Applied AI at the University of San Diego. I have been building an enterprise asset management platform (AgentSaasy NGAI) as an independent project, and alongside it I ran a pre-registered evaluation program called AEQ. I need to write the final paper for my course, and I want to figure out whether the white paper I already drafted can be adapted to satisfy the class requirements, or whether I should fork it into two documents. I am honestly not sure I have enough, and I want a frank read, not encouragement.

## The assignment

[PASTE THE FINAL PAPER ASSIGNMENT / RUBRIC / SYLLABUS EXCERPT HERE, including page count, required sections, citation expectations, and due date]

Course: [COURSE NUMBER AND NAME]

## What I already have

1. A drafted industry white paper, "Agentic Architecture for Enterprise Asset Management" (v2.1.0, about 1,150 lines / 16-20 pages). It covers a three-layer agent architecture (tools, LLM reasoning, orchestration), requirements engineering, a formal tool-layer spec, testing (37 tests passing), Monte Carlo capital planning simulation across four strategies, latency and cost benchmarks, and a business value section with ROI projections. It is written in a confident practitioner voice for a CTO audience. I am attaching it. (Local path for my own reference: TECHNICAL-WHITE-PAPER.md at the repo root.)

2. A pre-registered evaluation program (AEQ) with locked gates, amendments, and completed runs:
   - Grid-2Q experiment: five query classes (retrieval, analytical, synthesis, a distractor trap, quantitative) against multiple model tiers, temperature 0, three runs per cell, cross-family LLM judging (an Anthropic judge for OpenAI models and vice versa, never same-family). Pre-registration went through versions 1.0 to 1.3, each amendment recorded before the runs it governs. (Local: whitepaper/AEQ_Grid2Q_PreRegistration_v1.md through v1_3.md.)
   - Results as of 2026-07-24: the calibration gate passed on current models (the frontier reference passed 12/12 non-trap cells; the cheap tier failed 2/15 with the failures concentrated where predicted). The most interesting finding is a boundary trap (an urgent-sounding field note about an asset two points above the critical threshold) that catches even the frontier model 3 out of 3 times, so narrative pressure overrides a stated numeric policy. A quantization result also came out backwards from the naive expectation: a 4-bit quantized 3B model beat its own fp16 parent 3-0. (Local: experiments/grid2q/refresh_gpt56_2026-07-24/phase0_report.md, experiments/grid2q/multimodel_2026-07-24/, experiments/grid2q/phase1_2026-07-24/.)
   - A lessons ledger with 11 methodology lessons learned the hard way, e.g. "a rubric everything passes certifies nothing," "evidence must not contain the answer key," "output caps silently zero out reasoning-tier models," "deprecation calendars are part of experimental validity." (Local: whitepaper/AEQ_Lessons_Ledger.md.)
   - A study design doc framing AEQ as business value delivered per token consumed, comparing three agent architectures. (Local: experiments/STUDY-DESIGN.md.)
   - A dual-provider replication pre-registration and results, and an external validation writeup. (Local: whitepaper/AEQ_DualProvider_PreRegistration_v1.md, whitepaper/AEQ_External_Validation_RuVector_Filled.md.)

## What I want from you

1. Gap analysis against the rubric. Go requirement by requirement through the assignment and tell me which parts the existing material already satisfies, which parts need reframing, and which parts do not exist yet (I suspect: literature review / related work, formal citations, explicit research question, statistical treatment of the results, limitations section written academically).

2. A frank sufficiency verdict. Is the experimental base enough for a graduate final paper, or is it thin? If thin, what is the smallest addition that fixes it (more runs, a statistical test, a related-work section, a second dataset), given I have limited time before the deadline?

3. Scoping advice. The white paper tries to cover the whole platform. A class paper probably needs one tight question. Which slice would you carve out as the paper's spine? My instinct is the AEQ evaluation methodology and the frontier-fails-the-boundary-trap finding, with the platform as the motivating context rather than the subject. Push back if a different slice fits the rubric better.

4. The voice problem. The white paper is written as a seasoned practitioner selling an architecture, with strong ROI claims. My class papers need a humble graduate-student register: exploring, measuring, reporting limitations, no marketing numbers. Tell me concretely which sections or claims cannot survive the translation and what replaces them.

5. A decision and a plan. End with a clear recommendation: adapt the white paper, fork it, or write the class paper fresh while reusing the experiments. Then give me an ordered work plan with rough effort per step so I can judge it against the deadline.

Formatting notes for anything you draft: plain ASCII, no em dashes, past tense for anything describing work already done.
