#!/usr/bin/env python3
"""Keep a shared harness byte-identical across the repos that carry a copy.

Why this exists: on 2026-08-15 the Grid-2Q harness existed as two hand-edited
files in two repos. Two sessions changed them within thirty minutes, one porting
a price constant and one refactoring the query set out of the script. Git cannot
catch that, because they are different files in different repositories, so
nothing conflicts and nothing warns. The drift only surfaced when a push was
rejected for an unrelated reason.

The rule this enforces: one repo owns the file, every other copy is derived, and
a derived copy that has drifted is a bug rather than a variant. There is
deliberately no merge and no three-way anything. If the copy differs, the copy
is wrong.

Nothing instance-specific is baked in. Source directory, destination directory,
and the file list all arrive as required flags, so this works for any shared
bundle, not just this one.

  # fail if any copy has drifted (use in a pre-push hook or by hand)
  python sync_harness.py --check --source-dir DIR --dest-dir DIR \\
      --file aeq_grid2q_phase0.py --file queries.eam-phase0.json

  # overwrite the copies from the source of truth
  python sync_harness.py --sync --source-dir DIR --dest-dir DIR --file NAME
"""

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="report drift and exit non-zero; changes nothing")
    mode.add_argument("--sync", action="store_true",
                      help="overwrite the destination copies from the source")
    ap.add_argument("--source-dir", required=True, type=Path,
                    help="directory holding the authoritative files")
    ap.add_argument("--dest-dir", required=True, type=Path,
                    help="directory holding the derived copies")
    ap.add_argument("--file", required=True, action="append", dest="files",
                    metavar="NAME", help="filename present in both directories; repeatable")
    a = ap.parse_args()

    drifted, missing = [], []
    for name in a.files:
        src, dst = a.source_dir / name, a.dest_dir / name
        if not src.exists():
            print(f"[ERROR] source missing: {src}")
            return 2
        if not dst.exists():
            missing.append(name)
            continue
        if digest(src) != digest(dst):
            drifted.append(name)

    if a.sync:
        for name in drifted + missing:
            a.dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(a.source_dir / name, a.dest_dir / name)
            print(f"  synced  {name}")
        if not drifted and not missing:
            print("  already identical, nothing to do")
        return 0

    for name in missing:
        print(f"  MISSING {name}  (absent from {a.dest_dir})")
    for name in drifted:
        print(f"  DRIFTED {name}")
    if drifted or missing:
        print(f"\n{len(drifted) + len(missing)} file(s) out of sync. "
              f"The copy is wrong by definition; re-run with --sync.")
        return 1
    print(f"  all {len(a.files)} file(s) identical")
    return 0


if __name__ == "__main__":
    sys.exit(main())
