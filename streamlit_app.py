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

df = pd.read_csv('dataset_aangepast.csv')

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

zone_colors = {
    '1': [255, 0, 0],  # Red
    '2': [0, 255, 0],  # Green
    '3': [0, 0, 255]   # Blue
}

st.markdown("""
    <style>
        div[data-baseweb="select"] > div {
            background-color: #333 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

df['Start date'] = pd.to_datetime(df['Start date'])


# Dropdown to select zone
selected_zone = st.selectbox("Select Zone", ['All'] + sorted(df['Zone'].unique()))

# Dropdown to select date
unique_dates = list(map(str, df['Start date'].dt.date.unique()))
selected_date = st.selectbox("Select Date", ['All'] + sorted(unique_dates))

# Filter data based on selections
filtered_data = df.copy()
if selected_zone != 'All':
    filtered_data = filtered_data[filtered_data['Zone'] == selected_zone]
if selected_date != 'All':
    filtered_data = filtered_data[filtered_data['Start date'].dt.date.astype(str) == selected_date]

# Compute traveler count display
displayed_traveler_count = filtered_data['traveler_count'].mean() if selected_date == 'All' else filtered_data['traveler_count'].sum()
st.write(f"Traveler Count: {displayed_traveler_count:.2f}")

# Ensure filtered data contains valid color mapping
filtered_data['color'] = filtered_data['Zone'].map(zone_colors).apply(lambda x: x if isinstance(x, list) else [255, 255, 255])


ViewState = pdk.ViewState(
            latitude=51.50853,
            longitude=-0.12574,
            zoom=11,
            pitch=50,
        )


layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_data,
    pickable=True,
    # opacity=0.8,
    # stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=15,
    get_position="[Longitude, Latitude]",
    get_radius="traveler_count",
    get_color='color',
)

r = pdk.Deck(layers=[layer], 
             initial_view_state=ViewState, 
             tooltip={"text": "Station: {Station}\nBusyness: {traveler_count}"})
st.pydeck_chart(r)