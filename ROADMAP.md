# bible-mcp Roadmap

**Stance:** Non-commercial, public resource. This unlocks the CC BY-NC tier: ETCBC BHSA (richest Hebrew syntax database), ETCBC Dead Sea Scrolls transcriptions, ETCBC Peshitta, Seshat. No quarantine needed — but keep per-source license metadata anyway (good hygiene, and preserves optionality).

## Done (v0.1–v0.2, July 2026)
- [x] Re-pull BSB from berean.bible official (Gen 1:1 restored)
- [x] Canonical ID scheme: OSIS refs for scripture; WORK.chapter.paragraph for prose
- [x] Core ingestion: BSB + WEB (incl. Apocrypha) + OpenBible cross-refs + Theographic
- [x] MACULA Greek + Hebrew word-level data (613,690 words: lemma, Strong's, morph, glosses, domains)
- [x] Gutenberg shelf #1: Confessions, Imitation, Pilgrim's Progress, Presence, Julian, Orthodoxy
- [x] SQLite + FTS5 storage; MCP server with 10 tools (incl. word_study, get_interlinear, read_work)

## Done (v0.3)
- [x] DESIGN.md: embeddings architecture, TEI addressing spec, TVTMS spec, citation-graph methodology
- [x] Embeddings: bge-small-en-v1.5 (fastembed/ONNX), 54k chunks (verse/window/paragraph), float16 in SQLite, numpy exact search
- [x] semantic_search (hybrid RRF) + find_similar tools

## Done (v0.4, July 2026 — "quick hits")
- [x] Psalm superscription versification bug fixed: 62 psalms where Hebrew (MACULA) and English (BSB/WEB) verse numbers diverge, derived empirically from data already in the DB (no external TVTMS import needed for this case). `get_interlinear`/`word_study` now align correctly. Full TVTMS import (other traditions/books) stays deferred — DESIGN.md §3.
- [x] First patristic slice ingested: 1 Clement + Epistle of Barnabas (ANF, ANF vol. 1 compilation, Gutenberg #77576), simple WORK.chapter.paragraph addressing — full TEI/CTS addressing rigor deferred to a lookback pass, DESIGN.md §2.
- [x] Tier-1 citation graph: 267 scripture citations extracted from the translators' own footnotes (free byproduct of ingestion, per DESIGN.md §4 tier 1). New `get_citations` tool. Tiers 2-3 (verbatim shingling, allusion detection) stay deferred until there's more patristic volume and a concrete question driving it.
- [x] Strategic reframe: corpus breadth is not the bottleneck for the "delightful, accessible, grounded" goal — pausing corpus expansion in favor of a synthesis test-drive next.

## Done (v0.5, July 2026 — synthesis test-drive, "potter and clay")
- [x] Full pipeline run: corpus research → topic-prospector seeds → caucus-writer piece ("The Unfinished Verb") → friction report. Artifacts in `outputs/` with prototyped frontmatter (title/date/theme/layer/skill/draws_on).
- [x] **Bug found (live, user-visible): Isaiah 64 MT/English versification offset** — `get_interlinear("Isaiah 64:8")` pairs English 64:8 with Hebrew of MT 64:8 (= Eng 64:9); `word_study` refs for Isa 64 are MT-numbered but rendered with English text. Psalm fix doesn't cover it. Promotes TVTMS import (below).
- [x] **Citation-graph recall gap found**: 1 Clement 39 quotes Job 4:19 at length ("houses of clay") but `get_citations(Job 4:19)` returns nothing — footnote parsing missed it, or the edition leaves it unmarked (→ tier-2 shingling case).
- [x] **Pipeline lesson (the big one): the corpus should speak before the lens does.** A parallel plain-mode session (MCP attached, no skills) out-read the skill-shaped research on intra-corpus insight: it surfaced the 23/44 Isaiah distribution of yatsar, Isa 26:3's "steadfast yetser," the Gen 2:7 vs 2:19 double-yod control, and register mapping (protest/intimacy/conquest) — all present in the same tool results the skill pass had, but pruned by the skill's anti-predictable disposition. Skills are attention-shapers; applied at research time they silently prune the evidence base. → Pipeline revised below.

## Done (v0.6, July 2026 — pipeline formalized and road-tested)
- [x] **corpus-survey + corpus-composer skills built and revised to v1.1** (`.claude/skills/` — project-skill path, auto-discovered by Claude Code/Cowork sessions rooted in the repo), distilled from the potter experiment, then road-tested end-to-end on two fresh themes (living water, wilderness) by agents following the SKILL.md files verbatim. Both runs produced pilot-quality hinges and questions with no potter scaffolding — the discipline generalizes. Four convergent agent critiques applied as v1.1.
- [x] **Verification loop proven**: 6 sampled checkable claims, 6 confirmed, one hedge upgraded to a finding (Jer 17:13 miqweh pun corpus-visible via H4723/H4723a homograph split; Rev 12:6 ↔ Mark 1:3 share hetoimazō).
- [x] **New friction logged** (see `outputs/2026-07-17-pipeline-assessment.md`): versification offsets confirmed at Jer 8:23→9:1 and Hosea 2 (off by TWO — not all offsets are ±1), Exodus 8 class; get_citations recall misses now at three (Barnabas 11.1/Jer 2:13, Barnabas 9/Isa 40:3, 1 Clem 39/Job 4:19) → tier-2 shingling case is empirical; word_study needs zero-padded Strong's, rejects pointed lemmas and transliterations.
- [x] `outputs/` layer at nine artifacts across three themes; frontmatter schema stable.

## Done (v0.7, July 2026 — corpus improvements sprint)
- [x] **Versification fixed corpus-wide.** New `versemap` table: 988 MT/NA ↔ English alignments across 31 books, derived empirically (monotonic sequence alignment + banded DP for splits/merges) from the corpus's own two witnesses and validated by gloss-text overlap (mapped ≈0.75 vs identity ≈0.10 everywhere). All four known fixture bugs resolved (Isa 64, Jer 8:23→9:1, Hos 2 ±2, Exod 8), plus every classical seam (Joel 2–4, Mal 3–4, Num 16–17, 1Kgs 4–5, Dan, Neh, Kings/Chronicles) and the Greek-side cases (3John 14+15, Acts 19:41, Rev 12:18, 2Cor 13:13, Mark's critical-text-omitted verses). `get_interlinear`/`word_study` now map through versemap for all books; Psalms stay on psalm_offsets. Table schema is TVTMS-compatible — STEPBible import (unreachable from the build sandbox; drop the file into data/sources/ anytime) extends it to other traditions.
- [x] **word_study query fixes**: zero-padding optional (H953 works), bare numbers surface all lettered homograph variants side by side (H4723 + H4723a), unpointed/unaccented lemma queries match via diacritic-stripped index.
- [x] **Tool-description migration** done: homograph probing, get_citations sparsity, stemming conflation now documented in the tool docstrings themselves (skills v1.2 slimming can follow).
- [x] **MCP prompts shipped**: `corpus_survey(theme)` and `corpus_composer(theme)` served from `.claude/skills/` — the pipeline travels with the server.
- [x] **Apostolic Fathers complete**: 2 Clement, Polycarp, Martyrdom of Polycarp, Ignatius (shorter recension only — longer excluded as duplicating later expansion), Martyrdom of Ignatius, Diognetus, Pastor of Hermas, Papias — 305 paragraphs, 208 tier-1 citations, all embedded. (Also fixed a latent footnote-parsing bug that silently swallowed body text between footnote clusters in multi-section works.)
- [x] **Outputs layer ingested**: 6 research artifacts (3 themes × survey + brief) as `layer='output'` docs — searchable, semantically indexed, `draws_on` links live. Meta documents (assessments, friction reports) deliberately kept as files only.
- [x] Incremental-ingestion architecture: `scripts/ingest_additions.py` (--emit-json / --apply split, because the db can't round-trip the cloud sandbox's 20MB commit cap); prior db backed up as `db/bible.db.bak-20260718`.
- [!] **Restart the MCP server** (restart Claude Desktop or toggle the server) to load the new server.py — versemap-corrected interlinear, word_study fixes, and prompts activate then; new corpus data is already live.
- Corrections from the sprint: Irenaeus is NOT in pg77576 (that file is the Apostolic Fathers volume only — earlier friction report overclaimed); Irenaeus needs source acquisition (Gutenberg reachable from sandbox; exact ebook id TBD, or CCEL). draws_on link extraction undercounts on natural-style ref lists ("Gen 2:7, 2:19") — normalize in a follow-up. embed.py's count-based resume is approximate after incremental additions.

## Done (v0.8, July 2026 — Irenaeus)
- [x] **Against Heresies I–V + Fragments ingested** (806 sections, 1,598 tier-1 citations, embedded). Source: Wikisource transcription of ANF vol. I (Roberts-Rambaut; Gutenberg has no AH — only a secondary 1841 study). Wikitexts preserved in `data/sources/wikisource/` for provenance; parser `scripts/ingest_irenaeus.py`.
- [x] **DESIGN.md §2 addressing satisfied for AH**: the Wikisource anchors carry chapter:section, so `IREN-AH3.3.4` = Against Heresies, Book 3, chapter 3, section 4 — the standard patristics citation resolves directly (Preface = chapter 0). Verified live: `get_citations(Gen 2:7)` → AH2.34.4, AH4.20.1 (the hands-of-God chapter), AH5.15.2.

## Done (v0.9, July 2026 — public edition)
- [x] **All three publication paths scaffolded** (DECISIONS.md D14-D20): layered non-commercial licensing (LICENSE.md: sources keep own licenses; code PolyForm NC 1.0.0; compilation/derived data CC BY-NC 4.0; NOTICE.md attributions); Streamable-HTTP transport in server.py (env-switched, stateless — handshake + tools + prompts verified live in sandbox); Dockerfile with model pre-download; server.json registry manifest; DEPLOY.md runbook (GitHub + Release-asset db, Fly.io, mcp-publisher); .gitignore/.dockerignore.
- [x] **Justin Martyr ingested**: First Apology, Second Apology, Dialogue with Trypho, Martyrdom of Justin — 423 sections, ~408 tier-1 citations, embedded (Wikisource ANF I, third parser shape: bold-chapter works).
- [ ] **User actions to go live** (DEPLOY.md): `gh repo create` + release the db → `fly launch && fly deploy` → fill server.json placeholders → `mcp-publisher publish`. Anthropic connectors directory submission after the endpoint has run stably for a week or two.

## Next
- [ ] **Tier-2 citation shingling** — now with three confirmed footnote-index misses as validation fixtures (1 Clem 39/Job 4:19; Barnabas 11.1/Jer 2:13; Barnabas 9/Isa 40:3).
- [ ] draws_on normalization: parse "Book C:V, V2, V3" continuation lists so POTTER-* artifacts link fully.
- [ ] Fold the new AF shelf + outputs ingestion into build_db.py for full-rebuild parity (currently incremental-only).
- [ ] **Skill/server division of labor** (principle from the v0.6 road test: skills carry method; the server carries capability and its own documentation; any skill text about a tool's sharp edges is tech debt that migrates down):
  - [ ] Zero-pad/alias the word_study query path; accept unpointed-lemma and transliteration queries (kills three paper-cuts found in road test)
  - [ ] **Tool-description migration**: fold the road test's workaround knowledge into the tool docstrings themselves — word_study: letter-suffixed homograph variants exist (H4723 vs H4723a), probe them when a gloss looks too narrow; get_citations: coverage is two works via footnote extraction with known recall gaps, empty results are normal, full-text search is the real patristic probe; search: stemming conflates senses in prose layers. Then trim the corresponding paragraphs from the skills (v1.2 should be *shorter* than v1.1).
  - [ ] **MCP prompts**: expose `corpus-survey` and `corpus-composer` as FastMCP `@mcp.prompt()` templates on the server, so any bible-mcp user in any MCP client gets the discipline bundled with the corpus (distribution layer for the public-resource stance; repo `.claude/skills/` stays the source of truth, prompts are generated/synced from the same SKILL.md content).
- [x] **Synthesis pipeline — complete and bounded** (settled 2026-07-18). The pipeline is two stages and stops: **Layer 0** (raw corpus survey, no compositional lens — the corpus speaks first) → **Layer 2** (composed research brief with checkable-claims appendix, verified against the corpus). Its outputs are *raw research* and a *research brief* — the tool's terminus. Downstream use (the user's own writing, drawing on the briefs; chatting with layer 0/2 docs as context for clarification) is deliberately outside the tool's scope: no editing stage, no further pipeline layers, and user edits are not pipeline data. **The research outputs themselves remain data**: surveys and briefs are ingested into the corpus (`layer='output'`, `draws_on` links — see the outputs-formalization item below), so they are searchable, semantically indexed, and one hop from their grounding refs like every other layer. The bespoke skills implementing both stages exist at `.claude/skills/` (v1.1, road-tested on three themes).
- [ ] **TVTMS import — promoted from deferred** (DESIGN.md §3): Isaiah 64 bug is live in a flagship tool; also covers Joel 2/3, Malachi 3/4, 3 John. Supersedes further empirical one-off fixes.
- [ ] **Irenaeus slice from ANF vol. 1** (already in `data/sources/`) — highest-value patristic add, demonstrated by the test-drive (hands-of-God clay theology, John 9 ↔ Gen 2:7); check the 1 Clement 39 footnote question during the same pass.
- [ ] **Formalize `outputs/` as a corpus layer**: frontmatter schema prototyped and in use (first four artifacts, 2026-07-17); ingest via passages/links/embeddings with `layer='output'` and `draws_on` links back to grounding refs. Decide whether non-corpus sources (web/training citations) also belong in frontmatter.
- [ ] Rest of the Apostolic Fathers from the same source (Ignatius's letters, Polycarp, Martyrdom of Polycarp, 2 Clement, Shepherd of Hermas, Fragments of Papias) — same pipeline, ready to slice once needed
- [ ] Quality pass on apparatus leakage — confirmed in the wild by the test-drive: JULIAN.49.6/49.7 editorial list fragments pollute find_similar neighborhoods; IMITATION carries raw footnote markers "(2)" and underscore italics into results. Still low priority; batch with next ingestion pass.
- [ ] Tool-shape wishlist from the test-drive (minor): cross-work prose search (`version="prose"` or a `layer=` param — sweeping six works for one theme took six calls); reverse citations (given a patristic passage, which verses does it cite?)
- [ ] Fringe layer: Charles 1913 APOT, M.R. James 1924, Mattison PD gnostic translations (gospels.net)
- [ ] BHSA + ETCBC DSS Text-Fabric modules (NC — fine for us)
- [ ] Better chapter detection for PILGRIM/PRESENCE (currently single-chapter; paragraphs still addressable)
- [ ] JULIAN chapter 1 is still editorial front matter (long introduction before the real text; front-matter-before-first-heading is stripped, but JULIAN's introduction itself contains heading-like roman numerals) — needs a per-work start marker, not a general regex fix
- [ ] More Gutenberg: Josephus, Wesley, Luther (pre-1930 trans.), Eckhart (Field), Dark Night (verify edition)

## Roadmap (flagged for later)
- [ ] **"GitHub edition" of the corpus** — publish a clean, structured, versioned open edition (TEI/JSON with stable citation IDs) of ANF/NPNF and the wider assembled corpus as a public good. No authoritative structured ANF/NPNF edition exists anywhere; this would be a foundational contribution.
- [ ] The Philokalia problem: no PD English exists — assemble from PD constituent-author translations, seek license, or fresh translation
- [ ] Science interface: DRH, OpenNeuro contemplative datasets, PMC OA pipeline
- [ ] Outreach: CCEL (ThML permission), Biblindex/HiSoMA (citation data), DRH team (bulk endpoint)
- [ ] Embedding model upgrade path: re-run scripts/embed.py with a stronger model when semantic misses become noticeable (see DESIGN.md §1). Test-drive data point: hybrid query with "wheel" pulled Ezekiel/1 Kings wheels into top-10 — noticeable but workable; not yet a trigger.

## Reference
- corpus-survey.md — full source/license audit (July 2026)
- DESIGN.md — architecture decisions and specs for the next three build phases
- outputs/ — generated synthesis artifacts (layer='output'), first cohort 2026-07-17 (potter and clay: layer0 raw survey, seeds, composed piece, friction report)
