# Hospital Price Transparency Research

## Executive Summary

The CMS Hospital Price Transparency Rule (CMS-1717-F2), effective January 1, 2021, requires all
hospitals operating in the United States to publish machine-readable files (MRFs) of their standard
charges. As of 2026, there are ~5,000-7,600 hospitals in the US depending on inclusion criteria.
Multiple open-source projects and commercial entities have already begun collecting these files,
but no single authoritative, centralized source exists. The data is fragmented, inconsistent in
format, and frequently changes location.

---

## 1. The Regulation

**Rule:** CMS-1717-F2 (45 CFR Part 180)
**Effective:** January 1, 2021
**Enforcement:** CMS + HHS
**Key Requirements:**

- Every hospital must publish a **Machine-Readable File (MRF)** containing ALL standard charges
  for ALL items and services (chargemaster-level data)
- Must also publish **300 shoppable services** in consumer-friendly format (or provide a price
  estimator tool)
- File must be: publicly accessible, free, no login/PII required, digitally searchable
- File naming convention: `{ein}_{hospital-name}_standardcharges.{json|csv|xml}`
- Must include a `.txt` file in root folder with MRF URL metadata (as of Jan 1, 2024)
- Must include "Price Transparency" footer link on homepage (as of Jan 1, 2024)

**Data Elements Required:**
- Gross charges
- Payer-specific negotiated charges (with payer + plan name)
- De-identified minimum negotiated charge
- De-identified maximum negotiated charge
- Discounted cash price
- Billing codes (CPT, HCPCS, DRG, NDC, etc.)
- Setting (inpatient/outpatient)

**Enforcement (as of March 2026):**
- 11,440 total enforcement actions across 4,988 unique review cases
- 28 Civil Monetary Penalties (CMPs) issued
- Up to $5,500/day penalty for large hospitals
- 2025 was peak enforcement year: 5,432 actions
- CMS enforcement data available at: `data.cms.gov/provider-characteristics/hospitals-and-other-facilities/hospital-price-transparency-enforcement-activities-and-outcomes`

---

## 2. Hospital Universe

### Authoritative Source: CMS Provider Data Catalog

| Source | URL | Count | Notes |
|--------|-----|-------|-------|
| **CMS Hospital General Information** | `data.cms.gov/provider-data/dataset/xubh-q36u` | **5,432** | Medicare-certified only. Includes addresses, phone, type, quality rating. Updated quarterly. |
| **TPAFS/transparency-data hospitals.csv** | `github.com/TPAFS/transparency-data` | **~7,004** | Broader universe. Includes non-Medicare hospitals. Has bed count, lat/lon, EIN. |
| **Trilliant Health/ORIA MRF Directory** | `oria-data.trillianthealth.com` | **7,643** | Files tracked (not unique hospitals). 2.04 TB total data volume. |

### Hospital Types in CMS Dataset (5,432 total)

| Type | Count |
|------|-------|
| Acute Care Hospitals | 3,115 |
| Critical Access Hospitals | 1,378 |
| Psychiatric | 635 |
| Acute Care - Veterans Administration | 132 |
| Childrens | 94 |
| Rural Emergency Hospital | 41 |
| Acute Care - Department of Defense | 32 |
| Long-term | 5 |

### CMS Dataset Fields (38 fields)

Core: Facility ID, Name, Address, City, State, ZIP, County, Phone
Classification: Hospital Type, Ownership, Emergency Services, Birthing Friendly
Quality: Overall Rating (1-5), Mortality, Safety, Readmission, Patient Experience, Timely & Effective Care

---

## 3. Existing Data Collection Projects

### 3.1 TPAFS/transparency-data (Open Source, Persius Foundation)

**URL:** `github.com/TPAFS/transparency-data`
**License:** CC-BY-SA-4.0 (data), Apache 2.0 (code)
**What they have:**
- `machine_readable_links.csv`: ~7,199 hospital entries with MRF URLs
- `hospitals.csv`: ~7,004 hospitals with metadata (CCN, address, bed count, EIN, lat/lon)
- Coverage: All 50 states + DC + territories

**MRF URL Status:**
| Format | Count |
|--------|-------|
| CSV | ~1,399 |
| XLSX | ~1,051 (non-compliant format) |
| JSON | ~352 |
| Other | ~291 |
| XML | ~36 |

**Key Insight:** Many entries have EMPTY `machine_readable_url` fields -- hospitals where the MRF
URL is known to exist but could not be publicly identified. Data was last significantly updated ~2022.

**Limitations:** No Python scripts, no scrapers, no automated collection. Manual community
contributions via GitHub PRs. No automated URL health monitoring.

### 3.2 nathansutton/hospital-price-transparency (Open Source)

**URL:** `github.com/nathansutton/hospital-price-transparency`
**Coverage:** 5,000+ hospitals across all 50 states
**Approach:** Git-scraping with self-healing via Claude AI

