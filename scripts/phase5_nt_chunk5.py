"""Chunk 5 of the post-NT-expansion weight>=10 batch (indices 800-999)."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-nt-w10.json")))
OFFSET = 800

UPGRADES = {
    826: ("causes:a", "Mark 3:29's 'never forgiven' and Matt 25:46's 'eternal punishment' together tie unforgiven blasphemy against the Holy Spirit directly to the fate of eternal death."),
    841: ("causes:b", "Gal 4:6, the cited evidence's own source verse, ties the adoption/sonship status directly to the Spirit's cry of 'Abba, Father' — adoption is what produces the cry."),
    908: ("narrower:a", "Gen 37:24/Jer 38:6 both show a cistern used as an improvised prison — a specific type of dungeon, not a coordinate topic."),
    937: ("narrower:a", "Exod 28:18's list of breastplate gemstones (Song 5:14's 'precious stones' framing) treats sapphire as a specific type of precious stone."),
    950: ("part_of:a", "Lev 4:24/16:15, the cited evidence itself ('slaughter the goat for the sin offering'), name the goat as the required sacrificial material of the sin-offering ritual, matching the Lamb/Burnt-offering pattern."),
    951: ("narrower:a", "Lev 8:6 ('Moses... washed them') describes ablution as a specific washing rite within the broader purification category."),
    952: ("narrower:a", "Lev 14:8-9 describe ritual bathing as a specific technique within the broader purification category, matching the Ablution/Purification pattern."),
    953: ("symbol_of:a", "Matt 5:22's 'fire of hell' names fire as the defining image of hell, matching the established Fire/Eternal-death and Worm/Eternal-death pattern."),
    957: ("causes:a", "Num 19:11, the cited evidence's target verse, states contact with a dead body causes seven days of uncleanness — the defilement is what necessitates the purification rite."),
    958: ("part_of:a", "Heb 9:13's 'blood of goats and bulls, and the ashes of a heifer' names goat-material as a component substance used in purification rites, matching the established sacrificial-material pattern."),
    960: ("causes:a", "Isa 41:14/Titus 2:14 reflect the OT kinsman-redeemer (go'el) legal role — the kinsman is the one who performs the redemption."),
    990: ("narrower:b", "Solomon's Temple is a specific historical instance of the general Temple concept 1 Cor 3:17 refers to."),
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
        "model": "claude-in-session (Sonnet 5) — NT-expansion chunk 5 (indices 800-999)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-nt-w10-chunk5.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
