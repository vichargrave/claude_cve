# CVE Research: Amazon Threat Intelligence identifies Russian cyber threat group targeting Western critical infrastructure

**Generated:** 2026-04-27

## CVE Summary

| CVE ID         | Score | Severity | Description |
|----------------|-------|----------|-------------|
| CVE-2021-26084 | 9.8 | CRITICAL | In affected versions of Confluence Server and Data Center, an OGNL injection vulnerability exists that would allow an unauthenticated attacker to execute arbitrary code on a Confluence Server or Data Center instance. The affected versions are before version 6.13.23, from version 6.14.0 before 7.4.11, from version 7.5.0 before 7.11.6, and from version 7.12.0 before 7.12.5. |
| CVE-2022-26318 | 9.8 | CRITICAL | On WatchGuard Firebox and XTM appliances, an unauthenticated user can execute arbitrary code, aka FBX-22786. This vulnerability impacts Fireware OS before 12.7.2_U2, 12.x before 12.1.3_U8, and 12.2.x through 12.5.x before 12.5.9_U2. |
| CVE-2023-22518 | 9.8 | CRITICAL | All versions of Confluence Data Center and Server are affected by this unexploited vulnerability. This Improper Authorization vulnerability allows an unauthenticated attacker to reset Confluence and create a Confluence instance administrator account. Using this account, an attacker can then perform all administrative actions that are available to Confluence instance administrator leading to - but not limited to - full loss of confidentiality, integrity and availability.   Atlassian Cloud sites are not affected by this vulnerability. If your Confluence site is accessed via an atlassian.net domain, it is hosted by Atlassian and is not vulnerable to this issue. |
| CVE-2023-27532 | 7.5 | HIGH | Vulnerability in Veeam Backup & Replication component allows encrypted credentials stored in the configuration database to be obtained. This may lead to gaining access to the backup infrastructure hosts. |
| CVE-2024-21827 | 7.2 | HIGH | A leftover debug code vulnerability exists in the cli_server debug functionality of Tp-Link ER7206 Omada Gigabit VPN Router 1.4.1 Build 20240117 Rel.57421. A specially crafted series of network requests can lead to arbitrary command execution. An attacker can send a sequence of requests to trigger this vulnerability. |

## Research Report

I have sufficient and consistent information across multiple sources. Here is my report:

# Report: Amazon Threat Intelligence — Russian Cyber Threat Group Targeting Western Critical Infrastructure

## Summary
On December 15, 2025, Amazon Threat Intelligence (CISO CJ Moses) published a report disclosing a years-long (2021–2025) Russian state-sponsored cyber campaign attributed with high confidence to a GRU-linked threat cluster overlapping with **Sandworm / APT44 / Seashell Blizzard** (Russia's Main Intelligence Directorate, GRU). The campaign targeted Western critical infrastructure — particularly energy, electric utilities, water/waste, and other ICS-adjacent sectors — using compromise of customer-owned, misconfigured network edge devices (including some hosted on AWS) for credential harvesting, persistence, and lateral movement.

Key narrative reported across sources:
- 2021–2022: Exploitation of **WatchGuard Firebox/XTM** appliances (detected via Amazon's MadPot honeypot system) plus targeting of misconfigured edge devices.
- 2022–2023: Exploitation of **Atlassian Confluence** flaws.
- 2024: Exploitation of **Veeam Backup & Replication**.
- 2025: Tactical shift away from CVE exploitation toward **abuse of misconfigurations, weak SNMPv1/v2 community strings, exposed management interfaces, and outdated/unpatched edge devices**, including unpatched Cisco Smart Install issues.
Amazon stated it disrupted active operations and reduced the attack surface for this subcluster.

## CVEs Discussed in Connection With the Incident

1. **CVE-2022-26318** — Pre-authentication RCE in **WatchGuard Firebox / XTM** appliances; exploited 2021–2022 and detected by Amazon's MadPot honeypot system as the initial vector for the campaign.
   - https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-russian-cyber-threat-group-targeting-western-critical-infrastructure/
   - https://thehackernews.com/2025/12/amazon-exposes-years-long-gru-cyber.html
   - https://www.securityweek.com/amazon-russian-hackers-now-favor-misconfigurations-in-critical-infrastructure-attacks/
   - https://cyberscoop.com/amazon-threat-intel-russia-attacks-energy-sector-sandworm-apt44/
   - https://industrialcyber.co/industrial-cyber-attacks/russian-gru-hackers-target-network-edge-devices-in-sustained-energy-and-critical-infrastructure-attacks/
   - https://www.theregister.com/2025/12/15/amazon_ongoing_gru_campaign/

2. **CVE-2021-26084** — OGNL injection RCE in **Atlassian Confluence Server / Data Center**; exploited 2022–2023 phase of the campaign.
   - https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-russian-cyber-threat-group-targeting-western-critical-infrastructure/
   - https://thehackernews.com/2025/12/amazon-exposes-years-long-gru-cyber.html
   - https://therecord.media/russia-gru-hackers-target-energy-sector-sandworm
   - https://www.infosecurity-magazine.com/news/amazon-russian-gru-hackers-target/
   - https://www.darkreading.com/endpoint-security/russian-apt-attacking-critical-orgs-around-world

3. **CVE-2023-22518** — Improper authorization vulnerability in **Atlassian Confluence Data Center / Server**; exploited alongside CVE-2021-26084 during the 2022–2023 phase.
   - https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-russian-cyber-threat-group-targeting-western-critical-infrastructure/
   - https://www.theregister.com/2025/12/15/amazon_ongoing_gru_campaign/
   - https://www.infosecurity-magazine.com/news/amazon-russian-gru-hackers-target/
   - https://www.secureworld.io/industry-news/russian-sandworm-hackers-misconfigurations
   - https://thehackernews.com/2025/12/amazon-exposes-years-long-gru-cyber.html

4. **CVE-2023-27532** — Credential-disclosure flaw in **Veeam Backup & Replication**; exploited during the 2024 phase of the campaign before the actor pivoted to misconfiguration-based access.
   - https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-russian-cyber-threat-group-targeting-western-critical-infrastructure/
   - https://www.infosecurity-magazine.com/news/amazon-russian-gru-hackers-target/
   - https://www.secureworld.io/industry-news/russian-sandworm-hackers-misconfigurations
   - https://www.secpod.com/blog/aws-intelligence-report-gru-linked-hackers-behind-sustained-infrastructure-attacks/

## Notes
- These four CVEs (CVE-2022-26318, CVE-2021-26084, CVE-2023-22518, CVE-2023-27532) are the only specific CVE identifiers cited in the AWS advisory and in all secondary reporting I reviewed.
- Reporting also references unpatched **Cisco Smart Install** abuse and SNMPv1/v2 weaknesses, but these are described as misconfiguration/legacy-protocol issues rather than tied to a specific CVE in the context of this Amazon report.
- Some downstream commentary (e.g., a Hacker News/Facebook post) mentions CVE-2024-21827 (TP-Link), but this is not attributed by Amazon to this campaign — it appears in a general "edge device" discussion thread, not in the AWS report itself, so it is **not included** as an incident-related CVE.

**Primary source:** https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-russian-cyber-threat-group-targeting-western-critical-infrastructure/
