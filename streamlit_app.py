import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# np.random.seed(20)

# chart_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=["lat", "lon"],
# )

st.title("3D kaart van de fiets drukte op stations")

df = pd.read_csv('bestedatasetopoitbombaclat2.csv')

st.sidebar.title('Navigatie')

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #20283E; /* Change this to your desired color */
        }
    </style>
    """,
    unsafe_allow_html=True
)

options = st.sidebar.radio('Visualisaties',
                           options =['Fietsdrukte kaart'])

# tooltip = {
#     "html": "<b>Station:</b> {Station}<br><b>Busyness:</b> {traveler_count}",
#     "style": {"backgroundColor": "steelblue", "color": "white"}
# }

ViewState = pdk.ViewState(
            latitude=51.50853,
            longitude=-0.12574,
            zoom=11,
            pitch=50,
        )


layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=10,
    line_width_min_pixels=1,
    get_position=["Longitude", "Latitude"],
    get_radius="traveler_count",
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
)

r = pdk.Deck(layers=[layer], 
             initial_view_state=ViewState, 
             tooltip={"text": "Station: {Station}\nBusyness: {traveler_count}"})
st.pydeck_chart(r)