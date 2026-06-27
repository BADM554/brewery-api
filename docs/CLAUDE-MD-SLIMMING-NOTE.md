# Note: CLAUDE.md slimming opportunity

_Left 2026-06-28 during a cross-repo CLAUDE.md audit. Not yet done here — flagged for a future pass._

## Why

CLAUDE.md is ~313 lines. The session log is **not** the culprit (~3 lines, already archived). The weight
is inline operational runbooks that, per the global rule in `~/.claude/CLAUDE.md` ("include only
non-inferable knowledge; link instead of inline"), belong in `docs/` with a short summary + link.

⚠️ **This repo is PUBLIC** — when extracting, scrub any tokens/keys/endpoints; keep secrets in `.env` only.

## Suggested extractions (biggest first)

| Section | ~lines | Target |
|---------|-------:|--------|
| GitHub Actions Workflows | 39 | `docs/ci-workflows.md` |
| Local Development | 37 | `docs/local-development.md` |
| Architecture | 30 | `docs/architecture.md` |
| Deployment | 28 | `docs/deployment.md` |
| Data Structure | 28 | `docs/data-structure.md` |
| Troubleshooting | 20 | `docs/troubleshooting.md` |

Extracting the top 3–4 would drop CLAUDE.md by ~130 lines (→ ~180).

## The pattern (as applied to badm554, makerlab, canvas-mcp on 2026-06-28)

1. Move the full runbook section to `docs/<topic>.md` (verbatim, with a one-line header).
2. Replace it in CLAUDE.md with a ~5–10 line summary + a `[docs/<topic>.md](docs/<topic>.md)` link.
3. **Scrub any inline credentials** while moving — never leave secrets in a tracked file (this repo is public).
4. Commit; verify no content was lost (`wc -l` the new doc, grep a known string).
