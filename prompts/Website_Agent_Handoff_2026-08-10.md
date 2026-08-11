# HANDOFF - Website agent: publish "The Cost of a Question" v3.1.1 to bucketbranch.ai

**Written 2026-08-10. Paste into the session that maintains ~/Projects/Bucketbranch-ai.**

Ground truth as of this morning, verified by direct checks, trust this over any earlier handoff:

- https://bucketbranch.ai/papers/cost-of-a-question/ returns **404**. The paper is NOT live. The 2026-08-09 engineering handoff claimed it was; that was wrong. The site source `src/content/papers/cost-of-a-question.md` is a stub with `published: false` and version 3.0.0.
- The local site repo has committed but unpushed work through 3f53af4 (papers restructure, case studies, writing section, framework section with the AEQ spec, footer version stamp, the one-pager fold, the EAM paper at v2.1.1). `main` has no upstream set; nothing after the last push has reached github.com:ibucketbranch/bucketbranch.
- The live docroot has received two surgical syncs on top of the old layout: the EAM technical paper at v2.1.1 and /reference/agent-loop-economics/. Everything else committed locally is not yet live. A full build-and-mirror deploy is expected and desired; it ships all of it at once.
- AgentSaasy main is at 48a509d (harness reprice). Pull it fresh; the paper source is `whitepaper/AGENTIC_SUBSTITUTION_WhitePaper_v3_DRAFT.md`, title "The Cost of a Question", version block 3.1.1 with the 2026-08-09 scrub note.

## Task

1. Pull latest AgentSaasy main. Import the v3.1.1 paper into `src/content/papers/cost-of-a-question.md` with `scripts/import-paper.py` (required flags: --input, --output, --audit; use --strip-toc and --strip-header as you did for the EAM paper, and read the audit report before accepting the currency/math classification). Keep the existing frontmatter identity fields (title, subtitle, role, description, author, companion, companionNote). Set `version: "3.1.1"`, `date` to today, `published: true`.
2. The Section 3.3 scrub sentences reference `experiments/grid2q/phase1_2026-07-24/SCRUB_REPORT.md`. The AgentSaasy repo is private right now, so that path must render as plain text, not a hyperlink. No dead links.
3. If the papers layout links a downloadable PDF, build it from the v3.1.1 markdown (the PDF is gitignored in AgentSaasy, do not expect it there). If the layout does not link one, skip.
4. Build and gate: `npm run build && npm run check:build` must pass clean. Additional acceptance on top of the gate: case-insensitive grep over changed files for "agentic ai" and "agentic artificial intelligence" is zero hits; /reference/agent-loop-economics/ still resolves in dist (that URL is already public; if the one-pager fold moved it, keep a page or redirect at the old path).
5. Reconcile git before deploying: fetch, then `git push -u origin main`. If the remote has diverged, stop and reconcile; do not force-push.
6. Deploy the full dist with the standard mirror: `rsync -az --delete --checksum dist/ root@187.124.229.119:/var/www/bucketbranch/` using the hostinger key. The njoy paths on that host are nginx proxies, not files; the mirror does not touch them. Do not touch nginx config or anything outside the docroot.
7. Verify live after deploy: / returns 200; /papers/cost-of-a-question/ returns 200 and shows v3.1.1; /papers/agentic-architecture-enterprise-eam/ still shows v2.1.1 and zero occurrences of "288"; /reference/agent-loop-economics/ still returns 200.
8. Report back: the live URLs, the version strings you verified, and the commit you deployed from.

## Do not

- Do not edit anything in ~/Projects/AgentSaaSy except `git pull`.
- Do not remove or rewrite the pricing paragraphs; the paper's economics were recomputed for the 2026-08-07 luna reprice and the claim ledger governs them.
- Do not deploy from a dirty tree; commit first so the deployed state is reproducible.
