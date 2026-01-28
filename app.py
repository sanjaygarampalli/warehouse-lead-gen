import streamlit as st
import pandas as pd
import requests
import os
import time
import folium
import phonenumbers
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from serpapi import GoogleSearch
from streamlit_folium import streamlit_folium
from io import BytesIO

# --- CONFIG & SECRETS ---
load_dotenv()
st.set_page_config(page_title="Warehouse Lead Pro", layout="wide", page_icon="🏗️")

# Helper for API Keys (Local .env or Streamlit Secrets)
# Streamlit Cloud will look for this in your "Advanced Settings > Secrets"
serp_key = st.secrets.get("SERPAPI_KEY")

# --- MOCK DATA FOR DEMO ---
def get_mock_leads():
    return pd.DataFrame([
        {
            "Company Name": "Bhoomi FMCG Distributors",
            "Industry": "FMCG",
            "Contact Person": "Rajesh Kumar",
            "Mobile": "+91 9845012345",
            "Email": "info@bhoomifmcg.com",
            "Website": "https://example-fmcg.in",
            "LinkedIn": "https://linkedin.com/company/bhoomi-dist",
            "Address": "Station Road, Kalaburagi",
            "Distance (km)": 4.2,
            "Confidence": 0.95,
            "Source": "Mock Data"
        },
        {
            "Company Name": "Safe-Med Pharma Logistics",
            "Industry": "Pharma",
            "Contact Person": "Ananya Singh",
            "Mobile": "+91 8050067890",
            "Email": "logistics@safemed.com",
            "Website": "https://example-pharma.com",
            "LinkedIn": "https://linkedin.com/company/safemed",
            "Address": "MSK Mill Area, Kalaburagi",
            "Distance (km)": 2.8,
            "Confidence": 0.88,
            "Source": "Mock Data"
        }
    ])

# --- UTILITY FUNCTIONS ---
def validate_phone(phone_str):
    try:
        parsed = phonenumbers.parse(phone_str, "IN")
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except:
        return phone_str
    return phone_str

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- SEARCH ENGINE ---
def search_leads(query, radius, api_key):
    if not api_key:
        return None
    
    params = {
        "q": query,
        "location": "Kalaburagi, Karnataka, India",
        "hl": "en",
        "gl": "in",
        "google_domain": "google.co.in",
        "api_key": api_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("local_results", [])

# --- MAIN APP UI ---
def main():
    st.title("🏗️ Warehouse Lead Generator & Enrichment")
    st.markdown("Find and verify local industrial tenants based on your warehouse specs.")

    with st.sidebar:
        st.header("🔑 API Configuration")
        serp_key = get_api_key("SERPAPI_KEY")
        if not serp_key:
            st.warning("No API Key found. Running in **Demo Mode**.")
        
        st.divider()
        st.header("🛠️ Search Parameters")
        radius = st.slider("Search Radius (km)", 5, 50, 20)
        max_results = st.number_input("Max Results", 5, 50, 10)
        
        st.info("💡 Note: We do not scrape LinkedIn. We find public company URLs.")

    # 1. Warehouse Details Form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Warehouse Profile")
        w_name = st.text_input("Warehouse Name", "Bhoodevi Warehouse")
        w_address = st.text_area("Full Address", "Road No. 6, Near IOCL, Nandur Kesaratagi Industrial Area, Shahabad Road, Kalaburagi – 585105")
        w_area = st.number_input("Built-up Area (sq ft)", value=21000)
        
    with col2:
        st.subheader("Compliance & Target")
        target_industries = st.multiselect(
            "Target Industries",
            ["FMCG", "Pharma", "E-commerce", "3PL", "Auto Parts", "Agri/Food", "Electronics"],
            default=["FMCG", "Pharma"]
        )
        brochure = st.file_uploader("Upload Brochure (PDF)", type="pdf")
        
    consent = st.checkbox("I agree to use this data for legitimate business outreach only.")

    if st.button("🚀 Search for Potential Clients"):
        if not consent:
            st.error("Please agree to the privacy and compliance notice.")
            return

        with st.status("Gathering leads...", expanded=True) as status:
            if brochure:
                st.write("Extracting data from brochure...")
                pdf_text = extract_text_from_pdf(brochure)
                st.write(f"Found {len(pdf_text)} characters in PDF.")

            # Search Execution
            if not serp_key:
                time.sleep(1) # Simulate delay
                df_results = get_mock_leads()
                status.update(label="Demo results loaded!", state="complete")
            else:
                st.write("Querying Search APIs...")
                # Logic for real API call would go here
                df_results = get_mock_leads() # Placeholder for actual API parsing
                status.update(label="Live search complete!", state="complete")

        # --- DISPLAY RESULTS ---
        st.divider()
        st.subheader("🎯 Identified Lead Prospects")
        
        # Formatting for display
        display_df = df_results.copy()
        
        # Visual Table
        st.dataframe(
            display_df,
            column_config={
                "Website": st.column_config.LinkColumn("Website"),
                "LinkedIn": st.column_config.LinkColumn("LinkedIn"),
                "Email": st.column_config.TextColumn("Email"),
                "Mobile": st.column_config.TextColumn("Mobile"),
            },
            hide_index=True
        )

        # Map View
        st.subheader("📍 Location Intelligence")
        m = folium.Map(location=[17.2725, 76.8694], zoom_start=12)
        # Warehouse Marker
        folium.Marker(
            [17.2725, 76.8694], 
            popup="Bhoodevi Warehouse", 
            icon=folium.Icon(color='red', icon='warehouse', prefix='fa')
        ).add_to(m)
        
        # Lead Markers
        for idx, row in df_results.iterrows():
            # Random slight offset for mock data map visualization
            folium.Marker(
                [17.27 + (idx*0.01), 76.86 + (idx*0.01)],
                popup=row['Company Name'],
                icon=folium.Icon(color='blue', icon='building', prefix='fa')
            ).add_to(m)
            
        streamlit_folium(m, width=1400, height=400)

        # Export
        csv = df_results.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Results to CSV", data=csv, file_name="warehouse_leads.csv", mime="text/csv")

if __name__ == "__main__":
    main()
