import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(layout="wide")
st.title("🌍 Disaster Response Dashboard")

# ====================
# Data Upload & Selection
# ====================
st.sidebar.header("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

def load_data(file):
    df = pd.read_csv(file)
    return df

if uploaded_file:
    df = load_data(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
else:
    st.sidebar.warning("Please upload a CSV file.")
    st.stop()

# ====================
# Data Processing & Cleaning
# ====================
data = {}

# Overview
overview = df.iloc[1:7, :2].copy()
overview.columns = ["Category", "Details"]
data["Overview"] = overview.dropna()

# Infrastructure Dmg
infra_damage = df.iloc[10:15, :3].copy()
infra_damage.columns = ["Category", "Damage Details", "Estimated Cost (USD)"]
infra_damage["Estimated Cost (USD)"] = (
    infra_damage["Estimated Cost (USD)"]
    .astype(str)
    .str.replace(r'[^\d.]', '', regex=True)
    .pipe(pd.to_numeric, errors='coerce')
)
data["Infrastructure Damage"] = infra_damage.dropna()

# Causes of Disaster
causes = df.iloc[17:20, :2].copy()
causes.columns = ["Cause", "Details"]
data["Causes of Disaster"] = causes.dropna()

# Region-wise Impact
province_impact = df.iloc[22:26, :4].copy()
province_impact.columns = ["Region", "Deaths", "Houses Damaged", "Cropland Affected"]
for col in ["Deaths", "Houses Damaged"]:
    province_impact[col] = (
        province_impact[col]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    )
data["Region-Wise Impact"] = province_impact.dropna()

# Key Stats
key_stats = df.iloc[28:34, :2].copy()
key_stats.columns = ["Statistic", "Value"]
data["Key Statistics"] = key_stats.dropna()

# Damage Analysis
damage_loss = df.iloc[44:48, :7].copy()
damage_loss.columns = [
    "Region", "Damage (PKR Billion)", "Damage (USD Million)",
    "Loss (PKR Billion)", "Loss (USD Million)", "Needs (PKR Billion)", "Needs (USD Million)"
]
for col in damage_loss.columns[1:]:
    damage_loss[col] = (
        damage_loss[col]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .replace(r'^.$', np.nan, regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    )
data["Damage Analysis"] = damage_loss.dropna(how='all')

# ====================
# visuals :fire
# ====================
if "Region-Wise Impact" in data and not data["Region-Wise Impact"].empty:
    region_data = data["Region-Wise Impact"]
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2ecc71' if x < region_data['Deaths'].median() else '#e74c3c' for x in region_data['Deaths']]
    bars = ax.bar(region_data['Region'], region_data['Deaths'], color=colors, edgecolor='white')
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center',
                    va='bottom',
                    fontsize=10)
    ax.set_title('Casualties by Region', fontsize=14, pad=20, fontweight='bold')
    ax.set_ylabel('Number of Deaths', labelpad=15)
    ax.set_xlabel('')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    data["Casualty Analysis"] = fig

# ====================
# Streamlit Interface
# ====================
st.subheader("Human Impact Analysis")
if "Casualty Analysis" in data:
    st.pyplot(data["Casualty Analysis"])
st.markdown("""
**Actionable Insights:**
- Immediate medical aid required in high casualty regions.
- Evacuation support needed for remaining at-risk populations.
- Priority shelter allocation for displaced families.
""")

# Tabs 4 data section
tabs = st.tabs(["[💰 Damage Analysis]", "[🏥 Infrastructure]", "[📈 Statistics]", "[📋 Full Data]"])
with tabs[0]:
    if "Damage Analysis" in data:
        st.subheader("Financial Impact Assessment")
        st.dataframe(
            data["Damage Analysis"].style.format({
                'Damage (PKR Billion)': '{:,.1f}B',
                'Damage (USD Million)': '${:,.1f}M',
                'Loss (PKR Billion)': '{:,.1f}B',
                'Loss (USD Million)': '${:,.1f}M'
            }),
            use_container_width=True
        )
with tabs[1]:
    if "Infrastructure Damage" in data:
        st.subheader("Critical Infrastructure Damage")
        fig, ax = plt.subplots(figsize=(8,4))
        damage_df = data["Infrastructure Damage"]
        sns.barplot(
            x="Estimated Cost (USD)",
            y="Category",
            data=damage_df.sort_values("Estimated Cost (USD)", ascending=False),
            palette="viridis",
            ax=ax
        )
        ax.set_title("Estimated Repair Costs")
        st.pyplot(fig)
with tabs[3]:
    st.subheader("Complete Dataset Overview")
    for section in data:
        if section not in ["Casualty Analysis"]:
            with st.expander(f"📁 {section}"):
                st.dataframe(data[section], use_container_width=True)

# ====================
# emregency calculator :D
# ====================
with st.sidebar:
    st.header("🚨 Emergency Calculator")
    population = st.number_input("Affected population size:", min_value=1000, value=10000, step=1000)
    st.subheader("Daily Requirements")
    st.write(f"💧 Water: **{(population * 15):,} liters**")
    st.write(f"🍲 Food: **{(population * 2.1):,} kg**")
    st.write(f"🏥 Medical Kits: **{np.ceil(population/1000):.0f} units**")
    st.write(f"🛏️ Shelter: **{np.ceil(population/5):,} family tents**")
