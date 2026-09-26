"""Chunk 3 of the post-NT-expansion weight>=10 batch (indices 400-599).

Index 586 (Ransom<->Redemption, w=13) is a stale intra-batch duplicate of index 4
(w=52, already judged 'causes' in chunk 1) — Phase 4's candidate generation can
emit one row per (method, pair), so the same pair can appear twice in one static
batch file at different weights (same class of issue as Deuteronomy/Pentateuch in
the OT run). Kept as a no-op 'associated' here rather than re-inserting a
redundant edge."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-nt-w10.json")))
OFFSET = 400

UPGRADES = {
    413: ("causes:a", "Rom 5:1/5:10-11, the passage this evidence is drawn from, moves directly from 'having been justified' to 'we have now received the reconciliation' as its consequence."),
    434: ("causes:b", "Acts 7:58 shows the witnesses laying down their garments to carry out the stoning of Stephen — witnesses are the ones who initiate/perform the execution, per the legal tradition (Deut 17:7) this reflects."),
    447: ("narrower:a", "Isa 60:1/Mal 4:2 ('the sun of righteousness') present dayspring/dawn as a specific image of light, not a coordinate topic."),
    461: ("contrasts", "Matt 5:29/18:9, the cited evidence itself, use the explicit 'better to enter life... than to be thrown into Gehenna' framing — a direct textual opposition between the two fates."),
    490: ("causes:a", "Num 18:12 ('the freshest olive oil and finest wheat... firstfruits') and the wider agricultural-offering pattern support agriculture as what produces fruit/crops, matching the Agriculture-produces-X pattern."),
    491: ("narrower:a", "Heb 11:4, the cited evidence's target verse, explicitly calls Abel's lamb offering 'a better sacrifice' — a specific sacrificial material, not a coordinate topic."),
    498: ("symbol_of:b", "Matt 13:42's 'fiery furnace' is used as a direct image of the fate of eternal punishment, matching the Worm/Brimstone-symbol_of-Eternal-death pattern."),
    505: ("part_of:a", "Deut 16:3 makes unleavened bread a required component of Passover observance ('you must not eat leavened bread with it')."),
    508: ("symbol_of:a", "Isa 60:1 ('your light has come, and the glory of the LORD has risen') and Exod 29:43 extend the established Cloud/Shechinah pattern directly to Cloud as the visible form Glory takes."),
    509: ("part_of:b", "Heb 9:4, the cited evidence's own text, states the ark contained 'the tablets of the covenant' — the Ten Commandments are a physical component stored inside the ark."),
    512: ("part_of:a", "Lev 23:36 specifies a solemn assembly on the eighth day as a required element of the Feast of Tabernacles' observance."),
    515: ("part_of:a", "Exod 25:22/30:6, per Heb 9:5's conflation of the mercy seat with 'the place of propitiation,' establish the ark as the furniture the propitiation-site is built upon, matching the Cherub/Propitiation pattern."),
    517: ("part_of:a", "Exod 26:1/26:31 (cherubim worked into the tabernacle's fabric) extend the established Cherub/Curtain material pattern directly to the veil."),
    518: ("part_of:b", "2 Chr 3:14/Matt 27:51 name the veil as a woven component of Solomon's temple, matching the established temple-furnishing part_of pattern."),
    531: ("causes:b", "Acts 3:22, the cited evidence's own source verse ('Moses indeed said...'), reflects the traditional attribution of Deuteronomy's authorship to Moses, matching the Moses/Pentateuch pattern."),
    552: ("narrower:b", "John 5:46 ('if you believed Moses...he wrote of me') treats the Pentateuch (the writings of Moses) as one part of the wider body later called 'the Bible,' matching the Pentateuch/Scripture pattern."),
    578: ("causes:a", "John 3:16/Rom 5:10 present God's atoning love in Christ as what accomplishes reconciliation, completing the atonement-effects causal chain already established for Propitiation/Reconciliation."),
    586: ("assoc", "Stale duplicate of the pair already judged 'causes' in chunk 1 (from its higher-weight occurrence) — kept as a no-op associated rather than re-inserting a redundant edge; see module docstring."),
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
        "model": "claude-in-session (Sonnet 5) — NT-expansion chunk 3 (indices 400-599)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-nt-w10-chunk3.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments ({len(UPGRADES)} upgraded) to {out_path}")


if __name__ == "__main__":
    main()
