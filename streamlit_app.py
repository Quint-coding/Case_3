import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Sample Data (Replace with actual CSV file or database)
data = {
    "Station": ["A", "B", "C", "D", "E"],
    "Latitude": [40.7128, 40.7138, 40.7148, 40.7158, 40.7168],
    "Longitude": [-74.0060, -74.0070, -74.0080, -74.0090, -74.0100],
    "Passenger_Count": [1000, 2500, 1800, 3000, 2200]
}
df = pd.DataFrame(data)

# Streamlit UI
st.title("3D Metro Station Visualization")
st.write("### Hover over points to see details")

# Create a 3D Scatter Plot
fig = go.Figure()
fig.add_trace(go.Scatter3d(
    x=df["Longitude"],
    y=df["Latitude"],
    z=df["Passenger_Count"],
    mode='markers',
    marker=dict(
        size=10,
        color=df["Passenger_Count"],
        colorscale='Viridis',
        opacity=0.8
    ),
    text=df["Station"],
    hoverinfo='text+x+y+z'
))

# Labels
fig.update_layout(
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Passenger Count'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Show Plot
st.plotly_chart(fig)
