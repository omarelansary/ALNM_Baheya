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

def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'


def app():
    st.title(':bookmark_tabs: Admin DashBoard')
    # Create a new column for star ratings in visual format
    # dfperformane['star_visual'] = dfperformane['stars'].apply(lambda x: '⭐' * x)
    st.write(check_service_status('postgresql'))
    # Display the DataFrame in Streamlit
    # st.dataframe(
    #     dfperformane[['name', 'star_visual']],  # Select the columns to display
    #     column_config={
    #         "name": "Ratings",
    #         "star_visual": st.column_config.TextColumn(
    #             "Stars (1 to 5)",
    #         ),
    #     },
    #     hide_index=True,
    #     width=1200
    # )
    st.markdown("##")

# TOP KPI's (example KPIs, update with relevant columns)
    Tolal_doctors_num=len(dfdoc['name'])
    Tolal_analyst_num=len(dfdoc['name'])
    Total_total=Tolal_doctors_num+Tolal_analyst_num+1
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Physicians:")
        st.subheader(f"{Tolal_doctors_num}")
    with middle_column:
        st.subheader("Total Data Analyst:")
        st.subheader(f"{Tolal_analyst_num} years")
    with right_column:
        st.subheader("Total Website Users:")
        st.subheader(f"{Total_total}")

    st.markdown("""---""")

    # col = st.columns((1.5, 4.5, 2), gap='medium')
    # with col[0]:
    #     docs_name="Doctors"
    #     Tolal_doctors_num=len(dfdoc['name'])
    #     Tolal_analyst_num=len(dfdoc['name'])
    #     st.metric(label=docs_name, value=Tolal_analyst_num)
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
    st.subheader("Performance Ratings")
    for i, row in dfperformane.iterrows():
        st.write(f"{row['name']}:",f"{row['stars']}")
        st.progress(row['stars'] / 5)  # Assuming the stars are out of 5