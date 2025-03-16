import streamlit as st
import pandas as pd
import pydeck as pdk

# Streamlit app title
st.title("Geographical Busyness of London Stations")

# Sample data: Replace with real station coordinates and busyness levels
data = {
    "Station": ["Waterloo", "Victoria", "Liverpool Street", "Euston", "Paddington"],
    "Latitude": [51.5033, 51.4964, 51.5175, 51.5281, 51.5154],
    "Longitude": [-0.113, -0.144, -0.082, -0.133, -0.175],
    "Busyness": [100, 80, 90, 70, 85]  # Example busyness levels
}

df = pd.DataFrame(data)

# Define Pydeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["Longitude", "Latitude"],
    get_radius="Busyness",
    get_color=[255, 0, 0, 160],
    pickable=True,
    opacity=0.6,
)

# Define Pydeck view
view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=12,
    pitch=40,
)

# Create Pydeck map
map = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Station}: {Busyness} people"},
)

# Display the map in Streamlit
st.pydeck_chart(map)
