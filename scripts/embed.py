"""Generate embeddings into the embeddings table. Re-runnable; replaces prior vectors
for the same model. See DESIGN.md §1 for chunking and model rationale.

Usage: python3 scripts/embed.py [--model BAAI/bge-small-en-v1.5]
"""
import argparse
import os
import sqlite3
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.environ.get("BIBLE_DB_PATH", os.path.join(ROOT, "db", "bible.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS embeddings (
  id     INTEGER PRIMARY KEY,
  kind   TEXT NOT NULL,          -- verse | window | paragraph
  doc_id TEXT NOT NULL,
  ref    TEXT NOT NULL,          -- start ref
  end_ref TEXT,                  -- end ref for windows
  text   TEXT NOT NULL,          -- the embedded text (for display/debug)
  model  TEXT NOT NULL,
  dim    INTEGER NOT NULL,
  vec    BLOB NOT NULL           -- float16, L2-normalized
);
CREATE INDEX IF NOT EXISTS idx_emb_ref ON embeddings(ref);
CREATE INDEX IF NOT EXISTS idx_emb_kind ON embeddings(kind);
"""

WINDOW, STRIDE = 5, 3


def collect_chunks(con):
    """Yield (kind, doc_id, ref, end_ref, text) per DESIGN.md: BSB verses for 66 books,
    WEB verses for Apocrypha-only books, 5-verse windows, prose paragraphs."""
    chunks = []
    bsb_books = {r[0] for r in con.execute("SELECT DISTINCT book FROM passages WHERE doc_id='BSB'")}

    # verse + window chunks per (doc, book, chapter)
    for doc, book_filter in [("BSB", None), ("WEB", bsb_books)]:
        q = "SELECT book, chapter, verse, ref, text FROM passages WHERE doc_id=? ORDER BY seq"
        rows = con.execute(q, (doc,)).fetchall()
        by_ch = {}
        for book, ch, v, ref, text in rows:
            if book_filter is not None and book in book_filter:
                continue  # WEB: apocrypha-only
            chunks.append(("verse", doc, ref, None, text))
            by_ch.setdefault((book, ch), []).append((ref, text))
        for (book, ch), verses in by_ch.items():
            for i in range(0, len(verses), STRIDE):
                win = verses[i:i + WINDOW]
                if len(win) < 2:
                    continue
                chunks.append(("window", doc, win[0][0], win[-1][0], " ".join(t for _, t in win)))

    # prose paragraphs
    for doc_id, ref, text in con.execute(
            "SELECT doc_id, ref, text FROM passages WHERE doc_id NOT IN ('BSB','WEB') ORDER BY seq"):
        chunks.append(("paragraph", doc_id, ref, None, text))
    return chunks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--batch", type=int, default=256)
    args = ap.parse_args()

    import numpy as np
    from fastembed import TextEmbedding

    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)

    chunks = collect_chunks(con)
    # resumable: chunk order is deterministic; skip what's already stored
    already = con.execute("SELECT COUNT(*) FROM embeddings WHERE model=?", (args.model,)).fetchone()[0]
    if already >= len(chunks):
        print(f"Already complete: {already} vectors")
        return
    if already:
        print(f"Resuming at {already}/{len(chunks)}", flush=True)
    chunks_todo = chunks[already:]
    print(f"{len(chunks_todo)} chunks to embed with {args.model}", flush=True)

    model = TextEmbedding(model_name=args.model, threads=os.cpu_count())
    chunks = chunks_todo
    done = already
    for i in range(0, len(chunks), args.batch):
        batch = chunks[i:i + args.batch]
        vecs = list(model.embed([c[4] for c in batch], batch_size=args.batch))
        rows = []
        for (kind, doc, ref, end_ref, text), v in zip(batch, vecs):
            v = np.asarray(v, dtype=np.float32)
            v = v / (np.linalg.norm(v) + 1e-9)
            rows.append((kind, doc, ref, end_ref, text, args.model, len(v),
                         v.astype(np.float16).tobytes()))
        con.executemany(
            "INSERT INTO embeddings(kind,doc_id,ref,end_ref,text,model,dim,vec) VALUES(?,?,?,?,?,?,?,?)", rows)
        con.commit()
        done += len(batch)
        if done % 5120 < args.batch:
            print(f"  {done}/{len(chunks)}", flush=True)
    print(f"Done: {done} vectors", flush=True)


if __name__ == "__main__":
    main()
