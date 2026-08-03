"""bible-mcp — MCP server for Christian scholarship and research.

Corpus: BSB + WEB (with Apocrypha), OpenBible cross-references, Theographic entities.
Run:  uv run server.py   (or: python3 server.py, with `mcp` installed)
"""
import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from lib_refs import parse_ref, OSIS_TO_NAME  # noqa: E402

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

DB = os.environ.get(
    "BIBLE_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "bible.db"),
)

mcp = FastMCP("bible-mcp")


def _db():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def _expand_range_ref(ref: str):
    """'Gen.1.26-Gen.1.27' or 'Gen.1.26' -> list of concrete refs (same book+chapter only)."""
    if "-" not in ref:
        return [ref]
    a, b = ref.split("-", 1)
    try:
        ab, ac, av = a.split(".")
        bb, bc, bv = b.split(".")
        if ab == bb and ac == bc:
            return [f"{ab}.{ac}.{v}" for v in range(int(av), int(bv) + 1)]
    except ValueError:
        pass
    return [a, b]


@mcp.tool()
def get_passage(reference: str, version: str = "BSB") -> str:
    """Get Bible text for a reference like 'John 3:16', 'John 3:16-18', 'Genesis 1',
    or 'Tobit 4:5' (Apocrypha requires version='WEB'). Versions: BSB, WEB."""
    book, ch, v1, v2 = parse_ref(reference)
    con = _db()
    if v1 is None:
        rows = con.execute(
            "SELECT ref, verse, text FROM passages WHERE doc_id=? AND book=? AND chapter=? ORDER BY verse",
            (version.upper(), book, ch)).fetchall()
    else:
        rows = con.execute(
            "SELECT ref, verse, text FROM passages WHERE doc_id=? AND book=? AND chapter=? AND verse BETWEEN ? AND ? ORDER BY verse",
            (version.upper(), book, ch, v1, v2)).fetchall()
    con.close()
    if not rows:
        hint = " (Apocrypha books are only in version='WEB')" if version.upper() == "BSB" else ""
        return f"No text found for {reference} in {version}.{hint}"
    header = f"{OSIS_TO_NAME.get(book, book)} {ch} ({version.upper()})"
    body = "\n".join(f"{r['verse']}. {r['text']}" for r in rows)
    return f"{header}\n{body}"


@mcp.tool()
def search(query: str, version: str = "BSB", book: str = "", limit: int = 20) -> str:
    """Full-text search (stemmed, ranked). Supports phrases in quotes, AND/OR/NOT,
    e.g. 'living water', 'faith AND works NOT law'. Optional book filter e.g. 'Psalms'.
    NOTE: porter stemming conflates related surface forms — 'desert' also matches
    'deserted' and 'deserts' (as merits) in prose layers; quote exact phrases or
    add AND-terms to disambiguate."""
    con = _db()
    sql = ("SELECT p.ref, p.text FROM passages_fts f JOIN passages p ON p.id=f.rowid "
           "WHERE passages_fts MATCH ? AND p.doc_id=?")
    args = [query, version.upper()]
    if book:
        b, *_ = parse_ref(book + " 1")
        sql += " AND p.book=?"
        args.append(b)
    sql += " ORDER BY rank LIMIT ?"
    args.append(max(1, min(int(limit), 100)))
    try:
        rows = con.execute(sql, args).fetchall()
    except sqlite3.OperationalError as e:
        con.close()
        return f"Search syntax error: {e}"
    con.close()
    if not rows:
        return f"No matches for {query!r} in {version}."
    return "\n".join(f"[{r['ref']}] {r['text']}" for r in rows)


