"""Ingest Irenaeus, Against Heresies (5 books) + Fragments, from the Wikisource
transcription of Ante-Nicene Fathers Vol. I (Roberts-Rambaut translation, PD).

Addressing fulfils DESIGN.md §2's acceptance test directly: the ANF text numbers
sections within chapters, so IREN-AH3.3.4 = Against Heresies, Book 3, chapter 3,
section 4 — a standard patristics citation resolves to a ref with no lookup.
Preface = chapter 0. Continuation paragraphs merge into their section.

Inline <ref>...</ref> footnotes are captured per section and mined for scripture
citations (tier 1) with the same parser used for the Gutenberg ANF footnotes.

Emits the same JSON shape as ingest_additions.py; apply with:
  python3 scripts/ingest_additions.py --apply data/irenaeus-<date>.json --db db/bible.db
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from lib_refs import parse_scripture_citations, roman_to_int  # noqa: E402

BOOKS = [("I", "IREN-AH1"), ("II", "IREN-AH2"), ("III", "IREN-AH3"),
         ("IV", "IREN-AH4"), ("V", "IREN-AH5")]

REF_RE = re.compile(r"<ref[^>/]*>(.*?)</ref>|<ref[^>]*/>", re.S)
HEAD_RE = re.compile(r"^==\s*(.+?)\s*==\s*$", re.M)
ANCHOR_RE = re.compile(r"\{\{anchor\+\|(\d+):(\d+)\|\d+\}\}\.?\s*")
SECNUM_RE = re.compile(r"^(\d+)\.\s+")
FRAG_HEAD_RE = re.compile(r"^'''([IVXLC]+)\.'''\s*$", re.M)


def clean(text):
    text = text.replace("'''", "")
    text = re.sub(r"\{\{(?:small-caps|sc|Greek|greek|lang\|[^|]*)\|([^{}]*)\}\}", r"\1", text)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)          # drop remaining simple templates
    text = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]*)\]\]", r"\1", text)
    text = text.replace("''", "")
    text = re.sub(r"<[^>]+>", "", text)                  # any stray html
    import html
    text = html.unescape(text)
    return " ".join(text.split()).strip()


def _emit_section(rows, links, doc_id, chapter, sec, seg, seq):
    """Extract footnotes, clean, and append one section row (returns new seq)."""
    foots = [g for g in (mm.group(1) for mm in REF_RE.finditer(seg)) if g]
    text = clean(REF_RE.sub("", seg))
    if len(text) < 40:
        return seq
    seq += 1
    ref = f"{doc_id}.{chapter}.{sec}"
    rows.append((doc_id, ref, doc_id, chapter, sec, seq, text))
    for fnote in foots:
        for to in parse_scripture_citations(clean(fnote)):
            links.append((ref, to, "citation", 1.0, "ANF footnote (Wikisource ANF I transcription)"))
    return seq


def parse_ah_book(raw, doc_id):
    """Against Heresies book page: sections carry {{anchor+|ch:sec|sec}} markers;
    the Preface (chapter 0) uses plain '1. ' numbering; chapter argument-titles
    (bold line under ==Chapter N==) are prepended to that chapter's first section."""
    m = HEAD_RE.search(raw)
    if m:
        raw = raw[m.start():]
    rows, links, seq = [], [], 0
    # Preface: from ==Preface== to the first anchor
    first_anchor = ANCHOR_RE.search(raw)
    pm = re.search(r"^==\s*Preface\s*==\s*$", raw, re.M)
    if pm:
        pref = raw[pm.end(): first_anchor.start() if first_anchor else len(raw)]
        pref = re.sub(r"^==.*$", "", pref, flags=re.M)  # drop any heading line caught
        for para in re.split(r"\n\s*\n", pref):
            sm = SECNUM_RE.match(para.strip())
            if not sm:
                continue
            seq = _emit_section(rows, links, doc_id, 0, int(sm.group(1)),
                                para.strip()[sm.end():], seq)
    anchors = list(ANCHOR_RE.finditer(raw))
    titles = {}  # chapter -> argument title, from ==Chapter== + bold line
    for hm in HEAD_RE.finditer(raw):
        cm = re.match(r"^Chapter\s+([IVXLC]+)", hm.group(1), re.I)
        if cm:
            after = raw[hm.end():hm.end() + 600]
            tm = re.search(r"'''(.+?)'''", after, re.S)
            if tm:
                titles[roman_to_int(cm.group(1))] = clean(tm.group(1))
    for i, am in enumerate(anchors):
        ch, sec = int(am.group(1)), int(am.group(2))
        end = anchors[i + 1].start() if i + 1 < len(anchors) else len(raw)
        seg = raw[am.end():end]
        nh = HEAD_RE.search(seg)  # next chapter heading inside the tail
        if nh:
            seg = seg[:nh.start()]
        if sec == 1 and ch in titles:
            seg = f"[{titles[ch]}] " + seg
        seq = _emit_section(rows, links, doc_id, ch, sec, seg, seq)
    return rows, links


