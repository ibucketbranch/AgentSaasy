# Strategy prompt: unify the NGAI white paper and the AAI-501 final project as one body of work, two deliverables

Copy everything below the line into a Claude chat. Attach the files listed at the end (Claude chat cannot read your disk). The decision to keep the two deliverables separate is already made; the ask is how to make them reinforce each other.

---

I am a master's student in Applied AI at the University of San Diego (AAI-501, Intro to AI and ML). I have two related pieces of work and I decided to keep them as separate deliverables. I want a strategy for making them one coherent body of work without letting either one bleed into the other's lane.

Deliverable 1 is my graded final class project, due Aug 10, 2026, no extensions, 280 points. My instructor approved a solo path. The approved proposal (submitted Jul 14) is "Cost-Aware Routing of Large Language Models: Predicting the Cheapest Capable Model for Each Request." It committed me to the LLMRouterBench dataset (23,945 prompts, 391,645 records across models, each with token counts, dollar cost, and a quality score), two course algorithm types (classification to predict the cost-optimal model, regression to predict request cost), comparison against always-cheapest and always-strongest baselines, optional k-means clustering of prompts by economic profile, a scikit-learn pipeline in a documented notebook, GitHub with README and PEP 8, and an APA 7 report of about 10 pages. I am pasting the official scoring rubric below.

Deliverable 2 is an independent professional white paper on my AgentSaasy NGAI platform (enterprise asset management agents), which contains a pre-registered evaluation program I ran called AEQ. Highlights: a five-query-class grid (retrieval, analytical, synthesis, a boundary-trap distractor, quantitative) across model tiers at temperature 0 with cross-family LLM judging, pre-registration versions 1.0 to 1.3 each recorded before the runs they govern, a calibration gate that passed on current models (frontier 12/12 non-trap cells, cheap tier failing 2/15 where predicted), a boundary trap that catches even the frontier model 3 of 3 times (narrative urgency overriding a stated numeric threshold), a quantized 3B model beating its fp16 parent 3-0, and an 11-lesson methodology ledger. This is practitioner R&D in a confident professional voice, and it stays that way.

The two share one theme: pick the cheapest model that is still capable. AEQ measures whether cheap tiers hold up; the class project learns to predict, per request, which model to route to.

## What I want from you

1. Unification strategy. How do I present these as one research arc (my own measurements motivated the routing question, the routing project answers a piece of it, the results flow back into the white paper) while keeping the graded paper strictly inside its approved proposal? Concretely: where in the class report can I reference my own AEQ work (introduction, motivation, related work) without it counting against me, given the course's AI-disclosure and plagiarism rules and given that citing your own unpublished measurements in APA 7 needs a defensible format?

2. Rubric-mapped work plan for the class project. Map the remaining work to the rubric weights below (algorithms+theory+code 25%, execution 25%, analysis 20%, setup 15%, report 15%) and to the required artifacts (notebook, repo, ~10 page APA 7 report, 20-30 min recorded presentation, contributions appendix). Order the steps so the heavy-weight criteria get finished first, and flag which proposal promises are load-bearing (leakage-safe splits by prompt, label sensitivity to the quality threshold, cost-saved-at-quality metric instead of raw accuracy).

3. Voice firewall. The class paper needs a humble graduate-student register; the white paper is a confident practitioner document. List the specific claims and phrasings that must not cross from the white paper into the class paper (ROI projections, marketing numbers, "production-grade" language) and what the student-register equivalent looks like.

4. Feedback loop into the white paper. After the class project is done, which of its results earn a place in the white paper or the AEQ program (for example, a learned router as a fourth architecture in the AEQ study design), and which do not?

5. Risks. Anything that could threaten the Aug 10 submission: scope creep from the white paper side, the optional clustering step, dataset size or preprocessing surprises, Turnitin/AI-disclosure issues. For each, the mitigation.

## Official scoring rubric (captured from Canvas 2026-07-24; criterion 1 says "image set" but it is a recycled template, read it as "dataset")

1. Project Selection and Setup (15%, 42 pts): clearly stated objectives, feasible approach, available dataset, properly scoped.
2. Algorithm Descriptions, Theory and Source Code (25%, 70 pts): clear algorithm description, explicit theory with proper mathematical/logical composition, self-documenting code.
3. Execution and Output (25%, 70 pts): code executes on sample data; complete data set produced from multiple runs.
4. Analysis, Results and Conclusions (20%, 56 pts): well-presented results, accurate conclusions.
5. Report Format, Citations, Content (15%, 42 pts): proper length (~10 pages excluding appendices), APA 7, professional presentation. Length more than 20% out of bounds is penalized.

Other requirements: GitHub required with README, PEP 8, code submitted or publicly linked in both report and Canvas; graphical algorithm comparisons preferred; contributions appendix; Turnitin enabled; AI tool use must be explicitly disclosed, cited, and explained.

## Attachments I am providing

- Assignment_3.3_Proposal_AEQ_Routing.pdf (my approved proposal)
- Final_Team_Project_Instructions.md (official instructions, captured from Canvas)
- TECHNICAL-WHITE-PAPER.md (the white paper draft, v2.1.0)
- AEQ_Lessons_Ledger.md and AEQ_Grid2Q_PreRegistration_v1_3.md (the AEQ program)
- phase0_report.md from the 2026-07-24 refresh run (latest AEQ results)

Formatting for anything you draft: plain ASCII, no em dashes, past tense for work already done.
