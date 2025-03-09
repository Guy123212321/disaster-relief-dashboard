import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1dEzzG4yXoZTEW_g6LIblTepdLpiT6DfGnbquQhJ6f1Q/gviz/tq?tqx=out:csv"

@st.cache_data
def load_data():
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
        infra_damage["Estimated Cost (USD)"]
        .astype(str)
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
            province_impact[col]
            .astype(str)
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
    # 7. Damage/Loss/Needs (Critical Fix)
    # ----------------------------
    damage_loss = df.iloc[44:48, :7].copy()
    damage_loss.columns = [
        "Region", "Damage (PKR Billion)", "Damage (USD Million)", "Loss (PKR Billion)",
        "Loss (USD Million)", "Needs (PKR Billion)", "Needs (USD Million)"
    ]

    for col in damage_loss.columns[1:]:
        damage_loss[col] = (
            damage_loss[col]
            .astype(str)
            .str.replace(r'[^\d.]', '', regex=True)
            .replace(r'^\.$', np.nan, regex=True)
            .pipe(pd.to_numeric, errors='coerce')
        )
    data["Damage Analysis"] = damage_loss.dropna(how='all')

    # ----------------------------
    # Enhanced Visualization
    # ----------------------------
    if "Province-Wise Impact" in data and not data["Province-Wise Impact"].empty:
        province_data = data["Province-Wise Impact"]
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#2ecc71' if x < province_data['Deaths'].median() else '#e74c3c' for x in province_data['Deaths']]
        bars = ax.bar(province_data['Province'], province_data['Deaths'], color=colors, edgecolor='white')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:,.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)

        ax.set_title('Flood Casualties by Province\nPakistan 2022 Floods', fontsize=14, pad=20, fontweight='bold')
        ax.set_ylabel('Number of Deaths', labelpad=15)
        ax.set_xlabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.text(0.5, -0.3, "Critical Need: Sindh province accounts for 46% of total deaths\nData Source: NDMA",
                transform=ax.transAxes, ha='center', fontsize=9, color='#7f8c8d')

        data["Casualty Analysis"] = fig

    return data

data = load_data()

