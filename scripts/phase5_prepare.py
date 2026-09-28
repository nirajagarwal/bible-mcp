"""Phase 5 step 1: prepare a batch of concept_associated candidate edges, with real
evidence (both concepts' definitions + the actual verse text that produced the
edge), for the bounded verb-assignment pass described in DESIGN.md #5.

This does NOT call any LLM API itself (bible-mcp has no such credential wired up).
It writes an evidence file; the verb-assignment judgment is made by whoever/whatever
reads that file (in this run: Claude, in-session, held to the same fixed-vocabulary-
plus-cited-evidence rule the design calls for) and written back via phase5_apply.py.

Usage: python3 scripts/phase5_prepare.py [N] [min_weight]
  N          how many top-weighted concept_associated edges to prepare (default 50)
  min_weight only consider edges with weight >= this (default 0, i.e. no floor beyond N)

Output: outputs/phase5-batch-<date>.json

CONFIDENCE FLOOR (settled 2026-09-26, revised 2026-09-28, see DESIGN.md #5):
weight<7 is a permanent floor, never reviewed. Weight 7-9 was opened up for
review on 2026-09-28 (explicit decision to trade some per-pair rigor for
coverage at this scale) and fully completed — 8 edges sharpened out of 2,892,
with the sharpen rate collapsing to ~0 by weight 7. A partial sample into
weight 6 (408 pairs) confirmed the trend (0 upgrades) before the pass was
deliberately stopped rather than continued into weight 6-3's remaining ~20,800
pairs. Don't point this script below weight 7 without another explicit
decision recorded here.
"""
import glob
import json
import os
import sqlite3
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(ROOT, "outputs")
DB = os.environ.get("BIBLE_DB_PATH", os.path.join(ROOT, "db", "bible.db"))
OUT = os.path.join(OUTPUTS, f"phase5-batch-{date.today().isoformat()}-{{tag}}.json")

N = int(sys.argv[1]) if len(sys.argv) > 1 else 50
MIN_WEIGHT = float(sys.argv[2]) if len(sys.argv) > 2 else 0
TAG = sys.argv[3] if len(sys.argv) > 3 else "batch"


def already_judged_pairs():
    """Every pair that already has a logged judgment (any prior concept-build-log
    file), so re-running prepare for a wider weight net doesn't re-litigate pairs
    already reviewed under a narrower one."""
    seen = set()
    for path in glob.glob(os.path.join(OUTPUTS, "concept-build-log-*.jsonl")):
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            seen.add(frozenset(rec["pair"]))
    return seen


def concept(con, cid):
    return con.execute("SELECT id,label,definition FROM concepts WHERE id=?", (cid,)).fetchone()


def verse_text(con, ref):
    row = con.execute(
        "SELECT text FROM passages WHERE doc_id='BSB' AND ref=? UNION "
        "SELECT text FROM passages WHERE doc_id='WEB' AND ref=? LIMIT 1", (ref, ref)).fetchone()
    return row["text"] if row else None


def gather_evidence(con, a_id, b_id, source, limit=3):
    """Real verse-level evidence for why this pair was proposed. For 'coverse':
    verses both concepts are anchored to. For 'cross_reference_chain': (a's verse,
    cross-reference target that's one of b's verses) pairs."""
    a_refs = {r["ref"] for r in con.execute(
        "SELECT ref FROM concept_mentions WHERE concept_id=?", (a_id,)).fetchall()}
    b_refs = {r["ref"] for r in con.execute(
        "SELECT ref FROM concept_mentions WHERE concept_id=?", (b_id,)).fetchall()}
    ev = []
    if source == "coverse":
        for ref in sorted(a_refs & b_refs)[:limit]:
            t = verse_text(con, ref)
            if t:
                ev.append({"kind": "shared_verse", "ref": ref, "text": t})
    else:  # cross_reference_chain
        rows = con.execute(
            "SELECT DISTINCT cm.ref AS src, l.to_ref AS target FROM concept_mentions cm "
            "JOIN links l ON l.from_ref = cm.ref AND l.type='cross_reference' "
            "WHERE cm.concept_id=?", (a_id,)).fetchall()
        seen = set()
        for r in rows:
            if r["target"] in b_refs and r["target"] not in seen:
                seen.add(r["target"])
                ev.append({
                    "kind": "cross_reference", "from_ref": r["src"], "from_text": verse_text(con, r["src"]),
                    "to_ref": r["target"], "to_text": verse_text(con, r["target"]),
                })
            if len(ev) >= limit:
                break
    return ev


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    seen = already_judged_pairs()
    rows = con.execute(
        "SELECT from_ref, to_ref, weight, source FROM links "
        "WHERE type='concept_associated' AND weight >= ? ORDER BY weight DESC",
        (MIN_WEIGHT,)).fetchall()

    batch, skipped = [], 0
    for r in rows:
        if len(batch) >= N:
            break
        a_id, b_id = r["from_ref"].split(":", 1)[1], r["to_ref"].split(":", 1)[1]
        if frozenset((a_id, b_id)) in seen:
            skipped += 1
            continue
        ca, cb = concept(con, a_id), concept(con, b_id)
        if not ca or not cb:
            continue
        batch.append({
            "from_ref": r["from_ref"], "to_ref": r["to_ref"], "weight": r["weight"], "source": r["source"],
            "a": {"id": ca["id"], "label": ca["label"], "definition": (ca["definition"] or "")[:500]},
            "b": {"id": cb["id"], "label": cb["label"], "definition": (cb["definition"] or "")[:500]},
            "evidence": gather_evidence(con, a_id, b_id, r["source"]),
        })
    out_path = OUT.format(tag=TAG)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(batch, open(out_path, "w"), indent=2, ensure_ascii=False)
    total_at_or_above = con.execute(
        "SELECT COUNT(*) c FROM links WHERE type='concept_associated' AND weight>=?", (MIN_WEIGHT,)).fetchone()[0]
    print(f"Wrote {len(batch)} candidate pairs to {out_path} "
          f"(skipped {skipped} already-judged; {total_at_or_above} total at weight>={MIN_WEIGHT})")


if __name__ == "__main__":
    main()
