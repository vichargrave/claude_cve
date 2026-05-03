#!/usr/bin/env python3
"""Look up a CVE record on cve.org and print Updated, Published, Title, Description."""

import argparse
import re
import sys
from typing import Any

import anthropic
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-4-7"
CVE_API = "https://cveawg.mitre.org/api/cve/{cve_id}"
CVE_ID_RE = re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE)

SUMMARY_SYSTEM = (
    "You are a security analyst. Given a CVE description, produce a single "
    "concise sentence (max 30 words) capturing the affected product, the "
    "vulnerability type, and the impact. Output only the sentence — no "
    "preamble, no quotes, no labels."
)


def fetch_cve(cve_id: str) -> dict[str, Any]:
    url = CVE_API.format(cve_id=cve_id.upper())
    resp = requests.get(url, timeout=15, headers={"Accept": "application/json"})
    if resp.status_code == 404:
        raise LookupError(f"CVE not found: {cve_id}")
    resp.raise_for_status()
    return resp.json()


def summarize(description: str) -> str:
    """Generate a brief, intelligent summary of the CVE description via Claude."""
    if not description or description == "(no description)":
        return description
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SUMMARY_SYSTEM,
        messages=[{"role": "user", "content": description.strip()}],
    )
    return next(
        (b.text.strip() for b in response.content if b.type == "text"),
        description,
    )


def extract_fields(record: dict[str, Any]) -> dict[str, str]:
    meta = record.get("cveMetadata", {})
    containers = record.get("containers", {})
    cna = containers.get("cna", {}) or {}

    title = cna.get("title") or "(no title)"

    description = "(no description)"
    for entry in cna.get("descriptions", []) or []:
        if entry.get("lang", "").lower().startswith("en"):
            description = entry.get("value", description)
            break
    else:
        descs = cna.get("descriptions") or []
        if descs:
            description = descs[0].get("value", description)

    return {
        "ID": meta.get("cveId", "(unknown)"),
        "Published": meta.get("datePublished", "(unknown)"),
        "Updated": meta.get("dateUpdated", "(unknown)"),
        "Title": title,
        "Description": description,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Look up a CVE on cve.org.")
    parser.add_argument("cve_id", help="CVE identifier, e.g. CVE-2024-12345")
    args = parser.parse_args()

    if not CVE_ID_RE.match(args.cve_id):
        print(
            f"Error: '{args.cve_id}' is not a valid CVE ID (expected format CVE-YYYY-NNNN+).",
            file=sys.stderr,
        )
        return 2

    try:
        record = fetch_cve(args.cve_id)
    except LookupError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except requests.exceptions.Timeout:
        print("Error: cve.org request timed out. The service may be slow or unreachable.", file=sys.stderr)
        return 1
    except requests.exceptions.ConnectionError:
        print("Error: could not connect to cve.org. The service may be down or you may be offline.", file=sys.stderr)
        return 1
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        print(f"Error: cve.org returned HTTP {status}. The service may be unavailable.", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"Error: cve.org request failed: {e}", file=sys.stderr)
        return 1

    fields = extract_fields(record)
    bold = "\033[1m" if sys.stdout.isatty() else ""
    reset = "\033[0m" if sys.stdout.isatty() else ""
    summary = summarize(fields["Description"])

    for key in ("ID", "Published", "Updated"):
        print(f"{key}: {fields[key]}")
    print(f"{bold}Title: {fields['Title']}{reset}")
    print(f"Summary: {summary}")
    print(f"Description: {fields['Description']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
