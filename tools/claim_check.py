#!/usr/bin/env python3
"""claim-check: verify that published documents still agree with reality.

This repo publishes measured results. On 2026-08-20 it went from private to
public and several documents kept asserting things that had stopped being true:
the specification header said the repo was private, and the sibling repo's README
said the harness and the rubric were not published. One of those had never been
true at all. Nothing failed. The test suite was green the whole time, because
none of it is a code defect.

What this tool checks is narrower than "is the writing good" and much more
useful: a document asserts a fact that can be mechanically verified, and the
assertion disagrees with reality.

Every check here is deterministic. String comparison, file comparison, or an
HTTP GET against a documented API. There is deliberately no model in this tool,
including for the cases that feel fuzzy. A model asked "does this document
contradict reality" produces a confident wrong answer, which is the failure mode
the tool exists to catch.

Two failures on 2026-08-20 came from operations that reported success while
doing nothing: a `git rm --cached` silently undone by a later `git reset` while
the commit message claimed the removal, and a bulk edit that printed success and
changed zero files. That is why every check reports how many items it examined,
and why --selftest asserts that each check actually fires on a fixture built to
break it. A check that cannot fail is worse than no check.

Nothing instance-specific is baked in. Repo names, paths, file lists, and
patterns all come from the config file, whose path is a required flag.

Exit codes:
  0  every check passed
  1  at least one check found a real problem
  2  the tool could not run (bad config, missing file, network failure)

A network failure is never a passing repo. Exit 2 means "unknown", not "fine".
"""

import argparse
import fnmatch
import json
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

EXIT_OK, EXIT_FINDINGS, EXIT_CANNOT_RUN = 0, 1, 2

TEXT_SUFFIXES = {".md", ".txt", ".html", ".json", ".yml", ".yaml", ".py", ".cff", ".toml", ".ini"}


class CannotRun(Exception):
    """The tool cannot answer the question. Never downgrade this to a pass."""


class Finding:
    def __init__(self, check, path, line, message):
        self.check, self.path, self.line, self.message = check, path, line, message

    def __str__(self):
        where = f"{self.path}:{self.line}" if self.line else str(self.path)
        return f"{self.check} {where} {self.message}"


class Result:
    """Findings plus how many items were looked at.

    The count is not decoration. A check that examined zero files and passed
    looks identical to a clean repo unless the count is visible.
    """

    def __init__(self, findings, examined):
        self.findings, self.examined = findings, examined


# ---------------------------------------------------------------- state source

class StateSource:
    """Where ground truth comes from: the live APIs, or a captured snapshot.

    Offline operation is a first-class mode, not a degraded one. The snapshot
    format is documented in tools/README.md.
    """

    def __init__(self, spec, config, repo_root):
        self.spec, self.config, self.repo_root = spec, config, repo_root
        self.live = spec == "live"
        self.snapshot = None
        if not self.live:
            # Try the path as given, then relative to the repo. Fixtures pass a
            # path already relative to the working directory, real runs pass one
            # relative to the repo root; resolving only one way breaks the other.
            p = Path(spec)
            if not p.is_file():
                p = repo_root / spec
            if not p.is_file():
                raise CannotRun(f"state source is neither 'live' nor a readable file: {spec}")
            try:
                self.snapshot = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                raise CannotRun(f"state snapshot is not valid JSON: {p} ({e})")

    def _get_json(self, url):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise CannotRun(f"HTTP {e.code} fetching {url}")
        except Exception as e:
            raise CannotRun(f"network failure fetching {url}: {e}")

    def repo_is_private(self, full_name):
        """True/False. A 404 unauthenticated means private or nonexistent."""
        if self.live:
            d = self._get_json(f"https://api.github.com/repos/{full_name}")
            return True if d is None else bool(d.get("private"))
        repos = self.snapshot.get("repos", {})
        if full_name not in repos:
            raise CannotRun(
                f"repo {full_name} is not in the state snapshot. Recapture it, or the "
                f"check would silently skip a claim it cannot verify.")
        return bool(repos[full_name].get("private"))

    def fetch_repo_file(self, full_name, path, local_checkouts):
        """Sibling-repo file content. Live over raw, offline from a local checkout."""
        if self.live:
            url = f"https://raw.githubusercontent.com/{full_name}/main/{path}"
            try:
                with urllib.request.urlopen(url, timeout=20) as r:
                    return r.read().decode("utf-8")
            except Exception as e:
                raise CannotRun(f"could not fetch {url}: {e}")
        alias = None
        for k, v in self.config.get("repos", {}).items():
            if v == full_name:
                alias = k
        base = local_checkouts.get(alias) or local_checkouts.get(full_name)
        if not base:
            raise CannotRun(
                f"offline run needs config.local_checkouts['{alias or full_name}'] "
                f"to compare against {full_name}:{path}")
        p = Path(base)
        if not p.is_absolute():
            p = self.repo_root / p
        f = p / path
        if not f.is_file():
            raise CannotRun(f"local checkout is missing {f}")
        return f.read_text(encoding="utf-8")

    def requires_python(self, name, version):
        """The requires-python string for one pinned release, or None."""
        key = f"{name}=={version}"
        if self.live:
            d = self._get_json(f"https://pypi.org/pypi/{name}/{version}/json")
            if d is None:
                raise CannotRun(f"PyPI has no release {key}")
            return (d.get("info") or {}).get("requires_python")
        pypi = self.snapshot.get("pypi", {})
        if key not in pypi:
            raise CannotRun(f"{key} is not in the state snapshot")
        return pypi[key].get("requires_python")

    def age_warning(self):
        if self.live:
            return None
        cap = self.snapshot.get("captured")
        if not cap:
            return "state snapshot has no 'captured' date; cannot tell how stale it is"
        return None


