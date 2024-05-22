import streamlit as st
import random
import pandas as pd
import streamlit as st
import subprocess
import re

# Generate 30 different numbers from 0 to 40 for each row
working_days = [random.sample(range(41), 30) for _ in range(3)]

dfdoc = pd.DataFrame(
    {
        "name": ["Dr Ahmed", "Dr Karim", "Dr Yasser"],
        "working_days": working_days
    }
)

# Calculate total working days for each doctor
dfdoc['total_working_days'] = dfdoc['working_days'].apply(sum)

# Find the doctor with the highest total working days
top_doctor = dfdoc.loc[dfdoc['total_working_days'].idxmax()]

# Generate the DataFrame for performance ratings
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
    st.title(':bookmark_tabs: Admin DashBoard')
    # Create a new column for star ratings in visual format
    # dfperformane['star_visual'] = dfperformane['stars'].apply(lambda x: '⭐' * x)
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
    st.subheader("Working Days of Doctors")
    st.dataframe(
        dfdoc,
        column_config={
            "name": "Doctors",
            "working_days": st.column_config.LineChartColumn(
                "Working Days", y_min=0, y_max=40
            ),
        },
        hide_index=True,
        width=1200
    )

    # Display Performance Ratings
    st.subheader("Performance Ratings")
    for i, row in dfperformane.iterrows():
        st.write(f"{row['name']}:", f"{row['stars']}")
        st.progress(row['stars'] / 5)  # Assuming the stars are out of 5

    # # Display the top doctor who worked the most
    # st.subheader("Top Doctor of the Month")
    # st.write(f"Name: {top_doctor['name']}")
    # st.write(f"Total Working Days: {top_doctor['total_working_days']}")


