"""Compact reviewer view for a phase5_prepare.py batch — one dense line per pair
(index, weight, both labels, one truncated evidence snippet) instead of the full
indented JSON, to keep review token cost tractable at 24K-pair scale. Pairs with
no recoverable evidence are skipped entirely by default (they're auto-'associated'
per the no-evidence-no-upgrade rule — nothing to review), unless --all is passed.

Usage: python3 scripts/phase5_view.py <batch.json> <start> <end> [--all] [--full]
  --all   include no-evidence pairs too (normally skipped)
  --full  print full evidence text per pair instead of the one-line form
"""
import json
import sys

path, start, end = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
show_all = "--all" in sys.argv
full = "--full" in sys.argv
batch = json.load(open(path))


def snippet(ev, n=90):
    if not ev:
        return "(no evidence)"
    e = ev[0]
    if e["kind"] == "shared_verse":
        t = e["text"]
    else:
        t = f"{e['from_text']} || {e['to_text']}"
    t = t.replace("\n", " ").strip()
    return (t[:n] + "…") if len(t) > n else t


for i in range(start, min(end, len(batch))):
    p = batch[i]
    if not p["evidence"] and not show_all:
        continue
    a, b = p["a"], p["b"]
    if full:
        adef = (a["definition"] or "").split("(", 1)[0].strip()[:100]
        bdef = (b["definition"] or "").split("(", 1)[0].strip()[:100]
        print(f"[{i}] w={p['weight']:g} {a['label']!r}({a['id']}) <-> {b['label']!r}({b['id']})")
        print(f"    A: {adef}")
        print(f"    B: {bdef}")
        for ev in p["evidence"]:
            if ev["kind"] == "shared_verse":
                print(f"    EV shared_verse [{ev['ref']}]: {ev['text']}")
            else:
                print(f"    EV xref [{ev['from_ref']}]: {ev['from_text']}")
                print(f"       -> [{ev['to_ref']}]: {ev['to_text']}")
        print()
    else:
        print(f"[{i}] w={p['weight']:g} {a['label']}({a['id']}) <-> {b['label']}({b['id']}) | {snippet(p['evidence'])}")
