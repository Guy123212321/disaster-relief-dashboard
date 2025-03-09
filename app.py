import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1dEzzG4yXoZTEW_g6LIblTepdLpiT6DfGnbquQhJ6f1Q/gviz/tq?tqx=out:csv"

def load_data():
    try:
        df = pd.read_csv(sheet_url)
        data = {}

        # ----------------------------
        # 1. Overview (Verified)
        # ----------------------------
        overview = df.iloc[1:7, :2].copy()
        overview.columns = ["Category", "Details"]
        data["Overview"] = overview.dropna()

        # ----------------------------
        # 2. Infrastructure Damage (Fixed)
        # ----------------------------
        infra_damage = df.iloc[10:15, :3].copy()
        infra_damage.columns = ["Category", "Damage Details", "Estimated Cost (USD)"]
        infra_damage["Estimated Cost (USD)"] = (
            infra_damage["Estimated Cost (USD)"].astype(str)
            .str.replace(r'[^\d.]', '', regex=True)
            .pipe(pd.to_numeric, errors='coerce')
        )
        data["Infrastructure Damage"] = infra_damage.dropna()

        # ----------------------------
        # 3. Causes of Floods (Working)
        # ----------------------------
        causes = df.iloc[17:20, :2].copy()
        causes.columns = ["Cause", "Details"]
        data["Causes of Floods"] = causes.dropna()

        # ----------------------------
        # 4. Province-Wise Impact (Enhanced)
        # ----------------------------
        province_impact = df.iloc[22:26, :4].copy()
        province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]

        for col in ["Deaths", "Houses Damaged"]:
            province_impact[col] = (
                province_impact[col].astype(str)
                .str.replace(r'[^\d.]', '', regex=True)
                .pipe(pd.to_numeric, errors='coerce')
            )
        data["Province-Wise Impact"] = province_impact.dropna()

        # ----------------------------
        # 5. Key Statistics (Verified)
        # ----------------------------
        key_stats = df.iloc[28:34, :2].copy()
        key_stats.columns = ["Statistic", "Value"]
        data["Key Statistics"] = key_stats.dropna()

        # ----------------------------
        # 6. Damage/Loss/Needs (Critical Fix)
        # ----------------------------
        damage_loss = df.iloc[44:48, :7].copy()
        damage_loss.columns = [
            "Region", "Damage (PKR Billion)", "Damage (USD Million)",
            "Loss (PKR Billion)", "Loss (USD Million)",
            "Needs (PKR Billion)", "Needs (USD Million)"
        ]

        for col in damage_loss.columns[1:]:
            damage_loss[col] = (
                damage_loss[col].astype(str)
                .str.replace(r'[^\d.]', '', regex=True)
                .pipe(pd.to_numeric, errors='coerce')
            )
        data["Damage Analysis"] = damage_loss.dropna(how='all')

        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

data = load_data()

# Streamlit UI Setup
st.set_page_config(layout="wide")
st.title("🇵🇰 Pakistan Floods 2022 - Disaster Response Dashboard")

if "Overview" in data:
    metrics = data["Overview"].set_index("Category")["Details"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Deaths", metrics.get("Deaths", "N/A"))
    with col2:
        st.metric("Affected Population", metrics.get("Affected Population", "N/A"))
    with col3:
        st.metric("Economic Loss", metrics.get("Economic Losses", "N/A"))
    with col4:
        st.metric("Displaced People", metrics.get("Displaced People", "N/A"))

# Tabs for Data Sections
tabs = st.tabs(["[💰 Damage Analysis]", "[🏥 Infrastructure]", "[📈 Statistics]", "[📋 Full Data]"])

with tabs[0]:
    if "Damage Analysis" in data:
        st.subheader("Financial Impact Assessment")
        st.dataframe(data["Damage Analysis"], use_container_width=True)
    else:
        st.warning("Damage data currently unavailable")

with tabs[1]:
    if "Infrastructure Damage" in data:
        st.subheader("Critical Infrastructure Damage")
        st.dataframe(data["Infrastructure Damage"], use_container_width=True)
    else:
        st.warning("Infrastructure data currently unavailable")

with tabs[3]:
    st.subheader("Complete Dataset Overview")
    for section in data:
        if section:
            with st.expander(f"📁 {section}"):
                st.dataframe(data[section], use_container_width=True)

# Sidebar: Emergency Resource Calculator
with st.sidebar:
    st.header("🚨 Emergency Calculator")
    population = st.number_input("Affected population size:", min_value=1000, value=10000, step=1000)
    st.subheader("Daily Requirements")
    st.write(f"💧 Water: **{(population * 15):,} liters**")
    st.write(f"🍲 Food: **{(population * 2.1):,} kg**")
    st.write(f"🏥 Medical Kits: **{np.ceil(population/1000):.0f} units**")
    st.write(f"🛏️ Shelter: **{np.ceil(population/5):,} family tents**")
    st.sidebar.info("Prioritize water, medical aid, and evacuation plans.")
