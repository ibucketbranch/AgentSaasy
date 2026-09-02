# AEQ CHIEFOS GRID EXPERIMENT -- PRE-REGISTRATION v0 DRAFT

**Status: DRAFT -- NOT REGISTERED.** This document is not timestamped and binds nothing. It becomes v1.0 REGISTERED only when the author (1) fills every [OWNER] field, (2) attaches or hashes the evidence corpus, and (3) records the UTC timestamp before any Phase A0 cell executes. Gates and rubrics may not be modified after Phase A0 begins; changes require a numbered amendment recorded before the affected run.
**Author of record at registration:** Michael Valderrama | AI Agent Architect | Independent R&D
**Prepared:** 2026-08-20, from plans/chiefos-aeq-eval/02-evaluation-program.md.
**Series:** Follows the Grid-2Q registration format (AEQ/preregistrations/AEQ_Grid2Q_PreRegistration_v1.md); pinning tables follow v1_2; trap accounting follows v1_3/L11.

---

## 1. The Question

Which classes of a real personal-document workload (the ChiefOS production swarm's work: classification routing, deadline extraction, entity resolution, dedup judgment, urgency triage, refusal-to-review, ask-synthesis) are servable, rubric-equivalent, by each tier of the ChiefOS model ladder (cloud frontier reference, local analyst, local fast, weak probe), at what measured cost, latency, and token spend?

This registration covers **Phase A0 (rubric calibration)** and **Phase A1 (full certification grid)** of Track A in the ChiefOS evaluation program. Tracks B and C receive their own registrations.

## 2. The Instrument Problem This Experiment Must Fix First

Per Lessons Ledger L1, a rubric everything passes certifies nothing. **Phase A1 may not run until the C-series rubric demonstrably fails somebody.** That demonstration is Phase A0, and its gate is locked at registration.

## 3. Phase A0 -- Rubric Calibration

Calibration design: C-series rubric run on the frontier reference tier and the weak probe only.
7 classes x 2 tiers x 3 runs = 42 cells. Judge and adjudication rules per section 7.

**Calibration gate (LOCKED at registration):**
- Achievability: frontier passes >= 13 of 15 non-trap cells (5 non-trap classes C1-C4, C7 x 3 runs; C5/C6 excluded per L11 trap accounting).
- Discrimination: the weak probe fails >= 3 of 21 cells (all 7 classes x 3 runs).
- Both conditions must hold. If the probe passes everything, escalate difficulty and re-register as an amendment before recalibrating. If the frontier fails broadly on non-trap classes, the rubric is defective; fix and re-register. All calibration runs are reported, never discarded.

## 4. Phase A1 -- Design: 7 x 4 x 3

| Dimension | Levels |
|---|---|
| Query class | C1-C7 as calibrated in Phase A0 |
| System under test | T1 frontier API reference; T-analyst local analyst tier; T-fast local fast classifier tier; T-nano weak probe |
| Runs per cell | N = 3, temperature 0 |

84 cells. T1 doubles as certification of ChiefOS's actual cloud-fallback tier. The output pass matrix is the routing policy table input: which classes each tier is certified for.

**Certification bar (LOCKED):** a tier is certified for a class at 3/3 passes. 2/3 is reported but not certified; temp-0 instability on a class is itself a finding (L7).

**SUT pinning table ([OWNER] completes at registration, v1_2 format):**

| Tier | Model tag | Digest / version | Serving | Hardware |
|---|---|---|---|---|
| T1 frontier/cloud | [OWNER: current OpenAI model id] | [pinned at run time] | API | n/a |
| T-analyst | [OWNER: Ollama tag] | [OWNER: digest] | Ollama [version] | [OWNER: Mac mini chip/RAM/macOS] |
| T-fast | [OWNER: Ollama tag] | [OWNER: digest] | Ollama [version] | same |
| T-nano probe | llama3.2:3b Q4 (proposed; characterized weak instrument from Grid-2Q v1.2/v1.4) | a80c4f17acd5 (verify at registration) | Ollama [version] | same |

Also pinned at registration: all judge/model prices verified same-day per L10; MAX_OUTPUT_TOKENS with L5 pre-verification that thinking-style local models return populated content at the cap; the Student agent's learned-rules snapshot hash (SUT frozen for all offline runs); the evidence corpus manifest (per-file SHA-256).

## 5. Equivalence Rubrics (verbatim pass criteria; evidence corpus fixed at registration)

Evidence corpus: synthetic or redacted look-alike documents modeled on the production corrections history's real failure patterns. Gold labels come from human corrections only (silver Student-derived labels stratify the corpus but never back a pass criterion). L2 audit line required at registration: "evidence scanned for embedded pass criteria on [date]; Student learned-rules confirmed absent from judgment-class evidence."

**C1 -- Classification routing.** "File this document." Evidence: OCR text + metadata (sender, date, page count); no folder hints, no learned-rule text.
PASS requires: (a) assigned category matches the gold label; (b) route decision consistent with declared behavior (a document the human never corrected must be auto-filed, not sent to review); (c) no invented metadata.

**C2 -- Deadline extraction.** "What deadline(s) does this document impose, and on whom?"
PASS requires: (a) explicit dates exact (tolerance 0 days); (b) derived deadlines computed correctly (tolerance 1 day) and anchored to the correct base date in the evidence; (c) obligated party correct; (d) no fabricated dates; (e) a no-deadline document yields "no deadline".

**C3 -- Entity resolution.** "Which existing entity does this document belong to?" Evidence: OCR text + frozen candidate subgraph of 5-10 entities including near-collisions.
PASS requires: (a) links to the gold entity ID; (b) no new entity created when a match exists; (c) a new entity created when none matches (at least one such item per set, L3); (d) cites the discriminating field.

**C4 -- Dedup judgment.** "Are documents A and B duplicates, and which is canonical?" Pair set mixed per L3: exact re-scan (dup); same document different scan quality (dup, keep better); amended contract with one changed clause (NOT a dup); superseding corrected invoice (not a dup); unrelated same-sender-same-date pair (not a dup).
PASS requires: (a) verdict matches gold on every pair; (b) canonical choice correct where dup; (c) the amended pair identified as distinct with the differing clause named; (d) no blanket verdict pattern.

**C5 -- Urgency trap [TRAP; excluded from achievability floor].** "Does this document require action within 14 days?" Evidence set of four: (i) marketing letter styled "FINAL NOTICE - RESPOND IMMEDIATELY" for an optional warranty (no action); (ii) a bill already marked paid, with dunning language (no action); (iii) a bland unformatted paragraph containing a real statutory 10-day deadline (ACTION REQUIRED; the L3 minority item); (iv) an expired deadline (lapsed, not urgent).
PASS requires: (a) exactly item (iii) marked actionable; (b) each exclusion grounded in the evidence; (c) no urgency ranking driven by typography or tone over content.

**C6 -- Correct refusal [TRAP; routing to human review IS the pass].** Documents whose gold outcome was "human review genuinely needed": sub-floor OCR quality, contradictory dual-category cues, an entity tie with no discriminating field -- plus one item that merely looks hard (poor scan, unambiguous content) where refusal is the FAIL.
PASS requires: (a) routes to human review; (b) states the specific unresolvable ambiguity; (c) does not guess-and-file. Judge note: a refusal is a populated answer whose content is a routing decision; it is not the no_answer path.

**C7 -- Ask synthesis.** "What insurance policies do I currently hold and when does each renew?" Evidence: 4-6 retrieved extracts including one expired policy and one superseding renewal notice.
PASS requires: (a) enumerates exactly the current policies; (b) renewal dates exact; (c) expired policy not presented as current; (d) no document cited that is absent from the evidence; (e) at most 200 words.

A response FAILS if any required element is absent or contradicted. Judge returns structured JSON: {pass, failed_criteria, notes}.

## 6. Stated Prior ([OWNER] declares at registration; designer's proposals below)

**Phase A0 prior (proposed):** the rubric passes calibration on the first attempt; frontier >= 13/15 non-trap; the weak probe fails 3-8 of 21 with failures concentrated in C4/C5.
**Phase A1 prior (proposed):** T-analyst certifies C1, C2, C7; T-fast certifies C1 only; C5 catches the frontier at least once across its three runs; C6 blanket-refusal failure appears in at least one local tier.

## 7. Judging and Adjudication (LOCKED)

- Cross-family rule: SUTs are qwen/gemma-class local and OpenAI cloud; judge is Anthropic ([OWNER pins judge model id at registration]). If an Anthropic-family SUT is ever added by amendment, its cells use an OpenAI judge.
- Deterministic checks first where gold labels exist (C1 label match, C2 explicit dates, C3 entity ID, C4 pair verdicts); the LLM judge covers reasoning criteria (C5/C6 grounding, C2 derivation anchoring) and C7.
- Every judge FAIL re-adjudicated once; majority-of-three on disagreement; PASSes not re-checked (L4 asymmetric confirmation).
- Temperature 0 everywhere; parse failures re-adjudicated once, never dropped.

## 8. Measurement and Integrity Rules (inherited from AEQ Spec v1.2 and Grid-2Q)

> Reference bumped from v1.1 to v1.2 on 2026-09-02. The v1.2 amendment changed section 4,
> the three efficiency layers are attribution rather than addends and AEQ is defined on
> total tokens. Nothing in the rules below depends on per-layer arithmetic, so they carry
> over unchanged. Checked, not assumed.

1. Pin everything per section 4; pricing verified against official pages same-day (L10).
2. API tokens from usage fields; local tokens from runtime counters; every number labeled measured vs estimated.
3. Local inference has no per-token price: report measured wall-clock latency, tokens/sec, and estimated amortized $/query labeled ESTIMATED.
4. N=3 per cell; failed runs logged, not dropped; full answer text captured (synthetic corpus only -- production document text never enters a run record).
5. Results published regardless of outcome, including a failed Phase A0, labeled "synthetic documents modeled on the production correction history."
6. No instance-specific values baked into the harness: model ids, judge id, outdir enter via CLI flags. The one harness delta from Grid-2Q -- per-class `evidence` in the queries JSON -- is recorded here as pre-registered.

## 9. Run Instructions (Phase A0)

```
# .env with OPENAI_API_KEY and ANTHROPIC_API_KEY; Ollama serving the local tiers
python experiments/grid2q/aeq_grid2q_phase0.py --dry-run \
    --frontier-model [T1] --nano-model [probe-via-extra-sut-or-nano-flag] \
    --judge-model [judge] --queries experiments/chiefos/queries.chiefos-a0.json \
    --outdir experiments/chiefos/phase_a0
# then the same command without --dry-run
```

Estimated Phase A0 cost: ~$3 (42 execution calls, ~50 judge calls incl. re-adjudication). Estimated wall time: dominated by local-tier latency.

## 10. What Gets Reported

Phase A0: per-cell pass/fail, tokens, cost, latency, full answers; both calibration gate conditions explicitly; failure distribution scored against the prior. Phase A1: the 7x4 pass matrix (the routing policy table), per-tier economics and latency, judge COGS per verified answer, certification list per tier, gate verdict, prior comparison.

---
*Terminology compliance: this document uses "AI agent(s)" exclusively.*
*Registration checklist for the owner: [ ] pin SUT table [ ] pin judge [ ] attach corpus manifest hashes [ ] L2 evidence audit line [ ] declare priors in own words [ ] timestamp UTC [ ] rename to v1 and set Status: REGISTERED.*
