"""Build the OT concept graph (DESIGN.md #5): Easton's Bible Dictionary as concept/
keyword nodes, verse anchors, and mechanically-derived candidate edges. This covers
Phases 1-4 of the plan. Phase 5 (a bounded LLM verb-assignment pass over the
candidate edges this script produces) is separate and comes after this script's
output is inspected.

Operates on the existing db/bible.db incrementally — does NOT run a fresh full
corpus rebuild (unlike build_db.py's fresh_db()). Re-running is idempotent: it
deletes and rebuilds only what it owns (the EASTON document/passages, the
`concepts`/`concept_mentions` tables, and `links` rows whose type starts with
'concept_'), never touching passages/entities/lexicon from other ingestors.

Usage: python3 scripts/build_concepts.py
"""
import json
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "sources")
DB = os.environ.get("BIBLE_DB_PATH", os.path.join(ROOT, "db", "bible.db"))
sys.path.insert(0, HERE)
from lib_refs import book_to_osis, parse_ref  # noqa: E402
from build_db import add_document  # noqa: E402

OT_BOOKS = {
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam",
    "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov",
    "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos",
    "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal",
}
assert len(OT_BOOKS) == 39

# An inline markdown link's href fragment, e.g. '[Ex. 6:20](/exod#Exod.6.20)' ->
# 'Exod.6.20'. A range href like '(/gen#Gen.2.16-Gen.2.17)' collapses to the start
# verse — good enough for a verse anchor, not scholarly-precise about range extent.
_MDLINK_RE = re.compile(r"\]\(/[a-z0-9]+#([A-Za-z0-9]+\.\d+\.\d+)(?:-[A-Za-z0-9.]+)?\)")


