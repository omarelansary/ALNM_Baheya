import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data for doctors' appointments spanning multiple days
data = {
    'Patient': ['Patient A', 'Patient B', 'Patient C', 'Patient D', 'Patient E', 'Patient F'],
    'Start': ['2024-05-01', '2024-05-02', '2024-05-04', '2024-05-06', '2024-05-10', '2024-05-13'],
    'End': ['2024-05-8', '2024-05-9', '2024-05-11', '2024-05-13', '2024-05-17', '2024-05-20'],
}

# Create a DataFrame
df = pd.DataFrame(data)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

def app():
    # Choose the doctor to display appointments for
    doctor_name = 'Dr Ahmed'

    # Create a Gantt chart for the selected doctor's appointments
    fig = px.timeline(data, x_start='Start', x_end='End', y='Patient', title=f"{doctor_name}'s Appointments")
    fig.update_yaxes(categoryorder='total ascending')
    fig.update_layout(xaxis_title='Date', yaxis_title='Patient')

    # Configure layout to be wider

    # Display the Gantt chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    