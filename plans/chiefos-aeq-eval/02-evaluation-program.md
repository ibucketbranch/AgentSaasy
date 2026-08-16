# ChiefOS Evaluation Program - Applying AEQ / AEQ Grid / AEQ-L to a Live Multi-Agent Swarm

**Written 2026-08-16. Status: DESIGN, pre-registration draft basis. Nothing below is registered until timestamped per Grid-2Q practice.**

## 0. Framing decisions

1. **The unit of certification is one document-task, not one orchestrator cycle.** ChiefOS's hourly loop looks autonomous, but each dispatched job (classify this doc, extract this deadline, judge this dup pair) is a bounded, single-turn-shaped task. This keeps most of the program inside validated single-turn AEQ Grid machinery. What it does not rescue is measured honestly in Track C (coordination overhead) and Track B (AEQ-L), both labeled with the spec section 9 status warning.
2. **Three names, three jobs (spec 2.1) carries over verbatim.** Track A is AEQ Grid (certification of model-workload pairs). Track B is AEQ-L [PROPOSED] instrument readings. Track C is the section 11.5 designated instrument (Architecture Note section 7). No sentence in any report may need one name to mean two of these.
3. **The Student agent makes the SUT non-stationary.** Every offline run and the Track C experiment run with Student learning frozen (learned-rules table snapshotted; snapshot hash pinned). Live Track B records Student update events as covariates and resets class baselines after each learning event. This is the multi-agent analog of Lessons L7/L10: a certificate is a property of a pinned system; an unpinned learner rots the certificate from inside.
4. **Privacy is a pre-registered protocol, not an afterthought.** The offline corpus (Tracks A and C) is built from synthetic or redacted look-alike documents modeled on the corrections history's real failure patterns - publishable, shippable to a cloud judge. The live track (B) keeps document content local: scored overwhelmingly by deterministic checks; the small LLM-judged sample passes through a pinned redaction step before reaching the cloud judge.

## 1. Workload query classes (the C-series, analog of Q1-Q5)

Ground truth: the human review queue plus the corrections history. Every human correction is a labeled example (gold); every Student learning event is silver (derived from gold but mediated by the Student's generalization) - only gold backs rubric construction and published rates; silver is used for corpus stratification. Ledger rules applied throughout: L2 (evidence must not quote the pass rule - the Student's learned filing rules must NOT appear in the evidence for judgment-testing classes), L3 (every trap set mixed, no blanket strategy passes), L9 (at least one just-above-threshold item dressed in urgent language).

Seven classes. C5 and C6 are trap classes, excluded from the achievability floor per L11/v1.3 accounting.

**C1 - Classification routing.** "File this document." Evidence: OCR text + metadata (sender, date, page count), no folder hints, no learned-rule text.
PASS: (a) assigned category matches the gold label; (b) route decision consistent with the declared behavior (a doc the human never corrected must be auto-filed, not sent to review); (c) no invented metadata. Deterministically checkable against gold labels for (a).

**C2 - Deadline extraction with tolerance.** "What deadline(s) does this document impose, and on whom?"
PASS: (a) explicit dates exact-match (tolerance 0 days); (b) derived deadlines ("30 days from the date of this letter") computed correctly, tolerance 1 day, anchored to the correct base date; (c) obligated party correct; (d) no fabricated dates; (e) a document with no deadline yields "no deadline" (the arithmetic mirror of L8: binding the right evidence values to the right roles is the discriminator).

**C3 - Entity resolution.** "Which existing entity does this document belong to?" Evidence: OCR text + a frozen candidate entity subgraph (5-10 candidates including near-collisions: same surname different person, same account number different institution).
PASS: (a) links to the gold entity ID; (b) does not create a new entity when a match exists; (c) does create one when none matches (at least one such item per set, per L3); (d) cites the discriminating field - internal consistency alone proves nothing (L8).

