# claim-check

Verifies that published documents still agree with reality.

This repo publishes measured results. On 2026-08-20 it went from private to public and several
documents kept asserting things that had stopped being true. The specification header said the
repo was private. The sibling repo's README said the harness and the rubric were not published.
One of those had never been true at all: the rubrics were in the pre-registrations the whole
time, because pre-registration requires them to exist before the run they score.

Nothing failed. The 59 tests were green throughout, because none of this is a code defect. It is
a class of problem no test suite looks for: a document asserting a fact that can be mechanically
verified, where the assertion and reality disagree.

## Running it

```bash
python3 tools/claim_check.py \
  --config tools/claim_check.config.json \
  --repo-root . \
  --state-source live
```

Offline, against a captured snapshot instead of the network:

```bash
python3 tools/claim_check.py \
  --config tools/claim_check.config.json \
  --repo-root . \
  --state-source tools/claim_check.state.json
```

Both modes produce identical findings. Offline is a first-class path, not a degraded one, so this
runs on a machine with no network.

Exit codes: `0` clean, `1` found something real, `2` could not run. A network failure is `2`, never
`0`. Unknown is not the same as fine.

Every instance-specific value lives in the config file. Nothing is baked into the source and there
are no silent defaults, so a missing required flag is an error rather than a guess.

## The checks, and the failure each one came from

| Check | Catches | The actual failure behind it |
|---|---|---|
| `visibility-claims` | Prose asserting a repo is private, public, withheld, or available on request, contradicted by the live API | The spec header said "private" and the AEQ README said "not published" for an unknown number of hours after the flip |
| `paired-file-drift` | Two copies of one canonical document disagreeing outside a declared allowlist | The two public spec copies differed in about 25 places, and the one in Michael's name carried 34 em dashes against his own rule |
| `machine-paths` | `/Users/`, `/home/`, `C:\Users\` in tracked files | Two published drafts carried `/Users/<username>`, which this project forbids |
| `charset` | Em dashes, en dashes, curly quotes in publication-bound files | A previous check used `grep '[^\x00-\x7F]'`, which BSD grep does not read as hex, so it matched nothing and reported clean |
| `tracked-internal` | Internal working files that are git-tracked | Five internal drafts were unstaged deliberately, then swept back in by a later bare `git add -A` and published |
| `python-floor` | A claimed Python version lower than the pins actually require | The README promised 3.10 while numpy and scipy needed 3.12, so a reader on 3.10 got an unresolvable pip error |

## Two deliberate exemptions

**Dated records.** `CLAIM_LEDGER.md` is governed by "amend by dated entry, never by silent edit."
A 2026-08-10 entry saying the repo is private was true when written. Files in
`dated_record_files`, and any bullet beginning with a date, are skipped by `visibility-claims`.
A checker that pressured someone into rewriting an old entry to match today would falsify the
record it exists to protect. There is a green fixture for exactly this, and if the check fires on
it the selftest fails.

**Machine paths.** Exempted by explicit filename in `machine_path_allow_files`, never by pattern.
A rule clever enough to exempt "lines that are describing the rule" would also quietly exempt a
real leak with the same shape. Someone has to add the file on purpose.

## The selftest is the point

```bash
python3 tools/claim_check.py --selftest \
  --config tools/claim_check.config.json --repo-root . \
  --fixtures tools/claim_check_fixtures
```

Every check ships with a fixture it must flag and a fixture it must not. The selftest asserts
that the red fixture produced at least one finding, the green produced none, and both examined a
nonzero number of items. **A check that passes its red fixture fails the selftest.**

That third assertion is not padding. Every run also prints an examined-count per check, because a
check that inspected zero files and passed looks exactly like a clean repo otherwise. Two of the
2026-08-20 failures were operations that reported success while changing nothing: a `git rm
--cached` silently undone by a later `git reset` while the commit message claimed the removal,
and a bulk edit that printed success and touched no files.

The selftest also refuses to run over zero checks rather than passing vacuously. That mirrors a
real defect in a sibling tool, which crashed once every rule became unnecessary and its rules file
was emptied. A mechanism built to be retired has to survive having nothing left to do.

It found a bug in itself on the first run: relative state-source paths were being resolved against
`--repo-root` twice, so four checks could not load their fixtures. It reported CANNOT RUN and
exited nonzero rather than reporting a pass.

## Adding a check

1. Write the function. It takes a context and returns `Result(findings, examined)`. Count
   everything you looked at, not just what you flagged.
2. Register it in `CHECKS`.
3. Add `claim_check_fixtures/<name>/red/` and `<name>/green/`, each with its own `config.json`,
   plus `state.json` if it needs ground truth and `files.txt` if it needs a tracked-file list.
4. Run the selftest. A check without a red fixture fails it, by design.

Anything you cannot verify against an external source of truth does not belong here. No
"does this sound stale" heuristic, no readability scoring, no model. This tool reports whether a
claim is **true**, never whether it is well written.

It does not auto-fix, and it should not. A checker that edits published documents to make itself
pass is how a wrong statement becomes a permanent one. Deciding what a document should say is a
person's job.

## What it does not catch

It would not have told you the repo had been flipped. It catches the aftermath: every document
that quietly stopped being true. Last time that aftermath survived four days.
