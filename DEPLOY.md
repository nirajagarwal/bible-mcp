# Deploying bible-mcp (the three paths)

A guide for standing up your own instance — whether you're publishing a fresh
fork under your own account or just deploying a private copy. Everything below
runs from your local clone of the repo root. Fill in your own values wherever
you see a placeholder like `<your-repo-name>` or `<your-app-name>`.

If you forked the existing public repo, you likely only need **Path 2** (and
optionally Path 3) — Path 1 is for going from a private/local project to a
public repo for the first time.

## Path 1 — Public GitHub repository

```bash
cd your-clone-of-bible-mcp
git init            # if not already a repo
git add -A          # .gitignore excludes db/bible.db, backups, _to_delete
git commit -m "initial public commit"
gh repo create <your-repo-name> --public --source=. --push
```

Then attach the database to a release (the db is too big for git — GitHub's
file-size cap is 100MB and this db is ~230MB):

```bash
gh release create v0.1.0 db/bible.db \
  --title "<your-repo-name> v0.1.0" \
  --notes "Corpus db (SQLite+FTS5, ~230MB). See README for contents; LICENSE.md for terms."
```

Note: forking on GitHub does **not** copy Releases. If you forked rather than
starting fresh, download `db/bible.db` from the upstream release (or rebuild
it, below) and create your own release with it.

No release asset yet? Rebuild it: `build_db.py` from `data/sources/`,
then `ingest_additions.py --apply` for each `data/*-2026-*.json`, then `embed.py`.

## Path 2 — Hosted remote endpoint (Fly.io)

One-time: install flyctl (`brew install flyctl`), `fly auth signup` (or login).

```bash
cd your-clone-of-bible-mcp
fly launch --no-deploy --name <your-app-name> --vm-memory 1024 --no-db --no-redis
fly deploy                                                  # uploads context incl. db/bible.db (~230MB)
```

Notes:
- App names are global on Fly.io — if your first choice is taken, `fly launch`
  will auto-generate a suffixed name instead (or error on `fly apps create`);
  just pick another with `--name`.
- The Dockerfile pre-downloads the embedding model; RAM: 1GB machine is comfortable.
- The endpoint is `https://<your-app-name>.fly.dev/mcp` (or your custom domain via `fly certs add mcp.yourdomain.org`).
- Server is read-only; no auth by design. If abuse appears: Fly's proxy rate limits, or add a bearer-token check.
- Smoke test: point any MCP client at the URL, or:
  `npx @modelcontextprotocol/inspector https://<your-app-name>.fly.dev/mcp`
- `fly launch` may also offer to wire up a GitHub Actions auto-deploy workflow
  (`FLY_API_TOKEN` secret + `.github/workflows/fly-deploy.yml`). If you keep
  it, note that CI won't have `db/bible.db` — it's a release asset, not in git
  — so add a step to fetch it from your release before the Docker build:
  `gh release download --pattern 'bible.db' --dir db/`.

Add to Claude (any paid plan): Settings → Connectors → Add custom connector →
paste the URL. The corpus_survey / corpus_composer prompts ride along.

Render/Railway equivalents: both accept the same Dockerfile; set env
`BIBLE_MCP_TRANSPORT=streamable-http` (already in the image) and expose $PORT.

## Path 3 — Registries

Official MCP Registry (after Paths 1–2, since it points at both):

1. Edit `server.json`: replace the `NIRAJ_GITHUB_USERNAME`/`BIBLE_MCP_DOMAIN`
   placeholders with your own GitHub username and endpoint domain, and keep
   `description` to ≤100 characters (the registry's hard limit — a longer one
   is fine for the README or GitHub's own About field).
2. Install the publisher CLI and authenticate with GitHub (device flow):
   ```bash
   brew install mcp-publisher       # or: go install github.com/modelcontextprotocol/registry/cmd/publisher@latest
   mcp-publisher login github
   mcp-publisher validate           # sanity-check server.json before publishing
   mcp-publisher publish
   ```
   The `io.github.<username>/*` namespace is validated by your GitHub login,
   so this always publishes under your own account. The login token is
   short-lived — if `publish` fails with an expired-token error, just re-run
   `mcp-publisher login github` and try again.
3. Community aggregators (Glama, PulseMCP, mcp.so) pick it up from the registry.

Anthropic connectors directory: submission form + review; requires the remote
endpoint to be stable and to pass their checks. Do this after the endpoint has
run quietly for a week or two.

## Update cycle

New corpus version: bump `server.json` version, `gh release create vX.Y.Z db/bible.db`,
`fly deploy`, `mcp-publisher publish`. Code-only change: `fly deploy` alone.
