import streamlit as st
import pandas as pd
import requests
import os
import folium
import phonenumbers
from PyPDF2 import PdfReader
from streamlit_folium import st_folium  # Updated import
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Bhoodevi Warehouse Pro", layout="wide", page_icon="🏗️")

# --- MOCK DATA ---
def get_mock_leads():
    return pd.DataFrame([
        {"Company Name": "Bhoomi FMCG Distributors", "Industry": "FMCG", "Mobile": "+91 9845012345", "Address": "Kalaburagi", "Confidence": 0.95},
        {"Company Name": "Safe-Med Pharma", "Industry": "Pharma", "Mobile": "+91 8050067890", "Address": "Kalaburagi", "Confidence": 0.88}
    ])

# --- MAIN APP UI ---
def main():
    st.title("🏗️ Bhoodevi Warehouse: Lead Generator")
    
    # Sidebar for API Key
    with st.sidebar:
        st.header("🔑 Settings")
        # Direct link to Streamlit Secrets
        serp_key = st.secrets.get("SERPAPI_KEY")
        if not serp_key:
            st.warning("Running in Demo Mode. Add SERPAPI_KEY to Secrets for live data.")

    # Form
    col1, col2 = st.columns(2)
    with col1:
        w_name = st.text_input("Warehouse Name", "Bhoodevi Warehouse")
        w_area = st.number_input("Area (sq ft)", value=21000)
    with col2:
        target = st.multiselect("Target Industries", ["FMCG", "Pharma", "3PL"], default=["FMCG"])

    if st.button("🚀 Find Potential Clients"):
        st.balloons()
        df_results = get_mock_leads()
        st.subheader("🎯 Identified Lead Prospects")
        st.dataframe(df_results, use_container_width=True)

        # Map View
        st.subheader("📍 Location Intelligence")
        m = folium.Map(location=[17.2725, 76.8694], zoom_start=12)
        folium.Marker([17.2725, 76.8694], popup=w_name, icon=folium.Icon(color='red')).add_to(m)
        
        # Display map using st_folium
        st_folium(m, width=None, height=400, use_container_width=True)

if __name__ == "__main__":
    main()
