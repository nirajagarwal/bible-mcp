# Deploying bible-mcp (the three paths)

Decisions behind this runbook: DECISIONS.md D14–D19. Everything below runs on your
Mac from the repo root. Placeholders to fill: your GitHub username, your domain.

## Path 1 — Public GitHub repository

```bash
cd ~/bible-mcp
git init            # if not already a repo
git add -A          # .gitignore excludes db/bible.db, backups, _to_delete
git commit -m "bible-mcp public edition v0.9"
gh repo create bible-mcp --public --source=. --push
```

Then attach the database to a release (D16 — the db is too big for git):

```bash
gh release create v0.9.0 db/bible.db \
  --title "bible-mcp v0.9.0" \
  --notes "Corpus db (SQLite+FTS5, ~230MB). See README for contents; LICENSE.md for terms."
```

Users without the release asset can rebuild: `build_db.py` from `data/sources/`,
then `ingest_additions.py --apply` for each `data/*-2026-*.json`, then `embed.py`.

## Path 2 — Hosted remote endpoint (Fly.io)

One-time: install flyctl (`brew install flyctl`), `fly auth signup` (or login).

```bash
cd ~/bible-mcp
fly launch --no-deploy --name bible-mcp --vm-memory 1024   # accepts the Dockerfile; say no to db/redis
fly deploy                                                  # uploads context incl. db/bible.db (~230MB)
```

Notes:
- The Dockerfile pre-downloads the embedding model; RAM: 1GB machine is comfortable.
- The endpoint is `https://bible-mcp.fly.dev/mcp` (or your custom domain via `fly certs add mcp.yourdomain.org`).
- Server is read-only; no auth by design (D18). If abuse appears: Fly's proxy rate limits, or add a bearer-token check.
- Smoke test: point any MCP client at the URL, or:
  `npx @modelcontextprotocol/inspector https://bible-mcp.fly.dev/mcp`

Add to Claude (any paid plan): Settings → Connectors → Add custom connector →
paste the URL. The corpus_survey / corpus_composer prompts ride along.

Render/Railway equivalents: both accept the same Dockerfile; set env
`BIBLE_MCP_TRANSPORT=streamable-http` (already in the image) and expose $PORT.

## Path 3 — Registries

Official MCP Registry (after Paths 1–2, since it points at both):

1. Edit `server.json`: replace NIRAJ_GITHUB_USERNAME and BIBLE_MCP_DOMAIN.
2. Install the publisher CLI and authenticate with GitHub (device flow):
   ```bash
   brew install mcp-publisher       # or: go install github.com/modelcontextprotocol/registry/cmd/publisher@latest
   mcp-publisher login github
   mcp-publisher publish
   ```
   The `io.github.<username>/*` namespace is validated by your GitHub login.
3. Community aggregators (Glama, PulseMCP, mcp.so) pick it up from the registry.

Anthropic connectors directory: submission form + review; requires the remote
endpoint to be stable and to pass their checks. Do this after the endpoint has
run quietly for a week or two.

## Update cycle

New corpus version: bump `server.json` version, `gh release create vX.Y.Z db/bible.db`,
`fly deploy`, `mcp-publisher publish`. Code-only change: `fly deploy` alone.
