"""Chunk 2 of the post-NT-expansion weight>=10 batch (indices 200-399)."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-nt-w10.json")))
OFFSET = 200

UPGRADES = {
    201: ("narrower:b", "Mark 9:43/9:45 use Gehenna ('hell') directly as the destination of the eternal-punishment fate — a specific named instance, not a coordinate topic."),
    216: ("causes:b", "1 Cor 6:11's sequence ('washed, sanctified, justified') presents sanctification as the process that produces the state of holiness."),
    219: ("causes:b", "Rev 20:11-15 (the great-white-throne judgment scene) directly precedes and enacts the 'second death' — the final judgment is what pronounces the sentence of eternal death."),
    238: ("narrower:a", "Jas 5:16, the cited evidence's own source verse, coins 'effectual fervent prayer' as a specific quality of prayer, not a coordinate topic."),
    241: ("causes:b", "Rom 8:32/1 John 4:9 tie Christ's death (God 'gave Him up for us all') directly to the atoning act — the death is what accomplishes the atonement."),
    274: ("symbol_of:b", "Rev 21:23, the cited evidence itself, states 'the glory of God gives it light' — light is the visible form glory takes, matching the Cloud/Shechinah pattern."),
    277: ("narrower:b", "1 Cor 10:10's 'destroyer' references the destroying-angel tradition (Exod 12:23) — a specific named role within the broader angel category."),
    282: ("narrower:a", "The word 'martyr' derives directly from Greek martys, 'witness' — a martyr is specifically one who witnesses even unto death, a subtype of witness generally."),
    285: ("part_of:a", "1 Cor 10:16 ('the cup of blessing... a participation in the blood of Christ') names the cup as the central, required ritual element of the Lord's Supper."),
    286: ("symbol_of:b", "Isa 66:24, the cited evidence's target verse, uses the undying worm as the canonical image representing eternal punishment's unending nature."),
    287: ("symbol_of:a", "Matt 25:41's 'eternal fire' and Isa 30:33's Topheth imagery use brimstone/fire as the visible representation of the fate of eternal death, matching the Worm/Eternal-death pattern."),
    296: ("narrower:a", "Luke 3:1 names Herod (Antipas) as tetrarch of Galilee — a specific person holding that office, not a coordinate topic."),
    297: ("narrower:a", "Luke 3:1 names Philip as tetrarch of Ituraea — a specific person holding that office, matching the Antipas/Tetrarch pattern."),
    301: ("causes:b", "1 John 2:3 ('by this we can be sure that we have come to know Him') presents assurance as a certainty that arises from faith/obedience, matching the Faith-produces-X pattern already used for Faith/Justification."),
    305: ("narrower:a", "Col 3:5's 'evil desire' (concupiscence, the KJV term) is a specific named form of sinful inclination, not a coordinate topic to sin generally."),
    311: ("part_of:a", "Heb 9:5 explicitly conflates the cherubim overshadowing the mercy seat with 'the place of propitiation' — the cherubim are a structural element of the propitiation-site, matching the established Cherub/Mercy-seat pattern."),
    312: ("part_of:b", "Exod 29:38 names lambs as the required material offered daily on the altar — a specific material component of the burnt-offering ritual, matching the Wine/Drink-offering pattern."),
    315: ("fulfills:a", "Deut 18:15, the cited evidence's own source verse, is Moses' own prophecy of a coming prophet like himself — the traditional messianic reading Christ is understood to fulfill."),
    233: ("narrower:a", "Acts 2:21/Joel 2:32 ('calls on the name of the Lord') describe calling as a specific act of invocation/prayer, not a coordinate topic."),
    347: ("causes:a", "Heb 2:17 ('make propitiation for sins') and Col 1:21 ('once alienated... now reconciled') present propitiation as the act that accomplishes reconciliation."),
    365: ("narrower:b", "Propitiation is one of several specific NT mechanisms/metaphors (alongside ransom) for the single broader atonement doctrine, matching the Ransom/Atonement pattern from chunk 1."),
    366: ("causes:b", "Rom 3:25's own wording ('presented Him as a propitiation... to demonstrate His righteousness') ties propitiation directly to the righteousness/justification it establishes."),
    397: ("narrower:a", "John 5:47/Luke 16:31 treat 'the writings of Moses' (the Pentateuch) as one part of the wider body of Scripture referenced alongside 'the prophets.'"),
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
        "model": "claude-in-session (Sonnet 5) — NT-expansion chunk 2 (indices 200-399)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-nt-w10-chunk2.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
