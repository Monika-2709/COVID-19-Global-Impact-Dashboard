"""Reproducible data cleaning and summary workflow for the COVID dashboard."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent
real = ROOT / "data" / "owid-covid-data.csv"
demo = ROOT / "data" / "covid_demo_data.csv"
source = real if real.exists() else demo
df = pd.read_csv(source, low_memory=False)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
numeric = ["population","new_cases","total_cases","new_deaths","total_deaths",
           "people_vaccinated","people_fully_vaccinated","total_vaccinations","new_vaccinations_smoothed"]
for col in numeric:
    if col not in df:
        df[col] = pd.NA
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["date","location"]).copy()
# Documented cleaning: negative daily revisions are set to zero for daily charts;
# missing values remain missing (not replaced with zero) because missing != no cases.
for col in ["new_cases","new_deaths"]:
    df[col] = df[col].clip(lower=0)
df["cases_per_million"] = df["total_cases"] / df["population"] * 1_000_000
df["deaths_per_million"] = df["total_deaths"] / df["population"] * 1_000_000
df["fully_vaccinated_pct"] = (df["people_fully_vaccinated"] / df["population"] * 100).clip(upper=100)
df = df.sort_values(["location","date"])
df["new_cases_7d_avg"] = df.groupby("location")["new_cases"].transform(lambda s: s.rolling(7, min_periods=1).mean())
out = ROOT / "outputs"
out.mkdir(exist_ok=True)
df.to_csv(out / "cleaned_covid_data.csv", index=False)
latest = df.sort_values("date").groupby("location", as_index=False).tail(1)
latest[["location","date","population","total_cases","total_deaths","cases_per_million","deaths_per_million","fully_vaccinated_pct"]].to_csv(out / "country_latest_summary.csv", index=False)
print(f"Source: {source.name}")
print(f"Cleaned rows: {len(df):,}")
print(f"Countries/regions: {df['location'].nunique():,}")
print(f"Outputs written to: {out}")
