#!/bin/bash
# Watchdog runner for long experiment jobs, meant to be fired periodically by
# launchd (or cron). Each invocation is a no-op unless the job is neither
# finished nor currently running, in which case it starts the job under
# caffeinate -i so idle sleep cannot kill it.
#
# All instance specifics arrive as arguments; nothing is hardcoded:
#   grid_watchdog.sh <repo_root> <done_file> <log_file> <pgrep_marker> -- <command...>
#
#   repo_root     directory to cd into before starting (where .env lives)
#   done_file     file whose existence means the job completed (e.g. the report)
#   log_file      appended with watchdog events and the job's stdout/stderr
#   pgrep_marker  string unique to the job's command line, used to detect a live run
#   command...    the job itself, e.g. ./venv/bin/python experiments/... --flags
set -euo pipefail

if [ "$#" -lt 6 ]; then
    echo "usage: grid_watchdog.sh <repo_root> <done_file> <log_file> <pgrep_marker> -- <command...>" >&2
    exit 64
fi
REPO_ROOT="$1"; DONE_FILE="$2"; LOG_FILE="$3"; MARKER="$4"; shift 4
if [ "$1" != "--" ]; then
    echo "grid_watchdog.sh: expected -- before the command" >&2
    exit 64
fi
shift

# Job already finished: nothing to do.
[ -f "$DONE_FILE" ] && exit 0

# Job already running: leave it alone. Exclude this wrapper's own pid and its
# parent, since the marker also appears in our own argument list.
live=$(pgrep -f "$MARKER" | grep -v -e "^$$\$" -e "^$PPID\$" || true)
if [ -n "$live" ]; then
    exit 0
fi

cd "$REPO_ROOT"
mkdir -p "$(dirname "$LOG_FILE")"
echo "[watchdog $(date -u +%Y-%m-%dT%H:%M:%SZ)] starting: $*" >> "$LOG_FILE"
PYTHONUNBUFFERED=1 exec caffeinate -i "$@" >> "$LOG_FILE" 2>&1
