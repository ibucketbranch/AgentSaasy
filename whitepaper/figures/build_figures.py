"""Render the white paper figures from JSON specs.

Every number, label, and output filename lives in the spec files; this script
only knows how to draw the three figure types. Run:

    python3 build_figures.py --data-dir <dir of *.json specs> --out-dir <dir for PNGs>
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Palette roles (dataviz reference instance, light mode)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
STORY = "#2a78d6"          # categorical slot 1, the emphasis hue
DEEMPH = "#898781"          # gray for context marks; identity carried by labels
SEQ_RAMP = ["#cde2fb", "#6da7ec", "#256abf", "#104281"]  # blue steps 100/300/500/650

# Pinned to the font matplotlib bundles, deliberately. The earlier list started
# with Helvetica Neue and Arial, so output depended on which system fonts the
# rendering machine happened to have: a machine with Helvetica Neue produced
# different text metrics and a visibly different figure from one without, and
# every published figure here was in fact rendered on a machine that fell back
# to DejaVu. Pinning makes the render reproducible anywhere and keeps the
# already-published figures pixel-identical on rebuild. Verified 2026-08-15.
FONT = {"family": ["DejaVu Sans"]}
plt.rcParams.update({
    "font.family": FONT["family"],
    "text.color": INK,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def _title_block(fig, title, subtitle):
    fig.text(0.02, 0.965, title, fontsize=13, fontweight="semibold", color=INK,
             va="top", parse_math=False)
    fig.text(0.02, 0.915, subtitle, fontsize=9.5, color=INK_2, va="top",
             parse_math=False)


def _footnote(fig, text):
    # parse_math off: dollar amounts in footnotes must not trigger mathtext
    fig.text(0.02, 0.012, text, fontsize=7.5, color=MUTED, va="bottom",
             wrap=True, parse_math=False)


def draw_pass_matrix(spec, out_path):
    rows, cols, values = spec["rows"], spec["cols"], spec["values"]
    max_runs = spec["max_runs"]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    fig.subplots_adjust(top=0.80, bottom=0.14, left=0.28, right=0.96)

    for i, row_vals in enumerate(values):
        for j, v in enumerate(row_vals):
            color = SEQ_RAMP[min(v, len(SEQ_RAMP) - 1)]
            # 2px surface gap between cells, done as margin inside each cell
            ax.add_patch(plt.Rectangle((j + 0.02, i + 0.02), 0.96, 0.96,
                                       facecolor=color, edgecolor="none"))
            label_ink = "#ffffff" if v >= 2 else INK
            ax.text(j + 0.5, i + 0.5, f"{v}/{max_runs}", ha="center", va="center",
                    fontsize=11, fontweight="semibold", color=label_ink)

    ax.set_xlim(0, len(cols))
    ax.set_ylim(len(rows), 0)
    ax.set_xticks([j + 0.5 for j in range(len(cols))])
    ax.set_xticklabels(cols, fontsize=9, color=INK_2)
    ax.set_yticks([i + 0.5 for i in range(len(rows))])
    ax.set_yticklabels(rows, fontsize=9.5, color=INK_2)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    _title_block(fig, spec["title"], spec["subtitle"])
    _footnote(fig, spec["footnote"])
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def draw_cost_quality_scatter(spec, out_path):
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    fig.subplots_adjust(top=0.84, bottom=0.17, left=0.10, right=0.97)

    for p in spec["points"]:
        role = p["role"]
        if role == "story":
            face, edge, size = STORY, SURFACE, 90
        elif role == "bound":
            face, edge, size = SURFACE, MUTED, 80
        else:
            face, edge, size = DEEMPH, SURFACE, 70
        ax.scatter(p["cost"], p["quality"], s=size, facecolor=face,
                   edgecolor=edge, linewidth=2, zorder=3)
        label_color = INK if role == "story" else INK_2
        weight = "semibold" if role == "story" else "normal"
        ax.annotate(p["label"], (p["cost"], p["quality"]),
                    textcoords="offset points", xytext=(p["dx"], p["dy"]),
                    ha=p["ha"], fontsize=8.5, color=label_color,
                    fontweight=weight, linespacing=1.2)

    ax.set_xscale("log")
    ax.set_xlabel(spec["xlabel"], fontsize=9.5)
    ax.set_ylabel(spec["ylabel"], fontsize=9.5)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:g}"))
    ax.grid(True, which="major", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=8.5, length=0)

    _title_block(fig, spec["title"], spec["subtitle"])
    _footnote(fig, spec["footnote"])
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def draw_annual_cost_bars(spec, out_path):
    bars = spec["bars"]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    fig.subplots_adjust(top=0.76, bottom=0.24, left=0.30, right=0.94)

    ys = range(len(bars))
    for y, b in zip(ys, bars):
        color = STORY if b["role"] == "story" else DEEMPH
        ax.barh(y, b["value"], height=0.3, color=color, zorder=3)
        ax.text(b["value"] + max(x["value"] for x in bars) * 0.012, y,
                f"${b['value']:,}", va="center", ha="left", fontsize=9.5,
                fontweight="semibold" if b["role"] == "story" else "normal",
                color=INK if b["role"] == "story" else INK_2)

    ax.set_yticks(list(ys))
    ax.set_yticklabels([b["label"] for b in bars], fontsize=9.5, color=INK_2)
    ax.invert_yaxis()
    ax.set_xlabel(spec["xlabel"], fontsize=9.5)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.grid(True, axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=8.5, length=0)

    _title_block(fig, spec["title"], spec["subtitle"])
    _footnote(fig, spec["footnote"])
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def draw_paired_bars(spec, out_path):
    """Two side-by-side count panels sharing one y scale."""
    panels = spec["panels"]
    fig, axes = plt.subplots(1, len(panels), figsize=(7.2, 3.9))
    fig.subplots_adjust(top=0.70, bottom=0.30, left=0.08, right=0.97, wspace=0.32)

    for ax, panel in zip(axes, panels):
        bars = panel["bars"]
        xs = range(len(bars))
        for x, b in zip(xs, bars):
            color = STORY if b["role"] == "story" else DEEMPH
            ax.bar(x, b["value"], width=0.52, color=color, zorder=3)
            ax.text(x, b["value"] + spec["ymax"] * 0.035, str(b["value"]),
                    ha="center", va="bottom", fontsize=13, fontweight="bold",
                    color=INK if b["role"] == "story" else INK_2)
        ax.set_xticks(list(xs))
        ax.set_xticklabels([b["label"] + (" " + b["marker"] if b.get("marker") else "")
                            for b in bars], fontsize=8, color=INK_2)
        ax.set_ylim(0, spec["ymax"])
        ax.set_title(f"{panel['heading']}\n{panel['ylabel']}", fontsize=9,
                     color=INK_2, pad=10)
        ax.grid(True, axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.tick_params(labelsize=8, length=0)
        ax.text(0.5, -0.30, panel["caption"], transform=ax.transAxes, ha="center",
                va="top", fontsize=7, style="italic", color=MUTED)

    _title_block(fig, spec["title"], spec["subtitle"])
    _footnote(fig, spec["footnote"])
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


RENDERERS = {
    "pass_matrix": draw_pass_matrix,
    "cost_quality_scatter": draw_cost_quality_scatter,
    "annual_cost_bars": draw_annual_cost_bars,
    "paired_bars": draw_paired_bars,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", required=True, help="directory of figure spec *.json files")
    ap.add_argument("--out-dir", required=True, help="directory to write PNGs into")
    args = ap.parse_args()

    data_dir, out_dir = Path(args.data_dir), Path(args.out_dir)
    specs = sorted(data_dir.glob("*.json"))
    if not specs:
        sys.exit(f"no *.json specs found in {data_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    for spec_path in specs:
        spec = json.loads(spec_path.read_text())
        renderer = RENDERERS.get(spec["type"])
        if renderer is None:
            sys.exit(f"{spec_path.name}: unknown figure type {spec['type']!r}")
        out_path = out_dir / spec["output"]
        renderer(spec, out_path)
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
