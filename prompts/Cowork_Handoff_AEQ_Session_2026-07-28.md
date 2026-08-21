# COWORK HANDOFF PROMPT
## AEQ / White Paper Restructure — Session of 2026-07-28

---

### WHO I AM

Michael Valderrama | AI Agent Architect | Independent R&D
- 30 years in tech: Intel chipset I/O architecture (Sandy Bridge era), Apple Technical Program Manager, enterprise AI
- USAF veteran, MS Applied Artificial Intelligence (University of San Diego)
- Creator of the Agent Efficiency Quotient (AEQ) framework
- Builder of AgentSaaSy_EAM — an enterprise asset management AI agent system
- GitHub: github.com/ibucketbranch (AgentSaaSy repos currently **private**)
- Published: medium.com/@michael_valderrama

### IMPORTANT TERMINOLOGY

- NEVER say "Agentic AI" — use "AI Agents" or "Agentic Agents" instead. Run `grep -n -i "agentic ai"` on every document before delivery.
- AEQ is an ARCHITECTURE QUALITY metric, NOT a cost metric
- The chip concept is spelled **LEOPARD** (LLM Execution and Orchestration Processor, Advanced Routing Design) — not LEOpared
- Attribution: "Michael Valderrama | AI Agent Architect | Independent R&D © 2026"

---

## PART 1 — WHAT THIS SESSION FOUND

I brought in the v3 draft of "The Agentic Substitution" white paper for a publication readiness review. Two blockers and one structural problem came out of it.

### Blocker 1 — the headline cost figure priced an uncertified model

The paper's economics used **$0.0009/query**. That number was measured on **GPT-4o-mini at $0.15/$0.60 per MTok** in early 2026 — a model the AEQ certification program never certified.

The paper's own AEQ refresh run (2026-07-24) measured the **certified** tier (gpt-5.6-luna, $1/$6 per MTok) at **$0.0030/query**.

So the paper used an uncertified number in a paper arguing "certify before you deploy." Self-inflicted, and it's the one-sentence dismissal a reviewer reaches for.

Corrected figures (365,000 queries/yr at 1,000/day):
- Certified tier @ $0.0030 → **$1,095/yr** = 8.3% of a 20-seat UpKeep Premium bill ($13,200). Still a ~12x advantage.
- Frontier tier @ $0.0152 → $5,548/yr = 42% of Premium, and 96% of the entire Essential seat bill.

**That last line is the real finding: certification is what produces the economics.** Skip it, default to the frontier, and the substitution argument against the cheaper tier disappears.

### Blocker 2 — implementation labor was never quantified

The draft acknowledged labor in one clause. Quantifying it flips the conclusion at small scale:
- 20 seats, year one: ~$94,395 (build amortized + maintenance + re-cert + hosting + model spend) vs $13,200 incumbent. **The agent stack loses ~7:1.**
- Break-even vs UpKeep Premium: **~154 seats** with a 3-year amortized build; ~72 seats excluding build.
- Break-even vs Essential: ~400 seats.

This is *good* for the argument — it converts a weak "we're 2% of the cost" claim into a falsifiable seat-count threshold, and it explains why substitution shows up as seat shrinkage at renewal rather than platform rip-out.

**Full drop-in replacement text exists** in `v3_Blocker1_Blocker2_Corrections.md` (attached / in outputs).

### Structural problem — I have two different instruments both named AEQ

| | `AEQ_Specification_v1.0.md` (canonical) | The white paper's usage |
|---|---|---|
| Definition | Business Value Delivered ÷ Tokens Consumed | A pre-registered model certification program |
| Unit under test | The agent's architecture | The model, against query classes |
| Question | Is this agent well-built? | Is this model adequate for this workload? |
| Validated result | 4.68x token spread, identical value, same model | Cheap tier 12/12 non-trap cells vs frontier |

My own spec says: *"Anything that cites AEQ should cite this document as the source of truth."* The white paper cites AEQ and does not match it.

**Resolution agreed:** AEQ stays the architecture quality metric. The certification program becomes **AEQ Grid** (a named application of the framework to model selection). AEQ-L stays as the proposed loop variant. This must be fixed **before** any trademark filing — a mark meaning two things is a weaker mark.

---

## PART 2 — STRATEGIC DECISIONS MADE

### Cut the SaaS substitution frame

Four of six publication blockers exist only because of it (cost table, TCO, OpenRouter vendor exposure, and a routing-study repo that stays private until Aug 10). It's also the least differentiated claim I own — "AI agents will kill SaaS" is a crowded take.

### The unifying thesis I'm moving toward

