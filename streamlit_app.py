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

tooltip = {
    "html": "<b>Station:</b> {Station}<br><b>Busyness:</b> {traveler_count}",
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# ViewState = pdk.ViewState(
#             latitude=51.50853,
#             longitude=-0.12574,
#             zoom=11,
#             pitch=50,
#         )

# st.pydeck_chart(
#     pdk.Deck(
#         map_style=None,
#         initial_view_state=ViewState,
#         layers=[
#             pdk.Layer(
#                 "HexagonLayer",
#                 data=df,
#                 get_position="[Longitude, Latitude]",
#                 get_elevation="traveler_count",
#                 get_fill_color="[255, traveler_count, 100]",
#                 radius=300,
#                 elevation_scale=5,
#                 elevation_range=[0, 100],
#                 pickable=True,
#                 extruded=True,
#                 auto_highlight=True,
#             ),
#         ],
#         tooltip = tooltip
#     )
# )

# layer = pdk.Layer(
#     "ScatterplotLayer",
#     data = df,
#     get_position=["Longitude", "Latitude"],
#     auto_highlight=True,
#     elevation_scale=50,
#     pickable=True,
#     tooltip=True,
#     elevation_range=[0, 3000],
#     extruded=True,
#     coverage=1,
# )

layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position="coordinates",
    get_radius="exits_radius",
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36,
)

# Render
pdk_map = pdk.Deck(layers=[layer], initial_view_state=view_state)

st.pydeck_chart(pdk_map)