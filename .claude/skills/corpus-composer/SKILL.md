---
name: corpus-composer
description: Layer 2 of the bible-mcp synthesis pipeline — composes a polished, arc-driven piece from a Layer 0 corpus-survey artifact, welding cross-disciplinary material around the survey's spine. Use this whenever a survey artifact exists and the user wants the composed piece ("compose living water", "run the composer on the wilderness survey", "layer 2 on this", "write the piece"), or when the user asks for an essay/piece on a theme that already has a layer0-raw-survey file in outputs/. Requires a survey artifact as input — if none exists for the theme, run corpus-survey first rather than composing from scratch; composing without a survey demonstrably produces collage instead of argument.
---

# Corpus Composer (Layer 2)

You are turning a Layer 0 survey into a composed piece. The controlling principle, proven by A/B comparison (potter-and-clay, July 2026): **the survey is the spine, not a source.** The same composition skill run with and without a survey produced, respectively, an argument ("While the Clay Is Wet") and a collage. The survey's arc structures the piece; your cross-disciplinary additions compose *around* that spine. When survey material and a tempting perpendicular gem compete for a structural position, the survey wins.

## Input

Read the survey artifact fully before anything else. Identify, explicitly (in scratch notes), *this survey's own*:
- **arc** — every survey has one, and it is never the pilot's (the potter survey ran verb → cosmos → history → heart; the living-water survey ran translation-camouflage → ownership → grammar-fault-line; yours will be different again). Reverse-engineer it from how the survey's material actually builds.
- **hinge** — the one distinction or tension the material turns on ("whether the clay is still wet" was the pilot's; find this survey's).
- **register map**,
- **closing question** — this is usually your ending, handed forward,
- **epistemic tags and Gaps** — both must survive into your prose. Gaps (versification traps, citation-index misses, thin layers) are constraints you inherit, not problems you fix: never assert around a gap the survey flagged.

A prospector seed-stream for the theme, if one exists, is optional secondary input: mine it for collision material, not structure.

## Pipeline

Three steps. There is no facet-explosion step — with a survey in hand it re-answers questions already answered (measured waste in the pilot: ~7 of 17 planning categories pre-empted). Keep brief lab notes as `composer-notes.md` beside your output file; they cost little and every studied run has used them.

**1. Gem extraction — from the survey first.** Pull the survey's sharpest load-bearing items. Then, deliberately, extract 5-10 training-knowledge candidates by reading survey items *against* other domains: for each major survey finding ask "what field has something exact to say to this?" (chemistry to Jeremiah's two chapters; William James's plasticity to the yetser). This directed collision is where all the pilot's emergent material came from — it does not happen by free association, it happens by interrogating specific survey claims.

**2. Cross-pollinate and curate to the arc.** Keep a weld only if it is exact (the mechanism actually matches, not vibes-matches) and if it serves the survey's arc. Sequence: open on the hinge, alternate scales, place welds immediately after the survey material they illuminate, end on the survey's closing question — reopened, not answered. Shape: roughly 1,200-2,000 words; numbered sections plus a coda, as many or few as the arc needs — section count serves the arc, not a quota. Cut real gems that don't serve the spine without regret (the pilot cut the golem and the potter's field; both were good; neither belonged).

**3. Polish, preserving epistemic care.** One investigative voice; concrete names, dates, numbers; quote scripture rather than paraphrasing when wording carries the argument. Every epistemic tag in the survey survives translation into prose ("that is midrash, not grammar — but the consonantal difference is really there"). Never fabricate specificity: numbers, attributions, and study names you are confident of are the craft's asset; invented ones are its one unforgivable failure. When unsure, generalize or cut.

## Checkable-claims appendix — required

End the artifact (after the piece, under `## Checkable claims`) with every factual assertion that can be verified against the corpus with a tool call: occurrence counts, single-word links between passages ("obnayim occurs exactly twice"), quotation wordings, versification alignments. One line each: the claim + the verifying call. Three rules settle what belongs where: (a) carry forward a survey-verified claim only if your prose reasserts it, marked "verified in Layer 0"; (b) list every *new* corpus-checkable claim your composition introduced, unmarked — these are the verification pass's real work; (c) training-knowledge welds that cannot be tool-checked (halakhah, Qumran, physiology, art history) go in a short `### Outside-corpus assertions` note after the list — named so the human editor knows exactly which claims rest on the model's confidence rather than the corpus. These appendices get run through bible-mcp before Layer 3 — the verification pass has so far confirmed every sampled claim (H0070's two occurrences; the hetoimazō link between Rev 12:6 and Mark 1:3; the miqweh homograph at H4723/H4723a), and one check *upgraded* a hedge into a finding. This appendix is what makes the piece *grounded* rather than merely plausible.

## Output artifact

Write as `YYYY-MM-DD-<theme>-layer2-<short-title>.md`. Default location is the project's `outputs/` folder; a caller-directed path overrides the location (naming and frontmatter conventions still apply). Frontmatter:

```yaml
---
title: "<Piece title>"
date: <date>
theme: <kebab-case-theme>
layer: output
stage: layer2-composed
skill: corpus-composer
derived_from: <survey filename>
draws_on:
  - <refs actually used, from the survey's list plus any added>
---
```

## What NOT to do

Do not research from scratch or treat the survey as one source among many. Do not let a cross-disciplinary gem displace survey material from a structural position. Do not resolve the survey's central tension — the pilot's piece ends "What state is the clay in?", not with an answer; the corpus's unresolved questions are the product's live edge. Do not strip epistemic caveats for smoothness. Do not pad: a weld that needs a paragraph of setup isn't a weld.
