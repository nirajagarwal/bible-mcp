"""Chunk 2 of the weight>=10 batch (indices 150-299). Same mechanism as chunk1."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-w10.json")))

DECISIONS = [
    (150, "assoc", "Deut 24:21/24:19 tie gleaning law to provision for the poor — co-occurrence in law."),
    (151, "narrower:b", "1 Sam 15:23 names witchcraft as a specific occult practice within the broader divination Easton's entry catalogs."),
    (152, "assoc", "Amos 8:10/Jer 48:37 pair baldness and beard-cutting as coordinate mourning practices."),
    (153, "assoc", "Joel 1:4/2 Chr 6:28 list caterpillar and mildew as coordinate agricultural plagues."),
    (154, "assoc", "Deut 29:18/Hos 10:4 pair gall and hemlock as sibling poisonous plants, neither subsuming the other."),
    (155, "assoc", "Deut 32:42/32:23 use arrows and dart near-synonymously as weapon imagery, insufficient to assert hierarchy."),
    (156, "assoc", "1 Chr 6:8/1 Kgs 2:35 (genealogy, Benaiah replacing Joab) don't establish Ahitub specifically as a high priest in the cited text."),
    (157, "assoc", "1 Chr 18:16/2 Sam 20:25 co-list scribe and priestly officials in the same administrative roster."),
    (158, "assoc", "1 Kgs 1:8/2 Sam 20:25 co-list Benaiah and Zadok among David's officials."),
    (159, "assoc", "2 Chr 25:27/2 Kgs 14:19 narrate Amaziah's death and burial — narrative co-occurrence, not hierarchy."),
    (160, "assoc", "2 Kgs 18:18/2 Chr 34:8 don't establish Eliakim specifically as holding the recorder's office in the cited text."),
    (161, "causes:a", "Zech 8:19's four annual fasts specifically commemorate stages of the Babylonian siege and exile — the exile is what the fasts memorialize."),
    (162, "assoc", "Amos 2:9/Exod 3:8 (Amorite height compared to cedars; unrelated deliverance promise) — weak link, correct fallback."),
    (163, "assoc", "Deut 17:3/Jer 8:2 warn against astral worship generally without a specific heaven-moon hierarchy in the cited text."),
    (164, "narrower:b", "2 Kgs 17:16/Deut 4:19 name the sun as one of the 'host of heaven' worshiped as false gods."),
    (165, "narrower:b", "2 Kgs 21:3 places the 'host of heaven' as a specific class of objects worshiped within the heavens generally."),
    (166, "assoc", "Gen 3:15/Isa 7:14 present Christ as prophecy's fulfillment — a relation this vocabulary doesn't yet have a verb for; associated is the honest fallback."),
    (167, "narrower:b", "1 Kgs 1:40/Dan 3:5 name psaltery among Easton's catalog of specific instruments."),
    (168, "assoc", "1 Kgs 4:13/Deut 4:43 mention cities in a plain region without a taxonomic city-plain relation."),
    (169, "assoc", "Gen 14:6/Deut 2:12 treat Arabia and Edom as adjacent/overlapping regions (via the Horites/Seir), not one within the other."),
    (170, "assoc", "1 Kgs 19:19/19:13 (Elisha's oxen; Elijah's cloak) — weak/unrelated evidence, correct fallback."),
    (171, "assoc", "2 Sam 8:14/Gen 25:23 (Edom's subjugation; Esau's birthright oracle) — weak specific link to a first-born hierarchy."),
    (172, "assoc", "1 Sam 18:6/Judg 11:34 show timbrel accompanying dance — co-occurring instrument and practice, matching the Dance/Music,Instrumental pattern."),
    (173, "assoc", "1 Chr 25:5/2 Sam 24:11 don't establish more than co-occurrence of instrumental music and prophetic activity."),
    (174, "assoc", "1 Chr 2:50/1 Sam 7:1 mention both places in unrelated genealogical/narrative contexts — no hierarchy established."),
    (175, "causes:b", "Amos 8:10/Jer 6:26 show baldness (head-shaving) as a mourning expression, matching the established Mourn-causes pattern."),
    (176, "assoc", "Ezek 47:12/Ps 1:3 pair trees and rivers in blessing imagery — co-occurrence, not hierarchy."),
    (177, "assoc", "Ezek 16:11/Dan 5:16 (jewelry; unrelated interpretation offer) — weak/unrelated evidence."),
    (178, "part_of:b", "2 Sam 6:14/Gen 41:42 (linen ephod; robes of fine linen) support linen as one of apparel's materials, matching the Dress/Linen pattern."),
    (179, "assoc", "1 Kgs 18:38/Lev 10:2 (Nadab's death by fire) — narrative event, not a conceptual hierarchy."),
    (180, "assoc", "Dan 1:20/Exod 8:7 show an astrologer as a practitioner of magic arts — person-to-practice, matching the Divination/Wizard fallback."),
    (181, "assoc", "Deut 15:1/Exod 21:2 don't establish 'debtor' as a taxonomic subtype of loan — a role-holder relation."),
    (182, "narrower:b", "Lev 19:9/23:10 present first-fruits offering as one specific agricultural practice within the broader topic of agriculture."),
    (183, "assoc", "Num 28:25/28:26 place a holy convocation on the day of firstfruits within Pentecost's calendar — co-occurrence, matching the Convocation/First-fruits call."),
    (184, "assoc", "Exod 28:15/26:1 don't establish more than descriptive coloring, matching the Colour pattern."),
    (185, "assoc", "Exod 26:1/35:6 (curtain materials; general offering materials) — weak specific link between curtain and dress."),
    (186, "part_of:a", "Exod 26:1 specifies the tabernacle curtains are made of fine linen, matching the established material-composition pattern."),
    (187, "assoc", "1 Sam 18:4/Isa 61:10 co-list girdle and head ornamentation as sibling garment components, neither part of the other."),
    (188, "assoc", "Esth 8:15/6:8 don't establish more than descriptive coloring of royal garments."),
    (189, "narrower:a", "Ezek 44:18/Exod 39:28 describe the bonnet (turban) as a specific type of head-dress."),
    (190, "assoc", "2 Chr 35:13/Num 6:19 (Passover roasting; wave-offering wafers) — weak/unrelated evidence, container-content at best."),
    (191, "assoc", "Exod 29:13/Lev 9:19 don't establish a caul-clean hierarchy beyond general sacrificial context."),
    (192, "assoc", "Exod 29:13/29:22 don't establish a clean-liver hierarchy beyond general sacrificial context."),
    (193, "assoc", "Num 28:7/Exod 29:40 list oil and drink-offering as coordinate offering components, not composition (wine, not oil, is the drink-offering's material)."),
    (194, "narrower:b", "1 Kgs 7:23 describes 'the molten sea' as a specific, famously large laver in Solomon's temple — a named instance of the general laver category."),
    (195, "assoc", "Num 15:3/Exod 29:41 list flour and wine as coordinate offering components."),
    (196, "assoc", "Amos 6:6/Hos 3:1 (unrelated condemnation of excess; a separate marriage command) — weak/unrelated evidence."),
    (197, "assoc", "Amos 8:10/Jer 48:37 pair baldness and beard-clipping as coordinate mourning-related practices, neither subsuming the other."),
    (198, "assoc", "Deut 3:10/Num 21:33 mention Amorite cities including Edrei without establishing a clean containment relation in the cited text."),
    (199, "assoc", "2 Kgs 15:29/Num 32:1 place Aroer in Gadite territory — tribal allotment, not a taxonomic relation."),
    (200, "assoc", "Isa 43:19/Ps 105:41 use desert and wilderness near-synonymously."),
    (201, "assoc", "Deut 1:7/Josh 10:40 list hill country and plain as coordinate terrain categories conquered together."),
    (202, "part_of:b", "2 Chr 1:14/1 Kgs 9:19 show chariots as part of Solomon's military/army buildup."),
    (203, "assoc", "1 Sam 13:16/13:3 use encamping and garrisoning near-synonymously in the same military narrative."),
    (204, "part_of:b", "1 Kgs 5:6/Ezra 3:7 name cedar as the material commanded/procured for temple building construction."),
    (205, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (206, "part_of:b", "2 Chr 12:9/2 Kgs 16:8 place the temple's treasures within Jerusalem specifically — the temple is a building within the city."),
    (207, "assoc", "Ps 29:5/Isa 2:13 pair cedar and oak as coordinate tree types in judgment imagery, neither subsuming the other."),
    (208, "assoc", "Amos 1:3/2:6 (parallel oracle formulas against different nations) — weak/unrelated evidence for an agriculture-poetry relation."),
    (209, "assoc", "Ezek 23:37/Hos 1:2 use adultery and fornication near-synonymously in the prophetic marriage-metaphor."),
    (210, "assoc", "Amos 1:3/1:6 (both poetic oracle formulas) — weak/unrelated evidence for a poetry-prophecy hierarchy."),
    (211, "assoc", "Deut 17:3/2 Kgs 21:3 list moon and stars as coordinate objects of forbidden astral worship."),
    (212, "assoc", "Num 28:25/28:26 tie convocation to a calendar week, matching the Sabbath/Seven calendrical pattern."),
    (213, "assoc", "1 Kgs 9:28/Isa 13:12 name Ophir as gold's source location — a place-of-origin relation, not a taxonomic or causal claim about gold itself."),
    (214, "causes:a", "1 Kgs 19:16's command to anoint Jehu/Elisha shows the anointing act as what constitutes messianic (anointed-one) status."),
    (215, "assoc", "2 Kgs 14:9/Prov 26:9 pair bramble and thistle as coordinate thorny-plant types."),
    (216, "assoc", "Exod 29:13/29:18 show fat burned by fire on the altar — co-occurring ritual elements, not composition or clean causation."),
    (217, "narrower:b", "Ps 150:4/Exod 15:20 don't name 'organ' directly, but Easton's own Music,Instrumental catalog lists it among named instruments (pipe-organ/ugab), matching the established instrument-catalog pattern."),
    (218, "narrower:a", "Gen 22:7/8:20 (burnt-offering narratives) support burnt offering as a specific type within the general sacrifice category Easton's own Sacrifice entry would cover."),
    (219, "assoc", "1 Kgs 18:45/Num 25:8 — weak/unrelated evidence (storm clouds; an unrelated tent narrative) for a colour-tent relation."),
    (220, "assoc", "1 Kgs 18:2/2 Kgs 6:25 use dearth and famine near-synonymously."),
    (221, "assoc", "2 Sam 2:1/Num 13:22 place Talmai (a giant) in Hebron — person-in-place, not a place-within-place relation."),
    (222, "assoc", "Isa 53:10/9:7 (suffering-servant and messianic-increase passages) — weak specific link between covenant and prophecy in the cited text."),
    (223, "assoc", "Deut 16:11/12:7 use banquet and feast near-synonymously."),
    (224, "assoc", "Gen 27:28/Joel 2:19 list dew and wine as coordinate blessing-of-abundance items."),
    (225, "assoc", "Ezek 27:17/Deut 32:14 list corn and wine as coordinate trade/agricultural goods."),
    (226, "assoc", "Gen 45:18/27:28 list fat and wine as coordinate abundance items."),
    (227, "assoc", "Gen 28:18/1 Sam 7:12 show stones used both as idols and as memorial pillars in different narratives — mixed evidence, correctly kept associated."),
    (228, "assoc", "Exod 29:13/Lev 9:19 don't establish a sheep-specific liver hierarchy beyond general sacrificial fat context."),
    (229, "narrower:a", "2 Sam 13:18/Judg 5:30 describe the cloak as a specific garment within dress generally, matching the Mantle/Dress pattern."),
    (230, "assoc", "Isa 20:2/2 Kgs 1:8 (sackcloth removal; Elijah's hairy-garment description) — weak/unrelated link between dress and hair."),
    (231, "causes:b", "Ezra 9:3/Job 1:20 show beard-pulling/tearing as a mourning expression, matching the established Mourn-causes pattern."),
    (232, "causes:b", "Amos 8:10/Jer 6:26 show hair-related acts (baldness) as a mourning expression, matching the same causal pattern."),
    (233, "assoc", "Ezek 16:11/Gen 41:42 mention jewelry and dress in different narratives — weak/unrelated specific link."),
    (234, "part_of:b", "Ezek 16:10/16:13 name silk (or fine fabric) as part of the described adornment/clothing."),
    (235, "causes:b", "Exod 35:35 credits skilled weavers with producing the tabernacle's woven materials — the craft that produces the cloth used in dress."),
    (236, "assoc", "1 Chr 29:21/Num 15:10 list burnt offering and wine (drink-offering) as coordinate ritual components."),
    (237, "assoc", "Lev 23:10/Deut 16:9 tie first-fruits timing to a seven-week count, matching the Sabbath/Seven calendrical pattern."),
    (238, "assoc", "Josh 2:18/Lev 14:4 (scarlet cord; hyssop cleansing rite) — weak/unrelated link between colour and hyssop."),
    (239, "assoc", "Exod 29:42/25:22 show the cloud as a phenomenon associated with the tabernacle's meeting-place, not a structural part of it (distinct from the Cloud/Shechinah symbol relation)."),
    (240, "assoc", "Exod 34:27/Deut 31:9 record the covenant text within the Pentateuch's books — the covenant is an event/institution recorded there, not a literary subset of it."),
    (241, "assoc", "Deut 31:9/Mal 4:4 (Moses delivering the law; a later reference to it) — narrative connection, not hierarchy with the Pentateuch."),
    (242, "assoc", "2 Chr 33:6/Isa 19:3 list divination and idol-consultation as coordinate forbidden practices, not hierarchy."),
    (243, "narrower:a", "Lev 23:10/23:17 present the first-fruits offering as conducted via the wave-offering method — one instance of that broader ritual category."),
    (244, "assoc", "2 Sam 14:2/Ps 104:15 don't establish oil as structurally 'part of' the anointing practice in the way linen is part of a garment — associated is the honest fit for a practice-and-its-material relation."),
    (245, "assoc", "Exod 28:4/39:28 don't establish more than descriptive coloring, matching the Colour pattern."),
    (246, "narrower:a", "Deut 14:8/Isa 66:17 support boar as a specific wild type within the broader swine/pig category."),
    (247, "assoc", "Deut 18:10/2 Chr 33:6 list enchantments and familiar-spirit consultation as sibling forbidden practices, neither subsuming the other."),
    (248, "assoc", "1 Kgs 10:28/Ezek 27:7 (imported horses; a trading ship's sail) — weak/unrelated link between army and banner."),
    (249, "assoc", "1 Kgs 4:13/Num 32:41 name Havoth-jair as villages (not typically 'cities'), so associated avoids a category mismatch with the City concept."),
    (250, "assoc", "Num 32:41 names the villages after the person Jair — an eponym relation, not a city-instance relation, avoiding a category error."),
    (251, "assoc", "Deut 1:7/11:11 list plain and valley as coordinate terrain categories."),
    (252, "part_of:b", "1 Kgs 10:26/4:26 show horses as part of Solomon's military buildup, matching the Army/Chariot pattern."),
    (253, "assoc", "1 Chr 18:4/Deut 17:16 pair chariot and horse as complementary military equipment, neither part of the other."),
    (254, "assoc", "2 Chr 6:28/Joel 2:25 list caterpillar and palmer-worm as coordinate locust-plague terms, matching the Caterpillar/Mildew pattern."),
    (255, "part_of:b", "Judg 16:3/Ps 107:16 show gates as a structural component of fortified/fenced cities."),
    (256, "causes:a", "Isa 40:19/Judg 17:4 show the goldsmith's craft (casting, overlaying) as what produces the idol object, matching the Graving/Idol pattern."),
    (257, "assoc", "1 Sam 10:3/Lev 23:13 mention a flagon and wine offering in different contexts — container-content relation, matching the Cup/Wine call."),
    (258, "assoc", "2 Sam 6:5/Dan 3:7 list cornet and flute as sibling instruments, neither subsuming the other."),
    (259, "assoc", "2 Sam 6:5/Dan 3:7 list cornet and sackbut as sibling instruments."),
    (260, "assoc", "2 Sam 6:5/Dan 3:7 list cornet and psaltery as sibling instruments."),
    (261, "assoc", "2 Chr 12:15/9:29 (source-citation formulas for different kings' reigns) — weak/unrelated link between Chronicles and Nathan specifically."),
    (262, "assoc", "1 Chr 11:22/1 Kgs 1:8 (Benaiah's exploits; an official roster) — narrative proximity, not hierarchy, between Benaiah and giants."),
    (263, "assoc", "1 Kgs 15:2/2 Chr 13:2 record Maachah as Abijah's mother — genealogical, not hierarchy."),
    (264, "assoc", "2 Kgs 24:18/23:31 (regnal-formula verses about different kings) — the book narrates about Zedekiah, not a taxonomic relation."),
    (265, "assoc", "Esth 3:13/Isa 10:6 use captive and exile near-synonymously, matching the Captivity/Exile pattern."),
    (266, "assoc", "2 Kgs 25:9/Ps 79:1 describe the temple's destruction during the exile — historical co-occurrence, matching the Exile/Temple,Solomon's pattern."),
    (267, "assoc", "Neh 12:39/Zeph 1:10 mention a fish gate near fenced-city gates — incidental textual proximity, not a real conceptual relation."),
    (268, "assoc", "Dan 11:7/Isa 11:1 use 'branch' as a prophetic messianic image — a symbol within prophecy this vocabulary has no clean verb for; associated is the honest fallback."),
    (269, "causes:a", "Gen 1:1's own wording ('God created the heavens and the earth') directly ties the act of creation to heaven's origin."),
    (270, "assoc", "Gen 1:7/Ps 148:4 closely identify firmament and heaven in the cited text rather than establishing a clean one-subsumes-the-other hierarchy."),
    (271, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (272, "assoc", "Amos 5:8/Job 9:9 name Orion as a constellation God made — a category mismatch with 'astronomy' the field of study, so associated avoids a false hierarchy."),
    (273, "narrower:b", "2 Kgs 17:16/Deut 4:19 name stars as members of the 'host of heaven' category, matching the Moon/Sun pattern."),
    (274, "narrower:b", "1 Sam 18:6/Judg 11:34 name timbrel among Easton's catalog of specific instruments."),
    (275, "narrower:b", "Deut 2:10/Gen 14:5 name the Zamzummim as a specific giant people-group, matching the Emims/Giants pattern below."),
    (276, "assoc", "1 Kgs 22:48/2 Chr 9:21 use 'ships of Tarshish' as a trade-route designation, not a taxonomic ship-category relation."),
    (277, "assoc", "1 Chr 1:17/Ezek 27:10 list Lud and Put as coordinate peoples in genealogical/ethnographic lists."),
    (278, "assoc", "Ezek 38:5/30:5 list Cush and Lud as coordinate peoples."),
    (279, "narrower:a", "Gen 13:10/1 Kgs 7:46 place Gomorrah specifically within the plain of the Jordan, matching the established Edom/Teman and Edom/Bozrah geographic-containment pattern."),
    (280, "assoc", "Judg 1:10/Josh 14:15 place Ahiman (a giant) in Hebron — person-in-place, not place-within-place."),
    (281, "assoc", "2 Sam 2:1/Num 13:22 place Sheshai (a giant) in Hebron — person-in-place."),
    (282, "assoc", "Josh 14:15 states Hebron 'used to be called Kiriath-arba' — an alternate/earlier name, matching the Edom/Seir naming-equivalence pattern."),
    (283, "narrower:b", "Deut 2:10/Gen 14:5 name the Emim as a specific giant people-group within the broader Giants category."),
    (284, "assoc", "1 Kgs 5:12/Gen 21:32 use alliance and covenant near-synonymously, matching the Banner/Ensign pattern."),
    (285, "assoc", "Dan 4:13/4:10 show an angel appearing within a dream vision — co-occurring narrative elements, not hierarchy."),
    (286, "assoc", "1 Chr 2:9/2:42 mention Caleb and Hebron in genealogical lists without establishing a place-within-place relation to another region here."),
    (287, "assoc", "1 Kgs 11:43/2 Kgs 21:26 describe kings buried in garden-tombs — a location-of-burial relation, not composition or hierarchy."),
    (288, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (289, "assoc", "1 Chr 21:16/2 Kgs 6:17 show an angel and a fiery chariot in different theophany narratives — co-occurring imagery, not hierarchy."),
    (290, "assoc", "Isa 47:2/Judg 16:21 (veil removal; Samson's blinding) — weak/unrelated evidence for a dress-eye relation."),
    (291, "assoc", "Gen 42:38/37:35 use Sheol/the grave and the language later associated with Hell near-synonymously in these patriarchal narratives — near-synonyms, not hierarchy."),
    (292, "assoc", "Exod 26:14/Ezek 16:10 (tabernacle skin-covering; unrelated garment description) — weak specific link between badger skins and dress generally."),
    (293, "assoc", "Esth 8:15/Gen 41:42 list linen and (implicitly) fine fabrics as coordinate luxury materials, not hierarchy."),
    (294, "assoc", "Ezek 16:10/16:13 (embroidered clothing description) — weak specific link between head-dress and silk."),
    (295, "assoc", "1 Sam 14:25/Exod 3:8 pair honey and milk as coordinate items in 'land flowing with milk and honey' imagery."),
    (296, "assoc", "2 Chr 33:6/Lev 19:31 list familiar-spirit consultation and magic as sibling forbidden practices — kept associated for consistency with the Divination/Magic uncertainty."),
    (297, "assoc", "1 Chr 2:5/Gen 46:12 place Caleb within Judah's genealogy — tribal membership, kept associated matching the Anah/Horites pattern."),
    (298, "causes:b", "Jer 48:33/Hag 2:16 tie the wine-press's operation to wine's production — pressing produces the wine, matching the Weaving-produces-Linen pattern."),
    (299, "assoc", "1 Sam 26:6/Gen 15:20 list Hittites and Perizzites as coordinate Canaanite peoples."),
]


def main():
    judgments = []
    for idx, code, just in DECISIONS:
        p = BATCH[idx]
        a_id, b_id = p["a"]["id"], p["b"]["id"]
        entry = {"pair": [a_id, b_id], "justification": just}
        if code == "assoc":
            entry["verb"] = "associated"
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
        "model": "claude-in-session (Sonnet 5) — chunk 2 of the weight>=10 batch (indices 150-299)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-w10-chunk2.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments to {out_path}")


if __name__ == "__main__":
    main()
