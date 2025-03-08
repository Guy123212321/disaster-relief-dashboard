import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1dEzzG4yXoZTEW_g6LIblTepdLpiT6DfGnbquQhJ6f1Q/gviz/tq?tqx=out:csv"

# Load the dataset
df = pd.read_csv(sheet_url)

# Dictionary to store all sections
data = {}

# Section 1: Overview
overview = df.iloc[1:7, :2]
overview.columns = ["Category", "Details"]
data["Overview"] = overview

# Section 2: Infrastructure Damage
infrastructure_damage = df.iloc[10:15, :3]
infrastructure_damage.columns = ["Category", "Damage Details", "Estimated Cost (USD)"]
data["Infrastructure Damage"] = infrastructure_damage

# Section 3: Causes of the Floods
causes_of_floods = df.iloc[17:20, :2]
causes_of_floods.columns = ["Cause", "Details"]
data["Causes of the Floods"] = causes_of_floods

# Section 4: Province-Wise Impact
province_impact = df.iloc[22:26, :4]
province_impact.columns = ["Province", "Deaths", "Houses Damaged", "Cropland Affected"]
data["Province-Wise Impact"] = province_impact

# Section 5: Key Statistics (Summary)
key_statistics = df.iloc[28:34, :2]
key_statistics.columns = ["Statistic", "Details"]
data["Key Statistics (Summary)"] = key_statistics

# Section 6: How Was Aid Organized?
aid_organized = df.iloc[36:42, :2]
aid_organized.columns = ["Aid Effort", "Details"]
data["How Was Aid Organized?"] = aid_organized

# Section 7: Damage, Loss, and Needs
damage_loss_needs = df.iloc[44:48, :7]
damage_loss_needs.columns = ["Region", "Billion (PKR)", "Million (US$)", "Billion (PKR)", "Million (US$)", "Billions (PKR)", "Millions (US$)"]
data["Damage, Loss, and Needs"] = damage_loss_needs

# Section 8: Types of Resources Needed for Disaster Relief
resources_needed = df.iloc[50:55, :2]
resources_needed.columns = ["Category", "Examples"]
data["Types of Resources Needed for Disaster Relief"] = resources_needed

# Section 9: Quantities of Essential Resources Required
quantities_resources = df.iloc[57:61, :3]
quantities_resources.columns = ["Resource", "Per Person Requirement", "For 1 Million People"]
data["Quantities of Essential Resources Required"] = quantities_resources

# Section 10: Resource Prioritization by Timeframe
resource_prioritization = df.iloc[63:66, :2]
resource_prioritization.columns = ["Timeframe", "Priority Resources"]
data["Resource Prioritization by Timeframe"] = resource_prioritization

# Section 11: Resource Availability & Challenges
resource_availability = df.iloc[68:71, :2]
resource_availability.columns = ["Availability Source", "Details"]
data["Resource Availability & Challenges"] = resource_availability

# Section 12: Case Studies of Disaster Resource Distribution
case_studies = df.iloc[73:76, :3]
case_studies.columns = ["Disaster Event", "Key Resources Distributed", "Challenges Faced"]
data["Case Studies of Disaster Resource Distribution"] = case_studies

# Section 13: Data Sources for Disaster Resource Tracking
data_sources = df.iloc[78:82, :2]
data_sources.columns = ["Source", "Data Provided"]
data["Data Sources for Disaster Resource Tracking"] = data_sources

# Section 14: Recommendations for Better Resource Distribution
recommendations = df.iloc[84:87, :2]
recommendations.columns = ["Recommendation", "Why It’s Important?"]
data["Recommendations for Better Resource Distribution"] = recommendations

# Section 15: Immediate Actions and Long-Term Solutions
actions_solutions = df.iloc[89:101, :3]
actions_solutions.columns = ["Category", "Recommended Actions", "Details"]
data["Immediate Actions and Long-Term Solutions"] = actions_solutions

# Section 16: Disaster Impact on Vulnerable Groups
vulnerable_groups = df.iloc[103:106, :5]
vulnerable_groups.columns = ["Disaster", "People Affected", "Percentage of Women", "Percentage of Children", "Percentage of Elderly"]
data["Disaster Impact on Vulnerable Groups"] = vulnerable_groups

# Section 17: Aid Response Time in Major Cities
aid_response_cities = df.iloc[108:113, :3]
aid_response_cities.columns = ["City", "Time to Receive Initial Aid", "Key Challenges"]
data["Aid Response Time in Major Cities"] = aid_response_cities

# Section 18: Aid Response Time in Rural & Remote Areas
aid_response_rural = df.iloc[115:120, :4]
aid_response_rural.columns = ["Region", "Time to Receive Initial Aid", "Key Challenges", "Total Aid Received"]
data["Aid Response Time in Rural & Remote Areas"] = aid_response_rural

# Section 19: Causes of Pakistan Flood
causes_pakistan_flood = df.iloc[122:125, :2]
causes_pakistan_flood.columns = ["Cause", "Details"]
data["Causes of Pakistan Flood"] = causes_pakistan_flood

# Title of the dashboard
st.title("Disaster Relief Dashboard")

# Display all sections
for section_name, section_data in data.items():
    st.header(section_name)
    st.write(section_data)

# Plot deaths by province
st.header("Deaths by Province")
fig, ax = plt.subplots()
sns.barplot(x="Province", y="Deaths", data=data["Province-Wise Impact"], ax=ax)
st.pyplot(fig)
