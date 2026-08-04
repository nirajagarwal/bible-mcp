"""Build db/bible.db from data/sources/. Idempotent: rebuilds from scratch each run.

Usage: python3 scripts/build_db.py
"""
import json, os, re, sqlite3, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "sources")
DB = os.environ.get("BIBLE_DB_PATH", os.path.join(ROOT, "db", "bible.db"))
sys.path.insert(0, HERE)
from lib_refs import book_to_osis, PARATEXT_TO_OSIS, BOOK_ORDER, make_ref, parse_scripture_citations  # noqa: E402


def fresh_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.executescript(open(os.path.join(HERE, "schema.sql")).read())
    return con


def add_document(con, **kw):
    con.execute(
        "INSERT INTO documents(id,title,layer,language,translator,source_url,license,license_tier,notes) "
        "VALUES(:id,:title,:layer,:language,:translator,:source_url,:license,:license_tier,:notes)",
        {k: kw.get(k) for k in
         ["id", "title", "layer", "language", "translator", "source_url", "license", "license_tier", "notes"]},
    )


def ingest_bsb(con):
    """bereanbible.com/bsb.txt — 'Genesis 1:1<TAB>text', 3 header lines."""
    path = os.path.join(SRC, "bsb.txt")
    add_document(con, id="BSB", title="Berean Standard Bible", layer="canon", language="en",
                 translator="Berean Bible Translation Committee", source_url="https://berean.bible",
                 license="Public Domain", license_tier="A",
                 notes="Public domain as of 2023-04-30. 66 books.")
    line_re = re.compile(r"^(.+?) (\d+):(\d+)\t(.*)$")
    rows, seq, skipped = [], 0, []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            m = line_re.match(line.rstrip("\n"))
            if not m:
                continue
            name, ch, v, text = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4).strip()
            book = book_to_osis(name)
            if not book:
                skipped.append(name)
                continue
            if not text or text in ("-", "[[BLANK]]"):
                continue  # critical-text omitted verses ship empty
            seq += 1
            rows.append(("BSB", make_ref(book, ch, v), book, ch, v, seq, text))
    con.executemany("INSERT INTO passages(doc_id,ref,book,chapter,verse,seq,text) VALUES(?,?,?,?,?,?,?)", rows)
    if skipped:
        print(f"  BSB: skipped unknown books: {sorted(set(skipped))}")
    print(f"  BSB: {len(rows)} verses")


def ingest_web(con):
    """eBible.org eng-web VPL — 'GEN 1:1 text' (ecumenical edition incl. Apocrypha)."""
    path = os.path.join(SRC, "eng-web_vpl", "eng-web_vpl.txt")
    add_document(con, id="WEB", title="World English Bible (Ecumenical)", layer="canon", language="en",
                 translator="Michael Paul Johnson (ed.), rev. of ASV 1901", source_url="https://ebible.org/eng-web/",
                 license="Public Domain", license_tier="A",
                 notes="Includes full Apocrypha/Deuterocanon (83 books). 'World English Bible' is trademarked; text is PD.")
    line_re = re.compile(r"^([0-9A-Z]{3}) (\d+):(\d+)\s+(.*)$")
    rows, seq, skipped = [], 0, set()
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            m = line_re.match(line.rstrip("\n"))
            if not m:
                continue
            code, ch, v, text = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4).strip()
            book = PARATEXT_TO_OSIS.get(code)
            if not book:
                skipped.add(code)
                continue
            if not text:
                continue
            seq += 1
            rows.append(("WEB", make_ref(book, ch, v), book, ch, v, seq, text))
    con.executemany("INSERT INTO passages(doc_id,ref,book,chapter,verse,seq,text) VALUES(?,?,?,?,?,?,?)", rows)
    if skipped:
        print(f"  WEB: skipped unknown book codes: {sorted(skipped)}")
    print(f"  WEB: {len(rows)} verses")


