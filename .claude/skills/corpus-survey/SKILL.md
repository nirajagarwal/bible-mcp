---
name: corpus-survey
description: Layer 0 of the bible-mcp synthesis pipeline — a raw, skill-free reading discipline that lets the corpus speak before any compositional lens arrives. Use this whenever a new theme, word, motif, or passage enters the pipeline ("survey living water", "run layer 0 on wilderness", "raw survey of the vine", "let's start a new theme"), whenever the user asks what the corpus says about something, and ALWAYS before invoking corpus-composer or any composition skill on a fresh theme. If a theme has no survey artifact in outputs/, this skill comes first — composing without one silently prunes the evidence base.
---

# Corpus Survey (Layer 0)

You are producing the *seeds* for everything downstream: a survey of what the bible-mcp corpus actually contains on a theme, read in the corpus's own register. This is not a composition, not a hunt for the surprising, and not a summary of what you already know. The founding lesson of this pipeline (potter-and-clay test-drive, July 2026): a plain reading out-performed a skill-shaped one on intra-corpus insight, because interestingness filters applied at research time silently discard evidence. Here, the predictable done patiently *is* the job. Distribution tables, gloss ranges, and register maps are findings, not throat-clearing.

## The discipline — seven moves

Work through all seven. Order is flexible; coverage is not.

1. **Read tool metadata as findings.** Occurrence counts, book distributions, and gloss ranges in `word_study` output are where surprises live. "23 of 44 occurrences in Isaiah" is a discovery about who owns a word. A gloss range that puts "a.pot" next to "inclination" is a discovery about a root's double life. Quote these numbers in the survey; don't flatten them into "occurs frequently."

2. **Follow every root both directions — with a stopping rule.** For each key term, study the verb AND its noun derivatives AND close Strong's neighbors (H3335 → H3336 was the single richest move of the pilot). Do the same on the Greek side, and note where the LXX/NT vocabulary picks up the Hebrew (plassō for yatsar). Neighbor-chains can recurse forever; end a chain after two consecutive lookups that add nothing the survey will use. Practical notes: Strong's queries need zero-padding (H0953, not H953), homographs may hide under letter suffixes (H4723 "hope" vs H4723a "gathering of waters" — same written form; when a gloss looks too narrow for a word you suspect is richer, probe the lettered variants), and pointed-Hebrew lemma queries can fail where the Strong's number succeeds.

3. **Map rhetorical registers, not just occurrences.** The same image usually does different jobs in different mouths: polemic, petition, elegy, conquest, consolation. Name the registers and cite the verse where each lives (Isaiah's potter: protest 29:16/45:9, intimacy 64:8, conquest 41:25). This map is usually the survey's most valuable single artifact.

4. **Run controls.** When you notice an anomaly (a strange spelling, an odd gloss, a versification quirk), find the nearest comparable text and check it (Gen 2:7's double yod means little until Gen 2:19's single yod is beside it). One control per anomaly, minimum.

5. **Tag epistemic status inline.** Distinguish, in the text as you write: what the corpus data shows · what standard scholarship holds · what is midrash/tradition · what is your inference. The pilot's model: "The Talmud reads the doubled letter as the two yetsarim... that's midrash, not philology — but the consonantal difference itself is real." Never let a traditional reading pass as a textual fact.

6. **Sweep every layer, and report gaps as findings.** Canonical (BSB/WEB), Apocrypha (WEB), prose classics, patristic — search each (`search` with `version=<WORK>` per prose work; `semantic_search` crosses layers). "The patristic layer has nothing on this theme" is a result that drives corpus decisions; say it explicitly. Expect `get_citations` to be sparse — it currently covers two patristic works via footnote extraction with known recall gaps, so an empty result is normal and full-text `search` within the patristic works is the real probe; when full-text finds a quotation the citation index missed, log it in Gaps (three such misses found in the first three themes). Watch semantic_search for lexical hijack in hybrid mode (a rare literal word like "wheel" dominating); re-query without the noisy term. Watch stemmed search conflating unrelated senses in prose layers (desert/deserted/deserts-as-merits).

7. **End where the material points.** Close with (a) the synthesis question the corpus itself poses — the pilot's was "whether the clay is still wet" — stated in one sentence; (b) a **Checkable claims** list: specific assertions downstream layers or your own training knowledge suggested that can be verified with a tool call (word occurrence counts, single-word links between passages, versification alignments); (c) a **Gaps noticed** list: missing sources, thin layers, tool friction, suspected bugs.

## Tool coverage checklist

Before closing, confirm you have used: `word_study` (each key term, both languages, verb+noun), `search` (keyword, per relevant layer), `semantic_search` (2-3 phrasings), `get_interlinear` (each anchor verse), `get_cross_references` (one hub per register in your register map — the map defines what a hub is), `get_citations` (same hubs; sparse results expected), `get_passage` for Apocrypha texts, `compare_versions` on any verse where translation traditions plausibly diverge (MT/LXX forks, versification seams), `find_similar` on the verse your register map shows as most connected. For entity-rich themes (places, journeys, people), add `get_entity`/`entities_in_passage` on the two or three most-cited locations and stop there — entities support the survey, they aren't its subject. Skipping a tool is fine if you say why.

## Output artifact

Write a single markdown file named `YYYY-MM-DD-<theme>-layer0-raw-survey.md`. Default location is the project's `outputs/` folder; if the caller directs a different path, follow the caller — the naming and frontmatter conventions still apply. Frontmatter (`tools:` lists tools that produced findings; note separately any attempted tools that failed):

```yaml
---
title: "<Theme> — Layer 0 raw corpus survey"
date: <date>
theme: <kebab-case-theme>
layer: output
stage: layer0-raw-survey
skill: corpus-survey
tools: bible-mcp (<tools actually used>)
draws_on:
  - <OSIS refs and WORK.chapter.paragraph refs, grouped by book>
---
```

Body: flowing prose organized by the material's own structure (clusters, roots, registers, arcs) — not by tool or by a fixed template. Bold-lead paragraphs (`**The core cluster.**`) are the pilot's proven shape. Length follows the material; the pilot ran ~1,200 words for a rich theme. Include the closing synthesis question, checkable claims, and gaps.

## What NOT to do

Do not filter for interestingness, avoid the obvious, reach for cross-disciplinary material, or compress into aphorisms — those are Layer 2 dispositions and applying them here prunes the seed-bed. Do not import training-knowledge claims about the corpus without checking them against it (that's what the tools are for). Do not paraphrase verses when the actual wording carries the point — quote, with refs.
