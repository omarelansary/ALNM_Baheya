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
        colors = ['#cc8562', '#c08497', '#3a4440']

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
            title='Radar Plot',
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
    col12,col21=st.columns([3,2])
    data = Cache.get_dashBoardData_forAnalysts()
    # data = pd.read_excel('ourData/cairouniversity_march_known_nooutliers.xlsx')
    # data = Cache.get_dashBoardData_forAnalysts()
    # Clean and prepare your data
    data_clean = data[['Age', 'First_BMI', 'size_cm', 'Tumor_Type']].dropna()
    image_url_Numerical_Features_Distribution = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/Numerical_Features_Distribution.png"
    
    with col12:
     radar_plot(data, "First_BMI", "size_cm", "Age")
    col123,col222=st.columns([3,2]) 
    with col222: 
     st.image(image_url_Numerical_Features_Distribution)
    
    fig = px.scatter(
        data_clean,
        x='Age',
        y='First_BMI',
        size='size_cm',
        color='Tumor_Type',
        hover_name='Tumor_Type',
        title='Age vs. BMI Bubble Chart',
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

    fig = px.box(data, x='Tumor_Type', y='First_BMI', title='BMI Distribution by Tumor Type')

    # Show the box plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Create a pair plot using Seaborn
    pairplot = sns.pairplot(data[['Age', 'First_BMI', 'size_cm', 'KI67']], diag_kind='kde')

    # Show the pair plot in Streamlit
    st.pyplot(pairplot)

