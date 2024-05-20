import streamlit as st
import random
import pandas as pd
import streamlit as st
import subprocess
import re
# Set the page layout to wide
# st.set_page_config(layout="wide")

# Generate 30 different numbers from 0 to 40 for each row
working_days = [random.sample(range(41), 30) for _ in range(3)]

dfdoc = pd.DataFrame(
    {
        "name": ["Dr Ahmed", "Dr Karim", "Dr Yasser"],
        "working_days": working_days
    }
)


# Generate the DataFrame
dfperformane = pd.DataFrame(
    {
        "name": ["Performance Rating", "Usability Rating", "Learnability Rating"],
        "stars": [random.randint(2, 5) for _ in range(3)]
    }
)



def check_service_status(service_name):
    details = {}
    try:
        # Execute the systemctl command to check the status of the PostgreSQL service
        result = subprocess.run(['systemctl', 'status', service_name], text=True, capture_output=True)
        # Get the output as a text string
        status_output = result.stdout

        # Check if the service is enabled
        enabled_search = re.search(r'enabled;', status_output)
        details['Enabled'] = "Yes" if enabled_search else "No"

        # Find the active since time
        active_since_search = re.search(r'Active:\s(\d+);', status_output)
        details['Active'] = active_since_search.group(1) if active_since_search else "Not available"

        # Find the number of tasks
        tasks_search = re.search(r'Tasks:\s(\d+)', status_output)
        details['Tasks'] = tasks_search.group(1) if tasks_search else "Not available"

        # Find the memory usage
        memory_search = re.search(r'Memory:\s([\w\d.]+)', status_output)
        details['Memory'] = memory_search.group(1) if memory_search else "Not available"

        return details
    except Exception as e:
        return {"error": str(e)}




def app():
    st.title('Admin DashBoard')
    # Create a new column for star ratings in visual format
    dfperformane['star_visual'] = dfperformane['stars'].apply(lambda x: '⭐' * x)
    st.write(check_service_status('postgresql'))
    # Display the DataFrame in Streamlit
    st.dataframe(
        dfperformane[['name', 'star_visual']],  # Select the columns to display
        column_config={
            "name": "Ratings",
            "star_visual": st.column_config.TextColumn(
                "Stars (1 to 5)",
            ),
        },
        hide_index=True,
        width=1200
    )
    st.dataframe(
        dfdoc,
        column_config={
            "name": "Doctors",
            "working_days": st.column_config.LineChartColumn(
                "Working Days", y_min=0, y_max=40
            ),
        },
        hide_index=True,
        width=1200  # Adjust the width as needed
    )
    st.dataframe(
        dfdoc,
        column_config={
            "name": "Data Analyst",
            "working_days": st.column_config.LineChartColumn(
                "Working Days", y_min=0, y_max=40
            ),
        },
        hide_index=True,
        width=1200  # Adjust the width as needed
    )