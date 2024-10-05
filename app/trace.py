import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

# Fetching data from the API
r = requests.get('https://htv-project.onrender.com/api/getrecords').json()

# Preparing map data with connections between points
map_data = [{"lon": float(r[i]["locationy"]), "lat": float(r[i]["locationx"]),
             "lon2": float(r[i + 1]["locationy"]), "lat2": float(r[i + 1]["locationx"]),
             "outbound": 1} for i in range(len(r) - 1)]

location_data = pd.DataFrame(map_data)

# Streamlit UI
st.subheader("Today's GPS Trace")

# Define the ArcLayer for connections between points
arc_layer = pdk.Layer(
    "ArcLayer",
    data=location_data,
    get_source_position=["lon", "lat"],
    get_target_position=["lon2", "lat2"],
    get_source_color=[200, 30, 0, 160],
    get_target_color=[0, 200, 0, 160],
    auto_highlight=True,
    width_scale=0.0001,
    get_width="outbound",
    width_min_pixels=3,
    width_max_pixels=30,
)

# Set the initial view of the map
view_state = pdk.ViewState(
    latitude=location_data["lat"].mean(),
    longitude=location_data["lon"].mean(),
    zoom=11,
    pitch=50,
)

# Render the deck.gl map in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[arc_layer],
    initial_view_state=view_state,
    tooltip={"text": "GPS Trace"},
))
