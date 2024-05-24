import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import random
import subprocess
import re
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

# Function to check service status
def check_service_status(service_name):
    details = {}
    try:
        result = subprocess.run(['systemctl', 'status', service_name], text=True, capture_output=True)
        status_output = result.stdout
        enabled_search = re.search(r'enabled;', status_output)
        details['Enabled'] = "Yes" if enabled_search else "No"
        active_since_search = re.search(r'Active:\s(\d+);', status_output)
        details['Active'] = active_since_search.group(1) if active_since_search else "Not available"
        tasks_search = re.search(r'Tasks:\s(\d+)', status_output)
        details['Tasks'] = tasks_search.group(1) if tasks_search else "Not available"
        memory_search = re.search(r'Memory:\s([\w\d.]+)', status_output)
        details['Memory'] = memory_search.group(1) if memory_search else "Not available"
        return details
    except Exception as e:
        return {"error": str(e)}

def app():
    st.title(':bookmark_tabs: Admin Dashboard')

    st.write(check_service_status('postgresql'))

    # Display total physicians, data analysts, and website users
    total_doctors = len(dfdoc)
    total_analysts = total_doctors  # Assuming same number of analysts as doctors for demonstration
    total_users = total_doctors + total_analysts + 1

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader(":male-doctor: Total Physicians:")
        st.subheader(f"{total_doctors}")
    with middle_column:
        st.subheader(":male-technologist: Total Data Analysts:")
        st.subheader(f"{total_analysts}")
    with right_column:
        st.subheader(":male-office-worker: Total Website Users:")
        st.subheader(f"{total_users}")

    st.markdown("""---""")

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
        width=1200
    )
    st.subheader("    " )
    st.subheader("    " )
    # Display Performance Ratings
    col12,col21,col333=st.columns([2,4,2])
    with col21:
        
        # Create and display Altair chart
        brush = alt.selection_interval(encodings=['x'])
        
        base = alt.Chart(df_long).mark_area().encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('Filled_Risk_Prediction_Per_Day:Q', title='Filled Risk Prediction'),
            color='name:N'
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
    st.markdown("""---""")
    st.subheader("Evaluation esults")

    # Function to generate random ratings for each performance category
    def generate_random_ratings(num_categories):
        return [random.randint(2, 5) for _ in range(num_categories)]

    # Create the performance rating DataFrame
    performance_categories = ["Performance Rating", "Usability Rating", "Learnability Rating"]
    num_ratings = [random.randint(10, 50) for _ in range(len(performance_categories))]
    dfperformance = pd.DataFrame({
        "name": performance_categories,
        "stars": generate_random_ratings(len(performance_categories)),
        "num_ratings": num_ratings
    })

    # Convert the data to long format suitable for Altair
    values = pd.DataFrame(
        [
            {"value": row['stars'], "name": row['name'], "id": f"P{i+1}", "num_ratings": row['num_ratings']}
            for i, row in dfperformance.iterrows()
        ]
    )

    medians = pd.DataFrame(
        [
            {"name": cat, "median": dfperformance.loc[dfperformance['name'] == cat, 'stars'].values[0], "lo": "--", "hi": "-"}
            for cat in performance_categories
        ]
    )

    y_axis = alt.Y("name").axis(
        title=None,
        offset=50,
        labelFontWeight="bold",
        ticks=False,
        grid=True,
        domain=False,
    )

    base = alt.Chart(medians).encode(y_axis)

    bubbles = (
        alt.Chart(values)
        .transform_filter(
            (alt.datum.name != "Participant ID")
        )
        .mark_circle(color="#6EB4FD")
        .encode(
            alt.X("value:Q").title(None),
            y_axis,
            alt.Size("num_ratings:Q", scale=alt.Scale(range=[100, 1000])).legend(offset=75, title="Number of ratings"),
            tooltip=[alt.Tooltip("num_ratings:Q", format=".0f").title("Number of ratings")],  # Ensure count is displayed as integer
        )
    )

    ticks = base.mark_tick(color="black").encode(
        alt.X("median:Q")
        .axis(grid=False, values=[1, 2, 3, 4, 5], format=".0f")
        .scale(domain=[0, 6]),
    )

    texts_lo = base.mark_text(align="right", x=-5).encode(text="lo")
    texts_hi = base.mark_text(align="left", x=255).encode(text="hi")

    chart = (bubbles + ticks + texts_lo + texts_hi).properties(
        width=250, height=175
    ).configure_view(stroke=None)

    st.altair_chart(chart, use_container_width=True)
