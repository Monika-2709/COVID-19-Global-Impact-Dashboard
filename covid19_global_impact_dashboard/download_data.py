"""
Download Our World in Data's public COVID-19 dataset.
Run: python download_data.py
Source: https://github.com/owid/covid-19-data/tree/master/public/data
"""
from pathlib import Path
import pandas as pd

URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
OUT = Path(__file__).parent / "data" / "owid-covid-data.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)
print("Downloading public OWID COVID-19 data (large CSV; requires internet)...")
df = pd.read_csv(URL, low_memory=False)
keep = [
    "iso_code", "continent", "location", "date", "population",
    "new_cases", "total_cases", "new_deaths", "total_deaths",
    "people_vaccinated", "people_fully_vaccinated",
    "total_vaccinations", "new_vaccinations_smoothed",
]
df = df[[c for c in keep if c in df.columns]]
df.to_csv(OUT, index=False)
print(f"Saved {len(df):,} rows to {OUT}")