# --------------------------------------------------------------------- helpers

def tracked_files(config, repo_root):
    """The file list a check operates on.

    Normally git. Fixtures declare tracked_files_from instead, because a fixture
    must not have to stage anything to be tested.
    """
    declared = config.get("tracked_files_from")
    if declared:
        p = repo_root / declared
        if not p.is_file():
            raise CannotRun(f"tracked_files_from points at a missing file: {p}")
        return [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    try:
        out = subprocess.run(["git", "-C", str(repo_root), "ls-files"],
                             capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise CannotRun(f"could not list tracked files in {repo_root}: {e}")
    return [l for l in out.splitlines() if l]


def under_publication_paths(rel, publication_paths):
    for pp in publication_paths:
        if pp.endswith("/"):
            if rel.startswith(pp):
                return True
        elif rel == pp or rel.startswith(pp.rstrip("/") + "/"):
            return True
    return False


def read_text(repo_root, rel):
    p = repo_root / rel
    if not p.is_file():
        return None
    if p.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def require(config, key, check_name):
    if key not in config:
        raise CannotRun(
            f"check '{check_name}' needs config key '{key}'. Add it, or drop the check "
            f"from --check. Skipping it silently would be the same defect as a check "
            f"that examines nothing and passes.")
    return config[key]


def parse_python_floor(requires_python):
    """Highest >= floor in a requires-python spec, as a (major, minor) tuple."""
    if not requires_python:
        return None
    floors = re.findall(r">=\s*(\d+)\.(\d+)", requires_python)
    if not floors:
        return None
    return max((int(a), int(b)) for a, b in floors)


# ---------------------------------------------------------------------- checks

VISIBILITY_PHRASES = [
    (r"\bis private\b", "private"),
    (r"\bis public\b", "public"),
    (r"\(private\)", "private"),
    (r"\(public\)", "public"),
    (r"\|\s*private\s*\|", "private"),
    (r"\|\s*public\s*\|", "public"),
    (r"\bnot published\b", "private"),
    (r"\bwithheld\b", "private"),
    (r"\bis not released\b", "private"),
    (r"\bavailable on request\b", "private"),
    (r"\brequest the harness\b", "private"),
    (r"\bonly public home\b", "public"),
]

DATED_BULLET = re.compile(r"^\s*[-*]\s*\*?\*?(\d{4}-\d{2}-\d{2})")


def check_visibility_claims(ctx):
    """Sentences asserting a repo's visibility, checked against actual state.

    Dated records are deliberately exempt. CLAIM_LEDGER.md is governed by
    "amend by dated entry, never by silent edit", so a checker that pressures
    someone into rewriting a 2026-08-10 entry to match today is worse than no
    checker: it would falsify the record it is supposed to protect.
    """
    cfg, root = ctx.config, ctx.repo_root
    pub = require(cfg, "publication_paths", "visibility-claims")
    repos = require(cfg, "repos", "visibility-claims")
    dated_files = set(cfg.get("dated_record_files", []))
    alias_re = {a: re.compile(r"\b" + re.escape(a) + r"\b", re.I) for a in repos}

    findings, examined = [], 0
    for rel in tracked_files(cfg, root):
        if not under_publication_paths(rel, pub) or rel in dated_files:
            continue
        text = read_text(root, rel)
        if text is None:
            continue
        examined += 1
        in_dated = False
        for n, line in enumerate(text.splitlines(), 1):
            if DATED_BULLET.match(line):
                in_dated = True
            elif not line.strip():
                in_dated = False
            if in_dated:
                continue
            for pat, claimed in VISIBILITY_PHRASES:
                if not re.search(pat, line, re.I):
                    continue
                m = re.search(r"github\.com/([\w.-]+/[\w.-]+)", line)
                full = m.group(1).rstrip(".,;:)") if m else None
                if not full:
                    for alias, fn in repos.items():
                        if alias_re[alias].search(line):
                            full = fn
                            break
                if not full:
                    continue
                actual = "private" if ctx.state.repo_is_private(full) else "public"
                if actual != claimed:
                    # Quote the trigger. Attribution is a heuristic (nearest URL,
                    # then alias), so on a line making two claims at once it can
                    # name the wrong repo while still being right that the line
                    # is stale. Showing the phrase lets a human see which it is.
                    hit = re.search(pat, line, re.I).group(0)
                    findings.append(Finding(
                        "visibility-claims", rel, n,
                        f"phrase {hit!r} reads as {claimed}, but {full} is {actual}"))
                break
    return Result(findings, examined)


def check_paired_file_drift(ctx):
    """Two copies of one canonical document must agree, except where declared.

    Two public copies of the AEQ specification disagreed in about 25 places and
    nothing noticed. experiments/grid2q/sync_harness.py enforces the same
    one-owner-many-copies idea for byte-identical files; this differs by allowing
    declared per-copy exceptions, which is why it is not just a call into that.
    """
    cfg, root = ctx.config, ctx.repo_root
    pairs = require(cfg, "paired_files", "paired-file-drift")
    repos = require(cfg, "repos", "paired-file-drift")
    checkouts = cfg.get("local_checkouts", {})

    findings, examined = [], 0
    for pair in pairs:
        a_rel = pair["a"]
        a_text = read_text(root, a_rel)
        if a_text is None:
            raise CannotRun(f"paired file A is missing or unreadable: {a_rel}")
        full = repos.get(pair["b_repo"], pair["b_repo"])
        b_text = ctx.state.fetch_repo_file(full, pair["b_path"], checkouts)
        allow = [re.compile(p) for p in pair.get("allow_differ_matching", [])]
        examined += 1

        a_lines = [l.rstrip() for l in a_text.splitlines()]
        b_lines = [l.rstrip() for l in b_text.splitlines()]
        for n in range(max(len(a_lines), len(b_lines))):
            a = a_lines[n] if n < len(a_lines) else "<absent>"
            b = b_lines[n] if n < len(b_lines) else "<absent>"
            if a == b:
                continue
            if any(r.search(a) or r.search(b) for r in allow):
                continue
            findings.append(Finding(
                "paired-file-drift", a_rel, n + 1,
                f"differs from {full}:{pair['b_path']}\n"
                f"      here:  {a[:150]}\n"
                f"      there: {b[:150]}"))
    return Result(findings, examined)


MACHINE_PATH = re.compile(r"(/Users/|/home/|C:\\Users\\)")


def check_machine_paths(ctx):
    """No absolute machine paths in tracked files.

    The allowlist is by file and has to be edited on purpose. Pattern-matching
    an exception for "lines that look like they are describing the rule" would
    quietly exempt real leaks with the same shape.
    """
    cfg, root = ctx.config, ctx.repo_root
    allow = set(cfg.get("machine_path_allow_files", []))
    findings, examined = [], 0
    for rel in tracked_files(cfg, root):
        if rel in allow:
            continue
        text = read_text(root, rel)
        if text is None:
            continue
        examined += 1
        for n, line in enumerate(text.splitlines(), 1):
            m = MACHINE_PATH.search(line)
            if m:
                findings.append(Finding("machine-paths", rel, n,
                                        f"absolute machine path: {m.group(1)}"))
    return Result(findings, examined)


BANNED_CHARS = {"\u2014": "EM DASH", "\u2013": "EN DASH", "\u2018": "LEFT SINGLE QUOTE",
                "\u2019": "RIGHT SINGLE QUOTE", "\u201c": "LEFT DOUBLE QUOTE",
                "\u201d": "RIGHT DOUBLE QUOTE"}


def check_charset(ctx):
    """Publication-bound files stay plain ASCII on punctuation.

    Done in Python on decoded text, on purpose. An earlier attempt in this repo
    used grep '[^\\x00-\\x7F]', which BSD grep does not interpret as hex, so it
    matched nothing and reported clean.
    """
    cfg, root = ctx.config, ctx.repo_root
    pub = require(cfg, "publication_paths", "charset")
    exempt = set(cfg.get("charset_allow_files", []))
    findings, examined = [], 0
    for rel in tracked_files(cfg, root):
        if not under_publication_paths(rel, pub) or rel in exempt:
            continue
        text = read_text(root, rel)
        if text is None:
            continue
        examined += 1
        for n, line in enumerate(text.splitlines(), 1):
            for col, ch in enumerate(line, 1):
                if ch in BANNED_CHARS:
                    findings.append(Finding("charset", rel, n,
                                            f"col {col}: {BANNED_CHARS[ch]}"))
    return Result(findings, examined)


def check_tracked_internal(ctx):
    """Internal working files must not be tracked.

    Catches the git add -A trap: five internal drafts were unstaged on purpose,
    then swept back in by a later bare `add -A` and published.
    """
    cfg, root = ctx.config, ctx.repo_root
    pats = require(cfg, "internal_patterns", "tracked-internal")
    findings, examined = [], 0
    for rel in tracked_files(cfg, root):
        examined += 1
        base = rel.rsplit("/", 1)[-1]
        for pat in pats:
            # Case-insensitive on purpose. '*HANDOFF*.md' written in caps matched
            # none of the real _handoff.md and _Handoff_v1.md files, so the check
            # examined every tracked file and found nothing because its pattern
            # was wrong. That is the failure mode this tool is named after.
            if (fnmatch.fnmatch(rel.lower(), pat.lower())
                    or fnmatch.fnmatch(base.lower(), pat.lower())):
                findings.append(Finding("tracked-internal", rel, None,
                                        f"tracked but matches internal pattern '{pat}'"))
                break
    return Result(findings, examined)


def check_python_floor(ctx):
    """The claimed Python floor must not be lower than what the pins require.

    This fired for real: numpy and scipy needed 3.12 while the README promised
    3.10, so a reader on 3.10 following the quickstart got an unresolvable pip
    error rather than a clear version message.
    """
    cfg, root = ctx.config, ctx.repo_root
    spec = require(cfg, "python_floor_claim", "python-floor")
    claim_file, pattern = spec["file"], spec["pattern"]
    req_file = spec["requirements_file"]

    text = read_text(root, claim_file)
    if text is None:
        raise CannotRun(f"python_floor_claim.file is missing or unreadable: {claim_file}")
    m = re.search(pattern, text)
    if not m:
        raise CannotRun(
            f"python_floor_claim.pattern matched nothing in {claim_file}. A pattern that "
            f"stops matching after its target is reworded is a check that silently stops "
            f"checking, so this is an error rather than a pass.")
    claimed = tuple(int(x) for x in m.group(1).split("."))
    claim_line = text[:m.start()].count("\n") + 1

    reqs = (root / req_file)
    if not reqs.is_file():
        raise CannotRun(f"requirements file is missing: {req_file}")
    pins = re.findall(r"^([A-Za-z0-9_.\-]+)==([A-Za-z0-9_.\-]+)\s*$",
                      reqs.read_text(encoding="utf-8"), re.M)
    if not pins:
        raise CannotRun(f"no name==version pins found in {req_file}")

    findings, examined, real, driver = [], 0, None, None
    for name, version in pins:
        examined += 1
        floor = parse_python_floor(ctx.state.requires_python(name, version))
        if floor and (real is None or floor > real):
            real, driver = floor, f"{name}=={version}"

    if real and claimed < real:
        findings.append(Finding(
            "python-floor", claim_file, claim_line,
            f"claims Python {claimed[0]}.{claimed[1]}, but pins require "
            f"{real[0]}.{real[1]} (driven by {driver})"))
    return Result(findings, examined)


PIN_SHAPE = re.compile(r"^\s*([A-Za-z0-9_.\-]+)\s*(==|>=|~=)\s*[0-9]")


def normalize_pypi_name(name):
    """PyPI ignores case and treats '-' and '_' as the same character.

    requirements.txt carries canonical names (PyYAML, python-dotenv) while prose
    writes whatever the author typed, so a literal comparison would report a
    declared dependency as phantom.
    """
    return name.replace("_", "-").lower()


def check_phantom_pins(ctx):
    """A version pin must name a package that is actually a dependency.

    Commit 9dcd25e removed a scikit-learn pin from documents describing a project
    that never installed scikit-learn. Only the pin shape is flagged, never a
    bare mention: a note about numpy can say scikit-learn is built on it, and a
    style guide can teach scikit-learn patterns, without either being a claim
    about this project's dependencies. A pin says "install this version", which
    is either true or it is not, and that is what makes the check safe to fail on.
    """
    cfg, root = ctx.config, ctx.repo_root
    req_file = require(cfg, "phantom_pins_requirements_file", "phantom-pins")
    allow = set(cfg.get("phantom_pins_allow_files", []))

    reqs = root / req_file
    if not reqs.is_file():
        raise CannotRun(f"requirements file is missing: {req_file}")
    declared = set()
    for line in reqs.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if not stripped:
            continue
        m = re.match(r"([A-Za-z0-9_.\-]+)", stripped)
        if m:
            declared.add(normalize_pypi_name(m.group(1)))
    if not declared:
        raise CannotRun(f"no package names found in {req_file}")

    findings, examined = [], 0
    for rel in tracked_files(cfg, root):
        if rel in allow:
            continue
        # A package pinned in the requirements file trivially appears in the
        # requirements file, so that one file cannot contradict itself.
        if (root / rel).resolve() == reqs.resolve():
            continue
        text = read_text(root, rel)
        if text is None:
            continue
        examined += 1
        for n, line in enumerate(text.splitlines(), 1):
            m = PIN_SHAPE.match(line)
            if not m:
                continue
            name = m.group(1)
            if normalize_pypi_name(name) in declared:
                continue
            findings.append(Finding(
                "phantom-pins", rel, n,
                f"pins {name}, which is not in {req_file}: {line.strip()[:80]}"))
    return Result(findings, examined)


CHECKS = {
    "visibility-claims": check_visibility_claims,
    "paired-file-drift": check_paired_file_drift,
    "machine-paths": check_machine_paths,
    "charset": check_charset,
    "tracked-internal": check_tracked_internal,
    "python-floor": check_python_floor,
    "phantom-pins": check_phantom_pins,
}


# ------------------------------------------------------------------ selftest

class Ctx:
    def __init__(self, config, repo_root, state):
        self.config, self.repo_root, self.state = config, repo_root, state


def load_config(path):
    p = Path(path)
    if not p.is_file():
        raise CannotRun(f"config file not found: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise CannotRun(f"config is not valid JSON: {path} ({e})")


def run_selftest(fixtures_dir, names):
    """Prove each check fires on a fixture built to break it.

    A check that passes its red fixture fails the selftest. That is the whole
    point: the tool must not be able to report a clean repo by doing nothing.
    """
    fixtures = Path(fixtures_dir)
    if not fixtures.is_dir():
        print(f"SELFTEST cannot run: fixtures directory not found: {fixtures_dir}")
        return EXIT_CANNOT_RUN
    if not names:
        print("SELFTEST cannot run: no checks registered. A selftest over zero checks "
              "would pass vacuously, which is the defect it exists to prevent.")
        return EXIT_CANNOT_RUN

    ok = True
    for name in names:
        counts = {}
        for colour in ("red", "green"):
            d = fixtures / name / colour
            cfg_path = d / "config.json"
            if not cfg_path.is_file():
                print(f"SELFTEST {name}: MISSING {colour} fixture at {d}")
                ok = False
                counts[colour] = None
                continue
            try:
                cfg = load_config(cfg_path)
                state_spec = "live"
                if (d / "state.json").is_file():
                    state_spec = str(d / "state.json")
                ctx = Ctx(cfg, d, StateSource(state_spec, cfg, d))
                res = CHECKS[name](ctx)
                counts[colour] = (len(res.findings), res.examined)
            except CannotRun as e:
                print(f"SELFTEST {name}: {colour} fixture could not run: {e}")
                ok = False
                counts[colour] = None

        r, g = counts.get("red"), counts.get("green")
        if r is None or g is None:
            ok = False
            continue
        print(f"SELFTEST {name}: red={r[0]} findings, green={g[0]} findings, "
              f"examined={r[1]}/{g[1]}")
        if r[0] < 1:
            print(f"  FAIL {name} did not fire on its red fixture. The check cannot fail, "
                  f"so it proves nothing when it passes.")
            ok = False
        if g[0] != 0:
            print(f"  FAIL {name} fired on its green fixture ({g[0]} findings).")
            ok = False
        if r[1] < 1 or g[1] < 1:
            print(f"  FAIL {name} examined zero items. Passing while looking at nothing "
                  f"is the failure this tool exists to catch.")
            ok = False

    print(f"\nSELFTEST {'PASS' if ok else 'FAIL'} over {len(names)} check(s)")
    return EXIT_OK if ok else EXIT_FINDINGS


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True,
                    help="path to the config file (all instance-specific values live there)")
    ap.add_argument("--repo-root", required=True, type=Path,
                    help="repository to inspect")
    ap.add_argument("--check", action="append", dest="checks", metavar="NAME",
                    help=f"run only this check; repeatable. One of: {', '.join(CHECKS)}")
    ap.add_argument("--state-source",
                    help="'live' to query GitHub and PyPI, or a path to a state snapshot")
    ap.add_argument("--selftest", action="store_true",
                    help="run the checks against their fixtures instead of the repo")
    ap.add_argument("--fixtures", help="fixtures directory (required with --selftest)")
    a = ap.parse_args()

    names = a.checks or list(CHECKS)
    unknown = [n for n in names if n not in CHECKS]
    if unknown:
        print(f"unknown check(s): {', '.join(unknown)}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if a.selftest:
        if not a.fixtures:
            print("--selftest requires --fixtures", file=sys.stderr)
            return EXIT_CANNOT_RUN
        return run_selftest(a.fixtures, names)

    if not a.state_source:
        print("--state-source is required ('live' or a snapshot path). There is no "
              "default on purpose: a wrong guess about where truth comes from is "
              "exactly the bug this tool looks for.", file=sys.stderr)
        return EXIT_CANNOT_RUN

    root = a.repo_root.resolve()
    if not root.is_dir():
        print(f"--repo-root is not a directory: {root}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    try:
        config = load_config(a.config)
        state = StateSource(a.state_source, config, root)
    except CannotRun as e:
        print(f"cannot run: {e}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    warn = state.age_warning()
    if warn:
        print(f"WARNING {warn}")

    ctx = Ctx(config, root, state)
    all_findings, summary, cannot = [], [], False
    for name in names:
        try:
            res = CHECKS[name](ctx)
        except CannotRun as e:
            summary.append(f"  {name:20} CANNOT RUN  {e}")
            cannot = True
            continue
        all_findings.extend(res.findings)
        status = "PASS" if not res.findings else f"{len(res.findings)} FINDING(S)"
        summary.append(f"  {name:20} {status:16} examined {res.examined}")

    for f in all_findings:
        print(f)
    if all_findings:
        print()
    print("summary:")
    for line in summary:
        print(line)

    if cannot:
        return EXIT_CANNOT_RUN
    return EXIT_FINDINGS if all_findings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