def _slugify(label: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    return s or "x"


def _expand_maybe_range(ref: str):
    """A links.to_ref value is sometimes a same-book-chapter range (Gen.1.26-Gen.1.27,
    per lib_refs.parse_ref's own convention) — expand it to individual verse refs."""
    try:
        book, ch, v1, v2 = parse_ref(ref)
    except ValueError:
        return [ref]
    if v1 is None:
        return [ref]
    return [f"{book}.{ch}.{v}" for v in range(v1, (v2 or v1) + 1)]


def load_easton():
    """Group easton.json's flat itemNum rows by termID into one entry per headword.
    A group is concept-worthy if ANY of its rows is matchType='unmatched' — a group
    that's entirely person/place/multi is just an entity name under another guise
    (e.g. 'Abdon'), already covered by the `entities` table, and is skipped."""
    path = os.path.join(SRC, "theographic-json", "easton.json")
    raw = json.load(open(path, encoding="utf-8"))
    groups = defaultdict(list)
    for rec in raw:
        groups[rec["fields"]["termID"]].append(rec["fields"])
    entries = []
    for term_id, rows in groups.items():
        rows.sort(key=lambda r: r.get("itemNum", 0))
        if not any(r.get("matchType") == "unmatched" for r in rows):
            continue
        label = rows[0]["termLabel"].strip()
        text = "\n\n".join(t for t in (r.get("dictText", "").strip() for r in rows) if t)
        if not label or not text:
            continue
        entries.append({"term_id": term_id, "label": label, "text": text})
    return entries


def extract_refs(text: str):
    """Pull OSIS verse refs from Easton's inline markdown links. Kept only if the
    book resolves via lib_refs (defensive: hrefs are already OSIS-cased in this
    source, but a handful of oddities are worth tolerating rather than crashing on)."""
    out = []
    for frag in _MDLINK_RE.findall(text):
        book_raw, rest = frag.split(".", 1)
        book = book_to_osis(book_raw)
        if book:
            out.append(f"{book}.{rest}")
    return out


def phase1_ingest_easton(con, entries):
    """Ingest Easton's Dictionary as its own corpus citizen (documents+passages), so
    it's searchable/embeddable like every other layer, and so a later LLM pass can
    pull real definition text as evidence rather than a paraphrase of it."""
    con.execute("DELETE FROM passages WHERE doc_id='EASTON'")
    con.execute("DELETE FROM documents WHERE id='EASTON'")
    add_document(
        con, id="EASTON", title="Easton's Bible Dictionary", layer="reference", language="en",
        translator="Matthew George Easton (1897, 3rd ed.)",
        source_url="https://github.com/robertrouse/theographic-bible-metadata",
        license="Public Domain", license_tier="A",
        notes="1897 3rd edition, via Theographic's structured JSON re-derivation. Entries "
              "addressed EASTON.{seq}.1 (one paragraph per entry, itemNum fragments "
              "concatenated) since the source has no native chapter/verse structure.")
    rows = []
    for i, e in enumerate(entries, start=1):
        ref = f"EASTON.{i}.1"
        e["ref"] = ref
        rows.append(("EASTON", ref, "EASTON", i, 1, i, f"{e['label']}: {e['text']}"))
    con.executemany(
        "INSERT INTO passages(doc_id,ref,book,chapter,verse,seq,text) VALUES(?,?,?,?,?,?,?)", rows)
    print(f"  EASTON: {len(rows)} entries ingested as passages")


def phase2_seed_concepts(con, entries):
    """Concept nodes ('theme' type) from every concept-worthy Easton entry."""
    con.execute("DELETE FROM concepts WHERE source='easton' AND type='theme'")
    seen_ids, rows = set(), []
    for e in entries:
        cid, n = _slugify(e["label"]), 2
        while cid in seen_ids:
            cid, n = f"{_slugify(e['label'])}-{n}", n + 1
        seen_ids.add(cid)
        e["concept_id"] = cid
        rows.append((cid, "theme", e["label"], None, e["text"][:2000], "easton", 1.0,
                     json.dumps({"term_id": e["term_id"], "easton_ref": e["ref"]})))
    con.executemany(
        "INSERT INTO concepts(id,type,label,strong,definition,source,confidence,data) "
        "VALUES(?,?,?,?,?,?,?,?)", rows)
    print(f"  concepts: {len(rows)} theme nodes seeded from Easton")


_GLOSS_STOP = {
    "the", "a", "an", "of", "is", "to", "and", "in", "on", "for", "from", "with",
    "it", "his", "her", "their", "not", "be", "are", "was", "were", "have", "has",
    "had", "you", "he", "she", "they", "i", "we",
}


def _normalize_gloss(g: str) -> str:
    """words.gloss ships as dotted compounds with bracketed function words, e.g.
    'of.[the].covenant' or '[is].a.covenant' — strip brackets/parens and drop
    English function words to recover the bare content gloss ('covenant')."""
    g = re.sub(r"[\[\]()]", "", g)
    tokens = [t for t in re.split(r"[.\s]+", g.lower()) if t and t not in _GLOSS_STOP]
    return " ".join(tokens).strip()


def phase2b_link_keywords(con):
    """Where a concept's label exactly matches a word's normalized gloss (no fuzzy
    matching — a wrong link must never masquerade as a confident one), pair it with
    a type='keyword' node keyed by Strong's number and link concept -> keyword via
    concept_derived_from. Matches against `words.gloss` (contextual per-occurrence
    glosses), not `lexicon.headword` (which is the original-script Hebrew/Greek
    itself, not English, and so cannot ever match an English concept label)."""
    con.execute("DELETE FROM concepts WHERE type='keyword' AND source='easton'")
    con.execute("DELETE FROM links WHERE type='concept_derived_from'")

    # Restrict candidate strongs to content words (Noun/Verb/Adjective/Adverb, by
    # each strong's majority morph category). Function words (article/conjunction/
    # preposition/pronoun-suffix) occasionally carry a compound contextual gloss
    # like 'the.covenant' when MACULA's word-alignment attaches a multi-word English
    # span to a Hebrew grammatical particle — without this filter, stripping 'the'
    # from that gloss would wrongly mint a 'covenant' keyword node keyed to the
    # DEFINITE ARTICLE's Strong's number (H1886a) instead of the real noun's.
    morph_counts = defaultdict(Counter)
    for r in con.execute("SELECT strong, morph FROM words WHERE strong IS NOT NULL AND morph IS NOT NULL"):
        morph_counts[r["strong"]][r["morph"][0]] += 1
    content_strongs = {s for s, c in morph_counts.items() if c.most_common(1)[0][0] in ("N", "V", "A", "D")}

    word_rows = con.execute(
        "SELECT DISTINCT strong, gloss FROM words WHERE gloss IS NOT NULL AND strong IS NOT NULL").fetchall()
    by_headword = defaultdict(set)
    for r in word_rows:
        if r["strong"] not in content_strongs:
            continue
        norm = _normalize_gloss(r["gloss"])
        if norm:
            by_headword[norm].add(r["strong"])
    by_headword = {k: sorted(v) for k, v in by_headword.items()}

    # A keyword node's own label: the original-script lemma (majority vote across
    # its occurrences), not the English theme's label — reusing the theme's label
    # (e.g. "Idol") for every one of its keyword children made "Idol -> Idol" the
    # displayed edge, hiding which Hebrew/Greek word each one actually was.
    # words.lemma has 100% coverage here, unlike lexicon.headword (~69%, and ~0%
    # for Greek beyond Abbott-Smith's 517 entries), so it's the right source.
    lemma_counts = defaultdict(Counter)
    for r in con.execute("SELECT strong, lemma FROM words WHERE strong IS NOT NULL AND lemma IS NOT NULL"):
        lemma_counts[r["strong"]][r["lemma"]] += 1
    strong_to_lemma = {s: c.most_common(1)[0][0] for s, c in lemma_counts.items()}

    concepts = con.execute("SELECT id, label FROM concepts WHERE type='theme'").fetchall()
    kw_rows, edge_rows, seen_kw = [], [], set()
    for c in concepts:
        for strong in by_headword.get(c["label"].strip().lower(), []):
            kw_id = f"kw-{strong.lower()}"
            if kw_id not in seen_kw:
                seen_kw.add(kw_id)
                lemma = strong_to_lemma.get(strong)
                kw_label = f"{lemma} ({strong})" if lemma else strong
                kw_rows.append((kw_id, "keyword", kw_label, strong, None, "easton", 1.0,
                                 json.dumps({"derived_from_concept": c["id"]})))
            edge_rows.append((f"concept:{c['id']}", f"concept:{kw_id}",
                               "concept_derived_from", 1.0, "easton_lexicon_exact"))
    if kw_rows:
        con.executemany(
            "INSERT OR IGNORE INTO concepts(id,type,label,strong,definition,source,confidence,data) "
            "VALUES(?,?,?,?,?,?,?,?)", kw_rows)
    if edge_rows:
        con.executemany(
            "INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)", edge_rows)
    print(f"  keywords: {len(kw_rows)} lexeme nodes, {len(edge_rows)} concept_derived_from edges "
          f"(exact headword match)")


def phase3_concept_mentions(con, entries):
    """Verse anchors, filtered to the 39 OT books. A concept with only NT (or no)
    refs keeps its node but gets no mentions here — deferred, not deleted."""
    con.execute("DELETE FROM concept_mentions")
    rows, kept = [], set()
    for e in entries:
        ot_refs = {r for r in extract_refs(e["text"]) if r.split(".", 1)[0] in OT_BOOKS}
        for r in ot_refs:
            rows.append((e["concept_id"], r, "easton_parsed"))
        if ot_refs:
            kept.add(e["concept_id"])
    con.executemany(
        "INSERT OR IGNORE INTO concept_mentions(concept_id,ref,source) VALUES(?,?,?)", rows)
    print(f"  concept_mentions: {len(rows)} OT verse anchors across {len(kept)} concepts "
          f"({len(entries) - len(kept)} concepts deferred, no OT anchor found)")


def phase4_candidate_edges(con):
    """Mechanical, zero-LLM candidate edges: same-verse co-occurrence, existing
    cross-reference chains, and shared entity mentions. Nothing here is typed
    broader/narrower/contrasts/causes yet — that needs the Phase 5 LLM pass, which
    only ever refines a candidate this phase already produced, never invents a pair."""
    con.execute("DELETE FROM links WHERE type IN ('concept_associated', 'concept_instance_of')")

    mentions = con.execute("SELECT concept_id, ref FROM concept_mentions").fetchall()
    by_ref = defaultdict(set)
    for r in mentions:
        by_ref[r["ref"]].add(r["concept_id"])

    pair_weight = Counter()
    for ref, cids in by_ref.items():
        # Cap fan-out: a verse cited by dozens of Easton entries is too generic to
        # carry a meaningful pairwise signal and would swamp the graph in noise.
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

    assoc_rows = [(f"concept:{a}", f"concept:{b}", "concept_associated", float(w), "coverse")
                  for (a, b), w in pair_weight.items()]
    xref_rows = [(f"concept:{a}", f"concept:{b}", "concept_associated", float(w), "cross_reference_chain")
                 for (a, b), w in xref_weight.items()]

    ent_rows = con.execute(
        "SELECT em.entity_id AS eid, cm.concept_id AS cid, COUNT(*) AS n "
        "FROM entity_mentions em JOIN concept_mentions cm ON cm.ref = em.ref "
        "GROUP BY em.entity_id, cm.concept_id").fetchall()
    inst_rows = [(f"entity:{r['eid']}", f"concept:{r['cid']}", "concept_instance_of",
                  float(r["n"]), "shared_verse") for r in ent_rows]

    con.executemany("INSERT INTO links(from_ref,to_ref,type,weight,source) VALUES(?,?,?,?,?)",
                     assoc_rows + xref_rows + inst_rows)
    print(f"  edges: {len(assoc_rows)} concept_associated (coverse), "
          f"{len(xref_rows)} concept_associated (cross_reference_chain), "
          f"{len(inst_rows)} concept_instance_of (shared_verse)")


def report(con):
    print("\n--- Verification ---")
    for t in ("theme", "keyword"):
        n = con.execute("SELECT COUNT(*) c FROM concepts WHERE type=?", (t,)).fetchone()["c"]
        print(f"  concepts[{t}]: {n}")
    n = con.execute("SELECT COUNT(*) c FROM concept_mentions").fetchone()["c"]
    print(f"  concept_mentions: {n}")
    for t in ("concept_associated", "concept_instance_of", "concept_derived_from"):
        n = con.execute("SELECT COUNT(*) c FROM links WHERE type=?", (t,)).fetchone()["c"]
        print(f"  links[{t}]: {n}")
    # Direction check on a well-known concept, per the plan's inbound/outbound requirement.
    for cid in ("covenant", "sacrifice", "sabbath"):
        row = con.execute("SELECT id FROM concepts WHERE id=?", (cid,)).fetchone()
        if not row:
            continue
        inbound = con.execute(
            "SELECT COUNT(*) c FROM links WHERE to_ref=?", (f"concept:{cid}",)).fetchone()["c"]
        outbound = con.execute(
            "SELECT COUNT(*) c FROM links WHERE from_ref=?", (f"concept:{cid}",)).fetchone()["c"]
        print(f"  concept:{cid} -> inbound={inbound}, outbound={outbound}")


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(open(os.path.join(HERE, "schema.sql")).read())

    print("Loading Easton's Bible Dictionary…")
    entries = load_easton()
    print(f"  {len(entries)} concept-worthy entries (of the source's distinct termID groups)")

    print("Phase 1 — ingest Easton as a corpus document…")
    phase1_ingest_easton(con, entries)
    print("Phase 2 — seed concept nodes…")
    phase2_seed_concepts(con, entries)
    phase2b_link_keywords(con)
    print("Phase 3 — verse anchors (OT only)…")
    phase3_concept_mentions(con, entries)
    print("Phase 4 — mechanical candidate edges…")
    phase4_candidate_edges(con)

    con.commit()
    con.execute("INSERT INTO passages_fts(passages_fts) VALUES('optimize')")
    con.commit()
    report(con)
    con.close()


if __name__ == "__main__":
    main()
