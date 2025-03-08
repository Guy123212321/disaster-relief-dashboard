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

    # ----------------------------
    # 1. Overview
    # ----------------------------
    overview = df.iloc[1:7, :2].copy()
    overview.columns = ["Category", "Details"]
    data["Overview"] = overview.dropna()

    # ----------------------------
    # 2. Infrastructure Damage
    # ----------------------------
    infra_damage = df.iloc[10:15, :3].copy()
    infra_damage.columns = ["Category", "Damage Details", "Estimated Cost (USD)"]
    data["Infrastructure Damage"] = infra_damage.dropna()

    # ----------------------------
    # 3. Causes of Floods 
    # ----------------------------
    causes = df.iloc[17:20, :2].copy()
    causes.columns = ["Cause", "Details"]
    data["Causes of Floods"] = causes.dropna()

    # ----------------------------
    # 4. Province-Wise Impact (FIXED)
    # ----------------------------
    province_impact = df.iloc[22:26, :4].copy()
    province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]
    province_impact["Deaths"] = (
        province_impact["Deaths"]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    data["Province-Wise Impact"] = province_impact.dropna()

    # ----------------------------
    # 7. Damage/Loss/Needs (CRITICAL FIX)
    # ----------------------------
    damage_loss = df.iloc[44:48, :7].copy()
    damage_loss.columns = [
        "Region", 
        "Damage_Billion_PKR", 
        "Damage_Million_USD",
        "Loss_Billion_PKR", 
        "Loss_Million_USD", 
        "Needs_Billion_PKR", 
        "Needs_Million_USD"
    ]
    
    # Bulletproof numeric conversion
    numeric_cols = damage_loss.columns[1:]
    for col in numeric_cols:
        damage_loss[col] = (
            damage_loss[col]
            .astype(str)
            .str.replace(r'[^\d.]', '', regex=True)  # Remove all non-numeric
            .replace(r'^\.$', pd.NA, regex=True)     # Handle lone decimals
            .replace('', pd.NA)
            .pipe(pd.to_numeric, errors='coerce')
    
    data["Damage, Loss and Needs"] = damage_loss.dropna(how='all')

    # ----------------------------
    # 5-19. Other Sections (Add similarly)
    # ----------------------------
    # [Add all other sections using the same pattern]
    
    return data

# Load data
data = load_data()

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Disaster Relief Dashboard")

for section_name, section_data in data.items():
    st.header(section_name)
    if isinstance(section_data, pd.DataFrame) and not section_data.empty:
        st.dataframe(section_data.reset_index(drop=True))
    else:
        st.write("Data unavailable for this section")

# ----------------------------
# Deaths Plot (Failsafe)
# ----------------------------
if "Province-Wise Impact" in data:
    st.header("Deaths by Province Analysis")
    try:
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(
            x="Province",
            y="Deaths",
            data=data["Province-Wise Impact"],
            palette="viridis",
            ax=ax
        )
        ax.set_ylabel("Number of Deaths")
        ax.set_xlabel("")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Visualization unavailable: {str(e)}")