> **A model's specifications do not predict whether it is adequate for your workload. Only measuring the pair does.**

Five independent findings support it:
1. **The trap** — the biggest model failed worst. Size doesn't predict.
2. **Quantization** — a 4-bit 3B beat its own fp16 parent. Precision doesn't predict.
3. **4.68x** — same model, same query, same answer, 4.68x tokens. The model isn't even the variable.
4. **Routing** — a fixed cheap model rivaled every trained router. Per-request cleverness doesn't pay.
5. **Calibration gate** — a rubric everything passes measures nothing. The instrument must be able to fail something.

**OPEN QUESTION FOR COWORK:** I already have a competing unifying frame — the "Prompt to Silicon" three-layer story (Architecture / Runtime / Silicon) in `Cowork_Handoff_Prompt_to_Silicon.md`. That frame puts AEQ at Layer 1, quantization at Layer 2, LEOPARD at Layer 3. These are two different papers. **Help me pick one; do not silently merge them.**

### External (Gemini) architectural review — what to take

| Item | Call |
|---|---|
| "Static workload routing via pre-production certification" | **Take.** Names a finding I already have but never labeled. |
| Bounded domain query taxonomy | **Take, but reframe as a hypothesis.** I never measured what share of real inbound queries fall inside certified classes. Assert it as testable, not proven. |
| AEQ certification as CI/CD | **Take, one paragraph.** Extends playbook step 7. Under $5/month at $0.02/cell. |
| Pre-filter for unseen queries | Take as one sentence — a known gap, and the pre-filter itself needs certifying. |
| Zero-persistence / zero-copy over the EDW | **Park.** Untested vendor architecture. Do NOT put it in Section 7 — that section's credibility depends on being about what I *didn't* measure. |
| LangGraph deterministic multi-agent swarm | **Cut.** Contradicts my strongest line ("the architecture is deliberately boring") and I have zero measurements on it. |
| Retry budget on tool params | Park. Good hygiene, unrelated to the thesis. |

Note: the review explicitly "validated" the $0.0009 figure and never mentioned implementation labor. It missed both blockers. Treat it as a brainstorm, not a red team.

### LEOPARD — parked, with one framing fix

Expansion: **LLM Execution and Orchestration Processor, Advanced Routing Design.**

**Problem:** "Advanced Routing Design" points at per-request dynamic routing, which my own routing study says doesn't pay for itself. My paper and my chip name currently contradict each other.

**Fix:** ARD means executing a *pre-certified static* routing policy — decided offline by AEQ Grid — not making dynamic per-request choices. VLIW, not out-of-order execution.

**The stronger claim is determinism, not routing.** A certification is only valid if the runtime reproduces certified behavior. GPU batch nondeterminism (floating-point reduction order varying with batch composition) breaks that. Deterministic silicon makes certification durable in production. That's the missing leg of the stack:

| Layer | Function |
|---|---|
| AEQ Grid | Certifies which model is adequate per query class |
| Certification-time routing | Turns that into a fixed policy — no per-request decision |
| LEOPARD | Executes the policy deterministically so the certificate holds |

**Status: parked until the paper ships. Do not build on it.**

### IP / patent

- Goal is **credibility**, not acquisition. A patent on a chip with no fab path and nobody practicing the claims has near-zero acquisition value; provisionals get discounted hard in diligence.
- **Do not file a non-provisional.** ~$15–25k over 2–4 years, wrong stage.
- A provisional buys "patent pending" for $65 (micro entity) + drafting. Budget $2,500 if drafted properly — a thin provisional is worse than none.
- **AEQ trademark before the chip patent** — but only after the naming collision is resolved.
- **URGENT AND UNSTARTED: disclosure audit.** US gives a 12-month grace period from my own publication; most other countries have absolute novelty and foreign rights die on first disclosure. I publish constantly. Academic priority ≠ patent priority — I may have conflated these.

---

## PART 3 — WHAT NEEDS DOING

### Immediate / blocking

1. **Disclosure audit.** Every public appearance of LEOPARD (Medium, LinkedIn, X, talks, repos) with dates and whether the disclosure was enabling. One page, hand it to a patent attorney.
2. **Re-pin `aeq_experiment.py`.** Currently pinned to `gpt-4o-mini-2024-07-18` with pricing commented "as of 2025." That model is likely retired. **My flagship reproduction script violates my own deprecation-hygiene rule.**
3. **Judge model deprecation.** AEQ runs used `claude-opus-4-8` as judge on 2026-07-24; that generation is superseded. Either justify the pin (version stability across runs is legitimate — say so) or re-run.
4. **Quantization harness scrub.** The fp16-parent-scores-0 / Q4-child-scores-3 inversion is a harness bug until proven otherwise. Check: chat template mismatch (GGUF vs HF card), sampling config drift between runtimes, stop/EOS token handling, and whether the parent and child ran on the same inference stack. I gave the judge an error model; I never gave the runtime one. **If it doesn't survive, the paper has two findings instead of three — that is still a paper.**

