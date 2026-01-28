import streamlit as st
import pandas as pd
import folium
import re
from streamlit_folium import st_folium
from PyPDF2 import PdfReader
from PIL import Image

# --- INITIALIZATION ---
st.set_page_config(page_title="Samketan AI: Lead Pro", layout="wide")

if "leads" not in st.session_state:
    st.session_state.leads = None
if "coords" not in st.session_state:
    st.session_state.coords = [17.2725, 76.8694] # Default start

# --- UTILITY: Extract Lat/Lng from Google Maps URL ---
def extract_coords(text):
    # Matches @lat,lng or coordinates in the URL
    match = re.search(r'@([-.\d]+),([-.\d]+)', text)
    if match:
        return [float(match.group(1)), float(match.group(2))]
    # Fallback for plain "lat, lng" text input
    plain_match = re.search(r'([-.\d]+),\s*([-.\d]+)', text)
    if plain_match:
        return [float(plain_match.group(1)), float(plain_match.group(2))]
    return None

# --- SIDEBAR: GOOGLE MAP TAB ---
with st.sidebar:
    st.header("📍 Warehouse Location")
    st.info("Paste your Google Maps link or Lat/Long coordinates below.")
    
    location_input = st.text_input("Google Map Link / Coordinates", 
                                  placeholder="https://www.google.com/maps/@17.27,76.86...")
    
    if location_input:
        new_coords = extract_coords(location_input)
        if new_coords:
            st.session_state.coords = new_coords
            st.success("Location updated successfully!")
    
    # Visual confirmation map
    st.write("Current Pin:")
    m_side = folium.Map(location=st.session_state.coords, zoom_start=15)
    folium.Marker(st.session_state.coords, icon=folium.Icon(color='red', icon='warehouse', prefix='fa')).add_to(m_side)
    st_folium(m_side, height=250, width=250, key="sidebar_map")

# --- MAIN PAGE: INPUTS ---
st.title("🏗️ Samketan AI: Lead Generation")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Warehouse Details")
    w_text = st.text_area("Requirement Details (Text)", placeholder="e.g. 21,000 sq ft, RCC flooring, 30ft height...")
    w_pdf = st.file_uploader("Upload Brochure (PDF)", type="pdf")

with col2:
    st.subheader("📸 Visuals")
    w_photos = st.file_uploader("Upload Warehouse Photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if w_photos:
        st.write(f"✅ {len(w_photos)} photos ready for processing.")

# --- ACTION BUTTON ---
if st.button("🚀 Find Matching Clients"):
    with st.spinner("AI is analyzing requirements and matching tenants..."):
        # This simulates the AI result based on your input
        st.session_state.leads = pd.DataFrame([
            {
                "Company": "Bhoomi FMCG Pvt Ltd",
                "Type": "Distributor",
                "Position": "Proprietor",
                "Person Name": "Sanjay Kumar",
                "Person Mail ID": "contact@bhoodevi.in",
                "Person LinkedIn Profile ID": "linkedin.com/in/sanjay-kumar",
                "Contact": "+91 9845000000",
                "Match": "98%"
            },
            {
                "Company": "Retail Giant India",
                "Type": "E-commerce",
                "Position": "Logistics Manager",
                "Person Name": "Rahul Sharma",
                "Person Mail ID": "rahul.s@retail.com",
                "Person LinkedIn Profile ID": "linkedin.com/in/rahul-logs",
                "Contact": "+91 8050011223",
                "Match": "92%"
            }
        ])

# --- OUTPUT TABLE ---
if st.session_state.leads is not None:
    st.divider()
    st.subheader("🎯 Identified Lead Prospects")
    
    # Displaying exactly the columns you requested
    st.dataframe(
        st.session_state.leads,
        column_config={
            "Person LinkedIn Profile ID": st.column_config.LinkColumn("LinkedIn Profile"),
            "Person Mail ID": st.column_config.TextColumn("Email"),
            "Match": st.column_config.TextColumn("AI Match Score")
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Large Map Visualization
    st.subheader("🗺️ Proximity Analysis")
    m_main = folium.Map(location=st.session_state.coords, zoom_start=13)
    folium.Marker(st.session_state.coords, popup="Warehouse", icon=folium.Icon(color='red')).add_to(m_main)
    st_folium(m_main, width=1300, height=450)
    
    # Export Option
    csv = st.session_state.leads.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Lead List (CSV)", data=csv, file_name="samketan_leads.csv", mime="text/csv")
