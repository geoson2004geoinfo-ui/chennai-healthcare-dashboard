import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Healthcare Accessibility Dashboard",
    layout="wide"
)

st.title("Healthcare Accessibility Analysis - Chennai")

st.markdown("""
This interactive dashboard presents:

- Existing hospital locations
- Healthcare access zones
- Underserved healthcare regions
- Demand-supply accessibility gaps
- Proposed healthcare facility intervention
- Before vs after accessibility improvement
""")

# -----------------------------------
# Load Spatial Layers
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

access_zones = gpd.read_file(
    "access_zones.geojson"
)

# -----------------------------------
# Create Base Map
# -----------------------------------

m = folium.Map(
    location=[13.08, 80.27],
    zoom_start=11,
    control_scale=True
)

# -----------------------------------
# Existing Hospitals Layer
# -----------------------------------

hospital_layer = folium.FeatureGroup(
    name='Existing Hospitals',
    show=True
)

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
    ).add_to(hospital_layer)

hospital_layer.add_to(m)

# -----------------------------------
# Access Zones Layer
# -----------------------------------

access_layer = folium.FeatureGroup(
    name='Access Zones',
    show=True
)

folium.GeoJson(
    access_zones,
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'blue',
        'weight': 1,
        'fillOpacity': 0.1
    }
).add_to(access_layer)

access_layer.add_to(m)

# -----------------------------------
# Underserved Regions Layer
# -----------------------------------

underserved_layer = folium.FeatureGroup(
    name='Underserved Regions',
    show=True
)

folium.GeoJson(
    underserved_dashboard,
    style_function=lambda x: {
        'fillColor': 'red',
        'color': 'red',
        'weight': 1,
        'fillOpacity': 0.2
    }
).add_to(underserved_layer)

underserved_layer.add_to(m)

# -----------------------------------
# Proposed Facility Layer
# -----------------------------------

proposed_layer = folium.FeatureGroup(
    name='Proposed Healthcare Facility',
    show=True
)

for idx, row in proposed_dashboard.iterrows():

    folium.Marker(
        location=[
            row.geometry.y,
            row.geometry.x
        ],
        popup=(
            f"Proposed Healthcare Facility<br>"
            f"Nearest Hospital Gap: "
            f"{round(row['nearest_hospital_dist'],2)} meters"
        ),
        icon=folium.Icon(
            color='green',
            icon='plus-sign'
        )
    ).add_to(proposed_layer)

proposed_layer.add_to(m)

# -----------------------------------
# Layer Control
# -----------------------------------

folium.LayerControl(
    position='topright',
    collapsed=True
).add_to(m)

# -----------------------------------
# Display Map
# -----------------------------------

st_folium(
    m,
    use_container_width=True,
    height=700
)

# -----------------------------------
# Final Recommendation
# -----------------------------------

st.subheader("Final Recommendation")

st.write("""
Spatial accessibility analysis identified one strongly feasible
new healthcare facility location capable of improving accessibility
coverage within an underserved healthcare corridor while avoiding
redundant overlap with existing hospital service areas.
""")

# -----------------------------------
# Before vs After Impact
# -----------------------------------

st.subheader("Before vs After Accessibility Impact")

st.markdown("""
### Key Accessibility Findings

#### Before Intervention
- The identified underserved corridor experienced a nearest-hospital accessibility gap of approximately **3259.52 meters**.
- Existing healthcare coverage in this region was comparatively weaker than surrounding urban areas.
- Residents within this corridor were required to travel longer distances to reach nearby hospitals.

#### Proposed Intervention
- A new healthcare facility was proposed at:
  - **Longitude:** 80.20319
  - **Latitude:** 13.11804
- The proposed facility directly targets the identified accessibility gap region.

#### Expected Accessibility Improvement
- Introduction of the proposed facility is expected to substantially reduce local travel burden.
- The intervention improves healthcare accessibility coverage within the underserved corridor.
- Spatial overlap with existing hospitals remains minimal, improving overall network efficiency.

#### Budget and Optimization Decision
- Although the analysis allowed up to three new facilities, only one location demonstrated strong spatial feasibility and meaningful accessibility improvement.
- Additional candidate locations either overlapped existing healthcare coverage or fell within infeasible coastal regions.
- Therefore, the analysis recommended stopping after one facility due to diminishing marginal accessibility returns.
""")
