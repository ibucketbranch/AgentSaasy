# Image placement map

Every figure in the repo, what it proves, and where it belongs. All paths relative to repo root.

---

## The assets

| File | What it shows | Public-safe? |
|---|---|---|
| `whitepaper/figures/medium_hero_468.png` | "Same answer. 4.68x the tokens." Three-architecture bar chart. Headline claim in one image. | Yes |
| `whitepaper/figures/aeq_pass_matrix.png` | Cheap tier vs frontier across the five query classes. The "cheap model held up" proof. | Yes |
| `whitepaper/figures/annual_cost_bars.png` | Annual cost comparison. | Yes |
| `whitepaper/figures/breakeven_crossover.png` | Where the smart system starts paying for itself. | Yes |
| `whitepaper/figures/system_three_layers.png` | Reasoning / tools / orchestration architecture diagram. | Yes |
| `experiments/other_experiments/AEQ_Results_Infographic.jpg` | Standalone results infographic. | Yes |
| `whitepaper/figures/routing_cost_quality.png` | Routing study cost vs quality. | **NO — gated until Aug 10** (class study) |

---

## Placement by artifact

### Medium article (live)
`https://medium.com/@michael_valderrama/same-model-same-question-4-68x-the-tokens-455725b06add`

- **Hero image (top):** `medium_hero_468.png` — already the right shape and message for the crop
- **In the results section, after the numbers table:** `aeq_pass_matrix.png`
- Cap it at two images. More and readers scroll past all of them.
- Caption discipline: the hero says 4.68x, which is the single-turn simulated figure. The body cites the measured 5.51x / 2.04x live numbers. Name which experiment each image is from so a careful reader is not confused.

### LinkedIn post
- **One image only:** `medium_hero_468.png`. LinkedIn crops wide, and this one survives it.
- Do not attach the pass matrix here; it needs prose around it to mean anything.
- Alternative if you want reach over clarity: `AEQ_Results_Infographic.jpg` as a single-image post, link in first comment.

### X post (Blundin hook)
- **One image:** `medium_hero_468.png`. Same reason.

### bucketbranch.ai one-pager (live)
`https://bucketbranch.ai/reference/agent-loop-economics/`
- Currently all inline SVG, no raster figures. Optional addition: `system_three_layers.png` near the architecture discussion.

### GitHub README
- Embed `medium_hero_468.png` directly under the AEQ heading. A repo README with one strong figure above the fold reads far more credible than a wall of text.
- Markdown: `![Same answer, 4.68x the tokens](whitepaper/figures/medium_hero_468.png)`

### GitHub profile README (ibucketbranch/ibucketbranch)
- Optional: `medium_hero_468.png` under the AEQ section. Needs an absolute raw URL, since a profile README cannot use relative paths into another repo:
  `https://raw.githubusercontent.com/ibucketbranch/AgentSaasy/main/whitepaper/figures/medium_hero_468.png`

### AEQ Specification PDF
- `whitepaper/AEQ_Specification_v1.1.pdf` — 9 pages, generated Aug 7. Section 8 is the experimental results section; `medium_hero_468.png` and `aeq_pass_matrix.png` would both strengthen it if you want a v1.2 with figures embedded.

---

## Open item: repo name conflict

Three different names are in circulation across public-facing documents:

| Document | Cites |
|---|---|
| `README.md` (fixed) | `github.com/ibucketbranch/AgentSaasy` |
| `whitepaper/AEQ_Specification_v1.1.md` header | `github.com/ibucketbranch/AgentSaasy_NGAI` |
| `whitepaper/AGENTIC_SUBSTITUTION_WhitePaper_v3_DRAFT.md` | `github.com/ibucketbranch/AgentSaaSy_EAM` |

Git remote is `git@github.com:ibucketbranch/AgentSaasy.git`, so `AgentSaasy` is the live one.
The spec is now the document everything else cites as source of truth, and it points at a
name that does not resolve. Fix the spec header and regenerate the PDF before circulating it.
