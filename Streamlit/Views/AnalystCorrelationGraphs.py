import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.graph_objects as go
from ourData.cache import LocalCache

Cache = LocalCache()

def radar_plot(df, col1, col2, col3):
    try:
        # Normalize the data for radar chart
        min_val = min(df[col1].min(), df[col2].min(), df[col3].min())
        max_val = max(df[col1].max(), df[col2].max(), df[col3].max())
        normalized_df = (df[[col1, col2, col3]] - min_val) / (max_val - min_val)

        # Create categories and values for radar chart
        categories = [col1, col2, col3]
        values = normalized_df.mean().tolist()

        # Define colors
        colors = ["#c8387d", "#169DA6","#b4f8ed"]

        # Create radar chart
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Average',
            line=dict(color=colors[0])
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False
        )

        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

def app():
    st.title('Analyst Correlation Graphs')


    # Fetch data from the cache
    data = Cache.get_dashBoardData_forAnalysts()

    # List of columns to be used in the scatter plot
    scatterPlotColumns = ['Age', 'First_BMI', 'size_cm']

    # Convert the columns to numeric, coercing errors to NaN
    for col in scatterPlotColumns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Append 'Tumor_Type' to the list of columns for further processing
    scatterPlotColumns.append('Tumor_Type')

    # Clean the data by dropping rows with NaNs in the specified columns
    data_clean = data[scatterPlotColumns].dropna()

    # URL of the image to be displayed
    image_url_Numerical_Features_Distribution = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/Numerical_Features_Distribution.png"

    # Create a scatter plot using Plotly
    st.write("<br>", unsafe_allow_html=True) 
    st.subheader('Age vs. BMI Bubble Chart')
    fig = px.scatter(
        data_clean,
        x='Age',
        y='First_BMI',
        size='size_cm',
        color='Tumor_Type',
        hover_name='Tumor_Type',
        labels={'Age': 'Age', 'First_BMI': 'BMI'},
        size_max=60,
        color_discrete_map={
            'Invasive duct carcinoma (NST)': 'blue',
            'Invasive duct carcinoma in situ, DCIS': 'green',
            'Ductal carcinoma NOS': 'orange',
            'Other': 'red',
            'Mixed Tumor': 'purple',
            'Invasive tubular/cribriform carcinoma': 'brown',
            'Mucinous adenocarcinoma': 'pink',
            'Invasive Lobular carcinoma NOS': 'cyan'
        }
    )

    # Show the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    
    st.write("<br>", unsafe_allow_html=True) 
    st.subheader('BMI Distribution by Tumor Type')
    # Make box plot
    fig = px.box(data, x='Tumor_Type', y='First_BMI')

    # Show the box plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Create columns for layout with specified relative widths
    col12, col21 = st.columns([3, 2])
    # Display the radar plot in the first column
    with col12:
        st.subheader('Radar Plot')
        st.write("<br>", unsafe_allow_html=True) 
        st.markdown("""
            This radar chart illustrates the correlation of these metrics, highlighted by the pink shaded area, which connects each data point on the axes. This visualization method provides an effective snapshot of health-related measurements, offering insights into how each metric relates to the others within a single individual's data.

            - **Age**: Represents the age of the individual. Values are scaled between 0 and 1, where 1 would represent the maximum age in the dataset.
            - **First_BMI**: Indicates the initial Body Mass Index (BMI) of the individual, with values also scaled from 0 to 1. This scale allows for comparison across a standardized range.
            - **Size in cm**: Measures the size (likely of a medical concern such as a tumor) in centimeters, normalized on a 0 to 1 scale, simplifying comparison across different sizes.
            """, unsafe_allow_html=True)


    # Display the image in the second column
    with col21:
        radar_plot(data_clean, "First_BMI", "size_cm", "Age")

    
    st.subheader("Features Distribution")
    st.write("<br>", unsafe_allow_html=True)
    # Create columns for layout with specified relative widths
    col112,colspace, col121 = st.columns([10,1,10])
        # Display the radar plot in the first column
    with col112:
        # Create a pair plot using Seaborn
        pairplot = sns.pairplot(data[['Age', 'First_BMI', 'size_cm', 'KI67']], diag_kind='kde')

        # Show the pair plot in Streamlit
        st.pyplot(pairplot)

    # Display the image in the second column
    with col121:
        st.image(image_url_Numerical_Features_Distribution)


