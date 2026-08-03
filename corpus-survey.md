# Corpus Survey — Christian Scholarship & Research MCP
### Machine-readable sources, licenses verified July 2026

**Project:** bible-mcp — a public resource for Christian scholarship grounded in the full breadth of Christian literature (canon → patristics → apocrypha/pseudepigrapha → gnostic/heterodox → mystics), with an integrative/frontier lens toward neuroscience and psychology of religion, aimed at synthesis and new insight generation.

---

## The single most important finding

**Data scarcity is not the constraint. License engineering is.**

As of 2026 a fully open (public domain / CC BY) stack exists end-to-end for the canonical core, and substantial open material exists for every fringe layer. What does *not* exist anywhere is a system that joins these layers — and nobody has shipped the per-source provenance/license metadata layer that a legally clean public server requires. Both are buildable.

Three developments since ~2023 changed the landscape:

1. **Berean Standard Bible went public domain (April 2023)** — a modern, interlinear-backed English translation, free forever.
2. **SBLGNT relicensed to CC BY 4.0** — a critical Greek NT with no strings.
3. **The Calfa Patrologia Graeca corpus (March 2026)** — OCR of the remaining undigitized Migne PG volumes, ~6M lemmatized Greek tokens, openly released. Near-complete machine-readable Greek Fathers now exist.

---

## The gap this project fills

Verified against GitHub, MCP registries, and the commercial landscape (July 2026):

1. **No cross-corpus synthesis MCP server exists.** Dozens of Bible MCP servers exist; nearly all are verse-lookup wrappers. None wraps MACULA/Text-Fabric syntax trees. None serves patristics. Zero touch cognitive-science-of-religion data. The scripture ↔ Fathers ↔ empirical-science bridge is entirely empty.
2. **No "Sefaria for Christianity."** Sefaria proved the architecture (canonical addressing + link graph + open API) for Judaism; no Christian equivalent exists. STEPBible's TVTMS versification mapping is the unproductized connective tissue.
3. **No open patristics semantic search.** The Greek and Latin Fathers exist as TEI; the closed players (Logos, Magisterium AI, Catena) own this space commercially.
4. **No provenance layer.** No project ships per-source license metadata so downstream users know what they can reuse. Doing this well is itself a differentiator.

Closest prior art: `djayatillake/studybible-mcp` (18 tools, scripture-only), `TJ-Frederick/TheologAI` (commentaries), Sefaria (architectural model), Magisterium AI (closed, Catholic-magisterial). None occupies this project's territory.

---

## License tiers (the organizing principle)

Every source below is tagged into one of four tiers. The build should encode this per-document.

| Tier | Terms | Implication |
|---|---|---|
| **A — Free** | Public domain, CC0, CC BY | Ingest, transform, redistribute, commercial-safe |
| **B — Share-alike** | CC BY-SA | Ingest freely; derived *data* bundles must stay BY-SA |
| **C — Non-commercial** | CC BY-NC(-SA/ND) | Quarantine: fine for a free public server, poisons any commercial path. Keep in a separable module |
| **D — Closed** | Copyright, custom terms | Link, cite, or quote only; never bulk-ingest |

---

## Layer 1 — Canonical scripture

### Tier A core stack (complete, end-to-end)

| Resource | What | Format | License |
|---|---|---|---|
| WLC (tanach.us) / OSHB morphhb | Hebrew Bible + morphology, per-word IDs | OSIS XML, JSON | PD text; CC BY 4.0 morphology |
| SBLGNT | Critical Greek NT (Holmes) | XML | CC BY 4.0 (since 2023) |
| Nestle 1904 (biblicalhumanities) | Tagged Greek NT; MACULA's base | XML, TSV | PD + open components |
| CNTR Statistical Restoration | Computer-generated GNT from earliest MSS | TSV | CC BY 4.0 |
| **MACULA Greek + Hebrew** (Clear-Bible/Biblica) | Syntax trees, morphology, semantic roles, participant referents, Louw-Nida/SDBH domain codes, glosses | TEI, "lowfat" XML, TSV | **CC BY 4.0 — the centerpiece** |
| **STEPBible-Data** | TAHOT, TAGNT (incl. THGNT readings legally), lexicons, TIPNR names graph, **TVTMS versification mapping** | Plain TSV | **CC BY 4.0 — highest-value single ingest** |
| UBS SDBH / SDGNT | Semantic dictionaries of biblical Hebrew & Greek (open Louw-Nida successor) | XML/JSON | CC BY-SA 4.0 |
| WEB (with Apocrypha) | Modern English, complete | USFM/OSIS | Public domain |
| BSB | Modern English, interlinear-backed, Strong's-mapped | Text, Excel, DB | Public domain (2023) |
| KJV, ASV, Douay-Rheims, Brenton LXX | Classic English | USFM etc. | Public domain |
| unfoldingWord ULT/UST + notes | Aligned literal & simplified translations | USFM (Door43) | CC BY-SA 4.0 |
| Clementine Vulgate | Latin | Text/XML | Public domain |
| LXX Swete (First1KGreek / eliranwong) | Greek OT | XML/TSV | CC BY-SA 4.0 |
| OpenBible.info cross-references | ~340k ranked cross-refs | TSV | CC BY 4.0 |
| Treasury of Scripture Knowledge | Classic cross-refs | Text/DB | Public domain |
| Strong's, BDB, Abbott-Smith | Lexicons | XML/TEI | Public domain |
| Theographic Bible Metadata | Knowledge graph: ~3,000 people/places/periods/passages | JSON/CSV/Neo4j | CC BY-SA 4.0 |
| Clear-Bible Alignments + genesis-ai-datasets | Word alignments; AI/RAG-targeted data | JSON/TSV | CC BY-SA 4.0 |

