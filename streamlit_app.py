import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt


# Set page configuration
st.set_page_config(page_title="Fietsdrukte Dashboard", page_icon="🚲", layout="wide")

# Custom CSS to style the sidebar (dark theme)
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #1E1E1E !important;  /* Dark sidebar */
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] h4, 
        [data-testid="stSidebar"] h5, 
        [data-testid="stSidebar"] h6, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] p {
            color: white !important;  /* White text */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title("📍 Navigatie")
page = st.sidebar.radio("Ga naar", ["🏠 Home", 
                                    "🚲 Drukte Geo - Visualisatie", 
                                    "🚲 Drukte over de dag", 
                                    "🚲 Drukte Voorspellen"])

# Home Page
if page == "🏠 Home":
    st.title("🚲 Fietsdrukte Dashboard")
    st.subheader("Welkom bij het interactieve vervoerdrukte dashboard!")

    st.write("""
    Dit dashboard geeft inzicht in de drukte bij stations.
    Gebruik de navigatie aan de linkerzijde om naar de visualisaties te gaan.
             
    Team 8:
    Tammo van Leeuwen, Jorik Stavenuiter, Burhan Canbaz, Quint Klaassen
    """)

# Visualization Page
elif page == "🚲 Drukte Geo - Visualisatie":
    st.title("🚲 Drukte Geo - Visualisatie")
    st.write("Interactieve weergave van fietsdrukte bij stations.")


    ## start code voor kaart
    df = pd.read_csv("/Users/Quint/Desktop/Data science/Case 3/geo_drukte_df.csv")

    zone_colors = {
        '1': [255, 0, 0],  # Red
        '1,2' : [130, 200, 0],
        '2': [0, 255, 0],  # Green
        '2,3': [0, 130, 200],
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
        selected_row = selected_rows[['Start Date', 'tavg', 'wspd', 'wdir', 'prcp']].head(1).copy()
        
        # Convert wind direction to compass points
        selected_row['wdir'] = selected_row['wdir'].apply(wind_direction)
        
        # Rename columns for better display
        selected_row.rename(columns={
            'Start Date': 'Date',
            'tavg': 'Temperature (°C)',
            'wspd': 'Wind Speed (km/h)',
            'wdir': 'Wind Direction',
            'prcp' : 'Rain (mL)'
        }, inplace=True)

        selected_row['Date'] = pd.to_datetime(selected_row['Date']).dt.date

        # Display the weather data as a table
        st.write("### Weather Data")
        st.dataframe(selected_row.style.format({'Temperature (°C)': '{:.1f}', 'Wind Speed (km/h)': '{:.1f}', 'Rain (mL)': '{:.1f}'}))

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

elif page == "🚲 Drukte over de dag":
    st.title("🚲 Drukte over de dag")
    st.write("Interactieve weergave van fietsdrukte bij stations.")

        ## start code voor kaart
    df_rent = pd.read_csv('finaal_df.csv')

    tijdseenheid = st.selectbox('Selecteer tijdseenheid', ['Uur', 'Minuut'])
 
    fig, ax = plt.subplots(figsize=(8, 6))  # Maak een lege figuur
 
    # Maak de plot op basis van de geselecteerde tijdseenheid
    if tijdseenheid == 'Uur':
        tijd_counts = df_rent['uur'].value_counts().sort_index()
        tijd_counts = tijd_counts.reindex(range(24), fill_value=0)
        ax.plot(tijd_counts.index, tijd_counts.values, marker='o', linestyle='-', color='dodgerblue', label="Per uur")
        ax.set_xticks(range(24))  # Tick per uur
 
    # Verwerking per minuut
    if tijdseenheid == 'Minuut':
        geselecteerd_uur = st.slider("Selecteer een uur", min_value=0, max_value=23, value=12)
        df_filtered = df_rent[df_rent['uur'] == geselecteerd_uur]  # Filter op geselecteerd uur
        tijd_counts = df_filtered['minuut'].value_counts().sort_index()
        tijd_counts = tijd_counts.reindex(range(60), fill_value=0)
        ax.plot(tijd_counts.index, tijd_counts.values, marker='o', linestyle='-', color='green', label=f"Minuten binnen {geselecteerd_uur}:00")
 
    # Labels en titels
    ax.set_title('Verdeling van waarnemingen')
    ax.set_xlabel('Tijd')
    ax.set_ylabel('Aantal waarnemingen')
    ax.legend()
 
    plt.tight_layout()
 
    # Weergave in Streamlit
    st.pyplot(fig)

elif page == "🚲 Drukte Voorspellen":
    st.title("🚲 Drukte Voorspellen")
    st.write("Interactieve weergave van fietsdrukte bij stations.")
