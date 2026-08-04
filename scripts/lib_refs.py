"""Canonical reference handling: OSIS book codes, name/abbrev resolution, ref parsing."""
import re

# (osis, full name, paratext code, common aliases)
BOOKS = [
    ("Gen", "Genesis", "GEN", ["Ge", "Gn"]),
    ("Exod", "Exodus", "EXO", ["Ex", "Exo"]),
    ("Lev", "Leviticus", "LEV", ["Lv"]),
    ("Num", "Numbers", "NUM", ["Nm", "Nu"]),
    ("Deut", "Deuteronomy", "DEU", ["Dt"]),
    ("Josh", "Joshua", "JOS", ["Jos"]),
    ("Judg", "Judges", "JDG", ["Jdg", "Jgs"]),
    ("Ruth", "Ruth", "RUT", ["Ru"]),
    ("1Sam", "1 Samuel", "1SA", ["1 Sam", "1Sm"]),
    ("2Sam", "2 Samuel", "2SA", ["2 Sam", "2Sm"]),
    ("1Kgs", "1 Kings", "1KI", ["1 Kgs", "1 Kin"]),
    ("2Kgs", "2 Kings", "2KI", ["2 Kgs", "2 Kin"]),
    ("1Chr", "1 Chronicles", "1CH", ["1 Chr", "1 Chron"]),
    ("2Chr", "2 Chronicles", "2CH", ["2 Chr", "2 Chron"]),
    ("Ezra", "Ezra", "EZR", ["Ezr"]),
    ("Neh", "Nehemiah", "NEH", ["Ne"]),
    ("Esth", "Esther", "EST", ["Est"]),
    ("Job", "Job", "JOB", ["Jb"]),
    ("Ps", "Psalms", "PSA", ["Psalm", "Pss", "Psa"]),
    ("Prov", "Proverbs", "PRO", ["Prv", "Pr"]),
    ("Eccl", "Ecclesiastes", "ECC", ["Ecc", "Qoheleth"]),
    ("Song", "Song of Solomon", "SOL", ["Song of Songs", "SOS", "Canticles", "Sg"]),
    ("Isa", "Isaiah", "ISA", ["Is"]),
    ("Jer", "Jeremiah", "JER", ["Jr"]),
    ("Lam", "Lamentations", "LAM", ["La"]),
    ("Ezek", "Ezekiel", "EZE", ["Ez", "Ezk"]),
    ("Dan", "Daniel", "DAN", ["Dn"]),
    ("Hos", "Hosea", "HOS", ["Ho"]),
    ("Joel", "Joel", "JOE", ["Jl"]),
    ("Amos", "Amos", "AMO", ["Am"]),
    ("Obad", "Obadiah", "OBA", ["Ob"]),
    ("Jonah", "Jonah", "JON", ["Jon"]),
    ("Mic", "Micah", "MIC", ["Mi"]),
    ("Nah", "Nahum", "NAH", ["Na"]),
    ("Hab", "Habakkuk", "HAB", ["Hb"]),
    ("Zeph", "Zephaniah", "ZEP", ["Zep"]),
    ("Hag", "Haggai", "HAG", ["Hg"]),
    ("Zech", "Zechariah", "ZEC", ["Zec"]),
    ("Mal", "Malachi", "MAL", ["Ml"]),
    ("Matt", "Matthew", "MAT", ["Mt", "Mat"]),
    ("Mark", "Mark", "MAR", ["Mk", "Mrk"]),
    ("Luke", "Luke", "LUK", ["Lk"]),
    ("John", "John", "JOH", ["Jn", "Jhn"]),
    ("Acts", "Acts", "ACT", ["Ac"]),
    ("Rom", "Romans", "ROM", ["Rm"]),
    ("1Cor", "1 Corinthians", "1CO", ["1 Cor"]),
    ("2Cor", "2 Corinthians", "2CO", ["2 Cor"]),
    ("Gal", "Galatians", "GAL", ["Ga"]),
    ("Eph", "Ephesians", "EPH", ["Ep"]),
    ("Phil", "Philippians", "PHI", ["Php", "Phil"]),
    ("Col", "Colossians", "COL", ["Cl"]),
    ("1Thess", "1 Thessalonians", "1TH", ["1 Thess", "1 Thes"]),
    ("2Thess", "2 Thessalonians", "2TH", ["2 Thess", "2 Thes"]),
    ("1Tim", "1 Timothy", "1TI", ["1 Tim"]),
    ("2Tim", "2 Timothy", "2TI", ["2 Tim"]),
    ("Titus", "Titus", "TIT", ["Ti"]),
    ("Phlm", "Philemon", "PHM", ["Phm", "Philem"]),
    ("Heb", "Hebrews", "HEB", ["He"]),
    ("Jas", "James", "JAM", ["Jm", "Jam"]),
    ("1Pet", "1 Peter", "1PE", ["1 Pet", "1Pt"]),
    ("2Pet", "2 Peter", "2PE", ["2 Pet", "2Pt"]),
    ("1John", "1 John", "1JO", ["1 Jn", "1 John"]),
    ("2John", "2 John", "2JO", ["2 Jn", "2 John"]),
    ("3John", "3 John", "3JO", ["3 Jn", "3 John"]),
    ("Jude", "Jude", "JUD", ["Jud"]),
    ("Rev", "Revelation", "REV", ["Rv", "Apocalypse"]),
    # Deuterocanon / Apocrypha (WEB ecumenical edition, Paratext codes as shipped by eBible.org)
    ("Tob", "Tobit", "TOB", ["Tb"]),
    ("Jdt", "Judith", "JDT", ["Jth"]),
    ("EsthGr", "Esther (Greek)", "ESG", ["Greek Esther"]),
    ("Wis", "Wisdom of Solomon", "WIS", ["Wisdom", "Ws"]),
    ("Sir", "Sirach", "SIR", ["Ecclesiasticus", "Ben Sira"]),
    ("Bar", "Baruch", "BAR", []),
    ("DanGr", "Daniel (Greek)", "DNG", ["Greek Daniel"]),
    ("1Macc", "1 Maccabees", "1MA", ["1 Macc"]),
    ("2Macc", "2 Maccabees", "2MA", ["2 Macc"]),
    ("3Macc", "3 Maccabees", "3MA", ["3 Macc"]),
    ("4Macc", "4 Maccabees", "4MA", ["4 Macc"]),
    ("1Esd", "1 Esdras", "1ES", ["1 Esd"]),
    ("2Esd", "2 Esdras", "4ES", ["2 Esd", "4 Ezra"]),
    ("PrMan", "Prayer of Manasseh", "PRM", ["Manasseh"]),
    ("AddPs", "Psalm 151", "PSX", ["Ps151"]),
]

