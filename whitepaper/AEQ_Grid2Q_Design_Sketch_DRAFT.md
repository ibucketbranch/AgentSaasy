# AEQ GRID-2Q -- QUANTIZED SUT EXPERIMENT, DESIGN SKETCH

**Status:** DRAFT -- NOT REGISTERED. This is a design sketch for review. It becomes binding only when rewritten as a pre-registration with a timestamp recorded before the run.
**Author:** Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026
**Naming note:** Grid-1's pre-registration reserved "Grid-2" for the tool-selection experiment. This document uses **Grid-2Q** (Q for quantization) so that name stays available.

---

## 1. The Question

Does a quantized open-weight model, running on commodity local hardware, deliver rubric-equivalent answers to (a) its own full-precision parent and (b) a frontier API reference, per query class, and at what measured cost and speed?

Grid-1 v1.1 answered the hosted-tier version of this question: cheap API tiers pass at 100% on the current query classes. That result killed quantization as a savings story (nano already costs ~$0.001/query) but left the deployment-location question open: can a company move a workload class onto its OWN hardware with certified zero rubric loss? That is the question a frontier API cannot answer for them, the decision the market is now forced into by open-weight releases, and the AEQ Verify edge wedge ("this workload class passes the rubric on this hardware at this cost per verified-equivalent answer").

## 2. The Instrument Problem Grid-2Q Must Fix First

Grid-1 v1.1 passed 27/27 cells. A rubric that everything passes has no discrimination: it cannot tell tiers apart, so it also could not detect quantization damage if damage existed. **Grid-2Q is not allowed to run until the rubric can fail somebody.** That is Phase 0.

### Phase 0 -- Rubric hardening and calibration (gate before the experiment)

Add two query classes and tighten the existing three:

**Q4 -- Distractor rejection (new).** Evidence includes assets engineered to look critical without meeting the stated definition (e.g., health 52 with an alarming maintenance note, or a critical-looking asset explicitly marked decommissioned). PASS requires the answer to EXCLUDE the distractors and state the correct filtered set. Required-absence criteria are what quantized models are most likely to fumble: precision loss shows up first as blurred boundary judgments.

**Q5 -- Derived quantitative synthesis (new).** The answer requires computing a number not present in the evidence (e.g., total annual maintenance cost of critical assets as a percent of portfolio maintenance spend, correct to within 1 percentage point; or the cost-weighted average health score of one location). Multi-step arithmetic is a known early casualty of aggressive quantization. Exact tolerance is declared per query in the prereg.

**Tightening Q1-Q3:** Q1 raises the citation floor from 3-of-5 critical IDs to 5-of-5. Q2 requires the top TWO priorities in correct order, not just the top one. Q3 adds a required-absence criterion (no recommendation may reference an asset absent from the evidence).

**Calibration gate (locked before Phase 1):** run the hardened rubric on the Grid-1 frontier reference and on gpt-5-nano, N=3 per class.
- Frontier must pass >= 13 of 15 cells (integrity: rubric is achievable).
- Nano must FAIL at least 2 of 15 cells (discrimination: rubric can separate tiers).
- If nano still passes everything, escalate Q4/Q5 difficulty and recalibrate. If frontier fails broadly, the rubric is defective; fix and recalibrate. Calibration runs are reported, never discarded.

## 3. Design -- 5 x 3 x 3

| Dimension | Levels |
|---|---|
| Query class | Q1 retrieval (tightened), Q2 analytical (tightened), Q3 synthesis (tightened), Q4 distractor rejection, Q5 derived quantitative |
| System under test | T1 frontier API reference (pinned, e.g. gpt-5.2), T2 open-weight parent at full precision, T3 the SAME open-weight model quantized (e.g. 4-bit) |
| Runs per cell | N = 3, temperature 0 |

45 cells total. The load-bearing comparison is **T3 vs T2**: same weights, different precision, so any pass-rate gap is attributable to quantization and nothing else. T1 remains the external reference and integrity check. Do NOT compare a quantized model X against an API model Y and call the gap "quantization damage"; that confounds model identity with precision.

