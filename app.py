import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Healthcare Accessibility Dashboard",
    layout="wide"
)

st.title("Healthcare Accessibility Analysis - Chennai")

st.markdown("""
This dashboard presents:

- Existing hospital locations
- Underserved healthcare regions
- Proposed healthcare facility
- Accessibility improvement analysis
""")

# -----------------------------------
# Load GeoJSON Layers
# -----------------------------------

hospitals_dashboard = gpd.read_file(
    "hospitals_dashboard.geojson"
)

underserved_dashboard = gpd.read_file(
    "underserved_dashboard.geojson"
)

proposed_dashboard = gpd.read_file(
    "proposed_dashboard.geojson"
)

# -----------------------------------
# Create Map
# -----------------------------------

m = folium.Map(
    location=[13.08, 80.27],
    zoom_start=11
)

# Existing hospitals
for idx, row in hospitals_dashboard.iterrows():

    folium.CircleMarker(
        location=[
            row.geometry.y,
            row.geometry.x
        ],
        radius=4,
        color='blue',
        fill=True,
        fill_opacity=0.7,
        popup='Existing Hospital'
    ).add_to(m)

# Underserved regions
folium.GeoJson(
    underserved_dashboard,
    name='Underserved Regions'
).add_to(m)

# Proposed facility
for idx, row in proposed_dashboard.iterrows():

    folium.Marker(
        location=[
            row.geometry.y,
            row.geometry.x
        ],
        popup=(
            f"Proposed New Facility\n"
            f"Gap: {round(row['nearest_hospital_dist'],2)} m"
        ),
        icon=folium.Icon(color='green')
    ).add_to(m)

# Layer control
folium.LayerControl().add_to(m)

# Display map
st_folium(
    m,
    width=1200,
    height=700
)

# -----------------------------------
# Final Recommendation
# -----------------------------------

st.subheader("Final Recommendation")

st.write("""
Spatial analysis identified one strongly feasible healthcare facility location
that significantly improves accessibility within an underserved corridor while
avoiding redundant overlap with existing hospital coverage.
""")
