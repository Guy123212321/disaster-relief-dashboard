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
    infra_damage["Estimated Cost (USD)"] = (
        infra_damage["Estimated Cost (USD)"]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    )
    data["Infrastructure Damage"] = infra_damage.dropna()

    # ----------------------------
    # 3. Causes of Floods
    # ----------------------------
    causes = df.iloc[17:20, :2].copy()
    causes.columns = ["Cause", "Details"]
    data["Causes of Floods"] = causes.dropna()

    # ----------------------------
    # 4. Province-Wise Impact
    # ----------------------------
    province_impact = df.iloc[22:26, :4].copy()
    province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]
    province_impact["Deaths"] = (
        province_impact["Deaths"]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    )
    data["Province-Wise Impact"] = province_impact.dropna()

    # ----------------------------
    # 5. Key Statistics (Summary)
    # ----------------------------
    key_stats = df.iloc[28:34, :2].copy()
    key_stats.columns = ["Statistic", "Details"]
    data["Key Statistics"] = key_stats.dropna()

    # ----------------------------
    # 6. Aid Organization
    # ----------------------------
    aid_organized = df.iloc[36:42, :2].copy()
    aid_organized.columns = ["Aid Effort", "Details"]
    data["Aid Organization"] = aid_organized.dropna()

    # ----------------------------
    # 7. Damage, Loss and Needs
    # ----------------------------
    damage_loss = df.iloc[44:48, :7].copy()
    damage_loss.columns = [
        "Region", 
        "Damage (Billion PKR)", 
        "Damage (Million USD)", 
        "Loss (Billion PKR)", 
        "Loss (Million USD)", 
        "Needs (Billion PKR)", 
        "Needs (Million USD)"
    ]
    for col in damage_loss.columns[1:]:
        damage_loss[col] = (
            damage_loss[col]
            .astype(str)
            .str.replace(r'[^\d.]', '', regex=True)
            .pipe(pd.to_numeric, errors='coerce')
        )
    data["Damage, Loss and Needs"] = damage_loss.dropna(how='all')

    # ----------------------------
    # 8. Resources Needed
    # ----------------------------
    resources = df.iloc[50:55, :2].copy()
    resources.columns = ["Category", "Examples"]
    data["Resources Needed"] = resources.dropna()

    # ----------------------------
    # 9. Resource Quantities
    # ----------------------------
    quantities = df.iloc[57:61, :3].copy()
    quantities.columns = ["Resource", "Per Person", "For 1 Million"]
    data["Resource Quantities"] = quantities.dropna()

    # ----------------------------
    # 10. Resource Prioritization
    # ----------------------------
    prioritization = df.iloc[63:66, :2].copy()
    prioritization.columns = ["Timeframe", "Priority"]
    data["Resource Prioritization"] = prioritization.dropna()

    # ----------------------------
    # 11. Resource Challenges
    # ----------------------------
    challenges = df.iloc[68:71, :2].copy()
    challenges.columns = ["Source", "Details"]
    data["Resource Challenges"] = challenges.dropna()

    # ----------------------------
    # 12. Case Studies
    # ----------------------------
    case_studies = df.iloc[73:76, :3].copy()
    case_studies.columns = ["Disaster", "Resources Used", "Challenges"]
    data["Case Studies"] = case_studies.dropna()

    # ----------------------------
    # 13. Data Sources
    # ----------------------------
    sources = df.iloc[78:82, :2].copy()
    sources.columns = ["Source", "Data Type"]
    data["Data Sources"] = sources.dropna()

    # ----------------------------
    # 14. Recommendations
    # ----------------------------
    recommendations = df.iloc[84:87, :2].copy()
    recommendations.columns = ["Recommendation", "Importance"]
    data["Recommendations"] = recommendations.dropna()

    # ----------------------------
    # 15. Action Plan
    # ----------------------------
    actions = df.iloc[89:101, :3].copy()
    actions.columns = ["Category", "Action", "Details"]
    data["Action Plan"] = actions.dropna()

    # ----------------------------
    # 16. Vulnerable Groups
    # ----------------------------
    vulnerable = df.iloc[103:106, :5].copy()
    vulnerable.columns = ["Disaster", "Affected", "% Women", "% Children", "% Elderly"]
    for col in ["% Women", "% Children", "% Elderly"]:
        vulnerable[col] = (
            vulnerable[col]
            .astype(str)
            .str.replace(r'[^\d.]', '', regex=True)
            .pipe(pd.to_numeric, errors='coerce')
        )
    data["Vulnerable Groups"] = vulnerable.dropna()

    # ----------------------------
    # 17. City Response Times
    # ----------------------------
    city_response = df.iloc[108:113, :3].copy()
    city_response.columns = ["City", "Response Time", "Challenges"]
    data["City Response Times"] = city_response.dropna()

    # ----------------------------
    # 18. Rural Response Times
    # ----------------------------
    rural_response = df.iloc[115:120, :4].copy()
    rural_response.columns = ["Region", "Response Time", "Challenges", "Aid Received"]
    rural_response["Aid Received"] = (
        rural_response["Aid Received"]
        .astype(str)
        .str.replace(r'[^\d.]', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
    )
    data["Rural Response Times"] = rural_response.dropna()

    # ----------------------------
    # 19. Flood Causes
    # ----------------------------
    flood_causes = df.iloc[122:125, :2].copy()
    flood_causes.columns = ["Cause", "Details"]
    data["Flood Causes"] = flood_causes.dropna()

    return data

data = load_data()

# ====================
# Streamlit Interface
# ====================
st.title("🌍 Pakistan Floods 2022 Disaster Relief Dashboard")

for section, content in data.items():
    with st.container():
        st.header(section)
        if isinstance(content, pd.DataFrame) and not content.empty:
            st.dataframe(content.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Data unavailable for this section", icon="⚠️")
        st.markdown("---")

# Deaths Visualization
if "Province-Wise Impact" in data:
    st.header("Deaths Analysis by Province")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x="Province",
            y="Deaths",
            data=data["Province-Wise Impact"],
            palette="viridis",
            ax=ax
        )
        ax.set_title("Reported Deaths by Province", weight='bold')
        ax.set_ylabel("Number of Deaths", labelpad=15)
        ax.set_xlabel("")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Could not generate visualization: {str(e)}")
