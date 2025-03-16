import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 50)
y = np.sin(x)  # Example: Sine wave data

# Streamlit app title
st.title("Line Graph Example in Streamlit")

# Create a Matplotlib figure
fig, ax = plt.subplots()
ax.plot(x, y, marker='o', linestyle='-', color='b', label='Sine Wave')
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_title("Sample Line Graph")
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)
