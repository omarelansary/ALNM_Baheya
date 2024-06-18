import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from ourData.cache import LocalCache
awamacolor=["#c8387d" , "#ec6989","#169DA6","#b4f8ed"]

def app(userAuthData):

    Cache = LocalCache()

    df=Cache.get_assessment_byDocId(userAuthData['id'])

    # Check if the dataframe is loaded successfully
    if not df.empty:

        # ---- SIDEBAR ----
        st.sidebar.header("Please Filter Here:")
        tumor_grade = st.sidebar.multiselect(
            "Select the Tumor Grade:",
            options=df["patient_grade"].unique(),
            default=df["patient_grade"].unique()
        )

        family_history = st.sidebar.multiselect(
            "Select the Family History:",
            options=df["patient_family_history"].unique(),
            default=df["patient_family_history"].unique(),
        )

        tumor_location = st.sidebar.multiselect(
            "Select the Tumor Location:",
            options=df["patient_site"].unique(),
            default=df["patient_site"].unique()
        )

        t = st.sidebar.multiselect(
            "Select the T:",
            options=df["patient_t"].unique(),
            default=df["patient_t"].unique()
        )
        n = st.sidebar.multiselect(
            "Select the N:",
            options=df["patient_n"].unique(),
            default=df["patient_n"].unique()
        )
        df_selection = df.query(
            "(`patient_grade` == @tumor_grade) & (`patient_family_history` == @family_history) & (`patient_site` == @tumor_location) & (patient_t == @t) & (patient_n == @n)"
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
        average_age = round(df_selection["patient_age"].mean(), 1)
        most_common_location = df_selection["patient_site"].mode()[0]

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
        patients_by_tumor_type = df_selection["patient_tumor_type"].value_counts().reset_index()
        patients_by_tumor_type.columns = ["patient_tumor_type", "Count"]
        fig_tumor_type = px.bar(
            patients_by_tumor_type,
            x="Count",
            y="patient_tumor_type",
            orientation="h",
            title="<b>Patients by Tumor Type</b>",
            color_discrete_sequence=["#169DA6"] * len(patients_by_tumor_type),  # Pink color
            template="plotly_white",
        )
        fig_tumor_type.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False)
        )

        # Example Pie Chart
        tumor_grade_distribution = df_selection["patient_menopausal_state"].value_counts()
        fig_grade = px.pie(
            tumor_grade_distribution,
            values=tumor_grade_distribution.values,
            names=tumor_grade_distribution.index,
            title="<b>Menopausal state Distribution</b>",
            color_discrete_sequence=["#c8387d" , "#ec6989","#169DA6","#b4f8ed", "#C71585"]  # Pink color
        )
        fig_grade.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
        )

        # Example Box Plot
        fig_box = px.box(
            df_selection,
            x="patient_site",
            y="patient_age",
            title="<b>Age Distribution by Tumor Location</b>",
            color="patient_site",
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
