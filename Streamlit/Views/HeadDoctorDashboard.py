import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

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

# Define color palette
awamacolor = ["#c8387d", "#ec6989", "#169DA6", "#b4f8ed"]

def app():
    st.write('Head Doctor Dashboard')
    # Display total physicians, data analysts, and website users
    total_doctors = len(dfdoc)

    left_column, middle_column, right_column = st.columns(3)
   
    with middle_column:
        st.subheader(":male-doctor: Total Physicians:")
        st.subheader(f"{total_doctors}")
    

    st.markdown("""---""")
    col12, col521, col333 = st.columns([1,3, 1])
    with col521:
    # Display working days of doctors
        st.subheader("Filled Risk Prediction Per Day by Physicians")
        st.dataframe(
            dfdoc,
            column_config={
                "name": "Physicians",
                "Filled_Risk_Prediction_Per_Day": st.column_config.LineChartColumn(
                    "Filled Risk Prediction Per Day", y_min=0, y_max=40
                ),
                "Average_Filled_Risk_Prediction_Per_Day": "Average Filled Risk Prediction Per Day"
            },
            hide_index=True,
            width=900
        )
        
    st.subheader("    " )
    st.subheader("    " )
    
    # Display Performance Ratings
    col12, col21, col333 = st.columns([0.7,3, 1])
    with col21:
        
        # Create and display Altair chart
        brush = alt.selection_interval(encodings=['x'])
        
        base = alt.Chart(df_long).mark_area().encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('Filled_Risk_Prediction_Per_Day:Q', title='Filled Risk Prediction'),
            color=alt.Color('name:N', scale=alt.Scale(range=awamacolor))
        ).properties(
            width=800,
            height=200
        )
        
        upper = base.encode(
            alt.X('date:T').scale(domain=brush)
        )
        
        lower = base.properties(
            height=60
        ).add_params(brush)
        
        st.altair_chart(upper & lower)

# Run the app
