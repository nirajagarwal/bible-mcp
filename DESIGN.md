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
| `fulfills` | one direction (fulfiller→fulfilled) | a person/event actualizes what an earlier prophecy/type anticipated — e.g. Christ `fulfills` Prophecy, Branch `fulfills` Prophecy |
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

`fulfills` was added before the NT-expansion Phase 5 pass (2026-09-26), pre-emptively
rather than retroactively like `part_of`/`symbol_of` — the OT-only pass had already
surfaced the exact gap it fills (Christ/Prophecy, Branch/Christ, "Nativity of
Christ"/Prophecy, all correctly left `associated` for lack of a verb) even though
those concepts had almost no verse anchors yet. Once NT concepts gained real anchors
(Christ alone went from 0 to 19), messianic-fulfillment pairs became common and
high-weight enough (Christ↔Prophecy: weight 20) that waiting to add the verb until
the evidence was undeniable, the way `part_of` was added, would just have reproduced
the same backlog on purpose. Single direction, same reasoning as `part_of`: the verb
name fixes the reading, no mirrored inverse needed.

**Confidence floor (settled 2026-09-26, revised 2026-09-28)**: `concept_associated`
edges below weight 7 stay `associated` permanently, as a matter of policy, not
backlog. Originally the floor was weight<10, left untouched by explicit decision.
On 2026-09-28 that decision was deliberately revisited: the weight 3-9 tier
(24,124 never-judged pairs at the time) was opened for the same evidence-cited
Phase 5 review as weight≥10, accepting a lower per-pair scrutiny bar in exchange
for coverage at this scale (default-to-`associated` unless the cited evidence
states an explicit structural claim, same rule, applied faster). Weight 9 (632
pairs) and weight 8 (944) were reviewed in full, weight 7 (1,316) in full, and a
partial pass into weight 6 (408 of 1,969) — 3,300 pairs total, logged in
`outputs/concept-build-log-2026-09-28.jsonl` via `scripts/phase5_w39_chunk1-5.py`.
Result: **8 sharpened** (2 `narrower`, 3 `causes`, 1 `part_of`, 1 `symbol_of` in
weight=9; 1 `causes` in weight=8), all others correctly kept `associated`. The
sharpen rate collapsed from 1.5% (weight=9) to 0.1% (weight=8) to 0% (weight 7
and the weight=6 sample) — exactly the pattern the original floor predicted:
lower weight means fewer shared citations means thinner evidence means less
material for a sharper verb to hang on. Given the trend, the remaining ~20,800
pairs (weight 6 tail + 5 + 4 + 3, dominated by weight 1-2's 113,315 single-
citation pairs) were **not** reviewed — continuing would very likely add few if
any further upgrades for a very large amount of review effort. The floor is now
weight<7, not weight<10; as before, don't silently start reviewing below it
without another explicit decision recorded here.

**Scope**: the 39 protocanonical OT books for v1 (Deuterocanon/Apocrypha concepts
deferred, not discarded — Easton covers the whole Bible).

**MCP tools (added v0.14)**: three tools, mirroring the existing entity-graph
shape rather than inventing a new one. `get_concept(name, concept_type="")` mirrors
`get_entity` — label/id/Strong's lookup with the same tiered fallback (exact →
substring → prefix-stem), definition, verse anchors, and (new) instantiating
entities via `concept_instance_of`. `concepts_in_passage(reference)` mirrors
`entities_in_passage` exactly (same grouped-by-type shape, entity_mentions swapped
for concept_mentions). `get_concept_relations(name, verb="", limit=20)` is the one
genuinely new shape — the typed concept↔concept edges have no entity-graph analogue
— structured like `get_cross_references`/`get_citations` (a `links`-table query by
type, weight-ranked, limited). It excludes `concept_associated` by default (~139,000
mechanical edges vs. ~430 hand-reviewed typed ones) so a naive call doesn't return a
useless flood; `verb="associated"` opts back in. `concept_derived_from` (theme↔
keyword provenance) and `concept_instance_of` (entity→concept) are deliberately
excluded from `get_concept_relations`'s verb vocabulary — they're structural
metadata, already surfaced inline by `get_concept`, not part of the reviewed
theological-relation graph Phase 5/6 built.

One direction-handling subtlety worth documenting: `broader`/`narrower` are stored
as mirrored pairs (both rows exist), so querying only `from_ref` for a concept's own
label is complete — querying `to_ref` too would double the same relationship from
the other side. `causes`/`part_of`/`symbol_of`/`fulfills` are single-direction, so
both `from_ref` and `to_ref` must be checked and phrased accordingly (e.g. "part of"
vs. "has part"). `contrasts`/`associated` are symmetric single rows, checked via
`from_ref OR to_ref`. `get_concept`'s inline relation-count summary reuses this exact
per-verb direction logic (`_concept_relation_counts`) rather than a blanket `(from_ref=?
OR to_ref=?)` count — the earlier draft of that summary double-counted mirrored
`broader`/`narrower` pairs (advertising a `narrower` edge that `get_concept_relations`
would then fail to reproduce, since the "narrower" row lived on the *other* concept).

## Dependency policy

Core server: stdlib only. Semantic tier: numpy + fastembed (lazy). Never torch in the
serving path. Build-time tools may use anything.
