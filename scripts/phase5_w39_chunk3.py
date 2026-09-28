"""Chunk 3 of the weight 3-9 tier (raw indices 1000-1499, weight=8). No upgrades
found this chunk — reviewed evidence stayed generic co-citation throughout."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-28-w3-9.json")))
START, END = 1000, 1500

UPGRADES = {}


def build_entry(idx, code, just):
    p = BATCH[idx]
    a_id, b_id = p["a"]["id"], p["b"]["id"]
    entry = {"pair": [a_id, b_id], "justification": just}
    if code == "assoc":
        entry["verb"] = "associated"
    elif code == "contrasts":
        entry["verb"] = "contrasts"
    else:
        verb, side = code.split(":")
        first, second = (a_id, b_id) if side == "a" else (b_id, a_id)
        entry["verb"] = verb
        if verb == "narrower":
            entry["narrower"], entry["broader"] = first, second
        elif verb == "causes":
            entry["cause"], entry["effect"] = first, second
        elif verb == "part_of":
            entry["part"], entry["whole"] = first, second
        elif verb == "symbol_of":
            entry["symbol"], entry["symbolized"] = first, second
        elif verb == "fulfills":
            entry["fulfiller"], entry["fulfilled"] = first, second
    return entry


def main():
    judgments = []
    for idx in range(START, END):
        if idx >= len(BATCH):
            break
        if idx in UPGRADES:
            code, just = UPGRADES[idx]
            judgments.append(build_entry(idx, code, just))
            continue
        p = BATCH[idx]
        ev = p["evidence"]
        if not ev:
            cite = "no evidence recovered"
        elif ev[0]["kind"] == "shared_verse":
            cite = ev[0]["ref"]
        else:
            cite = f"{ev[0]['from_ref']}/{ev[0]['to_ref']}"
        code, just = "assoc", (
            f"Generic cross-reference-chain co-citation ({cite}) — no specific structural claim "
            f"in the cited evidence supports a sharper verb than associated."
        )
        judgments.append(build_entry(idx, code, just))

    out = {
        "batch_file": "phase5-batch-2026-09-28-w3-9.json",
        "model": "claude-in-session (Sonnet 5) — weight 3-9 tier chunk 3 (indices 1000-1499, weight=8)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-w3-9-chunk3.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