OSIS = {b[0] for b in BOOKS}
PARATEXT_TO_OSIS = {b[2]: b[0] for b in BOOKS}
# Standard Paratext codes (used by MACULA) that differ from eBible VPL codes
PARATEXT_TO_OSIS.update({
    "MRK": "Mark", "JHN": "John", "PHP": "Phil", "JAS": "Jas",
    "1JN": "1John", "2JN": "2John", "3JN": "3John",
    "EZK": "Ezek", "JOL": "Joel", "NAM": "Nah", "SNG": "Song",
})
NAME_TO_OSIS = {}
for osis, full, para, aliases in BOOKS:
    for key in [osis, full, para] + aliases:
        NAME_TO_OSIS[key.lower().replace(" ", "")] = osis
BOOK_ORDER = {b[0]: i for i, b in enumerate(BOOKS)}
OSIS_TO_NAME = {b[0]: b[1] for b in BOOKS}


def book_to_osis(name: str):
    """Resolve any book name/abbreviation/code to its OSIS code, or None."""
    return NAME_TO_OSIS.get(name.strip().lower().replace(".", "").replace(" ", ""))


_REF = re.compile(
    r"^\s*(?P<book>(?:[1-4]\s?)?[A-Za-z][A-Za-z .]*?)[\s.]+(?P<ch>\d+)"
    r"(?:[:.](?P<v1>\d+)(?:\s*[-–]\s*(?:[A-Za-z .]*?[\s.:])?(?P<v2>\d+))?)?\s*$"
)


def parse_ref(ref: str):
    """Parse 'John 3:16', 'John 3:16-18', 'Gen.1.1', '1 Cor 13:4' ->
    (osis_book, chapter, verse_start, verse_end) — verses None for whole chapter.

    Also accepts the full-ref-to-full-ref range form used internally for
    links.to_ref, e.g. 'Gen.1.26-Gen.1.27' (same book+chapter only — matches
    _expand_range_ref's convention in server.py), so a to_ref value copied
    straight from get_cross_references works as-is in any other tool."""
    if "-" in ref:
        left, _, right = ref.rpartition("-")
        try:
            lb, lc, lv1, _ = parse_ref(left)
            rb, rc, rv1, _ = parse_ref(right)
            if lb == rb and lc == rc and lv1 is not None and rv1 is not None:
                return lb, lc, lv1, rv1
        except ValueError:
            pass
    m = _REF.match(ref)
    if not m:
        raise ValueError(f"Cannot parse reference: {ref!r}")
    book = book_to_osis(m.group("book"))
    if not book:
        raise ValueError(f"Unknown book in reference: {ref!r}")
    ch = int(m.group("ch"))
    v1 = int(m.group("v1")) if m.group("v1") else None
    v2 = int(m.group("v2")) if m.group("v2") else v1
    return book, ch, v1, v2


def make_ref(book: str, chapter: int, verse: int) -> str:
    return f"{book}.{chapter}.{verse}"


_ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}


def roman_to_int(s: str):
    """Lowercase/uppercase roman numeral -> int, or None if invalid."""
    s = s.lower()
    total, prev = 0, 0
    for ch in reversed(s):
        v = _ROMAN.get(ch)
        if v is None:
            return None
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total if total > 0 else None


_CITATION_RE = re.compile(r"\b((?:[1-4]\s?)?[A-Za-z][a-z]+)\.?\s+([ivxlcdm]+)\.\s*(\d+)", re.I)


def parse_scripture_citations(text: str):
    """Find 'Book. roman-chapter. arabic-verse' citations in prose (e.g. ANF footnotes:
    'Eph. v. 21; 1 Pet. v. 5.') and resolve each to an OSIS ref. Non-citation text
    (translation notes, textual-critical remarks) yields an empty list, by design."""
    out = []
    for book_raw, roman, verse in _CITATION_RE.findall(text):
        book = book_to_osis(book_raw)
        ch = roman_to_int(roman)
        if book and ch:
            out.append(f"{book}.{ch}.{verse}")
    return out
