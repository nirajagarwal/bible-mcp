-- bible-mcp core schema
-- Canonical addressing: OSIS-style refs, e.g. Gen.1.1, Matt.5.3, Tob.4.5

CREATE TABLE IF NOT EXISTS documents (
  id           TEXT PRIMARY KEY,        -- e.g. 'BSB', 'WEB'
  title        TEXT NOT NULL,
  layer        TEXT NOT NULL,           -- canon | deuterocanon | patristic | pseudepigrapha | gnostic | mystic | reference
  language     TEXT NOT NULL,
  translator   TEXT,
  source_url   TEXT,
  license      TEXT,                    -- e.g. 'Public Domain', 'CC BY 4.0'
  license_tier TEXT,                    -- A | B | C | D  (see corpus-survey.md)
  notes        TEXT
);

CREATE TABLE IF NOT EXISTS passages (
  id      INTEGER PRIMARY KEY,
  doc_id  TEXT NOT NULL REFERENCES documents(id),
  ref     TEXT NOT NULL,               -- canonical OSIS ref
  book    TEXT NOT NULL,               -- OSIS book code, e.g. 'Gen'
  chapter INTEGER NOT NULL,
  verse   INTEGER NOT NULL,
  seq     INTEGER NOT NULL,            -- global reading order within doc
  text    TEXT NOT NULL,
  UNIQUE (doc_id, ref)
);
CREATE INDEX IF NOT EXISTS idx_passages_ref  ON passages(ref);
CREATE INDEX IF NOT EXISTS idx_passages_book ON passages(doc_id, book, chapter, verse);

-- Full-text search (BM25, porter stemming)
CREATE VIRTUAL TABLE IF NOT EXISTS passages_fts USING fts5(
  text,
  content='passages', content_rowid='id',
  tokenize='porter unicode61'
);
CREATE TRIGGER IF NOT EXISTS passages_ai AFTER INSERT ON passages BEGIN
  INSERT INTO passages_fts(rowid, text) VALUES (new.id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS passages_ad AFTER DELETE ON passages BEGIN
  INSERT INTO passages_fts(passages_fts, rowid, text) VALUES ('delete', old.id, old.text);
END;

-- Typed edges between references (and later: between prose sections, entities)
CREATE TABLE IF NOT EXISTS links (
  id       INTEGER PRIMARY KEY,
  from_ref TEXT NOT NULL,
  to_ref   TEXT NOT NULL,              -- may be a range, e.g. Gen.1.26-Gen.1.27
  type     TEXT NOT NULL,              -- cross_reference | citation | parallel | ...
  weight   REAL,                       -- e.g. openbible.info votes
  source   TEXT
);
CREATE INDEX IF NOT EXISTS idx_links_from ON links(from_ref);
CREATE INDEX IF NOT EXISTS idx_links_to   ON links(to_ref);

-- People, places, events, groups (Theographic + future)
CREATE TABLE IF NOT EXISTS entities (
  id          TEXT PRIMARY KEY,        -- source id, e.g. Theographic rec id
  type        TEXT NOT NULL,           -- person | place | event | people_group
  name        TEXT NOT NULL,
  slug        TEXT,                    -- e.g. 'aaron_1'
  description TEXT,
  data        TEXT                     -- JSON: everything else (dates, coords, relations)
);
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
CREATE INDEX IF NOT EXISTS idx_entities_slug ON entities(slug);

-- Word-level original-language data (MACULA Greek/Hebrew, CC BY 4.0)
CREATE TABLE IF NOT EXISTS words (
  id      INTEGER PRIMARY KEY,
  ref     TEXT NOT NULL,               -- verse ref, e.g. Gen.1.1
  pos     INTEGER NOT NULL,            -- word position within verse
  lang    TEXT NOT NULL,               -- grc | hbo | arc
  surface TEXT,                        -- word as written
  translit TEXT,
  lemma   TEXT,
  strong  TEXT,                        -- G#### / H####
  gloss   TEXT,
  english TEXT,                        -- contextual English
  morph   TEXT,
  domain  TEXT,                        -- semantic domain code (Louw-Nida / SDBH)
  ln      TEXT
);
CREATE INDEX IF NOT EXISTS idx_words_ref    ON words(ref);
CREATE INDEX IF NOT EXISTS idx_words_lemma  ON words(lemma);
CREATE INDEX IF NOT EXISTS idx_words_strong ON words(strong);

CREATE TABLE IF NOT EXISTS entity_mentions (
  entity_id TEXT NOT NULL REFERENCES entities(id),
  ref       TEXT NOT NULL,
  PRIMARY KEY (entity_id, ref)
);
CREATE INDEX IF NOT EXISTS idx_mentions_ref ON entity_mentions(ref);
