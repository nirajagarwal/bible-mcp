"""Builds outputs/phase5-judgments-<date>-w10-chunk1.json from a hand-reviewed
verb decision per pair (chunk 1 of the weight>=10 batch, indices 0-149), looking
up real concept ids from the batch file rather than re-deriving slugs by hand."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = json.load(open(os.path.join(ROOT, "outputs", "phase5-batch-2026-09-26-w10.json")))

# (index, code, justification). code: 'assoc' | 'narrower:a'/'narrower:b' (a/b = narrower
# side) | 'causes:a'/'causes:b' (a/b = cause side) | 'part_of:a'/'part_of:b' (a/b = part side)
DECISIONS = [
    (0, "part_of:a", "Cherubim were embroidered into the tabernacle's curtains and mounted on the mercy-seat — a decorative/structural element of the tabernacle, not a separate category."),
    (1, "narrower:a", "Harp is one specific instrument Easton's Music,Instrumental entry catalogs alongside psaltery and lyre."),
    (2, "assoc", "Judg 2:1/Gen 12:7 don't establish a hierarchy between angel and captain in the cited evidence."),
    (3, "assoc", "Exod 29:13/29:22 describe fat covering the liver — adjacent anatomical parts, matching the earlier Fat/Liver call."),
    (4, "assoc", "Isa 24:20/29:9 pair strong drink and wine as coordinate intoxicants, not one subsuming the other."),
    (5, "assoc", "1 Chr 6:8/2 Sam 8:17 record Ahitub as Zadok's father — genealogical, not conceptual hierarchy."),
    (6, "assoc", "Isa 20:6/Jer 47:4 don't establish more than co-occurrence in judgment oracles."),
    (7, "causes:b", "Num 35:19 institutes the avenger of blood specifically as the response to a murder — the crime is what activates the role."),
    (8, "assoc", "Deut 16:11/16:14 list foreigner and poor as coordinate categories owed festival generosity."),
    (9, "part_of:a", "Exod 26:14 names badger (dugong) skins as one of the tabernacle's covering materials."),
    (10, "part_of:b", "Exod 25:22/30:6 place the mercy-seat as the cover of the ark specifically — a component, not a coordinate object."),
    (11, "part_of:a", "Exod 25:31/Zech 4:2 describe bowls as part of the lampstand's construction."),
    (12, "assoc", "Blue is a descriptive dye-color of tabernacle curtains, not a physical material component like linen or skins."),
    (13, "assoc", "Descriptive-property relation, matching the earlier Colour/Dress pattern."),
    (14, "assoc", "Weak evidence (1 Chr 21:29 doesn't discuss dress) — correct fallback."),
    (15, "part_of:a", "Exod 26:31 specifies the veil is made of 'finely spun linen' — an explicit material component."),
    (16, "assoc", "1 Kings 6:20/6:22 mention censers and the altar in the same temple-furnishing description, not a part-of relation."),
    (17, "assoc", "Descriptive property of the priestly mitre, matching the Colour pattern."),
    (18, "assoc", "1 Sam 19:13/Judg 18:17 mention both as ancient cultic objects in unrelated narratives — coordinate, not hierarchical."),
    (19, "assoc", "Deut 14:29/16:11 list poor and widows as coordinate categories owed charity."),
    (20, "assoc", "1 Sam 28:8/Isa 8:19 show a wizard as a practitioner using a familiar spirit — person-to-practice, matching the earlier Divination/Wizard call."),
    (21, "assoc", "Lev 23:36/Deut 16:8 use convocation and solemn meeting as near-synonymous festival terms."),
    (22, "narrower:a", "Deut 29:18 names gall among substances producing bitter poison — a specific poisonous plant."),
    (23, "narrower:a", "Amos 6:12 names hemlock similarly as a specific bitter/poisonous plant."),
    (24, "narrower:b", "Jerusalem is one specific instance of a fortified/fenced city, per 2 Sam 5:6's siege narrative."),
    (25, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
    (26, "assoc", "Deut 17:3/4:19 list sun and moon together as coordinate objects of forbidden astral worship."),
    (27, "narrower:b", "Deut 4:19/2 Kgs 17:16 name moon and stars as members of the 'host of heaven' category."),
    (28, "assoc", "Weak evidence link (Exod 26:1/26:31 concern the veil's own construction, not dress generally)."),
    (29, "narrower:b", "1 Chr 13:8/1 Sam 10:5 list pipe among other named instruments in Easton's instrumental-music catalog."),
    (30, "assoc", "Gen 12:7/8:20 don't establish more than co-occurrence of altar and fire in sacrifice narratives."),
    (31, "assoc", "Coordinate livestock categories, no hierarchy in the cited evidence."),
    (32, "assoc", "2 Chr 33:6/Lev 19:31 don't clearly subordinate magic to divination or vice versa in the cited text."),
    (33, "assoc", "Exod 3:8/3:17 (the Exodus deliverance promise) don't establish a prophecy-wine relation."),
    (34, "assoc", "Coordinate vulnerable-persons categories in festival law."),
    (35, "assoc", "1 Kgs 2:3/Mal 4:4 use 'law of Moses' as effectively synonymous with the Pentateuch's content, not a hierarchy."),
    (36, "part_of:a", "1 Kgs 8:6/2 Sam 6:17 show the ark being brought into and housed within the tabernacle — a furnishing, not a coordinate structure."),
    (37, "assoc", "1 Sam 23:9/23:6 (Abiathar's ephod) don't establish a high-priest/teraphim relation."),
    (38, "assoc", "Havoth-jair is named after the person Jair (1 Chr 2:22) — an eponym relation, not conceptual hierarchy."),
    (39, "assoc", "Dan 9:25/Isa 9:6 don't establish a governor-prophecy hierarchy in the cited text."),
    (40, "assoc", "1 Kgs 2:25/2 Sam 8:18 list Cherethites and Pelethites as a paired royal guard unit, matching earlier Benaiah pairings."),
    (41, "assoc", "Jer 41:1/36:12 place fasting and Zedekiah's reign in the same historical period without a direct causal or hierarchical link in the cited text."),
    (42, "assoc", "Hag 1:1/Ezra 2:2 co-list names in a post-exilic leadership roster."),
    (43, "assoc", "Deut 2:10/Num 13:22 place giants (Anakim) in Hebron geographically — not a taxonomic relation."),
    (44, "assoc", "Near-synonymous administrative titles in the cited passages."),
    (45, "assoc", "Deut 23:19/Exod 22:25 legislate lending to the poor — co-occurrence in law, not hierarchy."),
    (46, "assoc", "Exod 23:16/34:22 tie first-fruits to the Feast of Weeks calendrically, not taxonomically."),
    (47, "part_of:a", "Exod 26:1 specifies the tabernacle's ten curtains as its covering — a structural component."),
    (48, "part_of:a", "Exod 25:31/1 Kgs 7:49 describe bowls as part of the candlestick/lampstand's construction."),
    (49, "part_of:b", "Lev 16:12 uses a censer/firepan to carry coals from the altar — one of the altar's named utensils."),
    (50, "assoc", "Ezek 44:18/Exod 39:28 describe headdress coloring descriptively, matching the Colour pattern."),
    (51, "assoc", "Ezek 18:8/Jer 15:10 treat usury as interest practice, not a taxonomic subtype of debt, matching the earlier Loan/Usury call."),
    (52, "assoc", "Deut 3:10/Num 21:33 mention Amorite cities without establishing 'city' as a category Amorites belong to."),
    (53, "narrower:a", "Deuteronomy is explicitly one of the five books comprising the Pentateuch."),
    (54, "narrower:a", "1 Chr 13:8/1 Sam 10:5 list cymbals as one instrument within the broader practice of music."),
    (55, "narrower:a", "Amos 4:2/Isa 37:29 use fish-hooks as a specific application of hooks generally."),
    (56, "assoc", "Hag 1:1/Neh 7:7 co-list names in a post-exilic leadership roster."),
    (57, "assoc", "Ezek 16:32/Jer 3:1 use harlot and adultery as overlapping terms in the prophetic marriage-metaphor, matching the earlier Fornication/Harlot call."),
    (58, "causes:b", "Gen 4:10/9:5 tie bloodguilt directly to the act of murder — the killing is what causes the blood to 'cry out.'"),
    (59, "narrower:b", "Lev 1:14 names the turtledove as a specific sacrificial bird within the broader dove category Gen 15:9 also uses."),
    (60, "assoc", "Gen 14:7/Num 20:1 treat Kadesh and Meribah as adjacent/overlapping place references, not hierarchy."),
    (61, "assoc", "1 Sam 1:4/Deut 16:11 use entertaining and feasting near-synonymously."),
    (62, "assoc", "1 Sam 25:36/2 Sam 13:23 use banquet and entertain near-synonymously."),
    (63, "assoc", "Exod 24:4/Gen 28:18 describe unrelated stone-setting events at different locations — weak link, correct fallback."),
    (64, "narrower:a", "Amos 1:12/Isa 34:6 name Bozrah as a specific city within Edom under the same judgment oracle."),
    (65, "causes:a", "2 Sam 13:19/Esth 4:1 both show sackcloth donned as an expression of mourning, matching the established Mourn/Fast causal pattern."),
    (66, "assoc", "1 Sam 25:36/Nah 1:10 pair banquet and wine as co-occurring, not hierarchical."),
    (67, "assoc", "2 Kgs 17:25/Jer 5:6 list lions and wolves as coordinate predators in judgment imagery."),
    (68, "assoc", "Exod 40:34/Isa 6:4 (day/night counterparts of the same theophany) — coordinate, not one symbolizing the other."),
    (69, "assoc", "Dan 2:2/Isa 8:19 show an astrologer as a practitioner of divination, matching the person-to-practice pattern."),
    (70, "assoc", "Deut 16:9/Exod 34:22 tie Pentecost to the count of weeks calendrically, not taxonomically."),
    (71, "part_of:a", "Esth 1:6/Exod 26:1 name linen among the tabernacle's construction materials."),
    (72, "part_of:a", "1 Chr 28:11/1 Kgs 6:3 place the mercy-seat's plans within Solomon's temple construction."),
    (73, "assoc", "1 Sam 2:18/2:28 don't establish the ephod as structurally part of the high priest (a person), so associated is the honest fit."),
    (74, "assoc", "Descriptive property of the ephod's coloring, matching the Colour pattern."),
    (75, "part_of:b", "Exod 39:28/Ezek 44:18 explicitly name linen as the bonnet's (turban's) material."),
    (76, "assoc", "Exod 29:13/Lev 9:19 discuss sacrificial fat generally, not specifically a sheep-fat hierarchy."),
    (77, "assoc", "Weak/unclear evidence for a food-liver hierarchy in the cited text."),
    (78, "assoc", "1 Chr 29:21/Num 15:10 list lamb and wine as co-occurring offering components."),
    (79, "assoc", "Deut 12:3/1 Kgs 15:13 show idols destroyed at high places — co-occurring cultic elements, not one subsuming the other."),
    (80, "assoc", "Deut 24:19/14:29 tie agricultural gleaning law to provision for the poor — co-occurrence in law."),
    (81, "narrower:b", "Ezra 3:10/1 Chr 15:24 name trumpets among Easton's catalog of instruments."),
    (82, "assoc", "1 Kgs 10:26/4:26 use army and host near-synonymously."),
    (83, "assoc", "1 Kgs 8:3/Josh 6:6 show music/trumpets accompanying the ark's processions — co-occurring ceremonial elements."),
    (84, "assoc", "1 Kgs 4:13/Deut 3:4 mention Bashan's cities without establishing 'city' as a category Bashan belongs to."),
    (85, "assoc", "Jer 51:14/51:27 pair cankerworm and caterpillar as coordinate locust-plague terms."),
    (86, "assoc", "1 Chr 15:28/13:8 list cornet and cymbals as sibling instruments, neither subsuming the other."),
    (87, "assoc", "Isa 5:11/5:22 pair music and wine in a 'woe' oracle against revelry — co-occurrence, not hierarchy."),
    (88, "assoc", "1 Kgs 5:8/6:34 (cypress doors) don't establish a cedar-leaf relation in the cited text."),
    (89, "assoc", "1 Chr 5:17/2 Kgs 15:5 co-list two kings in a chronological reference, not hierarchy."),
    (90, "assoc", "2 Chr 29:1/Isa 1:1 name a contemporary king and prophet — co-occurrence, not hierarchy."),
    (91, "assoc", "2 Chr 36:10/36:7 describe the temple's plundering during the exile — historical co-occurrence, not a clean causal claim about the Temple concept itself."),
    (92, "narrower:a", "Black is a specific instance of the general Colour category itself (unlike Colour-applied-to-an-object pairings, which stayed associated)."),
    (93, "assoc", "Gen 1:14/Deut 4:19 don't make the moon a subtype of the field of astronomy — category mismatch, associated is the honest fit."),
    (94, "assoc", "Deut 5:14/Gen 2:2 don't establish more than the Sabbath law's application to proselytes."),
    (95, "assoc", "Exod 35:3/12:16 tie Sabbath to the seven-day cycle numerically, not taxonomically."),
    (96, "assoc", "Num 28:25/Exod 12:16 tie convocation to a seven-day festival calendar, not taxonomically."),
    (97, "assoc", "Gen 22:7/8:20 show fire consuming a burnt offering — a definitional element of the ritual itself, matching the Altar/Fire call."),
    (98, "narrower:a", "1 Chr 15:21/1 Sam 10:5 name the harp as a specific instrument within the broader practice of music."),
    (99, "assoc", "Gen 12:7/8:20 don't establish more than co-occurrence of altar and burnt offering."),
    (100, "assoc", "Gen 12:6/Gen 35:4 describe different locations/events (Shechem vs. Bethel's oak) — weak link, correct fallback."),
    (101, "assoc", "Coordinate livestock categories."),
    (102, "assoc", "Gen 36:20/14:6 record Anah as a member of the Horites — genealogical/ethnic membership, kept associated for consistency with other person-to-people-group pairs."),
    (103, "assoc", "1 Kgs 8:38/8:22 use 'seeking God's face' idiomatically within prayer — thematic, not hierarchical."),
    (104, "part_of:b", "Deut 32:14/Isa 7:22 name milk as the source from which butter is made."),
    (105, "assoc", "1 Sam 25:3/Josh 15:13 place Caleb in narrative proximity to giants (Anakim) without a hierarchy between the concepts."),
    (106, "causes:a", "Deut 28:8/2 Kgs 6:27 tie agricultural blessing/scarcity directly to wine's availability — farming produces the crop wine is made from."),
    (107, "assoc", "2 Sam 24:16/Zech 9:7 don't establish an angel-governor hierarchy in the cited text."),
    (108, "narrower:b", "1 Sam 28:14/2 Kgs 2:8 (Elijah's mantle/cloak) show mantle as a specific garment type within dress generally."),
    (109, "assoc", "2 Chr 5:12/1 Chr 13:8 mention linen-clad singers alongside instrumental music — co-occurrence in temple service, not hierarchy."),
    (110, "causes:b", "Deut 15:1/Exod 21:2 (debt cancellation, loan-servitude law) show a loan as what creates a debt obligation."),
    (111, "part_of:b", "Lev 16:12 names the pan (censer) as one of the altar's utensils, per Exod 27:3's utensil list."),
    (112, "assoc", "Descriptive property of the mantle's coloring, matching the Colour pattern."),
    (113, "assoc", "Exod 29:13/Lev 9:19 don't establish a caul-food hierarchy beyond general sacrificial-fat context."),
    (114, "assoc", "Exod 29:27/Lev 10:15 pair the wave breast and heave thigh as coordinate priestly-portion offerings, not hierarchy."),
    (115, "assoc", "Ps 102:6/Mic 1:8 pair cormorant and owl as coordinate desolate-place birds."),
    (116, "narrower:b", "Deut 24:19/Lev 23:22 describe gleaning as a specific harvesting practice within agriculture generally."),
    (117, "assoc", "2 Sam 10:4/Jer 41:5 mention beard-shaving/cutting as a practice, not a hierarchy with 'cutting' generally."),
    (118, "assoc", "Isa 44:15/44:10 describe idol-worship (adoring what one has fashioned) — verb-object relation, not hierarchy."),
    (119, "narrower:a", "Deut 18:15/34:10 present Moses as the archetypal prophet — a specific instance of the prophet category."),
    (120, "assoc", "1 Chr 11:22/2 Sam 8:18 co-list Benaiah and Ira among David's officers."),
    (121, "assoc", "Neh 12:1/12:10 co-list names in a priestly genealogy."),
    (122, "assoc", "Hag 1:1/Neh 7:7 co-list names in a post-exilic leadership roster."),
    (123, "part_of:a", "1 Sam 4:4/Num 7:89 place cherubim on the mercy-seat specifically — a structural component of it."),
    (124, "part_of:b", "1 Kgs 8:6/Isa 37:16 (enthroned above the cherubim) show cherubim as part of the ark's overall design."),
    (125, "narrower:b", "1 Chr 13:8/1 Sam 10:5 list tabret (tambourine) among Easton's instrument catalog."),
    (126, "assoc", "Coordinate livestock categories."),
    (127, "narrower:a", "Josh 15:14/Num 13:33 name Ahiman as one of the sons of Anak — a specific giant."),
    (128, "narrower:b", "Deut 2:10/Num 13:22 name Sheshai as one of the Anakim giants."),
    (129, "narrower:b", "Deut 2:10/Num 13:22 name Talmai as one of the Anakim giants."),
    (130, "assoc", "1 Sam 17:12/Ps 132:6 use Ephratah as Bethlehem's alternate/clan name, not a sub-region."),
    (131, "narrower:b", "1 Kgs 21:27/Isa 22:12 (sackcloth on the waist) show the girdle as one specific garment/accessory within dress generally."),
    (132, "assoc", "Gen 40:11/Prov 3:10 pair cup and wine as instrument-and-content, not hierarchy."),
    (133, "causes:b", "Esth 1:6/Exod 26:1 don't directly evidence this, but Easton's own entries tie linen cloth to the weaver's craft that produces it from flax thread."),
    (134, "assoc", "Coordinate food/drink items in abundance-blessing lists."),
    (135, "narrower:b", "Deut 16:11/16:14 (rejoicing law extended to sojourners) — a proselyte is specifically a converted foreigner, a subtype."),
    (136, "narrower:b", "Exod 13:12/Num 18:15 show firstborn redemption as one specific application of the broader consecration principle."),
    (137, "assoc", "Num 28:25/28:26 place a holy convocation on the day of firstfruits — co-occurring calendar elements, not hierarchy."),
    (138, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule, despite the plausible mercy-seat/tabernacle relationship."),
    (139, "narrower:a", "Exod 26:14/Isa 4:6 (tent coverings, tent as shelter) support the tabernacle as a specific sacred tent, a subtype of tent generally."),
    (140, "assoc", "Descriptive property of curtain coloring, matching the Colour pattern."),
    (141, "narrower:a", "Blue is a specific instance of the general Colour category, matching the Black/Colour call."),
    (142, "assoc", "Descriptive property of the veil's coloring, matching the Colour pattern."),
    (143, "part_of:a", "1 Kgs 8:6/6:19 place the ark within Solomon's temple's inner sanctuary."),
    (144, "assoc", "Exod 27:9/1 Kgs 6:36 (courtyard construction) show tabernacle and temple as successive sanctuaries, not one part of the other."),
    (145, "assoc", "Exod 28:40/28:4 co-list bonnet and girdle as sibling priestly-garment components, neither part of the other."),
    (146, "assoc", "1 Sam 14:18/Judg 20:18 don't establish the Thummim as structurally part of the high priest (a person)."),
    (147, "assoc", "Exod 29:2/Num 6:19 pair cake and wafers as coordinate baked-goods offering types."),
    (148, "assoc", "Exod 29:13/Lev 7:3 don't establish a clean/fat hierarchy beyond general sacrificial context."),
    (149, "assoc", "No verse evidence was recovered for this pair — kept as associated per the no-evidence-no-upgrade rule."),
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
        "model": "claude-in-session (Sonnet 5) — chunk 1 of the weight>=10 batch (indices 0-149)",
        "judgments": judgments,
    }
    out_path = os.path.join(ROOT, "outputs", f"phase5-judgments-{date.today().isoformat()}-w10-chunk1.json")
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(judgments)} judgments to {out_path}")


if __name__ == "__main__":
    main()
