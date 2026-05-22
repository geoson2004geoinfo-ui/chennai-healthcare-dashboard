
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Healthcare Accessibility Dashboard",
    layout="wide"
)

st.title("Healthcare Accessibility Analysis - Chennai")

st.markdown(
'''
This dashboard presents:
- Existing hospital locations
- Underserved healthcare regions
- Proposed new healthcare facility
- Accessibility improvement analysis
'''
)

# Create Folium map
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
        popup='Proposed New Facility',
        icon=folium.Icon(color='green')
    ).add_to(m)

folium.LayerControl().add_to(m)

# Display map
st_folium(m, width=1200, height=700)

# Final recommendation
st.subheader("Final Recommendation")

st.write(
'''
Spatial analysis identified one strongly feasible new healthcare facility location
that significantly improves accessibility within an underserved corridor while
avoiding redundant overlap with existing hospital coverage.
'''
)