**C4 - Dedup judgment.** "Are documents A and B duplicates, and which is canonical?" Set construction per L3, mixed by design: exact re-scan (dup), same doc different scan quality (dup, keep better scan), amended contract with one changed clause (NOT a dup - the near-miss that punishes blanket "duplicate" answers), corrected invoice superseding the original (not a dup; supersedes relation), unrelated docs from same sender/date (not a dup).
PASS: (a) verdict matches gold on every pair; (b) canonical choice correct where dup; (c) the amended-document pair explicitly identified as distinct with the differing clause named; (d) no blanket verdict pattern.

**C5 - Urgency trap [TRAP CLASS].** The health-52 analog. "Does this document require action within 14 days?" Evidence set of four: (i) marketing letter styled as "FINAL NOTICE - RESPOND IMMEDIATELY" for an optional warranty (no action); (ii) a bill already marked paid, with threatening dunning language (no action); (iii) a bland, unformatted paragraph containing a real statutory 10-day deadline (ACTION REQUIRED - the L3 minority item); (iv) an expired deadline (flag as lapsed, not urgent).
PASS: (a) exactly item (iii) marked actionable; (b) each exclusion grounded in the evidence; (c) no urgency ranking driven by typography or tone over content. Excluded from the achievability floor per L11; frontier performance on C5 reported as a standalone finding.

**C6 - Correct refusal [TRAP CLASS; routing to human review IS the pass].** Evidence: documents where the gold outcome was "human review genuinely needed": illegible OCR below a stated quality floor, a document matching two categories with contradictory cues, an entity-resolution tie with no discriminating field.
PASS: (a) routes to human review; (b) states the specific unresolvable ambiguity (not a generic hedge); (c) does not guess-and-file. Per L3 the set includes one item that merely looks hard (poor scan, unambiguous content) where refusal is the FAIL - blanket refusal cannot pass. This class operationalizes the AEQ-L numerator decision (a correct halt counts as value) inside the single-turn grid.
Harness note: the judge auto-fails empty answers (no_answer path). A refusal is a populated answer whose content is a routing decision - no harness conflict, but the rubric text must say so explicitly.

**C7 - Ask synthesis.** The Q3 analog for the Ask feature. "What insurance policies do I currently hold and when does each renew?" Evidence: 4-6 retrieved extracts including one expired policy (must be excluded or marked expired) and one renewal notice superseding an older doc.
PASS: (a) enumerates exactly the current policies; (b) renewal dates exact; (c) expired policy not presented as current; (d) no document cited that is absent from the evidence; (e) at most 200 words.

## 2. The three evaluation tracks

### Track A - Offline AEQ Grid certification of ChiefOS's model tiers

Direct reuse of the grid2q harness pattern. 7 classes x 4 tiers x 3 runs = 84 cells, temperature 0, N=3 per L7.

Tiers: **T1** frontier API reference (current OpenAI model, pinned + priced same-day per L10; it is also the cloud-fallback tier ChiefOS actually calls, so this row doubles as certification of the fallback); **T-fast** the fast local classifier (Ollama, digest-pinned per v1.2 practice); **T-analyst** the local analyst (digest-pinned); **T-nano** a designated weak discrimination probe (recommend llama3.2:3b Q4, digest a80c4f17acd5, already characterized as weak in the v1.2/v1.4 runs - reuse of a characterized instrument).

Unchanged from the existing harness: call machinery, retry discipline (L6), fail-confirmation adjudication (L4), cap-artifact logging (L5 - pre-verify the local models return populated content at MAX_OUTPUT_TOKENS per v1.4 s2 practice; thinking-style local models are the known risk), report format, --extra-sut local endpoints, cross-family judging.

**Required harness change (the one code delta):** EVIDENCE is currently a single module-level constant baked into the user message and JUDGE_PROMPT_TEMPLATE (aeq_grid2q_phase0.py lines 101-137, 310-334). ChiefOS classes need per-class evidence. The queries JSON schema gains an `evidence` field per class; build_user_message and call_judge read it from the class record. Small, pre-registerable delta.

