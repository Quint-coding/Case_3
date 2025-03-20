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
    - Tammo van Leeuwen, 
    - Jorik Stavenuiter, 
    - Burhan Canbaz, 
    - Quint Klaassen
    """)

# Visualization Page
elif page == "🚲 Drukte Geo - Visualisatie":
    st.title("🚲 Drukte Geo - Visualisatie")
    st.write("Interactieve weergave van fietsdrukte bij stations.")


    ## start code voor kaart
    df = pd.read_csv("geo_drukte.csv")

    zone_colors = {
        '1': [255, 0, 0],  # Red
        '1,2' : [130, 200, 0],
        '2': [0, 255, 0],  # Green
        '2,3': [0, 130, 200],
        '3': [0, 0, 255]   # Blue
    }

    df['Start Date'] = pd.to_datetime(df['Start Date'], format='ISO8601')
    df.dropna(subset=['Zone'])

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
 
    # Laad dataset
    df_rent = pd.read_csv('finaal_df.csv')
 
    # Engelse dagen omzetten naar Nederlands
    dagen_mapping = {
        "Monday": "Maandag",
        "Tuesday": "Dinsdag",
        "Wednesday": "Woensdag",
        "Thursday": "Donderdag",
        "Friday": "Vrijdag",
        "Saturday": "Zaterdag",
        "Sunday": "Zondag"
    }
    df_rent['dag_van_de_week_start'] = df_rent['dag_van_de_week_start'].map(dagen_mapping)
 
    tijdseenheid = st.selectbox('Selecteer tijdseenheid', ['Uur', 'Minuut'])
    dag_opties = ['Alles', 'Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag']
    geselecteerde_dag = st.selectbox('Selecteer dag', dag_opties)
 
    # Filter dataset op geselecteerde dag (behalve als "Alles" is gekozen)
    if geselecteerde_dag != "Alles":
        df_rent = df_rent[df_rent['dag_van_de_week_start'] == geselecteerde_dag]
 
    st.write(f"Aantal rijen na filtering: {len(df_rent)}")  # Debugging: laat aantal overgebleven rijen zien
 
    fig, ax = plt.subplots(figsize=(8, 6))
 
    if tijdseenheid == 'Uur':
        tijd_counts = df_rent['uur'].value_counts().sort_index()
        tijd_counts = tijd_counts.reindex(range(24), fill_value=0)
        ax.plot(tijd_counts.index, tijd_counts.values, marker='o', linestyle='-', color='dodgerblue', label="Per uur")
        ax.set_xticks(range(24))
 
    if tijdseenheid == 'Minuut':
        geselecteerd_uur = st.slider("Selecteer een uur", min_value=0, max_value=23, value=12)
        df_filtered = df_rent[df_rent['uur'] == geselecteerd_uur]
        tijd_counts = df_filtered['minuut'].value_counts().sort_index()
        tijd_counts = tijd_counts.reindex(range(60), fill_value=0)
        ax.plot(tijd_counts.index, tijd_counts.values, marker='o', linestyle='-', color='green', label=f"Minuten binnen {geselecteerd_uur}:00")
 
    ax.set_title('Verdeling van waarnemingen')
    ax.set_xlabel('Tijd')
    ax.set_ylabel('Aantal waarnemingen')
    ax.legend()
 
    plt.tight_layout()
    st.pyplot(fig)
 
elif page == "🚲 Drukte Voorspellen":
    st.title("🚲 Drukte Voorspellen")
    st.write("Interactieve weergave van fietsdrukte bij stations.")

    # Data inladen
    df = pd.read_csv('finaal_df.csv')
    
    # Data opschonen
    df['dag_van_de_week_start'] = df['dag_van_de_week_start'].str.strip()
    
    # Aantal rentals per dag + uur tellen
    df_grouped = df.groupby(['dag_van_de_week_start', 'uur']).agg({
        'Duration': 'count',  # Aantal rentals
        'tavg': 'mean', 'prcp': 'mean', 'wspd': 'mean'  # Gemiddelde weergegevens
    }).reset_index()
    
    # Hernoemen
    df_grouped.rename(columns={'Duration': 'rentals'}, inplace=True)
    
    # Gemiddeld aantal rentals per uur over ALLE dagen
    df_avg_per_uur = df_grouped.groupby('uur')['rentals'].mean().reset_index()
    df_avg_per_uur.rename(columns={'rentals': 'gem_rentals'}, inplace=True)
    
    # Data opslaan
    df_grouped = df_grouped.merge(df_avg_per_uur, on="uur")
    df_grouped['weercorrectie'] = (df_grouped['tavg'] / df_grouped['tavg'].mean()) * (1 - df_grouped['prcp'] / 10)
    
    # Finale voorspelling zonder ML (simpele schatting)
    df_grouped['voorspelling'] = df_grouped['gem_rentals'] * df_grouped['weercorrectie']
    
    # Selecteer een dag
    dagen = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dag = st.selectbox("Selecteer een dag:", dagen)
    
    # Selecteer een uur
    uur = st.slider("Selecteer een uur:", min_value=0, max_value=23, value=12)
    
    # Weer aanpassen
    tavg = st.number_input("Gemiddelde temperatuur (°C)", min_value=-10.0, max_value=40.0, value=15.0)
    prcp = st.number_input("Neerslag (mm)", min_value=0.0, max_value=50.0, value=0.0)
    
    # Zoek de basisvoorspelling op
    basis_rental = df_grouped[(df_grouped["dag_van_de_week_start"] == dag) & (df_grouped["uur"] == uur)]
    
    if basis_rental.empty:
        st.warning("Geen data beschikbaar voor deze selectie.")
    else:
        gem_rentals = basis_rental["gem_rentals"].values[0]
        tavg_mean = df_grouped["tavg"].mean()
    
        # Kwadratische correctie toepassen
        weercorrectie = (tavg / tavg_mean) ** 2 * (1 - (prcp / 10) ** 2)
    
        # Voorspelling berekenen en nooit onder 0 laten komen
        voorspelling = max(0, gem_rentals * weercorrectie)
    
        st.subheader(f"📊 Geschat aantal verhuurde fietsen: {int(voorspelling)}")
    
    # Filter de data: Alleen Duration < 30.000
    df_filtered = df[df['Duration'] < 3600]/3600
    
    # Definieer onafhankelijke en afhankelijke variabele
    X = df_filtered[['uur']]
    y = df_filtered['Duration']
    
    # Voeg een constante toe voor de OLS-regressie
    X = sm.add_constant(X)
    
    # Voer de OLS-regressie uit
    model = sm.OLS(y, X).fit()
    
    # Maak de voorspellingen
    df_filtered['Predicted_Duration'] = model.predict(X)
    
    # Plot de resultaten
    plt.figure(figsize=(10, 6))
    plt.scatter(df_filtered['uur'], df_filtered['Duration'], color='blue', alpha=0.5, label='Data')
    plt.plot(df_filtered['uur'], df_filtered['Predicted_Duration'], color='red', label='OLS Regressielijn')
    
    # Labels en titel
    plt.xlabel('Uur van de dag')
    plt.ylabel('Duur van de rit (seconden)')
    plt.title('OLS Regressie: Uur vs Duur van de Rit')
    plt.legend()
    plt.show()
    
    # Print de regressie samenvatting
    model.summary()