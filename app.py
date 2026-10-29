import streamlit as st
import pandas as pd
import altair as alt
from config.database import get_db_engine

# Page Configuration
st.set_page_config(
    page_title="Remote Job Market Analytics",
    page_icon="💼",
    layout="wide"
)

# Custom Styling & CSS
st.markdown("""
    <style>
    .main { padding: 1.5rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; color: #1E293B; }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem; font-weight: 600; color: #64748B; }
    </style>
""", unsafe_allow_html=True)

# Cache MySQL Database Query (5-minute TTL)
@st.cache_data(ttl=300)
def fetch_mysql_data():
    engine = get_db_engine()
    query = "SELECT * FROM dim_jobs"


import streamlit as st
import pandas as pd
import plotly.express as px
from config.database import get_db_engine

# Page Configuration
st.set_page_config(
    page_title="Remote Job Market Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def fetch_mysql_data():
    engine = get_db_engine()
    query = "SELECT * FROM dim_jobs"
    return pd.read_sql(query, con=engine)

try:
    df = fetch_mysql_data()

    # --- Sidebar Filters ---
    st.sidebar.title("Filter Listings")
    
    # Filter by Company
    companies = ["All"] + sorted(list(df["company"].dropna().unique()))
    selected_company = st.sidebar.selectbox("Select Company", companies)
    
    # Filter by Currency
    currencies = ["All"] + sorted(list(df["currency"].dropna().unique()))
    selected_currency = st.sidebar.selectbox("Select Currency", currencies)

    # Apply Filters
    filtered_df = df.copy()
    if selected_company != "All":
        filtered_df = filtered_df[filtered_df["company"] == selected_company]
    if selected_currency != "All":
        filtered_df = filtered_df[filtered_df["currency"] == selected_currency]
    

    # --- Header ---
    st.title("Remote Job Market Intelligence")
    st.caption("Live insights extracted, cleaned, and served via MySQL pipeline")
    st.divider()

    # --- Key Metrics (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Listings", f"{len(filtered_df):,}")
    col2.metric("Active Employers", f"{filtered_df['company'].nunique():,}")
    
    valid_salaries = filtered_df[filtered_df["avg_salary"] > 0]
    avg_sal = valid_salaries["avg_salary"].mean() if not valid_salaries.empty else 0
    max_sal = valid_salaries["avg_salary"].max() if not valid_salaries.empty else 0

    col3.metric("Avg Salary", f"${avg_sal:,.0f}" if avg_sal > 0 else "N/A")
    col4.metric("Top Offered Salary", f"${max_sal:,.0f}" if max_sal > 0 else "N/A")

    st.write("") # Blank space

    # --- Interactive Plotly Charts ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Top Employers Hiring")
        top_companies = (
            filtered_df["company"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_companies.columns = ["Company", "Job Count"]
        
        fig_company = px.bar(
            top_companies,
            x="Job Count",
            y="Company",
            orientation="h",
            color="Job Count",
            color_continuous_scale="Viridis",
            text="Job Count"
        )
        fig_company.update_layout(
            yaxis={"categoryorder": "total ascending"},
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=380
        )
        st.plotly_chart(fig_company, use_container_width=True)

    with chart_col2:
        st.subheader("Top Hiring Geographies")
        top_locations = (
            filtered_df["location"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_locations.columns = ["Location", "Job Count"]
        
        fig_loc = px.bar(
            top_locations,
            x="Job Count",
            y="Location",
            orientation="h",
            color="Job Count",
            color_continuous_scale="Blues",
            text="Job Count"
        )
        fig_loc.update_layout(
            yaxis={"categoryorder": "total ascending"},
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=380
        )
        st.plotly_chart(fig_loc, use_container_width=True)

    # --- Raw Data Section ---
    st.divider()
    st.subheader("Explorer: MySQL Warehouse Table (`dim_jobs`)")
    
    # Search Filter for Table
    search_query = st.text_input("Quick Search (by Position / Title):", "")
    if search_query:
        table_df = filtered_df[filtered_df["position"].str.contains(search_query, case=False, na=False)]
    else:
        table_df = filtered_df

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "avg_salary": st.column_config.NumberColumn("Avg Salary", format="$%d"),
            "posted_date": st.column_config.DatetimeColumn("Posted Date", format="D MMM YYYY"),
        }
    )

except Exception as err:
    st.error(f"Error loading data from MySQL: {err}")
    st.info("Ensure MySQL service is active (`net start MySQL80`) and `python -m scripts.run_pipeline` has run.")