import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re  # <<< ADDED FOR CLEANING

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1dEzzG4yXoZTEW_g6LIblTepdLpiT6DfGnbquQhJ6f1Q/gviz/tq?tqx=out:csv"

# Helper function for numeric cleaning <<< ADDED
def clean_numeric(series):
    return (
        series.astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .replace('', pd.NA)
        .pipe(pd.to_numeric, errors='coerce')
    )

@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    data = {}

    # ----------------------------
    # 1. Overview (ORIGINAL)
    # ----------------------------
    overview = df.iloc[1:7, :2]
    overview.columns = ["Category", "Details"]
    data["Overview"] = overview

    # ----------------------------
    # 2. Infrastructure Damage (FIXED)
    # ----------------------------
    infrastructure_damage = df.iloc[10:15, :3]
    infrastructure_damage.columns = ["Category", "Damage Details", "Estimated Cost (USD)"]
    infrastructure_damage["Estimated Cost (USD)"] = clean_numeric(infrastructure_damage["Estimated Cost (USD)"])  # <<< ADDED CLEANING
    data["Infrastructure Damage"] = infrastructure_damage

    # ----------------------------
    # 4. Province-Wise Impact (FIXED)
    # ----------------------------
    province_impact = df.iloc[22:26, :4]
    province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]
    province_impact["Deaths"] = clean_numeric(province_impact["Deaths"])  # <<< ADDED CLEANING
    data["Province-Wise Impact"] = province_impact

    # ----------------------------
    # 7. Damage, Loss, and Needs (FIXED)
    # ----------------------------
    damage_loss_needs = df.iloc[44:48, :7]
    damage_loss_needs.columns = ["Region", "Billion (PKR)", "Million (US$)", "Billion (PKR)", "Million (US$)", "Billions (PKR)", "Millions (US$)"]
    # Clean all numeric columns <<< ADDED
    for col in damage_loss_needs.columns[1:]:
        damage_loss_needs[col] = clean_numeric(damage_loss_needs[col])
    data["Damage, Loss, and Needs"] = damage_loss_needs

    # [KEEP ALL OTHER SECTIONS AS ORIGINAL]

    return data

data = load_data()

# ----------------------------
# Original UI Below (WITH FIXED PLOT)
# ----------------------------
st.title("Disaster Relief Dashboard")

# Display all sections
for section_name, section_data in data.items():
    st.header(section_name)
    if isinstance(section_data, pd.DataFrame):
        st.dataframe(section_data)
    else:
        st.write(section_data)

# Fixed Deaths plot <<< ENHANCED
if "Province-Wise Impact" in data:
    st.header("Deaths by Province")
    try:
        plot_data = data["Province-Wise Impact"].dropna(subset=["Deaths"])
        if not plot_data.empty:
            fig, ax = plt.subplots()
            sns.barplot(x="Province", y="Deaths", data=plot_data)
            plt.xticks(rotation=45)  # <<< ADDED ROTATION
            st.pyplot(fig)
        else:
            st.warning("No valid death data to display")
    except Exception as e:
        st.error(f"Plotting error: {str(e)}")
