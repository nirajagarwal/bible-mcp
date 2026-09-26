"""Chunk 7 (final) of the post-NT-expansion weight>=10 batch (indices 1200-1458)."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-nt-w10.json")))
OFFSET = 1200
END = 1459  # exclusive; batch has 1459 total pairs, this chunk covers the tail

UPGRADES = {
    1211: ("part_of:a", "Exod 28:22-28 describes the breastplate being bound to the ephod with gold chains and rings — a specific attached component of the ephod, not a coordinate topic."),
    1213: ("part_of:a", "Lev 16:13, the cited evidence's target verse, has the censer's incense cloud cover the mercy seat so the officiant does not die — the censer is the instrument that makes the Day-of-Atonement propitiation ritual possible, matching the established sacrificial-material/instrument pattern."),
    1228: ("narrower:a", "Song 5:14/Isa 54:11 list beryl among precious stones — a specific type within the broader precious-stones category, matching the established Sapphire/Precious-stone pattern."),
    1233: ("narrower:a", "Exod 30:34's incense-spice list and Song 3:6's 'perfumed with... frankincense' treat frankincense as a specific aromatic substance within the broader perfumes category."),
    1234: ("narrower:b", "John 12:3, the cited evidence's target verse, names spikenard specifically as 'ointment of spikenard' — a specific type of perfume, not a coordinate topic."),
    1235: ("part_of:b", "Eph 6:17 ('the sword of the Spirit') lists the sword alongside breastplate, shield, and helmet as one piece of the armor of God — a component, not a coordinate topic."),
    1240: ("narrower:b", "Lev 1:14/Luke 2:24 both use turtledoves as an offering species — a specific type of bird, matching the established specific-type pattern."),
    1245: ("symbol_of:a", "Heb 9:12-15, the cited evidence itself, draws an explicit typological contrast between the goat's blood (annual atonement) and Christ's own blood (eternal redemption) — the goat sacrifice prefigures Christ's atoning death, matching the established sacrificial-typology pattern."),
    1248: ("narrower:a", "Lev 13:2's diagnostic law and Deut 28:27's plague list both treat leprosy as one recognized type of plague/disease, not a coordinate topic."),
    1260: ("narrower:b", "Isa 8:20's 'law and testimony' (Law generally) and the Mosaic law of Ps 19:7 stand in a general/specific relationship — the Law of Moses is a specific historical instance of Law generally, matching the established Temple/Solomon's-Temple pattern."),
    1266: ("symbol_of:a", "Rom 9:21, the cited evidence's own source verse ('Hath not the potter power over the clay...'), uses the potter/clay image as Paul's explicit illustration for God's sovereign predestining choice in that same chapter."),
    1268: ("fulfills:a", "Deut 18:15's promise of a coming prophet 'like unto me' is applied to Christ in the NT (cf. Acts 3:22, Acts 7:37) — Christ fulfills the specific office of 'the Prophet' foretold in Deuteronomy."),
    1303: ("narrower:b", "Isa 28:28/Matt 3:12 both describe winnowing as a specific farming technique within the broader category of agriculture."),
    1310: ("part_of:b", "Rom 1:7 addresses believers as 'called to be saints' within the church at Rome — saints are the members that constitute the church body, matching Paul's recurring body/member ecclesiology."),
    1317: ("symbol_of:a", "Isa 60:6's frankincense offering and the incense-as-prayer image (cf. Ps 141:2, Rev 5:8) support frankincense as a recognized biblical symbol for prayer ascending to God."),
    1322: ("narrower:a", "John 19:39's 'myrrh and aloes' and Prov 7:17's perfume list both treat aloes as a specific aromatic substance within the broader perfumes category, matching the frankincense/spikenard pattern."),
    1325: ("symbol_of:a", "Isa 51:17's 'cup of his fury' and Rev 14:10's 'cup of his indignation... tormented... for ever and ever' both use the cup image as the defining symbol of divine wrath culminating in eternal punishment, matching the established Fire/Eternal-death symbol pattern."),
    1335: ("narrower:b", "John 12:3's 'ointment of spikenard' names spikenard as a specific type of ointment, not a coordinate topic."),
    1336: ("symbol_of:a", "Matt 13:42's 'furnace of fire' is Christ's own recurring image for hell/final punishment, matching the established Fire/Eternal-death and Worm/Eternal-death symbol pattern."),
    1350: ("part_of:a", "Mark 15:46's burial account and Isa 53:9's 'made his grave with the wicked' describe the funeral/burial as one specific stage within the broader doctrine of Christ's humiliation (incarnation, suffering, death, burial), not a coordinate topic."),
    1351: ("part_of:a", "John 11:38/Matt 27:60 describe the burial as a specific stage within the broader doctrine of Christ's humiliation, matching the Funeral/Humiliation-of-Christ pattern."),
    1370: ("fulfills:a", "Mic 5:2's Bethlehem-birthplace prophecy is cited in John 7:42 ('out of the town of Bethlehem') as fulfilled specifically by Jesus."),
    1396: ("symbol_of:a", "John 3:14-15, the cited evidence's own source verse, draws Christ's explicit typological comparison: 'as Moses lifted up the serpent... so must the Son of man be lifted up... that whosoever believeth... should have eternal life' — the brazen serpent is the named symbol of the way to eternal life."),
    1397: ("symbol_of:b", "John 3:15 (fiery/brazen serpent typology, per Num 21:8-9) is the same explicit symbol for the way to eternal life referenced in the Brass/Eternal-life pattern above."),
    1403: ("causes:a", "John 3:16, the cited evidence's own source verse ('whosoever believeth in him... should... have everlasting life'), ties God's atoning gift of the Son directly to believers receiving eternal life."),
    1414: ("part_of:b", "Gal 4:4/1 Tim 3:16 describe the incarnation ('God sent forth his Son, made of a woman... God was manifest in the flesh') as the opening stage of the broader doctrine of Christ's humiliation, matching the Funeral/Burial pattern above."),
    1418: ("narrower:b", "2 Cor 12:2-4, the cited evidence's own source passage, identifies 'the third heaven' and 'paradise' as the same experience — paradise is a specific realm within heaven, not a coordinate topic."),
    1448: ("causes:b", "Col 1:21's 'alienated and enemies in your mind by wicked works, yet now hath he reconciled' directly ties sin/wicked works to the resulting need for, and act of, reconciliation."),
    1451: ("causes:a", "Eph 2:16, the cited evidence's own source verse ('reconcile both unto God in one body by the cross'), names the cross as the specific means that produces reconciliation."),
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
    for idx in range(OFFSET, END):
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
        "model": "claude-in-session (Sonnet 5) — NT-expansion chunk 7 (indices 1200-1458, final)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-nt-w10-chunk7.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
