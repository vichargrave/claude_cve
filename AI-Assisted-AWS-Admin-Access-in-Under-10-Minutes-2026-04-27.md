# CVE Research: AI-Assisted AWS Admin Access in Under 10 Minutes

**Generated:** 2026-04-27

## CVE Summary

| CVE ID         | Score | Severity | Description |
|----------------|-------|----------|-------------|
| CVE-2022-40684 | 9.8 | CRITICAL | An authentication bypass using an alternate path or channel [CWE-288] in Fortinet FortiOS version 7.2.0 through 7.2.1 and 7.0.0 through 7.0.6, FortiProxy version 7.2.0 and version 7.0.0 through 7.0.6 and FortiSwitchManager version 7.2.0 and 7.0.0 allows an unauthenticated atttacker to perform operations on the administrative interface via specially crafted HTTP or HTTPS requests. |
| CVE-2024-21762 | 9.8 | CRITICAL | A out-of-bounds write in Fortinet FortiOS versions 7.4.0 through 7.4.2, 7.2.0 through 7.2.6, 7.0.0 through 7.0.13, 6.4.0 through 6.4.14, 6.2.0 through 6.2.15, 6.0.0 through 6.0.17, FortiProxy versions 7.4.0 through 7.4.2, 7.2.0 through 7.2.8, 7.0.0 through 7.0.14, 2.0.0 through 2.0.13, 1.2.0 through 1.2.13, 1.1.0 through 1.1.6, 1.0.0 through 1.0.7 allows attacker to execute unauthorized code or commands via specifically crafted requests |
| CVE-2025-22225 | 8.2 | HIGH | VMware ESXi contains an arbitrary write vulnerability. A malicious actor with privileges within the VMX process may trigger an arbitrary kernel write leading to an escape of the sandbox. |
| CVE-2025-8088  | 8.8 | HIGH | A path traversal vulnerability affecting the Windows version of WinRAR allows the attackers to execute arbitrary code by crafting malicious archive files. This vulnerability was exploited in the wild and was discovered by Anton Cherepanov, Peter Košinár, and Peter Strýček      from ESET. |
| CVE-2026-33017 | 9.8 | CRITICAL | Langflow is a tool for building and deploying AI-powered agents and workflows. In versions prior to 1.9.0, the POST /api/v1/build_public_tmp/{flow_id}/flow endpoint allows building public flows without requiring authentication. When the optional data parameter is supplied, the endpoint uses attacker-controlled flow data (containing arbitrary Python code in node definitions) instead of the stored flow data from the database. This code is passed to exec() with zero sandboxing, resulting in unauthenticated remote code execution. This is distinct from CVE-2025-3248, which fixed /api/v1/validate/code by adding authentication. The build_public_tmp endpoint is designed to be unauthenticated (for public flows) but incorrectly accepts attacker-supplied flow data containing arbitrary executable code. This issue has been fixed in version 1.9.0. |

## Research Report

## Research Report: AI-Assisted AWS Admin Access in Under 10 Minutes

### Summary of the Incident

The article at https://cybersecuritynews.com/aws-admin-access-in-minutes/ reports on an incident originally documented by the **Sysdig Threat Research Team (TRT)** on **November 28, 2025**. Key facts publicly reported:

- A threat actor obtained **exposed AWS credentials from publicly accessible S3 buckets** and used **AI/LLM tooling (reportedly Claude)** to automate reconnaissance, generate malicious code, and chain privilege escalations.
- The adversary moved from initial access to **full AWS administrative privileges in roughly 8 minutes**, compromising **19 distinct AWS principals**.
- The post-exploitation activity abused **AWS Lambda** (code execution / role pivoting), **IAM** (over-permissive roles), and **Amazon Bedrock** models (LLMjacking-style abuse).
- The story has been widely echoed by Dark Reading, eSecurityPlanet, CSO Online, Hackread, Security Boulevard, GBHackers, Vectra AI, and The Hacker News.

Sources:
- https://cybersecuritynews.com/aws-admin-access-in-minutes/
- https://www.sysdig.com/blog/ai-assisted-cloud-intrusion-achieves-admin-access-in-8-minutes
- https://www.darkreading.com/cloud-security/8-minute-access-ai-aws-environment-breach
- https://www.csoonline.com/article/4126336/from-credentials-to-cloud-admin-in-8-minutes-ai-supercharges-aws-attack-chain.html
- https://hackread.com/8-minute-takeover-ai-hijack-cloud-access/
- https://www.esecurityplanet.com/threats/ai-driven-attack-gains-aws-admin-privileges-in-under-10-minutes/

### CVEs Associated with the Incident

**No CVEs are associated with this incident.**

After multiple targeted searches across the original Sysdig blog, the cybersecuritynews.com article, and secondary coverage in mainstream security press, none of the publications reference any CVE identifier in connection with this attack. This is consistent with the nature of the breach: it was **not a vulnerability-exploitation incident** but rather an abuse of:

- Publicly exposed long-lived AWS credentials (a misconfiguration/credential-hygiene issue),
- Over-permissive IAM roles,
- Legitimate AWS service features (Lambda execution, Bedrock model invocation),
- AI/LLM tooling used by the attacker for automation.

This conclusion is independently corroborated by automated CVE-extraction services that ingested the Sysdig report:

- TI-Mindmap report on the Sysdig article: **"0 CVE(s) referenced"** — https://ti-mindmap-hub.com/preview/report/3c7422e5-65bc-4fb8-9241-9058f69a8adb
- Rösti CTI repackager on the same article: **"No CVE found"** — https://rosti.dev/reports/xlcZjy9H

Note: Some weekly-newsletter / LinkedIn pages link to the cybersecuritynews.com article alongside unrelated stories that mention CVEs (e.g., CVE-2025-22225 for ESXi, CVE-2025-8088 for WinRAR, CVE-2024-21762 / CVE-2022-40684 for FortiOS, CVE-2026-33017 for Langflow). Those CVEs are **not** discussed in connection with the AWS/Sysdig incident itself; they appear only as adjacent items in roundup posts and should not be attributed to this incident.
