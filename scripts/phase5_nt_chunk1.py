"""Chunk 1 of the post-NT-expansion weight>=10 batch (indices 0-199 of
phase5-batch-2026-09-26-nt-w10.json). Same mechanism as the OT chunk scripts.
Default verdict is 'associated' (this batch is dominated by dense generic
Reformed-soteriology cross-citation and apostle-name co-listings); only pairs
with specific, citable support for a sharper verb are upgraded."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-nt-w10.json")))

# Explicit upgrades only; every other index in range(200) defaults to associated.
UPGRADES = {
    4: ("causes:a", "Titus 2:14's own wording ('gave Himself... to redeem us') ties the ransom-payment directly to the redemption it accomplishes."),
    15: ("causes:b", "1 Cor 9:1 grounds Paul's apostleship explicitly in having seen the risen Lord ('Am I not an apostle? Have I not seen Jesus?') — witnessing the resurrection is what qualifies him."),
    19: ("narrower:a", "Heb 1:14 explicitly calls angels 'ministering spirits' — angels are a specific class of spirit-being, not a coordinate category."),
    28: ("narrower:a", "1 Cor 15 (the wider passage this verse belongs to) presents Christ's resurrection as the 'firstfruits' of the general resurrection — a specific first instance of the broader category."),
    29: ("narrower:a", "John 3:36 (in the wider passage) treats eternal life as a specific, qualified form of life, distinct from mere biological existence."),
    45: ("causes:a", "John 10:18 ('I lay it down by myself... I have power to take it again') and Acts 2:24 together reflect the kenosis-then-exaltation sequence: Christ's voluntary humiliation/death precedes and is followed by His resurrection."),
    46: ("causes:a", "Rom 5:1, the cited target verse itself, states justification is 'by faith' directly."),
    55: ("narrower:b", "1 Cor 16:1's 'collection for the saints' is explicitly an act of almsgiving — a specific named instance of the broader practice."),
    63: ("causes:b", "Acts 13:2 shows the Spirit's call ('set apart... for the work I have called them') as what constitutes Paul and Barnabas apostles for that mission."),
    64: ("narrower:b", "Ransom is one of several NT metaphors (alongside sacrifice, propitiation) for the single broader doctrine of atonement — Titus 2:14's ransom language sits within the wider atonement framework."),
    104: ("causes:a", "2 Tim 4:1 directly names Christ 'who will judge the living and the dead' 'and by His appearing' — His coming is what enacts the judgment."),
    110: ("part_of:a", "1 Cor 5:7 ('Christ our Passover lamb has been sacrificed') and Exod 12 establish the lamb as the central required component of the Passover ritual, not a coordinate topic."),
    121: ("causes:a", "Mark 12:26's own phrase 'the book of Moses' reflects the traditional attribution of the Pentateuch's authorship to Moses."),
    122: ("narrower:a", "Heb 6:2 lists Christian baptism under 'instruction about baptisms... purification' — baptism is presented as a specific purification rite, not a coordinate topic."),
    154: ("contrasts", "Dan 12:2, the cited evidence itself, states the two fates side by side as explicit opposites: 'some to everlasting life, some to shame and everlasting contempt.'"),
    157: ("narrower:a", "'Election of Grace' names grace as its own category by its very title — a specific doctrine of election that is itself grace-based, not a coordinate topic to Grace generally."),
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
    for idx in range(200):
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
                f"Dense but generic co-citation in the NT soteriological cross-reference cluster "
                f"({cite}) — no specific textual claim in the cited evidence supports a sharper verb than associated."
            )
        judgments.append(build_entry(idx, code, just))

    out = {
        "batch_file": "phase5-batch-2026-09-26-nt-w10.json",
        "model": "claude-in-session (Sonnet 5) — NT-expansion chunk 1 (indices 0-199)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-nt-w10-chunk1.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
