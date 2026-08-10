# HANDOFF — Claude Code in Cursor: publish white paper v3.1.1 + engineering backlog
**Updated 2026-08-09. Supersedes the 2026-08-07 version of this prompt.**

Paste everything below into Claude Code inside Cursor, opened at ~/Projects/AgentSaaSy.

---

You are working in the AgentSaasy repo (canonical remote: github.com/ibucketbranch/AgentSaasy, branch main). Read CLAUDE.md at the repo root first — it carries the standing rules (terminology, naming discipline, claim ledger governance). Then read whitepaper/CLAIM_LEDGER.md; it is the source of truth for claim status. Pull latest main before touching anything.

## What has happened since the last handoff (context, do not redo)

1. **The quantization scrub (former Task 1) is COMPLETE — do not redo it.** The D1 inversion was forensically audited and then live-reproduced on freshly pulled weights: verdict SURVIVES. Full chain in `experiments/grid2q/phase1_2026-07-24/SCRUB_REPORT.md` (three dated addenda: audit, template verification, live replay with digests). The replay script is `experiments/grid2q/replay_q5_inversion.py`. Ledger D1 is CLOSED.
2. The white paper is published at bucketbranch.ai/papers/cost-of-a-question/ and has now been updated locally to **v3.1.1**: Section 3.3 gained a scrub-and-reproduction paragraph, and the version block was bumped. The updated markdown and regenerated 16-page PDF are committed on main (see task 1 below).
3. The Medium article is live: https://medium.com/@michael_valderrama/same-model-same-question-4-68x-the-tokens-455725b06add — `whitepaper/AEQ_CrossLink_Map.md` placeholders have been filled with this URL.
4. Prices were re-verified 2026-08-07: gpt-5.6-luna was repriced 5x down to $0.20/$1.20 per MTok (see commit e478368 and the paper's pricing note). The paper handles it; the harness does not yet (task 2).

## Task 1 — Publish white paper v3.1.1 to the site (READY NOW for pickup)

The updated paper is committed on AgentSaasy main as of the commit tagged in the message "White paper v3.1.1". Source of truth: `whitepaper/AGENTIC_SUBSTITUTION_WhitePaper_v3_DRAFT.md` (title: "The Cost of a Question"). In the bucketbranch.ai site repo:

1. Update /papers/cost-of-a-question/ content from the v3.1.1 markdown. The delta vs what is live: (a) Section 3.3 quantization paragraph now includes the scrub-and-live-reproduction sentences with the SCRUB_REPORT path; (b) version block reads v3.1.1 with the 2026-08-09 note.
2. Bump the displayed version to v3.1.1 and the date to August 9, 2026.
3. If the site links a PDF, regenerate or copy from the repo's regenerated PDF (16 pages). The PDF is gitignored in AgentSaasy; build from markdown or request the file.
4. Acceptance: case-insensitive grep on changed files for "agentic ai" and "agentic artificial intelligence" = zero hits; all internal links resolve; the SCRUB_REPORT reference renders as text or a repo link (repo is currently private — do not create a dead hyperlink; plain path text is fine until the repo flips public).

## Task 2 — Harness price constants (still pending)

`experiments/aeq_experiment.py` lines ~91-92 still carry PRICE_IN_PER_MTOK = 1.00 / PRICE_OUT_PER_MTOK = 6.00 (verified 2026-07-24). OpenAI repriced gpt-5.6-luna to **$0.20 in / $1.20 out** (verified 2026-08-07 at openai.com/api/pricing). Update the constants and comment block with the new figures and date. Do not touch recorded result files. Also check `aeq_grid_experiment.py` and `experiments/grid2q/aeq_grid2q_phase0.py` for hardcoded prices; same treatment.

## Task 3 — Package the public reproduction repo (aeq-reproduce) (still pending)

Create sibling repo ~/Projects/aeq-reproduce (fresh git init, NOT a clone — nothing leaks via history). Contents: the grid2q harness and pre-registration series, the emitted run reports (refresh_gpt56_2026-07-24, multimodel_2026-07-24, phase1_2026-07-24 including SCRUB_REPORT.md, localmodels_2026-07-29), the 4.68x experiment (aeq_experiment.py, aeq_dual_results.txt, STUDY-DESIGN.md), `replay_q5_inversion.py` as the flagship instant demo (local-only, no API keys), a copy of AEQ_Specification_v1.1.md, and a single entry point `python reproduce.py --all`. README covers the one-command quickstart, per-experiment costs, and links to bucketbranch.ai/papers/. **New standing rule from the scrub: every local-model run records `ollama list` digests alongside tags in its report.** Strict exclusions: no client-adjacent material, no draft posts, no handoff prompts, no .env or keys, pinned requirements.txt, verify clean-venv install.

## Acceptance before you finish (all tasks)

- Case-insensitive grep across everything touched: zero hits for "agentic ai" / "agentic artificial intelligence".
- python -m py_compile on every touched .py file.
- CLAIM_LEDGER.md gets a dated entry for the harness reprice (C2 row already notes it as pending in the harness).
- Standing rules: no MacGyver, sourced claims only, pre-registration discipline non-negotiable.
