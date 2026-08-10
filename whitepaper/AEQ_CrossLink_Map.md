# AEQ cross-link map

Every public artifact and what it should point to. Swap `[MEDIUM_URL]` and `[EXACT MEDIUM TITLE]`
once per file. Repo URL used throughout: github.com/ibucketbranch/AgentSaasy

---

## The link graph

```
   Goldberg / CIO Dive article (external, the news hook)
              ^
              | cited by all three
              |
   Medium article  <----->  bucketbranch.ai one-pager
        ^      \                    |
        |       \                   v
   LinkedIn post  ------------>  GitHub repo (primary evidence, dated attribution)
        |                            ^
        |                            |
   Discussion 7.1 (Canvas) ----------+
```

Rule of thumb: **GitHub is the evidence, Medium is the explanation, the one-pager is the
brand home, LinkedIn is the megaphone, Canvas is coursework.** Everything points down the
chain toward evidence; nothing points at LinkedIn.

---

## 1. Discussion 7.1 (Canvas) — STATUS: wired, pending Medium URL

- Inline: `(Valderrama, 2026a, 2026b)` at the AEQ introduction. DONE
- Reference: Goldberg (2026), Torres (2026), Valderrama (2026a, GitHub), Valderrama (2026b, Medium). DONE, Medium entry needs URL + title
- Do NOT link: the class routing study, until Aug 10 submission and repo flip
- Do NOT link: bucketbranch.ai (commercial site in coursework reads as self-promotion)

## 2. Medium article — STATUS: yours to wire while publishing

Link out to:
- The Goldberg CIO Dive piece, high in the article. This is the news hook and it earns the timeliness.
- The Torres / EY piece where the 4-in-5 and 37% figures appear.
- The GitHub repo, placed immediately next to the measured numbers (2.04x / 5.51x, 4.68x) so a skeptic can verify. This is the load-bearing link.
- The bucketbranch.ai one-pager, as further reading on where AEQ plugs into a loop architecture.
- Bucketbranch in the author bio at the bottom. Not in the body.

Do NOT link: the class routing study.

## 3. bucketbranch.ai one-pager (agent_loop_economics_onepager_v1_1_WEB.html) — STATUS: wired, pending Medium URL

- Footer: GitHub repo. DONE
- Footer: Medium article as plain-language writeup. DONE, needs URL + title
- Header + bio: bucketbranch.ai. DONE

## 4. LinkedIn post — STATUS: needs rewrite from measured numbers

- One link only: the Medium article. Multiple links split clicks and LinkedIn suppresses external links.
- Tag Chen Goldberg, since the post builds on her argument and you already commented on her thread.
- Repo link goes in the first comment, not the post body.

## 5. GitHub repo README — STATUS: not done, worth doing

Add a short "Writeups" section near the top:
- Medium: plain-language explanation of the measured AEQ results
- bucketbranch.ai: the agent-loop economics reference one-pager

This closes the loop. Someone who arrives at the evidence can find the explanation, which is
how a repo visitor becomes a reader and eventually a client.

---

## Open items

1. `[MEDIUM_URL]` and `[EXACT MEDIUM TITLE]` in two files: the Canvas draft and this one-pager.
2. Repo URL check: this page and the crosslink map use `github.com/ibucketbranch/AgentSaasy`,
   while the v3 whitepaper draft cites `github.com/ibucketbranch/AgentSaaSy_EAM`. Confirm which
   one is public and correct, then make every artifact agree. A dead repo link in a graded
   reference list or a launch post is the one error that costs credibility outright.
3. Aug 10 gate: nothing citing the class routing study publishes before submission and repo flip.
