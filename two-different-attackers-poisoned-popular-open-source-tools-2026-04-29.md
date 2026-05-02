# CVE Research: Two different attackers poisoned popular open source tools

**Generated:** 2026-04-29

## CVE Summary

| CVE ID         | Score | Severity | Description |
|----------------|-------|----------|-------------|
| CVE‑2026‑33634 | 8.8 | HIGH | Trivy is a security scanner. On March 19, 2026, a threat actor used compromised credentials to publish a malicious Trivy v0.69.4 release, force-push 76 of 77 version tags in `aquasecurity/trivy-action` to credential-stealing malware, and replace all 7 tags in `aquasecurity/setup-trivy` with malicious commits. This incident is a continuation of the supply chain attack that began in late February 2026. Following the initial disclosure on March 1, credential rotation was performed but was not atomic (not all credentials were revoked simultaneously). The attacker could have use a valid token to exfiltrate newly rotated secrets during the rotation window (which lasted a few days). This could have allowed the attacker to retain access and execute the March 19 attack. Affected components include the `aquasecurity/trivy` Go / Container image version 0.69.4, the `aquasecurity/trivy-action` GitHub Action versions 0.0.1 – 0.34.2 (76/77), and the`aquasecurity/setup-trivy` GitHub Action versions 0.2.0 – 0.2.6, prior to the recreation of 0.2.6 with a safe commit. Known safe versions include versions 0.69.2 and 0.69.3 of the Trivy binary, version 0.35.0 of trivy-action, and version 0.2.6 of setup-trivy. Additionally, take other mitigations to ensure the safety of secrets. If there is any possibility that a compromised version ran in one's environment, all secrets accessible to affected pipelines must be treated as exposed and rotated immediately. Check whether one's organization pulled or executed Trivy v0.69.4 from any source. Remove any affected artifacts immediately. Review all workflows using `aquasecurity/trivy-action` or `aquasecurity/setup-trivy`. Those who referenced a version tag rather than a full commit SHA should check workflow run logs from March 19–20, 2026 for signs of compromise. Look for repositories named `tpcp-docs` in one's GitHub organization. The presence of such a repository may indicate that the fallback exfiltration mechanism was triggered and secrets were successfully stolen. Pin GitHub Actions to full, immutable commit SHA hashes, don't use mutable version tags. |
| CVE‑2026‑34841 | 9.8 | CRITICAL | Bruno is an open source IDE for exploring and testing APIs. Prior to 3.2.1, Bruno was affected by a supply chain attack involving compromised versions of the axios npm package, which introduced a hidden dependency deploying a cross-platform Remote Access Trojan (RAT). Users of @usebruno/cli who ran npm install between 00:21 UTC and ~03:30 UTC on March 31, 2026 may have been impacted. Upgrade to 3.2.1 |

## Research Report

# Security Incident Report: Two Different Attackers Poisoned Popular Open Source Tools

## Summary

The Register feature ["Two different attackers poisoned popular open source tools - and showed us the future of supply chain compromise"](https://www.theregister.com/2026/04/11/trivy_axios_supply_chain_attacks/) covers two unrelated supply‑chain compromises that occurred in March 2026 against widely‑used open source developer tooling:

1. **Trivy (Aqua Security) — TeamPCP campaign (March 19, 2026)**
   - The threat actor "TeamPCP" used a stolen credential to force‑push malicious commits to 75/76 (or 76/77, depending on source) version tags of `aquasecurity/trivy-action` and all 7 tags of `aquasecurity/setup-trivy`, plus published a malicious `trivy v0.69.4`. The injected code stole CI/CD secrets (AWS, GCP, Azure, GitHub PATs) from any workflow that ran the action.
   - The compromise cascaded into **Checkmarx KICS, LiteLLM, Telnyx, and Bitwarden CLI** ecosystems.
   - Tracked under **CVE-2026-33634** (CVSS 9.4) and added to CISA's KEV catalog.

2. **Axios npm (March 30–31, 2026)**
   - A different, unrelated attacker (attributed by Google TIG/UNC1069 reporting to North Korean activity, separate from TeamPCP) hijacked the npm account of axios maintainer "jasonsaayman" via a stolen long‑lived npm token and published trojanized versions `axios@1.14.1` and `axios@0.30.4` containing a malicious dependency `plain-crypto-js@4.2.1` that delivered a cross‑platform RAT.
   - The Axios package compromise itself was not assigned a CVE (it's an account takeover, not a code flaw), but the downstream impact on the Bruno API IDE (`@usebruno/cli`) was tracked as **CVE-2026-34841**.

## CVEs Discussed in Connection With the Incident

| CVE | Relation to incident | Source(s) |
|-----|----------------------|-----------|
| **CVE‑2026‑33634** | **Attributed.** Embedded malicious code in Aqua Security Trivy / `trivy-action` / `setup-trivy` — the actual vulnerability ID assigned to the TeamPCP Trivy supply‑chain compromise. CVSS 9.4, added to CISA KEV. | https://access.redhat.com/security/vulnerabilities/RHSB-2026-001 ; https://github.com/advisories/GHSA-69fq-xp46-6x23 ; https://www.helpnetsecurity.com/2026/03/27/cve-2026-33017-cve-2026-33634-exploited/ ; https://thehackernews.com/2026/04/openai-revokes-macos-app-certificate.html ; https://www.rapid7.com/db/vulnerabilities/trivy-cve-2026-33634/ |
| **CVE‑2026‑34841** | **Attributed (downstream).** Tracks the impact of the malicious Axios `1.14.1`/`0.30.4` packages on Bruno CLI (`@usebruno/cli`) — i.e., the Axios npm supply‑chain compromise as recorded against an affected consumer. The Axios package compromise itself received no separate CVE. | https://nvd.nist.gov/vuln/detail/CVE-2026-34841 ; https://github.com/usebruno/bruno/security/advisories/GHSA-658g-p7jg-wx5g ; https://www.endorlabs.com/vulnerability/cve-2026-34841 ; https://cve.circl.lu/vuln/cve-2026-34841 |
| CVE-2025-30066 | **Background only — NOT attributed.** This is the earlier (March 2025) `tj-actions/changed-files` GitHub Actions supply‑chain attack. Multiple write‑ups cite it as the precedent / pattern that the 2026 Trivy attack mimicked, but it is not the exploited vulnerability in this incident. | https://snyk.io/articles/trivy-github-actions-supply-chain-compromise/ ; https://medium.com/@jbpoley/the-security-scanner-turned-spy-github-actions-supply-chain-attacks-and-the-fix-that-works-19ddf3107593 |
| CVE-2026-40175 | **Co‑occurring, NOT attributed.** A separate prototype‑pollution / CRLF "gadget chain" bug in Axios. Aikido and others explicitly note it is unrelated to (and not exploitable in the same way as) the March 2026 supply‑chain compromise. | https://www.aikido.dev/blog/axios-cve-2026-40175-a-critical-bug-thats-not-exploitable |
| CVE-2026-33017 | **Co‑occurring, NOT attributed.** Langflow code‑injection RCE listed alongside CVE-2026-33634 in CISA / Help Net Security alerts; unrelated to the Trivy/Axios attacks. | https://www.helpnetsecurity.com/2026/03/27/cve-2026-33017-cve-2026-33634-exploited/ |
| CVE-2025-30154 | **Background only — NOT attributed.** The reviewdog upstream compromise that fed into tj-actions in 2025; cited only as historical context for cascading supply‑chain attacks. | https://www.cloudsek.com/blog/the-scanner-was-the-weapon-36-months-of-precision-supply-chain-attacks-against-devsecops-infrastructure |

## Final attributed list
