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

    # =============================================
    # FIXED: Damage, Loss, and Needs Section
    # =============================================
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
    
    # SAFE numeric conversion with multiple fallbacks
    numeric_cols = damage_loss_needs.columns[1:]
    for col in numeric_cols:
        damage_loss_needs[col] = (
            damage_loss_needs[col]
            .astype(str)
            .str.strip()  # Remove whitespace
            .str.replace(r'[^\d.]', '', regex=True)  # Keep only numbers and dots
            .replace(r'^\.$', pd.NA, regex=True)  # Replace lone dots with NA
            .replace('', pd.NA)
            .pipe(pd.to_numeric, errors='coerce')  # SAFEST conversion method
        )
    
    data["Damage, Loss, and Needs"] = damage_loss_needs.dropna(how='all')

    # =============================================
    # Province-Wise Impact (Guaranteed Working)
    # =============================================
    province_impact = df.iloc[22:26, :4].copy()
    province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]
    
    province_impact["Deaths"] = (
        province_impact["Deaths"]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    )
    
    data["Province-Wise Impact"] = province_impact.dropna()

    # Add other sections using same pattern...

    return data

data = load_data()

# =============================================
# Streamlit Display
# =============================================
st.title("Disaster Relief Dashboard")

for section_name, section_data in data.items():
    st.header(section_name)
    if isinstance(section_data, pd.DataFrame) and not section_data.empty:
        st.dataframe(section_data.reset_index(drop=True))
    else:
        st.write("Data unavailable")

# Plot with error handling
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
        st.error(f"Could not render plot: {str(e)}")
