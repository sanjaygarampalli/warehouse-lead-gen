import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PyPDF2 import PdfReader
from PIL import Image
import io

# --- APP CONFIG ---
st.set_page_config(page_title="Samketan AI: Lead Pro", layout="wide", page_icon="🏗️")

if "leads" not in st.session_state:
    st.session_state.leads = None

# --- UI HEADER ---
st.title("🏗️ Samketan AI: Warehouse Lead Generator")
st.write("Input your warehouse details to find and verify the best matching tenants.")

# --- INPUT SECTION ---
with st.sidebar:
    st.header("📍 Warehouse Geography")
    st.write("Click on the map to set your warehouse coordinates.")
    m_input = folium.Map(location=[17.3297, 76.8343], zoom_start=12)
    m_input.add_child(folium.LatLngPopup())
    map_data = st_folium(m_input, height=300, width=300)
    
    # Capture Coordinates
    lat, lng = 17.3297, 76.8343
    if map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]
    st.success(f"Coordinates: {lat:.4f}, {lng:.4f}")

st.subheader("📝 Warehouse Specifications")
col1, col2 = st.columns(2)

with col1:
    w_text = st.text_area("Describe your Warehouse (Text Input)", 
                          placeholder="Example: 21,000 sq ft RCC warehouse in Kalaburagi with 4 loading docks...")
    w_pdf = st.file_uploader("Upload Warehouse Brochure (PDF)", type="pdf")

with col2:
    w_photos = st.file_uploader("Upload Warehouse Photos (Optional)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if w_photos:
        st.write(f"✅ {len(w_photos)} photos uploaded.")

# --- PROCESSING LOGIC ---
if st.button("🚀 Generate Matching Leads"):
    with st.spinner("Analyzing requirements and searching web..."):
        # Placeholder for AI logic that parses PDF/Text and searches via Serper API
        # Output columns as requested by the user
        st.session_state.leads = pd.DataFrame([
            {
                "Company": "Bhoomi FMCG Pvt Ltd",
                "Type": "Distributor",
                "Position": "Supply Chain Manager",
                "Person Name": "Sanjay G",
                "Person Mail ID": "sanjay@bhoomi.in",
                "Person LinkedIn Profile ID": "linkedin.com/in/sanjayg",
                "Contact": "+91 9845000000",
                "Match": "98%"
            },
            {
                "Company": "Safe-Med Pharma",
                "Type": "Manufacturing",
                "Position": "Logistics Head",
                "Person Name": "Ananya Rao",
                "Person Mail ID": "arao@safemed.com",
                "Person LinkedIn Profile ID": "linkedin.com/in/arao-logs",
                "Contact": "+91 8050011122",
                "Match": "92%"
            }
        ])

# --- OUTPUT SECTION ---
if st.session_state.leads is not None:
    st.divider()
    st.subheader("🎯 Identified Lead Prospects")
    
    # The requested output table
    st.dataframe(
        st.session_state.leads,
        column_config={
            "Person LinkedIn Profile ID": st.column_config.LinkColumn("LinkedIn"),
            "Person Mail ID": st.column_config.TextColumn("Email"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Map Visualization
    st.subheader("🗺️ Proximity Map")
    m_output = folium.Map(location=[lat, lng], zoom_start=13)
    folium.Marker([lat, lng], popup="Your Warehouse", icon=folium.Icon(color='red', icon='warehouse', prefix='fa')).add_to(m_output)
    st_folium(m_output, width=1300, height=400)
    
    # Download
    csv = st.session_state.leads.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Lead List to CSV", data=csv, file_name="warehouse_leads.csv", mime="text/csv")
