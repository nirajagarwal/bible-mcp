# bible-mcp Design Decisions

Decisions recorded with rationale so later work inherits the why, not just the what.

---

## 1. Semantic search / embeddings (v0.3 — implemented)

### Model: `BAAI/bge-small-en-v1.5` via fastembed (ONNX)

Chosen for the *deployment shape*, not leaderboard rank. The MCP server runs on the
user's Mac and must embed queries at request time, so the model must load fast and run
on CPU without a 2GB torch dependency. fastembed is ONNX-only (~small install), and
bge-small (384-dim, ~65MB) embeds thousands of texts/sec on Apple Silicon CPU.

Trade-off accepted: bge-small is weaker than large 2025-era embedders on nuance.
Mitigations: (a) hybrid retrieval with BM25 covers exact-term queries; (b) the schema
records the model name per vector, so upgrading = re-run `embed.py` with a better model
(e.g., nomic-embed-text, EmbeddingGemma) and nothing else changes. Upgrade when semantic
misses become noticeable, not before.

### Storage: float16 BLOBs in SQLite + numpy brute-force cosine

No vector extension, no ANN index. Rationale: at our scale (~50k chunks now, <1M even
with full patristics) exact brute-force dot product over normalized float16 vectors is
milliseconds in numpy and *exact* (no recall loss). We already fought multi-Python
extension pain on this machine; sqlite-vec would reintroduce it for zero benefit at
this scale. Revisit only past ~1M chunks.

### Chunking: three granularities

| kind | what | why |
|---|---|---|
| `verse` | single verses (BSB for 66 books; WEB for Apocrypha-only books) | precision targets |
| `window` | 5-verse sliding windows, stride 3, BSB+WEB-Apocrypha | verses are too small to carry themes; windows capture pericope-level meaning |
| `paragraph` | prose works as already chunked | natural units |

Only ONE translation embedded per canonical book — embedding both BSB and WEB would put
near-duplicate vectors in every neighborhood and crowd out cross-layer hits. WEB serves
Apocrypha (BSB lacks it); BSB serves everything else.

### Retrieval: Reciprocal Rank Fusion (k=60) of BM25 + cosine

RRF needs no score calibration between the two systems and is the robust standard.
`semantic_search` returns the fused list; pure-vector and pure-lexical remain available
(`search` is pure FTS5). `find_similar(ref)` reuses the stored vector — no re-embedding.

### Server behavior

fastembed + numpy are lazy-imported on first semantic call; all v0.2 tools work without
them. Vector matrix loads once per process and is cached. First-ever call downloads the
model (~65MB) — README warns about this.

---

## 2. Prose/TEI addressing spec (for the patristic slice — next)

- Every work gets a registry entry: work code, author, canonical title, source edition,
  license, structure profile (e.g. `book.chapter.section`).
- Refs remain dot-paths in the existing `passages` schema: `IREN-AH.3.3.4` = Irenaeus,
  Against Heresies, book 3, chapter 3, section 4. `book` column holds the work code,
  `chapter`/`verse` hold the top two numeric levels; deeper TEI paths go in a new
  nullable `path` column.
- Scholarly citation compatibility is the acceptance test: if a standard patristics
  citation can't be resolved to a ref, the addressing failed.
- Gutenberg prose already ingested stays as-is (WORK.chapter.paragraph); the registry
  will retrofit those six works.

## 3. Versification (TVTMS — next)

- Ingest STEPBible TVTMS into a `versemap` table: (tradition, source_ref, canonical_ref, note).
- Canonical scheme = the English/KJV-style numbering our current texts share.
- Applied at *ingestion* for any future Hebrew-numbered (MT Psalms) or Greek-numbered
  (LXX) source; query-time tradition parameter can come later.
- Known hot spots: Psalm titles (MT +1 offset), Joel 2/3, Malachi 3/4, 3 John 14/15.

## 4. Scripture-in-the-Fathers citation graph (research design — later)

Three-tier detection, each writing `links` rows (type='citation', weight=confidence,
source=method):

1. **Edition markers** — ANF/NPNF footnotes mark most citations; parse them during TEI
   ingestion. High precision, free.