def _lxx_psalm_group(chapter, verse):
    """Map a Brenton (native LXX) Psalm chapter/verse to its (book, chapter) group in
    the canonical English/KJV-style numbering BSB/WEB use. LXX merges MT/English Ps
    9+10 into one psalm and splits MT/English Ps 116 and 147 each into two; final verse
    numbers are assigned sequentially within each group afterward (not by arithmetic on
    Brenton's own verse labels, which have irregularities like '115:4a' that don't
    survive remapping cleanly). Every boundary here was verified against WEB's text,
    not just against the standard scholarly correspondence (see chat)."""
    if chapter <= 8:
        return ("Ps", chapter)
    if chapter == 9:
        return ("Ps", 9) if verse <= 21 else ("Ps", 10)
    if chapter <= 112:
        return ("Ps", chapter + 1)
    if chapter == 113:
        return ("Ps", 114) if verse <= 8 else ("Ps", 115)
    if chapter in (114, 115):
        return ("Ps", 116)
    if chapter <= 145:
        return ("Ps", chapter + 1)
    if chapter in (146, 147):
        return ("Ps", 147)
    if chapter <= 150:
        return ("Ps", chapter)
    if chapter == 151:
        return ("PSX", 1)
    raise ValueError(f"Unexpected LXX Psalm chapter: {chapter}")


def ingest_brenton(con):
    """eBible.org eng-Brenton VPL — Brenton's 1851 English Septuagint (LXX), OT +
    Apocrypha only (no NT). Psalms are remapped to the canonical English/KJV-style
    chapter/verse numbering BSB/WEB share (LXX's own numbering diverges throughout
    most of the Psalter — see _lxx_psalm_group). Other divergent books (Jeremiah's
    relocated/shorter oracles-against-nations section, Daniel-Greek, Exodus, Job,
    Esther-Greek, Baruch) ship under Brenton's own native LXX chapter/verse structure;
    full alignment for those stays deferred, same status as TVTMS proper (ROADMAP.md)."""
    path = os.path.join(SRC, "eng-brenton_vpl", "eng-Brenton_vpl.txt")
    add_document(
        con, id="LXX", title="Septuagint (Brenton Translation)", layer="canon", language="en",
        translator="Sir Lancelot C. L. Brenton", source_url="https://ebible.org/eng-Brenton/",
        license="Public Domain", license_tier="A",
        notes="Published 1851. Old Testament + Apocrypha only (no NT). Psalms remapped to "
              "standard English/KJV numbering; Jeremiah, Daniel-Greek, Exodus, Job, "
              "Esther-Greek, and Baruch retain Brenton's native LXX chapter/verse "
              "structure, which diverges from BSB/WEB in these books (reordering and/or "
              "length, not just numbering) — full alignment deferred, see ROADMAP.md.")
    # LXX Joshua/Judges/Kings especially carry well-documented "plus" material —
    # extra verses the Hebrew/English tradition lacks, labeled with a letter suffix
    # in the source (e.g. '1KI 2:35a'..'2:35o', fifteen extra verses after 2:35).
    # The letter is captured and preserved in `ref` (distinct, citable addresses);
    # `verse` stays the base integer since it's just used for range lookups, and
    # `seq` (not `verse`) is what preserves true reading order.
    line_re = re.compile(r"^([0-9A-Z]{3}) (\d+):(\d+)([a-z]?)\s+(.*)$")

    entries = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            m = line_re.match(line.rstrip("\n"))
            if not m:
                continue
            code, ch, v, letter, text = (
                m.group(1), int(m.group(2)), int(m.group(3)), m.group(4), m.group(5).strip())
            if not text:
                continue
            if code == "EZR" and ch > 10:
                continue  # chs 11-23 duplicate Nehemiah (LXX "Esdras B"); the standalone
                          # NEH below is conventionally numbered and used instead
            entries.append((code, ch, v, letter, text))

    rows, seq, skipped = [], 0, set()
    psa_groups = {}

    def flush_psalms():
        nonlocal seq
        for (book, ch), texts in psa_groups.items():
            if book == "Ps":
                # Same superscription-as-verse-1 pattern compute_psalm_offsets() already
                # fixes for the Hebrew side: Brenton counts some psalm superscriptions as
                # their own verse(s) (usually 1, but longer historical superscriptions —
                # Ps 51/52/54/60 — split across 2), where BSB folds the whole thing into
                # verse 1's text. Detect via BSB's actual verse count (already ingested)
                # and merge the leading extra lines to match — not drop, no content lost.
                bsb_max = con.execute(
                    "SELECT MAX(verse) FROM passages WHERE doc_id='BSB' AND book='Ps' AND chapter=?",
                    (ch,)).fetchone()[0]
                extra = len(texts) - bsb_max if bsb_max else 0
                if extra > 0:
                    texts = [" ".join(texts[:extra + 1])] + texts[extra + 1:]
            for i, text in enumerate(texts, start=1):
                seq += 1
                rows.append(("LXX", make_ref(book, ch, i), book, ch, i, seq, text))
        psa_groups.clear()

    for code, ch, v, letter, text in entries:
        if code == "PSA":
            psa_groups.setdefault(_lxx_psalm_group(ch, v), []).append(text)
            continue
        if psa_groups:
            flush_psalms()
        book = PARATEXT_TO_OSIS.get(code)
        if not book:
            skipped.add(code)
            continue
        seq += 1
        rows.append(("LXX", make_ref(book, ch, v) + letter, book, ch, v, seq, text))
    flush_psalms()

    con.executemany("INSERT INTO passages(doc_id,ref,book,chapter,verse,seq,text) VALUES(?,?,?,?,?,?,?)", rows)
    if skipped:
        print(f"  LXX: skipped unknown book codes: {sorted(skipped)}")
    print(f"  LXX: {len(rows)} verses")


