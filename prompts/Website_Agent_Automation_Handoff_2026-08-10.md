# HANDOFF - Website agent: automate the publish pipeline end to end

**Written 2026-08-10 by the AgentSaaSy session. Paste into the session that maintains ~/Projects/Bucketbranch-ai.**

Michael's decision: the publish pipeline should run without him. Two gaps stand between today's manual flow and that: deploys require a human rsync, and the publish queue is only read when someone opens your session. Close both.

## Part 1 - Enable auto-deploy on push

Your deploy.yml is already written and correct; it is disabled only because the secrets were never configured. Finish it:

1. Generate a NEW dedicated ed25519 deploy keypair for CI. Do not reuse the personal hostinger key; a leaked CI secret must never cost the personal key.
2. Install the new public key on the VPS (root@187.124.229.119) in authorized_keys. You have SSH access with the existing key to do this. If you can scope a non-root deploy user that owns only /var/www/bucketbranch, prefer that; document whichever you do.
3. Set the repository secrets on github.com/ibucketbranch/bucketbranch via gh: DEPLOY_SSH_KEY (the new private key), DEPLOY_HOST, DEPLOY_USER, DEPLOY_PATH (/var/www/bucketbranch), and the SITE_URL variable (https://bucketbranch.ai). CF_BEACON_TOKEN only if Michael provides it; the workflow tolerates its absence.
4. Re-enable the push trigger in deploy.yml (the commented block at the top) so main deploys on merge.
5. Prove it: land a trivial commit, watch the Actions run go green, verify the live site answered 200 in the workflow's own check. Then delete the trivial commit's change if it was visible.

After this, "published" means "pushed to main," and nobody rsyncs by hand again.

## Part 2 - Scheduled queue check

The AgentSaaSy session maintains /Users/hudsonclaw/Projects/AgentSaaSy/prompts/website-publish-queue.json (schema documented in docs/AGENTSAASY-PUBLISH-NUDGE.md, which you wrote). Set up a scheduled run of your session, daily at 09:00 local unless Michael says otherwise, that does exactly this:

1. Read the queue file. For every entry with status "ready", no future embargo, and an empty blockers array: pull latest AgentSaasy main, import the source, run the build and check:build gate, commit, push (Part 1 then deploys it).
2. Write back status "published", published_at, and the live URL to the queue entry. Leave "blocked" entries alone but re-read their blockers in case you can now resolve them; if you block something Michael marked ready, put the reason in blockers.
3. If the queue has nothing actionable, exit without committing anything. A no-op run should leave no trace beyond its log.
4. Never publish an entry with a non-empty blockers array, whatever its status says. Never link github.com/ibucketbranch/AgentSaasy anywhere public; it is private. The public evidence home is github.com/ibucketbranch/AEQ.

Use whatever scheduling mechanism fits your environment (a Claude Code scheduled routine, launchd, or cron invoking a headless session). Whichever you pick, the schedule must survive reboots, and its failures must be visible: on a failed run, leave the failure reason where Michael will see it, do not fail silently.

## Standing constraints

- The check:build gate is non-negotiable: no em dashes in output, no "agentic ai" terminology, canonical URLs, no dead internal links.
- The two currently queued entries (cost-of-a-question v3.1.3 and the agent-loop-economics footer fix) are your first real test; publish them through the new pipeline rather than by hand.
- Report back to Michael when both parts work: the Actions run URL, the schedule you installed, and the two entries published.
