import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import random
import subprocess
import re
from datetime import datetime, timedelta

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

   
    st.markdown("""---""")
    st.subheader("Evaluation Results")

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
