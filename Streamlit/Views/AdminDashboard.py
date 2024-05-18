import streamlit as st
import random
import pandas as pd
import streamlit as st

# Set the page layout to wide
st.set_page_config(layout="wide")

# Generate 30 different numbers from 0 to 40 for each row
working_days = [random.sample(range(41), 30) for _ in range(3)]

df = pd.DataFrame(
    {
        "name": ["Dr Ahmed", "Dr Karim", "Dr Yasser"],
        "working_days": working_days
    }
)

def app():
    st.title('Admin DashBoard')
    
    st.dataframe(
        df,
        column_config={
            "name": "Doctors",
            "working_days": st.column_config.LineChartColumn(
                "Working Days", y_min=0, y_max=40
            ),
        },
        hide_index=True,
        width=1200  # Adjust the width as needed
    )
