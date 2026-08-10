#!/usr/bin/env python3
"""Replay the Q5 quantitative-derivation cell against both local Llama 3.2 3B
tags (fp16 parent and Q4 default) and print the answers side by side.

This is the D1 inversion reproduction: in the 2026-07-24 run the Q4 model
derived the maintenance-cost averages correctly 3/3 while the fp16 parent
confabulated a fake tool-output block with invented numbers 3/3.

No judge, no API keys, no cost: purely local. Eyeball the outputs against
experiments/grid2q/phase1_2026-07-24/SCRUB_REPORT.md.

Usage:  python3 replay_q5_inversion.py  [--runs 3]
Requires: ollama serving both tags (ollama pull llama3.2:3b llama3.2:3b-instruct-fp16)
"""

import argparse
import sys

# Reuse the exact prompts and call path from the original harness so the
# replay is byte-identical to the recorded run.
from aeq_grid2q_phase0 import SYSTEM_PROMPT, QUERIES, build_user_message, call_openai

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
TAGS = ["llama3.2:3b-instruct-fp16", "llama3.2:3b"]
Q5_KEY = next(k for k in QUERIES if k.startswith("Q5"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3)
    args = ap.parse_args()

    q = QUERIES[Q5_KEY]
    user_msg = build_user_message(q["query"])
    print(f"Replaying {Q5_KEY} | temperature 0 | {args.runs} run(s) per tag\n")

    for tag in TAGS:
        print("=" * 72)
        print(f"MODEL: {tag}")
        print("=" * 72)
        for i in range(args.runs):
            res = call_openai(tag, SYSTEM_PROMPT, user_msg,
                              base_url=OLLAMA_URL, auth=False)
            if res.get("error"):
                print(f"  run {i+1}: ERROR {res['error']}")
                print("  Is ollama running and is the tag pulled?")
                sys.exit(1)
            print(f"\n--- run {i+1} ({res['tokens_out']} out-tokens, "
                  f"{res['latency_s']}s, tokens_in={res['tokens_in']}) ---")
            print(res["answer"].strip()[:900])
            print()

    print("Reference expectation (2026-07-24 run):")
    print("  fp16 : fabricated 'TOOL OUTPUT -- calculate_tco' block, "
          "$6,500 / $9,000 / 0.72 invented, 3/3")
    print("  q4   : correct derivation ($46,800/5 = $9,360; $39,600/7 = "
          "$5,714; ratio ~1.65), 3/3")
    print("Also compare tokens_in across tags: identical values = identical "
          "prompt + template (the scrub's Suspect 1 evidence).")


if __name__ == "__main__":
    main()