**Candidate SUT model:** an open-weight model with a credible full-precision hosted endpoint AND a local quantized build (llama.cpp / Ollama / MLX on Apple Silicon). Pin the exact checkpoint hash and quantization method (e.g., Q4_K_M GGUF) at registration. If the Kimi K3 weights land on Hugging Face as the podcast discussion anticipated, it is the topical choice; otherwise any current open-weight model of mid size qualifies. The design is model-agnostic; the prereg pins the instance.

**Hardware anchor:** the local machine is part of the certified claim. Record chip, RAM, OS, runtime (e.g., "Apple M-series, 64 GB, macOS 26, llama.cpp b####"). The certification artifact is "workload class W passes on model M at quantization Q on hardware H."

**Replay semantics:** identical to Grid-1. All tiers receive the same deterministic tool outputs injected as evidence. Declared limitation carries forward: this does not test tool selection; that remains Grid-2 (tool routing), unbuilt.

**Adjudication:** cross-family judge, claude-opus-4-8 (the v1.1 lesson: the haiku judge produced arithmetically false rejections; do not regress). Structured JSON verdicts, parse failures re-adjudicated once, never dropped. Judge COGS reported separately, as in Grid-1.

## 4. Stated Prior (declare before running)

To be declared by the author at registration. Suggested shape, informed by published quantization evaluations: "T3 (4-bit) passes >= 85% of the cells T2 passes, with losses concentrated in Q4/Q5; T2 aggregate vs the frontier reference >= 70%." Declare it, then let the grid score it.

## 5. Go / No-Go Gates (to be locked at registration)

| Gate | Condition | Meaning |
|---|---|---|
| GREEN | T3 cell passes >= 90% of T2 cell passes AND T2+T3 aggregate vs rubric >= 70% AND Q4+Q5 combined >= 50% | "Quantization-lossless for this workload class" is certifiable. The edge/on-prem certification pitch stands with measured evidence. |
| YELLOW | T3 holds on Q1-Q3 but drops Q4 or Q5 below 50% | Certification is per query class: route easy classes local, keep hard classes on the wire. Still a product, narrower claim. |
| RED | T3 loses > 25% of T2's passes, or losses spread across all classes | Quantization damage is real at this size/method; the certifier story survives (AEQ correctly detected it) but the local-deployment pitch does not, at this configuration. |

Note the asymmetry worth writing down now: **RED is still a useful result.** An instrument that catches quantization damage is exactly what a certifier sells. Only Phase-0 failure (a rubric that cannot discriminate) is a dead end.

## 6. Measurement Rules (inherited from AEQ Spec v1.0 and Grid-1, plus local-inference additions)

1. Pin everything: checkpoint hashes, quantization method, runtime version, judge model, temperature 0, pricing at run date, verified against official pages before publication.
2. API tokens measured from usage fields; local tokens from the runtime's own counters; all numbers labeled measured vs estimated.
3. Local cost has no per-token price. Report: (a) measured wall-clock latency per query, (b) measured tokens/sec, (c) an estimated $/query from amortized hardware + measured watts if captured (macOS powermetrics), clearly labeled ESTIMATED. Latency is a first-class result, not a footnote: it is the number that does not deflate.
4. N=3 per cell, failed runs logged, full answer text captured for audit.
5. Results published regardless of outcome, including a failed Phase 0.

## 7. Execution Sketch

Phase 0 (calibration): extend the Grid-1 script's query/rubric tables with Q4/Q5 and the tightened criteria; run frontier + nano only; evaluate the calibration gate. Estimated cost: a few dollars of API + judge.
Phase 1 (the grid): stand up the local quantized model and the full-precision endpoint for the same weights; run the 45-cell grid; judge; report. Wall time dominated by local inference; API cost still small; judge cost scales from v1.1's ~$0.15 to roughly $0.25-0.50.
All parameters (model ids, endpoints, hardware string, quantization tag, tolerances) enter via config/flags, not constants baked into the script.

## 8. What Gets Reported

Per-cell pass/fail, tokens, cost or cost-estimate, latency, full answers. Aggregates: pass matrix (class x tier), the T3/T2 retention ratio per class (the headline number), latency and tokens/sec per tier, judge COGS per verified query, gate verdict against section 5, and the measured result scored against the section 4 prior. Plus the prototype certification artifact: one page stating workload class, model, quantization, hardware, retention ratio, and cost, in the form AEQ Verify would hand a customer.

---
*Terminology compliance: this document uses "AI agent(s)" exclusively.*
