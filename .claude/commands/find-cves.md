---
description: Find CVEs discussed on the Internet related to a security incident
argument-hint: "[incident description] [--json path] [--markdown [path]] [--no-enrich]"
allowed-tools: Bash
---

Run the CVE research agent on the user's incident.

Use the Bash tool to execute:

```
./venv/bin/python find_cves.py $ARGUMENTS
```

The script loads `ANTHROPIC_API_KEY` and `SERPER_API_KEY` from `.env` automatically. It prints a progress log to stderr and the final report (CVE table + research summary) to stdout. After the command completes, show the user the script's stdout verbatim — do not re-summarize it.

If `$ARGUMENTS` is empty, ask the user to describe the incident before running the command.
