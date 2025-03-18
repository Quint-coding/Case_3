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
    "html": "<b>Busyness:</b> {busyness}",
    "style": {"backgroundColor": "steelblue", "color": "white"},
}

ViewState = pdk.ViewState(
            latitude=51.50853,
            longitude=-0.12574,
            zoom=11,
            pitch=50,
        )

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=ViewState,
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=df,
                get_position="[Longitude, Latitude]",
                radius=200,
                elevation_scale=50,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                auto_highlight=True,
            ),
        ],
    )
)

