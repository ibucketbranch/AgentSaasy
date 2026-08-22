# ChiefOS Swarm Data Plane - Provisioning Record

**Provisioned 2026-08-20 per `03-live-visualization.md`. Status: LIVE, awaiting the ingest secret and first emitter traffic.**

## What exists

Supabase project **chiefos-swarm** (ref `boxngtgdlrajahvcbruh`, region us-west-1, free tier, $0/month), dedicated to the public sanitized telemetry feed. Deliberately separate from the njoy project so the swarm data plane shares nothing with production client infrastructure.

- Project URL: `https://boxngtgdlrajahvcbruh.supabase.co`
- Publishable (anon) key, designed-public, safe to embed in the site page:
  `sb_publishable_iR0QumHCzZ0bfoGWhx3DeQ_wSKdKCDM`
  (legacy JWT anon key also exists if the site's supabase-js version needs it)

### Database (migration `swarm_data_plane_v1`)

- `public.swarm_events` - contract v1 envelopes: `(v, seq, ts, cycle_id, type, data jsonb)`, unique on `(cycle_id, seq)` so emitter retries are idempotent. Indexed by cycle, by time, by type.
- `public.swarm_cycles` - one row per cycle: `started_at`, `completed_at`, `summary` (the cycle_completed data).
- RLS enabled on both: SELECT for anon/authenticated, no public writes. Writes happen only through the service role inside the Edge Function.
- Realtime publication includes `swarm_events` inserts (the page's live mode).
- Retention: pg_cron job `swarm-events-retention` deletes raw events older than 30 days, daily at 03:30 UTC. Cycle summaries are kept indefinitely.
- Storage: public bucket `swarm`; the Edge Function rewrites `swarm/snapshot.json` after every completed cycle (cache-control 60s).

### Edge Function `ingest` (v1, ACTIVE)

`POST https://boxngtgdlrajahvcbruh.supabase.co/functions/v1/ingest`

- Auth: `Authorization: Bearer <INGEST_SECRET>` - a function secret, not a Supabase JWT (verify_jwt is off; the function does its own check and returns 401 without the secret).
- Body: one envelope or an array of up to 500: `{"v":1,"seq":N,"ts":ISO,"cycle_id":"c-...","type":...,"data":{...}}`.
- Validation is structural, enforcing the contract in `03-live-visualization.md` section 3: event types, agent/tier/task_kind/outcome enums, numeric fields, `run_id_hash` as short hex, ISO timestamps. **No free-text field exists in the schema, so a path, prompt, or name cannot leak even by emitter bug.** Invalid envelopes get a 422 with the failing index; nothing partial is written.
- Side effects: upserts events (duplicates ignored), maintains `swarm_cycles` on `cycle_started` / `cycle_completed`, and regenerates the snapshot on `cycle_completed`.

## What the owner must do (one-time, ~5 minutes)

1. Generate a strong secret and set it as Edge Function secret `INGEST_SECRET` in the Supabase dashboard (Project Settings -> Edge Functions -> Secrets) for project chiefos-swarm. Store the same value in the Mac mini's keychain/env for the emitter. It must never enter any repo.
2. Smoke-test from the mini:

```
curl -s -X POST \
  -H "Authorization: Bearer $INGEST_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"v":1,"seq":1,"ts":"2026-08-20T12:00:00Z","cycle_id":"c-2026-08-20T12","type":"heartbeat","data":{}}' \
  https://boxngtgdlrajahvcbruh.supabase.co/functions/v1/ingest
```

Expected: `{"ok":true,"inserted":1}`. A wrong/missing secret returns 401; a malformed envelope returns 422.

3. Point the ChiefOS emitter (telemetry phase 7, the public projector) at the ingest URL, batching per `03-live-visualization.md` 1.2.

## What the website page consumes

- Snapshot: `https://boxngtgdlrajahvcbruh.supabase.co/storage/v1/object/public/swarm/snapshot.json`
- Realtime: supabase-js subscription to INSERTs on `public.swarm_events` using the publishable key.
- Both are read-only; the worst a leaked ingest secret allows is fake telemetry rows (rotate the secret to fix); the publishable key allows reads of already-public data only.
- nginx CSP check before v1 ships: `connect-src` must allow `https://boxngtgdlrajahvcbruh.supabase.co` and `wss://boxngtgdlrajahvcbruh.supabase.co`.

## Contract discipline

The Edge Function validator, the mini's emitter, and the site's player all pin contract `v: 1`. Changing the contract means bumping `v` in all three and letting the page's unknown-major fallback (RECORDED mode) cover the transition. The validator is the enforcement point: extend its enums only in lockstep with a registered schema change.
