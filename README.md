# COVID-19 Global Impact Dashboard

An interactive data analytics project for exploring COVID-19 cases, deaths, and vaccination trends across countries and time periods.

## Overview

This project demonstrates an end-to-end data analytics workflow using Python, Pandas, and Streamlit. It focuses on data cleaning, metric engineering, country-level comparisons, and interactive visualization.

## Features

- Interactive country and date-range filters
- COVID-19 case and death trend analysis
- Population-normalized metrics: cases and deaths per million
- Vaccination progress comparisons
- Optional rolling-average visualization
- Data preview and filtered CSV export
- Reproducible data-cleaning workflow

## Technologies

- Python
- Pandas and NumPy
- Streamlit
- Plotly
- CSV datasets

## Project Structure

```text
covid19_global_impact_dashboard/
├── app.py
├── analysis.py
├── download_data.py
├── requirements.txt
├── README.md
├── PROJECT_FILES.txt
├── executive_summary.pdf
├── data/
│   └── covid_demo_data.csv
└── outputs/
```

## Installation and Usage

Install the dependencies:

```bash
pip install -r requirements.txt
```

Download the public dataset:

```bash
python download_data.py
```

Run the cleaning pipeline:

```bash
python analysis.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

## Data Source

Our World in Data — COVID-19 dataset:

https://github.com/owid/covid-19-data/tree/master/public/data

**Note:** The included demo dataset is illustrative and is not real-world COVID-19 data. Use the public dataset for factual analysis and verify findings before publishing them.

## Learning Outcomes

- Data cleaning and preprocessing
- Handling missing and invalid values
- Feature engineering and rolling averages
- Exploratory data analysis
- Interactive dashboard development
- Data storytelling and visualization

## Future Improvements

- Add more advanced country-level comparisons
- Include additional indicators and filters
- Add automated data refresh
- Develop a deeper analysis of vaccination and mortality trends

**Project category:** Data Analytics | Data Visualization | Python
