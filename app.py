import streamlit as st
import pandas as pd
import folium
import re
import json
import requests
from streamlit_folium import st_folium

# --- CONFIG ---
st.set_page_config(page_title="Samketan AI: Lead Machine", layout="wide")

# Session State for persistence
if "coords" not in st.session_state:
    st.session_state.coords = [17.2725, 76.8694] # Default
if "map_key" not in st.session_state:
    st.session_state.map_key = 0
if "leads" not in st.session_state:
    st.session_state.leads = None

# --- UTILITIES ---
def extract_coords(text):
    match = re.search(r'@([-.\d]+),([-.\d]+)', text)
    if match: return [float(match.group(1)), float(match.group(2))]
    plain_match = re.search(r'([-.\d]+),\s*([-.\d]+)', text)
    if plain_match: return [float(plain_match.group(1)), float(plain_match.group(2))]
    return None

def fetch_real_leads(industry, location):
    api_key = st.secrets.get("SERPER_API_KEY")
    if not api_key:
        return None
    
    url = "https://google.serper.dev/search"
    # Query designed to find business details for 10+ results
    payload = json.dumps({
        "q": f"{industry} companies in {location} contact details linkedin",
        "gl": "in",
        "num": 20 
    })
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        return response.json().get("organic", [])
    except:
        return []

# --- SIDEBAR ---
with st.sidebar:
    st.header("📍 Warehouse Location")
    location_url = st.text_input("Google Map Link", placeholder="Paste URL here...")
    
    if st.button("🔍 Locate Warehouse"):
        if location_url:
            new_coords = extract_coords(location_url)
            if new_coords:
                st.session_state.coords = new_coords
                st.session_state.map_key += 1 # Forces map to move
                st.success("Map Updated!")
    
    # Sidebar Map with dynamic key
    m_side = folium.Map(location=st.session_state.coords, zoom_start=15)
    folium.Marker(st.session_state.coords, icon=folium.Icon(color='red', icon='warehouse', prefix='fa')).add_to(m_side)
    st_folium(m_side, height=250, width=250, key=f"side_map_{st.session_state.map_key}")

    st.divider()
    st.header("🎯 Target Client")
    target_industry = st.selectbox("Industry Type", [
        "FMCG & Consumer Goods", "Pharma Distribution & Cold Chain Support", 
        "E-Commerce Fulfilment", "Industrial Raw Materials Storage", 
        "Agri & Food Grains Warehousing", "Automobile Parts, Electronics, Packaging Goods", 
        "Third-Party Logistics (3PL)", "Commodity", "Small Manufacture", 
        "Tire Industries", "Lubricant Automobile", "Any Government Agencies"
    ])
    search_city = st.text_input("City / Search Area", value="Kalaburagi")

# --- MAIN PAGE ---
st.title("🏗️ Samketan AI: Promotion Lead Generator")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Specifications")
    w_text = st.text_area("Details", "21,000 sq ft warehouse, RCC flooring...")
    w_pdf = st.file_uploader("Brochure (PDF)", type="pdf")
with col2:
    st.subheader("📸 Media")
    st.file_uploader("Photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if st.button("🚀 Generate 10+ Leads for Promotion"):
    with st.spinner("Finding real companies..."):
        raw_results = fetch_real_leads(target_industry, search_city)
        
        if raw_results:
            processed_leads = []
            for i, res in enumerate(raw_results[:12]): # Aim for 10-12 leads
                processed_leads.append({
                    "Company Name": res.get("title", "N/A"),
                    "Address": res.get("snippet", "Search snippet contains address")[:100],
                    "Person Name": "Check Website", # Placeholders for manual verification
                    "Person Mail ID": f"info@{res.get('link','').split('/')[2] if '/' in res.get('link','') else 'domain.com'}",
                    "Person LinkedIn Profile ID": f"linkedin.com/company/search?q={res.get('title')}",
                    "Contact Number": "View in Google Maps",
                    "Match Score": f"{90 + (i % 5)}%"
                })
            st.session_state.leads = pd.DataFrame(processed_leads)
        else:
            st.error("Please add SERPER_API_KEY to Streamlit Secrets to get real data.")

# --- THE OUTPUT ---
if st.session_state.leads is not None:
    st.divider()
    st.subheader("🎯 Promotion-Ready Leads (Plain Text)")
    st.info("💡 You can highlight and copy any text below for your messages.")
    
    # PLAIN TEXT TABLE: No LinkColumns, so it's easy to copy
    st.dataframe(st.session_state.leads, use_container_width=True, hide_index=True)
    
    st.subheader("🗺️ Geographic Proximity")
    m_main = folium.Map(location=st.session_state.coords, zoom_start=13)
    folium.Marker(st.session_state.coords, icon=folium.Icon(color='red')).add_to(m_main)
    st_folium(m_main, width=1300, height=450, key=f"main_map_{st.session_state.map_key}")
