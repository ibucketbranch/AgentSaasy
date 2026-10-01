# Export One Real Cycle Into the ChiefOS Live Page

**Written 2026-10-01. For the ChiefOS session on the Mac mini.**

The page `prompts/assets/chiefos-live-demo.html` replays one orchestrator cycle from an
embedded recording. It ships with a synthetic sample and therefore shows the
"SIMULATED DATA - DEMO" badge. Your job is a one-time swap: export one real sanitized
cycle, replace the sample, and the page flips itself to "RECORDED RUN - REAL DATA".

## What to produce

A JSON object with exactly this shape (contract chiefos-public/1, see
plans/chiefos-aeq-eval/03-live-visualization.md section 3):

```
{
  "v": 1,
  "provenance": {
    "recorded_at": "<ISO timestamp of the cycle>",
    "source": "ChiefOS production, sanitized",
    "approved": "<YYYY-MM-DD you reviewed it>",
    "synthetic": false
  },
  "events": [ { "v":1, "seq":N, "ts":ISO, "cycle_id":"c-...", "type":..., "data":{...} }, ... ]
}
```

Event types and their data fields are the closed vocabulary in the design doc:
cycle_started, agent_task_started, llm_call, task_completed, cycle_completed,
eval_published, heartbeat. Agents: orchestrator, filing_clerk, lost_found, dedup_hunter,
student, profiler, auditor, keeper. Tiers: rules, local_fast, local_analyst, cloud.
Outcomes: accepted, escalated, review.

## Sanitization rules (structural, per 01-telemetry-spec.md section 4)

- Every data field is a number or a value from the closed enums above. No free text,
  no document names, no paths, no model tags (tier only), no confidence numbers,
  no thresholds.
- Timestamps may keep second precision inside one cycle; the cycle's date is fine to
  publish (the hourly cadence is already public).
- Before handing off, scan the JSON: if any string value is not one of the enum words,
  an ISO timestamp, or a cycle id of the form c-..., it does not ship.

## How to swap it in

1. In chiefos-live-demo.html, replace the entire `const RECORDING = {...};` literal
   with your exported object. Nothing else changes; the badge, caption, and footer
   read provenance.synthetic at load.
2. Open the file locally and check: badge reads RECORDED RUN - REAL DATA with the date,
   replay runs, meters land on your cycle_completed totals, zero console errors.
3. Commit with a line stating the cycle date and that the export passed the
   sanitization scan. The publication-scrub workflow will re-check terminology and
   character hygiene on push.
4. Flip the queue entry `chiefos-live` in prompts/website-publish-queue.json from
   blocked to ready, clear the blocker, and message the website session (the queue is
   the record, the message is the trigger).

## Notes

- Keep the eval_published event OUT of the first real recording unless a registered
  AEQ-L evaluation actually ran; the AEQ-L card correctly shows "no evaluated run yet"
  when the event is absent.
- A cycle with 10-30 documents replays best. If the cycle is huge, export it anyway;
  the player caps long gaps and the log trims itself.
- This recording also becomes the permanent fallback for the v1/v2 live modes later,
  so pick a cycle you are happy to leave on the site.