@mcp.tool()
def get_cross_references(reference: str, limit: int = 20) -> str:
    """Cross-references for a verse (OpenBible.info, ranked by community votes),
    with the target text included. E.g. reference='Romans 5:12'."""
    book, ch, v1, _ = parse_ref(reference)
    if v1 is None:
        return "Please give a specific verse, e.g. 'Romans 5:12'."
    ref = f"{book}.{ch}.{v1}"
    con = _db()
    rows = con.execute(
        "SELECT to_ref, weight FROM links WHERE from_ref=? AND type='cross_reference' "
        "ORDER BY weight DESC LIMIT ?", (ref, max(1, min(int(limit), 100)))).fetchall()
    out = [f"Cross-references for {ref}:"]
    for r in rows:
        targets = _expand_range_ref(r["to_ref"])
        texts = []
        for t in targets[:3]:
            row = con.execute(
                "SELECT text FROM passages WHERE doc_id='BSB' AND ref=? "
                "UNION SELECT text FROM passages WHERE doc_id='WEB' AND ref=? LIMIT 1",
                (t, t)).fetchone()
            if row:
                texts.append(row["text"])
        joined = " ".join(texts) if texts else "(text not in corpus)"
        out.append(f"[{r['to_ref']}] (votes: {int(r['weight'])}) {joined}")
    con.close()
    if len(out) == 1:
        return f"No cross-references found for {ref}."
    return "\n".join(out)


@mcp.tool()
def get_entity(name: str, entity_type: str = "") -> str:
    """Look up a biblical person, place, event, or people group by name
    (Theographic knowledge graph). Returns details and where they appear.
    entity_type optional: person | place | event | people_group."""
    con = _db()
    sql = "SELECT * FROM entities WHERE (name LIKE ? OR slug LIKE ?)"
    args = [name, name.lower().replace(" ", "_") + "%"]
    if entity_type:
        sql += " AND type=?"
        args.append(entity_type)
    rows = con.execute(sql + " LIMIT 5", args).fetchall()
    if not rows:
        rows = con.execute(
            "SELECT * FROM entities WHERE name LIKE ? " + ("AND type=? " if entity_type else "") + "LIMIT 5",
            ([f"%{name}%"] + ([entity_type] if entity_type else []))).fetchall()
    if not rows and len(name) >= 4:
        # spelling variants (Melchizedek vs Melchisedec): prefix match on the stem
        rows = con.execute(
            "SELECT * FROM entities WHERE name LIKE ? " + ("AND type=? " if entity_type else "") + "LIMIT 5",
            ([name[:4] + "%"] + ([entity_type] if entity_type else []))).fetchall()
    if not rows:
        con.close()
        return f"No entity found matching {name!r}."
    out = []
    for r in rows:
        data = json.loads(r["data"] or "{}")
        head = f"{r['name']} ({r['type']}, id={r['id']})"
        details = []
        for k in ("gender", "birthYear", "deathYear", "startDate", "duration",
                  "openBibleLat", "openBibleLong", "featureType", "aliases"):
            if data.get(k):
                details.append(f"{k}={data[k]}")
        mentions = con.execute(
            "SELECT ref FROM entity_mentions WHERE entity_id=? LIMIT 12", (r["id"],)).fetchall()
        n = con.execute(
            "SELECT COUNT(*) c FROM entity_mentions WHERE entity_id=?", (r["id"],)).fetchone()["c"]
        refs = ", ".join(m["ref"] for m in mentions)
        desc = (r["description"] or "").strip()
        if len(desc) > 400:
            desc = desc[:400] + "…"
        block = head
        if details:
            block += "\n  " + "; ".join(str(d) for d in details)
        if desc:
            block += f"\n  {desc}"
        block += f"\n  Mentions ({n} total): {refs}{'…' if n > 12 else ''}"
        out.append(block)
    con.close()
    return "\n\n".join(out)


