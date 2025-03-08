import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data  # Cache the data to improve performance
def load_data():
    # Load the CSV file
    df = pd.read_csv("disaster_data - DATA.csv", header=None)  # Load without headers initially

    # Manually define the sections and their respective rows
    sections = {
        "Overview": (1, 7),
        "Infrastructure Damage": (10, 15),
        "Causes of the Floods": (17, 20),
        "Province-Wise Impact": (22, 26),
        "Key Statistics (Summary)": (28, 34),
        "How Was Aid Organized?": (36, 42),
        "Damage, Loss, and Needs": (44, 48),
        "Types of Resources Needed for Disaster Relief": (50, 55),
        "Quantities of Essential Resources Required": (57, 61),
        "Resource Prioritization by Timeframe": (63, 66),
        "Resource Availability & Challenges": (68, 71),
        "Case Studies of Disaster Resource Distribution": (73, 76),
        "Data Sources for Disaster Resource Tracking": (78, 82),
        "Recommendations for Better Resource Distribution": (84, 87),
        "Immediate Actions and Long-Term Solutions": (89, 101),
        "Disaster Impact on Vulnerable Groups": (103, 106),
        "Aid Response Time in Major Cities": (108, 113),
        "Aid Response Time in Rural & Remote Areas": (115, 120),
        "Causes of Pakistan Flood": (122, 125),
    }

    # Extract and clean each section
    data = {}
    for section_name, (start_row, end_row) in sections.items():
        section_data = df.iloc[start_row:end_row, :].dropna(how="all")  # Drop empty rows
        if not section_data.empty:
            # Set the first row as column headers
            section_data.columns = section_data.iloc[0]
            section_data = section_data[1:].reset_index(drop=True)
            data[section_name] = section_data

    return data

# Load the data
data = load_data()

# Title of the dashboard
st.title("Disaster Relief Dashboard")

# Display all sections
for section_name, section_data in data.items():
    st.header(section_name)
    if isinstance(section_data, pd.DataFrame):
        st.dataframe(section_data)  # Use st.dataframe for DataFrames
    else:
        st.write(section_data)  # Use st.write for other data types

# Plot deaths by province (if the section exists)
if "Province-Wise Impact" in data:
    st.header("Deaths by Province")
    try:
        # Clean the "Deaths" column by removing non-numeric characters
        province_impact = data["Province-Wise Impact"].copy()
        province_impact["Deaths"] = province_impact["Deaths"].str.replace("~", "").str.replace(",", "").astype(float)

        # Plot the data
        fig, ax = plt.subplots()
        sns.barplot(x="Province", y="Deaths", data=province_impact, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error plotting data: {e}")
