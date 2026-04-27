# SolarWinds Orion Supply-Chain Attack — CVE Research

**Generated:** 2026-04-27
**Incident:** SolarWinds Orion supply-chain attack

## CVE Summary Table

| CVE ID         | Score | Severity | Description |
|----------------|-------|----------|-------------|
| CVE-2020-10148 | 9.8 | CRITICAL | The SolarWinds Orion API is vulnerable to an authentication bypass that could allow a remote attacker to execute API commands. |
| CVE-2020-13169 | 9.0 | CRITICAL | Stored XSS (Cross-Site Scripting) exists in the SolarWinds Orion Platform before 2020.2.1 on multiple forms and pages. |
| CVE-2020-14005 | 8.8 | HIGH | SolarWinds Orion (with Web Console WPM 2019.4.1, and Orion Platform HF4 or NPM HF2 2019.4) allows remote attackers to execute arbitrary code via Visual Basic scripts. |
| CVE-2020-27869 | 8.8 | HIGH | Remote attackers can escalate privileges on affected installations of SolarWinds Network Performance Monitor via SQL injection. |
| CVE-2020-27870 | 6.5 | MEDIUM | Remote attackers can disclose sensitive information on affected installations of SolarWinds Orion. |
| CVE-2020-35856 | 4.8 | MEDIUM | SolarWinds Orion Platform before 2020.2.5 allows stored XSS attacks by an administrator on the Customize View page. |
| CVE-2020-4006  | 9.1 | CRITICAL | VMware Workspace ONE Access, Access Connector, Identity Manager, and Identity Manager Connector command-injection vulnerability. |
| CVE-2021-25274 | 9.8 | CRITICAL | The Collector Service in SolarWinds Orion Platform before 2020.2.4 uses MSMQ (Microsoft Message Queue) and doesn't securely deserialize messages — RCE. |
| CVE-2021-25275 | 7.8 | HIGH | SolarWinds Orion Platform before 2020.2.4 installs and uses a SQL Server backend with insecurely stored credentials. |
| CVE-2021-25276 | 7.1 | HIGH | In SolarWinds Serv-U before 15.2.2 Hotfix 1, a directory containing user profile files (including users' password hashes) has weak ACLs. |
| CVE-2021-3109  | 4.8 | MEDIUM | The custom menu item options page in SolarWinds Orion Platform before 2020.2.5 allows Reverse Tabnabbing. |
| CVE-2021-31474 | — | — | Insecure-deserialization RCE in SolarWinds NPM (no NVD enrichment returned). |
| CVE-2021-31475 | — | — | RCE in Orion Job Scheduler via insecure deserialization (no NVD enrichment returned). |
| CVE-2021-35211 | — | — | Memory-escape RCE in SolarWinds Serv-U SSH (no NVD enrichment returned). |

---

# Report: SolarWinds Orion Supply‑Chain Attack — Related CVEs

## Summary of the Incident

In December 2020, FireEye (Mandiant) and Microsoft disclosed a sophisticated supply‑chain compromise of **SolarWinds' Orion network‑management platform**. A nation‑state actor — later attributed to Russia's SVR (APT29 / "Cozy Bear" / "UNC2452" / "Nobelium") — compromised the Orion build pipeline and inserted a backdoor known as **SUNBURST / Solorigate** into a digitally‑signed update of `SolarWinds.Orion.Core.BusinessLayer.dll` between roughly March and June 2020. The trojanized update was distributed to ~18,000 customers, with follow‑on intrusions ("hands‑on‑keyboard") at high‑value targets including the U.S. Departments of Treasury, Commerce, State, Energy, Homeland Security, FireEye/Mandiant, Microsoft, Mimecast and others.

A second, distinct .NET web shell called **SUPERNOVA** (attributed to a separate actor, "SPIRAL") was found on Orion servers, dropped via an Orion API authentication‑bypass flaw. Investigators also identified follow‑on tools (TEARDROP, RAINDROP, GoldMax, Sibot, GoldFinder, Sunshuttle) and Golden‑SAML / token‑forgery activity to pivot into Microsoft 365 tenants. Subsequent vulnerability‑research attention also produced several additional Orion CVEs unrelated to the original backdoor itself but disclosed in the same window.

---

## CVEs Discussed in Connection with the Incident

### Directly tied to the SolarWinds/Orion compromise

- **CVE‑2020‑10148** – SolarWinds Orion API authentication bypass that allowed remote attackers to execute API commands; the vulnerability used to install the **SUPERNOVA** web shell on Orion servers.
  https://nvd.nist.gov/vuln/detail/CVE-2020-10148
  https://attack.mitre.org/software/S0578/
  https://threatprotect.qualys.com/2020/12/30/supernova-solarwinds-orion-api-authentication-bypass-vulnerability-cve-2020-10148/
  https://www.ibm.com/docs/en/randori?topic=2022-solarwinds-orion-cve-2020-10148

- **CVE‑2020‑14005** – Authenticated RCE in Orion Web Console via arbitrary Visual Basic scripts; explicitly linked by Trend Micro and ZDI to the SUNBURST campaign.
  https://nvd.nist.gov/vuln/detail/CVE-2020-14005
  https://www.thezdi.com/blog/2021/1/20/three-bugs-in-orions-belt-chaining-multiple-bugs-for-unauthenticated-rce-in-the-solarwinds-orion-platform
  https://www.trendmicro.com/en_us/research/20/l/overview-of-recent-sunburst-targeted-attacks.html

- **CVE‑2020‑13169** – Stored XSS in multiple Orion forms/pages; called out alongside CVE‑2020‑14005 in incident‑response advisories about the Orion compromise.
  https://nvd.nist.gov/vuln/detail/CVE-2020-13169
  https://access.redhat.com/solutions/5661671
  https://cert.europa.eu/publications/security-advisories/2020-060/

- **CVE‑2020‑27869** – SQL‑injection privilege escalation in Orion (NPM 2020 HF1, Orion Platform 2020.2.1) — disclosed by ZDI as part of the post‑SUNBURST "Three Bugs in Orion's Belt" research and chained for unauthenticated RCE.
  https://www.thezdi.com/blog/2021/1/20/three-bugs-in-orions-belt-chaining-multiple-bugs-for-unauthenticated-rce-in-the-solarwinds-orion-platform
  https://www.cve.org/CVERecord?id=CVE-2020-27869

- **CVE‑2020‑27870** – Information‑disclosure in Orion 2020.2.1 (chained with the bugs above); disclosed by ZDI in the same SUNBURST‑era research.
  https://nvd.nist.gov/vuln/detail/CVE-2020-27870
  https://www.thezdi.com/blog/2021/1/20/three-bugs-in-orions-belt-chaining-multiple-bugs-for-unauthenticated-rce-in-the-solarwinds-orion-platform

- **CVE‑2020‑35856** – Stored XSS in Orion's Customize View page; patched in the same set of Orion fixes following the breach.
  https://nvd.nist.gov/vuln/detail/CVE-2020-35856
  https://securityaffairs.com/115983/security/solarwinds-updates-rce.html

- **CVE‑2021‑3109** – Reverse‑tabnabbing/open‑redirect in Orion custom menu items, patched alongside critical Orion RCE fixes after the breach.
  https://www.cve.org/CVERecord?id=CVE-2021-3109
  https://thehackernews.com/2021/03/solarwinds-orion-vulnerability.html
  https://www.rapid7.com/blog/post/2021/03/29/solarwinds-patches-four-new-vulnerabilities-in-their-orion-platform/

- **CVE‑2021‑25274** – Critical MSMQ/Collector‑service deserialization RCE in Orion, found by Trustwave during heightened post‑SUNBURST scrutiny.
  https://nvd.nist.gov/vuln/detail/cve-2021-25274
  https://thehackernews.com/2021/02/3-new-severe-security-vulnerabilities.html
  https://threatprotect.qualys.com/2021/02/04/solarwinds-full-system-control-vulnerabilities-cve-2021-25274-cve-2021-25275-cve-2021-25276/

- **CVE‑2021‑25275** – Local privilege escalation in Orion (credential exposure), disclosed in the same Trustwave advisory series.
  https://thehackernews.com/2021/02/3-new-severe-security-vulnerabilities.html
  https://threatprotect.qualys.com/2021/02/04/solarwinds-full-system-control-vulnerabilities-cve-2021-25274-cve-2021-25275-cve-2021-25276/

- **CVE‑2021‑25276** – Privilege escalation in SolarWinds Serv‑U FTP (file ACL weakness); disclosed in the same Trustwave advisory cluster following the Orion breach.
  https://thehackernews.com/2021/02/3-new-severe-security-vulnerabilities.html
  https://its.ny.gov/2021-021

- **CVE‑2021‑31474** – Insecure‑deserialization RCE in SolarWinds NPM, disclosed via ZDI ("Three More Bugs in Orion's Belt").
  https://www.rapid7.com/db/vulnerabilities/solarwinds-orion_platform-cve-2021-31474/
  https://www.thezdi.com/blog/2021/2/11/three-more-bugs-in-orions-belt

- **CVE‑2021‑31475** – RCE in Orion Job Scheduler via insecure deserialization; ZDI's follow‑up Orion research.
  https://nvd.nist.gov/vuln/detail/CVE-2021-31475
  https://www.thezdi.com/blog/2021/2/11/three-more-bugs-in-orions-belt

- **CVE‑2021‑35211** – Memory‑escape RCE in SolarWinds Serv‑U SSH; while a separate 2021 zero‑day exploited by DEV‑0322/TA505, it is widely covered alongside SolarWinds Orion advisories and CISA's KEV catalog under the SolarWinds umbrella.
  https://nvd.nist.gov/vuln/detail/CVE-2021-35211
  https://www.tenable.com/blog/cve-2021-35211-solarwinds-serv-u-managed-file-transfer-zero-day-exploited-dev-0322
  https://blog.fox-it.com/2021/11/08/ta505-exploits-solarwinds-serv-u-vulnerability-cve-2021-35211-for-initial-access/

### Used by the same threat actor / discussed as a related vector

- **CVE‑2020‑4006** – Command‑injection in VMware Workspace ONE Access / Identity Manager. NSA/Krebs reporting tied this flaw to the SolarWinds attackers, who used it to forge SAML tokens and pivot — frequently described as a parallel/secondary vector in the same espionage campaign.
  https://nvd.nist.gov/vuln/detail/cve-2020-4006
  https://krebsonsecurity.com/2020/12/vmware-flaw-a-vector-in-solarwinds-breach/
  https://www.tenable.com/blog/cve-2020-4006-vmware-command-injection-flaw-exploited-by-russian-state-sponsored-threat-actors
  https://securityaffairs.com/112535/security/solarwinds-vmware-cisco.html

### Adjacent: FireEye Red‑Team tool theft (discovered while investigating SolarWinds)

The FireEye breach announcement (which led to discovery of SUNBURST) included countermeasures for **16 publicly known CVEs** that the stolen Red Team tools could weaponize. They are not vulnerabilities in Orion itself, but are routinely listed in SolarWinds/FireEye incident write‑ups. Per Qualys/Palo Alto Unit 42:

- **CVE‑2019‑11510** – Pulse Secure SSL VPN arbitrary file read
- **CVE‑2020‑1472** – "Zerologon" Netlogon EoP
- **CVE‑2018‑13379** – Fortinet FortiOS path traversal
- **CVE‑2018‑15961** – Adobe ColdFusion RCE
- **CVE‑2019‑0604** – Microsoft SharePoint RCE
- **CVE‑2019‑0708** – "BlueKeep" Microsoft RDP RCE
- **CVE‑2019‑11580** – Atlassian Crowd RCE
- **CVE‑2019‑19781** – Citrix ADC/Gateway RCE
- **CVE‑2020‑10189** – Zoho ManageEngine Desktop Central RCE
- **CVE‑2014‑1812** – Windows Group Policy Preferences password disclosure
- **CVE‑2020‑0688** – Microsoft Exchange RCE
- **CVE‑2016‑0167** – Microsoft Windows local privilege escalation
- **CVE‑2017‑11774** – Microsoft Outlook security‑feature bypass
- **CVE‑2018‑8581** – Microsoft Exchange privilege escalation
- **CVE‑2019‑8394** – Zoho ManageEngine ServiceDesk Plus arbitrary file upload
- **CVE‑2019‑3398** – Atlassian Confluence path traversal/RCE

Sources for the FireEye/SolarWinds 16‑CVE list:
https://blog.qualys.com/qualys-insights/2020/12/22/qualys-security-advisory-solarwinds-fireeye
https://success.qualys.com/support/s/article/000006470
https://unit42.paloaltonetworks.com/fireeye-red-team-tool-breach/
https://www.zscaler.com/blogs/security-research/zscaler-coverage-solarwinds-cyberattacks-and-fireeye-red-team-tools-theft

---

### Notes
- The trojanization of the Orion build itself was **never assigned a CVE** — it was a malicious code insertion, tracked instead as malware (SUNBURST/Solorigate, MITRE S0559) and as a campaign (MITRE C0024).
- The **single CVE most synonymous with the incident** is **CVE‑2020‑10148**, the Orion API authentication bypass leveraged to drop SUPERNOVA, and the only Orion CVE listed in CISA's KEV catalog as part of this incident: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- The **VMware CVE‑2020‑4006** is the most prominent non‑Orion CVE attributed to the same Russian threat actor in connection with this campaign.
