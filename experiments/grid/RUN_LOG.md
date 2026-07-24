# AEQ 3x3x3 Grid -- Run Log

Factual record of every execution of `aeq_grid_experiment.py`, kept per the
integrity rules in AEQ_Grid_PreRegistration_v1.md section 6 (failed runs
logged, not dropped; results published regardless of outcome). Author:
Michael Valderrama. Log written 2026-07-24.

## Run 1 -- 2026-07-23 (v1.0 config) -- INVALID

Script exit 0, but every Anthropic judge call was rejected with
`judge_http_400: "Your credit balance is too low to access the Anthropic API"`.
No adjudication occurred (judge COGS $0.000000), so the frontier self-pass
check read 0% and the pre-registration's integrity rule invalidated the run.
Independently, all 18 T2/T3 cells returned `no_answer`: gpt-5-mini and
gpt-5-nano consumed the entire MAX_OUTPUT_TOKENS=600 completion budget on
internal reasoning tokens and emitted zero visible text. The frontier tier
(gpt-5.2) produced real answers (128-348 output tokens per run).

Measured SUT costs (real): T1 $0.004191, T2 $0.001337, T3 $0.000268 per query.
Printed verdict: RED (not meaningful; run invalid).
Remedy: author added Anthropic API credit.
Artifacts: overwritten in place by Run 2 before archiving practice was
adopted; the numbers above are from the session record of Run 1's report.

## Run 2 -- 2026-07-23T22:04:40Z (v1.0 config) -- INVALID

Judge (claude-haiku-4-5-20251001) executed normally ($0.017132 total judge
spend). Frontier self-pass came in at 7/9, below the required 8/9, firing the
integrity flag again. Diagnosis of the two failed cells (both Q1_retrieval):
the judge rejected correct frontier answers with arithmetically false notes,
e.g. "GEN-004 (health 46) does not meet the critical threshold of health < 50"
when 46 is below 50 and the evidence defines critical as h<50 with 7 of 12
critical assets unshown. Conclusion: rubric sound, judge model erred.
All 18 T2/T3 cells were again `no_answer` under the 600-token cap.

Measured SUT costs: T1 $0.004497, T2 $0.001342, T3 $0.000268 per query.
Printed verdict: RED (not meaningful; run invalid).
Remedy: pre-registration amended to v1.1
(whitepaper/AEQ_Grid_PreRegistration_v1_1.md, author-approved):
MAX_OUTPUT_TOKENS 600 -> 4000, JUDGE_MODEL -> claude-opus-4-8, judge pricing
row -> $5/$25 per MTok. Gates, rubrics, queries, evidence, and the declared
prior unchanged.
Artifacts: archived at `v1_0_run2_2026-07-23/`.

## Run 3 -- 2026-07-24T00:27:34Z (v1.1 config) -- VALID

Frontier self-pass 9/9; integrity check satisfied. All 27 cells passed
(aggregate SUT pass 100% vs the declared 75-80% prior; Q3 100%).
Costs: T1 $0.004263, T2 $0.002037, T3 $0.000946 per query.
Cost deltas: T1/T2 2.1x, T1/T3 4.5x, both below the 5x GREEN gate.
Judge COGS: $0.011268 per verified query (claude-opus-4-8).

Computed verdict: YELLOW. Note: the result matches no gate definition
literally (quality conditions exceed GREEN, cost delta fails it; aggregate is
not in YELLOW's 40-70% band); the script emits YELLOW as the residual bucket
when GREEN's cost condition fails. The v1.0 gate taxonomy did not anticipate
perfect quality with insufficient cost spread.

Open item carried on all runs: PRICING_VERIFIED = False. The OpenAI pricing
rows are third-party placeholders and must be verified against the official
pricing page before any cost figure is published; the judge row was verified
against Anthropic's published $5/$25 on 2026-07-23.

Artifacts: `aeq_grid_report.md`, `aeq_grid_raw.json` (current files).
