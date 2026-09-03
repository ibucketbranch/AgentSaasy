# HANDOFF PROMPT — bucketbranch.ai: site review fix punch list, 2026-08-31

Paste everything below this line into the session that has the bucketbranch.ai site repo.

---

You are working on the bucketbranch.ai website. A full site review on 2026-08-31 found the issues below. Fix all of them. Before changing anything, inspect the repo to learn the stack and conventions; match the existing theme and templates. Do not invent a new design language.

## Hard requirements (apply to every file you touch)

- NEVER write "Agentic AI" or "agentic artificial intelligence." Use "AI agents," "AI agent architecture," or "agentic architecture." Case-insensitive grep for both banned forms on every file you touch before finishing.
- Plain ASCII in all copy: straight quotes, regular hyphens, no em dashes, no curly quotes, no emoji.
- Attribution where the template shows an author: "Michael Valderrama | AI Agent Architect | Independent R&D (c) 2026"
- Do not soften numbers or add marketing superlatives.
- Never link the Blueberry repository (private). github.com/ibucketbranch/AEQ, github.com/ibucketbranch/AgentSaasy, and github.com/ibucketbranch/MS-AAI-501-Final_Project_IntroAI are public and safe to link. Never link ibucketbranch/MS-AAI-501 (course archive, private).

## Task 1 — Process the publish queue

Read prompts/website-publish-queue.json in the AgentSaaSy repo (main branch, commit bda49fc or later (was bd9586b before that commit was rewritten on 2026-09-02 to strip an AI attribution trailer; same tree, new hash)). Two entries are status "ready":

1. agentic-architecture-enterprise-eam (v2.1.1): the live page at /papers/agentic-architecture-enterprise-eam/ still displays "White Paper - v2.1.0" in its own header block while the papers index and homepage cite v2.1.1. Re-import from TECHNICAL-WHITE-PAPER.md so the page header, abstract cost sentence ($0.0009 measured average, about $329 per year), and version-history table match the v2.1.1 source.
2. agentsaasy-eam (v1.1): re-import /case-studies/agentsaasy-eam/ from the new canonical source whitepaper/CASE_STUDY_AgentSaaSy_EAM.md. Changes: a dated pricing note under the measurements marking $0.0030/query as a run-date upper bound after the 2026-08-07 certified-tier reprice, and the technical-reference citation bumped to v2.1.1. Keep the version-history table; do not strip trailing sections.

When each is live and verified, write "published" with published_at and the live URL back onto its queue entry, per the queue protocol.

## Task 2 — Papers index bug

The /papers/ index lists only the technical reference. "The Cost of a Question" v3.1.5 is published at /papers/cost-of-a-question/ and featured on the homepage but missing from its own section index. Restore it to the index with its one-line role description ("The economics thesis: certified cheap models against per-seat pricing, with a break-even accounting.").

## Task 3 — Framework landing page version drift

/framework/ still describes the AEQ specification as v1.1 dated August 2026. The current spec is v1.2, dated 2026-08-25, live at /framework/aeq/. Update the landing copy. Do not redirect or remove v1.1; it stays published and citable per the aeq-specification queue entry notes.

## Task 4 — Writing page date error

/writing/ dates the Medium article "Same Model, Same Question, 4.68x the Tokens" as July 2026. It published August 8, 2026. Correct the date.

## Task 5 — Cross-page version sweep

After Tasks 1-3, grep the whole site for "v2.1.0" and "v1.1" in contexts citing the technical reference or the AEQ spec, and update any stray citations (the case study's "Read the engineering" link is one known instance). Citations that legitimately refer to the v1.1 spec as a historical version stay.

## Task 6 — PROPOSE ONLY, do not publish without Michael's approval

Two editorial items. Draft them and show Michael before anything goes live:

1. Resume page positioning: /resume/ leads with "Senior Engineering Program Manager" while the rest of the site says "AI Agent Architect." Draft a bridging headline and one-paragraph intro that frames the program-management record as the delivery track behind the R&D, so the two identities introduce each other instead of competing.
2. Writing section expansion: the section holds one Medium article and two LinkedIn posts. Propose a layout for adding recent LinkedIn/X posts as dated excerpt entries with outbound links. Michael supplies the post URLs; do not fabricate entries.

## Acceptance checks before you finish

- Fetch each changed page live and verify: EAM paper header says v2.1.1; case study shows the pricing note and cites v2.1.1; /papers/ index lists both papers; /framework/ says v1.2; /writing/ says August 8, 2026.
- Banned-term grep is clean on every touched file.
- Queue entries 1 and 2 written back as "published" with published_at and URLs.
- Report back a list of every file changed and every check result.
