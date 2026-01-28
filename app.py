import streamlit as st
import pandas as pd
import folium
import re
from streamlit_folium import st_folium
from PyPDF2 import PdfReader
from PIL import Image

# --- INITIALIZATION ---
st.set_page_config(page_title="Samketan AI: Warehouse Lead Pro", layout="wide")

if "leads" not in st.session_state:
    st.session_state.leads = None
if "coords" not in st.session_state:
    st.session_state.coords = [17.2725, 76.8694] # Default start

# --- UTILITY: Extract Lat/Lng & Format Links ---
def extract_coords(text):
    match = re.search(r'@([-.\d]+),([-.\d]+)', text)
    if match: return [float(match.group(1)), float(match.group(2))]
    plain_match = re.search(r'([-.\d]+),\s*([-.\d]+)', text)
    if plain_match: return [float(plain_match.group(1)), float(plain_match.group(2))]
    return None

def format_linkedin(link):
    # Ensures the link always starts with https:// for the browser to open it
    if pd.isna(link) or link == "": return None
    link = str(link).strip()
    if not link.startswith("http"):
        return f"https://{link}"
    return link

# --- SIDEBAR: LOCATION & TARGET CLIENTS ---
with st.sidebar:
    st.header("📍 Warehouse Location")
    location_input = st.text_input("Paste Google Map Link or Coordinates", 
                                  placeholder="e.g. http://maps.google.com/...")
    
    if st.button("🔍 Locate Warehouse"):
        if location_input:
            new_coords = extract_coords(location_input)
            if new_coords:
                st.session_state.coords = new_coords
                st.success("Location Pin Updated!")
            else:
                st.error("Invalid link. Please use a full Google Maps URL.")

    # Sidebar map preview
    m_side = folium.Map(location=st.session_state.coords, zoom_start=15)
    folium.Marker(st.session_state.coords, icon=folium.Icon(color='red', icon='warehouse', prefix='fa')).add_to(m_side)
    st_folium(m_side, height=250, width=250, key="sidebar_map")

    st.divider()
    
    st.header("🎯 Target Client Selection")
    target_industry = st.selectbox("Select Target Industry", [
        "FMCG & Consumer Goods",
        "Pharma Distribution & Cold Chain Support",
        "E-Commerce Fulfilment",
        "Industrial Raw Materials Storage",
        "Agri & Food Grains Warehousing",
        "Automobile Parts, Electronics, Packaging Goods",
        "Third-Party Logistics (3PL)",
        "Commodity",
        "Small Manufacture",
        "Tire Industries",
        "Lubricant Automobile",
        "Any Government Agencies"
    ])

# --- MAIN INPUTS ---
st.title("🏗️ Samketan AI: Lead Generation")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Specifications")
    w_text = st.text_area("Requirement Details", placeholder="e.g. 21,000 sq ft, RCC flooring...")
    w_pdf = st.file_uploader("Upload Brochure (PDF)", type="pdf")

with col2:
    st.subheader("📸 Warehouse Media")
    w_photos = st.file_uploader("Upload Photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# --- SEARCH BUTTON ---
if st.button("🚀 Find Matching Leads"):
    with st.spinner(f"Analyzing {target_industry} leads..."):
        # Simulated Output - Ensuring URLs are correctly prefixed with https://
        data = [
            {
                "Company": "Bhoomi FMCG Pvt Ltd",
                "Type": "Distributor",
                "Position": "Proprietor",
                "Person Name": "Sanjay Kumar",
                "Person Mail ID": "mailto:contact@bhoodevi.in",
                "Person LinkedIn Profile ID": "https://www.linkedin.com/in/sanjay-kumar", # Full URL
                "Contact": "+91 9845000000",
                "Match": "98%"
            }
        ]
        st.session_state.leads = pd.DataFrame(data)

# --- OUTPUT TABLE ---
if st.session_state.leads is not None:
    st.divider()
    st.subheader("🎯 Identified Lead Prospects")
    
    # Apply link formatting to the LinkedIn column
    st.session_state.leads["Person LinkedIn Profile ID"] = st.session_state.leads["Person LinkedIn Profile ID"].apply(format_linkedin)
    
    st.dataframe(
        st.session_state.leads,
        column_config={
            "Person LinkedIn Profile ID": st.column_config.LinkColumn("LinkedIn Profile", display_text="Open Profile"),
            "Person Mail ID": st.column_config.LinkColumn("Email", display_text="Send Mail"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Result Map
    m_main = folium.Map(location=st.session_state.coords, zoom_start=13)
    folium.Marker(st.session_state.coords, popup="Warehouse Location", icon=folium.Icon(color='red')).add_to(m_main)
    st_folium(m_main, width=1300, height=450)