Output: the pass matrix per (tier x class) IS the routing policy table input (Architecture Note s2): which classes the fast tier is certified for, which need the analyst, which go to cloud, which always route to review.

Gate (locked at registration): a tier is certified for a class at 3/3 passes; 2/3 is reported but not certified (temp-0 instability on a class is itself a finding per L7).

### Track B - Live/continuous AEQ-L from telemetry [PROPOSED metric; this track IS its validation experiment]

Everything here carries the spec section 9 status warning. Track B is the "at least one instrumented loop experiment" that section 11.3 requires for graduation.

Outcome taxonomy (per document lifecycle, locked before the window opens):

| Code | Outcome | Numerator? |
|---|---|---|
| S1 | Auto-processed (filed/extracted/deduped), no human correction within window W | Yes |
| S2 | Correct refusal: routed to review; human's resolution differed from the system's top candidate, or human confirmed genuine ambiguity | Yes (correct halt = value) |
| F1 | Silent failure: auto-processed, corrected by human within W | No |
| F2 | Incorrect halt: routed to review; human accepted the system's top-1 suggestion unchanged (refusal wasted human time) | No |
| F3 | Mechanical failure: retry-exhausted, crash, cap artifact (logged separately per L5) | No |

The S2/F2 adjudication rule ("did the human's action match top-1?") is deterministic from the review-queue log - no judge needed. This resolves the halt-correctness open question of section 9 for this workload by construction, exactly the kind of result that feeds AEQ-L validation.

Denominator: cumulative tokens for the document's full lifecycle across all 8 agents - including retries, Dedup Hunter rework, Auditor re-checks, and the amortized Orchestrator share (per-dispatch tokens attributed to the doc IDs in that dispatch; fixed cycle overhead split evenly across the cycle's docs, method disclosed). Known undercount, disclosed: the Apple Vision OCR step consumes zero tokens; reported as a zero-token step with wall-clock alongside, per spec 10.3.

Correction-latency window W: measured first, not guessed. Phase B0 computes the empirical time-from-filing-to-correction distribution from existing history; W is pinned at the 95th percentile. Outcomes are provisional until W elapses, then final. No number computed on provisional outcomes is publishable.

Gate mapping (weekly, per class, minimum cell n >= 30 finalized documents - below that the class reports "insufficient n," never a rate):

- GREEN: class pass rate (S1+S2) within 5 points of the Track A certified rate for the serving tier, AND F1 rate <= locked threshold (propose 2% for C1/C4; zero tolerated F1 for C2 deadlines - a silently wrong deadline is the maximum-damage failure).
- YELLOW: pass rate holds but AEQ-L drops more than 20% vs the class's trailing 4-week baseline (waste regression: retries, refusal churn, token bloat), or refusal rate drifts more than 2x baseline. Action: investigate; candidate re-cert.
- RED: F1 above threshold or pass rate below the certified floor. Action: the class's routing row falls back one tier (fast -> analyst -> cloud -> always-review) until re-certification - the same semantics as the Grid-2Q RED gate ("the instrument caught it" is a healthy outcome).

This mirrors spec section 7 (per-agent baselines, regression as early warning) and section 9.5's gate A/B testing: the budget-gated cloud fallback and the rule-based degradation ladder are forks (9.6), and turning each on/off in controlled windows against AEQ-L is the fork-gated-validation experiment.

### Track C - The section 11.5 coordination-overhead experiment (Architecture Note section 7, realized)

Three arms, as pre-registered in the Note, instantiated for ChiefOS:

- **Arm A:** one frontier API agent (the pinned T1 model) with all ChiefOS tools, processing the batch end-to-end, single agent, no orchestrator.
- **Arm B:** one certified cheap agent - the local analyst-tier model with all tools (only classes it certified for in Track A; a Track A RED class stays in the batch and its failures count - the arm may not shed hard work).
- **Arm C:** the production swarm: Orchestrator + the 7 workers, production prompts, production handoffs, pinned configuration.

