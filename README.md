# bible-mcp

An MCP server for Christian scholarship and research. Non-commercial, aiming to become a public resource. See `corpus-survey.md` for the full source/license landscape and `ROADMAP.md` for direction.

## What's in it (v0.9)

| Data | Source | License |
|---|---|---|
| Berean Standard Bible (66 books) | berean.bible | Public Domain |
| World English Bible, Ecumenical (83 books incl. Apocrypha) | ebible.org | Public Domain |
| 613,690 original-language words: Greek NT + Hebrew/Aramaic OT with lemmas, Strong's, morphology, glosses, semantic domains | MACULA (Clear-Bible/Biblica) | CC BY 4.0 |
| ~345,000 ranked cross-references | openbible.info | CC BY |
| ~4,800 people/places/events/groups + 53,000 verse links | Theographic Bible Metadata | CC BY-SA 4.0 |
| Six PD classics: Augustine's Confessions, Imitation of Christ, Pilgrim's Progress, Practice of the Presence of God, Julian's Revelations, Chesterton's Orthodoxy | Project Gutenberg | Public Domain |
| The Apostolic Fathers, ten works: 1 & 2 Clement, Epistle of Barnabas, Polycarp to the Philippians, Martyrdom of Polycarp, Epistles of Ignatius (shorter recension), Martyrdom of Ignatius, Epistle to Diognetus, Pastor of Hermas, Fragments of Papias | ANF (Roberts-Donaldson-Crombie), Project Gutenberg #77576 | Public Domain |
| **Irenaeus**: Against Heresies, Books I–V + Fragments — 806 sections addressed as `IREN-AH<book>.<chapter>.<section>` so standard citations (AH 3.3.4) resolve directly; 1,598 tier-1 scripture citations | ANF vol. I (Roberts-Rambaut), Wikisource transcription | Public Domain |
| **Justin Martyr**: First Apology, Second Apology, Dialogue with Trypho, Martyrdom of Justin — 423 sections, ~408 tier-1 citations | ANF vol. I, Wikisource transcription | Public Domain |
| Tier-1 citation graph: scripture citations extracted from the translators' own footnotes across the patristic shelf (see DESIGN.md §4) | — | — |
| **Versemap**: 988 empirically derived MT/NA ↔ English verse alignments across 31 books (Joel 2–4, Malachi 3–4, Hosea, Isaiah 64, Kings/Chronicles/Nehemiah seams, 3 John, Acts 19, Rev 12…), gloss-validated; plus the Psalms superscription offsets | derived from corpus | — |
| **Research outputs layer** (`layer='output'`): Layer 0 corpus surveys + Layer 2 research briefs for potter-and-clay, living water, wilderness — searchable, embedded, with `draws_on` links back to their grounding refs | generated in-project | — |
| ~55,800 embeddings (verse/window/paragraph) for semantic + hybrid search across every layer | bge-small-en-v1.5, generated locally | — |

All in one SQLite file (`db/bible.db`, ~230MB) with FTS5 full-text search. Prose works are addressed as `WORK.chapter.paragraph`. See DESIGN.md for the architecture rationale.

## Tools

- `get_passage(reference, version="BSB")` — Bible text for a reference, e.g. `John 3:16`, `John 3:16-18`, `Genesis 1`. Versions: BSB, WEB (Apocrypha requires `version="WEB"`).
- `search(query, version="BSB", book="", limit=20)` — Full-text search, stemmed and ranked (BM25). Supports quoted phrases and AND/OR/NOT, e.g. `faith AND works NOT law`. `version` also takes any prose work id. Note: stemming conflates related surface forms (e.g. "desert" also matches "deserted") — quote exact phrases or add AND-terms to disambiguate.
- `semantic_search(query, top_k=12, kind="", hybrid=True)` — Meaning-based search across the whole corpus (scripture + prose), hybrid-fused with keyword search (RRF) by default. Finds passages on a theme even with no shared words, e.g. "divine self-emptying". `kind` optional: verse | window | paragraph.
- `find_similar(reference, top_k=10)` — Nearest passages by embedding to a given verse or prose paragraph, across scripture, Apocrypha, and the classics. Powers parallel-finding across corpus layers.
- `word_study(query, language="", limit=15)` — Original-language word study by Strong's number (zero-padding optional), lemma (pointed or unpointed), or English gloss. Returns occurrence counts, gloss range, book distribution, and sample verses. Lettered homograph variants (e.g. H4723 vs H4723a — same written form, different word) are surfaced together. `language` optional: grc | hbo | arc.
- `get_interlinear(reference)` — Word-by-word original language for a verse or short range: surface form, lemma, Strong's, gloss, morphology. Versemap-corrected across all books, not just Psalms.
- `get_cross_references(reference, limit=20)` — Cross-references for a verse (OpenBible.info, ranked by community votes), with the target text included.
- `get_citations(reference, limit=20)` — Where a verse is cited by name in the patristic corpus, extracted from the translators' own footnotes (tier 1). Complements `get_cross_references` (scripture→scripture); this is patristic text→scripture. Coverage is sparse by design — an empty result doesn't mean uncited; full-text `search` within the patristic works is the thorough probe.
- `get_entity(name, entity_type="")` — Look up a biblical person, place, event, or people group by name (Theographic knowledge graph); returns details and where they appear. `entity_type` optional: person | place | event | people_group.
- `entities_in_passage(reference)` — People, places, and events linked to a verse or chapter, e.g. `Genesis 14`.
- `read_work(work, chapter=1, start=1, end=5)` — Read a prose work by paragraph range (CONFESSIONS, IMITATION, PILGRIM, PRESENCE, JULIAN, ORTHODOXY, 1CLEMENT, BARNABAS, and others — see `corpus_info()` for the full list). Use `search(version=<WORK>)` to find passages first.
- `compare_versions(reference)` — A verse or short range in BSB and WEB, side by side.
- `corpus_info()` — What's in the corpus: documents, layers, licenses, and counts.

