import streamlit as st
import pandas as pd
from config.database import get_db_engine

st.set_page_config(page_title="Job Market Pipeline Dashboard", layout="wide")
st.title("Himalayas Job Market Dashboard")

@st.cache_data(ttl=300)
def fetch_mysql_data():
    engine = get_db_engine()
    query = "SELECT * FROM dim_jobs"
    return pd.read_sql(query, con=engine)

try:
    df = fetch_mysql_data()

    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs Loaded", f"{len(df):,}")
    col2.metric("Unique Companies", f"{df['company'].nunique():,}")
    
    valid_salaries = df[df["avg_salary"] > 0]
    avg_sal = valid_salaries["avg_salary"].mean() if not valid_salaries.empty else None
    col3.metric("Average Salary (USD)", f"${avg_sal:,.0f}" if pd.notna(avg_sal) else "N/A")

    st.divider()

    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("Top Employers Hiring")
        st.bar_chart(df["company"].value_counts().head(10))

    with right_col:
        st.subheader("Top Locations")
        st.bar_chart(df["location"].value_counts().head(10))

    st.subheader("Raw MySQL Table Data (`dim_jobs`)")
    st.dataframe(df, use_container_width=True)

except Exception as err:
    st.error(f"Error loading data from MySQL: {err}")
    st.info("Ensure MySQL is running, `.env` contains correct credentials, and `python -m scripts.run_pipeline` has executed.")
    