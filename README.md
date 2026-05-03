# claude_cve

A CVE research agent. Given a free‑form description of a security incident, it uses Claude (with Google search via [Serper](https://serper.dev)) to find every CVE publicly discussed in connection with the incident, enriches each CVE with NVD data (CVSS score, severity, description), and prints a table plus a narrative report with source URLs.

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- A [Serper API key](https://serper.dev/) (Google search)

### What is Serper?

[Serper](https://serper.dev) is a paid API that returns Google search results as structured JSON. The agent uses it to give Claude live web access — when Claude calls the `web_search` tool, the script forwards the query to Serper and feeds the results back into the conversation. Without a Serper key the agent has no way to find sources, so this key is required.

To get a key:

1. Sign up at [https://serper.dev](https://serper.dev).
2. Open the **API Key** page in the dashboard.
3. Copy the key shown there. The free tier includes 2,500 queries, which is plenty for trying out this agent (each run typically issues 5–15 queries).

### Getting an Anthropic API key

1. Sign in at [https://console.anthropic.com](https://console.anthropic.com).
2. Go to **Settings → API Keys** and click **Create Key**.
3. Copy the key — you won't be able to view it again after closing the dialog.

## Setup

```bash
git clone <this repo>
cd claude_cve

python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Creating the `.env` file

The script reads both API keys from a `.env` file in the project root. Start from the provided template:

```bash
cp .env.example .env
```

Then open `.env` in your editor and paste in the keys you collected above:

```
ANTHROPIC_API_KEY=sk-ant-...your-anthropic-key...
SERPER_API_KEY=...your-serper-key...
```

Notes:

- No quotes, no spaces around the `=`, one key per line.
- `.env` is git-ignored — keys stay on your machine and won't be committed.
- The script loads `.env` automatically via `python-dotenv`; you don't need
  to `export` the variables yourself.

To verify the keys are wired up correctly, run any quick query — e.g. `./find-cves "Log4Shell"`. If a key is missing or invalid the script will exit with an error pointing at the offending variable.

## Running from the command line

The simplest invocation — pass the incident description as a single quoted argument:

```bash
./venv/bin/python find_cves.py "SolarWinds Orion supply-chain attack"
```

A convenience wrapper is provided that uses the venv's Python automatically:

```bash
./find-cves "Log4Shell"
```

Progress (search queries, enrichment progress) is written to **stderr**; the final CVE table and research summary go to **stdout**, so you can redirect them:

```bash
./find-cves "MOVEit Transfer breach 2023" > report.txt
```

### Flags

| Flag | Description |
|------|-------------|
| `‑‑markdown [PATH]` | Write a markdown report (table + summary). Pass a path to use it directly, or omit the value to auto-name the file as `<incident-slug>-<YYYY-MM-DD>.md` in the current directory. |
| `‑‑json PATH` | Write the full structured result (incident, report, enriched CVEs, source URLs) as JSON. |
| `‑‑no‑enrich` | Skip NVD enrichment. Faster, but you lose CVSS scores, severity, and descriptions. |
| `‑h`, `‑‑help` | Show usage. |

### Examples

Auto-named markdown report alongside terminal output:

```bash
./find-cves "Kaseya VSA ransomware 2021" --markdown
# writes ./kaseya-vsa-ransomware-2021-2026-04-27.md
```

Custom markdown path + JSON dump, skipping NVD lookups:

```bash
./find-cves "Log4Shell" \
    --markdown reports/log4shell.md \
    --json     reports/log4shell.json \
    --no-enrich
```

## Running inside the Claude CLI

This project ships a slash command at `.claude/commands/find-cves.md`. From inside the Claude Code CLI launched in this repo, type:

```
/find-cves <incident description>
```

For example:

```
/find-cves SolarWinds Orion supply-chain attack
/find-cves Log4Shell
/find-cves MOVEit Transfer breach 2023
```

Claude will run `find_cves.py` for you and show the resulting table and report verbatim. If you also want a saved file, ask in the same turn — e.g. *"run /find-cves on Log4Shell and save the markdown report"* — and Claude will pass `--markdown` for you.

## Output

The terminal output has two parts:

1. **CVE table** — one row per CVE, with CVSS score, severity, and a truncated
   description.
2. **Research summary** — Claude's narrative report, with source URLs inline
   next to each CVE.

A markdown file written via `--markdown` contains the same two sections, plus a header line with the incident name and the generation date.

## How it works

1. Claude is given the incident description and access to a `web_search` tool that proxies queries to Serper.
2. Claude issues several searches from different angles (vendor, product, threat actor, attack name, etc.) until it has gathered enough sources, then produces a report listing every CVE it found with the URL where each was discussed.
3. The script extracts CVE IDs and their associated URLs from the report.
4. For each CVE, it queries the NVD API to fetch description, CVSS score, and severity (skip with `--no-enrich`).
5. Results are printed (and optionally written to JSON / markdown).

## Files

- `find_cves.py` — the agent script
- `find-cves` — bash wrapper that uses the venv's Python
- `.claude/commands/find-cves.md` — Claude Code slash-command definition
- `requirements.txt` — Python dependencies
- `.env.example` — template for required API keys