## Prompts

The server also exposes the synthesis pipeline as MCP prompts, generated from `.claude/skills/` (the source of truth): `corpus_survey(theme)` — Layer 0 raw reading discipline; `corpus_composer(theme)` — Layer 2 research-brief composition. Any MCP client that installs bible-mcp gets the discipline bundled with the data.

## Setup

```bash
pip install -r requirements.txt   # core: just `mcp`
pip install fastembed numpy       # optional semantic tier (semantic_search, find_similar)
python3 scripts/build_db.py       # rebuild db from data/sources (optional; db ships built)
python3 scripts/embed.py          # regenerate embeddings (optional; ships built; resumable)
```

The first semantic query downloads the embedding model (~65MB, one time). Without
fastembed/numpy installed, all non-semantic tools work normally. See DESIGN.md for
architecture decisions (model choice, chunking, hybrid retrieval).

Claude Desktop / Cowork — add to MCP config:

```json
{
  "mcpServers": {
    "bible-mcp": {
      "command": "python3",
      "args": ["/path/to/bible-mcp/server.py"]
    }
  }
}
```

## Layout

```
data/sources/   raw acquired sources (immutable; re-derive, never edit)
data/versemap.tsv        derived MT/NA <-> English verse alignments
data/additions-*.json    prepared incremental ingestions (applied via scripts/ingest_additions.py)
scripts/        schema.sql, lib_refs.py, build_db.py, build_versemap.py, align_splits.py, ingest_additions.py
db/bible.db     the built corpus (SQLite + FTS5)
outputs/        synthesis-pipeline artifacts (Layer 0 surveys, Layer 2 briefs, reports)
.claude/skills/ corpus-survey + corpus-composer (pipeline skills; source for MCP prompts)
server.py       MCP server (FastMCP, read-only on the db)
```

## Public edition

This is a **non-commercial public resource**. Licensing is layered — sources keep
their own licenses (all PD / CC BY / CC BY-SA); the code is PolyForm Noncommercial
1.0.0; the compilation and derived data (versemap, citation graph, embeddings,
outputs layer) are CC BY-NC 4.0. Full details: `LICENSE.md`, attributions in
`NOTICE.md`.

Three ways to use it:
1. **Remote (no install)** — add the hosted endpoint as a custom connector in any
   MCP client (Claude: Settings → Connectors → Add custom connector):
   `https://bible-mcp-server.fly.dev/mcp`
2. **Local (stdio)** — clone, download `db/bible.db` from the latest GitHub
   Release (or rebuild from `data/sources/`), add the config above.
3. **Self-host** — `Dockerfile` ships the Streamable-HTTP server; see `DEPLOY.md`.

## Design notes

- Canonical addressing: OSIS-style refs (`Gen.1.1`) everywhere; every table keys on them.
- Provenance: every document row carries source, license, and license tier (A=free, B=share-alike, C=non-commercial, D=closed — we are non-commercial, so C is usable).
- The 16 verses "missing" from BSB (Matt 17:21, John 5:4, Acts 8:37…) are the standard critical-text omissions, not bugs.
- Versification: `versemap` (all books) + `psalm_offsets` (superscriptions) align MACULA's MT/NA numbering to English. Both derived empirically from the corpus's own two witnesses and validated by gloss-text overlap; the table schema is TVTMS-compatible so the STEPBible data can extend it to other traditions (LXX, Vulgate) later.
- Ignatius ships in the shorter (Middle) recension only; the ANF longer recension is a later expansion and would duplicate every chapter in search.
- The research outputs layer is generated, clearly tagged (`layer='output'`), and can never be confused with primary sources; `draws_on` links tie each artifact to its grounding refs.
- Next per ROADMAP.md: Irenaeus (source acquisition), tier-2 citation shingling (three confirmed footnote-index misses as fixtures), TVTMS proper.
