# COVID-19 Global Impact Dashboard

A portfolio-ready analytics project covering data cleaning, missing-value handling, derived metrics, population-normalized comparisons, trend analysis, and an interactive Streamlit dashboard.

## Important data note
The included `data/covid_demo_data.csv` is **illustrative demo data generated for an offline preview**. It is not observed COVID-19 data and must not be cited as real-world evidence. To use the public dataset, run `python download_data.py`. The downloader retrieves the Our World in Data COVID-19 dataset and saves the relevant columns to `data/owid-covid-data.csv`. The app automatically prefers that file when present.

Data source: Our World in Data, COVID-19 dataset: https://github.com/owid/covid-19-data/tree/master/public/data  
Dataset documentation: https://github.com/owid/covid-19-data/blob/master/public/data/README.md

## Run on Windows
1. Install Python 3.10 or later.
2. Extract the ZIP folder.
3. Open Command Prompt / VS Code terminal in this folder.
4. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
5. Install libraries:
   ```bash
   pip install -r requirements.txt
   ```
6. Optional but recommended for factual analysis: download public data:
   ```bash
   python download_data.py
   ```
7. Run cleaning and metrics:
   ```bash
   python analysis.py
   ```
8. Launch dashboard:
   ```bash
   streamlit run app.py
   ```
The dashboard opens in your browser. If you skip step 6, it opens with the clearly labelled illustrative demo dataset.

## Deliverables
- `data/covid_demo_data.csv`: offline demo data, clearly labelled.
- `download_data.py`: fetches public OWID data.
- `analysis.py`: cleaning, derived metrics, and output CSV generation.
- `app.py`: interactive dashboard with country/date filters, time trends, per-million normalization, vaccination comparison, and CSV export.
- `outputs/`: place for generated cleaned data and summary CSVs.
- `executive_summary.pdf`: one-page project summary and analysis plan.

## Cleaning assumptions
- Invalid dates are parsed as missing and rows without a date or location are removed.
- Numeric fields are coerced to numeric; unparseable values become missing.
- Negative daily case/death revisions are clipped to zero for daily trend charts, while the raw source remains unchanged in the downloaded file.
- Missing values are not automatically replaced with zero because a missing report is not necessarily zero cases.
- Rates per million use the reported population denominator.
- Vaccination percentage is people fully vaccinated divided by population, capped at 100% for display.
- Rolling averages smooth daily/weekly reporting noise; the app labels its seven-observation rolling average.

## Suggested questions / insights to write after using real data
1. Which countries experienced the highest cases per million during the selected period?
2. How did the timing and size of case waves differ by country?
3. Did higher vaccination coverage coincide with lower subsequent death rates? Treat this as an association, not proof of causation; age, prior infection, variants, reporting, and health-system factors also matter.
4. Which countries have the largest gap between first-dose and full-vaccination coverage?
5. How do population-normalized comparisons differ from raw totals?

## Portfolio description
Built a COVID-19 analytics pipeline using Python, Pandas, and Streamlit. Cleaned time-series data, documented missing-value and revision-handling assumptions, engineered per-million rates and rolling averages, and created an interactive dashboard for comparing country-level cases, deaths, and vaccination progress.
