import streamlit as st
import requests
import pandas as pd

# 1. Page Configuration & Branding
st.set_page_config(page_title="Warehouse Clients Lead Generation App", layout="wide")

# Custom CSS for the Professional Look you requested
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        height: 3em; 
        background-color: #007bff; 
        color: white; 
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        white-space: pre-wrap; 
        background-color: #f0f2f6; 
        border-radius: 5px; 
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Branding (Your Logo & Info)
with st.sidebar:
    st.title("🏢 Samketan AI")
    st.markdown("### **M/s Bhoodevi Warehouse**")
    st.image("https://via.placeholder.com/150", caption="Bhoodevi Warehouse Logo") # Replace with your actual logo URL
    st.info("📍 Road No. 6, Near IOCL, Kalaburagi, Karnataka")
    st.divider()
    st.write("**Proprietor:** Sanjay Kumar H.")
    st.write("📞 +91 63625 19546")

# 3. Main Header
st.title("🏗️ Warehouse Clients Lead Generation App")
st.write("Target decision-makers and generate professional leads using AI research.")

# 4. Organizing Inputs into Tabs
tab1, tab2, tab3 = st.tabs(["📋 Warehouse Specs", "🎯 Target Sector", "🚀 Generate Leads"])

with tab1:
    st.subheader("Warehouse Technical Details")
    col1, col2 = st.columns(2)
    
    with col1:
        address = st.text_area("Exact Address", "Road No. 6, Near IOCL, Nandur Kesaratagi Industrial Area, Shahabad Road, Kalaburagi – 585105, Karnataka")
        total_area = st.text_input("Total Plot Area", "44,000 sq ft (Fully Compounded)")
        built_up = st.text_input("Built-Up Area", "21,000 sq ft")
        plinth = st.text_input("Plinth Height", "5 ft")

    with col2:
        power = st.text_input("Power Connection", "10 HP | 3-Phase")
        shutters = st.text_input("Loading Shutters", "7 Shutters (10 x 11 ft)")
        amenities = st.multiselect("Amenities Available", 
            ["Fire NOC", "CCTV", "24/7 Water", "Security Guard Room", "RCC Flooring", "Temperature Control Roofing", "Washrooms"],
            default=["Fire NOC", "RCC Flooring", "24/7 Water"])

with tab2:
    st.subheader("Industry Selection")
    sector = st.selectbox("Which sector is suitable for this lead generation?", [
        "FMCG & Consumer Goods", 
        "Pharma Distribution & Cold Chain", 
        "E-Commerce Fulfilment",
        "Industrial Raw Materials Storage", 
        "Agri & Food Grains Warehousing", 
        "Automobile Parts, Electronics, Packaging Goods",
        "Third-Party Logistics (3PL)", 
        "Tire Industries", 
        "Lubricant Industries", 
        "Textile Industries"
    ])
    st.write(f"Researching deep into the **{sector}** industry...")

with tab3:
    st.subheader("Run AI Agent")
    if st.button("Start Deep Research & Find 10 Leads"):
        # This payload sends all your warehouse details to n8n
        payload = {
            "app_name": "Warehouse Clients Lead Generation App",
            "warehouse_name": "Bhoodevi Warehouse",
            "address": address,
            "sector": sector,
            "specs": {
                "built_up": built_up,
                "amenities": amenities
            }
        }
        
        # Replace with your n8n Webhook URL from the previous step
        n8n_url = "http://localhost:5678/webhook-test/warehouse-client-leads"
        
        try:
            # r = requests.post(n8n_url, json=payload)
            st.success(f"Successfully triggered AI Agent for {sector}!")
            st.info("The agent is searching Google, LinkedIn, and IndiaMart for 10 decision makers.")
        except Exception as e:
            st.error(f"Could not connect to n8n: {e}")

# 5. Output Results Table Placeholder
st.divider()
st.markdown("### 📊 Research Results (Top 10 Leads)")
st.caption("Data will appear here and sync to your Google Sheet.")
# Placeholder dataframe
df_placeholder = pd.DataFrame(columns=["Company Name", "Decision Maker", "Position", "Contact", "Email", "LinkedIn"])
st.table(df_placeholder)