@mcp.tool()
def entities_in_passage(reference: str) -> str:
    """List the people, places, and events linked to a verse or chapter,
    e.g. 'Genesis 14' or 'John 3:16'."""
    book, ch, v1, v2 = parse_ref(reference)
    con = _db()
    if v1 is None:
        refs_rows = con.execute(
            "SELECT DISTINCT ref FROM passages WHERE book=? AND chapter=?", (book, ch)).fetchall()
    else:
        refs_rows = [{"ref": f"{book}.{ch}.{v}"} for v in range(v1, (v2 or v1) + 1)]
    refs = [r["ref"] for r in refs_rows]
    if not refs:
        con.close()
        return f"No passages found for {reference}."
    q = ",".join("?" * len(refs))
    rows = con.execute(
        f"SELECT e.type, e.name, COUNT(*) c FROM entity_mentions m JOIN entities e ON e.id=m.entity_id "
        f"WHERE m.ref IN ({q}) GROUP BY e.id ORDER BY e.type, c DESC", refs).fetchall()
    con.close()
    if not rows:
        return f"No linked entities for {reference}."
    out = [f"Entities in {reference}:"]
    cur = None
    for r in rows:
        if r["type"] != cur:
            cur = r["type"]
            out.append(f"\n{cur.upper()}S:")
        out.append(f"  {r['name']} ({r['c']} verse{'s' if r['c'] > 1 else ''})")
    return "\n".join(out)


@mcp.tool()
def compare_versions(reference: str) -> str:
    """Show a verse or short range in both BSB and WEB side by side."""
    book, ch, v1, v2 = parse_ref(reference)
    if v1 is None:
        v1, v2 = 1, 999
    con = _db()
    out = []
    for ver in ("BSB", "WEB"):
        rows = con.execute(
            "SELECT verse, text FROM passages WHERE doc_id=? AND book=? AND chapter=? AND verse BETWEEN ? AND ? ORDER BY verse",
            (ver, book, ch, v1, v2 or v1)).fetchall()
        if rows:
            body = "\n".join(f"  {r['verse']}. {r['text']}" for r in rows)
            out.append(f"{ver}:\n{body}")
    con.close()
    return "\n\n".join(out) if out else f"Nothing found for {reference}."


_COMBINING = re.compile(r"[֑-ׇ̀-ͯ᷀-᷿]")
_lemma_index = {"map": None}


def _strip_marks(s):
    import unicodedata
    return _COMBINING.sub("", unicodedata.normalize("NFD", s or ""))


def _lemma_candidates(con, q):
    """Match a lemma query ignoring Hebrew niqqud / Greek accents: 'יצר' or 'αγαπη'
    finds the pointed/accented lemmas as stored."""
    if _lemma_index["map"] is None:
        m = {}
        for (lem,) in con.execute("SELECT DISTINCT lemma FROM words WHERE lemma IS NOT NULL"):
            m.setdefault(_strip_marks(lem), set()).add(lem)
        _lemma_index["map"] = m
    return sorted(_lemma_index["map"].get(_strip_marks(q.strip()), set()))


