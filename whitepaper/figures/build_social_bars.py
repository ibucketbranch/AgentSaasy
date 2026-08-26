#!/usr/bin/env python3
"""Render a social-format horizontal bar chart from a figure spec JSON.

Brand-palette companion to build_figures.py, sized for LinkedIn/X rather than
the paper. Reads the same spec files; nothing instance-specific is baked in.

Bar coloring is derived from the spec, not hardcoded:
  role == "story"          -> cyan accent (the point being made)
  highest value in the set -> vermilion accent (the thing being compared against)
  everything else          -> recessive slate

The two headline lines follow the same rule so the type never contradicts the
bars: the top line takes the vermilion (comparison) accent and the bottom line
takes the cyan (story) accent. Pass them in that order.

Palette note: the two accents are the published brand pair. They pass CVD
separation (14.8 deutan), normal-vision separation (29.6), chroma floor, and
contrast vs the dark surface. They sit outside the validator's dark-mode
lightness band; kept anyway for consistency with the already-published figures,
with every bar directly labeled so identity is never carried by color alone.

Usage:
  python build_social_bars.py --data DATA.json --out OUT.png \
      --eyebrow "TEXT" --headline-top "TEXT" --headline-bot "TEXT"

Requires: Google Chrome (headless) for the HTML -> PNG step.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SURFACE = "#0E1620"
CYAN = "#3FD0C9"      # story accent
VERMILION = "#E86A5C"  # comparison accent
SLATE = "#4A5A6E"      # recessive
INK = "#E8EEF2"
INK_MUTED = "#8FA3B8"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def format_value(v, fmt):
    """Value formatting is a property of the data, not of this renderer.

    It was hardcoded to dollars because the first spec through here was an annual
    cost chart. A token-count spec then rendered "$869", which is the shape of
    baked-in instance value Michael's standing rule forbids. Passed in now.
    """
    if fmt == "money":
        return f"${v:,.0f}"
    if fmt == "count":
        return f"{v:,.0f}"
    raise SystemExit(f"unknown value format {fmt!r}; use money or count")


def build_html(spec, eyebrow, top, bot, value_format, callout, callout_label):
    """callout is the counterweight number.

    A card gets screenshotted without its post. This one says the wasteful build
    used fewer output tokens, which is true and, alone, misleading: it still cost
    more in total. Post 1's card carried its own counterweight as the big 4.68x.
    Anything stated on a card that a reader could take the wrong way needs the
    correction on the same card, not in the body copy.
    """
    bars = spec["bars"]
    callout_html = ""
    if callout:
        callout_html = (
            f'<div class="callout"><div class="clab">{callout_label}</div>'
            f'<div class="cval">{callout}</div></div>')
    peak = max(b["value"] for b in bars)

    rows = []
    for b in bars:
        if b.get("role") == "story":
            color = CYAN
        elif b["value"] == peak:
            color = VERMILION
        else:
            color = SLATE
        pct = b["value"] / peak * 100
        rows.append(f"""
      <div class="row">
        <div class="lab">{b['label']}</div>
        <div class="track"><div class="bar" style="width:{pct:.2f}%;background:{color}"></div></div>
        <div class="val">{format_value(b['value'], value_format)}</div>
      </div>""")

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:2400px; height:1350px; background:{SURFACE};
    background-image:radial-gradient(ellipse at 20% 0%, #16212E 0%, {SURFACE} 60%);
    font-family:'Inter','Helvetica Neue',Arial,sans-serif; color:{INK};
    padding:100px 130px; display:flex; flex-direction:column; }}
  .eyebrow {{ font-family:'SF Mono',Menlo,monospace; font-size:30px; letter-spacing:.34em;
    color:{INK_MUTED}; text-transform:uppercase; margin-bottom:52px; }}
  .eyebrow b {{ color:{CYAN}; font-weight:600; }}
  h1 {{ font-size:104px; line-height:1.1; font-weight:700; letter-spacing:-.02em; }}
  h1 .c {{ color:{CYAN}; }}
  h1 .v {{ color:{VERMILION}; }}
  .chart {{ margin-top:76px; margin-bottom:auto; }}
  .row {{ display:flex; align-items:center; margin:40px 0; }}
  .lab {{ width:620px; text-align:right; padding-right:44px; font-size:40px; font-weight:600; }}
  .track {{ flex:1; height:74px; display:flex; align-items:center; }}
  .bar {{ height:100%; border-radius:0 8px 8px 0; }}
  .val {{ width:280px; padding-left:36px; font-size:44px; font-weight:700; }}
  .callout {{ position:absolute; right:120px; top:880px; text-align:right; }}
  .clab {{ font-family:ui-monospace,monospace; font-size:30px; letter-spacing:.14em;
           color:{INK_MUTED}; text-transform:uppercase; }}
  .cval {{ font-size:150px; font-weight:700; color:{VERMILION}; line-height:1.05; }}
  footer {{ border-top:1px solid #22303F; padding-top:34px; display:flex;
    justify-content:space-between; font-family:'SF Mono',Menlo,monospace;
    font-size:25px; color:{INK_MUTED}; letter-spacing:.05em; }}
</style></head><body>
  <div class="eyebrow">{eyebrow}</div>
  <h1><span class="v">{top}</span><br><span class="c">{bot}</span></h1>
  <div class="chart">{''.join(rows)}</div>
  {callout_html}
  <footer><span>{spec['subtitle']}</span><span>bucketbranch.ai</span></footer>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="figure spec JSON")
    ap.add_argument("--out", required=True, help="output PNG path")
    ap.add_argument("--eyebrow", required=True, help="kicker line; wrap a word in <b> to accent it")
    ap.add_argument("--headline-top", required=True)
    ap.add_argument("--headline-bot", required=True)
    ap.add_argument("--callout", default="",
                    help="counterweight figure shown large, e.g. 1.75x. Optional, but "
                         "supply it whenever the headline alone could mislead a reader "
                         "who sees the card without the post.")
    ap.add_argument("--callout-label", default="",
                    help="small uppercase label above the callout")
    ap.add_argument("--value-format", required=True, choices=("money", "count"),
                    help="how bar values are rendered. Required, no default: this "
                         "renderer used to assume dollars and silently mislabeled a "
                         "token-count spec.")
    a = ap.parse_args()

    if not Path(CHROME).exists():
        sys.exit(f"[ERROR] Chrome not found at {CHROME}")

    spec = json.loads(Path(a.data).read_text())
    html = build_html(spec, a.eyebrow, a.headline_top, a.headline_bot, a.value_format,
                      a.callout, a.callout_label)

    with tempfile.TemporaryDirectory() as td:
        page = Path(td) / "chart.html"
        page.write_text(html)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=2400,1350", "--default-background-color=00000000",
                        f"--screenshot={a.out}", f"file://{page}"],
                       check=True, capture_output=True)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
