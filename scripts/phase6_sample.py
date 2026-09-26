"""Phase 6: build a stratified random sample of Phase 5's typed (non-associated)
edges for independent validation, re-fetching evidence fresh from the db rather
than trusting the stored justification text.

Usage: python3 scripts/phase6_sample.py
Output: outputs/phase6-sample-<date>.json
"""
import json
import os
import random
import sqlite3
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.environ.get("BIBLE_DB_PATH", os.path.join(ROOT, "db", "bible.db"))
LOG_FILES = [os.path.join(ROOT, "outputs", "concept-build-log-2026-09-26.jsonl")]

SAMPLE_SIZES = {"narrower": 15, "causes": 10, "part_of": 12, "symbol_of": 2, "contrasts": 1}
random.seed(42)


def verse_text(con, ref):
    row = con.execute(
        "SELECT text FROM passages WHERE doc_id='BSB' AND ref=? UNION "
        "SELECT text FROM passages WHERE doc_id='WEB' AND ref=? LIMIT 1", (ref, ref)).fetchone()
    return row["text"] if row else None


def fresh_evidence(con, a_id, b_id, limit=3):
    a_refs = {r["ref"] for r in con.execute(
        "SELECT ref FROM concept_mentions WHERE concept_id=?", (a_id,)).fetchall()}
    b_refs = {r["ref"] for r in con.execute(
        "SELECT ref FROM concept_mentions WHERE concept_id=?", (b_id,)).fetchall()}
    shared = sorted(a_refs & b_refs)[:limit]
    ev = [{"ref": r, "text": verse_text(con, r)} for r in shared if verse_text(con, r)]
    if ev:
        return {"kind": "shared_verse", "items": ev}
    # try cross-reference chain in either direction
    rows = con.execute(
        "SELECT DISTINCT cm.ref AS src, l.to_ref AS target FROM concept_mentions cm "
        "JOIN links l ON l.from_ref = cm.ref AND l.type='cross_reference' "
        "WHERE cm.concept_id=?", (a_id,)).fetchall()
    out = []
    for r in rows:
        if r["target"] in b_refs:
            out.append({"from_ref": r["src"], "from_text": verse_text(con, r["src"]),
                        "to_ref": r["target"], "to_text": verse_text(con, r["target"])})
        if len(out) >= limit:
            break
    if out:
        return {"kind": "cross_reference", "items": out}
    return {"kind": "none", "items": []}


def main():
    log = []
    for path in LOG_FILES:
        log.extend(json.loads(l) for l in open(path) if l.strip())
    by_verb = defaultdict(list)
    for r in log:
        if r["verb"] != "associated":
            by_verb[r["verb"]].append(r)

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    sample = []
    for verb, n in SAMPLE_SIZES.items():
        pool = by_verb.get(verb, [])
        picked = random.sample(pool, min(n, len(pool)))
        for rec in picked:
            a_id, b_id = rec["pair"]
            ca = con.execute("SELECT id,label,definition FROM concepts WHERE id=?", (a_id,)).fetchone()
            cb = con.execute("SELECT id,label,definition FROM concepts WHERE id=?", (b_id,)).fetchone()
            # find the actual stored edge(s) for this pair (any concept_* type except associated)
            edges = con.execute(
                "SELECT from_ref,to_ref,type,weight FROM links WHERE type LIKE 'concept_%' "
                "AND type != 'concept_associated' AND type != 'concept_instance_of' AND type != 'concept_derived_from' "
                "AND ((from_ref=? AND to_ref=?) OR (from_ref=? AND to_ref=?))",
                (f"concept:{a_id}", f"concept:{b_id}", f"concept:{b_id}", f"concept:{a_id}")).fetchall()
            sample.append({
                "verb_claimed": verb,
                "original_justification": rec["justification"],
                "a": {"id": ca["id"], "label": ca["label"], "definition": (ca["definition"] or "")[:400]} if ca else None,
                "b": {"id": cb["id"], "label": cb["label"], "definition": (cb["definition"] or "")[:400]} if cb else None,
                "stored_edges": [dict(e) for e in edges],
                "fresh_evidence": fresh_evidence(con, a_id, b_id),
            })

    out_path = os.path.join(ROOT, "outputs", f"phase6-sample-{date.today().isoformat()}.json")
    json.dump(sample, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(sample)} sampled edges to {out_path}")
    for verb, n in SAMPLE_SIZES.items():
        print(f"  {verb}: {min(n, len(by_verb.get(verb, [])))} sampled of {len(by_verb.get(verb, []))} total")


if __name__ == "__main__":
    main()
