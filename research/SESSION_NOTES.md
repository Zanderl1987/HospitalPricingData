# Session Notes — Hospital Price Transparency Research

**Date:** 2026-07-11
**Goal:** Research hospital pricing data landscape under CMS Price Transparency Rule

---

## What We Did

### 1. Researched the Regulation
- CMS-1717-F2 (45 CFR Part 180), effective January 1, 2021
- Requires ALL US hospitals to publish machine-readable files (MRFs) of standard charges
- 2024 updates: mandatory CMS template format, .txt metadata file in root, footer link requirement
- 2026 updates: enforcement of new template requirements started April 1, 2026
- Enforcement data: 11,440 actions, 28 CMPs issued, $5,500/day max penalty

### 2. Downloaded Authoritative Hospital List
- **Source:** CMS Provider Data Catalog (`data.cms.gov/provider-data/dataset/xubh-q36u`)
- **File:** `data/cms_hospital_general_information.csv` (1.4 MB, 5,432 hospitals)
- **Fields:** 38 columns — Facility ID, Name, Address, City, State, ZIP, County, Phone, Hospital Type, Ownership, Quality Ratings, Mortality/Safety/Readmission measures
- **Breakdown:** 3,115 acute care, 1,378 critical access, 635 psychiatric, 132 VA, 94 children's, 41 rural emergency, 32 DoD, 5 long-term

### 3. Downloaded Enforcement Data
- **Source:** CMS Enforcement Activities dataset
- **File:** `data/cms_enforcement_actions_q1_2026.csv` (1 MB, 11,440 actions)
- **Key stats:** 3,340 "Met Requirements", 3,225 Closure Notices, 2,993 Warning Notices, 1,751 CAP Requests, 28 CMP Notices
- **Top enforcement states:** TX (1,175), CA (970), FL (686), OH (414), PA (409)

### 4. Identified Existing Data Collection Projects
- **TPAFS/transparency-data** — Best open MRF URL registry (~7,199 hospitals), CC-BY-SA, Rust validator, but stale (~2022), no scrapers
- **nathansutton/hospital-price-transparency** — Self-healing scraper using Claude AI, 5,000+ hospitals, git-scraping, daily validation + auto-fix pipeline
- **PricePortal (IUPUI)** — Academic pipeline for CA+IN (528 hospitals), 6.42 GB Zenodo corpus
- **Trilliant Health/ORIA** — Commercial DuckDB data lake, 7,643 files, 2.04 TB, 7.29B negotiated rates
- **hospitalpricingfiles.org** — Patient Rights Advocate nonprofit aggregator (JS-rendered, used as URL source by nathansutton)
- **githubbar/hospital-price-transparency** — Indiana-focused, SQLite database, shoppable services extraction

### 5. Probed Hospital Websites
- Mayo Clinic, Cleveland Clinic, Johns Hopkins, Mass General, Stanford Children's — all returned 403/404 to automated requests
- Smaller hospitals (e.g., Langdon Prairie Health) served MRF files directly without WAF blocking
- **Key finding:** Direct MRF file URLs on CDN/blob storage are accessible; hospital main websites are not

### 6. Analyzed MRF File Formats
- CMS naming convention: `{ein}_{hospital-name}_standardcharges.{json|csv|xml}`
- TPAFS data: CSV (~1,399), XLSX (~1,051, non-compliant), JSON (~352), Other (~291), XML (~36)
- ORIA/Trilliant data: Tall CSV 3.x (3,609), JSON 3.x (1,954), Wide CSV 3.x (1,311)
- File sizes: 210 bytes to 7.7 GB

---

## Key Data Sources (URLs)

| Resource | URL |
|----------|-----|
| CMS Hospital General Information | `data.cms.gov/provider-data/dataset/xubh-q36u` |
| CMS Enforcement Actions | `data.cms.gov/provider-characteristics/hospitals-and-other-facilities/hospital-price-transparency-enforcement-activities-and-outcomes` |
| CMS Price Transparency Hub | `cms.gov/priorities/key-initiatives/hospital-price-transparency` |
| CMS Technical Specs | `github.com/CMSgov/hospital-price-transparency` |
| CMS MRF Templates | `github.com/CMSgov/price-transparency-guide` |
| TPAFS/transparency-data | `github.com/TPAFS/transparency-data` |
| nathansutton scraper | `github.com/nathansutton/hospital-price-transparency` |
| PricePortal (Zenodo) | `doi.org/10.5281/zenodo.19941038` |
| hospitalpricingfiles.org | `hospitalpricingfiles.org` |
| Trilliant Health ORIA | `oria-data.trillianthealth.com` |

---

## Files Created This Session

```
HospitalPricingData/
├── data/
│   ├── cms_hospital_general_information.csv    (1.4 MB, 5,432 hospitals)
│   └── cms_enforcement_actions_q1_2026.csv     (1 MB, 11,440 actions)
└── research/
    ├── HOSPITAL_PRICE_TRANSPARENCY_RESEARCH.md  (full research document)
    ├── download_data.py                         (data collection script)
    └── SESSION_NOTES.md                         (this file)
```

---

## What's Verified vs. Unverified

### Verified
- CMS hospital list downloads and contains 5,432 records with expected fields
- CMS enforcement data downloads and contains 11,440 records
- Direct MRF file URLs are accessible via HTTP GET (tested Langdon Prairie Health CSV)
- TPAFS/transparency-data repo exists and has ~7,199 MRF URL entries
- nathansutton repo exists and has 5,000+ hospital URLs across 50 states

### Unverified
- Whether TPAFS MRF URLs are still live (data from ~2022, likely many stale)
- Whether nathansutton's URL JSON files can be downloaded and used directly
- Whether hospitalpricingfiles.org has an accessible API (site requires JavaScript)
- Whether the CMS naming convention discovery approach (guessing URLs from EIN + name) works at scale
- How the nathansutton Claude auto-fix pipeline performs in practice
- Whether Trilliant Health offers any free/bulk data access

---

## Next Session Priorities

1. **Clone TPAFS/transparency-data** and analyze `machine_readable_links.csv` — count live vs dead URLs, identify coverage gaps
2. **Clone nathansutton/hospital-price-transparency** and extract `dim/urls/*.json` — these are the most complete URL registry
3. **Merge URL sources** with CMS hospital list on CCN/Facility ID
4. **HTTP HEAD validation** of all known MRF URLs
5. **Prototype a small-scale downloader** — pick one state, download all MRFs, measure sizes and formats
6. **Prototype a parser** — handle CSV tall/wide, JSON 2.x/3.x formats at minimum

---

## Blockers / Open Questions

- **No centralized MRF URL directory from CMS** — this is the core problem. The rule requires hospitals to publish but CMS doesn't aggregate the URLs.
- **WAF/CDN blocking** — major hospital sites block automated access. Need headless browser for discovery phase, but direct MRF file URLs on separate infrastructure are often accessible.
- **Format variance** — despite CMS templates, many hospitals use custom formats. Parser needs to handle significant edge cases.
- **Python not available on this machine** via standard paths — need to figure out Python environment or use PowerShell for scripting.
- **Scale** — MRFs total 2+ TB. Downloading and parsing all of them is a multi-day effort requiring significant storage.