**Key Architecture:**
- URL registry in `dim/urls/{state}.json` (51 files, one per state)
- Sources URLs from `hospitalpricingfiles.org` (external browser scraper)
- Format-specific scrapers: CMSStandardCSVScraper, CMSStandardJSONScraper, etc.
- Daily validation + auto-fix pipeline using Claude Code CLI
- Output: `data/{STATE}/{CCN}.jsonl` with normalized price records

**URL Patterns Observed:**
- Direct file hosting: `hospital.org/wp-content/uploads/..._standardcharges.csv`
- Third-party hosting: `sthpiprd.blob.core.windows.net` (Hospital Price Index)
- CDN hosting: `claraprice.net`, `craneware.com`, `panaceainc.com`
- Many hospitals serve files from unexpected paths

**Self-Healing Mechanism:**
1. Daily validation catches broken URLs (404/403)
2. `fix_broken_urls.py` scrapes hospital transparency pages for new links
3. Claude AI analyzes failures and finds replacement URLs
4. Changes go through PR review before merge
5. Daily PR limit of 5 to prevent runaway automation

### 3.3 PricePortal (Academic, IUPUI)

**URL:** `github.com/iupui-soic/mrf-pricing-research`
**Coverage:** 528 hospitals in California + Indiana
**Dataset:** 6.42 GB on Zenodo (DOI: 10.5281/zenodo.19941038)

**Pipeline:**
1. `build_hospital_list.py` - Pulls CMS data, filters to target states
2. `discover_mrf_urls.py` - Per-host crawl + filename validation
3. `download_mrfs.py` - Per-host rate-limited downloader (~72 GB total for CA+IN)
4. `parse_mrf.py` - Multi-format parser into unified parquet

**Key Finding:** Median chargemaster-to-Medicare ratio is 3.92x in CA vs 2.19x in IN.

### 3.4 Trilliant Health / ORIA (Commercial)

**URL:** `oria-data.trillianthealth.com`
**Coverage:** 7,643 files, 6,000+ hospitals
**Data Volume:** 2.04 TB, 7.29 billion negotiated rates
**Format:** DuckDB data lake + web search + AI chatbot (Oria)

**MRF File Type Distribution:**
| Format | Count |
|--------|-------|
| Tall CSV 3.x | 3,609 |
| Wide CSV 3.x | 1,311 |
| Tall CSV 2.x | 305 |
| Wide CSV 2.x | 219 |
| JSON 3.x | 1,954 |
| JSON 2.x | 68 |

**Note:** This is a commercial product. Free DuckDB shell available on their site, but full
data download requires contacting them.

### 3.5 hospitalpricingfiles.org (Patient Rights Advocate)

**URL:** `hospitalpricingfiles.org`
**Maintained by:** Patient Rights Advocate (nonprofit)
**What it does:** Aggregates MRF links for all hospitals. JavaScript-rendered app (not scrapable
without headless browser). Used as primary URL source by nathansutton project.

### 3.6 githubbar/hospital-price-transparency

**URL:** `github.com/githubbar/hospital-price-transparency`
**Approach:** Downloads MRFs from hospitalpricingfiles.org API, normalizes into SQLite
**Focus:** Indiana hospitals, shoppable services extraction
**Tools:** Django web app, SQLite database, shoppable code filtering

---

## 4. Accessibility Analysis: What We Actually Found

### 4.1 Direct MRF File Access

**Finding:** Direct MRF file URLs are accessible via HTTP GET without authentication.

**Example (successful):**
- `https://lph.hospital/wp-content/uploads/2026/05/363617578_Langdon-Prairie-Health_standardcharges.csv`
- Returns CSV directly (5MB+), no login required
- Follows CMS naming convention

**File sizes range from:**
- 210 bytes (empty/minimal) to 7.7 GB (St Joseph Mercy Ann Arbor)
- Most are 10-500 MB

### 4.2 Hospital Website Access

**Finding:** Major hospital websites BLOCK automated access (webfetch/browser).

| Hospital | Result |
|----------|--------|
| Mayo Clinic | 403 Forbidden |
| Cleveland Clinic | 404 Not Found |
| Johns Hopkins | 403 Forbidden |
| Mass General | 404 Not Found |
| Stanford Children's | 404 Not Found |

**Pattern:** Large hospital systems use CDN/WAF protection (Cloudflare, Akamai) that blocks
non-browser requests. The MRF files themselves are often hosted on separate infrastructure
(CDNs, blob storage) that may not have the same protections.

### 4.3 Discovery Challenges

1. **No centralized directory:** CMS does not maintain a list of MRF URLs
2. **URL instability:** Hospitals change file locations without notice
3. **Hidden placement:** MRF links are often buried in website footers or subpages
4. **Format inconsistency:** Despite CMS naming convention, many hospitals use non-standard names
5. **XLSX non-compliance:** ~1,051 hospitals serve Excel files (not machine-readable per CMS)
6. **Third-party hosting:** Many hospitals outsource to vendors (Craneware, Panacea, etc.)

