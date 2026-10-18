from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).parent
REAL_DATA = ROOT / "data" / "owid-covid-data.csv"
DEMO_DATA = ROOT / "data" / "covid_demo_data.csv"

st.set_page_config(page_title="COVID-19 Global Impact Dashboard", page_icon="🌍", layout="wide")
st.title("🌍 COVID-19 Global Impact Dashboard")
st.caption("Explore cases, deaths, and vaccination trends across countries and time.")

@st.cache_data
def load_data():
    path = REAL_DATA if REAL_DATA.exists() else DEMO_DATA
    df = pd.read_csv(path, low_memory=False)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["new_cases","total_cases","new_deaths","total_deaths","population",
                "people_vaccinated","people_fully_vaccinated","total_vaccinations",
                "new_vaccinations_smoothed"]:
        if col not in df.columns:
            df[col] = float("nan")
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["data_source"] = "Our World in Data" if path == REAL_DATA else "Illustrative demo data"
    return df

df = load_data()
if df["data_source"].iloc[0] == "Illustrative demo data":
    st.warning("You are viewing illustrative demo data, not observed COVID-19 statistics. Run `python download_data.py` to load the public Our World in Data dataset.")

df = df[df["location"].notna() & df["date"].notna()].copy()
countries = sorted(df["location"].dropna().unique())
default_countries = [c for c in ["India","United States","Brazil","United Kingdom","Germany"] if c in countries]
with st.sidebar:
    st.header("Dashboard filters")
    selected = st.multiselect("Countries / regions", countries, default=default_countries or countries[:5])
    min_date, max_date = df["date"].min().date(), df["date"].max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    metric = st.selectbox("Trend metric", ["new_cases", "new_deaths", "people_fully_vaccinated", "people_vaccinated"])
    per_million = st.checkbox("Normalize case/death rates per million people", value=True)
    rolling = st.checkbox("Show 7-day rolling average", value=True)

if not selected:
    st.info("Select at least one country from the sidebar.")
    st.stop()
if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Choose a start and end date.")
    st.stop()

start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
view = df[df["location"].isin(selected) & df["date"].between(start, end)].copy()
view = view.sort_values(["location","date"])
for col in ["new_cases","new_deaths"]:
    view[col] = view[col].clip(lower=0)
if per_million and metric in ["new_cases","new_deaths"]:
    view["display_metric"] = view[metric] / view["population"] * 1_000_000
    y_label = "Per million people"
else:
    view["display_metric"] = view[metric]
    y_label = metric.replace("_"," ").title()
if rolling and metric in ["new_cases","new_deaths"]:
    view["display_metric"] = view.groupby("location")["display_metric"].transform(lambda s: s.rolling(7, min_periods=1).mean())

latest = view.sort_values("date").groupby("location", as_index=False).tail(1)
total_cases = latest["total_cases"].fillna(0).sum()
total_deaths = latest["total_deaths"].fillna(0).sum()
vacc = latest["people_fully_vaccinated"].fillna(0).sum()
pop = latest["population"].fillna(0).sum()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Countries selected", f"{len(selected)}")
c2.metric("Latest cumulative cases", f"{total_cases:,.0f}")
c3.metric("Latest cumulative deaths", f"{total_deaths:,.0f}")
c4.metric("Fully vaccinated people", f"{vacc:,.0f}")

st.subheader("Trend over time")
fig = px.line(view, x="date", y="display_metric", color="location", labels={"date":"Date","display_metric":y_label,"location":"Country"}, title=f"{metric.replace('_',' ').title()} over time")
st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Country comparison")
    comp = latest.copy()
    comp["cases_per_million"] = comp["total_cases"] / comp["population"] * 1_000_000
    comp["deaths_per_million"] = comp["total_deaths"] / comp["population"] * 1_000_000
    comp["fully_vaccinated_pct"] = comp["people_fully_vaccinated"] / comp["population"] * 100
    choice = st.selectbox("Compare by", ["Cases per million","Deaths per million","Fully vaccinated (%)"])
    colmap = {"Cases per million":"cases_per_million","Deaths per million":"deaths_per_million","Fully vaccinated (%)":"fully_vaccinated_pct"}
    fig2 = px.bar(comp, x="location", y=colmap[choice], color="location", title=choice)
    fig2.update_layout(showlegend=False, xaxis_title="", yaxis_title=choice)
    st.plotly_chart(fig2, use_container_width=True)
with right:
    st.subheader("Vaccination progress")
    v = latest.copy()
    v["fully_vaccinated_pct"] = (v["people_fully_vaccinated"] / v["population"] * 100).clip(upper=100)
    fig3 = px.bar(v, x="location", y="fully_vaccinated_pct", color="location", title="Fully vaccinated people (% of population)")
    fig3.update_layout(showlegend=False, xaxis_title="", yaxis_title="Percent")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Data preview")
show_cols = [c for c in ["date","location","population","new_cases","new_deaths","people_vaccinated","people_fully_vaccinated"] if c in view.columns]
st.dataframe(view[show_cols].tail(100), use_container_width=True)
st.download_button("Download filtered data as CSV", view.to_csv(index=False).encode("utf-8"), "covid_filtered_data.csv", "text/csv")
st.caption(f"Source mode: {df['data_source'].iloc[0]}. Per-million metrics support fairer comparisons across different population sizes.")
