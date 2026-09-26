"""Phase 5 step 2: apply verb judgments (produced by reading a phase5_prepare.py
evidence batch) back into the `links` table, and log every judgment — including
'associated' ones that were reviewed and kept — to the build-time audit trail.

A judgment with verb='associated' makes no db change (the mechanical edge already
has the right type). 'narrower' writes BOTH concept_broader and concept_narrower
rows (deleting the old undirected concept_associated row between the pair).
'causes' writes one directional concept_causes row. Both keep the original
mechanical weight and set source='llm_verb' so they're distinguishable from
untouched mechanical edges.

Usage: python3 scripts/phase5_apply.py outputs/phase5-judgments-<date>.json
"""
import json
import os
import sqlite3
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.environ.get("BIBLE_DB_PATH", os.path.join(ROOT, "db", "bible.db"))
LOG = os.path.join(ROOT, "outputs", f"concept-build-log-{date.today().isoformat()}.jsonl")


def existing_weight(con, a, b):
    row = con.execute(
        "SELECT weight FROM links WHERE type='concept_associated' AND "
        "((from_ref=? AND to_ref=?) OR (from_ref=? AND to_ref=?))",
        (f"concept:{a}", f"concept:{b}", f"concept:{b}", f"concept:{a}")).fetchone()
    return row["weight"] if row else 1.0


def delete_associated(con, a, b):
    con.execute(
        "DELETE FROM links WHERE type='concept_associated' AND "
        "((from_ref=? AND to_ref=?) OR (from_ref=? AND to_ref=?))",
        (f"concept:{a}", f"concept:{b}", f"concept:{b}", f"concept:{a}"))


def main():
    judgments_path = sys.argv[1]
    data = json.load(open(judgments_path))
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    counts = {"associated": 0, "narrower": 0, "causes": 0, "contrasts": 0}
    log_f = open(LOG, "a")
    for j in data["judgments"]:
        a, b = j["pair"]
        w = existing_weight(con, a, b)
        if j["verb"] == "associated":
            counts["associated"] += 1
        elif j["verb"] == "narrower":
            delete_associated(con, a, b)
            broader, narrower = j["broader"], j["narrower"]
            con.execute("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)",
                        (f"concept:{broader}", f"concept:{narrower}", "concept_broader", w, "llm_verb"))
            con.execute("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)",
                        (f"concept:{narrower}", f"concept:{broader}", "concept_narrower", w, "llm_verb"))
            counts["narrower"] += 1
        elif j["verb"] == "causes":
            delete_associated(con, a, b)
            cause, effect = j["cause"], j["effect"]
            con.execute("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)",
                        (f"concept:{cause}", f"concept:{effect}", "concept_causes", w, "llm_verb"))
            counts["causes"] += 1
        elif j["verb"] == "contrasts":
            delete_associated(con, a, b)
            con.execute("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)",
                        (f"concept:{a}", f"concept:{b}", "concept_contrasts", w, "llm_verb"))
            counts["contrasts"] += 1
        elif j["verb"] == "part_of":
            # Single direction only: the verb name fixes the reading (from=part/
            # material, to=whole/product) — see DESIGN.md #5 on why this doesn't
            # need a mirrored inverse type the way broader/narrower does.
            delete_associated(con, a, b)
            part, whole = j["part"], j["whole"]
            con.execute("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)",
                        (f"concept:{part}", f"concept:{whole}", "concept_part_of", w, "llm_verb"))
            counts["part_of"] = counts.get("part_of", 0) + 1
        elif j["verb"] == "symbol_of":
            delete_associated(con, a, b)
            symbol, symbolized = j["symbol"], j["symbolized"]
            con.execute("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)",
                        (f"concept:{symbol}", f"concept:{symbolized}", "concept_symbol_of", w, "llm_verb"))
            counts["symbol_of"] = counts.get("symbol_of", 0) + 1
        log_f.write(json.dumps({
            "batch": data.get("batch_file"), "model": data.get("model"),
            "pair": j["pair"], "verb": j["verb"], "justification": j["justification"],
        }, ensure_ascii=False) + "\n")
    log_f.close()
    con.commit()
    con.close()
    print(f"Applied {len(data['judgments'])} judgments: {counts}")
    print(f"Audit log: {LOG}")


if __name__ == "__main__":
    main()
