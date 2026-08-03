# Decision Record

Decisions made in building and publishing bible-mcp, with rationale. Additions go at the top.

## 2026-07-18 — Going public (all three paths)

**D14. Three publication paths, executed together.** (1) Public GitHub repository — the corpus-as-code public good; (2) hosted remote MCP endpoint (Streamable HTTP) so anyone on Claude or any MCP client can add the server by URL with no install; (3) registry listings (official MCP Registry via server.json; Anthropic connectors directory as follow-up). One repo feeds all three.

**D15. Non-commercial, layered licensing.** The project is a non-commercial public resource (stated stance since v0.1; it is also what later unlocks the CC BY-NC scholarly tier — ETCBC BHSA, DSS transcriptions). Licensing is layered because the law of the parts differs from the law of the whole:
- **Underlying sources keep their own licenses**, unchanged and unrestricted by us: BSB (PD), WEB (PD; "World English Bible" is trademarked, text is not), Gutenberg texts (PD, PG boilerplate stripped per their trademark terms), Wikisource ANF transcriptions (PD), MACULA (CC BY 4.0), OpenBible cross-references (CC BY), Theographic (CC BY-SA 4.0). Nothing we do narrows anyone's rights to those sources at their origin. See NOTICE.md for attributions.
- **Our code** (server, scripts, skills): PolyForm Noncommercial 1.0.0.
- **Our derived and generated data** (versemap, citation graph, embeddings, the outputs research layer, the compilation/arrangement itself): CC BY-NC 4.0.
- **Honest caveat recorded**: the Theographic entity subset inside the db remains CC BY-SA (share-alike, commercial use permitted) — a collection license cannot override a part's license, and we don't pretend it does. Anyone wanting commercially usable data goes to the sources; the *assembled instrument* is NC.

**D16. Database distribution: GitHub Release asset, not Git LFS.** db/bible.db (~230MB) exceeds GitHub's 100MB file cap. Release assets are free, versioned with tags, and curl-able from Dockerfiles; LFS has bandwidth quotas that a public data project would burn. The repo also ships full rebuild capability (data/sources + scripts) as the deeper guarantee.

**D17. `outputs/` is included in the public edition.** The research layer is generated, clearly tagged (`layer='output'`), CC BY-NC, and demonstrates what the instrument is for. Meta-documents (assessments, friction reports) also ship — they are the project's lab notebook and part of its value as a public method.

**D18. Hosting: Fly.io, single small always-on machine.** The workload shape — persistent process, ~230MB read-only SQLite, ~500MB-1GB RAM with the ONNX model + embeddings matrix loaded, zero write path — fits a container VM, not serverless (Vercel's Python functions cap bundles far below the db size). Fly gives a Dockerfile deploy, a free-enough tier, and `fly deploy` from the repo. Render/Railway are drop-in equivalents if Fly displeases; the Dockerfile is host-agnostic. Public read-only server, no auth; rate limiting at Fly's proxy if abuse appears.

**D19. Transport: Streamable HTTP, stateless.** Claude custom connectors require Streamable HTTP as of May 2026 (SSE deprecated). `BIBLE_MCP_TRANSPORT=streamable-http` switches the same server.py; stdio remains the default for local use. Stateless mode so instances scale horizontally without session affinity.

**D20. Corpus expansion for launch: Justin Martyr.** First Apology, Second Apology, Dialogue with Trypho, Martyrdom of Justin (423 sections, ~408 tier-1 citations) from the same Wikisource ANF I tree as Irenaeus — chosen because (a) the second-century apologist corpus is the natural companion to Irenaeus for the citation graph, (b) the marginal cost was one new parser function, (c) Dialogue with Trypho is the richest early source for OT-in-Christian-reading, directly serving the pipeline's themes. BHSA/DSS (the NC tier the stance unlocks) stays deferred — Text-Fabric import is real engineering, tracked on the roadmap.

## 2026-07-18 — Earlier (corpus improvements sprint)

**D13. Versification via empirical versemap** rather than TVTMS import (sandbox could not fetch STEPBible; the method — sequence alignment of the corpus's own two witnesses, gloss-validated — proved exact and self-contained; table schema kept TVTMS-compatible).
**D12. db mutations ship as emit/apply JSON migrations** because the 230MB db cannot round-trip the cloud sandbox's 20MB commit cap.
**D11. Ignatius: shorter recension only** (longer is a later expansion; both would duplicate every chapter in search).
**D10. Irenaeus from Wikisource, not Gutenberg** (Gutenberg lacks Against Heresies; Wikisource anchors give Book.chapter.section addressing that satisfies DESIGN.md §2's citation acceptance test directly).

## 2026-07-17 — Pipeline

**D9. The pipeline is bounded**: Layer 0 (raw survey) → Layer 2 (research brief) and stops. User edits are not pipeline data; research outputs are (ingested as `layer='output'`).
**D8. The corpus speaks before the lens**: raw, skill-free reading precedes any compositional discipline — interestingness filters applied at research time silently prune the evidence base (established by A/B comparison on potter-and-clay).
**D7. Two bespoke skills** (corpus-survey, corpus-composer) live in `.claude/skills/` as source of truth; MCP prompts serve them to remote users; tool docstrings absorb workaround knowledge (skills trend shorter).
**D6. Checkable-claims verification loop**: every brief ends with tool-verifiable claims; the pass runs before delivery (6/6 confirmed in first run, one hedge upgraded to a finding).

## Earlier (v0.1–v0.4)

**D5. One SQLite file, FTS5, no vector extension** — exact brute-force numpy over float16 at this scale; revisit past ~1M chunks.
**D4. bge-small-en-v1.5 via fastembed** — deployment shape over leaderboard rank; model recorded per vector so upgrades are a re-run.
**D3. OSIS refs everywhere; prose as WORK.chapter.paragraph.**
**D2. Per-source license metadata on every document row** (tier A/B/C/D) — the reason D15 was easy.
**D1. Non-commercial public resource** — the founding stance.
