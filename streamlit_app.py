import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(page_title="Fietsdrukte Dashboard", page_icon="🚲", layout="wide")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default to home page

# Function to switch pages
def switch_page(page_name):
    st.session_state.page = page_name

# Home Page Content
if st.session_state.page == "home":
    st.title("🚲 Fietsdrukte Dashboard")
    st.subheader("Welkom bij het interactieve fietsdrukte dashboard!")

    st.write("""
    Dit dashboard geeft inzicht in de drukte van fietsenstallingen op stations.
    Klik op de knop hieronder om de visualisaties te bekijken.
    """)

    # Navigation Button
    if st.button("Ga naar Visualisaties 🚀"):
        switch_page("visualisatie")

    # Display an image (optional)
    st.image("https://source.unsplash.com/1600x500/?bicycle,city", use_column_width=True)

# Visualization Page Content
elif st.session_state.page == "visualisatie":
    st.title("📊 Fietsdrukte Visualisaties")
    st.write("Hier kun je de interactieve visualisaties bekijken van de fietsdrukte bij stations.")

    # Back Button to go to Home Page
    if st.button("🔙 Terug naar Home"):
        switch_page("home")

## start code voor kaart
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

# Dropdown to select zone
selected_zone = st.selectbox("Select Zone", ['All'] + sorted(df['Zone'].astype(str).unique()))

# Slider to select date range
min_date = df['Start Date'].min().date()
max_date = df['Start Date'].max().date()
selected_date = st.slider("Select Date", min_value=min_date, max_value=max_date, value=min_date)

## Wheather info
def wind_direction(degrees):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    index = round(degrees / 45) % 8
    return directions[index]

selected_rows = df[df['Start Date'].dt.date == selected_date]

# Ensure filtered data is not empty
if not selected_rows.empty:
    # Select relevant weather columns (adjust column names if needed)
    selected_row = selected_rows[['Start Date', 'tavg', 'wspd', 'wdir']].head(1).copy()
    
    # Convert wind direction to compass points
    selected_row['wdir'] = selected_row['wdir'].apply(wind_direction)
    
    # Rename columns for better display
    selected_row.rename(columns={
        'Start Date': 'Date',
        'tavg': 'Temperature (°C)',
        'wspd': 'Wind Speed (km/h)',
        'wdir': 'Wind Direction'
    }, inplace=True)

    # Display the weather data as a table
    st.write("### Weather Data")
    st.dataframe(selected_row.style.format({'Temperature (°C)': '{:.1f}', 'Wind Speed (km/h)': '{:.1f}'}))

else:
    st.write("No weather data available for the selected date.")


# Filter data based on selections
filtered_data = df.copy()
if selected_zone != 'All':
    filtered_data = filtered_data[filtered_data['Zone'] == selected_zone]
filtered_data = filtered_data[filtered_data['Start Date'].dt.date == selected_date]

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
    radius_scale=5,
    radius_min_pixels=1,
    radius_max_pixels=10,
    get_position="[Longitude, Latitude]",
    get_radius="traveler_count",
    get_color='color',
)

r = pdk.Deck(layers=[layer], 
             initial_view_state=ViewState, 
             tooltip={"text": "Station: {Station}\nBusyness: {traveler_count}"})
st.pydeck_chart(r)