2. **Verbatim matching** — character n-gram shingling of patristic text against the
   translation the edition quotes (and Greek↔Greek once First1KGreek lands). Catches
   unmarked quotations.
3. **Allusion candidates** — embedding similarity + shared rare lemmas, emitted at low
   confidence for human/LLM review. This is where new insight lives; never auto-promote
   to high confidence.

Validation: sample against Biblindex counts for a few well-studied Fathers.

---

## 5. OT concept graph (research design — building now)

Abstract theological concepts (Covenant, Sacrifice, Sabbath, Holiness, ...) and lexical
keywords, distinct from the existing `entities` table (named people/places/events).
Seeded from Easton's Bible Dictionary (`data/sources/theographic-json/easton.json`,
already in the repo, previously unused) rather than hand-curated or LLM-brainstormed:
its ~3,700 `matchType='unmatched'` entries are exactly the abstract-concept vocabulary,
each with real 1890s definition text and inline markdown scripture links that parse
directly into verse anchors.

**Storage**: SQLite, not a new datastore. New `concepts`/`concept_mentions` tables
(mirror `entities`/`entity_mentions`). Edges reuse the existing `links` table —
`from_ref`/`to_ref` accept `concept:{id}` or `entity:{id}` alongside bare OSIS refs;
`idx_links_from`/`idx_links_to` already give inbound/outbound queries for free.
`get_cross_references`/`get_citations` filter `links` by an explicit `type=`, so the
new `concept_*` types are additive and cannot leak into their output.

**Generation discipline — same three-tier confidence model as §4, applied to a graph
instead of a citation list**: mechanical candidate edges first (shared verse mentions,
shared entity mentions, existing cross-reference chains — zero fabrication risk,
`confidence`/`weight` = an overlap count), then a *bounded* LLM pass assigns a verb
from a fixed vocabulary to an already-evidenced pair and must cite the real shared
verse; a justification that doesn't reference the given evidence falls back to
`associated` rather than being trusted. The LLM may also propose new concept nodes
Easton doesn't separate (e.g. splitting "Sacrifice"), written with `source='llm'`
and `confidence<1.0`, never auto-wired into `concept_instance_of` edges until
reviewed. This mirrors §4's rule: never auto-promote a low-confidence guess.

**Verb vocabulary** (as `links.type`, prefixed `concept_`):

| verb | direction stored | meaning |
|---|---|---|
| `broader` / `narrower` | both, mirrored | taxonomic hierarchy |
| `causes` | one direction (cause→effect) | narrative/theological causation |
| `part_of` | one direction (part/material→whole/product) | composition or physical part-whole — e.g. Wine `part_of` Drink-offering, Lamp `part_of` Candlestick |
| `symbol_of` | one direction (symbol→symbolized) | a visible sign standing for something else — e.g. Cloud `symbol_of` Shechinah |
| `contrasts` | one row (either column matches) | symmetric opposition |
| `associated` | one row (either column matches) | fallback: real evidence, no sharper verb earned or warranted |

`part_of`/`symbol_of` were added after the first Phase 5 batch (50 top-weighted
edges) found real, evidenced relationships the original five verbs had no honest
slot for — material composition and part-whole kept getting force-fitted toward
`associated` even when the evidence was clear, which was itself the correct call
at the time (per the fallback rule) but a vocabulary gap, not a judgment failure.
Unlike `broader`/`narrower`, these two store only one direction: the verb name
itself fixes the semantic reading (`part_of` always means "from is part of to"),
so a single row answers both "what is X part of" (`from_ref=X`) and "what are the
parts of Y" (`to_ref=Y`) without needing a mirrored inverse type.

**Scope**: the 39 protocanonical OT books for v1 (Deuterocanon/Apocrypha concepts
deferred, not discarded — Easton covers the whole Bible). No new MCP tools yet; this
is a dataset-only milestone, validated (sampled against source verses, following the
project's own "checkable claims" discipline) before anything queries it live.

## Dependency policy

Core server: stdlib only. Semantic tier: numpy + fastembed (lazy). Never torch in the
serving path. Build-time tools may use anything.