---

## 5. Data Source Vetting Summary

| Source | Status | Access Model | Rate Limits | Data Quality | Recommendation |
|--------|--------|--------------|-------------|--------------|----------------|
| CMS Hospital General Information | **GO** | Public API + CSV download | None (government data) | High (authoritative) | **PRIMARY** - Use for hospital universe |
| CMS Enforcement Data | **GO** | Public CSV downloads | None | High | **SUPPLEMENTARY** - Compliance tracking |
| TPAFS/transparency-data | **GO** | GitHub (CC-BY-SA) | GitHub rate limits | Medium (stale ~2022) | **PRIMARY** - Best existing MRF URL list |
| nathansutton MRF URLs | **GO** | GitHub (open source) | GitHub rate limits | High (self-healing) | **PRIMARY** - Most complete URL registry |
| hospitalpricingfiles.org | **PARTIAL** | JS-rendered app | Unknown | High | **SUPPLEMENTARY** - URL source |
| Trilliant Health/ORIA | **NO-GO** | Commercial | Unknown | Very High | **REFERENCE** - Too expensive for now |
| PricePortal (Zenodo) | **GO** | Zenodo download | None | High (academic) | **REFERENCE** - CA+IN only |
| Direct hospital websites | **FRAGILE** | Varies | WAF blocks common | Low (inconsistent) | **LAST RESORT** - For gap-filling |

---

## 6. Recommended Approach for Data Collection

### Phase 1: Build Hospital Universe (Week 1)
1. Download CMS Hospital General Information CSV (5,432 hospitals)
2. Cross-reference with TPAFS `hospitals.csv` (7,004 hospitals) for broader coverage
3. Merge datasets on CCN/Facility ID
4. Output: Unified hospital list with CCN, name, address, type, website domain

### Phase 2: Collect MRF URLs (Week 1-2)
1. Clone TPAFS/transparency-data and extract `machine_readable_links.csv`
2. Clone nathansutton/hospital-price-transparency and extract `dim/urls/*.json`
3. Merge URL sources, deduplicate on CCN
4. Flag hospitals with no known MRF URL
5. Output: Hospital-to-MRF-URL mapping

### Phase 3: Validate & Download MRFs (Week 2-3)
1. HTTP HEAD check all known MRF URLs
2. For broken URLs, attempt discovery via:
   - CMS naming convention on known hospital domains
   - `hospitalpricingfiles.org` API
   - Hospital transparency page scraping (with headless browser)
3. Download accessible MRFs
4. Output: Local archive of MRF files

### Phase 4: Parse & Normalize (Week 3-4)
1. Multi-format parser (CSV tall/wide, JSON 2.x/3.x, XML)
2. Normalize to common schema (CPT code, description, price type, amount)
3. Cross-reference with Medicare fee schedules
4. Output: Unified pricing database

### Key Risks
- **URL churn:** MRF URLs change frequently; need ongoing validation
- **WAF blocking:** Some hospital sites block automated access
- **Format variance:** Despite CMS templates, many hospitals use custom formats
- **File size:** Some MRFs are 7+ GB; need chunked downloading
- **Legal:** Review ToS for hospitalpricingfiles.org and any aggregator sites

---

## 7. File Naming Convention (CMS Standard)

```
{ein}_{hospital-name}_standardcharges.{json|csv|xml}
```

**Example:**
```
81-4791043_santa-rosa-memorial-hospital_standardcharges.json
363617578_Langdon-Prairie-Health_standardcharges.csv
```

**Required .txt file in root:**
```
{hospital-location-name}
{source-page-URL}
{MRF-file-URL}
{point-of-contact}
```

---

## 8. Key URLs

| Resource | URL |
|----------|-----|
| CMS Price Transparency Hub | `cms.gov/priorities/key-initiatives/hospital-price-transparency` |
| CMS Hospital General Information | `data.cms.gov/provider-data/dataset/xubh-q36u` |
| CMS Enforcement Actions | `data.cms.gov/provider-characteristics/hospitals-and-other-facilities/hospital-price-transparency-enforcement-activities-and-outcomes` |
| CMS Technical Specs (GitHub) | `github.com/CMSgov/hospital-price-transparency` |
| CMS MRF Templates | `github.com/CMSgov/price-transparency-guide` |
| TPAFS/transparency-data | `github.com/TPAFS/transparency-data` |
| nathansutton scraper | `github.com/nathansutton/hospital-price-transparency` |
| PricePortal (Zenodo) | `doi.org/10.5281/zenodo.19941038` |
| hospitalpricingfiles.org | `hospitalpricingfiles.org` |
| Trilliant Health ORIA | `oria-data.trillianthealth.com` |
| Fonteum enforcement analysis | `fonteum.com/research/hospital-price-transparency-compliance-2026` |
