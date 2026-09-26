"""Chunk 4 of the weight>=10 batch (indices 450-599). Same mechanism as chunk1-3.

Note: index 459 (Deuteronomy<->Pentateuch, w=11) is a stale duplicate — Phase 4's
candidate generation creates one links row per (method, pair), so the same concept
pair can appear twice in the static batch file if both 'coverse' and
'cross_reference_chain' produced a row for it. This exact pair was already judged
'narrower' in chunk1 (from its w=19 occurrence), which deleted all concept_associated
rows for the pair including this one's underlying row. Kept as 'associated' here
(a safe no-op — nothing left to delete or duplicate) rather than re-inserting a
redundant edge. Flagged in ROADMAP.md as a Phase 4 dedup gap to fix before the next
mechanical-edge generation pass."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-w10.json")))

DECISIONS = [
    (450, "assoc", "Amos 1:1/2 Kgs 14:21 place Amos's ministry during Uzziah's reign — temporal co-occurrence, not hierarchy."),
    (451, "assoc", "Hag 1:1/Neh 7:7 co-list Jeshua among post-exilic leaders alongside a governor reference."),
    (452, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (453, "assoc", "Neh 12:1/12:10 co-list Ezra-era and Jeshua-lineage names in a priestly genealogy."),
    (454, "assoc", "Jer 50:38/51:7 condemn Babylon's idols within a prophetic oracle — thematic co-occurrence, not hierarchy."),
    (455, "assoc", "Ezek 16:32/Jer 3:20 discuss adultery in the prophetic marriage-metaphor; no direct textual link to Song of Solomon in the cited evidence."),
    (456, "assoc", "Dan 3:10/3:15 list flute and sackbut as sibling instruments, neither subsuming the other."),
    (457, "assoc", "Dan 3:10/3:15 list flute and psaltery as sibling instruments."),
    (458, "assoc", "Dan 3:10/3:15 list psaltery and sackbut as sibling instruments."),
    (459, "assoc", "Stale duplicate of the pair already judged narrower in chunk1 (from its higher-weight occurrence) — kept as a no-op associated rather than re-inserting a redundant edge; see module docstring."),
    (460, "assoc", "Deut 5:14/Gen 2:2 tie the Sabbath's application to sojourners numerically, not taxonomically, to 'seven.'"),
    (461, "assoc", "Same evidence as Proselyte/Seven — a calendrical coincidence, not hierarchy."),
    (462, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (463, "assoc", "Ezek 38:5/30:5 list Cush and Put as coordinate peoples."),
    (464, "assoc", "Ezek 38:5/27:10 (Cush and Put; Persia/Lydia/Put as warriors) — weak/unrelated link to 'Pul' specifically."),
    (465, "assoc", "Dan 9:25/Isa 9:6 present messianic prophecy, matching the Christ/Prophecy fallback."),
    (466, "assoc", "Gen 4:12/Lev 26:36 (the curse on tilling; a covenant-curse of faintness) — weak/unrelated evidence for an agriculture-leaf relation."),
    (467, "narrower:b", "Num 13:33 identifies the Nephilim as the ancestral/named category behind the Anakim giants the spies encountered, matching the Emims/Zamzummims specific-giant-group pattern."),
    (468, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (469, "assoc", "2 Sam 21:16/Gen 14:5 (a giant's bronze-tipped spear; unrelated Rephaim narrative) — weak, not a copper-composition claim about the Giants concept itself."),
    (470, "assoc", "Exod 29:13/Lev 9:19 don't establish a clean/food hierarchy beyond general sacrificial-fat context, matching Caul/Food."),
    (471, "assoc", "Exod 29:13/29:18 don't establish a clean/fire hierarchy beyond general sacrificial context."),
    (472, "assoc", "2 Chr 15:16/Exod 34:13 show groves and high places torn down together in cultic reform, matching the Altar/Grove and Altar/High-place pattern."),
    (473, "assoc", "1 Kgs 7:48/2 Chr 4:8 list basins among the temple's general furnishings, not specifically the altar's own utensils (unlike the firepan/pan cases)."),
    (474, "assoc", "Exod 21:12/Gen 9:6 address murder's penalty broadly; the cities-of-refuge institution is a specific application this pair's evidence doesn't directly establish."),
    (475, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (476, "causes:b", "Gen 9:21 directly ties drinking wine to becoming drunk — the wine is what causes the drunkenness."),
    (477, "assoc", "Gen 10:7/Ps 72:10 name Seba as Cush's son; kept associated as an eponym relation rather than asserting taxonomic hierarchy, matching the Havoth-jair/Jair pattern."),
    (478, "assoc", "Ezek 38:22/Gen 19:24 show brimstone raining on Gomorrah — an instrument-of-judgment relation, not hierarchy."),
    (479, "narrower:b", "Gen 14:2 places Zeboim among the cities of the plain Deut 34:3 also describes, matching the Gomorrah/Plain geographic-containment pattern."),
    (480, "assoc", "Deut 11:30/Gen 12:6 (Shechem's mountains; Abram's journey) — weak/unrelated link to 'grove' specifically."),
    (481, "assoc", "Ezra 2:28/Josh 8:17 co-list Ai and Bethel as neighboring cities, siblings."),
    (482, "assoc", "1 Chr 27:25/2 Chr 26:10 (a royal storehouse official; wilderness towers) — weak/unrelated link to 'plain.'"),
    (483, "assoc", "Gen 14:5/Jer 48:1 co-list Kirjathaim and Nebo as neighboring Moabite towns, siblings."),
    (484, "narrower:b", "Josh 12:4 names Edrei as one of Og of Bashan's cities, matching the geographic-containment pattern."),
    (485, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (486, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (487, "assoc", "Josh 15:4/Num 34:5 use 'brook of Egypt' and 'river of Egypt' as alternate names for the same boundary feature, matching the Edom/Seir naming-equivalence pattern."),
    (488, "assoc", "Gen 15:18/Exod 3:8 (the Euphrates covenant-boundary; the deliverance promise) — weak/unrelated link between river and wine."),
    (489, "assoc", "Gen 16:10/17:20 (an angel's promise to Hagar; a blessing on Ishmael) — weak/unrelated link to prayer specifically."),
    (490, "assoc", "Deut 32:14/Ps 81:16 list butter and wheat as coordinate abundance items."),
    (491, "causes:a", "Deut 32:14/Isa 7:22 tie goat's milk directly to the goat as its source — the animal produces the milk."),
    (492, "assoc", "1 Sam 25:1/Deut 34:8 show burial and communal mourning as companion practices, matching the Funeral/Mourn call."),
    (493, "assoc", "1 Sam 25:3/Josh 15:13 show Caleb given Kirjath-arba (Hebron) as inheritance, matching the Caleb/Hebron pattern."),
    (494, "narrower:a", "Exod 30:13/Lev 27:25 present the shekel as the specific standard unit within the broader system of weights and valuations."),
    (495, "assoc", "2 Chr 9:1/Isa 60:6 (the queen of Sheba's camels; a prophecy of camel caravans) — weak/unrelated link to the ephah measure."),
    (496, "assoc", "2 Kgs 4:42/Deut 32:14 list food and wine/milk as coordinate provision items."),
    (497, "assoc", "2 Kgs 4:42/Deut 32:14 don't specifically establish goat as a food-subtype in the cited text — kept associated rather than overreaching."),
    (498, "assoc", "Deut 28:40/Mic 6:15 list olive-oil anointing and wine-pressing as coordinate agricultural blessings/curses, not a direct anoint-wine relation."),
    (499, "assoc", "1 Chr 5:1/Deut 21:17 discuss Jacob obtaining the firstborn birthright — a narrative event involving a person, not a taxonomic first-born/Jacob relation."),
    (500, "narrower:a", "1 Sam 15:12/7:12 (Saul's monument; Samuel's memorial stone) support the pillar as a specific standing-stone form within the general stone category."),
    (501, "part_of:a", "Exod 22:17/1 Sam 18:25 show the dowry/bride-price as a required component of the marriage transaction."),
    (502, "assoc", "2 Chr 33:6/1 Sam 15:23 list divination and idolatry-adjacent rebellion as coordinate forbidden-practice categories, not hierarchy."),
    (503, "assoc", "2 Sam 19:24/15:30 (Mephibosheth's unkempt beard; David's mourning journey) — weak/unrelated evidence for a beard-as-dress-type claim."),
    (504, "assoc", "Deut 32:14/Gen 49:11 list goat and wine as coordinate abundance items."),
    (505, "assoc", "Deut 1:1/Josh 9:1 (Moses' location beyond Jordan; an unrelated news report) — weak/unrelated link to 'plain.'"),
    (506, "assoc", "Exod 3:1/24:13 (Moses shepherding; Moses ascending a mountain) — different narratives, no clean desert-hill relation established."),
    (507, "assoc", "Amos 1:3/1:6 (parallel oracle formulas against different nations) — weak/unrelated evidence for an agriculture-prophecy relation."),
    (508, "assoc", "Josh 24:33/Exod 6:23 record Eleazar and Nadab as brothers, sons of Aaron — genealogical, not hierarchy."),
    (509, "narrower:a", "Exod 8:21/Ps 78:45 present the plague of flies as one specific instance within the general category of plagues."),
    (510, "assoc", "1 Kgs 8:5/1 Chr 16:1 show burnt offerings performed at the tabernacle, matching the Altar/Burnt-offering location-practice pattern."),
    (511, "assoc", "Lev 23:2/Ps 81:3 tie a holy convocation to the Feast of Trumpets' calendar, matching the Convocation/First-fruits co-occurrence pattern."),
    (512, "part_of:b", "Judg 4:3/Josh 17:16 name iron as the reinforcing material of chariots ('chariots of iron')."),
    (513, "assoc", "Isa 17:13/Ps 1:4 use chaff in unrelated poetic judgment images — weak specific link to agriculture as a concept."),
    (514, "assoc", "1 Sam 18:6/Exod 15:20 show Miriam the prophetess dancing — person-role co-occurrence, not hierarchy."),
    (515, "assoc", "2 Sam 6:14/1 Sam 2:18 (David dancing in a linen ephod; Samuel's linen garment) — narrative co-occurrence, not hierarchy."),
    (516, "assoc", "2 Sam 6:14/1 Sam 2:18 show David dancing while wearing an ephod — narrative detail, not hierarchy."),
    (517, "assoc", "1 Kgs 19:11/Exod 19:16 list earthquake and thunder as coordinate theophany phenomena, siblings."),
    (518, "assoc", "Deut 24:19/Lev 23:22 tie gleaning law to provision for foreigners, matching the Agriculture/Poor pattern."),
    (519, "assoc", "Lev 25:39/Exod 21:2 (debt-servitude release law; Hebrew-servant law) — related legal concepts, not a clean freedom-loan hierarchy."),
    (520, "assoc", "Deut 18:10/1 Sam 28:3 use witch and wizard as near-synonymous occult-practitioner terms, matching the established practitioner-pair pattern."),
    (521, "assoc", "Deut 10:18/Exod 22:22 list citizen-protections and widow-protections as coordinate categories owed justice."),
    (522, "assoc", "Num 9:5/Josh 5:10 record Passover observance within Pentateuch narrative — the book records the practice, not a hierarchy."),
    (523, "assoc", "Num 28:26/Exod 23:16 tie a convocation to the Feast of Tabernacles' calendar, matching the Convocation/Pentecost pattern."),
    (524, "assoc", "Exod 25:4/Ezek 16:10 name blue as a descriptive dye-color in clothing description, matching the Colour/Dress pattern."),
    (525, "assoc", "Exod 30:34/25:6 list frankincense and anointing oil as coordinate spice/ritual ingredients, siblings."),
    (526, "assoc", "Lev 16:2/2 Chr 5:14 show the cloud appearing near the ark's dwelling-place — co-occurring phenomenon, not a structural relation, matching the Cloud/Tabernacle call."),
    (527, "assoc", "Exod 29:42/25:22 show the cloud associated with the meeting-place above the mercy-seat — co-occurrence, matching the Cloud/Tabernacle call."),
    (528, "narrower:b", "Exod 25:30/1 Chr 23:29 name cake among baked-goods offerings — cake is a specific type of bread/baked good."),
    (529, "assoc", "Exod 26:1/26:31 name curtain and veil as distinct tabernacle fabric elements, siblings rather than one part of the other."),
    (530, "part_of:b", "Exod 26:31 specifies the veil as a distinct woven component of the tabernacle's overall structure."),
    (531, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (532, "part_of:b", "Exod 27:3/38:3 name flesh-hooks among the altar's bronze utensils, matching the Altar/Pan and Altar/Firepan pattern."),
    (533, "assoc", "Exod 28:40/28:4 co-list girdle and mitre as distinct priestly-garment items, siblings."),
    (534, "assoc", "Job 28:19/Exod 28:17 compare gold and gemstones (ruby) in value — coordinate precious materials, not hierarchy."),
    (535, "assoc", "Lev 3:5/Exod 29:13 don't clearly establish fire and food as hierarchically related beyond general sacrificial context."),
    (536, "assoc", "Exod 29:13/Lev 9:19 don't establish a sheep-specific food hierarchy beyond general sacrificial-fat context, matching Fat/Sheep and Food/Goat."),
    (537, "assoc", "Song 4:14/Gen 43:11 (spice list; unrelated gift-giving narrative) — weak/unrelated link between frankincense and wine."),
    (538, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (539, "assoc", "1 Kgs 16:33/Exod 34:13 show Asherah poles and high places as coordinate cultic-reform targets, matching the Idol/High-place pattern."),
    (540, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (541, "assoc", "Deut 12:11/12:5 (the chosen place for offerings; the chosen place generally) — both concern worship centralization, not a direct high-place/tithe hierarchy."),
    (542, "assoc", "Deut 24:13/24:15 address pledge-return and wage-timeliness as adjacent but distinct labor/finance laws, not hierarchy."),
    (543, "assoc", "Deut 18:10/2 Chr 33:6 list enchantments and witchcraft as sibling forbidden practices, neither subsuming the other."),
    (544, "assoc", "2 Chr 33:6/28:3 (child sacrifice; incense in the valley of Hinnom) — both idolatrous practices in the same valley, not a divination-Gehenna hierarchy."),
    (545, "assoc", "Dan 2:2/Isa 8:19 show an astrologer and familiar-spirit consultation as coordinate occult-practitioner terms."),
    (546, "assoc", "Dan 1:20/Isa 19:3 show an astrologer and unrelated Egyptian-spirit failure — weak link, but kept consistent with the practitioner-pair fallback."),
    (547, "assoc", "Deut 18:10/1 Sam 28:3 show enchantments and a wizard as practice-and-practitioner, matching the established fallback."),
    (548, "assoc", "2 Chr 33:6/1 Sam 15:23 list familiar-spirit consultation and witchcraft as sibling forbidden practices."),
    (549, "narrower:b", "Lev 25:9/Num 10:10 tie trumpet-blowing to the Feast of Trumpets specifically, matching the First-fruits/Pentecost pattern of a feast named for its central practice."),
    (550, "assoc", "Isa 41:14/Ps 19:14 use kinsman and redeemer near-synonymously as overlapping legal-theological role terms."),
    (551, "assoc", "Isa 11:2/59:21 present Christ's relation to the covenant — a messianic-fulfillment relation this vocabulary has no verb for, matching the Christ/Prophecy fallback."),
    (552, "assoc", "1 Chr 23:21/23:6 (Merarite genealogy; Levitical divisions) — weak/unrelated specific link to Eleazar."),
    (553, "assoc", "Isa 32:2/41:18 (a hiding place from wind; rivers on bare heights) — weak/unrelated link between agriculture and valley."),
    (554, "assoc", "2 Kgs 13:25/14:25 (territory restoration; Jeroboam II's border) — narrative/political co-occurrence, not hierarchy."),
    (555, "narrower:b", "Josh 12:4 names Edrei among the sixty cities of Bashan captured, matching the Fenced-cities/Jerusalem specific-city pattern."),
    (556, "assoc", "2 Chr 33:6/2 Kgs 23:24 list divination and teraphim as coordinate objects/practices of the same reform, not hierarchy."),
    (557, "assoc", "Jer 48:23/Num 32:38 co-list Baal-meon and Nebo as neighboring Moabite towns, siblings."),
    (558, "assoc", "1 Kgs 4:13/Num 32:41 use Bashan-havoth-jair as a fuller/alternate form of Havoth-jair, matching the Edom/Seir naming-equivalence pattern."),
    (559, "assoc", "Num 32:41 names the region after the person Jair — an eponym relation, matching the Havoth-jair/Jair pattern."),
    (560, "assoc", "Deut 12:12/16:14 (festival rejoicing law) doesn't specifically address begging — weak/unrelated evidence."),
    (561, "assoc", "Amos 6:12/5:7 pair hemlock and wormwood as coordinate bitterness metaphors, matching the Gall/Hemlock pattern."),
    (562, "assoc", "Isa 43:19/41:18 use desert and valley in parallel blessing/transformation imagery, not hierarchy."),
    (563, "assoc", "1 Chr 19:7/2 Sam 10:6 list Maachah and Rehob as allied Aramean kingdoms, siblings."),
    (564, "assoc", "Dan 2:10/2:27 show astrologer and Daniel's own role as interpreter — a practitioner-comparison, matching the established fallback."),
    (565, "assoc", "1 Chr 8:33/1 Sam 9:1 record Abiel as Kish's ancestor — genealogical, not hierarchy."),
    (566, "assoc", "1 Chr 8:33/2 Sam 2:8 record Abiel as an ancestor in Abner and Eshbaal's line — genealogical, not hierarchy."),
    (567, "assoc", "1 Chr 25:1/2 Kgs 3:15 show Asaph appointed for music and a musician summoned elsewhere — person-practice relation, not hierarchy."),
    (568, "assoc", "1 Chr 25:1/1 Sam 10:5 show Asaph's musical appointment near an instrumental-music narrative — person-practice relation."),
    (569, "assoc", "2 Sam 15:30/Esth 6:12 (David's barefoot mourning walk; Haman's separate account) — weak/unrelated evidence for a barefoot-dress relation."),
    (570, "assoc", "1 Sam 25:36/Nah 1:10 list sheep and wine as coordinate feast provisions, matching the Banquet/Wine pattern."),
    (571, "assoc", "2 Sam 5:11/1 Chr 14:1 show Hiram supplying materials for building, matching the Cedar/Hiram provider-resource pattern."),
    (572, "assoc", "Isa 35:2/Song 7:5 (blooming/rejoicing imagery; a hair-color description) — weak/unrelated link between cedar and colour."),
    (573, "assoc", "1 Chr 11:22/2 Sam 8:18 (Benaiah's exploits; his command over Cherethites) — narrative/administrative proximity to Philistine-adjacent context, not hierarchy."),
    (574, "assoc", "Esth 3:12/1 Kgs 21:8 show a seal used to authenticate written decrees — an instrument-for-practice relation, not composition."),
    (575, "assoc", "2 Kgs 12:10/2 Sam 8:17 (a money chest; unrelated priestly genealogy) — weak/unrelated link between the ark and Zadok."),
    (576, "assoc", "2 Chr 26:17/1 Chr 12:28 (a priest named Azariah; a separate Zadok reference) — weak/unrelated specific link."),
    (577, "assoc", "1 Kgs 7:9/5:17 describe building-stone construction generally; kept associated rather than asserting 'house' as a clean broader category over 'temple' from this evidence."),
    (578, "assoc", "1 Kgs 8:22/Exod 9:33 show Solomon praying at the altar, matching the Altar/Sacrifice location-practice pattern."),
    (579, "assoc", "1 Kgs 10:11/2 Chr 8:18 show Hiram's fleet supplying algum wood, matching the Cedar/Hiram provider-resource pattern."),
    (580, "assoc", "1 Kgs 10:11/2 Chr 8:18 show Hiram's fleet supplying almug wood, matching the same pattern."),
    (581, "assoc", "1 Kgs 15:8/14:1 (Abijam's burial notice; an unrelated illness of Jeroboam's son) — coincidental textual proximity, not a real relation."),
    (582, "assoc", "2 Chr 25:27/2 Kgs 14:19 show Jehoash's conspiracy against Amaziah — narrative co-occurrence, not hierarchy."),
    (583, "assoc", "1 Chr 5:26/5:6 name Tiglath-pileser and a captivity context near Isaiah's era — historical co-occurrence, not hierarchy."),
    (584, "assoc", "Jer 44:17/7:18 discuss 'queen of heaven' worship without clearly identifying it as a hierarchy with the moon specifically in the cited text."),
    (585, "narrower:b", "Jer 46:2/2 Kgs 23:29 name Necho II as a specific historical Pharaoh — an instance of the general Pharaoh title."),
    (586, "assoc", "Jer 40:8/2 Kgs 25:23 co-list Jaazaniah and Johanan among military captains after Jerusalem's fall."),
    (587, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (588, "assoc", "2 Chr 34:14/Ezra 7:10 show scribes handling the law, matching the Pentateuch/Scribes role relation."),
    (589, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (590, "assoc", "2 Chr 36:10/Dan 5:2 (temple vessels taken to Babylon; Belshazzar's feast) — same narrative arc but not a direct exile-wine hierarchy."),
    (591, "narrower:b", "Joel 3:15's darkened sun and moon describes an eclipse-like event as a specific instance of darkness generally."),
    (592, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (593, "assoc", "Job 38:29/6:16 use frost and ice in parallel winter-phenomena imagery, siblings rather than one causing the other in the cited text."),
    (594, "assoc", "Ps 19:10/119:103 compare gold and honey in value within a poetic parallelism, coordinate not hierarchy."),
    (595, "assoc", "Isa 13:22/34:13 mention dragon (jackal) and nettle-adjacent thorn imagery in adjacent desolation oracles, coordinate not hierarchy."),
    (596, "assoc", "Isa 11:8/59:5 use adder and basilisk near-synonymously as venomous-serpent terms."),
    (597, "assoc", "Isa 1:25/Mal 3:3 show the refiner acting upon dross to purify metal — an agent-object relation the fixed vocabulary's causes verb doesn't cleanly fit (refining removes dross, it doesn't produce it)."),
    (598, "assoc", "Isa 59:17/9:7 use armor imagery near a messianic-increase prophecy — poetic parallel, not hierarchy, matching the Christ/Prophecy-adjacent fallback."),
    (599, "assoc", "Dan 3:5/3:7 show worship triggered by instrument sounds including the psaltery, matching the Adore/Cornet pattern."),
]


def main():
    judgments = []
    for idx, code, just in DECISIONS:
        p = BATCH[idx]
        a_id, b_id = p["a"]["id"], p["b"]["id"]
        entry = {"pair": [a_id, b_id], "justification": just}
        if code == "assoc":
            entry["verb"] = "associated"
        elif code == "contrasts":
            entry["verb"] = "contrasts"
        else:
            verb, side = code.split(":")
            first, second = (a_id, b_id) if side == "a" else (b_id, a_id)
            entry["verb"] = verb
            if verb == "narrower":
                entry["narrower"], entry["broader"] = first, second
            elif verb == "causes":
                entry["cause"], entry["effect"] = first, second
            elif verb == "part_of":
                entry["part"], entry["whole"] = first, second
        judgments.append(entry)

    out = {
        "batch_file": "phase5-batch-2026-09-26-w10.json",
        "model": "claude-in-session (Sonnet 5) — chunk 4 of the weight>=10 batch (indices 450-599)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-w10-chunk4.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments to {out_path}")


if __name__ == "__main__":
    main()