### Restricted/avoid (Tier C/D)

ETCBC BHSA and Peshitta/SyrNT (CC BY-NC — richest Hebrew syntax DB, keep as optional NC module; MACULA Hebrew covers the permissive tier), OpenGNT (BY-NC-ND), PROIEL (BY-NC-SA), Rahlfs/CATSS LXX (DBG restrictions), THGNT (proprietary — use STEPBible TAGNT for its readings), ESV/NIV APIs (tight caps, non-commercial, doctrinal conditions), NET/LEB (custom terms). API.Bible free tier is prototyping-only.

**Watch:** STEPBible **TAGOT** (open tagged LXX, "coming") would fill the biggest remaining canonical gap.

---

## Layer 2 — Patristics & historical theology

### Recommended clean stack

| Need | Source | License |
|---|---|---|
| Fathers in English | ANF/NPNF (Schaff, 1867–1900) — text is PD; rebuild from PD sources or get CCEL's ThML permission (one email) | PD (translations) |
| Greek Fathers | **First1KGreek** (TEI/EpiDoc) + **Calfa PG corpus** (2026, ~6M lemmatized tokens, noisy OCR at 1.05% CER) | CC BY-SA / open |
| Latin Fathers & medievals | **Corpus Corporum** (entire Patrologia Latina, ~215M words, TEI) + OGL csel-dev | CC-SA posture |
| Coptic | Coptic SCRIPTORIUM (incl. Apophthegmata Patrum) | CC BY |
| Syriac | Digital Syriac Corpus (500+ TEI texts) + Syriaca.org linked data | CC BY 4.0 |
| Creeds/confessions | Creeds.json (PD subset — filter per-file), Book of Concord via 1921 Triglotta, Westminster standards | PD/Unlicense |
| First seven councils | NPNF Series II vol. 14 | PD |
| Aquinas | PD English Dominican Fathers Summa (1911–25) + PD Latin printings | PD |
| Calvin | Beveridge Institutes + Calvin Translation Society commentaries (CCEL) | PD |
| Reformation-era English | **EEBO-TCP** — ~60k early English books in TEI, fully public since 2020 | CC0/PD |
| Reference | Schaff-Herzog + 1913 Catholic Encyclopedia (via Wikisource, not New Advent) | PD |

### Blocked / grey (Tier D)

