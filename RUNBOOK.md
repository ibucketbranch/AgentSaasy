# RUNBOOK

Facts about this repo for an agent working in it. Everything here was checked
against the code on the date given, not recalled. If you repeat a claim from
this file you may say it was verified then. If you need it true *now*, re-check
it; the commands are included so that is cheap.

Verified 2026-08-24.

## What this is

Two things share the repo. `AgentSaaSy_EAM` is a working enterprise asset
management agent. The AEQ program is the measurement method it was the workload
for. The specification and public run records live in the separate
`ibucketbranch/AEQ` repo; this one is the reference implementation.

This repo has been public since 2026-08-20. Both it and the AEQ repo are
public, confirmed against the GitHub API.

## Stack

One chat model behind seven tools over a pandas DataFrame, orchestrated with
LangChain in a ReAct pattern.

- Model: `gpt-4o-mini` via `ChatOpenAI` (`langchain_openai`)
- Tools: 7 functions in `agent.py`, each carrying an `@tool` decorator
- Data: `data/asset_data.csv`, 50 synthetic assets, 10 columns. No database.
- Python 3.12 or newer per the README, and the pins genuinely require it

Check the tool count with `grep -c '^@tool' agent.py`.

## The seven tools

`query_assets`, `analyze_asset_health`, `predict_failures`, `calculate_tco`,
`track_compliance`, `optimize_field_routes`, `plan_capital_strategy`.

Two of them are the ones added later, and things that predate them tend to
still say five: `optimize_field_routes` and `plan_capital_strategy`.

`optimize_field_routes` is a scenario model over statistical simulation, not a
solved road network. Drive-time reductions come from industry multipliers on a
baseline. Documentation that reads as though it routes against real geography
is overstating it.

`plan_capital_strategy` takes `monte_carlo_iterations`, default 1000. That
default is why anything invoking it is slow.

## Tests

59 tests, in 12 classes across `tests/test_agent.py` and
`tests/test_capital_planning.py`. They are methods on `Test*` classes, not
module-level functions, so `grep '^def test_'` finds nothing and is misleading.

They take about 183 seconds. That number matters: it is longer than some agent
shell timeouts, and a timeout there reads as a hang rather than a slow suite.
CI takes 5 to 8 minutes for the same suite, which is normal for the runner and
not a symptom.

    python3 -m pytest tests/ -q

No API key needed. The tools are testable without one.

## Running the demos

There are six entry points and they overlap, which is the main reason "the
demo" is ambiguous. `chat_agent.py` is what the README points people at.
`demo_full_agent.py` is the one that exercises all seven tools and has an
`--iterations N` flag for a fast path.

    ./venv/bin/python demo_full_agent.py --iterations 50   about 23s
    ./venv/bin/python demo_full_agent.py                   about 158s

Anything reaching the model needs `OPENAI_API_KEY` in `.env`, which is
gitignored. Without it the tools still work but the ReAct loop fails on the
first model call.

Both `venv` and `.venv` exist and are both Python 3.13. `venv` is the one in
use.

## claim-check

`tools/claim_check.py` verifies that published documents still agree with
reality, and runs in CI on every push and pull request.

Its selftest runs first and is a gate: it proves each check still fires
against a fixture built to break it. A check that cannot fail is treated as
broken, not passing. Run both before assuming a green result means anything:

    python3 tools/claim_check.py --selftest --config tools/claim_check.config.json \
      --repo-root . --fixtures tools/claim_check_fixtures
    python3 tools/claim_check.py --config tools/claim_check.config.json \
      --repo-root . --state-source live

Things that will trip it:

- Absolute machine paths in any tracked file. The regex matches the home
  directory prefix itself rather than the username after it, so replacing your
  username with a placeholder does not clear the finding; the file needs an
  explicit allowlist entry, and only three have one. This very bullet had to be
  worded around that.
- The phrases `is private`, `not published`, `withheld`, `is not released`,
  `available on request`, `request the harness`, checked against live repo
  visibility. This bites when a doc describes something as unavailable that has
  since been published.
- Files matching `*HANDOFF*.md` being tracked. Eleven were untracked on
  2026-08-20 for that reason, and a `.gitignore` pattern now blocks new ones.
  Use `git add -f` if one genuinely belongs in public.
- Non-ASCII in anything under `publication_paths`. Root-level files outside
  that list are not charset-checked, but the machine-path check covers
  everything tracked.

`prompts/` is deliberately outside `publication_paths`, so instructions written
for agents are not visibility-checked. A stale instruction there still acts on
the world; one was found telling a website agent never to link this repo
because it was private.
