import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from ourData.cache import LocalCache

def app():

    Cache = LocalCache()

    df = Cache.get_data_from_excel()

    # Check if the dataframe is loaded successfully
    if df is None:
        st.stop()

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    tumor_grade = st.sidebar.multiselect(
        "Select the Tumor Grade:",
        options=df["Grade"].unique(),
        default=df["Grade"].unique()
    )

    family_history = st.sidebar.multiselect(
        "Select the Family History:",
        options=df["family_history"].unique(),
        default=df["family_history"].unique(),
    )

    tumor_location = st.sidebar.multiselect(
        "Select the Tumor Location:",
        options=df["Site"].unique(),
        default=df["Site"].unique()
    )

    t = st.sidebar.multiselect(
        "Select the T:",
        options=df["T"].unique(),
        default=df["T"].unique()
    )
    n = st.sidebar.multiselect(
        "Select the N:",
        options=df["N"].unique(),
        default=df["N"].unique()
    )
    df_selection = df.query(
        "(`Grade` == @tumor_grade) & (`family_history` == @family_history) & (`Site` == @tumor_location) & (T == @t) & (N == @n)"
    )

    # Check if the dataframe is empty:
    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop() # This will halt the app from further execution.

    # ---- MAINPAGE ----
    st.title(":bar_chart: Dashboard")
    st.markdown("##")

    # TOP KPI's (example KPIs, update with relevant columns)
    total_patients = len(df_selection)
    average_age = round(df_selection["Age"].mean(), 1)
    most_common_location = df_selection["Site"].mode()[0]

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Patients:")
        st.subheader(f"{total_patients}")
    with middle_column:
        st.subheader("Average Age:")
        st.subheader(f"{average_age} years")
    with right_column:
        st.subheader("Most Common Tumor Location:")
        st.subheader(f"{most_common_location}")

    st.markdown("""---""")

    # Bar Chart for Patients by Tumor Type
    patients_by_tumor_type = df_selection["Tumor_Type"].value_counts().reset_index()
    patients_by_tumor_type.columns = ["Tumor_Type", "Count"]
    fig_tumor_type = px.bar(
        patients_by_tumor_type,
        x="Count",
        y="Tumor_Type",
        orientation="h",
        title="<b>Patients by Tumor Type</b>",
        color_discrete_sequence=["#E75480"] * len(patients_by_tumor_type),  # Pink color
        template="plotly_white",
    )
    fig_tumor_type.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    # Example Pie Chart
    tumor_grade_distribution = df_selection["Menopausal_state"].value_counts()
    fig_grade = px.pie(
        tumor_grade_distribution,
        values=tumor_grade_distribution.values,
        names=tumor_grade_distribution.index,
        title="<b>Menopausal state Distribution</b>",
        color_discrete_sequence=["#FFC0CB", "#FF69B4", "#FF1493", "#DB7093", "#C71585"]  # Pink color
    )
    fig_grade.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Example Box Plot
    fig_box = px.box(
        df_selection,
        x="Site",
        y="Age",
        title="<b>Age Distribution by Tumor Location</b>",
        color="Site",
        color_discrete_sequence=px.colors.qualitative.Pastel  # Use a pastel color palette
    )
    fig_box.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_tumor_type, use_container_width=True)
    right_column.plotly_chart(fig_grade, use_container_width=True)

    st.plotly_chart(fig_box, use_container_width=True)

    # Display filtered data table
    st.subheader("Filtered Data")
    st.write(df_selection)

    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


