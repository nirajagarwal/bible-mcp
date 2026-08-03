"""Incremental corpus additions: the rest of the Apostolic Fathers (from the
Gutenberg #77576 compilation already in data/sources) and the outputs/ research
layer (Layer 0 surveys + Layer 2 briefs, layer='output', with draws_on links).

Two modes:
  --emit-json PATH   parse + (optionally --embed) generate vectors, write rows JSON
  --apply JSON --db DB   insert previously emitted rows into a database

The emit/apply split exists because the primary db is too large to round-trip
through the cloud sandbox; rows are prepared where the sources are and applied
where the db is. Running with --db directly (on the Mac) does both in one step.

Ignatius: the ANF text alternates SHORTER and LONGER recensions chapter by
chapter; only the SHORTER (Middle) recension is ingested — the scholarly
standard text. The longer recension is a later expansion; ingesting both would
duplicate every chapter in search results.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from lib_refs import parse_scripture_citations  # noqa: E402

CHAPTER_RE = re.compile(
    r"^(BOOK|CHAPTER|CHAP\.|PART|LETTER|SECTION|VISION|COMMANDMENT|SIMILITUDE)\s+[IVXLC0-9A-Z]+\b.*$"
    r"|^[IVXLC]+\.?\s*$|^CHAPTER\s+\w+", re.I)
EPISTLE_RE = re.compile(r"^THE (EPISTLE|MARTYRDOM) OF IGNATIUS", re.I)
FOOTNOTE_BLOCK_RE = re.compile(r"Footnote (\d+):\s*\n\s*\n(.*?)(?=\nFootnote \d+:|\Z)", re.S)
MARKER_RE = re.compile(r"\[(\d+)\]")

# (start_line, end_line, doc_id, title, author, opts) — 1-indexed, end exclusive
AF_SHELF = [
    (2718, 3210, "2CLEMENT", "The Second Epistle of Clement", "Ancient homily (author unknown, misattributed to Clement)", {}),
    (3253, 3847, "POLYCARP", "The Epistle of Polycarp to the Philippians", "Polycarp of Smyrna", {}),
    (3847, 4631, "MARTPOLY", "The Martyrdom of Polycarp", "Church of Smyrna (encyclical)", {"skip_to_chap": True}),
    (6980, 13438, "IGNATIUS", "The Epistles of Ignatius (shorter recension)", "Ignatius of Antioch", {"ignatius": True}),
    (14089, 14443, "MARTIGN", "The Martyrdom of Ignatius", "Attributed to eyewitness companions", {"skip_to_chap": True}),
    (14496, 15198, "DIOGNETUS", "The Epistle to Diognetus", "Anonymous (Mathetes)", {}),
    (15333, 20125, "HERMAS", "The Pastor of Hermas", "Hermas of Rome", {}),
    (20144, 20512, "PAPIAS", "Fragments of Papias", "Papias of Hierapolis", {}),
]

OUTPUTS = [
    # (doc_id, title, relpath under outputs/)
    ("POTTER-L0", "Potter and Clay — Layer 0 raw corpus survey", "2026-07-18-potter-clay-layer0-raw-survey.md"),
    ("POTTER-BRIEF", "What the Clay Is Allowed to Say (research brief)", "2026-07-18-potter-clay-layer2-what-the-clay-is-allowed-to-say.md"),
    ("WATER-L0", "Living Water — Layer 0 raw corpus survey", "2026-07-17-living-water-layer0-raw-survey.md"),
    ("WATER-BRIEF", "The Water That Moves (research brief)", "2026-07-17-living-water-layer2-the-water-that-moves.md"),
    ("WILD-L0", "Wilderness — Layer 0 raw corpus survey", "2026-07-17-wilderness-layer0-raw-survey.md"),
    ("WILD-BRIEF", "A Land Not Sown (research brief)", "2026-07-17-wilderness-layer2-a-land-not-sown.md"),
]

PROSE_REF_RE = re.compile(r"\b([A-Z][A-Z0-9]{2,}\.\d+\.\d+)\b")
OSIS_REF_RE = re.compile(r"\b((?:[1-3])?[A-Z][a-z]+\.\d+\.\d+(?:-\d+)?)\b")


def slice_work(lines, start, end, doc_id, opts):
    """Gutenberg text lines -> (passages rows, citation link rows).
    Same paragraph discipline as build_db.ingest_patristic_gutenberg, plus:
    skip_to_chap (drop intro-note apparatus before the first chapter heading)
    and the Ignatius shorter/longer state machine."""
    raw = "\n".join(lines[start - 1:end - 1])
    # Footnotes: "Footnote N:" blocks whose continuation blocks are indented.
    # NOTE: a single regex-to-end-of-cluster approach (as in build_db) silently
    # swallows body text between footnote clusters in works with per-section
    # clusters (Ignatius' epistles, Hermas' visions) — classify block-by-block.
    footnotes = {}
    paras, fn_current = [], None
    for block in re.split(r"\n\s*\n", raw):
        if not block.strip():
            continue
        m = re.match(r"^\s*Footnote (\d+):\s*$", block.strip())
        if m:
            fn_current = int(m.group(1))
            footnotes[fn_current] = ""
            continue
        lines_ = [l for l in block.splitlines() if l.strip()]
        if fn_current is not None and all(l.startswith(("  ", "\t")) for l in lines_):
            footnotes[fn_current] += (" " if footnotes[fn_current] else "") + " ".join(block.split())
            continue
        fn_current = None
        paras.append(block)
    chapter, para_n, seq, rows = 1, 0, 0, []
    marker_ref = {}
    started = not opts.get("skip_to_chap")
    keep = True  # Ignatius recension state
    for p in paras:
        text = " ".join(p.split())
        if not text:
            continue
        head = p.strip().splitlines()[0].strip()
        stripped = text.strip("_ ").rstrip(".")
        if opts.get("ignatius"):
            if stripped.upper() == "SHORTER":
                keep = True
                continue
            if stripped.upper() == "LONGER":
                keep = False
                continue
            if EPISTLE_RE.match(head):
                if para_n > 0:
                    chapter += 1
                para_n = 0
                keep = True
                started = True
                continue
        if CHAPTER_RE.match(head) and len(text) < 200:
            if para_n > 0:
                chapter += 1
            para_n = 0
            started = True
            if opts.get("ignatius"):
                keep = True
            continue
        if not started or not keep:
            continue
        if len(text) < 40 or re.search(r"\.{5,}", text) or text.isupper():
            continue
        para_n += 1
        seq += 1
        ref = f"{doc_id}.{chapter}.{para_n}"
        for num in MARKER_RE.findall(text):
            marker_ref[int(num)] = ref
        text = MARKER_RE.sub("", text)
        text = re.sub(r"\s+([,.;:])", r"\1", text).strip()
        rows.append((doc_id, ref, doc_id, chapter, para_n, seq, text))
    links = []
    for num, txt in footnotes.items():
        fr = marker_ref.get(num)
        if not fr:
            continue
        for to in parse_scripture_citations(txt):
            links.append((fr, to, "citation", 1.0, "ANF footnote (Roberts-Donaldson-Crombie translation)"))
    return rows, links


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text, body = text[3:end], text[end + 4:]
    fm = {}
    key = None
    for line in fm_text.splitlines():
        m = re.match(r"^(\w[\w_-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip().strip('"')
        elif line.strip().startswith("- ") and key:
            fm[key] = (fm.get(key) or "") + " ; " + line.strip()[2:]
    return fm, body


def ingest_output_file(path, doc_id, title):
    text = open(path, encoding="utf-8").read()
    fm, body = parse_frontmatter(text)
    rows, chapter, para_n, seq = [], 1, 0, 0
    first_heading_seen = False
    for block in re.split(r"\n\s*\n", body):
        t = " ".join(block.split()).strip()
        if not t:
            continue
        if t.startswith("##"):
            if first_heading_seen or para_n > 0:
                chapter += 1
            first_heading_seen = True
            para_n = 0
            continue
        if t.startswith("#"):
            continue
        t = re.sub(r"^[-*]\s+", "", t)
        if len(t) < 40:
            continue
        para_n += 1
        seq += 1
        rows.append((doc_id, f"{doc_id}.{chapter}.{para_n}", doc_id, chapter, para_n, seq, t))
    # draws_on -> links (scripture refs via citation parser on natural forms; prose/OSIS refs verbatim)
    links, seen = [], set()
    draws = (fm.get("draws_on") or "").replace(";", " ; ")
    for ref in OSIS_REF_RE.findall(draws):
        base = ref.split("-")[0]
        if base not in seen:
            seen.add(base)
            links.append((doc_id, base, "draws_on", 1.0, "output frontmatter"))
    for ref in PROSE_REF_RE.findall(draws):
        if ref not in seen:
            seen.add(ref)
            links.append((doc_id, ref, "draws_on", 1.0, "output frontmatter"))
    for ref in parse_scripture_citations(draws):
        if ref not in seen:
            seen.add(ref)
            links.append((doc_id, ref, "draws_on", 1.0, "output frontmatter"))
    doc = dict(id=doc_id, title=title, layer="output", language="en",
               translator=None, source_url=None, license="Project-generated (research output)",
               license_tier="A",
               notes=f"Synthesis-pipeline artifact. theme={fm.get('theme')} stage={fm.get('stage')} "
                     f"skill={fm.get('skill')} date={fm.get('date')} derived_from={fm.get('derived_from')}")
    return doc, rows, links


def emit(args):
    out = {"documents": [], "passages": [], "links": [], "embeddings": []}
    lines = open(args.gutenberg, encoding="utf-8-sig").read().split("\n")
    for start, end, doc_id, title, author, opts in AF_SHELF:
        rows, links = slice_work(lines, start, end, doc_id, opts)
        out["documents"].append(dict(
            id=doc_id, title=title, layer="patristic", language="en",
            translator="Roberts, Donaldson & Crombie (Ante-Nicene Fathers)",
            source_url="https://www.gutenberg.org/ebooks/77576",
            license="Public Domain", license_tier="A",
            notes=f"Author: {author}. Project Gutenberg #77576. Tier-1 citations from translators' footnotes."
                  + (" Shorter recension only; longer recension excluded as later expansion." if opts.get("ignatius") else "")))
        out["passages"].extend(rows)
        out["links"].extend(links)
        print(f"  {doc_id}: {len(rows)} paragraphs, {len(links)} citations")
    for doc_id, title, rel in OUTPUTS:
        path = os.path.join(args.outputs_dir, rel)
        doc, rows, links = ingest_output_file(path, doc_id, title)
        out["documents"].append(doc)
        out["passages"].extend(rows)
        out["links"].extend(links)
        print(f"  {doc_id}: {len(rows)} paragraphs, {len(links)} draws_on links")
    if args.embed:
        import numpy as np
        from fastembed import TextEmbedding
        model_name = "BAAI/bge-small-en-v1.5"
        model = TextEmbedding(model_name=model_name, threads=os.cpu_count())
        texts = [p[6] for p in out["passages"]]
        vecs = list(model.embed(texts, batch_size=256))
        for (doc_id, ref, *_rest, text), v in zip(
                [(p[0], p[1], p[6]) for p in out["passages"]], vecs):
            v = np.asarray(v, dtype=np.float32)
            v = v / (np.linalg.norm(v) + 1e-9)
            out["embeddings"].append(dict(kind="paragraph", doc_id=doc_id, ref=ref,
                                          end_ref=None, text=text, model=model_name,
                                          dim=len(v), vec=v.astype(np.float16).tobytes().hex()))
        print(f"  embeddings: {len(out['embeddings'])} vectors")
    json.dump(out, open(args.emit_json, "w"))
    print(f"emitted -> {args.emit_json}")


def apply(args):
    import sqlite3
    data = json.load(open(args.apply))
    con = sqlite3.connect(args.db)
    for d in data["documents"]:
        con.execute("INSERT OR REPLACE INTO documents(id,title,layer,language,translator,source_url,license,license_tier,notes) "
                    "VALUES(:id,:title,:layer,:language,:translator,:source_url,:license,:license_tier,:notes)", d)
        con.execute("DELETE FROM links WHERE from_ref LIKE ? AND type IN ('citation','draws_on')", (d["id"] + "%",))
        for (pid,) in con.execute("SELECT id FROM passages WHERE doc_id=?", (d["id"],)).fetchall():
            con.execute("DELETE FROM passages WHERE id=?", (pid,))
        con.execute("DELETE FROM embeddings WHERE doc_id=?", (d["id"],))
    con.executemany("INSERT INTO passages(doc_id,ref,book,chapter,verse,seq,text) VALUES(?,?,?,?,?,?,?)",
                    data["passages"])
    con.executemany("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)", data["links"])
    for e in data["embeddings"]:
        con.execute("INSERT INTO embeddings(kind,doc_id,ref,end_ref,text,model,dim,vec) VALUES(?,?,?,?,?,?,?,?)",
                    (e["kind"], e["doc_id"], e["ref"], e["end_ref"], e["text"], e["model"], e["dim"],
                     bytes.fromhex(e["vec"])))
    con.commit()
    print("applied:", len(data["passages"]), "passages,", len(data["links"]), "links,",
          len(data["embeddings"]), "embeddings")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gutenberg", default=os.path.join(ROOT, "data", "sources", "gutenberg", "pg77576.txt"))
    ap.add_argument("--outputs-dir", default=os.path.join(ROOT, "outputs"))
    ap.add_argument("--emit-json")
    ap.add_argument("--embed", action="store_true")
    ap.add_argument("--apply")
    ap.add_argument("--db", default=os.path.join(ROOT, "db", "bible.db"))
    args = ap.parse_args()
    if args.emit_json:
        emit(args)
    elif args.apply:
        apply(args)
    else:
        ap.error("use --emit-json or --apply")


if __name__ == "__main__":
    main()
