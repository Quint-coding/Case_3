import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Set page config for better layout
st.set_page_config(page_title="Fietsdrukte Dashboard", page_icon="🚲", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Center the title */
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #ddd;
            margin-bottom: 30px;
        }

        /* Background styling */
        .main {
            background: linear-gradient(to right, #20283E, #1E3A5F);
            padding: 50px;
            border-radius: 15px;
        }

        /* Center image */
        .center {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }

        /* Button Styling */
        .stButton>button {
            width: 50%;
            display: block;
            margin: auto;
            background-color: #FF4B4B;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #CC3A3A;
        }
    </style>
""", unsafe_allow_html=True)

# Main container with styling
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # Title
    st.markdown('<div class="title">🚲 Fietsdrukte Dashboard</div>', unsafe_allow_html=True)
    
    # Subtitle
    st.markdown('<div class="subtitle">Interactieve visualisaties van fietsdrukte bij stations.</div>', unsafe_allow_html=True)

    # Optional image (replace with your own)
    st.markdown('<div class="center"><img src="https://source.unsplash.com/1600x500/?bicycle,city" width="80%"></div>', unsafe_allow_html=True)

    # Navigation button
    if st.button("Ga naar Visualisaties 🚀"):
        st.switch_page("app.py")  # Update this with the correct file name

    st.markdown('</div>', unsafe_allow_html=True)

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

