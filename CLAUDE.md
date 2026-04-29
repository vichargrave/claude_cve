# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository State

**Purpose:** A CVE research agent. Given a free-form description of a security incident, it uses Claude (`claude-opus-4-7`) plus Google search via [Serper](https://serper.dev) to find every CVE publicly discussed in connection with the incident, enriches each CVE with NVD data (CVSS score, severity, description), and prints a table plus a narrative report with source URLs.

**Key files:**
- `find_cves.py` — main agent script (~400 lines). Runs an agentic loop with a `web_search` tool backed by Serper, extracts CVE IDs and source URLs from Claude's report, then enriches each via the NVD API.
- `find-cves` — bash wrapper that invokes `./venv/bin/python find_cves.py "$@"`.
- `.claude/commands/find-cves.md` — Claude Code slash command (`/find-cves <incident>`).
- `requirements.txt` — `anthropic`, `requests`, `python-dotenv`.
- `.env.example` — template for `ANTHROPIC_API_KEY` and `SERPER_API_KEY`.
- `README.md` — user-facing documentation.

**CLI flags on `find_cves.py`:**
- `--markdown [PATH]` — write a markdown report; omit PATH to auto-name as `<slug>-<YYYY-MM-DD>.md`.
- `--json PATH` — write full structured results.
- `--no-enrich` — skip NVD lookups.

**Generated reports in repo root** (sample outputs from prior runs):
- `AI-Assisted-AWS-Admin-Access-in-Under-10-Minutes-2026-04-27.md`
- `amazon-threat-intelligence-identifies-russian-cyber-threat-g-2026-04-27.md`
- `solarwinds-orion-cves-2026-04-27.md`
- `vertex-ai-vulnerability-exposes-google-cloud-data-and-privat-2026-04-27.md`

**Runtime requirements:** Python 3.10+, populated `.env`, working venv at `./venv/`.

## Git Workflow

Work must be committed to Git regularly and pushed to GitHub to ensure no loss of progress or status. Follow these practices:

**Commit Frequency:**
- Commit after completing each logical unit of work (feature, bug fix, documentation update)
- Do not accumulate multiple changes before committing
- Aim for frequent, incremental commits rather than large batches

**Commit Messages:**
- Use clear, descriptive commit messages that explain what changed and why
- Format: Start with a present-tense imperative verb (e.g., "Add feature", "Fix bug", "Update docs")
- Include context about the change when relevant
- Example: "Add keyboard shortcut for find/replace" or "Fix win detection edge case in tic tac toe"

**Pushing:**
- Push commits to GitHub regularly (after each commit or at the end of each work session)
- This ensures changes are backed up and accessible remotely
- Never leave uncommitted work in progress without a clear reason

**Session-end safety net:**
- A `SessionEnd` hook in `.claude/settings.local.json` runs on every Claude Code session exit. If the working tree is dirty, it stages all changes (`git add -A`), commits them with the message `"Auto-commit on Claude Code session end"`, and pushes if an upstream is configured (otherwise it prints `(no upstream — not pushing)` and exits cleanly).
- The hook bypasses pre-commit and pre-push hooks (`--no-verify` on both `git commit` and `git push`) so the auto-commit can never be rejected by a local hook. This is the catch-all safety net — run lint/test checks during the session, not at session end.
- The hook is a backstop, not a substitute for the commit-frequently / push-regularly discipline above. Prefer creating meaningful, scoped commits during the session over relying on the catch-all auto-commit.
