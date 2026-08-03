"""Build the `versemap` table: original-language (MT/NA) verse refs <-> English (BSB/WEB) refs.

Derived EMPIRICALLY from the two witnesses already in the DB — the `words` table
(MACULA, Masoretic/Nestle numbering) and the `passages` table (BSB/WEB, English
numbering) — using monotonic sequence alignment per book, validated by token
overlap between MACULA's English glosses and the English verse text.

Psalms stay on the existing `psalm_offsets` mechanism (superscriptions are
one-to-many and already handled). This module covers every OTHER book.

The table is designed so a future TVTMS import (STEPBible, CC BY) can extend or
replace rows: (scheme, src_ref, dst_ref, note). Today scheme='MT' means
"original-language numbering as found in MACULA" for both testaments.

Usage (offline build): python3 scripts/build_versemap.py --counts tmp-vcounts.json \
    --detail tmp-vdetail.json --out data/versemap.tsv
"""
import argparse
import json
import re
import sys

STOP = {"the", "and", "of", "a", "to", "in", "he", "it", "is", "was", "for", "that",
        "with", "his", "him", "not", "they", "them", "i", "you", "will", "shall",
        "on", "be", "have", "has", "as", "at", "by", "from", "their", "her", "she"}


def toks(s):
    return [t for t in re.findall(r"[a-z']+", (s or "").lower()) if t not in STOP][:30]


def overlap(a, b):
    """Fraction of a's tokens found in b (bag semantics)."""
    ta, tb = toks(a), set(toks(b))
    if not ta:
        return 0.0
    return sum(1 for t in ta if t in tb) / len(ta)


def verse_list(per_book, book):
    """Ordered [(ch, v), ...] for a book from {'Book.C.V': ...} keys."""
    out = []
    pref = book + "."
    for ref in per_book:
        if ref.startswith(pref):
            _, c, v = ref.rsplit(".", 2)
            out.append((int(c), int(v)))
    return sorted(out)


def build_book_map(book, wrefs, erefs, wtext, etext, report):
    """Return list of (mt_ref, eng_ref) pairs where they differ, or None if book
    can't be safely aligned (logged)."""
    if len(wrefs) != len(erefs):
        report.append(f"  SKIP {book}: verse totals differ (words {len(wrefs)} vs eng {len(erefs)}) — needs split/merge handling")
        return None
    pairs = []
    scores_id, scores_map = [], []
    for (wc, wv), (ec, ev) in zip(wrefs, erefs):
        if (wc, wv) == (ec, ev):
            continue
        mt_ref = f"{book}.{wc}.{wv}"
        eng_ref = f"{book}.{ec}.{ev}"
        # validate: gloss stream of mt_ref should match mapped English verse
        # better than it matches the same-numbered English verse (identity).
        g = wtext.get(mt_ref, "")
        s_map = overlap(g, etext.get(eng_ref, ""))
        s_id = overlap(g, etext.get(mt_ref, ""))
        scores_map.append(s_map)
        scores_id.append(s_id)
        pairs.append((mt_ref, eng_ref))
    if pairs:
        avg_map = sum(scores_map) / len(scores_map)
        avg_id = sum(scores_id) / len(scores_id)
        verdict = "OK" if avg_map > avg_id else "SUSPECT"
        report.append(f"  {verdict} {book}: {len(pairs)} shifted verses; gloss-overlap mapped={avg_map:.2f} vs identity={avg_id:.2f}")
        if avg_map <= avg_id:
            return None
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", required=True)
    ap.add_argument("--detail", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    counts = json.load(open(args.counts))
    detail = json.load(open(args.detail))
    wtext, etext = detail["w"], detail["e"]

    books = sorted({r.rsplit(".", 2)[0] for r in wtext})
    report, rows, skipped = [], [], []
    for book in books:
        if book == "Ps":
            continue  # psalm_offsets handles Psalms (one-to-many superscriptions)
        wrefs = verse_list(wtext, book)
        erefs = verse_list(etext, book)
        got = build_book_map(book, wrefs, erefs, wtext, etext, report)
        if got is None:
            skipped.append(book)
            continue
        rows.extend(got)

    with open(args.out, "w") as f:
        f.write("scheme\tsrc_ref\tdst_ref\tnote\n")
        for mt, en in rows:
            f.write(f"MT\t{mt}\t{en}\tempirical sequence alignment, gloss-validated\n")
    print("\n".join(report))
    print(f"\nversemap rows: {len(rows)}  |  books skipped: {skipped}")


if __name__ == "__main__":
    main()
