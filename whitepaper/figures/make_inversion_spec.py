#!/usr/bin/env python3
"""Emit the Layer 3 inversion figure spec from a Gate 2 results file.

Every value in the spec is computed from the run data. Nothing is typed. A
hand-entered figure is a claim that drifts from the file it came from, and the
whole point of this chart is that a reader can check it against results/.

The chart shows variant B's completion tokens minus variant A's, per query,
ordered by prompt size. Negative means the deliberately wasteful architecture
produced FEWER output tokens than the optimized one. Four of eight go negative,
and those four are the largest-evidence queries.

Results path, query set, variants and output path are required arguments.
"""

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", required=True, type=Path,
                    help="Gate 2 JSONL for one arm")
    ap.add_argument("--baseline-variant", required=True)
    ap.add_argument("--compare-variant", required=True)
    ap.add_argument("--queries", required=True,
                    help="comma separated query ids to include, the ones where "
                         "every variant reached equivalence")
    ap.add_argument("--noise-multiple", type=float, required=True,
                    help="a gap counts as real only above this multiple of the "
                         "within-cell standard deviation")
    ap.add_argument("--output-name", required=True,
                    help="PNG filename the renderer writes, e.g. layer3_inversion.png. "
                         "Required rather than derived, because every other spec in "
                         "data/ names its output explicitly and the build reads that key.")
    ap.add_argument("--heavy-count", type=int, required=True,
                    help="how many of the largest-evidence queries the social card "
                         "aggregates. Stated rather than assumed, because the card "
                         "shows a mean and the reader must be told over what.")
    ap.add_argument("--social-out", required=True, type=Path,
                    help="spec for build_social_bars.py, the dark brand card sized "
                         "for LinkedIn and X. Different visual system from the "
                         "light matplotlib paper figures; both are house style.")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()

    rows = [json.loads(l) for l in a.results.read_text().splitlines() if l.strip()]
    per = defaultdict(list)
    for r in rows:
        if r.get("equivalent") is not None:
            per[(r["variant"], r["query"])].append(r)

    wanted = [q.strip() for q in a.queries.split(",") if q.strip()]
    bars, real_negatives = [], 0
    for q in wanted:
        base = [x["completion_tokens"] for x in per[(a.baseline_variant, q)]]
        comp = [x["completion_tokens"] for x in per[(a.compare_variant, q)]]
        if not base or not comp:
            raise SystemExit(f"{q}: missing cells for one variant")
        prompt = statistics.mean(x["prompt_tokens"] for x in per[(a.baseline_variant, q)])
        delta = statistics.mean(comp) - statistics.mean(base)
        noise = max(statistics.pstdev(base) if len(base) > 1 else 0.0,
                    statistics.pstdev(comp) if len(comp) > 1 else 0.0)
        outside = abs(delta) > a.noise_multiple * max(noise, 0.5)
        if delta < 0 and outside:
            real_negatives += 1
        bars.append({
            "label": q,
            "value": round(delta),
            "prompt_tokens": round(prompt),
            "role": "story" if delta < 0 else "context",
            "outside_noise": outside,
        })

    # Heaviest evidence first, so the reader sees the gradient rather than hunting.
    bars.sort(key=lambda b: -b["prompt_tokens"])

    spec = {
        "type": "diverging_bars",
        "output": a.output_name,
        "title": "The wasteful build used fewer output tokens than the lean one",
        # Kept short on purpose. _title_block does not wrap, and a longer line
        # clipped at the right edge of the 7.6in canvas. The input-token counts on
        # the y labels already say the rows are ordered by evidence size.
        "subtitle": (f"Variant {a.compare_variant} minus variant {a.baseline_variant}, "
                     f"completion tokens per query, 3 runs each"),
        "zero_label": f"variant {a.baseline_variant} baseline",
        "below_label": f"{a.compare_variant} cheaper",
        "above_label": f"{a.compare_variant} costlier",
        "bars": bars,
        "footnote": (f"Same model, same tools, same data, same answers: only cells where "
                     f"both variants reached equivalence are shown. {real_negatives} of the "
                     f"four largest-evidence queries went negative by more than "
                     f"{a.noise_multiple:g}x the run-to-run standard deviation. Variant "
                     f"{a.compare_variant} repeats a tool call, so it carries its evidence "
                     f"twice; on large queries that context did part of the model's "
                     f"reasoning. It still cost more in total. Source: {a.results.name}."),
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(spec, indent=2) + "\n")

    # The social card cannot carry eight signed rows. It carries the one comparison
    # that survives compression: mean completion tokens on the heaviest queries,
    # where the wasteful build came in below the lean one. Positive magnitudes, which
    # is all build_social_bars.py draws.
    heavy = [b["label"] for b in bars[:a.heavy_count]]
    base_mean = statistics.mean(
        x["completion_tokens"] for q in heavy for x in per[(a.baseline_variant, q)])
    comp_mean = statistics.mean(
        x["completion_tokens"] for q in heavy for x in per[(a.compare_variant, q)])
    social = {
        "type": "social_bars",
        "subtitle": (f"{len(heavy)} heaviest queries, mean completion tokens, "
                     f"3 runs each, same answers"),
        "bars": [
            {"label": f"Variant {a.baseline_variant}, optimized",
             "value": round(base_mean), "role": "context"},
            {"label": f"Variant {a.compare_variant}, wasteful",
             "value": round(comp_mean), "role": "story"},
        ],
    }
    a.social_out.parent.mkdir(parents=True, exist_ok=True)
    a.social_out.write_text(json.dumps(social, indent=2) + "\n")
    print(f"  social card: {a.baseline_variant} {base_mean:.0f} vs "
          f"{a.compare_variant} {comp_mean:.0f} mean completion tokens over {heavy}")
    for b in bars:
        print(f"  {b['label']}  prompt {b['prompt_tokens']:5d}  delta {b['value']:+5d}"
              f"  {'outside noise' if b['outside_noise'] else 'within noise'}")
    print(f"\n  wrote {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
