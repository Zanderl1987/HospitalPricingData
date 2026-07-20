[README.md](https://github.com/user-attachments/files/30173196/README.md)
# HospitalPricingData# HospitalPricingData

Research repository for CMS Hospital Price Transparency data collection and analysis.

## Overview

The CMS Hospital Price Transparency Rule (CMS-1717-F2, effective January 1, 2021) requires all U.S. hospitals to publish machine-readable files (MRFs) of their standard charges. This repository contains:

- **Authoritative hospital universe** from CMS (5,432 Medicare-certified hospitals)
- **Enforcement tracking data** (11,440+ actions, 28 CMPs issued)
- **Research documentation** on existing data collection projects
- **Data collection scripts** for downloading and processing CMS datasets

## Repository Structure

```
HospitalPricingData/
├── data/
│   ├── cms_hospital_general_information.csv    # 5,432 hospitals, 38 fields
│   └── cms_enforcement_actions_q1_2026.csv     # 11,440 enforcement actions
├── research/
│   ├── HOSPITAL_PRICE_TRANSPARENCY_RESEARCH.md # Comprehensive landscape analysis
│   ├── SESSION_NOTES.md                        # Session-by-session research log
│   ├── download_data.py                        # CMS data downloader
│   └── DATA_DICTIONARY.md                      # Field definitions & MRF format reference
├── CONTRIBUTING.md
├── requirements.txt
└── .gitignore
```

## Quick Start

```bash
# Clone and setup
git clone https://github.com/Zanderl1987/HospitalPricingData.git
cd HospitalPricingData
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Download latest CMS data
cd research && python download_data.py

# View hospital summary
python -c "
import pandas as pd
df = pd.read_csv('../data/cms_hospital_general_information.csv')
print(f'Total hospitals: {len(df)}')
print(df['Hospital Type'].value_counts())
"
```

## Data Sources

| Dataset | Source | Records | Updated | License |
|---------|--------|---------|---------|---------|
| Hospital General Information | [CMS Provider Data Catalog](https://data.cms.gov/provider-data/dataset/xubh-q36u) | 5,432 | Quarterly | Public Domain |
| Enforcement Actions Q1 2026 | [CMS Enforcement Data](https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/hospital-price-transparency-enforcement-activities-and-outcomes) | 11,440 | Quarterly | Public Domain |

### Hospital Universe Breakdown

| Hospital Type | Count |
|---------------|-------|
| Acute Care Hospitals | 3,115 |
| Critical Access Hospitals | 1,378 |
| Psychiatric | 635 |
| VA Hospitals | 132 |
| Children's Hospitals | 94 |
| Rural Emergency Hospitals | 41 |
| DoD Hospitals | 32 |
| Long-term Care | 5 |

## Research Findings Summary

### Existing MRF Collection Projects

| Project | Coverage | Approach | License | Status |
|---------|----------|----------|---------|--------|
| [TPAFS/transparency-data](https://github.com/TPAFS/transparency-data) | ~7,199 URLs | Community-curated CSV | CC-BY-SA 4.0 | Stale (~2022) |
| [nathansutton/hospital-price-transparency](https://github.com/nathansutton/hospital-price-transparency) | 5,000+ hospitals | Self-healing scraper (Claude AI) | Open source | Active |
| [PricePortal (IUPUI)](https://github.com/iupui-soic/mrf-pricing-research) | 528 hospitals (CA+IN) | Academic pipeline | Zenodo/CC-BY | Static |
| [Trilliant Health/ORIA](https://oria-data.trillianthealth.com) | 7,643 files, 6,000+ hospitals | Commercial DuckDB lake | Commercial | Active |

### Key Challenges

1. **No centralized MRF directory** — CMS requires publication but doesn't aggregate URLs
2. **URL volatility** — Hospitals change file locations without notice
3. **WAF blocking** — Major hospital websites block automated access (Cloudflare, Akamai)
4. **Format inconsistency** — Despite CMS templates, many use custom formats (XLSX, custom CSV)
5. **Scale** — Full MRF corpus ~2+ TB (7.29B negotiated rates per Trilliant)

### Recommended Collection Strategy

1. **Start with nathansutton's URL registry** (`dim/urls/{state}.json`) — most complete, self-healing
2. **Cross-reference with TPAFS** for broader coverage (~7,199 vs ~5,000)
3. **Validate via HTTP HEAD** before downloading
4. **Parse with multi-format support** — CSV tall/wide, JSON 2.x/3.x, XML 3.x
5. **Normalize to common schema** — CPT/HCPCS/DRG, price type, amount, payer

## Data Dictionary

See [`research/DATA_DICTIONARY.md`](research/DATA_DICTIONARY.md) for:
- CMS Hospital General Information field definitions
- Enforcement action code meanings
- MRF format specifications (CMS standard + observed variants)
- Required data elements per CMS-1717-F2

## Regulation Reference

| Resource | Link |
|----------|------|
| CMS Price Transparency Hub | <https://cms.gov/priorities/key-initiatives/hospital-price-transparency> |
| Final Rule (CMS-1717-F2) | <https://federalregister.gov/d/2020-24569> |
| Technical Specifications | <https://github.com/CMSgov/hospital-price-transparency> |
| MRF Templates | <https://github.com/CMSgov/price-transparency-guide> |
| Enforcement Data | <https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/hospital-price-transparency-enforcement-activities-and-outcomes> |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style (ruff, type hints)
- Adding new data sources
- Research documentation standards
- Data ethics guidelines

## License

- Code: MIT License
- Data: Public domain (U.S. government works) / CC-BY-SA where noted
- Research docs: CC-BY-4.0

## Citation

If you use this data in research, please cite:

```
HospitalPricingData: CMS Hospital Price Transparency Research Repository
GitHub: https://github.com/Zanderl1987/HospitalPricingData
Data sources: CMS Provider Data Catalog, CMS Enforcement Activities
```

## Related Work

- [TPAFS/transparency-data](https://github.com/TPAFS/transparency-data) — MRF URL registry
- [nathansutton/hospital-price-transparency](https://github.com/nathansutton/hospital-price-transparency) — Self-healing scraper
- [PricePortal (IUPUI)](https://doi.org/10.5281/zenodo.19941038) — CA+IN academic dataset
- [CMS Price Transparency GitHub](https://github.com/CMSgov/hospital-price-transparency) — Official templates & specs
