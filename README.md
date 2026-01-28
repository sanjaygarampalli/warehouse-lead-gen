# 🏗️ AI Warehouse Lead Generator

A specialized Streamlit application for warehouse owners to identify, analyze, and contact potential business clients. This tool is designed to find a variety of tenants, from large-scale storage users to small manufacturers and packaging units.

## 🌟 Key Features
- **Flexible Lead Discovery:** Search for a wide range of industries including:
    - **Storage & Warehousing:** 3PL, E-commerce, and regional distribution centers.
    - **Manufacturing:** Small-scale manufacturers and local industrial units.
    - **Packaging:** Industrial packaging and assembly services.
- **Visual Warehouse Profile:** - Upload high-resolution photos of the facility.
    - Attach PDF brochures for automated detail extraction.
- **Location Intelligence:** - Integrates with Google Maps to show the exact warehouse location.
    - Finds prospects within a custom radius (5km to 100km).
- **Export Ready:** Generate and download a CSV list of leads with verified contact details.

## 🛠️ Setup & Deployment
1. **API Keys:** This app requires a `SERPAPI_KEY` (or Serper.dev) for real-time lead searches.
2. **Secrets:** In Streamlit Community Cloud, add your keys under **Advanced Settings > Secrets**.
3. **Local Run:** ```bash
   pip install -r requirements.txt
   streamlit run app.py
