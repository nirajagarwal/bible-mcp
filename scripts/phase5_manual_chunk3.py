"""Chunk 3 of the weight>=10 batch (indices 300-449). Same mechanism as chunk1/2."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-w10.json")))

DECISIONS = [
    (300, "assoc", "2 Chr 30:5/Lev 23:4 show the congregation gathering for Passover — co-occurrence, not hierarchy."),
    (301, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule, despite Passover plausibly being a specific sacrifice type."),
    (302, "assoc", "Deut 14:29/16:11 include both citizen-Levite and foreigner as coordinate beneficiaries of festival law, not framed as opposites in the cited text."),
    (303, "assoc", "1 Sam 10:5/1 Chr 13:8 (a Philistine garrison; unrelated musical procession) — weak/unrelated link."),
    (304, "assoc", "Hag 1:1/Ezra 3:2 (altar-building per the law) — narrative proximity, not hierarchy with the Pentateuch."),
    (305, "assoc", "Exod 22:29/23:16 tie first-fruits to the harvest feast calendrically; Tabernacles is a separate autumn feast, not a subtype."),
    (306, "assoc", "Exod 25:4 names blue among the tabernacle's yarn colors — a descriptive dye-color, matching the Colour/Linen pattern rather than a physical material component."),
    (307, "part_of:a", "Exod 26:1 specifies cherubim worked into the tabernacle's curtains, matching the Cherub/Tabernacle pattern."),
    (308, "assoc", "1 Sam 2:28/Exod 28:4 name the mantle among priestly garments without establishing it as structurally part of the high priest (a person)."),
    (309, "assoc", "Descriptive property of the ephod's coloring, matching the Colour pattern."),
    (310, "assoc", "Exod 29:40/Num 15:7 list the tenth-deal flour measure and wine as coordinate offering components."),
    (311, "narrower:a", "Exod 32:20/Deut 7:25 treat the golden calf as a specific, famous instance of the general idol category."),
    (312, "assoc", "1 Kgs 2:27/Josh 18:1 (Abiathar's banishment; a congregation assembly) — weak/unrelated link between Eleazar and the tabernacle in the cited text."),
    (313, "assoc", "Deut 21:12/Lev 14:9 (captive-woman mourning rites; purification after skin disease) — an indirect/weak link, correct fallback."),
    (314, "assoc", "2 Chr 31:15/31:13 co-list Jeshua and Shimei among Levitical officials."),
    (315, "part_of:a", "Deut 33:17 describes the unicorn's horns anatomically — a body-part relation, unlike the adjacent-organs cases (Fat/Liver) kept associated."),
    (316, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (317, "assoc", "2 Chr 34:14/Ezra 7:10 show scribes studying/handling the law — a role relation, not hierarchy with the Pentateuch."),
    (318, "assoc", "1 Sam 19:13/Judg 18:17 mention both as ancient cultic objects in unrelated narratives, matching the Teraphim/Thummim pattern."),
    (319, "assoc", "1 Sam 6:2/Dan 5:7 show a soothsayer as a practitioner-role, matching the person-to-practice fallback used for Wizard/Astrologer."),
    (320, "assoc", "1 Sam 16:20/Gen 43:11 pair bottle and wine as container-content, matching the Cup/Wine pattern."),
    (321, "assoc", "1 Chr 3:1/1 Sam 27:3 list Abigail and Ahinoam as David's co-wives — genealogical, not hierarchy."),
    (322, "assoc", "1 Kgs 2:25/2 Sam 8:18 co-list Cherethite officials including Ira."),
    (323, "assoc", "1 Chr 11:22/2 Sam 20:23 record Jehoiada as Benaiah's father — genealogical, not hierarchy."),
    (324, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (325, "assoc", "Isa 22:12/Amos 8:10 tie baldness to mourning practice; kept associated rather than stretching to a contrasts or causes claim the cited text doesn't clearly support."),
    (326, "assoc", "1 Chr 3:10/1 Kgs 15:8 (genealogy; burial notice) — narrative co-occurrence, not hierarchy."),
    (327, "assoc", "Ps 18:14/144:6 use arrows and lightning as parallel poetic images of divine judgment, not hierarchy or causation."),
    (328, "part_of:a", "Ezek 41:23/2 Chr 4:22 describe doors/gates as part of the temple's sanctuary structure."),
    (329, "assoc", "1 Chr 5:26/2 Kgs 15:19 (Assyrian tribute/deportation) — weak specific link to Isaiah in the cited text."),
    (330, "assoc", "Same evidence as Captivity/Isaiah — weak specific link, correct fallback."),
    (331, "assoc", "Jer 41:2/40:7 (Ishmael's plot; captains after the fall of Jerusalem) — narrative co-occurrence, the book narrates the fast, not a hierarchy."),
    (332, "assoc", "Jer 39:10/52:16 describe those left behind after Zedekiah's captivity — historical co-occurrence, not hierarchy."),
    (333, "assoc", "1 Chr 9:11/Neh 11:11 co-list Azariah and Meshullam in a priestly genealogy."),
    (334, "assoc", "Amos 2:9/Exod 3:8 (Amorite height vs. cedars; the Exodus promise) — weak/unrelated evidence."),
    (335, "assoc", "Isa 9:6/7:14 present messianic prophecy — a relation this vocabulary has no verb for; associated is the honest fallback, matching the Christ/Prophecy call."),
    (336, "assoc", "Ezek 27:6 names oaks from Bashan (not cedar) alongside an unrelated cedar-of-Lebanon oracle — mismatched evidence, correct fallback."),
    (337, "assoc", "Isa 11:8/59:5 pair adder and cockatrice as coordinate venomous-serpent terms, neither subsuming the other."),
    (338, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (339, "assoc", "Ps 19:1/115:16 don't make heaven a subtype of the field of astronomy — category mismatch, associated is the honest fit."),
    (340, "assoc", "Gen 1:14/Deut 4:19 — same category-mismatch reasoning as Astronomy/Moon."),
    (341, "assoc", "2 Kgs 17:16/Deut 4:19 list stars and sun as coordinate objects of forbidden astral worship."),
    (342, "assoc", "Amos 5:8/Job 9:9 name Pleiades as a constellation — category mismatch with the field of astronomy, matching the Astronomy/Orion call."),
    (343, "assoc", "Isa 41:14/Job 25:6 use 'man' and 'son of man' as synonymous poetic parallelism (Hebrew poetic doubling), not a hierarchy."),
    (344, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (345, "assoc", "Gen 2:13/Isa 11:11 (the Gihon river's naming; an unrelated coastland prophecy) — weak/unrelated evidence."),
    (346, "assoc", "1 Sam 19:24/Mic 1:8 show nakedness as a state reached by removing dress in mourning/prophetic-sign contexts — kept associated rather than asserting a contrasts or causal claim the text doesn't clearly frame."),
    (347, "assoc", "Dan 9:25/Isa 9:6 present messianic prophecy, matching the Christ/Prophecy fallback."),
    (348, "narrower:b", "1 Chr 25:1/1 Sam 10:5 name the pipe as one instrument within the broader practice of music, matching the Harp/Music pattern."),
    (349, "assoc", "Gen 12:7/8:20 show sacrifice performed at the altar — instrument-for-practice, matching the Altar/Burnt-offering call."),
    (350, "assoc", "2 Kgs 23:12/23:4 show altars and (Asherah) groves torn down together in cultic reform — coordinate objects, not hierarchy."),
    (351, "assoc", "2 Kgs 16:4/Deut 12:2 show altars built at high places — co-occurring cultic elements, matching the Idol/High-place call rather than a structural part-of."),
    (352, "assoc", "Gen 10:31/10:5 (genealogical dispersion; coastland peoples) — a loose thematic link, correct fallback."),
    (353, "assoc", "1 Chr 1:17/Ezek 27:10 co-list Lud and Put/Pul as coordinate names in genealogical/ethnographic lists."),
    (354, "assoc", "Gen 10:19/14:2 list Gomorrah and Zeboim as coordinate cities of the plain, siblings rather than one subsuming the other."),
    (355, "contrasts", "Gen 16:2 (Sarai's barrenness as a divine restraint) and Ps 127:3 (children as a heritage/blessing) frame barrenness and having a child as the two poles of a real theological reproach/blessing opposition — the clearest genuine antonym pair in this batch."),
    (356, "assoc", "Deut 11:30/Gen 12:6 (Shechem's mountains; Abram's journey) — weak/unrelated link between grove and plain in the cited text."),
    (357, "narrower:b", "Gen 12:6 places Shechem within the plain region Deut 11:30 describes, matching the established Gomorrah/Plain geographic-containment pattern."),
    (358, "assoc", "Deut 11:30/Gen 12:6 mention Gilgal and Shechem as separate locations in the same general passage — not a containment relation between them."),
    (359, "narrower:b", "Job 1:3/1 Sam 25:2 list oxen among cattle possessions — ox is a specific type of cattle."),
    (360, "assoc", "Deut 2:10/Gen 14:5 place giants at Kirjathaim — person-group-in-place, matching the Giants/Hebron pattern."),
    (361, "assoc", "Dan 12:1/Isa 9:7 (Michael's apocalyptic role; messianic increase) — co-occurrence in eschatological material, not hierarchy."),
    (362, "assoc", "Deut 32:14/Job 20:17 use milk and rivers as parallel poetic images of abundance, not hierarchy."),
    (363, "assoc", "Exod 23:20/14:19 show an angel and the pillar of fire as parallel guiding-presence images in the Exodus narrative — coordinate, matching the Cloud/Fire sibling treatment."),
    (364, "narrower:b", "2 Kgs 4:42/Deut 32:14 list milk among food items — milk is a specific type of food."),
    (365, "assoc", "Deut 32:13/Ps 81:16 list milk and wheat as coordinate abundance items."),
    (366, "assoc", "1 Sam 25:2/Gen 38:13 (a sheep business; an unrelated Tamar narrative) — weak/unrelated evidence."),
    (367, "assoc", "Num 13:22/Gen 23:2 (Hebron's giants; Sarah's death at Kiriath Arba) — weak link, not a city-giants hierarchy."),
    (368, "assoc", "2 Sam 3:35/1:12 place a funeral meal and mourning practice in adjacent narratives — closely intertwined companion practices, not one causing the other."),
    (369, "assoc", "Gen 50:13/23:20 describe cave-tombs and garden-tombs as separate burial-place types, not hierarchy."),
    (370, "assoc", "Exod 2:16/1 Sam 9:11 (Midian's flock-tending daughters; unrelated city elders) — weak/unrelated evidence."),
    (371, "assoc", "Deut 11:11/Gen 27:28 (the land's description; Isaac's blessing) — weak/unrelated link between valley and wine."),
    (372, "assoc", "Josh 24:26/Exod 24:4 show the law recorded and covenant renewed at Shechem — a location-of-recording relation, not hierarchy."),
    (373, "narrower:b", "1 Kgs 21:27/2 Sam 3:31 show sackcloth as a specific mourning garment within dress generally."),
    (374, "assoc", "1 Kgs 21:27/2 Sam 3:31 show fasting and sackcloth as parallel companion expressions of grief, neither causing the other."),
    (375, "narrower:a", "Gen 40:3 places Joseph 'in custody' — Easton's Dungeon entry describes a specific, harsher subtype of the general prison/custody category."),
    (376, "assoc", "Esth 8:15/Gen 41:42 mention fine fabrics descriptively, matching the Colour pattern rather than a material composition claim specific to silk."),
    (377, "assoc", "Deut 32:13/Ps 81:16 list honey and wheat as coordinate abundance items."),
    (378, "assoc", "2 Sam 6:19/1 Chr 16:3 pair entertaining/distributing food and wine as co-occurring practices."),
    (379, "causes:b", "1 Chr 5:1/Deut 21:17 tie the birthright privilege directly to firstborn status — being firstborn is what grants the birthright."),
    (380, "assoc", "2 Kgs 2:24/1 Kgs 13:24 place lions in forest/road settings — habitat co-occurrence, not hierarchy."),
    (381, "assoc", "1 Kgs 10:11/2 Chr 8:18 show merchants using ships for trade — person-instrument relation, not hierarchy."),
    (382, "assoc", "1 Sam 18:6/Exod 15:20 show Miriam leading a dance — person-practice relation, not hierarchy."),
    (383, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (384, "assoc", "Exod 6:16/Num 26:57 list Kohathites and Merarites as coordinate Levitical clans, siblings."),
    (385, "assoc", "1 Sam 2:35/1 Kgs 2:35 (a prophecy of a faithful priest; its fulfillment in Zadok) — narrative connection, not a direct Eleazar-Zadok hierarchy from the cited text."),
    (386, "narrower:a", "Isa 33:4/Joel 2:9 use caterpillar within the same locust-plague semantic field Joel's fourfold terminology describes, treated as a specific term within the broader locust category."),
    (387, "assoc", "Exod 13:4/23:15 tie Passover to the month of Abib calendrically, not taxonomically."),
    (388, "assoc", "1 Sam 18:6/Exod 15:20 (women dancing) — narrative co-occurrence, not hierarchy."),
    (389, "narrower:b", "Exod 17:14/34:27 show Moses writing on a scroll — the Pentateuch is a specific instance of 'the book/writing' referenced."),
    (390, "narrower:b", "Exod 20:8/23:12 tie the Sabbath principle to the sabbatical-year law — the sabbatical year is a specific instance of the broader festival/appointed-time calendar."),
    (391, "assoc", "Deut 14:29/16:11 list poor and proselyte as coordinate beneficiaries of festival law."),
    (392, "assoc", "Lev 19:31/Exod 22:18 pair familiar-spirit consultation and witchcraft as near-synonymous forbidden practices."),
    (393, "assoc", "Deut 18:10/Exod 22:18 show a witch/sorceress as a practitioner of divination-adjacent practice, matching the person-to-practice fallback."),
    (394, "assoc", "Exod 22:25/Jer 15:10 tie usury law to lending to the poor — co-occurrence in law."),
    (395, "assoc", "Deut 14:21/Lev 22:8 (unclean-food law) don't actually cite Ezekiel's own text — no direct evidence for this specific book-concept pairing."),
    (396, "assoc", "Deut 12:12/16:14 (festival rejoicing law) don't specifically address begging — weak/unrelated evidence."),
    (397, "assoc", "Deut 16:9/Exod 23:16 list Pentecost and Tabernacles as coordinate pilgrimage feasts, siblings not hierarchy."),
    (398, "assoc", "Lev 23:6/Deut 16:8 place a solemn assembly within the festival calendar near first-fruits offerings — co-occurrence, matching the Convocation/First-fruits pattern."),
    (399, "assoc", "Deut 12:2/Exod 23:24 show idols destroyed at high places, matching the High place/Idol call."),
    (400, "part_of:a", "1 Kgs 9:28/1 Chr 29:4 name gold (from Ophir) as material used for Solomon's temple."),
    (401, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (402, "assoc", "Exod 26:1/26:31 name blue as a curtain dye-color, matching the Colour pattern rather than a physical material claim."),
    (403, "assoc", "1 Sam 2:18/Exod 28:4 co-list ephod and girdle as sibling priestly-garment items, not one part of the other from the cited text."),
    (404, "assoc", "2 Kgs 1:8/Zech 13:4 co-list girdle and mantle as distinct garment types, siblings."),
    (405, "part_of:a", "Exod 28:39 (implied by the priestly-garment list Exod 28:4 cites) has the mitre/turban woven of fine linen, matching the established linen-composition pattern."),
    (406, "assoc", "Exod 28:40/28:4 use bonnet and mitre as Easton's distinct terms for related but different priestly headwear (common priest vs. high priest), kept associated rather than asserting hierarchy."),
    (407, "narrower:b", "Exod 28:40/28:4 support the mitre as a specific type of head-dress, matching the Bonnet/Head-dress pattern."),
    (408, "narrower:b", "Exod 28:15/28:6 name scarlet as a specific instance of colour, matching the Black/Colour and Blue/Colour pattern."),
    (409, "assoc", "Ezek 21:21/Judg 17:5 (Babylon's divination methods; Micah's shrine) — weak/mixed evidence, not a clean divination-Thummim hierarchy."),
    (410, "assoc", "Exod 39:28/Ezek 44:18 co-list bonnet and breeches as distinct priestly-garment items, siblings."),
    (411, "part_of:b", "Exod 28:42 explicitly commands linen undergarments (breeches), matching the established linen-composition pattern."),
    (412, "assoc", "Exod 29:13/Lev 9:19 don't establish a sheep-specific caul hierarchy beyond general sacrificial-fat context, matching Fat/Sheep."),
    (413, "assoc", "Lev 16:12/10:1 (censer coals; Nadab and Abihu's incident) — weak/unrelated evidence for an altar-wine relation."),
    (414, "part_of:a", "1 Chr 18:8/22:14 place the laver's bronze material within Solomon's temple-building provisions."),
    (415, "assoc", "Exod 30:23/Prov 7:17 list calamus and myrrh as coordinate spice ingredients, siblings."),
    (416, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule, despite goldsmiths plausibly performing graving."),
    (417, "assoc", "Ezek 24:17/2 Sam 15:30 (turban removal in mourning; David's mourning journey) — weak/tangential link, correct fallback rather than asserting bonnet is a type of dress from this specific evidence."),
    (418, "narrower:b", "Deut 24:19/Lev 23:22 describe leaving field corners unharvested as a specific gleaning practice within agriculture, matching the Glean/Agriculture pattern."),
    (419, "assoc", "Lev 23:5/Josh 5:10 (Passover timing; its observance) — narrative co-occurrence, the Pentateuch records first-fruits law, not a hierarchy."),
    (420, "assoc", "1 Kgs 8:3/Num 4:15 show Eleazar's priestly duties toward the ark — a role relation, not hierarchy."),
    (421, "assoc", "1 Chr 2:55/Judg 4:11 connect Jehonadab's family to the Kenites — genealogical/ethnic relation, matching the Anah/Horites pattern."),
    (422, "assoc", "1 Kgs 8:3/Deut 31:9 (the ark's transport; Moses writing the law) — weak/unrelated specific link."),
    (423, "narrower:b", "Deut 3:17 places Ashdoth-pisgah within the Arabah/plain region Gen 13:10 also describes, matching the geographic-containment pattern."),
    (424, "narrower:b", "1 Sam 19:13/Hos 3:4 show teraphim as a specific household-idol type within the general idol category."),
    (425, "assoc", "2 Sam 14:2/Ruth 3:3 pair anointing and hair-care as coordinate self-care/beautification practices, not hierarchy."),
    (426, "narrower:a", "Deut 32:33 names the asp as a specific venomous creature, matching the Gall/Poison and Hemlock/Poison specific-source pattern."),
    (427, "narrower:a", "Isa 11:8 names the adder as a specific venomous creature, matching the same pattern."),
    (428, "assoc", "Josh 15:15/10:38 (Debir's conquest) don't establish a Debir-writing relation beyond the traditional etymology — no textual evidence for the connection in the cited verses."),
    (429, "narrower:a", "1 Kgs 2:25/2 Sam 8:18 name the Cherethites as a specific coastal people-group closely identified with the broader Philistines in the tradition these verses reflect."),
    (430, "assoc", "Esth 6:11/8:15 describe royal apparel's coloring, matching the Colour pattern."),
    (431, "assoc", "1 Kgs 13:24/Prov 26:13 (a lion encountered on a road; a proverb about excuse-making) — weak/loose link to 'hunting' specifically."),
    (432, "assoc", "1 Chr 29:29/1 Sam 9:9 show the Chronicles citing seer-records as a source — a book-genre relation, not hierarchy."),
    (433, "assoc", "1 Chr 14:1/1 Kgs 5:6 show carpenters working with cedar — a practitioner-material relation, not a composition of the carpenter concept itself."),
    (434, "assoc", "1 Kgs 5:8/2 Sam 6:5 list cedar and fir as coordinate construction-wood types, siblings."),
    (435, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule, despite flute plausibly being a specific instrument."),
    (436, "narrower:b", "1 Kgs 1:40/Dan 3:5 name the sackbut among Easton's catalog of specific instruments."),
    (437, "assoc", "Dan 3:5/3:7 show worship triggered by instrument sounds including the cornet — co-occurrence, not hierarchy."),
    (438, "assoc", "1 Chr 18:17/2 Sam 20:23 co-list Ira among Cherethite/Pelethite officials."),
    (439, "assoc", "2 Sam 8:18/1 Kgs 1:44 connect Jehoiada (Benaiah's father) to the Pelethite-commanding context indirectly — genealogical/administrative proximity, not hierarchy."),
    (440, "assoc", "Ezra 7:28/Neh 1:11 use 'God's hand' and prayer idiomatically together, matching the Face/Prayer pattern."),
    (441, "assoc", "1 Chr 11:22/1 Kgs 1:8 co-list Benaiah and Shimei among David's officials."),
    (442, "assoc", "1 Chr 9:11/Neh 11:11 (a priestly genealogy; an unrelated captain reference) — weak/unrelated evidence."),
    (443, "part_of:a", "1 Chr 28:11/1 Kgs 6:3 place the parlour/porch chamber within Solomon's temple's plan."),
    (444, "causes:a", "Dan 9:2/Zech 7:5 tie captivity-period fasting directly to the exile, matching the Exile/Fast causal pattern."),
    (445, "assoc", "2 Kgs 18:17/2 Chr 32:9 connect Hezekiah's engineering works to the Gihon spring — a person-project relation, not hierarchy."),
    (446, "assoc", "Ezek 29:6/2 Kgs 18:21 use cane and reed near-synonymously as a fragile-support image."),
    (447, "assoc", "2 Kgs 19:28/Amos 4:2 use bridle and hook as parallel images of forced restraint/captivity, not hierarchy."),
    (448, "assoc", "2 Chr 36:1/1 Chr 3:15 record Shallum as Jehoahaz's alternate throne-name, matching the Edom/Seir naming-equivalence pattern."),
    (449, "assoc", "Neh 10:3/12:13 co-list Amariah and Meshullam in a priestly genealogy."),
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
        "model": "claude-in-session (Sonnet 5) — chunk 3 of the weight>=10 batch (indices 300-449)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-w10-chunk3.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments to {out_path}")


if __name__ == "__main__":
    main()
