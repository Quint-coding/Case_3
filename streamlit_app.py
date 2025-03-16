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


st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=df,
                get_position="[Longitude, Latitude]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position="[Longitude, Latitude]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)