@mcp.tool()
def word_study(query: str, language: str = "", limit: int = 15) -> str:
    """Original-language word study across the whole Bible. Query by Strong's number
    ('G26', 'H2617', zero-padding optional — 'H953' works), lemma (pointed or
    unpointed: 'חֶסֶד' or 'חסד', accented or bare Greek), or English gloss
    ('lovingkindness'). Returns occurrence counts, gloss range, book distribution,
    and sample verses. NOTE: homographs are split by letter-suffixed Strong's
    variants (e.g. H4723 'hope' vs H4723a 'gathering of waters' — same written
    form) — when a gloss range looks too narrow for a word you suspect is richer,
    probe the lettered variants; the output lists every variant lemma it finds
    under your query. Gloss-keyed queries match substrings and may conflate
    lemmas — prefer Strong's or lemma queries for exact counts.
    language optional: grc | hbo | arc."""
    con = _db()
    q = query.strip()
    where, args = None, None
    m = re.fullmatch(r"([GgHh])0*(\d+)([a-c]?)", q)
    if m:
        # zero-pad to the 4-digit storage form; if a bare number has lettered
        # variants, include them all so homographs are visible side by side.
        base = f"{m.group(1).upper()}{int(m.group(2)):04d}"
        if m.group(3):
            where, args = "strong = ?", [base + m.group(3)]
        else:
            where, args = "(strong = ? OR (strong LIKE ? AND length(strong) = ?))", \
                          [base, base + "_", len(base) + 1]
    else:
        where, args = "lemma = ?", [q]
        if not con.execute(f"SELECT 1 FROM words WHERE {where} LIMIT 1", args).fetchone():
            cands = _lemma_candidates(con, q)
            if cands:
                where = "lemma IN (" + ",".join("?" * len(cands)) + ")"
                args = cands
            else:
                where, args = "(gloss LIKE ? OR english LIKE ?)", [f"%{q}%", f"%{q}%"]
    if language:
        where += " AND lang = ?"
        args.append(language)
    total = con.execute(f"SELECT COUNT(*) c FROM words WHERE {where}", args).fetchone()["c"]
    if not total:
        con.close()
        return f"No occurrences found for {query!r}."
    lemmas = con.execute(
        f"SELECT lemma, strong, lang, COUNT(*) c FROM words WHERE {where} "
        "GROUP BY lemma, strong ORDER BY c DESC LIMIT 8", args).fetchall()
    glosses = con.execute(
        f"SELECT gloss, COUNT(*) c FROM words WHERE {where} AND gloss IS NOT NULL "
        "GROUP BY lower(gloss) ORDER BY c DESC LIMIT 10", args).fetchall()
    books = con.execute(
        f"SELECT substr(ref,1,instr(ref,'.')-1) b, COUNT(*) c FROM words WHERE {where} "
        "GROUP BY b ORDER BY c DESC LIMIT 12", args).fetchall()
    samples = con.execute(
        f"SELECT DISTINCT w.ref FROM words w WHERE {where} LIMIT ?", args + [max(1, min(int(limit), 40))]).fetchall()
    out = [f"Word study: {query} — {total} occurrences"]
    out.append("Lemmas: " + "; ".join(f"{r['lemma']} ({r['strong']}, {r['lang']}, {r['c']}x)" for r in lemmas))
    out.append("Gloss range: " + "; ".join(f"{r['gloss']} ({r['c']})" for r in glosses if r["gloss"]))
    out.append("Distribution: " + ", ".join(f"{r['b']} {r['c']}" for r in books))
    out.append("Sample verses:")
    for s in samples:
        display_ref = _display_ref_for_heb_ref(con, s["ref"])
        row = con.execute("SELECT text FROM passages WHERE doc_id='BSB' AND ref=? "
                          "UNION SELECT text FROM passages WHERE doc_id='WEB' AND ref=? LIMIT 1",
                          (display_ref, display_ref)).fetchone()
        label = s["ref"] if display_ref == s["ref"] else f"{s['ref']} = {display_ref}"
        out.append(f"  [{label}] {row['text'] if row else ''}")
    con.close()
    return "\n".join(out)


@mcp.tool()
def get_interlinear(reference: str) -> str:
    """Word-by-word original language for a verse or short range: surface form,
    lemma, Strong's, gloss, morphology. E.g. 'John 1:1' or 'Genesis 1:1-3'."""
    book, ch, v1, v2 = parse_ref(reference)
    if v1 is None:
        v1, v2 = 1, 3
    con = _db()
    out = []
    for v in range(v1, (v2 or v1) + 1):
        ref = f"{book}.{ch}.{v}"
        heb_refs = _heb_refs_for_display_verse(con, book, ch, v)
        rows = []
        for hr in heb_refs:
            rows.extend(con.execute("SELECT * FROM words WHERE ref=? ORDER BY pos", (hr,)).fetchall())
        if not rows:
            continue
        eng = con.execute("SELECT text FROM passages WHERE doc_id='BSB' AND ref=? "
                          "UNION SELECT text FROM passages WHERE doc_id='WEB' AND ref=? LIMIT 1",
                          (ref, ref)).fetchone()
        out.append(f"{ref}" + (f" — {eng['text']}" if eng else ""))
        for w in rows:
            bits = [w["surface"] or ""]
            if w["translit"]:
                bits.append(f"({w['translit']})")
            bits.append(f"lemma={w['lemma']}")
            if w["strong"]:
                bits.append(w["strong"])
            if w["gloss"]:
                bits.append(f"'{w['gloss']}'")
            if w["morph"]:
                bits.append(w["morph"])
            out.append("   " + " ".join(bits))
    con.close()
    return "\n".join(out) if out else f"No word-level data for {reference} (words cover Hebrew OT + Greek NT)."


