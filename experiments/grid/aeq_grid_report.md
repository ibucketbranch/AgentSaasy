# AEQ 3x3x3 GRID -- RESULTS
Run completed: 2026-07-23T22:04:40Z | Runs per cell: 3
Models: {'T1_frontier': 'gpt-5.2', 'T2_mid': 'gpt-5-mini', 'T3_nano': 'gpt-5-nano'} | Judge: claude-haiku-4-5-20251001
Pricing verified against official pages: False  << VERIFY BEFORE PUBLICATION

## PASS-RATE MATRIX (query class x tier)
  Q1_retrieval   | T1_frontier: 1/3 | T2_mid: 0/3 | T3_nano: 0/3
  Q2_analytical  | T1_frontier: 3/3 | T2_mid: 0/3 | T3_nano: 0/3
  Q3_synthesis   | T1_frontier: 3/3 | T2_mid: 0/3 | T3_nano: 0/3

## AGGREGATES
  Frontier reference self-pass : 78%  (integrity check; must be >= ~89%)
  Aggregate SUT pass (T2+T3)   : 0%   (declared prior: 75-80%)
  Q3 (hardest) SUT pass        : 0%
  Mean cost/query  T1: $0.004497  T2: $0.001342  T3: $0.000268
  Cost delta  T1/T2: 3.4x   T1/T3: 16.8x
  Verification overhead per verified query (judge COGS): $0.000000

## GATE VERDICT (locked thresholds -- pre-registration section 5)
  >>> RED <<<
  GREEN : agg >= 70% AND cost delta >= 5x AND Q3 >= 50%
  YELLOW: agg 40-70%, or GREEN numbers with Q3 < 50%
  RED   : agg < 40%, or passes confined to Q1

## FAILED CELLS
  Q1_retrieval x T2_mid run 1: no_answer -- 
  Q1_retrieval x T2_mid run 2: no_answer -- 
  Q1_retrieval x T2_mid run 3: no_answer -- 
  Q2_analytical x T2_mid run 1: no_answer -- 
  Q2_analytical x T2_mid run 2: no_answer -- 
  Q2_analytical x T2_mid run 3: no_answer -- 
  Q3_synthesis x T2_mid run 1: no_answer -- 
  Q3_synthesis x T2_mid run 2: no_answer -- 
  Q3_synthesis x T2_mid run 3: no_answer -- 
  Q1_retrieval x T3_nano run 1: no_answer -- 
  Q1_retrieval x T3_nano run 2: no_answer -- 
  Q1_retrieval x T3_nano run 3: no_answer -- 
  Q2_analytical x T3_nano run 1: no_answer -- 
  Q2_analytical x T3_nano run 2: no_answer -- 
  Q2_analytical x T3_nano run 3: no_answer -- 
  Q3_synthesis x T3_nano run 1: no_answer -- 
  Q3_synthesis x T3_nano run 2: no_answer -- 
  Q3_synthesis x T3_nano run 3: no_answer -- 

  [!] INTEGRITY FLAG: frontier reference failed its own rubric too often.
      Per pre-registration: fix rubric, re-register as v1.1, re-run.

Full answers and per-cell data: aeq_grid_raw.json
Author: Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026