Tanner's councils translation (© Georgetown), Luther's Works AE (© Concordia/Fortress — use pre-1930 translations), WJE Online apparatus (Yale — Edwards' own words PD via 19th-c. editions), Corpus Thomisticum & aquinas.cc & augustinus.it (all-rights-reserved sites), Sources Chrétiennes Online, ODCC, English Denzinger (Latin PD). **CCEL nuance:** underlying texts PD, but CCEL claims copyright on its XML files and restricts large-scale/commercial republication — use PD text content or ask permission.

**Biblindex** (650k+ patristic biblical citations) has no API, no bulk export — high-value outreach target for the Lyon team; the scripture→Fathers citation graph it holds is exactly this project's connective tissue.

**Notable gap that is itself an opportunity:** no authoritative structured GitHub edition of ANF/NPNF exists. Producing one (clean TEI/JSON with CTS-style citations) would be a foundational public contribution.

---

## Layer 3 — Fringes

### Apocrypha & pseudepigrapha

Deuterocanon: fully clean via WEB (ecumenical edition), Brenton, KJV Apocrypha, Douay — all PD in USFM at ebible.org.

OT Pseudepigrapha: **R.H. Charles's 1913 APOT is the PD backbone** (Jubilees, 1 Enoch, Testaments, 2 Baruch, 4 Ezra, Ascension of Isaiah, and the Damascus Document as "Fragments of a Zadokite Work"). Charlesworth's OTP is locked until ~2078 — copies on archive.org are unauthorized; do not ingest. Odes of Solomon has PD alternatives (Bernard 1912, Harris 1911). The Online Critical Pseudepigrapha (original-language critical editions) is read-only — no open license, no XML export; PD print editions are the redistribution path.

### Dead Sea Scrolls — the hard problem

Found 1947 → **no PD English translation of the sectarian corpus exists** (Vermes, García Martínez, Wise-Abegg-Cook all copyrighted). Clean path: (a) ETCBC/dss Text-Fabric transcriptions + morphology (Abegg's data; **CC BY-NC** — quarantine tier); (b) biblical scrolls aligned to PD English; (c) Damascus Document via Charles 1913; (d) fresh translations generated/licensed later. Leon Levy digital library: © IAA, link only.

### Gnostic & heterodox

- **Gospel of Thomas and friends: Mark Mattison's translations at gospels.net are explicitly public domain** — Thomas, Mary, Philip, Truth, Judas. This is a quietly excellent find; check each page's statement.
- G.R.S. Mead (Pistis Sophia, Fragments of a Faith Forgotten) and Grenfell-Hunt Oxyrhynchus fragments: PD.
- **M.R. James, Apocryphal New Testament (1924): PD** — the definitive NT-apocrypha collection (Protevangelium, Acts of Paul/Peter/Thomas, Gospel of Peter, apocalypses), full text on Wikisource.
- Coptic NH transcriptions via the Marcion project (thin copyright on ancient-text transcriptions; provenance diligence advised). Robinson's NHL English is © Brill — gnosis.org hosts it by permission and it cannot be re-served.
- Heresiology: ANF Irenaeus and Hippolytus PD; Epiphanius's Panarion English (Williams) is © Brill — locked, only the Greek is PD.

### Mystics & contemplatives

Largely clean via early translations, all on CCEL/Wikisource/Archive:

| Author/text | Clean PD edition |
|---|---|
| Desert Fathers | Budge, *Paradise of the Holy Fathers* (1907); Coptic AP corpus CC BY |
| Pseudo-Dionysius | Parker (1897), Rolt (1920) |
| Cloud of Unknowing | Middle English PD; Underhill 1912 modernization PD |
| Julian of Norwich | Warrack (1901) |
| Meister Eckhart | Field (c. 1909), Evans vol. 1 (1924) |
| Teresa of Ávila / John of the Cross | Lewis (1870s), Stanbrook *Interior Castle* (1921) — zero-risk; Peers likely PD-US but verify renewal per title |
| Thomas à Kempis | Benham (1874) |
| Brother Lawrence | 1895 translation |
| Isaac of Nineveh | **Wensinck, Mystic Treatises (1923) — PD**, full text online |
| Kebra Nagast | Budge (1922) PD |

**The one real hole: the Philokalia.** No PD English exists — Palmer-Sherrard-Ware is copyrighted and the 1950s Kadloubovsky-Palmer partials were URAA-restored in the US. Options: PD Greek (Venice 1782) + PD translations of constituent authors where they exist, licensing outreach, or fresh translation. Worth treating as a named project.

**Cross-cutting warning:** archive.org hosting is not evidence of public domain — Charlesworth, Hermeneia 1 Enoch, and Robinson NHL scans there are all unauthorized.

---

## Layer 4 — Science interface & infrastructure

### Neuroscience / psychology of religion

- **Literature pipeline (legally bundle-able):** PMC Open Access subset (commercial-use tier; contemplative neuroscience is well covered because NIH-funded) + Frontiers + PLOS (gold OA, CC BY) + PsyArXiv (OSF API; per-preprint license). The prestige psychology-of-religion journals (APA, T&F, SAGE) are metadata/abstract-only. **Templeton World Charity Foundation mandates CC BY** for funded work since 2021 — much religion-science research is therefore legally open.
- **Datasets:** Database of Religious History (**CC BY 4.0**, GraphQL backend — the best structured CSR dataset; no AI tool wraps it); Pulotu (CC BY, CLDF on GitHub); OpenNeuro meditation EEG/fMRI datasets — all **CC0** (verified: ds001787 expert meditators, ds003969 breath-focus, ds003816 loving-kindness). Seshat is BY-NC (quarantine); WVS and Pew are query-only, never bundle.
- **Instruments:** Fetzer/NIA BMMRS booklet free from fetzer.org (best open compendium); DUREL free for research; Hood M-Scale treat as copyrighted, cite only.

### Standards & tooling

- **Formats:** TEI P5 (all open patristic corpora), USFM/USX with **USJ (JSON) as the natural MCP payload**, OSIS (frozen; read-only input), CTS URNs (the citation model to emulate — extend Scaife-style canonical addressing to the whole corpus), IIIF (deep-link zoomable manuscript images without hosting them).
- **Text-Fabric** (MIT): the richest query layer for annotated corpora; note the datasets themselves carry their own licenses (BHSA NC, N1904 from MACULA).
- **Manuscripts:** INTF **NT.VMR has a documented public API with CC BY 4.0 transcriptions** — the best open scholarly NT manuscript layer. DigiVatLib is full IIIF (non-commercial reuse). CSNTM is permission-based. British Library still recovering from the 2023 cyberattack — unreliable dependency. e-codices and Gallica are strong IIIF supplements.
- **Sefaria** is the architectural model to study: canonical addressing + bidirectional link graph + open API + per-text license metadata. Its API is also the right interface to Hebrew Bible + Jewish commentary (Rashi, Talmud) alongside the Christian layers.

---

## Build implications for the MCP server

1. **Encode the license tier per document from day one.** Provenance metadata (source, edition, translator, license, URL) on every text unit. This is both legal hygiene and a public differentiator.
2. **Canonical addressing is the spine.** A CTS-style URN scheme spanning scripture (with TVTMS versification mapping), Fathers (Migne column refs), and fringe texts. Everything else — cross-refs, citation graphs, semantic search — hangs off stable addresses.
3. **Start with the Tier-A canonical stack + one patristic slice** (e.g., ANF/NPNF + First1KGreek for the Apostolic Fathers) rather than boiling the ocean. MACULA + STEPBible + BSB/WEB + OpenBible cross-refs + Theographic gives immediate deep capability.
4. **The insight-generation layer is where nothing exists:** scripture→Fathers reception tracing (a Biblindex-like open citation graph), semantic search across layers, contemplative-practice texts linked to the empirical literature (Philokalia-adjacent authors ↔ OpenNeuro/PMC contemplative neuroscience), motif tracking across canonical/apocryphal/gnostic parallels (e.g., Thomas ↔ Synoptics).
5. **Quarantine NC sources** (BHSA, ETCBC DSS, Seshat) in an optional module so a future commercial or grant-funded path stays clean.
6. **Three named sub-projects worth doing as public goods:** a structured open ANF/NPNF edition; an open scripture-in-the-Fathers citation graph; the Philokalia problem (license, assemble from PD constituents, or translate).
7. **Outreach list:** CCEL (ThML permission), Biblindex/HiSoMA (citation data), DRH team (bulk endpoint), possibly Faber (Philokalia).

---

## Source verification

All license claims above were verified against live license pages, repo LICENSE files, or publisher statements in July 2026 by four parallel research passes. Key flagged uncertainties: Peers translations need per-title US renewal checks (Stanford Copyright Renewal DB); Beta maṣāḥǝft exact CC variant per-repo; DRH bulk-download endpoint; N1904 Text-Fabric license terms; USFM 3.2 finality. Full source URL lists are retained in the research notes for each layer.

### Primary repositories (the short list to clone first)

- github.com/Clear-Bible/macula-greek, macula-hebrew, Alignments, genesis-ai-datasets
- github.com/STEPBible/STEPBible-Data
- github.com/openscriptures/morphhb, HebrewLexicon
- github.com/LogosBible/SBLGNT · github.com/biblicalhumanities/Nestle1904
- github.com/ubsicap/ubs-open-license (SDBH/SDGNT)
- ebible.org (WEB, Brenton, KJV, DRA in USFM) · berean.bible
- github.com/OpenGreekAndLatin/First1KGreek · github.com/calfa-co/Patrologia-Graeca
- mlat.uzh.ch (Corpus Corporum) · github.com/CopticScriptorium/corpora · github.com/srophe/syriac-corpus
- github.com/NonlinearFruit/Creeds.json · github.com/textcreationpartnership (EEBO-TCP)
- github.com/robertrouse/theographic-bible-metadata · openbible.info cross-refs
- gospels.net (Mattison PD translations) · Wikisource (M.R. James 1924, Charles Enoch)
- religiondatabase.org (DRH) · openneuro.org (ds001787, ds003969, ds003816)
- ntvmr.uni-muenster.de (API) · github.com/Sefaria/Sefaria-Project (architecture study)
