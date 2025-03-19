import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("3D kaart van de fiets drukte op stations")

df = pd.read_csv('dataset_aangepast.csv')
weather_df = pd.read_csv('weather_london.csv')

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


st.markdown("""
    <style>
        div[data-baseweb="select"] > div {
            background-color: #333 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

zone_colors = {
    '1': [255, 0, 0],  # Red
    '1,2' : [130, 130, 0],
    '2': [0, 255, 0],  # Green
    '2,3': [0, 130, 130],
    '3': [0, 0, 255]   # Blue
}

df['Start Date'] = pd.to_datetime(df['Start Date'])
weather_df['Date'] = pd.to_datetime(weather_df['Date'])

# Dropdown to select zone
selected_zone = st.selectbox("Select Zone", ['All'] + sorted(df['Zone'].astype(str).unique()))

# Slider to select date range
min_date = df['Start Date'].min().date()
max_date = df['Start Date'].max().date()
selected_date = st.slider("Select Date", min_value=min_date, max_value=max_date, value=min_date)

# Filter data based on selections
filtered_data = df.copy()
if selected_zone != 'All':
    filtered_data = filtered_data[filtered_data['Zone'] == selected_zone]
filtered_data = filtered_data[filtered_data['Start Date'].dt.date == selected_date]


## Weer data weergeven o.b.v geselcteerde datum
selected_weather = weather_df[weather_df['Date'].dt.date == selected_date]

if not selected_weather.empty:
    temperature = selected_weather['tavg'].values[0]
    wind_richting = selected_weather['wdir'].values[0]
    precipitation = selected_weather['prcp'].values[0]
    st.write(f"🌡️ Average temperature: {temperature}°C | ☁️ Wind direction: {wind_richting} | Precipitation {precipitation}")
else:
    st.write("⚠️ No weather data available for this date.")

# Compute traveler count display
displayed_traveler_count = filtered_data['traveler_count'].mean() if selected_date == 'All' else filtered_data['traveler_count'].sum()
st.write(f"Total raveler Count: {displayed_traveler_count:.0f}")

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

