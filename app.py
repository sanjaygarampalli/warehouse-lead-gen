import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image

# --- INITIALIZATION ---
st.set_page_config(page_title="Samketan AI: Warehouse Leads", layout="wide")

# This keeps your results from disappearing!
if "search_results" not in st.session_state:
    st.session_state.search_results = None

# --- APP UI ---
st.title("🏗️ Samketan AI: Lead Generation")
st.markdown("Customize your warehouse requirements to find matching tenants.")

# 1. CUSTOMIZATION SECTION
with st.expander("🛠️ Customize Warehouse Requirements", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        w_name = st.text_input("Warehouse Name", value="Bhoodevi Warehouse")
        w_area = st.number_input("Built-up Area (sq ft)", value=21000)
        w_location = st.text_input("Location", value="Kalaburagi, Karnataka")
    
    with col2:
        industries = st.multiselect(
            "Target Industries", 
            ["FMCG", "Pharma", "E-commerce", "Logistics", "Manufacturing", "Packaging"],
            default=["FMCG", "Pharma"]
        )
        # PHOTO UPLOAD FEATURE
        uploaded_images = st.file_uploader("Upload Warehouse Photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Display uploaded photos immediately
if uploaded_images:
    st.subheader("📸 Warehouse Gallery")
    cols = st.columns(len(uploaded_images))
    for idx, img_file in enumerate(uploaded_images):
        img = Image.open(img_file)
        cols[idx].image(img, use_container_width=True, caption=f"Image {idx+1}")

# 2. SEARCH BUTTON
if st.button("🚀 Find & Verify Leads"):
    with st.spinner("Searching live data..."):
        # Simulated search logic (you can connect your API key here)
        mock_data = pd.DataFrame([
            {"Company": "Global Logistics Ltd", "Type": "3PL", "Contact": "+91 9900011122", "Match": "98%"},
            {"Company": "PurePharma Labs", "Type": "Pharma", "Contact": "+91 8877665544", "Match": "92%"},
            {"Company": "QuickPack Solutions", "Type": "Packaging", "Contact": "+91 7766554433", "Match": "85%"}
        ])
        st.session_state.search_results = mock_data

# 3. PERSISTENT RESULTS DISPLAY
if st.session_state.search_results is not None:
    st.divider()
    st.subheader("🎯 Best Match Leads")
    st.dataframe(st.session_state.search_results, use_container_width=True)
    
    # Map View
    st.subheader("📍 Proximity Analysis")
    m = folium.Map(location=[17.3297, 76.8343], zoom_start=12)
    folium.Marker([17.3297, 76.8343], popup=w_name, icon=folium.Icon(color='red', icon='warehouse', prefix='fa')).add_to(m)
    st_folium(m, width=1200, height=400)
    
    # Export
    csv = st.session_state.search_results.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Lead List", data=csv, file_name="warehouse_leads.csv", mime="text/csv")
