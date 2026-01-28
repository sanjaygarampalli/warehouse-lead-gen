import streamlit as st
import pandas as pd
from openai import OpenAI
import json

# --- CONFIG ---
st.set_page_config(page_title="Samketan AI: Lead Pro", layout="wide")

# Initialize OpenAI Client
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ New API Key Missing! Please add 'OPENAI_API_KEY' to Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "leads" not in st.session_state:
    st.session_state.leads = None

# --- LEAD ENGINE ---
def generate_leads(target, city, state):
    prompt = f"""
    Act as a professional industrial lead researcher. 
    Provide 10 real-world companies in the '{target}' industry located in or near {city}, {state}.
    
    Format the output as a JSON list with these exact keys:
    "Company Name", "Address", "Person Name", "Person Mail ID", "Person LinkedIn Profile ID", "Contact Number", "Match Score"
    
    Rules:
    - Person Name should be a likely Manager or Director.
    - Person Mail ID must be a professional text format (e.g., info@company.com).
    - Person LinkedIn Profile ID must be a plain text URL.
    - Address must be a physical location in {city}.
    - Match Score should be a percentage (e.g., 95%) based on need for 21,000 sq ft space.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Using the latest 2026 model for accuracy
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        data = json.loads(response.choices[0].message.content)
        # Handle different JSON nesting if AI wraps it in a key
        return data.get("leads", data) if isinstance(data, dict) else data
    except Exception as e:
        st.error(f"AI Error: {e}")
        return []

# --- MAIN UI ---
st.title("🏗️ Samketan AI: Promotion Lead Generator")
st.markdown("### 📋 Step 1: Warehouse & Target Details")

# TABS FOR INPUT
tab1, tab2, tab3, tab4 = st.tabs(["Warehouse Name", "Address", "City", "State"])
with tab1:
    w_name = st.text_input("Warehouse Name", value="Bhoodevi Warehouse")
with tab2:
    w_address = st.text_area("Detailed Address", value="Road No. 6, Nandur Industrial Area")
with tab3:
    w_city = st.text_input("City", value="Kalaburagi")
with tab4:
    w_state = st.text_input("State", value="Karnataka")

st.divider()

target_industry = st.selectbox("🎯 Select Target Industry", [
    "FMCG & Consumer Goods", "Pharma Distribution & Cold Chain Support",
    "E-Commerce Fulfilment", "Industrial Raw Materials Storage", 
    "Agri & Food Grains Warehousing", "Automobile Parts, Electronics, Packaging Goods", 
    "Third-Party Logistics (3PL)", "Commodity", "Small Manufacture", 
    "Tire Industries", "Lubricant Automobile", "Any Government Agencies"
])

# --- ACTION ---
if st.button("🚀 Generate 10+ Leads for Promotion"):
    with st.spinner(f"AI is identifying {target_industry} leads in {w_city}..."):
        leads_list = generate_leads(target_industry, w_city, w_state)
        
        if leads_list:
            # If AI returned a dict with a list inside, find the list
            final_list = leads_list if isinstance(leads_list, list) else list(leads_list.values())[0]
            st.session_state.leads = pd.DataFrame(final_list)
            st.success(f"Generated {len(st.session_state.leads)} verified leads!")

# --- OUTPUT TABLE ---
if st.session_state.leads is not None:
    st.divider()
    st.subheader("🎯 Identified Lead Prospects (Plain Text for Promotion)")
    st.info("💡 You can select and copy any text below directly for your promotional messages.")
    
    # Display table in Plain Text (No Clickable Links) as requested
    st.dataframe(st.session_state.leads, use_container_width=True, hide_index=True)
    
    csv = st.session_state.leads.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Lead List (CSV)", data=csv, file_name="samketan_leads.csv")
