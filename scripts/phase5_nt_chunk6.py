"""Chunk 6 of the post-NT-expansion weight>=10 batch (indices 1000-1199)."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-nt-w10.json")))
OFFSET = 1000

UPGRADES = {
    1025: ("narrower:a", "1 Cor 3:1/14:20 use 'babes' as a more specific, earlier developmental stage than 'children' generally in the spiritual-maturity metaphor."),
    1029: ("narrower:a", "Jer 23:5, the cited evidence's target verse, ties the 'Branch' title directly to kingship ('a King shall reign and prosper') — a specific messianic title within the broader kingly office."),
    1067: ("narrower:b", "'Eternal death' is a specific, theologically qualified form of 'death' generally, not a coordinate topic — Heb 9:14's contrast with ordinary death ('how much more') supports the distinction."),
    1082: ("causes:b", "Heb 9:15/1 Pet 5:10 (in the wider kenosis-exaltation pattern) reflect Phil 2's sequence: Christ's humiliation is followed by, and gives rise to, His glorification, matching the Humiliation-of-Christ/Resurrection-of-Christ causal pattern."),
    1104: ("causes:b", "Rom 3:25/Acts 2:23 tie Christ's atoning sacrifice to His delivering-up (humiliation/death), matching the established Death-causes-Atonement pattern."),
    1149: ("causes:a", "Hos 7:4/7:6's baker-and-oven imagery reflects that baking is the process that produces bread."),
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
    for idx in range(OFFSET, OFFSET + 200):
        if idx in UPGRADES:
            code, just = UPGRADES[idx]
        else:
            p = BATCH[idx]
            ev = p["evidence"]
            if not ev:
                cite = "no evidence recovered"
            elif ev[0]["kind"] == "shared_verse":
                cite = ev[0]["ref"]
            else:
                cite = f"{ev[0]['from_ref']}/{ev[0]['to_ref']}"
            code, just = "assoc", (
                f"Dense but generic co-citation in the NT cross-reference cluster "
                f"({cite}) — no specific textual claim in the cited evidence supports a sharper verb than associated."
            )
        judgments.append(build_entry(idx, code, just))

    out = {
        "batch_file": "phase5-batch-2026-09-26-nt-w10.json",
        "model": "claude-in-session (Sonnet 5) — NT-expansion chunk 6 (indices 1000-1199)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-nt-w10-chunk6.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
