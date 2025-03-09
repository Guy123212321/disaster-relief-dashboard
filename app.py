import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1dEzzG4yXoZTEW_g6LIblTepdLpiT6DfGnbquQhJ6f1Q/gviz/tq?tqx=out:csv"

@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    data = {}

    # ====================
    # Critical Fixes for Graphs
    # ====================
    
    # 1. Province Impact Data Fix
    province_impact = df.iloc[22:26, :4].copy()
    province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]
    
    # Convert deaths to numeric
    province_impact["Deaths"] = (
        province_impact["Deaths"]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .replace('', pd.NA)
        .pipe(pd.to_numeric, errors='coerce')
    )
    data["Province-Wise Impact"] = province_impact.dropna()

    # 2. Infrastructure Damage Fix
    infra_damage = df.iloc[10:15, :3].copy()
    infra_damage.columns = ["Category", "Damage Details", "Estimated Cost (USD)"]
    
    # Clean cost values
    infra_damage["Estimated Cost (USD)"] = (
        infra_damage["Estimated Cost (USD)"]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    )
    data["Infrastructure Damage"] = infra_damage.dropna()

    return data

data = load_data()

# ====================
# Existing UI Preservation
# ====================
st.set_page_config(layout="wide")
st.title("🇵🇰 Pakistan Floods 2022 - Disaster Response Dashboard")

# ----------------------------
# Fixed Metric Row
# ----------------------------
if "Province-Wise Impact" in data:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_deaths = data["Province-Wise Impact"]["Deaths"].sum()
        st.metric("Total Confirmed Deaths", f"{int(total_deaths):,}")
    with col2:
        st.metric("Most Affected Province", 
                "Sindh" if "Sindh" in data["Province-Wise Impact"]["Province"].values else "N/A")

# ----------------------------
# Fixed Deaths Visualization
# ----------------------------
if "Province-Wise Impact" in data and not data["Province-Wise Impact"].empty:
    st.subheader("Casualty Analysis by Province")
    try:
        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(
            x="Province",
            y="Deaths",
            data=data["Province-Wise Impact"],
            palette="viridis",
            ax=ax
        )
        ax.set_title("Reported Deaths by Province", weight='bold', pad=20)
        ax.set_ylabel("Number of Deaths", labelpad=15)
        st.pyplot(fig)
    except Exception as e:
        st.warning("Casualty data visualization temporarily unavailable")

# ----------------------------
# Fixed Infrastructure Costs
# ----------------------------
if "Infrastructure Damage" in data and not data["Infrastructure Damage"].empty:
    st.subheader("Infrastructure Repair Costs")
    try:
        cost_data = data["Infrastructure Damage"].dropna(subset=["Estimated Cost (USD)"])
        
        fig2, ax2 = plt.subplots(figsize=(12,6))
        sns.barplot(
            x="Estimated Cost (USD)",
            y="Category",
            data=cost_data.sort_values("Estimated Cost (USD)", ascending=False),
            palette="mako",
            ax=ax2
        )
        ax2.set_title("Estimated Repair Costs (USD Millions)", pad=20, fontweight='bold')
        ax2.set_xlabel("Cost in USD Millions", labelpad=15)
        st.pyplot(fig2)
        
    except Exception as e:
        st.warning("Cost analysis currently unavailable")

# ----------------------------
# Existing Emergency Calculator
# ----------------------------
with st.sidebar:
    st.header("🚨 Resource Calculator")
    population = st.number_input("Affected population size:", 
                               min_value=1000, 
                               value=10000, 
                               step=1000)
    
    st.subheader("Daily Requirements")
    st.write(f"💧 Water: **{(population * 15):,} liters**")
    st.write(f"🍲 Food: **{(population * 2.1):,} kg**")
    st.markdown("---")
    st.info("""
    **Operational Priorities:
    1. Clean water distribution
    2. Emergency shelter setup
    3. Medical supply delivery
    """)