### The build sequence agreed

1. **Claim ledger** — numbered list of every assertion the paper will make, mapped to the experiment that produces it, with a status flag (reproducible / needs re-run / unsupported). Lock this BEFORE writing. This is what stops the frame drift.
2. **One harness, one entry point** — `python reproduce.py --all` runs each experiment and emits reports. Re-pinned models, pricing verified same day. Every number in the paper traces to a file that script emitted.
3. **Write the paper against the emitted reports** — not from memory, not from old drafts. No report, no claim.
4. **Demo = live run of the trap.** Do not build a separate demo. The reproduction script IS the demo. The trap plays in a room (a frontier model adding a health-52 asset to a critical list under a threshold of 50, three for three, because a field note sounded urgent). 4.68x is a table and doesn't.
5. **Post last**, pointing at paper + runnable repo, so "contact me for more" leads somewhere real.

### Repo decision — unresolved

`AgentSaaSy_EAM` and `AgentSaasy_NGAI` are both private (404 unauthenticated). Only `claudeskills` and `Introduction` are public under the account.

**The white paper's entire "Where the Evidence Lives" appendix cites paths inside a private repo.** Every citation currently 404s for a reader.

Recommended: carve out a purpose-built **`aeq-reproduce`** public repo — harness, rubrics, reports, no client-adjacent material, no half-finished branches. Easier to make presentable than opening a working repo, and it's exactly what a reader wants: clone, set a key, run one command, watch the trap fire.

---

## PART 4 — DEPENDENCY WARNING

**The Blocker 1 and Blocker 2 correction text was written for the SaaS-framed paper.** If the restructure to the "specs don't predict adequacy" thesis goes ahead:

- Blocker 2 (TCO / break-even) becomes **moot** — there's no seat-price comparison to defend. Do not spend time implementing it.
- Blocker 1 survives in reduced form: use certified numbers, never uncertified ones. That principle applies regardless of frame.
- The vendor pricing table, the UpKeep comparison, and the OpenRouter claim all disappear with the SaaS frame.

**Confirm the frame decision before implementing any Section 6 work.**

---

## PART 5 — OPEN QUESTIONS I NEED ANSWERED

1. **Which unifying frame** — "specs don't predict adequacy" or "Prompt to Silicon"? These are different papers.
2. **Is `experiments/grid2q/` a runnable harness or a set of result files?** This determines whether the reproduction repo is a packaging job or a build.
3. **Actual build hours** for the AgentSaaSy stack (demo vs. what a production build would take). Only needed if the SaaS frame survives.
4. **LEOPARD one-liner is incomplete** — "...secure, deterministic, and high-performance inference across multiple ___". Models? Tenants? Domains? If "tenants," that's an isolation claim that needs its own treatment.
5. **Does the trap harness exist as code**, or were those reports assembled by hand?

---

## PART 6 — ASSETS IN PLAY

| File | Status |
|---|---|
| `AGENTIC_SUBSTITUTION_WhitePaper_v3_DRAFT.pdf` | Under restructure; frame in question |
| `v3_Blocker1_Blocker2_Corrections.md` | Drafted this session; conditional on frame decision |
| `AEQ_Specification_v1_0.md` | **Canonical.** Source of truth for the AEQ term. |
| `TECHNICAL-WHITE-PAPER.md` (v2.1.0) | Canonical architecture reference. Has a minor internal inconsistency: cost/query stated as $0.0009 but the annualized $288 implies $0.0008 and a 360-day year. Clean in v2.1.1. |
| `aeq_experiment.py` | 645 lines, working. Needs model re-pin + price re-verify. |
| `experiments/grid2q/*` | Not yet reviewed — status unknown |
| `claude_AEQ_Verify_Product_Thesis_v0_1.md` | Parked |
| `claude_AEQ_Verify_Viability_Report_Jul2026.md` | Parked |

---

## HOW I WANT TO WORK

- Direct, no-nonsense. Stay in brainstorming mode until I explicitly say to draft.
- Source all claims. Flag anything hypothetical as hypothetical. Do not fabricate.
- Pre-registration before data collection is non-negotiable.
- Run the banned-term grep on every deliverable.
- Address me as "big dog Michael."
