import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import random
import subprocess
import re
from datetime import datetime, timedelta

# Function to check service status on Windows
def check_service_status(service_name):
    details = {}
    try:
        result = subprocess.run(['sc', 'query', service_name], text=True, capture_output=True)
        status_output = result.stdout

        running_search = re.search(r'STATE\s+:\s+\d+\s+(\w+)', status_output)
        details['State'] = running_search.group(1) if running_search else "Not available"
        
        # Add more parsing if needed for other details
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

    awamacolor = ["#c8387d", "#ec6989", "#169DA6", "#b4f8ed"]
    bubbles = (
        alt.Chart(values)
        .transform_filter(
            (alt.datum.name != "Participant ID")
        )
        .mark_circle()
        .encode(
            alt.X("value:Q").title(None),
            y_axis,
            alt.Size("num_ratings:Q", scale=alt.Scale(range=[100, 1000])).legend(offset=75, title="Number of ratings"),
            color=alt.Color('name:N', scale=alt.Scale(range=awamacolor)),
            tooltip=[alt.Tooltip("num_ratings:Q", format=".0f").title("Number of ratings")],  # Ensure count is displayed as integer
        )
    )

    ticks = base.mark_tick(color="black").encode(
        alt.X("median:Q")
        .axis(grid=False, values=[1, 2, 3, 4, 5], format=".0f")
        .scale(domain=[0, 6]),
    )

    texts_lo = base.mark_text(align="right", x=-5).encode(text="lo")
    texts_hi = base.mark_text(align="left", x=455).encode(text="hi")

    chart = (bubbles + ticks + texts_lo + texts_hi).properties(
        width=500, height=300  # Adjust width and height as needed
    ).configure_view(stroke=None)

    st.altair_chart(chart, use_container_width=True)
