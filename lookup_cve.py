#!/usr/bin/env python3
"""Look up a CVE record on cve.org and print Updated, Published, Title, Description."""

import argparse
import re
import sys
from typing import Any

import requests

CVE_API = "https://cveawg.mitre.org/api/cve/{cve_id}"
CVE_ID_RE = re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE)


def fetch_cve(cve_id: str) -> dict[str, Any]:
    url = CVE_API.format(cve_id=cve_id.upper())
    resp = requests.get(url, timeout=15, headers={"Accept": "application/json"})
    if resp.status_code == 404:
        raise LookupError(f"CVE not found: {cve_id}")
    resp.raise_for_status()
    return resp.json()


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
    for key in ("ID", "Published", "Updated", "Title", "Description"):
        print(f"{key}: {fields[key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
