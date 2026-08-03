# bible-mcp remote server (Streamable HTTP) — see DECISIONS.md D18/D19, DEPLOY.md
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "mcp>=1.0,<2.0" fastembed numpy

# Pre-download the embedding model at build time so first queries are fast.
RUN python3 -c "from fastembed import TextEmbedding; TextEmbedding('BAAI/bge-small-en-v1.5')"

COPY server.py ./
COPY scripts/lib_refs.py ./scripts/
COPY .claude/skills ./.claude/skills
# The database is built/maintained outside the image pipeline; copy it in.
# (deploying from the repo root on a machine that has db/bible.db — see DEPLOY.md)
COPY db/bible.db ./db/bible.db

ENV BIBLE_MCP_TRANSPORT=streamable-http \
    PORT=8080

EXPOSE 8080
CMD ["python3", "server.py"]
