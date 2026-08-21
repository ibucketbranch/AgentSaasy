# Prompt: teach the AgentSaaSy session to nudge the website

Paste everything below the line into the session that maintains `~/Projects/AgentSaaSy`. It is written to be pasted once and then kept in that project's `CLAUDE.md` so it survives new sessions.

The design: AgentSaaSy never touches the website repo. It writes one machine-readable queue file inside its own tree. The website session reads that file at the start of every session and publishes what is marked ready.

---

You are the AgentSaaSy session. A separate session owns the bucketbranch.ai website at `~/Projects/Bucketbranch-ai` and publishes your work. You two communicate through one file.

## The rule

**Never edit anything under `~/Projects/Bucketbranch-ai`.** You do not build, deploy, or import anything. Your job ends at telling the website session what is ready.

## The queue file

Maintain `prompts/website-publish-queue.json` in this repo. It is a JSON array. One object per artifact that the website should carry. Create it if it does not exist.

Add or update an entry whenever any of these happen:

- A white paper, specification, or reference document reaches a version you would show someone.
- An existing published document changes in a way a reader would notice: a corrected figure, a retitle, a version bump, a retracted claim.
- An embargo lifts on something already queued.
- A repository that a published document cites changes visibility.

Do not queue drafts you are still arguing with. "Ready" means you would defend it in public today.

## Entry schema

Every field is required unless marked optional. Use plain ASCII, no em dashes.

```json
[
  {
    "id": "cost-of-a-question",
    "status": "ready",
    "kind": "paper",
    "title": "The Cost of a Question",
    "version": "3.1.1",
    "source": "/Users/hudsonclaw/Projects/AgentSaaSy/whitepaper/AGENTIC_SUBSTITUTION_WhitePaper_v3_DRAFT.md",
    "changed": "Retitled from The Agentic Substitution. Economics corrected to the certified tier. Section 3.3 quantization finding scrub-verified and live-reproduced.",
    "figures": "/Users/hudsonclaw/Projects/AgentSaaSy/whitepaper/figures/",
    "embargo": null,
    "blockers": [],
    "notes": "Section 3.3 cites experiments/grid2q/phase1_2026-07-24/SCRUB_REPORT.md. That repo is private, so it must render as plain text, not a link."
  }
]
```

Field meanings:

- **id**: stable slug, lowercase and hyphenated. Never change it once the website has published under it, because it becomes the URL.
- **status**: `ready`, `blocked`, or `published`. Only the website session sets `published`. You set `ready` or `blocked`.
- **kind**: `paper`, `spec`, `case-study`, `reference`, or `writing`. This decides which section of the site it lands in.
- **title** and **version**: exactly as they should appear to a reader.
- **source**: absolute path to the markdown the website should import. Not a PDF. If only a PDF exists, say so in `blockers`.
- **changed**: what a returning reader would notice. Not a changelog dump, one or two sentences.
- **figures** (optional): absolute path to the directory holding any images the document references. Omit if it has none.
- **embargo**: `null`, or an ISO date the website must not publish before. The website will not publish an entry with a future embargo date even if status is `ready`.
- **blockers**: array of strings. Anything that must be resolved before publishing. Empty array means clear.
- **notes** (optional): anything the website needs to get right that is not obvious from the source.

## Things that have gone wrong before, so call them out explicitly

Put these in `notes` or `blockers` when they apply. Each one has already cost a real mistake:

1. **Citations to private repositories.** If the document names a GitHub repo, say whether it is public. A citation to a private repo renders as a dead end for every reader, and it has shipped more than once.
2. **Figures the document references but that do not travel with it.** Give the directory. If a figure is gated by an embargo, name that figure specifically.
3. **A source that was corrected after a handoff was written.** If you fix a number in a source document, update the entry's `changed` field the same day. The website hashes every source it imported and will detect the drift, but it will not know why the change happened.
4. **Documents whose own header cites a version or repo that has moved.** Say so.

## When you change a source that is already published

Do not create a new entry. Update the existing one: bump `version`, rewrite `changed`, and set `status` back to `ready`. The website tracks a hash of every source it imported, so it will flag the drift on its own, but your `changed` line is what tells it whether the edit is publishable or mid-thought.

## What you get back

The website session sets `status` to `published` and appends a `published_at` date and the live URL. Treat those fields as read-only. If you see `blocked` on an entry you marked ready, read the `blockers` array; the website put the reason there.

## Do not

- Do not write anything except `prompts/website-publish-queue.json`. No handoff prose files; this replaces them.
- Do not queue anything under an active embargo without setting the `embargo` date.
- Do not include credentials, API keys, or private URLs in any field.
