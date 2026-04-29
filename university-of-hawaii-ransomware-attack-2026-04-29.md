# CVE Research: University of Hawaii ransomware attack

**Generated:** 2026-04-29

## CVE Summary

_No CVEs found._

## Research Report

I have enough information to compose a final report.

# Report: University of Hawaii Ransomware Attack — CVE Search

## Incident Summary

The most widely reported "University of Hawaii ransomware attack" refers to a **ransomware attack on the University of Hawaiʻi Cancer Center's Epidemiology Division**, discovered on or around **August 31, 2025** and publicly disclosed in late 2025 / early 2026. An unauthorized third party encrypted systems and exfiltrated data tied to long-running cancer research studies (some data going back to 1993). The university confirmed that personal information — including names, Social Security numbers, dates of birth, and driver's license / state ID information — for approximately **1.15–1.24 million individuals** was compromised. UH reportedly engaged with the attackers, and disclosure was delayed for several months, prompting governance and notification-timeline criticism.

Sources covering the incident include:
- https://www.hawaii.edu/news/2026/02/27/notice-of-cyberattack-uh-cancer-center/
- https://hawaii.edu/cancercenter/incident/
- https://www.bleepingcomputer.com/news/security/university-of-hawaii-cancer-center-hit-by-ransomware-attack/
- https://www.bleepingcomputer.com/news/security/university-of-hawaii-cancer-center-ransomware-attack-affects-nearly-12-million-people/
- https://www.securityweek.com/1-2-million-affected-by-university-of-hawaii-cancer-center-data-breach/
- https://therecord.media/university-of-hawaii-ransomware-data-breach
- https://www.hipaajournal.com/university-of-hawaii-cancer-center-ransomware-data-breach/
- https://www.bankinfosecurity.com/cancer-center-research-study-hack-affects-12m-a-30912
- https://www.civilbeat.org/2026/01/uh-engaged-with-hackers-who-highjacked-cancer-study-data/
- https://www.rescana.com/post/university-of-hawaii-cancer-center-ransomware-attack-data-breach-delayed-notification-and-cyberse

(Note: A separate, earlier event — the **2023 Hawaiʻi Community College ransomware attack by the NoEscape gang** — also matches "University of Hawaii ransomware." It is covered at https://thecyberexpress.com/hawaii-community-college-ransomware-attack/ and https://research.checkpoint.com/2023/31st-july-threat-intelligence-report/. No CVEs were tied to that incident either.)

## CVEs Associated with the Incident

**No CVE identifiers have been publicly attributed to either the 2025 UH Cancer Center ransomware attack or the 2023 Hawaiʻi Community College ransomware attack.**

- The TechJack Solutions intelligence write-up explicitly states: *"No specific CVE has been publicly attributed. No patch is applicable, this is an operational security failure, not a software vulnerability exploit."*
  - Source: https://techjacksolutions.com/scc-intel/university-of-hawaii-cancer-center-ransomware-attack-exposes-1-2-million-records/
- No vendor advisory, university statement, government breach notice, or mainstream news reporting (BleepingComputer, SecurityWeek, The Record, BankInfoSecurity, HIPAA Journal, Civil Beat, Paubox, NetSec.news) names a CVE used for initial access, lateral movement, or encryption.
- The threat actor / ransomware family behind the UH Cancer Center attack has not been publicly identified, which is consistent with the absence of any disclosed exploited vulnerability.

### Caveat — incidental CVE mentions in the same articles (NOT linked to this incident)

A few aggregator/news-roundup pages mention CVEs in proximity to coverage of the UH attack, but these are unrelated stories appearing on the same blog index pages. For completeness:

- **CVE-2026-32746** — A critical unpatched GNU InetUtils telnetd RCE flaw. It appears on the same Rescana blog index page as the UH article but is a **separate, unrelated story**, not an exploit used in the UH attack.
  - Source (index page where both stories co-occur): https://www.rescana.com/blog and https://www.rescana.com/post/university-of-hawaii-cancer-center-ransomware-attack-data-breach-delayed-notification-and-cyberse

## Bottom Line

After a thorough search across vendor advisories, breach-notification news outlets, threat-intel blogs, university statements, and aggregator sites, **no CVE has been publicly discussed as the vulnerability behind the University of Hawaii (Cancer Center, 2025) ransomware attack** — and likewise none for the earlier Hawaiʻi Community College (NoEscape, 2023) ransomware attack. The only CVEs that appear "near" the incident in search results are unrelated items co-listed on the same news-aggregation pages.