@mcp.tool()
def read_work(work: str, chapter: int = 1, start: int = 1, end: int = 5) -> str:
    """Read a prose work from the corpus by paragraph range. Works: CONFESSIONS
    (Augustine), IMITATION (à Kempis), PILGRIM (Bunyan), PRESENCE (Brother Lawrence),
    JULIAN (Julian of Norwich), ORTHODOXY (Chesterton), 1CLEMENT (Clement of Rome),
    BARNABAS (Epistle of Barnabas). Chapters = books/chapters of the work; use
    search(version=<WORK>) to find passages first, or corpus_info() for the full list."""
    con = _db()
    rows = con.execute(
        "SELECT ref, verse, text FROM passages WHERE doc_id=? AND chapter=? AND verse BETWEEN ? AND ? ORDER BY verse",
        (work.upper(), int(chapter), int(start), int(end))).fetchall()
    doc = con.execute("SELECT title FROM documents WHERE id=?", (work.upper(),)).fetchone()
    con.close()
    if not rows:
        return f"Nothing found for {work} chapter {chapter} paragraphs {start}-{end}."
    head = f"{doc['title'] if doc else work} — chapter {chapter}"
    return head + "\n" + "\n\n".join(f"[{r['ref']}] {r['text']}" for r in rows)


def _psalm_offset(con, chapter):
    row = con.execute("SELECT offset FROM psalm_offsets WHERE chapter=?", (chapter,)).fetchone()
    return row["offset"] if row else 0


