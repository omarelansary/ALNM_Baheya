import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.write('Analyst DashBoard')
        # Load your data
    data = pd.read_excel('ourData/cairouniversity_march_known_nooutliers.xlsx')

    # Clean and prepare your data
    data_clean = data[['Age', 'First_BMI', 'size_cm', 'Tumor_Type']].dropna()

    # Create a bubble chart using Plotly
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