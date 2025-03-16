import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit app title
st.title("Geographical Busyness of London Stations")

# Sample data: Replace with real station coordinates and busyness levels
data = {
    "Station": ["Waterloo", "Victoria", "Liverpool Street", "Euston", "Paddington"],
    "Latitude": [51.5033, 51.4964, 51.5175, 51.5281, 51.5154],
    "Longitude": [-0.113, -0.144, -0.082, -0.133, -0.175],
    "Busyness": [100, 80, 90, 70, 85]  # Example busyness levels
}

# Convert data to GeoDataFrame
df = pd.DataFrame(data)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# Load a basemap of London (or any shapefile of interest)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create plot
fig, ax = plt.subplots(figsize=(8, 6))
world[world.name == "United Kingdom"].plot(ax=ax, color='lightgrey')
gdf.plot(ax=ax, column="Busyness", cmap="coolwarm", markersize=gdf["Busyness"] * 2, legend=True, edgecolor='black')

# Annotate stations
for idx, row in gdf.iterrows():
    ax.text(row.Longitude, row.Latitude, row.Station, fontsize=9, ha='right')

ax.set_title("London Stations Busyness")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Display the plot in Streamlit
st.pyplot(fig)
