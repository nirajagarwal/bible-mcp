"""Chunk 1 of the weight 3-9 tier (raw indices 0-499 of
phase5-batch-2026-09-28-w3-9.json, all weight=9). Same mechanism as prior chunk
scripts. Default verdict is 'associated' (this tier is dominated by generic
cross-reference-chain co-citation with only 1-3 evidence items, much thinner
than the weight>=10 tier); only pairs with an explicit, literally-quoted
structural claim in the cited evidence are upgraded."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-28-w3-9.json")))
START, END = 0, 500

UPGRADES = {
    0: ("causes:b", "Rev 4:11, the cited evidence itself, states existence and creation flow from God's will/sovereignty ('by Your will they exist and were created')."),
    9: ("narrower:b", "Lev 23:3, the cited evidence, opens the chapter listing Israel's appointed feasts and explicitly names the Sabbath first among them ('these are my appointed feasts') — Sabbath is a specific instance of the religious-festival calendar, not a coordinate topic."),
    15: ("part_of:b", "Rev 2:7, the cited evidence itself, places the tree of life explicitly inside Paradise ('the tree of life, which is in the Paradise of my God')."),
    158: ("narrower:a", "The cited evidence (Exod 13:2-ish 'set apart to Yahweh all that opens the womb, and every firstborn') is literally the law of firstborn redemption — a specific named practice within the broader theological category of Redemption, not a coordinate topic."),
    223: ("causes:b", "The cited evidence directly describes the manufacturing act ('fashioned it with an engraving tool, and made it a molded calf') — the graving/engraving process is what produces the golden calf."),
    237: ("symbol_of:a", "The cited evidence (Heb 9:19-context, blood of goats used in the Mosaic covenant-ratification/atonement ritual) reflects the standard NT typological reading of the OT sacrificial goat as prefiguring Christ's atoning intercession — same pattern as the already-established Lamb/Cloud/Fire symbol_of edges."),
    464: ("causes:a", "Rom 3:25, the cited evidence itself, names the atoning sacrifice (propitiation) as the mechanism God presented 'through faith in His blood' by which redemption/justification is accomplished — propitiation is presented as what effects redemption, not a coordinate topic."),
}


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
        "model": "claude-in-session (Sonnet 5) — weight 3-9 tier chunk 1 (indices 0-499, all weight=9)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-w3-9-chunk1.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