def _has_versemap(con):
    return bool(con.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='versemap'").fetchone())


def _heb_refs_for_display_verse(con, book, chapter, verse):
    """English (BSB/WEB) verse ref -> the original-language words-table ref(s) it covers.

    Two mechanisms, layered:
    - Psalms: the psalm_offsets superscription shift (MT numbers the title as v1),
      which is one-to-many at verse 1 — kept on its own path.
    - Everything else: the `versemap` table (empirically derived MT/NA <-> English
      alignment across 30+ books: Joel 2-4, Malachi 3-4, Hosea, Isaiah 64, the
      Nehemiah/Kings/Chronicles seams, 3 John, Acts 19, Rev 12, etc.), falling back
      to identity where no row exists."""
    if book == "Ps":
        k = _psalm_offset(con, chapter)
        if not k:
            return [f"{book}.{chapter}.{verse}"]
        if verse == 1:
            return [f"{book}.{chapter}.{v}" for v in range(1, k + 2)]
        return [f"{book}.{chapter}.{verse + k}"]
    eng_ref = f"{book}.{chapter}.{verse}"
    if _has_versemap(con):
        rows = con.execute(
            "SELECT src_ref FROM versemap WHERE dst_ref=?", (eng_ref,)).fetchall()
        if rows:
            return [r["src_ref"] for r in rows]
        # if this English ref is itself the *source* side of a mapping, its words
        # live under a different English verse — return nothing rather than the
        # wrong verse's words being implied; identity only when unmapped both ways.
        claimed = con.execute(
            "SELECT dst_ref FROM versemap WHERE src_ref=?", (eng_ref,)).fetchone()
        if claimed:
            return [eng_ref]  # words exist at this original-language ref; caller shows them under their true home via display mapping
    return [eng_ref]


def _display_ref_for_heb_ref(con, heb_ref):
    """Inverse: an original-language words-table ref -> the English display ref
    (BSB/WEB verse) it falls under."""
    try:
        book, ch, v = heb_ref.split(".")
        ch, v = int(ch), int(v)
    except ValueError:
        return heb_ref
    if book == "Ps":
        k = _psalm_offset(con, ch)
        if not k:
            return heb_ref
        return f"{book}.{ch}.1" if v <= k + 1 else f"{book}.{ch}.{v - k}"
    if _has_versemap(con):
        row = con.execute(
            "SELECT dst_ref FROM versemap WHERE src_ref=? LIMIT 1", (heb_ref,)).fetchone()
        if row:
            return row["dst_ref"]
    return heb_ref


EMB_MODEL = "BAAI/bge-small-en-v1.5"
_emb_cache = {"matrix": None, "meta": None, "model": None}


def _load_semantic():
    """Lazy-load numpy matrix + fastembed model. Raises with a helpful message if the
    semantic tier isn't installed (see DESIGN.md dependency policy)."""
    import numpy as np
    if _emb_cache["matrix"] is None:
        con = _db()
        rows = con.execute(
            "SELECT kind, doc_id, ref, end_ref, text, vec FROM embeddings WHERE model=?",
            (EMB_MODEL,)).fetchall()
        con.close()
        if not rows:
            raise RuntimeError("No embeddings in db — run scripts/embed.py first.")
        _emb_cache["meta"] = [(r["kind"], r["doc_id"], r["ref"], r["end_ref"], r["text"]) for r in rows]
        _emb_cache["matrix"] = np.vstack(
            [np.frombuffer(r["vec"], dtype=np.float16).astype(np.float32) for r in rows])
    if _emb_cache["model"] is None:
        from fastembed import TextEmbedding
        _emb_cache["model"] = TextEmbedding(model_name=EMB_MODEL)
    return _emb_cache


def _embed_query(text: str):
    import numpy as np
    cache = _load_semantic()
    v = np.asarray(next(iter(cache["model"].embed([text]))), dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-9)


@mcp.tool()
def semantic_search(query: str, top_k: int = 12, kind: str = "", hybrid: bool = True) -> str:
    """Meaning-based search across the whole corpus — scripture AND prose works — using
    embeddings, optionally fused with keyword search (hybrid, recommended). Finds
    passages about a theme even with no shared words, e.g. 'divine self-emptying',
    'the soul's dark night'. kind optional: verse | window | paragraph."""
    try:
        import numpy as np
        cache = _load_semantic()
    except ImportError:
        return "Semantic tier not installed: pip install fastembed numpy (in the server's venv)."
    except RuntimeError as e:
        return str(e)
    qv = _embed_query(query)
    sims = cache["matrix"] @ qv
    meta = cache["meta"]
    order = sims.argsort()[::-1]
    K = 60  # RRF constant
    scores = {}

    def add(key, rank, payload):
        s, p = scores.get(key, (0.0, payload))
        scores[key] = (s + 1.0 / (K + rank), p)

    n_added = 0
    for rank, idx in enumerate(order):
        k_, doc, ref, end_ref, text = meta[idx]
        if kind and k_ != kind:
            continue
        add(ref, rank + 1, (k_, doc, ref, end_ref, text, float(sims[idx])))
        n_added += 1
        if n_added >= 100:
            break
    if hybrid:
        con = _db()
        try:
            frows = con.execute(
                "SELECT p.ref, p.doc_id, p.text FROM passages_fts f JOIN passages p ON p.id=f.rowid "
                "WHERE passages_fts MATCH ? ORDER BY rank LIMIT 50",
                (" OR ".join('"' + w.replace('"', "") + '"' for w in query.split()),)).fetchall()
            for rank, r in enumerate(frows):
                add(r["ref"], rank + 1, ("verse", r["doc_id"], r["ref"], None, r["text"], 0.0))
        except sqlite3.OperationalError:
            pass
        con.close()
    ranked = sorted(scores.items(), key=lambda kv: -kv[1][0])[:max(1, min(int(top_k), 40))]
    out = [f"Semantic{'/hybrid' if hybrid else ''} results for {query!r}:"]
    for ref_key, (score, (k_, doc, ref, end_ref, text, sim)) in ranked:
        span = f"{ref}–{end_ref}" if end_ref else ref
        out.append(f"[{span}] ({doc}) {text[:280]}")
    return "\n".join(out)


@mcp.tool()
def find_similar(reference: str, top_k: int = 10) -> str:
    """Find passages semantically similar to a given verse or prose paragraph ref —
    across scripture, Apocrypha, and the classics. E.g. 'Philippians 2:7' or
    'JULIAN.27.2'. Powers parallel-finding across corpus layers."""
    try:
        import numpy as np
        cache = _load_semantic()
    except ImportError:
        return "Semantic tier not installed: pip install fastembed numpy (in the server's venv)."
    except RuntimeError as e:
        return str(e)
    # resolve ref: try scripture parse, else use raw (prose refs)
    try:
        book, ch, v1, _ = parse_ref(reference)
        ref = f"{book}.{ch}.{v1 or 1}"
    except ValueError:
        ref = reference.strip()
    meta = cache["meta"]
    idx = next((i for i, m in enumerate(meta) if m[2] == ref and m[0] in ("verse", "paragraph")), None)
    if idx is None:
        return f"No embedding found for {ref}."
    qv = cache["matrix"][idx]
    sims = cache["matrix"] @ qv
    order = sims.argsort()[::-1]
    out = [f"Passages similar to [{ref}] — {meta[idx][4][:160]}"]
    seen = {ref}
    for i in order:
        k_, doc, r_, end_ref, text = meta[i]
        if r_ in seen or (end_ref and ref >= r_ and ref <= end_ref):
            continue
        seen.add(r_)
        span = f"{r_}–{end_ref}" if end_ref else r_
        out.append(f"[{span}] ({doc}, {sims[i]:.3f}) {text[:240]}")
        if len(out) > max(1, min(int(top_k), 30)):
            break
    return "\n".join(out)


@mcp.tool()
def get_citations(reference: str, limit: int = 20) -> str:
    """Where a Bible verse is cited by name in the patristic corpus, extracted from
    the translators' own footnotes (tier 1). E.g. reference='Ephesians 5:21'.
    Complements get_cross_references, which links scripture to scripture; this
    links patristic text to scripture. COVERAGE NOTE: footnote extraction has
    known recall gaps — an empty result is normal and does NOT mean the verse is
    uncited; full-text `search` within the patristic works is the thorough probe
    (verbatim quotations are regularly found that the footnote index missed)."""
    book, ch, v1, _ = parse_ref(reference)
    if v1 is None:
        return "Please give a specific verse, e.g. 'Ephesians 5:21'."
    ref = f"{book}.{ch}.{v1}"
    con = _db()
    rows = con.execute(
        "SELECT from_ref, source FROM links WHERE to_ref=? AND type='citation' LIMIT ?",
        (ref, max(1, min(int(limit), 50)))).fetchall()
    if not rows:
        con.close()
        return f"No patristic citations found for {ref} in the current corpus."
    out = [f"Patristic citations of {ref}:"]
    for r in rows:
        p = con.execute("SELECT doc_id, text FROM passages WHERE ref=?", (r["from_ref"],)).fetchone()
        doc = con.execute("SELECT title FROM documents WHERE id=?", (p["doc_id"],)).fetchone() if p else None
        title = doc["title"] if doc else (p["doc_id"] if p else r["from_ref"])
        snippet = (p["text"][:200] + "…") if p and len(p["text"]) > 200 else (p["text"] if p else "")
        out.append(f"[{r['from_ref']}] {title}: {snippet}")
    con.close()
    return "\n".join(out)


@mcp.tool()
def corpus_info() -> str:
    """What's in the corpus: documents, layers, licenses, and counts."""
    con = _db()
    docs = con.execute("SELECT * FROM documents").fetchall()
    out = ["bible-mcp corpus:"]
    for d in docs:
        n = con.execute("SELECT COUNT(*) c FROM passages WHERE doc_id=?", (d["id"],)).fetchone()["c"]
        out.append(f"- {d['id']}: {d['title']} | {d['language']} | {d['license']} (tier {d['license_tier']}) | {n} passages")
        if d["notes"]:
            out.append(f"    {d['notes']}")
    for label, sql in [
        ("cross-reference links", "SELECT COUNT(*) c FROM links"),
        ("entities", "SELECT COUNT(*) c FROM entities"),
        ("entity-verse mentions", "SELECT COUNT(*) c FROM entity_mentions"),
        ("original-language words (Greek)", "SELECT COUNT(*) c FROM words WHERE lang='grc'"),
        ("original-language words (Hebrew/Aramaic)", "SELECT COUNT(*) c FROM words WHERE lang IN ('hbo','arc')"),
    ]:
        out.append(f"- {label}: {con.execute(sql).fetchone()['c']}")
    con.close()
    return "\n".join(out)


def _skill_text(name):
    """Load a pipeline skill from the repo's .claude/skills/ (source of truth).
    The skills are versioned with the corpus; these prompts are the MCP
    distribution layer, so any client that installs bible-mcp gets the
    synthesis discipline bundled with the data."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        ".claude", "skills", name, "SKILL.md")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return f"(skill file not found at {path})"
    # strip YAML frontmatter — the prompt consumer needs the body
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    return text.strip()


@mcp.prompt()
def corpus_survey(theme: str) -> str:
    """Layer 0 of the bible-mcp synthesis pipeline: a raw, skill-free reading of a
    theme through the corpus — distributions as findings, registers mapped,
    intertexts traced, epistemic status tagged. Run this before any composition."""
    return (f"Run a Layer 0 corpus survey for the theme \"{theme}\" using the "
            f"bible-mcp tools, following this discipline:\n\n{_skill_text('corpus-survey')}")


@mcp.prompt()
def corpus_composer(theme: str) -> str:
    """Layer 2 of the bible-mcp synthesis pipeline: compose a research brief from an
    existing Layer 0 survey artifact — the survey is the spine; cross-disciplinary
    material welds around it; every corpus-checkable claim is listed for verification."""
    return (f"Compose the Layer 2 research brief for the theme \"{theme}\" from its "
            f"Layer 0 survey artifact, following this discipline:\n\n{_skill_text('corpus-composer')}")


if __name__ == "__main__":
    # Transport selection:
    #   default            -> stdio (local use: Claude Desktop / Cowork config)
    #   BIBLE_MCP_TRANSPORT=streamable-http -> public remote endpoint
    # Stateless HTTP so instances scale horizontally with no session affinity;
    # the server is read-only over the db, so no auth is required for public use.
    transport = os.environ.get("BIBLE_MCP_TRANSPORT", "stdio")
    if transport == "streamable-http":
        mcp.settings.host = os.environ.get("HOST", "0.0.0.0")
        mcp.settings.port = int(os.environ.get("PORT", "8080"))
        mcp.settings.stateless_http = True
        # FastMCP() defaults to loopback-only DNS-rebinding protection (host="127.0.0.1"
        # at construction time); this is a public no-auth read-only endpoint, so
        # there's no localhost boundary to protect and the loopback-only allowlist would
        # otherwise reject every real request's Host header.
        mcp.settings.transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
