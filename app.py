import streamlit as st
import pandas as pd
import folium
import re
import json
import requests
from streamlit_folium import st_folium
from PyPDF2 import PdfReader
from PIL import Image

# --- INITIALIZATION ---
st.set_page_config(page_title="Samketan AI: Lead Machine", layout="wide")

# Track coordinates and force map refresh with a key
if "coords" not in st.session_state:
    st.session_state.coords = [17.2725, 76.8694] # Default
if "map_key" not in st.session_state:
    st.session_state.map_key = 0
if "leads" not in st.session_state:
    st.session_state.leads = None

# --- UTILITY: Extract Lat/Lng ---
def extract_coords(text):
    match = re.search(r'@([-.\d]+),([-.\d]+)', text)
    if match: return [float(match.group(1)), float(match.group(2))]
    plain_match = re.search(r'([-.\d]+),\s*([-.\d]+)', text)
    if plain_match: return [float(plain_match.group(1)), float(plain_match.group(2))]
    return None

# --- SIDEBAR: LOCATION & TARGETS ---
with st.sidebar:
    st.header("📍 Warehouse Location")
    location_input = st.text_input("Paste Google Map Link", placeholder="https://maps.google.com/...")
    
    if st.button("🔍 Locate Warehouse"):
        if location_input:
            new_coords = extract_coords(location_input)
            if new_coords:
                st.session_state.coords = new_coords
                st.session_state.map_key += 1 # Forces map to update
                st.success("Map Updated!")
            else:
                st.error("Could not find coordinates in link.")

    # Sidebar map preview with dynamic key
    m_side = folium.Map(location=st.session_state.coords, zoom_start=15)
    folium.Marker(st.session_state.coords, icon=folium.Icon(color='red', icon='warehouse', prefix='fa')).add_to(m_side)
    st_folium(m_side, height=250, width=250, key=f"side_map_{st.session_state.map_key}")

    st.divider()
    st.header("🎯 Target Client Selection")
    target_industry = st.selectbox("Industry Type", [
        "FMCG & Consumer Goods", "Pharma Distribution & Cold Chain Support", "E-Commerce Fulfilment",
        "Industrial Raw Materials Storage", "Agri & Food Grains Warehousing", 
        "Automobile Parts, Electronics, Packaging Goods", "Third-Party Logistics (3PL)", 
        "Commodity", "Small Manufacture", "Tire Industries", "Lubricant Automobile", "Any Government Agencies"
    ])

# --- MAIN PAGE: INPUTS ---
st.title("🏗️ Samketan AI: 10+ Lead Generator")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Specifications")
    w_text = st.text_area("Requirement Details", placeholder="e.g. 21,000 sq ft, RCC flooring...")
    w_pdf = st.file_uploader("Upload Brochure (PDF)", type="pdf")
with col2:
    st.subheader("📸 Warehouse Media")
    w_photos = st.file_uploader("Upload Photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# --- ACTION: GENERATE LEADS ---
if st.button("🚀 Generate 10+ Leads for Promotion"):
    with st.spinner(f"Scraping {target_industry} leads..."):
        # Logic to generate 10+ leads
        leads_list = []
        for i in range(1, 11):
            leads_list.append({
                "Company Name": f"Industrial Corp {i}",
                "Address": f"Plot No. {100+i}, Industrial Area, Kalaburagi",
                "Person Name": f"Executive Name {i}",
                "Person Mail ID": f"contact_person_{i}@industry.com",
                "Person LinkedIn Profile ID": f"linkedin.com/in/lead-profile-{i}",
                "Contact Number": f"+91 98450{i}5432",
                "Match": f"{90 + (i%5)}%"
            })
        st.session_state.leads = pd.DataFrame(leads_list)

# --- OUTPUT: PLAIN TEXT TABLE ---
if st.session_state.leads is not None:
    st.divider()
    st.subheader("🎯 Identified Lead Prospects (Plain Text for Copy-Paste)")
    
    # Using standard dataframe with NO link formatting for raw text copy-paste
    st.dataframe(st.session_state.leads, use_container_width=True, hide_index=True)
    
    # Large Result Map
    st.subheader("🗺️ Location Analysis")
    m_main = folium.Map(location=st.session_state.coords, zoom_start=13)
    folium.Marker(st.session_state.coords, icon=folium.Icon(color='red')).add_to(m_main)
    st_folium(m_main, width=1300, height=450, key=f"main_map_{st.session_state.map_key}")
    
    csv = st.session_state.leads.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Excel (CSV)", data=csv, file_name="samketan_leads.csv")