Batch: one frozen set of 100 synthetic/redacted documents, stratified across C1-C7 in the live class mix proportions (measured from telemetry in Phase B0), including trap and refusal-warranted items. Manifest with per-file SHA-256 pinned at registration.

Measured per arm: rubric pass count (same C-series rubrics, same judge, same fail re-adjudication - the equivalence rubric the Note requires), cumulative tokens, wall clock. For Arm C additionally the attribution decomposition, the section 11.5 payload:

```
orchestration_tax = (orchestrator tokens_in+out
                     + inter-agent handoff payload tokens
                     + duplicated-context re-stuffing tokens)
                    / total arm tokens
```

plus a per-agent table (tokens, passes attributable, retries) - spec section 7 "track per agent" applied to attribution for the first time.

Pinned before the run: batch manifest + hashes; all 8 agent system prompts (checksummed); Ollama digests + ollama version + hardware line (v1.2 table format); cloud model ID + same-day price verification (L10); Orchestrator in single-batch mode (not hourly wall-clock dispatch - timing jitter is not the phenomenon under test); retry caps identical across arms; cloud-fallback budget gate at a fixed registered policy per arm (recommend OFF for B and C's local claim; an ON variant may be registered, not improvised); Student frozen (snapshot hash); judge model; the win/loss gates; the prior.

Gates and prior (declared before running; to be confirmed by the operator at registration - these are the designer's proposals):

- GREEN: Arm C pass count >= Arm A pass count - 5 (of 100) AND Arm C total tokens <= 50% of Arm A's. The swarm thesis graduates.
- YELLOW: Arm C matches Arm B's passes but orchestration tax > 35% - narrow agents work, coordination is the waste; the finding is the tax number.
- RED: Arm C loses more than 10 passes to Arm B (same models, coordination subtracts accuracy) - publishable break-even result.
- Proposed prior: Arm C within 5 passes of Arm A at 25-40% of Arm A's tokens; orchestration tax lands 15-30%; Arm B beats Arm C on tokens but loses 5+ passes on C4/C5 (specialist framing helps on judgment classes).

Where single-turn genuinely breaks here: Arm A's frontier agent will chain tool calls per document (multi-step trajectories), so answer-equivalence gives way to outcome-equivalence - which is precisely the AEQ-L numerator generalization. Track C therefore reports under AEQ-L accounting with the section 9 caveat attached. Not a flaw; section 11.5 names this experiment as the instrument because it forces the question.

## 3. Judging design

**Family assignment.** SUTs are qwen/gemma-class local models plus an OpenAI cloud tier, so the judge is Anthropic (claude-opus-4-8), per the cross-family independence rule (spec 10.1) and existing harness convention. Do not economize by moving high-volume judging to a smaller same-vendor tier: L4 records the false-rejection history, and false FAILs corrupt discrimination. If an Anthropic-family SUT is ever added, those cells use the harness's existing OpenAI-judge path so no family self-grades.

**Deterministic first (spec 10.2: model-independent measurements carry the evidentiary weight).** No LLM judge is spent where ground truth is free: C1 filing correctness (gold label match, time-lagged via W); C2 explicit dates (exact match); C4 dedup verdicts (gold pair labels; hash-equality pairs free); C3 entity link (gold ID match); S2-vs-F2 halt adjudication (top-1-match rule); all token counts, retries, latency, gate decisions.

The LLM judge is reserved for: C7 Ask synthesis, the reasoning criteria of C5/C6 (grounded exclusions, stated ambiguity), C2 derived-deadline anchoring, and audit sampling.

**Sampling protocol (live track):**

1. 100% of the interesting events: every refusal (S2/F2 candidates get the deterministic rule; the judge additionally scores the stated reasoning on a sample), every human correction (F1s are the material to mine for new trap items), every F3.
2. 5% uniform random sample of S1 successes per class per week, judge-audited against the class rubric - the false-PASS detector (a deterministic label match can pass an answer that also fabricated a date in prose).
3. Fail re-adjudication carried verbatim from v1.1/L4: every judge FAIL re-judged once, majority-of-three on disagreement; PASSes not re-checked.

**Cost.** Judge call ~3,000 in / 150 out tokens (ChiefOS documents run longer than the EAM evidence block) at opus-4-8 verified pricing, about $0.019 per verdict. Track A full grid: ~100 verdicts, ~$2/certification run. Track B weekly at ~500 docs/week: ~70-80 verdicts, ~$1.50/week. Track C: ~150 verdicts, ~$3/run. Whole-program judge COGS under $10/month. Cost is not a constraint; discipline is.

**Redaction constraint (live track only):** the judged sample passes through a pinned redaction step (names/account numbers to stable pseudonyms) before leaving the machine. The map is deterministic so rubric criteria still bind ("cites the discriminating field" remains checkable on pseudonyms). Registered as part of the judge protocol.

## 4. Pre-registration plan

One registration document per track, Grid-2Q series format, each timestamped before its first cell. Locked before any data collection:

1. Rubrics verbatim for C1-C7, including the evidence documents (or hashes for corpus files) - with an explicit L2 audit line: "evidence scanned for embedded pass criteria on [date]; Student learned-rules confirmed absent from judgment-class evidence."
2. Gates: Track A certification bar (3/3), Track B GREEN/YELLOW/RED thresholds and minimum n, Track C arm gates - all numeric, all locked.
3. Calibration gate analog (Phase 0 for the new rubric - it must fail someone weak before certifying anyone, L1): achievability = frontier passes >= 13 of 15 non-trap cells (5 non-trap classes x 3 runs; C5/C6 excluded per L11); discrimination = the weak probe fails >= 3 of 21 cells (all 7 classes x 3), with the declared prior that failures concentrate in C4/C5. Both must hold; a non-discriminating rubric forces an escalation amendment, never silent tuning; all calibration runs reported.
4. Model pins: Ollama tags + digests + ollama version + hardware line per the v1.2 table; cloud model ID with same-day price verification per L10; judge ID; temperature 0; MAX_OUTPUT_TOKENS with the L5 pre-verification note for thinking-tier locals.
5. Sampling rates and windows: the 100%/5% protocol, window W (pinned from the B0 measurement, percentile cited), the 4-week Track B observation window, Student-freeze snapshot hashes.
6. N: Track A/Phase 0 N=3 per cell (L7 cited). Track C: one batch of 100 docs per arm (the batch is the replication unit; per-doc temp-0 determinism carries L7's stability argument), with a declared option for one replication batch as an amendment. Track B: minimum 30 finalized docs per class per reported rate; the window extends rather than the bar dropping.
7. Declared priors for all three tracks - results scored against the prediction, not fitted to it.
8. Amendment discipline: changes numbered and recorded before the affected run; the Lessons Ledger receives an entry for every self-caught defect, same append-only format.

## 5. What can honestly be claimed, and when

Publishable as MEASURED (house rule: published claims use real API results only):

- Track A pass matrices, per-cell tokens (usage fields / runtime counters), latencies, judge COGS, calibration outcomes - including a failed Phase 0 (published regardless).
- Track C arm totals, pass counts, orchestration-tax decomposition, wall clock. The first real number against spec 11.5; the headline.
- Track B event counts and rates on finalized outcomes (S1/S2/F1/F2/F3 per class after window W).
- Frontier trap performance on C5 as a standalone finding (L11 accounting).

Reported only as ESTIMATED / caveated:

- Any $/query for local inference (no per-token price; amortization labeled, per Grid-2Q rule; latency and tokens/sec are the measured numbers).
- Every AEQ-L value, labeled "AEQ-L [PROPOSED, per AEQ Spec v1.1 s9]" - instrument readings from the metric's own validation deployment, never established findings. The correct publishable claim is one level up: the outcome taxonomy and halt-adjudication rule were operationalized and held up / broke in these ways - that is section 11.3 graduation evidence.
- Provisional (pre-window-W) outcome rates: internal dashboard only.
- Anything computed on the synthetic/redacted corpus carries "synthetic documents modeled on the production correction history."
- Coverage ratio (Note s4) stays [HYPOTHESIS] until the escape-hatch/refusal log has a full window behind it.
- Silver (Student-derived) labels never back a published rate; gold only.

Never claimable: cross-domain absolute AEQ scores (11.1 stands); "the swarm is efficient" as a general claim - only "for this workload, this batch, this configuration, the measured tax was X%."

## 6. Phasing - cheapest first real number, then the sequence

**Phase B0 (free, first): correction-latency and class-mix measurement.** Pure PostgreSQL queries over existing history: time-to-correction distribution (pins W), class frequency mix (pins Track C stratification), correction-rate baseline per class. No API spend, no new code beyond SQL. Pins two registration parameters with measured values instead of guesses.

**Phase A0 (~$3, days): ChiefOS Grid Phase 0 - rubric calibration.** Build the C1-C7 corpus (synthetic/redacted, seeded from real F1 failure patterns), register, run frontier + weak probe through the minimally modified grid2q harness. First real publishable number: a calibrated, discriminating rubric for a personal-document workload, with the frontier's C5 trap performance as the hook finding. If calibration fails, that is published too, cheaply learned.

**Phase A1 (~$3-5): full certification grid** - 7 x 4 x 3, emits the pass matrix and routing policy table. Headline: which classes of a real personal-document workload certify onto $0-marginal local models - the AEQ Verify wedge on his own production system, all measured.

**Phase C (~$5-15 cloud spend, one weekend): the coordination-overhead experiment.** Requires Track A's certificates (Arm B must be "certified cheap") and B0's class mix. The section 11.5 designated instrument, executed. Either the swarm thesis graduates or the break-even is the finding; both publishable under the Note's own framing.

**Phase B1 (4-week registered window): live AEQ-L instrumentation.** Telemetry hooks, deterministic scorer, weekly judge sampling, GREEN/YELLOW/RED dashboard. At window close: finalized outcome rates (measured) + AEQ-L readings (proposed-metric label) + the S2/F2 adjudication-rule verdict = the section 11.3 graduation evidence for spec v1.2.

**Phase B2 (ongoing): fork-gated A/B.** One fork at a time, registered per experiment: cloud-fallback budget gate on/off, degradation ladder thresholds, review-queue confidence threshold - each judged by whether AEQ-L rises (section 9.6 rule 2 made empirical). The steady-state program.

## Where the single-turn limitation genuinely breaks (consolidated)

1. Arm A trajectories in Track C - multi-step per doc; scored under outcome-equivalence (AEQ-L accounting), disclosed.
2. Student learning - non-stationary SUT; frozen for A/C, covariate-and-rebaseline for B.
3. Apple Vision OCR - zero-token work; denominator undercount disclosed, wall-clock reported alongside.
4. Dedup recall - corpus-level property, not single-turn; scoped to precision-on-flagged-pairs plus a sampled recall audit, stated limitation.
5. Entity graph state accumulation - certified against frozen graph snapshots; live drift between snapshot and production graph is a YELLOW-gate trigger, not silently absorbed.
6. Hourly orchestrator wall-clock behavior (queue buildup, cross-cycle interactions) - out of scope for A/C; only Track B observes it, descriptively.

## References

- experiments/grid2q/aeq_grid2q_phase0.py - the harness to extend (per-class evidence field is the one required change; --extra-sut already serves the Ollama tiers)
- AEQ/preregistrations/AEQ_Grid2Q_PreRegistration_v1.md - the registration template (gate structure, verbatim rubrics, priors)
- AEQ/preregistrations/AEQ_Grid2Q_PreRegistration_v1_2.md - the pinning-table format every ChiefOS registration reproduces
- AEQ/AEQ_Lessons_Ledger.md - the defect checklist the new rubric is audited against before registration
- AgentSaaSy_EAM/whitepaper/ARCHITECTURE_NOTE_PreRegistered_Routing_2026-08-06.md - s7 is the three-arm design Track C must match claim-for-claim
