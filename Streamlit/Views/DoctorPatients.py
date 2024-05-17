import streamlit as st
import sys
from Networking.Networking import Networking
import pandas as pd
from ourData.cache import LocalCache
import io
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
st.set_page_config(
    page_title="Risk Assessment",
    layout="wide",  # Set layout to wide mode
    initial_sidebar_state="collapsed",  # Collapse the sidebar initially
)

def app():
    st.write('ALL Your Patients Doctor')
    Network = Networking()
    cacheInMemory = LocalCache()
    st.title("My patients")
    df = cacheInMemory.get_assessment_byDocId_version2()
    st.write(cacheInMemory.get_assessment_byDocId_version2())
    # col1, col2 = st.columns(2)

    columns = df.columns.tolist()
    # Drop the 'id' column
    df = df.drop(columns=['id','MRN'])

    columns = df.columns.tolist()

    # Display DataFrame
    col1, col2 = st.columns(2)

    with col1:
        x_axis = st.selectbox('Select the X-axis', options=columns + ["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns + ["None"])
        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 'Histogram']
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

    # Generate the plot based on user selection
    if st.button('Generate Plot'):
        with col2:
            color = "#c08497"
            fig, ax = plt.subplots(figsize=(8, 6))

            if plot_type == 'Line Plot':
                if y_axis == "None":
                    sns.lineplot(x=df[x_axis], y=df.index, ax=ax, color=color)
                elif x_axis == "None":
                    sns.lineplot(y=df[y_axis], x=df.index, ax=ax, color=color)
                else:
                    sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax, color=color)
            elif plot_type == 'Bar Chart':
                if y_axis == "None":
                    sns.barplot(x=df[x_axis], y=df.index, ax=ax, color=color)
                elif x_axis == "None":
                    sns.barplot(y=df[y_axis], x=df.index, ax=ax, color=color)
                else:
                    sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax, color=color)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax, color=color)
            elif plot_type == 'Distribution Plot':
                if x_axis == "None":
                    sns.histplot(df[y_axis], kde=True, ax=ax, color=color)
                    ax.set_ylabel('Density')
                elif y_axis == "None":
                    sns.histplot(df[x_axis], kde=True, ax=ax, color=color)
                    ax.set_xlabel('Density')
                else:
                    sns.histplot(df[x_axis], kde=True, ax=ax, color=color)
                    ax.set_ylabel('Density')
            elif plot_type == 'Count Plot':
                if y_axis == "None":
                    sns.countplot(x=df[x_axis], ax=ax, color=color)
                elif x_axis == "None":
                    sns.countplot(y=df[y_axis], ax=ax, color=color)
                else:
                    sns.countplot(x=df[x_axis], y=df[y_axis], ax=ax, color=color)
            elif plot_type == 'Histogram':
                if x_axis != "None":
                    df[x_axis].hist(ax=ax, color=color)
                elif y_axis != "None":
                    df[y_axis].hist(ax=ax, color=color)

            # Customize plot
            if x_axis != "None" and y_axis != "None":
                plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=14)
                plt.xlabel(x_axis, fontsize=12)
                plt.ylabel(y_axis, fontsize=12)
            elif x_axis != "None":
                plt.title(f'{plot_type} of {x_axis}', fontsize=14)
                plt.xlabel(x_axis, fontsize=12)
                plt.ylabel('', fontsize=12)
            elif y_axis != "None":
                plt.title(f'{plot_type} of {y_axis}', fontsize=14)
                plt.xlabel('', fontsize=12)
                plt.ylabel(y_axis, fontsize=12)

            plt.xticks(rotation=90)

            # Show plot
            st.pyplot(fig)