def parse_fragments(raw, doc_id):
    """Fragments page: bold roman headings '''N.''' number the fragments;
    each fragment becomes chapter N with blank-line paragraphs as sections."""
    rows, links, seq = [], [], 0
    parts = FRAG_HEAD_RE.split(raw)
    it = iter(parts[1:])
    for roman, body in zip(it, it):
        ch = roman_to_int(roman)
        sec = 0
        for para in re.split(r"\n\s*\n", body):
            if not para.strip() or para.strip().startswith("{{"):
                continue
            sec += 1
            seq = _emit_section(rows, links, doc_id, ch, sec, para, seq)
    return rows, links


CHAPTER_BOLD_RE = re.compile(r"^'''Chapter ([IVXLC]+)\.?(?:&#8212;|—|--)?\s*(.*?)'''\s*$", re.M)


def parse_bold_chapters(raw, doc_id):
    """Works with bold '''Chapter N.—Title''' headings and plain paragraphs
    (Justin Martyr's works in the Wikisource ANF I transcription). Chapter from
    the roman numeral; paragraphs within a chapter become sections 1..n; the
    chapter argument-title is prepended to section 1."""
    rows, links, seq = [], [], 0
    parts = CHAPTER_BOLD_RE.split(raw)
    it = iter(parts[1:])
    for roman, title, body in zip(it, it, it):
        ch = roman_to_int(roman)
        title = clean(title)
        sec = 0
        for para in re.split(r"\n\s*\n", body):
            p = para.strip()
            if not p or p.startswith("{{") or p.startswith("=="):
                continue
            sec += 1
            if sec == 1 and title:
                p = f"[{title}] " + p
            seq = _emit_section(rows, links, doc_id, ch, sec, p, seq)
    return rows, links


def parse_page(raw, doc_id):
    if doc_id == "IREN-FRAG":
        return parse_fragments(raw, doc_id)
    if doc_id.startswith("JUSTIN"):
        return parse_bold_chapters(raw, doc_id)
    return parse_ah_book(raw, doc_id)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", default="/tmp")
    ap.add_argument("--emit-json", required=True)
    ap.add_argument("--embed", action="store_true")
    ap.add_argument("--justin", action="store_true")
    args = ap.parse_args()

    out = {"documents": [], "passages": [], "links": [], "embeddings": []}
    if args.justin:
        shelf = [("justin_The_First_Apology.wiki", "JUSTIN-1AP", "The First Apology"),
                 ("justin_The_Second_Apology.wiki", "JUSTIN-2AP", "The Second Apology"),
                 ("justin_Dialogue_with_Trypho.wiki", "JUSTIN-DIAL", "Dialogue with Trypho"),
                 ("justin_The_Martyrdom_of_Justin_Martyr.wiki", "JUSTIN-MART", "The Martyrdom of Justin Martyr")]
        author = "Justin Martyr"
    else:
        shelf = [(f"ah{r}.wiki", d, f"Against Heresies, Book {r}") for r, d in BOOKS]
        shelf.append(("ahFRAG.wiki", "IREN-FRAG", "Fragments from the Lost Writings of Irenaeus"))
        author = "Irenaeus of Lyons"
    for fname, doc_id, title in shelf:
        raw = open(os.path.join(args.src_dir, fname), encoding="utf-8").read()
        rows, links = parse_page(raw, doc_id)
        out["documents"].append(dict(
            id=doc_id, title=f"{title} ({author})", layer="patristic", language="en",
            translator="Roberts & Rambaut (Ante-Nicene Fathers vol. I)",
            source_url="https://en.wikisource.org/wiki/Ante-Nicene_Fathers/Volume_I",
            license="Public Domain", license_tier="A",
            notes=f"Author: {author}. Wikisource transcription of ANF I. "
                  "Refs are Book.chapter.section per standard citation (Preface = chapter 0). "
                  "Tier-1 citations from translators' footnotes."))
        # dedupe: transcription sources occasionally duplicate a block
        # (e.g. Dialogue ch. CXVI appears twice on Wikisource) — keep first.
        seen = {p[1] for p in out["passages"]}
        fresh = []
        for r in rows:
            if r[1] in seen:
                print(f"    dedup: dropping duplicate {r[1]}")
                continue
            seen.add(r[1])
            fresh.append(r)
        kept = {r[1] for r in fresh}
        links = [l for l in links if l[0] in kept or l[0] in {p[1] for p in out['passages']}]
        out["passages"].extend(fresh)
        out["links"].extend(links)
        print(f"  {doc_id}: {len(fresh)} sections, {len(links)} citations")
    if args.embed:
        import numpy as np
        from fastembed import TextEmbedding
        model_name = "BAAI/bge-small-en-v1.5"
        model = TextEmbedding(model_name=model_name, threads=os.cpu_count())
        texts = [p[6] for p in out["passages"]]
        vecs = []
        for i in range(0, len(texts), 64):  # small batches: AH sections are long
            vecs.extend(model.embed(texts[i:i + 64], batch_size=16))
        for p, v in zip(out["passages"], vecs):
            v = np.asarray(v, dtype=np.float32)
            v = v / (np.linalg.norm(v) + 1e-9)
            out["embeddings"].append(dict(kind="paragraph", doc_id=p[0], ref=p[1], end_ref=None,
                                          text=p[6], model=model_name, dim=len(v),
                                          vec=v.astype(np.float16).tobytes().hex()))
        print(f"  embeddings: {len(out['embeddings'])}")
    json.dump(out, open(args.emit_json, "w"))
    print(f"emitted -> {args.emit_json}")


if __name__ == "__main__":
    main()
