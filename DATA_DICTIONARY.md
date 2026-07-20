# Data Dictionary

## `data/cms_hospital_general_information.csv`

Source: [CMS Provider Data Catalog - Hospital General Information](https://data.cms.gov/provider-data/dataset/xubh-q36u)

### Fields (38 columns)

| Column | Type | Description |
|--------|------|-------------|
| `Facility ID` | string | CMS Certification Number (CCN) — 6-digit unique identifier |
| `Facility Name` | string | Hospital legal name |
| `Address` | string | Street address |
| `City/Town` | string | City |
| `State` | string | 2-letter state code |
| `ZIP Code` | string | 5-digit ZIP |
| `County/Parish` | string | County name |
| `Telephone Number` | string | Phone (format: (XXX) XXX-XXXX) |
| `Hospital Type` | string | Classification (see table below) |
| `Hospital Ownership` | string | Ownership category (see table below) |
| `Emergency Services` | string | "Yes" / "No" |
| `Meets criteria for birthing friendly designation` | string | "Y" / "N" / empty |
| `Hospital overall rating` | int | 1–5 star rating (empty = not available) |
| `Hospital overall rating footnote` | string | Footnote code for rating |
| `MORT Group Measure Count` | int | Mortality measure group count |
| `Count of Facility MORT Measures` | int | Number of mortality measures reported |
| `Count of MORT Measures Better` | int | Measures better than national rate |
| `Count of MORT Measures No Different` | int | Measures not different from national |
| `Count of MORT Measures Worse` | int | Measures worse than national rate |
| `MORT Group Footnote` | string | Footnote for mortality group |
| `Safety Group Measure Count` | int | Safety measure group count |
| `Count of Facility Safety Measures` | int | Number of safety measures reported |
| `Count of Safety Measures Better` | int | Safety measures better than national |
| `Count of Safety Measures No Different` | int | Safety measures not different |
| `Count of Safety Measures Worse` | int | Safety measures worse than national |
| `Safety Group Footnote` | string | Footnote for safety group |
| `READM Group Measure Count` | int | Readmission measure group count |
| `Count of Facility READM Measures` | int | Number of readmission measures |
| `Count of READM Measures Better` | int | Readmission measures better |
| `Count of READM Measures No Different` | int | Readmission measures not different |
| `Count of READM Measures Worse` | int | Readmission measures worse |
| `READM Group Footnote` | string | Footnote for readmission group |
| `Pt Exp Group Measure Count` | int | Patient experience measure group count |
| `Count of Facility Pt Exp Measures` | int | Number of patient experience measures |
| `Pt Exp Group Footnote` | string | Footnote for patient experience |
| `TE Group Measure Count` | int | Timely & Effective Care measure group count |
| `Count of Facility TE Measures` | int | Number of timely/effective measures |
| `TE Group Footnote` | string | Footnote for TE group |

### Hospital Type Values

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

### Hospital Ownership Values

| Ownership | Example |
|-----------|---------|
| Government - Hospital District or Authority | Public hospital districts |
| Government - Federal | VA, DoD, IHS |
| Government - Local | County/city hospitals |
| Government - State | State university hospitals |
| Proprietary | For-profit (HCA, Tenet, etc.) |
| Tribal | IHS/Tribal facilities |
| Voluntary non-profit - Church | Faith-based non-profits |
| Voluntary non-profit - Other | Secular non-profits |
| Voluntary non-profit - Private | Other non-profits |

---

## `data/cms_enforcement_actions_q1_2026.csv`

Source: [CMS Hospital Price Transparency Enforcement Activities](https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/hospital-price-transparency-enforcement-activities-and-outcomes)

### Fields

| Column | Type | Description |
|--------|------|-------------|
| `Facility ID` | string | CMS Certification Number (CCN) |
| `Facility Name` | string | Hospital name |
| `State` | string | 2-letter state |
| `Action Type` | string | Enforcement action category (see below) |
| `Action Date` | date | Date action was taken (YYYY-MM-DD) |
| `Status` | string | Current status of action |
| `Details` | string | Additional details |

### Action Type Values

| Action Type | Count | Description |
|-------------|-------|-------------|
| `Met Requirements` | 3,340 | Hospital found compliant |
| `Closure Notice` | 3,225 | Review closed without penalty |
| `Warning Notice` | 2,993 | Initial non-compliance notice |
| `Corrective Action Plan (CAP) Request` | 1,751 | Required to submit CAP |
| `Civil Monetary Penalty (CMP) Notice` | 28 | Formal penalty assessment |

### Notes

- 11,440 total actions across 4,988 unique review cases
- Multiple actions per hospital possible
- CMP maximum: $5,500/day for hospitals with >550 beds
- Data as of Q1 2026 (January–March 2026 enforcement cycle)

---

## MRF File Format Reference (External)

Not in this repo, but relevant for parsing:

### CMS Standard Formats

| Format | Version | Structure |
|--------|---------|-----------|
| CSV | 2.0 / 3.0 | Tall (long) or Wide (payer columns) |
| JSON | 2.0 / 3.0 | Nested objects per item/service |
| XML | 3.0 | Structured equivalent of JSON 3.0 |

### Required Data Elements (per CMS-1717-F2)

- Gross charge
- Payer-specific negotiated charge (payer + plan name)
- De-identified minimum negotiated charge
- De-identified maximum negotiated charge
- Discounted cash price
- Billing code (CPT, HCPCS, DRG, NDC, etc.)
- Code type
- Setting (inpatient/outpatient/both)

### Naming Convention

```
{ein}_{hospital-name}_standardcharges.{json|csv|xml}
```

Example: `363617578_Langdon-Prairie-Health_standardcharges.csv`

### Required Root Metadata File

```
{hospital-location-name}
{source-page-URL}
{MRF-file-URL}
{point-of-contact}
```