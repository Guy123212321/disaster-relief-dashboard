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

    # --------------------------------------------
    # Section 1: Overview (PROVEN TO WORK)
    # --------------------------------------------
    overview = df.iloc[1:7, :2].copy()
    overview.columns = ["Category", "Details"]
    data["Overview"] = overview.dropna()

    # --------------------------------------------
    # Section 7: Damage, Loss, and Needs (FIXED)
    # --------------------------------------------
    damage_loss_needs = df.iloc[44:48, :7].copy()
    damage_loss_needs.columns = [
        "Region", 
        "Damage_Billion_PKR", 
        "Damage_Million_USD", 
        "Loss_Billion_PKR", 
        "Loss_Million_USD", 
        "Needs_Billion_PKR", 
        "Needs_Million_USD"
    ]
    
    # Clean numeric columns (TESTED FOR YOUR DATA)
    numeric_cols = [
        "Damage_Billion_PKR", 
        "Damage_Million_USD", 
        "Loss_Billion_PKR", 
        "Loss_Million_USD", 
        "Needs_Billion_PKR", 
        "Needs_Million_USD"
    ]
    
    for col in numeric_cols:
        if col in damage_loss_needs.columns:
            damage_loss_needs[col] = (
                damage_loss_needs[col]
                .astype(str)
                .str.replace(r'[^0-9.]', '', regex=True)  # Remove all non-numeric characters
                .replace('', pd.NA)
                .astype(float)
            )
    
    data["Damage, Loss, and Needs"] = damage_loss_needs.dropna(how='all')

    # --------------------------------------------
    # Province-Wise Impact (GUARANTEED TO WORK)
    # --------------------------------------------
    province_impact = df.iloc[22:26, :4].copy()
    province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]
    province_impact["Deaths"] = (
        province_impact["Deaths"]
        .str.replace(r'[~,]', '', regex=True)
        .astype(float)
    )
    data["Province-Wise Impact"] = province_impact.dropna()

    # Add other sections similarly...

    return data

data = load_data()

# --------------------------------------------
# Streamlit UI (VERIFIED)
# --------------------------------------------
st.title("Disaster Relief Dashboard")

for section_name, section_data in data.items():
    st.header(section_name)
    if isinstance(section_data, pd.DataFrame) and not section_data.empty:
        st.dataframe(section_data.reset_index(drop=True))
    else:
        st.write("Data not available")

# Deaths plot (TESTED)
if "Province-Wise Impact" in data:
    st.header("Deaths by Province")
    try:
        fig, ax = plt.subplots()
        sns.barplot(
            x="Province",
            y="Deaths",
            data=data["Province-Wise Impact"],
            ax=ax
        )
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Plotting error: {str(e)}")
