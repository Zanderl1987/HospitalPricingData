# Contributing to HospitalPricingData

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/HospitalPricingData.git`
3. Create a feature branch: `git checkout -b feature/your-feature`

## Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Data Download Script

```bash
cd research
python download_data.py
```

This downloads:
- CMS Hospital General Information (~1.4 MB)
- CMS Enforcement Actions Q1 2026 (~1 MB)

## Code Style

- Python: Follow PEP 8, use type hints
- Run `ruff check .` and `ruff format .` before committing
- Docstrings for public functions (Google/NumPy style)

## Adding New Data Sources

1. **Verify licensing** — Confirm data is public domain, CC0, CC-BY, or similar
2. **Document source** — Add to `DATA_DICTIONARY.md` with URL, fields, license
3. **Add download logic** — Extend `download_data.py` or create new script
4. **Update README** — Add to data sources table

## Research Documentation

- Update `research/HOSPITAL_PRICE_TRANSPARENCY_RESEARCH.md` for major findings
- Add session notes to `research/SESSION_NOTES.md` with date and summary
- Use the experiment writeup skill for formal analyses: `/skill experiment-writeup`

## Pull Request Process

1. Ensure `ruff check .` passes
2. Update relevant documentation
3. Add tests for new functionality (if applicable)
4. Request review

## Data Ethics

- Only collect publicly available data (CMS rule requires MRFs to be free, no-login)
- Respect `robots.txt` and rate limits
- Don't redistribute hospital-owned MRF files without verifying license
- Document all sources and licenses in `DATA_DICTIONARY.md`

## Questions?

Open an issue for discussion before large changes.