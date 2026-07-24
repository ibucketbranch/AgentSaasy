# AEQ 3x3x3 GRID -- RESULTS
Run completed: 2026-07-24T00:27:34Z | Runs per cell: 3
Models: {'T1_frontier': 'gpt-5.2', 'T2_mid': 'gpt-5-mini', 'T3_nano': 'gpt-5-nano'} | Judge: claude-opus-4-8
Pricing verified against official pages: False  << VERIFY BEFORE PUBLICATION

## PASS-RATE MATRIX (query class x tier)
  Q1_retrieval   | T1_frontier: 3/3 | T2_mid: 3/3 | T3_nano: 3/3
  Q2_analytical  | T1_frontier: 3/3 | T2_mid: 3/3 | T3_nano: 3/3
  Q3_synthesis   | T1_frontier: 3/3 | T2_mid: 3/3 | T3_nano: 3/3

## AGGREGATES
  Frontier reference self-pass : 100%  (integrity check; must be >= ~89%)
  Aggregate SUT pass (T2+T3)   : 100%   (declared prior: 75-80%)
  Q3 (hardest) SUT pass        : 100%
  Mean cost/query  T1: $0.004263  T2: $0.002037  T3: $0.000946
  Cost delta  T1/T2: 2.1x   T1/T3: 4.5x
  Verification overhead per verified query (judge COGS): $0.011268

## GATE VERDICT (locked thresholds -- pre-registration section 5)
  >>> YELLOW <<<
  GREEN : agg >= 70% AND cost delta >= 5x AND Q3 >= 50%
  YELLOW: agg 40-70%, or GREEN numbers with Q3 < 50%
  RED   : agg < 40%, or passes confined to Q1

## FAILED CELLS
  (none)

Full answers and per-cell data: aeq_grid_raw.json
Author: Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026