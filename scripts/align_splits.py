"""Banded sequence alignment for books whose MT/Greek vs English verse totals differ
(splits and merges at chapter seams). Complements build_versemap.py's 1-1 zip.

Moves: 1-1 match, 1-2 split (one source verse spans two English verses),
2-1 merge (two source verses fold into one English verse). Scored by token
overlap between MACULA English glosses and English verse text; small penalty
for split/merge so they're only chosen when the text demands them.

Emits versemap rows for every non-identity covering pair, with note split/merge.
"""
import json
import re
import sys

STOP = {"the", "and", "of", "a", "to", "in", "he", "it", "is", "was", "for", "that",
        "with", "his", "him", "not", "they", "them", "i", "you", "will", "shall",
        "on", "be", "have", "has", "as", "at", "by", "from", "their", "her", "she"}
EXCLUDE = {"Mark.16.99"}  # apparatus code for the shorter-ending variant, no English counterpart


def toks(s):
    return [t for t in re.findall(r"[a-z']+", (s or "").lower()) if t not in STOP][:40]


def overlap(a, b):
    ta, tb = toks(a), set(toks(b))
    if not ta:
        return 0.05  # empty gloss: weak neutral score, favors diagonal
    return sum(1 for t in ta if t in tb) / len(ta)


def align_book(book, wtext, etext, band=12):
    pref = book + "."
    W = sorted(((int(c), int(v)) for r in wtext if r.startswith(pref) and r not in EXCLUDE
                for _, c, v in [r.rsplit(".", 2)]), key=lambda x: x)
    E = sorted(((int(c), int(v)) for r in etext if r.startswith(pref)
                for _, c, v in [r.rsplit(".", 2)]), key=lambda x: x)
    wr = [f"{book}.{c}.{v}" for c, v in W]
    er = [f"{book}.{c}.{v}" for c, v in E]
    n, m = len(wr), len(er)
    NEG = -1e9
    # DP over (i, j): best score aligning first i source verses to first j English verses
    score = {(0, 0): 0.0}
    back = {}
    for i in range(n + 1):
        for j in range(max(0, i - band), min(m, i + band) + 1):
            if (i, j) not in score:
                continue
            s = score[(i, j)]
            if i < n and j < m:  # 1-1
                val = s + overlap(wtext.get(wr[i], ""), etext.get(er[j], ""))
                if val > score.get((i + 1, j + 1), NEG):
                    score[(i + 1, j + 1)] = val
                    back[(i + 1, j + 1)] = (i, j, "1-1")
            if i < n and j + 1 < m:  # 1-2 split
                val = s + overlap(wtext.get(wr[i], ""), etext.get(er[j], "") + " " + etext.get(er[j + 1], "")) - 0.30
                if val > score.get((i + 1, j + 2), NEG):
                    score[(i + 1, j + 2)] = val
                    back[(i + 1, j + 2)] = (i, j, "1-2")
            if i + 1 < n and j < m:  # 2-1 merge
                val = s + overlap(wtext.get(wr[i], "") + " " + wtext.get(wr[i + 1], ""), etext.get(er[j], "")) - 0.30
                if val > score.get((i + 2, j + 1), NEG):
                    score[(i + 2, j + 1)] = val
                    back[(i + 2, j + 1)] = (i, j, "2-1")
    if (n, m) not in back and (n, m) != (0, 0):
        return None, f"  FAIL {book}: no alignment path (band={band})"
    # traceback
    ops = []
    cur = (n, m)
    while cur != (0, 0):
        pi, pj, op = back[cur]
        ops.append((pi, pj, op))
        cur = (pi, pj)
    ops.reverse()
    rows, oddities = [], []
    for i, j, op in ops:
        if op == "1-1":
            if wr[i] != er[j]:
                rows.append((wr[i], er[j], "shift"))
        elif op == "1-2":
            rows.append((wr[i], er[j], "split:first"))
            rows.append((wr[i], er[j + 1], "split:second"))
            oddities.append(f"{wr[i]} -> {er[j]}+{er[j+1]}")
        elif op == "2-1":
            rows.append((wr[i], er[j], "merge:first"))
            rows.append((wr[i + 1], er[j], "merge:second"))
            oddities.append(f"{wr[i]}+{wr[i+1]} -> {er[j]}")
    note = f"  OK {book}: {len(rows)} mapped pairs; splits/merges: {'; '.join(oddities) if oddities else 'none'}"
    return rows, note


def main():
    detail = json.load(open(sys.argv[1]))
    out_path = sys.argv[2]
    wtext, etext = detail["w"], detail["e"]
    books = sorted({r.rsplit(".", 2)[0] for r in wtext})
    all_rows = []
    for book in books:
        rows, note = align_book(book, wtext, etext)
        print(note)
        if rows:
            all_rows.extend(rows)
    with open(out_path, "w") as f:
        for mt, en, kind in all_rows:
            f.write(f"MT\t{mt}\t{en}\tempirical DP alignment ({kind}), gloss-validated\n")
    print(f"\nrows: {len(all_rows)}")


if __name__ == "__main__":
    main()
