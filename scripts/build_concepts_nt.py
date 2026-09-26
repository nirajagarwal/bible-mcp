"""NT expansion of the concept graph (DESIGN.md #5), phases 1-4 only. Additive by
design: Phase 5's already-reviewed typed edges (narrower/broader/causes/part_of/
symbol_of/contrasts) are never touched. concept_associated and concept_instance_of
were never manually reviewed — they're safe to fully recompute from the enlarged
(OT+NT) concept_mentions pool, so unreviewed pairs get the benefit of the fuller
evidence instead of being stuck with an OT-only weight forever.

Phases 1 (Easton ingestion) and 2 (theme-concept seeding) already covered the whole
Bible on the very first run — `load_easton()`/`phase1_ingest_easton`/
`phase2_seed_concepts` in build_concepts.py never filtered by testament, only
Phase 3 (verse anchors) did. So this script only needs:
  Phase 3b: add NT-filtered concept_mentions (does not touch or remove OT rows)
  Phase 4b: recompute concept_associated + concept_instance_of from the combined
            pool, skipping any pair that already has a reviewed typed edge

Usage: python3 scripts/build_concepts_nt.py
"""
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_concepts import DB, load_easton, extract_refs, _expand_maybe_range  # noqa: E402

NT_BOOKS = {
    "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph",
    "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb",
    "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev",
}
assert len(NT_BOOKS) == 27

REVIEWED_TYPES = (
    "concept_narrower", "concept_broader", "concept_causes",
    "concept_part_of", "concept_symbol_of", "concept_contrasts",
)


def phase3b_nt_mentions(con, entries):
    """Add NT verse anchors on top of the existing OT ones. Purely additive:
    INSERT OR IGNORE, never deletes an existing (OT) concept_mentions row.

    load_easton() (reused as-is from build_concepts.py) only carries term_id/
    label/text — concept_id is assigned by phase2_seed_concepts, which already
    ran on the original build and isn't re-run here (the theme nodes already
    exist). So look each entry's real concept_id up by the term_id stashed in
    concepts.data at seed time, rather than re-deriving slugs and hoping the
    iteration order still matches."""
    term_id_to_concept = {}
    for r in con.execute("SELECT id, data FROM concepts WHERE type='theme' AND source='easton'"):
        data = json.loads(r["data"] or "{}")
        tid = data.get("term_id")
        if tid:
            term_id_to_concept[tid] = r["id"]

    rows, newly_activated, enriched, unmatched = [], set(), set(), 0
    existing = {r["concept_id"] for r in con.execute(
        "SELECT DISTINCT concept_id FROM concept_mentions").fetchall()}
    for e in entries:
        cid = term_id_to_concept.get(e["term_id"])
        if not cid:
            unmatched += 1
            continue
        nt_refs = {r for r in extract_refs(e["text"]) if r.split(".", 1)[0] in NT_BOOKS}
        if not nt_refs:
            continue
        for r in nt_refs:
            rows.append((cid, r, "easton_parsed_nt"))
        if cid in existing:
            enriched.add(cid)
        else:
            newly_activated.add(cid)
    if unmatched:
        print(f"  WARNING: {unmatched} entries had no matching theme concept by term_id")
    con.executemany(
        "INSERT OR IGNORE INTO concept_mentions(concept_id,ref,source) VALUES(?,?,?)", rows)
    print(f"  concept_mentions (NT): {len(rows)} new anchors — "
          f"{len(newly_activated)} concepts newly activated (were OT-empty), "
          f"{len(enriched)} existing OT concepts enriched with NT anchors")


def already_reviewed_pairs(con):
    pairs = set()
    placeholders = ",".join("?" * len(REVIEWED_TYPES))
    for r in con.execute(
            f"SELECT from_ref, to_ref FROM links WHERE type IN ({placeholders})", REVIEWED_TYPES):
        a = r["from_ref"].split(":", 1)[1] if r["from_ref"].startswith("concept:") else None
        b = r["to_ref"].split(":", 1)[1] if r["to_ref"].startswith("concept:") else None
        if a and b:
            pairs.add(frozenset((a, b)))
    return pairs


