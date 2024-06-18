import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import random
from datetime import datetime, timedelta
import plotly.express as px

# Generate 30 different numbers from 0 to 40 for each row
working_days = [random.sample(range(41), 30) for _ in range(3)]
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(30)]

# Create DataFrame with dates
dfdoc = pd.DataFrame({
    "name": ["Dr Ahmed", "Dr Karim", "Dr Yasser"],
    "Filled_Risk_Prediction_Per_Day": working_days
})

# Convert to long format for Altair
df_long = dfdoc.explode("Filled_Risk_Prediction_Per_Day")
df_long['date'] = dates * 3  # Repeat the dates for each doctor
df_long.reset_index(drop=True, inplace=True)

# Calculate average filled risk prediction per day for each doctor
dfdoc['Average_Filled_Risk_Prediction_Per_Day'] = dfdoc['Filled_Risk_Prediction_Per_Day'].apply(lambda x: round(np.mean(x)))

# Sample data for doctors' appointments spanning multiple days
appointment_data = {
    'Patient': ['Patient A', 'Patient B', 'Patient C', 'Patient D', 'Patient E', 'Patient F'],
    'Start': ['2024-05-01', '2024-05-02', '2024-05-04', '2024-05-06', '2024-05-10', '2024-05-13'],
    'End': ['2024-05-08', '2024-05-09', '2024-05-11', '2024-05-13', '2024-05-17', '2024-05-20'],
}

# Create a DataFrame for appointments
df_appointments = pd.DataFrame(appointment_data)
df_appointments['Start'] = pd.to_datetime(df_appointments['Start'])
df_appointments['End'] = pd.to_datetime(df_appointments['End'])

# Define color palette
awamacolor = ["#c8387d", "#ec6989", "#169DA6", "#b4f8ed"]

def app():
    # Choose the doctor to display risk prediction data for
    doctor_name = 'Dr Ahmed'
    
    # Create a Gantt chart for the selected doctor's appointments
    fig = px.timeline(
        df_appointments, 
        x_start='Start', 
        x_end='End', 
        y='Patient', 
        title="Doctor's Appointments",
        color_discrete_sequence=awamacolor
    )
    fig.update_yaxes(categoryorder='total ascending')
    fig.update_layout(xaxis_title='Date', yaxis_title='Patient')

    # Display the Gantt chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("    " )
    st.subheader("    " )
    
    # Display Performance Ratings
    col12, col21, col333 = st.columns([2, 4, 2])
    with col21:
        st.subheader("Filled Risk Prediction Per Day by Physician")

        # Filter data for the selected doctor
        df_doctor = df_long[df_long['name'] == doctor_name]

        # Create and display Altair chart
        brush = alt.selection_interval(encodings=['x'])
        
        base = alt.Chart(df_doctor).mark_area(color=awamacolor[0]).encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('Filled_Risk_Prediction_Per_Day:Q', title='Filled Risk Prediction'),
            color=alt.Color('name:N', scale=alt.Scale(range=awamacolor))
        ).properties(
            width=600,
            height=200
        )
        
        upper = base.encode(
            alt.X('date:T').scale(domain=brush)
        )
        
        lower = base.properties(
            height=60
        ).add_params(brush)
        
        st.altair_chart(upper & lower)
