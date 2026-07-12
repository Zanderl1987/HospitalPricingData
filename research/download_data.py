"""
Hospital Price Transparency - Data Collection Starter Script

Downloads:
1. CMS Hospital General Information (authoritative hospital list)
2. TPAFS MRF URL registry (best existing MRF URL collection)
3. CMS Enforcement Actions data
"""

import urllib.request
import csv
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def download_file(url: str, dest: Path, desc: str = ""):
    """Download a file with progress indication."""
    print(f"Downloading {desc or url}...")
    try:
        urllib.request.urlretrieve(url, dest)
        size_mb = dest.stat().st_size / (1024 * 1024)
        print(f"  -> {dest.name} ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def download_cms_hospital_list():
    """Download the CMS Hospital General Information CSV."""
    url = (
        "https://data.cms.gov/provider-data/sites/default/files/"
        "resources/893c372430d9d71a1c52737d01239d47_1777413958/"
        "Hospital_General_Information.csv"
    )
    dest = DATA_DIR / "cms_hospital_general_information.csv"
    return download_file(url, dest, "CMS Hospital General Information")


def download_cms_enforcement():
    """Download the latest CMS enforcement actions CSV."""
    url = (
        "https://data.cms.gov/sites/default/files/2026-04/"
        "9430fe24-3b59-4b87-ab73-18aa391fcde6/"
        "Hospital_Price_Transparency_Enforcement_Activities_and_Outcomes_Q1_2026.csv"
    )
    dest = DATA_DIR / "cms_enforcement_actions_q1_2026.csv"
    return download_file(url, dest, "CMS Enforcement Actions Q1 2026")


def summarize_hospital_list():
    """Summarize the downloaded hospital list."""
    csv_path = DATA_DIR / "cms_hospital_general_information.csv"
    if not csv_path.exists():
        print("Hospital list not downloaded yet.")
        return

    print("\n=== CMS Hospital List Summary ===")
    hospitals = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hospitals.append(row)

    print(f"Total hospitals: {len(hospitals)}")

    # By type
    types = {}
    for h in hospitals:
        t = h.get("Hospital Type", "Unknown")
        types[t] = types.get(t, 0) + 1
    print("\nBy Type:")
    for t, count in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")

    # By state
    states = {}
    for h in hospitals:
        s = h.get("State", "Unknown")
        states[s] = states.get(s, 0) + 1
    print(f"\nStates covered: {len(states)}")
    top_states = sorted(states.items(), key=lambda x: -x[1])[:10]
    print("Top 10 states:")
    for s, count in top_states:
        print(f"  {s}: {count}")

    # Sample fields
    if hospitals:
        print(f"\nSample fields: {list(hospitals[0].keys())}")


if __name__ == "__main__":
    print("=" * 60)
    print("Hospital Price Transparency - Data Collection")
    print("=" * 60)

    download_cms_hospital_list()
    download_cms_enforcement()
    summarize_hospital_list()

    print("\n" + "=" * 60)
    print("Next steps:")
    print("  1. Clone TPAFS/transparency-data for MRF URLs")
    print("  2. Clone nathansutton/hospital-price-transparency for MRF URLs")
    print("  3. Merge URL sources with CMS hospital list")
    print("  4. Validate and download MRF files")
    print("=" * 60)
