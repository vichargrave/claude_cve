#!/usr/bin/env python3
"""Find CVEs discussed on the Internet related to a specified security incident."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import date
from typing import Any

import anthropic
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-4-7"
CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
URL_PATTERN = re.compile(r"https?://[^\s\)\]\}>'\"`,]+")
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
SERPER_API = "https://google.serper.dev/search"
MAX_AGENT_TURNS = 12

SYSTEM_PROMPT = (
    "You are a security research assistant. The user will describe a security "
    "incident. Use the web_search tool (which queries Google via SERPER) to "
    "find articles, vendor advisories, blog posts, and public discussions "
    "about this incident on the Internet. Identify every CVE identifier "
    "(format: CVE-YYYY-NNNN) that is discussed in connection with the "
    "incident. Be thorough — issue several searches from different angles: "
    "the vendor name, product names, the attack technique, the threat actor, "
    "and any publicly reported indicators. After your research, produce a "
    "concise report that:\n"
    "  1. Summarizes what is publicly known about the incident.\n"
    "  2. Lists every related CVE you found, each with a one-line note about "
    "how it relates to the incident.\n"
    "  3. Includes the source URL(s) where each CVE was discussed in a "
    "parseable form (place URLs inline near the CVE they belong to).\n"
    "If you find no CVEs after a thorough search, say so explicitly."
)

TOOLS: list[dict[str, Any]] = [
    {
        "name": "web_search",
        "description": (
            "Search the web via Google (using SERPER). Returns the top organic "
            "results with title, URL, and snippet, plus any answer box or "
            "knowledge-graph data Google returned. Use this repeatedly with "
            "different queries to find articles, advisories, and discussions "
            "relevant to a security incident or CVE."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string.",
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of organic results to request (1-20, default 10).",
                    "minimum": 1,
                    "maximum": 20,
                },
            },
            "required": ["query"],
        },
    },
]


def search_serper(query: str, num_results: int = 10) -> dict[str, Any]:
    """Run a Google search via SERPER and return condensed results."""
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        return {"error": "SERPER_API_KEY is not set"}

    try:
        resp = requests.post(
            SERPER_API,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "num": max(1, min(20, num_results))},
            timeout=20,
        )
    except requests.RequestException as e:
        return {"error": f"SERPER request failed: {e}"}

    if resp.status_code != 200:
        return {"error": f"SERPER returned HTTP {resp.status_code}: {resp.text[:200]}"}

    data = resp.json()
    organic = [
        {
            "title": r.get("title", ""),
            "link": r.get("link", ""),
            "snippet": r.get("snippet", ""),
        }
        for r in data.get("organic", [])
    ]
    out: dict[str, Any] = {"query": query, "organic": organic}
    if data.get("answerBox"):
        ab = data["answerBox"]
        out["answer_box"] = {
            "title": ab.get("title", ""),
            "answer": ab.get("answer") or ab.get("snippet", ""),
            "link": ab.get("link", ""),
        }
    if data.get("knowledgeGraph"):
        kg = data["knowledgeGraph"]
        out["knowledge_graph"] = {
            "title": kg.get("title", ""),
            "type": kg.get("type", ""),
            "description": kg.get("description", ""),
        }
    return out


def dispatch_tool(name: str, tool_input: dict[str, Any]) -> str:
    """Execute a tool call and return its result as a string for tool_result."""
    if name == "web_search":
        result = search_serper(
            query=tool_input["query"],
            num_results=int(tool_input.get("num_results", 10)),
        )
        return json.dumps(result, ensure_ascii=False)
    return json.dumps({"error": f"unknown tool: {name}"})


def research_cves(client: anthropic.Anthropic, incident: str) -> dict[str, Any]:
    """Run the agentic loop: Claude searches via SERPER until done, then reports."""
    messages: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": (
                f"Security incident:\n\n{incident}\n\n"
                "Find every CVE discussed on the Internet in connection with "
                "this incident. Show the source URL for each."
            ),
        }
    ]

    response: Any = None
    for turn in range(MAX_AGENT_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            thinking={"type": "adaptive"},
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            break

        tool_uses = [b for b in response.content if getattr(b, "type", None) == "tool_use"]
        messages.append({"role": "assistant", "content": response.content})

        tool_results: list[dict[str, Any]] = []
        for tu in tool_uses:
            print(
                f"      web_search: {tu.input.get('query', '')!r}",
                file=sys.stderr,
            )
            content = dispatch_tool(tu.name, tu.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": content,
                }
            )
        messages.append({"role": "user", "content": tool_results})
    else:
        print(
            f"      (hit MAX_AGENT_TURNS={MAX_AGENT_TURNS}; using report so far)",
            file=sys.stderr,
        )

    report_text = "".join(
        b.text for b in response.content if getattr(b, "type", None) == "text"
    )

    cve_to_urls: dict[str, set[str]] = {}
    for cve in CVE_PATTERN.findall(report_text):
        cve_to_urls.setdefault(cve.upper(), set())

    for chunk in re.split(r"\n\s*\n|\n", report_text):
        cves = {c.upper() for c in CVE_PATTERN.findall(chunk)}
        urls = URL_PATTERN.findall(chunk)
        for cve in cves:
            cve_to_urls.setdefault(cve, set()).update(urls)

    return {
        "report": report_text,
        "cves": {cve: sorted(urls) for cve, urls in cve_to_urls.items()},
        "stop_reason": response.stop_reason,
    }


def enrich_cve(cve_id: str) -> dict[str, Any]:
    try:
        resp = requests.get(
            NVD_API,
            params={"cveId": cve_id},
            timeout=15,
            headers={"User-Agent": "claude-cve/0.1"},
        )
    except requests.RequestException as e:
        return {"error": f"NVD request failed: {e}"}
    if resp.status_code != 200:
        return {"error": f"NVD returned HTTP {resp.status_code}"}

    vulns = resp.json().get("vulnerabilities", [])
    if not vulns:
        return {"error": "not found in NVD"}

    cve = vulns[0]["cve"]
    desc = next(
        (d["value"] for d in cve.get("descriptions", []) if d.get("lang") == "en"),
        "",
    )

    score, severity, version = None, None, None
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        entries = cve.get("metrics", {}).get(key)
        if entries:
            m = entries[0]
            cvss = m.get("cvssData", {})
            score = cvss.get("baseScore")
            severity = cvss.get("baseSeverity") or m.get("baseSeverity")
            version = key.removeprefix("cvssMetric")
            break

    return {
        "description": desc,
        "score": score,
        "severity": severity,
        "cvss_version": version,
        "published": cve.get("published"),
        "references": [r.get("url") for r in cve.get("references", [])[:8]],
    }


def slugify(text: str, max_len: int = 60) -> str:
    """Turn an incident description into a filesystem-safe slug."""
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or "incident"


def render_markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No CVEs found._"

    def cell(s: Any) -> str:
        return str(s).replace("|", "\\|").replace("\n", " ") if s not in (None, "") else "—"

    cve_w = max(len("CVE ID"), max(len(r["cve_id"]) for r in rows))
    header = "CVE ID".ljust(cve_w)
    lines = [
        f"| {header} | Score | Severity | Description |",
        f"|{'-' * (cve_w + 2)}|-------|----------|-------------|",
    ]
    for r in rows:
        cve_cell = cell(r["cve_id"]).ljust(cve_w).replace("-", "‑")
        lines.append(
            f"| {cve_cell} | {cell(r.get('score'))} | "
            f"{cell(r.get('severity'))} | {cell(r.get('description'))} |"
        )
    return "\n".join(lines)


def build_markdown_report(incident: str, rows: list[dict[str, Any]], report: str) -> str:
    return (
        f"# CVE Research: {incident}\n\n"
        f"**Generated:** {date.today().isoformat()}\n\n"
        "## CVE Summary\n\n"
        f"{render_markdown_table(rows)}\n\n"
        "## Research Report\n\n"
        f"{report.strip()}\n"
    )


def render_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No CVEs found."

    headers = ("CVE ID", "Score", "Severity", "Description")

    def short_desc(r: dict[str, Any]) -> str:
        d = r.get("description") or ""
        return (d[:117] + "...") if len(d) > 120 else d

    cve_w = max(len(headers[0]), max(len(r["cve_id"]) for r in rows))
    score_w = max(len(headers[1]), 5)
    sev_w = max(len(headers[2]), 8)
    desc_w = max(len(headers[3]), max((len(short_desc(r)) for r in rows), default=0))

    def fmt(a: str, b: str, c: str, d: str) -> str:
        return f"{a:<{cve_w}}  {b:<{score_w}}  {c:<{sev_w}}  {d:<{desc_w}}"

    out = [
        fmt(*headers),
        fmt("-" * cve_w, "-" * score_w, "-" * sev_w, "-" * desc_w),
    ]
    for r in rows:
        score = "" if r.get("score") is None else str(r["score"])
        out.append(fmt(r["cve_id"], score, r.get("severity") or "", short_desc(r)))
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("incident", help="Description of the security incident")
    parser.add_argument(
        "--json",
        dest="json_path",
        help="Write full results (report + enriched CVEs + sources) to this JSON path",
    )
    parser.add_argument(
        "--markdown",
        dest="markdown_path",
        nargs="?",
        const="__auto__",
        default=None,
        help=(
            "Write a markdown report (CVE table + research summary). "
            "Pass a path to use it directly, or omit the value to auto-name "
            "the file as <incident-slug>-<YYYY-MM-DD>.md in the cwd."
        ),
    )
    parser.add_argument(
        "--no-enrich",
        action="store_true",
        help="Skip NVD enrichment (faster, no descriptions/scores)",
    )
    args = parser.parse_args()

    missing = [k for k in ("ANTHROPIC_API_KEY", "SERPER_API_KEY") if not os.environ.get(k)]
    if missing:
        print(f"error: missing env var(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    client = anthropic.Anthropic()

    print(f"[1/2] Researching: {args.incident!r}", file=sys.stderr)
    research = research_cves(client, args.incident)
    cve_ids = sorted(research["cves"].keys())
    print(
        f"      Found {len(cve_ids)} CVE(s): {', '.join(cve_ids) or '(none)'}",
        file=sys.stderr,
    )

    rows: list[dict[str, Any]] = []
    for i, cve_id in enumerate(cve_ids, 1):
        row: dict[str, Any] = {
            "cve_id": cve_id,
            "sources": research["cves"][cve_id],
        }
        if not args.no_enrich:
            print(f"[2/2] Enriching {cve_id} ({i}/{len(cve_ids)})", file=sys.stderr)
            row.update(enrich_cve(cve_id))
            time.sleep(0.7)  # NVD throttles anonymous clients to ~5 req / 30s
        rows.append(row)

    print()
    print(render_table(rows))
    print()
    print("--- Research summary ---")
    print(research["report"].strip())

    if args.json_path:
        with open(args.json_path, "w") as f:
            json.dump(
                {
                    "incident": args.incident,
                    "report": research["report"],
                    "cves": rows,
                },
                f,
                indent=2,
                default=str,
            )
        print(f"\n[output] Wrote full results to {args.json_path}", file=sys.stderr)

    if args.markdown_path:
        md_path = args.markdown_path
        if md_path == "__auto__":
            md_path = f"{slugify(args.incident)}-{date.today().isoformat()}.md"
        with open(md_path, "w") as f:
            f.write(build_markdown_report(args.incident, rows, research["report"]))
        print(f"\n[output] Wrote markdown report to {md_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
