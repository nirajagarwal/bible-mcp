# Pipeline Assessment: corpus-survey + corpus-composer, first road test

**Date:** 2026-07-17 · **Test themes:** living water, wilderness · **Baseline:** potter-and-clay (pilot) · **Protocol:** skills drafted from the potter experiment's evidence → two full Layer 0 → Layer 2 runs by independent agents following the SKILL.md files verbatim → verification sampling → v1.1 revision from convergent critiques.

## Verdict: the pipeline generalizes

Both themes produced surveys and pieces of pilot quality with **zero potter-specific scaffolding carried over**. Each theme found its own hinge and its own question, which is the strongest sign the discipline (not the example) is doing the work:

**Living water** — hinge: *living = moving* (stored water is dead water). Headline findings: English translation splits *mayim chayyim* by register ("flowing/fresh" in Torah ritual, "living" in theology), so keyword search structurally loses half the theme — a method finding of the translation-camouflage class. John + Revelation own 42 of 79 NT *hydōr* occurrences; John uses the participle (*hydōr zōn*, water that lives) while Revelation always shifts to the genitive (*hydōr zōēs*, water that gives life) — a total, corpus-verifiable grammatical fault line. Sir 24:21 ("drink me and thirst for more") verbatim contradicts John 4:14 ("never thirst"). Julian inverts the whole theme: God is the thirsty one. Question: **does living water end thirst or teach it?**

**Wilderness** — hinge: *midbar* is a place, *shemamah* is a verdict; the Greek then grammaticalizes the split (*erēmos* the noun hosts theophany and refuge; *erēmoō/erēmōsis* the verb-family only destroys). The dabar/midbar braid handled with exemplary epistemic care: folk etymology named as such, while the corpus data underneath it (dabar's largest raw count in Numbers; MT Hos 2:16 putting "I will speak" inside "the wilderness"; Deut 8:3) stands on its own. The Isa 40:3 attachment fork (MT binds "in the wilderness" to the way; all three Gospels to the voice) mapped with the LXX middle-term correctly flagged unverifiable in-corpus. Question: **is emptiness the corpus's precondition for address?**

## Verification loop: 6 calls, 6 confirmations, 1 upgrade

Sampled the highest-leverage checkable claims: Rev 12:6 and Mark 1:3 share *hetoimazō* (the prepared *place* and prepared *way* are one verb — an obnayim-class link, now confirmed); Rev 7:17 is genitive *zōēs* (the John/Revelation split holds); and the Jer 17:13 *miqweh* pun the composer hedged is **corpus-visible after all** — MACULA splits the identical written form into H4723 "hope" and H4723a "gathering of waters" (Gen 1:10, Exod 7:19, Lev 11:36). A verification pass that *upgrades* a hedge into a finding is the loop working exactly as designed.

## New corpus friction (adds to the docket)

1. **Versification offsets are worse than the Isaiah-64 case suggested**: Jer 8:23 returns empty in word_study (MT = Eng 9:1); **Hosea 2 interlinear is off by two** (Eng 2:14 = MT 2:16) — offsets are not uniformly ±1; Exodus 8-class skew in word_study samples. Four confirmed offset sites now. TVTMS import's priority hardens further.
2. **get_citations recall misses now number three**: Barnabas 11.1 quoting Jer 2:13, Barnabas 9 quoting Isa 40:3, plus the pilot's 1 Clem 39/Job 4:19. All verbatim quotations found by full-text search, all invisible to the footnote-extracted index. The tier-2 shingling case is no longer speculative.
3. **word_study interface paper-cuts**: Strong's queries require zero-padding (H953 fails, H0953 works); pointed-Hebrew lemma queries fail where Strong's numbers succeed; gloss-keyed queries conflate lemmas; transliteration queries (e.g. "miqweh") return nothing.
4. Stemmed prose search conflates senses (desert/deserted/"deserts" as merits).

## Skill revision (v1.0 → v1.1, applied)

The four agents' critiques converged independently on the same gaps — a good sign the skills' flaws were structural, not stylistic. Fixed: caller-path precedence over the hardcoded `outputs/`; the checkable-claims carry-forward policy plus a required `Outside-corpus assertions` note for uncheckable training-knowledge welds; arc guidance de-overfitted from the pilot ("identify *this* survey's arc"); hub-verse selection now defined by the register map (one hub per register); `get_citations` sparsity expectations set, with full-text search named as the real patristic probe; root-chain stopping rule and entity budget added; the composer's section-count quota subordinated to the arc.

## Recommendations

1. Ingest all five artifacts (2 surveys, 2 pieces, this assessment) into `outputs/` — the layer now has nine members and the frontmatter schema has survived three themes unchanged.
2. TVTMS import remains #1 on the build list, now with four confirmed offset sites as its test fixtures.
3. The citation-graph fix should be re-scoped from "check one footnote" to "tier-2 verbatim shingling, validated against the three known misses."
4. Zero-pad and alias the word_study query path (cheap server-side fix; three paper-cuts disappear).
5. The pipeline is ready for routine use: survey → compose → verify → edit. The next real test is Layer 3 — your edits on any of these three pieces will show what the pipeline still over- or under-delivers.