def phase4b_recompute_unreviewed(con):
    """Recompute concept_associated and concept_instance_of from the now-larger
    concept_mentions pool. Any pair that already graduated to a reviewed typed
    edge is skipped entirely — that edge is left exactly as Phase 5/6 left it."""
    reviewed = already_reviewed_pairs(con)
    print(f"  {len(reviewed)} pairs already reviewed (typed edges) — will not be touched")

    mentions = con.execute("SELECT concept_id, ref FROM concept_mentions").fetchall()
    by_ref = defaultdict(set)
    for r in mentions:
        by_ref[r["ref"]].add(r["concept_id"])

    pair_weight = Counter()
    for ref, cids in by_ref.items():
        if 2 <= len(cids) <= 30:
            for a, b in combinations(sorted(cids), 2):
                pair_weight[(a, b)] += 1

    xref_hits = con.execute(
        "SELECT DISTINCT cm.concept_id AS a, l.to_ref AS target FROM concept_mentions cm "
        "JOIN links l ON l.from_ref = cm.ref AND l.type = 'cross_reference'").fetchall()
    xref_weight = Counter()
    for r in xref_hits:
        for target_ref in _expand_maybe_range(r["target"]):
            for b in by_ref.get(target_ref, ()):
                if b != r["a"]:
                    xref_weight[tuple(sorted((r["a"], b)))] += 1

    skipped = 0
    assoc_updates = {}
    for (a, b), w in pair_weight.items():
        if frozenset((a, b)) in reviewed:
            skipped += 1
            continue
        assoc_updates[(a, b, "coverse")] = w
    for (a, b), w in xref_weight.items():
        if frozenset((a, b)) in reviewed:
            skipped += 1
            continue
        assoc_updates[(a, b, "cross_reference_chain")] = w

    con.execute("DELETE FROM links WHERE type='concept_associated'")
    rows = [(f"concept:{a}", f"concept:{b}", "concept_associated", float(w), src)
            for (a, b, src), w in assoc_updates.items()]
    con.executemany("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)", rows)
    print(f"  concept_associated: {len(rows)} rows recomputed from combined OT+NT evidence "
          f"({skipped} candidate rows skipped — pair already has a reviewed typed edge)")

    con.execute("DELETE FROM links WHERE type='concept_instance_of'")
    ent_rows = con.execute(
        "SELECT em.entity_id AS eid, cm.concept_id AS cid, COUNT(*) AS n "
        "FROM entity_mentions em JOIN concept_mentions cm ON cm.ref = em.ref "
        "GROUP BY em.entity_id, cm.concept_id").fetchall()
    inst_rows = [(f"entity:{r['eid']}", f"concept:{r['cid']}", "concept_instance_of",
                  float(r["n"]), "shared_verse") for r in ent_rows]
    con.executemany("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)", inst_rows)
    print(f"  concept_instance_of: {len(inst_rows)} rows recomputed from combined OT+NT evidence")


def report(con):
    print("\n--- Verification ---")
    n = con.execute("SELECT COUNT(*) c FROM concept_mentions WHERE source='easton_parsed_nt'").fetchone()["c"]
    print(f"  NT-sourced concept_mentions: {n}")
    n = con.execute("SELECT COUNT(DISTINCT concept_id) c FROM concept_mentions").fetchone()["c"]
    print(f"  total concepts with >=1 mention (OT or NT): {n}")
    for t in ("concept_associated", "concept_instance_of"):
        n = con.execute("SELECT COUNT(*) c FROM links WHERE type=?", (t,)).fetchone()["c"]
        print(f"  links[{t}]: {n}")
    for t in REVIEWED_TYPES:
        n = con.execute("SELECT COUNT(*) c FROM links WHERE type=?", (t,)).fetchone()["c"]
        print(f"  links[{t}] (untouched): {n}")
    print()
    print("  weight distribution of concept_associated after recompute:")
    for lo, hi, label in [(22, 10**9, ">=22 (old top tier)"), (10, 21, "10-21 (old reviewed floor..top)"),
                           (1, 9, "1-9 (confidence floor, stays associated by policy)")]:
        n = con.execute("SELECT COUNT(*) c FROM links WHERE type='concept_associated' AND weight>=? AND weight<=?",
                         (lo, hi)).fetchone()["c"]
        print(f"    weight {label}: {n}")
    # regression sentinels
    for t in ("cross_reference", "citation"):
        n = con.execute("SELECT COUNT(*) c FROM links WHERE type=?", (t,)).fetchone()["c"]
        print(f"  regression check links[{t}]: {n}")


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    entries = load_easton()
    print(f"Loaded {len(entries)} concept-worthy Easton entries (whole-Bible pool)")
    print("Phase 3b — NT verse anchors (additive)...")
    phase3b_nt_mentions(con, entries)
    print("Phase 4b — recompute unreviewed candidate edges from combined OT+NT evidence...")
    phase4b_recompute_unreviewed(con)
    con.commit()
    report(con)
    con.close()


if __name__ == "__main__":
    main()