def ingest_crossrefs(con):
    """openbible.info cross_references.txt — 'From<TAB>To<TAB>Votes'."""
    path = os.path.join(SRC, "cross-references", "cross_references.txt")
    rows = []
    with open(path, encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            frm, to, votes = parts[0], parts[1], parts[2]
            try:
                w = float(votes)
            except ValueError:
                continue
            rows.append((frm, to, "cross_reference", w, "openbible.info CC-BY"))
    con.executemany("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)", rows)
    print(f"  cross-references: {len(rows)} links")


def ingest_theographic(con):
    """Theographic Bible metadata (CC BY-SA 4.0): people, places, events + verse mentions."""
    tdir = os.path.join(SRC, "theographic-json")
    verses = json.load(open(os.path.join(tdir, "verses.json")))
    rec_to_ref = {v["id"]: v["fields"].get("osisRef") for v in verses if v.get("fields", {}).get("osisRef")}

    def load(fname, etype, name_field, slug_field=None, desc_field=None):
        items = json.load(open(os.path.join(tdir, fname)))
        ents, mentions = [], []
        for it in items:
            f = it.get("fields", {})
            name = f.get(name_field)
            if not name:
                continue
            keep = {k: v for k, v in f.items() if not isinstance(v, list) or k in ("aliases",)}

            def _s(val):
                if val is None:
                    return None
                if isinstance(val, list):
                    return " ".join(str(x) for x in val) or None
                return str(val)

            ents.append((it["id"], etype, str(name), _s(f.get(slug_field)) if slug_field else None,
                         _s(f.get(desc_field)) if desc_field else None, json.dumps(keep)))
            for vrec in f.get("verses", []) or []:
                ref = rec_to_ref.get(vrec)
                if ref:
                    mentions.append((it["id"], ref))
        con.executemany("INSERT OR IGNORE INTO entities(id,type,name,slug,description,data) VALUES(?,?,?,?,?,?)", ents)
        con.executemany("INSERT OR IGNORE INTO entity_mentions(entity_id,ref) VALUES(?,?)", mentions)
        print(f"  theographic {etype}: {len(ents)} entities, {len(mentions)} mentions")

    load("people.json", "person", "name", slug_field="personLookup", desc_field="dictText")
    load("places.json", "place", "kjvName", slug_field="placeLookup", desc_field="comment")
    load("peopleGroups.json", "people_group", "groupName")

    # events: verse + participant links kept in data JSON, mentions resolved
    events = json.load(open(os.path.join(tdir, "events.json")))
    ents, mentions = [], []
    for it in events:
        f = it.get("fields", {})
        title = f.get("title")
        if not title:
            continue
        data = {"startDate": f.get("startDate"), "duration": f.get("duration"),
                "participants": f.get("participants", []), "predecessor": f.get("predecessor")}
        ents.append((it["id"], "event", title, None, None, json.dumps(data)))
        for vrec in f.get("verses", []) or []:
            ref = rec_to_ref.get(vrec)
            if ref:
                mentions.append((it["id"], ref))
    con.executemany("INSERT OR IGNORE INTO entities(id,type,name,slug,description,data) VALUES(?,?,?,?,?,?)", ents)
    con.executemany("INSERT OR IGNORE INTO entity_mentions(entity_id,ref) VALUES(?,?)", mentions)
    print(f"  theographic event: {len(ents)} entities, {len(mentions)} mentions")


_WORD_REF = re.compile(r"^([0-9A-Z]{3}) (\d+):(\d+)!(\d+)$")


def _macula_ref(raw):
    m = _WORD_REF.match(raw)
    if not m:
        return None, None
    book = PARATEXT_TO_OSIS.get(m.group(1))
    if not book:
        return None, None
    return f"{book}.{int(m.group(2))}.{int(m.group(3))}", int(m.group(4))


def ingest_macula(con):
    """MACULA Greek (Nestle1904) + Hebrew (WLC) word-level TSVs — CC BY 4.0 (Biblica/Clear-Bible)."""
    import csv
    csv.field_size_limit(10_000_000)
    add_document(con, id="MACULA-GRC", title="MACULA Greek (Nestle1904 word data)", layer="reference",
                 language="grc", translator=None, source_url="https://github.com/Clear-Bible/macula-greek",
                 license="CC BY 4.0", license_tier="A", notes="Word-level: lemma, Strong's, morphology, glosses, Louw-Nida domains.")
    add_document(con, id="MACULA-HEB", title="MACULA Hebrew (WLC word data)", layer="reference",
                 language="hbo", translator=None, source_url="https://github.com/Clear-Bible/macula-hebrew",
                 license="CC BY 4.0", license_tier="A", notes="Word-level: lemma, Strong's, morphology, glosses, SDBH domains.")

    def rows_from(path, is_greek):
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                ref, pos = _macula_ref(r.get("ref", ""))
                if not ref:
                    continue
                if is_greek:
                    strong = ("G" + r["strong"]) if r.get("strong") else None
                    yield (ref, pos, "grc", r.get("text"), None, r.get("lemma"), strong,
                           r.get("gloss") or r.get("english"), r.get("english"), r.get("morph"),
                           r.get("domain"), r.get("ln"))
                else:
                    lang = {"H": "hbo", "A": "arc"}.get(r.get("lang", "H"), "hbo")
                    sn = r.get("strongnumberx") or ""
                    strong = ("H" + sn) if sn else None
                    yield (ref, pos, lang, r.get("text"), r.get("transliteration"), r.get("lemma"), strong,
                           r.get("gloss") or r.get("english"), r.get("english"), r.get("morph"),
                           r.get("sdbh") or r.get("lexdomain"), None)

    for path, is_greek, label in [
        (os.path.join(SRC, "macula-greek-Nestle1904.tsv"), True, "Greek"),
        (os.path.join(SRC, "macula-hebrew.tsv"), False, "Hebrew"),
    ]:
        batch, n = [], 0
        for row in rows_from(path, is_greek):
            batch.append(row)
            if len(batch) >= 20000:
                con.executemany(
                    "INSERT INTO words(ref,pos,lang,surface,translit,lemma,strong,gloss,english,morph,domain,ln) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", batch)
                n += len(batch)
                batch = []
        if batch:
            con.executemany(
                "INSERT INTO words(ref,pos,lang,surface,translit,lemma,strong,gloss,english,morph,domain,ln) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", batch)
            n += len(batch)
        print(f"  MACULA {label}: {n} words")


GUTENBERG_SHELF = [
    # (gutenberg_id, doc_id, title, author/translator, layer)
    (3296, "CONFESSIONS", "The Confessions of St. Augustine", "tr. E. B. Pusey", "patristic"),
    (1653, "IMITATION", "The Imitation of Christ (Thomas à Kempis)", "tr. William Benham", "mystic"),
    (131, "PILGRIM", "The Pilgrim's Progress (John Bunyan)", "John Bunyan", "classic"),
    (5657, "PRESENCE", "The Practice of the Presence of God (Brother Lawrence)", "1895 translation", "mystic"),
    (52958, "JULIAN", "Revelations of Divine Love (Julian of Norwich)", "ed. Grace Warrack", "mystic"),
    (16769, "ORTHODOXY", "Orthodoxy (G. K. Chesterton)", "G. K. Chesterton", "classic"),
]

_CHAPTER_RE = re.compile(
    r"^(BOOK|CHAPTER|CHAP\.|PART|LETTER|SECTION)\s+[IVXLC0-9]+\b.*$|^[IVXLC]+\.?\s*$|^CHAPTER\s+\w+", re.I)
_FOOTNOTE_BLOCK_RE = re.compile(r"Footnote (\d+):\s*\n\s*\n(.*?)(?=\nFootnote \d+:|\Z)", re.S)
_MARKER_RE = re.compile(r"\[(\d+)\]")

PATRISTIC_SHELF = [
    # (start_line, end_line, doc_id, title, author) — 1-indexed into pg77576.txt, end exclusive
    (281, 2688, "1CLEMENT", "The First Epistle of Clement to the Corinthians", "Clement of Rome"),
    (4631, 6790, "BARNABAS", "The Epistle of Barnabas", "Pseudo-Barnabas"),
]


def ingest_patristic_gutenberg(con):
    """Apostolic Fathers (Roberts-Donaldson-Crombie translation, ANF vol. 1),
    Project Gutenberg #77576, Public Domain. Addressing: DOC.chapter.paragraph,
    same pattern as the Gutenberg classics. Also extracts tier-1 scripture
    citations from the translators' own footnotes into the links table
    (see DESIGN.md §4 — this is the free, high-confidence tier)."""
    path = os.path.join(SRC, "gutenberg", "pg77576.txt")
    lines = open(path, encoding="utf-8-sig").read().split("\n")

    for start_line, end_line, doc_id, title, author in PATRISTIC_SHELF:
        raw = "\n".join(lines[start_line - 1:end_line - 1])
        add_document(con, id=doc_id, title=title, layer="patristic", language="en",
                     translator="Roberts, Donaldson & Crombie (Ante-Nicene Fathers)",
                     source_url="https://www.gutenberg.org/ebooks/77576",
                     license="Public Domain", license_tier="A",
                     notes=f"Author: {author}. Project Gutenberg #77576. Tier-1 scripture citations "
                           "extracted from the translators' own footnotes.")

        footnote_text = {}

        def _capture(m):
            footnote_text[int(m.group(1))] = m.group(2).strip()
            return ""

        body = _FOOTNOTE_BLOCK_RE.sub(_capture, raw)
        paras = re.split(r"\n\s*\n", body)
        chapter, para_n, seq, rows = 1, 0, 0, []
        marker_ref = {}
        for p in paras:
            text = " ".join(p.split())
            if not text:
                continue
            head = p.strip().splitlines()[0].strip()
            if _CHAPTER_RE.match(head) and len(text) < 200:
                if para_n > 0:
                    chapter += 1
                para_n = 0
                continue
            if len(text) < 40:
                continue
            if re.search(r"\.{5,}", text) or text.isupper():
                continue
            para_n += 1
            seq += 1
            ref = f"{doc_id}.{chapter}.{para_n}"
            for num in _MARKER_RE.findall(text):
                marker_ref[int(num)] = ref
            text = _MARKER_RE.sub("", text)
            text = re.sub(r"\s+([,.;:])", r"\1", text).strip()
            rows.append((doc_id, ref, doc_id, chapter, para_n, seq, text))
        con.executemany("INSERT INTO passages(doc_id,ref,book,chapter,verse,seq,text) VALUES(?,?,?,?,?,?,?)", rows)

        link_rows = []
        for num, txt in footnote_text.items():
            from_ref = marker_ref.get(num)
            if not from_ref:
                continue
            for to_ref in parse_scripture_citations(txt):
                link_rows.append((from_ref, to_ref, "citation", 1.0,
                                  "ANF footnote (Roberts-Donaldson-Crombie translation)"))
        con.executemany("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)", link_rows)
        print(f"  {doc_id}: {len(rows)} paragraphs in {chapter} chapters, {len(link_rows)} scripture citations captured")


def ingest_gutenberg(con):
    """PD classics from Project Gutenberg. Addressing: DOC.chapter.paragraph.
    Gutenberg boilerplate is stripped (their trademark terms); text itself is PD."""
    for gid, doc_id, title, translator, layer in GUTENBERG_SHELF:
        path = os.path.join(SRC, "gutenberg", f"pg{gid}.txt")
        raw = open(path, encoding="utf-8-sig").read()
        # strip Gutenberg header/footer
        m1 = re.search(r"\*\*\* ?START OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", raw)
        m2 = re.search(r"\*\*\* ?END OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", raw)
        body = raw[m1.end() if m1 else 0: m2.start() if m2 else len(raw)]
        add_document(con, id=doc_id, title=title, layer=layer, language="en", translator=translator,
                     source_url=f"https://www.gutenberg.org/ebooks/{gid}",
                     license="Public Domain", license_tier="A",
                     notes=f"Project Gutenberg #{gid}; boilerplate stripped per PG trademark terms.")
        paras = re.split(r"\n\s*\n", body)
        has_headings = any(_CHAPTER_RE.match(p.strip().splitlines()[0].strip())
                            for p in paras if p.strip())
        chapter, para_n, seq, rows = 1, 0, 0, []
        body_started = not has_headings   # if no headings exist, nothing to skip as "front matter"
        for p in paras:
            text = " ".join(p.split())
            if not text:
                continue
            head = p.strip().splitlines()[0].strip()
            if _CHAPTER_RE.match(head) and len(text) < 200:
                if para_n > 0:          # only advance if current chapter has content
                    chapter += 1
                para_n = 0
                body_started = True     # first heading marks end of front matter
                continue
            if not body_started:        # drop title page / translator credit / TOC before ch. 1
                continue
            if len(text) < 40:      # skip TOC lines, page furniture
                continue
            if re.search(r"\.{5,}", text) or text.isupper():  # TOC dotted leaders, shout-case headings
                continue
            para_n += 1
            seq += 1
            rows.append((doc_id, f"{doc_id}.{chapter}.{para_n}", doc_id, chapter, para_n, seq, text))
        con.executemany("INSERT INTO passages(doc_id,ref,book,chapter,verse,seq,text) VALUES(?,?,?,?,?,?,?)", rows)
        print(f"  {doc_id}: {len(rows)} paragraphs in {chapter} chapters")


def compute_psalm_offsets(con):
    """Fix the classic Psalms superscription-versification mismatch: the Masoretic
    Hebrew (and thus MACULA's word-level data) numbers the superscription as verse 1
    for ~62 psalms, while English translations (BSB/WEB) fold it into verse 1 without
    a separate number. Derived empirically from data already in the DB — no external
    TVTMS import needed for this specific, well-scoped case (see chat: full TVTMS
    stays deferred; only Psalms needs this today)."""
    con.execute("CREATE TABLE IF NOT EXISTS psalm_offsets (chapter INTEGER PRIMARY KEY, offset INTEGER NOT NULL)")
    con.execute("DELETE FROM psalm_offsets")
    heb_max = {}
    for (ref,) in con.execute("SELECT DISTINCT ref FROM words WHERE ref LIKE 'Ps.%'"):
        _, ch, v = ref.split(".")
        ch, v = int(ch), int(v)
        heb_max[ch] = max(heb_max.get(ch, 0), v)
    bsb_max = dict(con.execute(
        "SELECT chapter, MAX(verse) FROM passages WHERE doc_id='BSB' AND book='Ps' GROUP BY chapter"))
    rows = [(ch, heb_max[ch] - bsb_max[ch]) for ch in heb_max
            if bsb_max.get(ch) and heb_max[ch] != bsb_max[ch]]
    con.executemany("INSERT INTO psalm_offsets(chapter, offset) VALUES(?,?)", rows)
    print(f"  Psalm versification offsets: {len(rows)} psalms corrected (superscription shift)")


def load_versemap(con):
    """Load the prepared data/versemap.tsv (MT/NA <-> English refs, empirically derived
    and gloss-validated by build_versemap.py + align_splits.py) into the `versemap`
    table. Not part of schema.sql: server.py checks for the table at runtime and
    degrades gracefully without it, but a full rebuild should still restore it."""
    path = os.path.join(ROOT, "data", "versemap.tsv")
    con.execute(
        "CREATE TABLE IF NOT EXISTS versemap "
        "(scheme TEXT NOT NULL, src_ref TEXT NOT NULL, dst_ref TEXT NOT NULL, note TEXT)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_versemap_src ON versemap(src_ref)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_versemap_dst ON versemap(dst_ref)")
    con.execute("DELETE FROM versemap")
    rows = []
    with open(path, encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 4:
                rows.append(tuple(parts))
    con.executemany("INSERT INTO versemap(scheme,src_ref,dst_ref,note) VALUES(?,?,?,?)", rows)
    print(f"  versemap: {len(rows)} rows")


def main():
    con = fresh_db()
    print("Ingesting…")
    ingest_bsb(con)
    ingest_web(con)
    ingest_brenton(con)
    ingest_crossrefs(con)
    ingest_theographic(con)
    ingest_macula(con)
    ingest_gutenberg(con)
    ingest_patristic_gutenberg(con)
    compute_psalm_offsets(con)
    load_versemap(con)
    con.commit()
    con.execute("INSERT INTO passages_fts(passages_fts) VALUES('optimize')")
    con.commit()
    n = con.execute("SELECT COUNT(*) FROM passages").fetchone()[0]
    print(f"Done. {n} passages -> {DB}")


if __name__ == "__main__":
    main()
