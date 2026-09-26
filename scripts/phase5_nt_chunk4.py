"""Chunk 4 of the post-NT-expansion weight>=10 batch (indices 600-799)."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-nt-w10.json")))
OFFSET = 600

UPGRADES = {
    622: ("narrower:b", "Exod 25:8 uses 'sanctuary' for what becomes the tabernacle, while Ps 114:2 applies 'sanctuary' metaphorically to all of Judah — sanctuary has the broader range, tabernacle the specific physical structure."),
    623: ("part_of:a", "Exod 26:31, the cited evidence, makes the veil/doors a structural component of the tabernacle, matching the Curtain/Tabernacle and Veil/Tabernacle pattern."),
    631: ("narrower:a", "Lev 27:29's 'no person set apart for destruction may be ransomed' describes anathema (herem) as a specific, harsher subtype of consecration/devotion distinguished by its destructive outcome."),
    649: ("contrasts", "Luke 16:19-31 (the Lazarus/rich-man parable this evidence is drawn from) explicitly frames Abraham's bosom and Hades/torment as the two opposite afterlife destinations, separated by 'a great chasm.'"),
    669: ("narrower:a", "Col 3:5, the cited evidence itself, lists 'covetousness, which is idolatry' among sins to put to death — idolatry is explicitly categorized as a specific sin, not a coordinate topic."),
    707: ("part_of:a", "Heb 12:24's 'sprinkled blood' of 'the mediator of a new covenant' names blood as the defining ritual substance establishing a covenant, matching the Lamb/Passover and Bread/Passover material-component pattern."),
    740: ("narrower:b", "Exod 25:30's 'Bread of the Presence' (shewbread) is a specific ceremonial type of bread, not a coordinate topic."),
    741: ("narrower:a", "John 5:35 ('he was the burning and shining lamp') treats a lamp as a specific light-source device, a subtype of light generally."),
    754: ("causes:b", "Num 21:2's vow ('If you will indeed deliver this people... I will utterly destroy their cities') directly leads to the anathema/devoted-to-destruction outcome — the vow is what produces the anathema status."),
    762: ("narrower:b", "Gal 3:19/John 1:17 name Moses as the one 'through' whom the law was given — Moses served in a mediator role for the old covenant, a specific instance of the broader Mediator category."),
    783: ("narrower:a", "John 19:23/Mark 15:24 (the crucifixion narrative) is a specific, central event within the broader doctrine of Christ's humiliation, which also includes the incarnation and earthly suffering generally."),
    785: ("narrower:a", "Prov 23:32/Jer 8:17 use adder alongside 'snake'/'vipers' as a specific type of serpent, not a coordinate topic."),
    793: ("narrower:b", "Isa 11:1/Jer 23:5 (messianic king prophecies) describe 'the kingly office of Christ' as one of Christ's specific traditional offices (alongside prophet and priest), a specific aspect of the broader Christ concept."),
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
        "model": "claude-in-session (Sonnet 5) — NT-expansion chunk 4 (indices 600-799)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-nt-w10-chunk4.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
