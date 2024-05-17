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

    # Load the data
    df = cacheInMemory.get_assessment_byDocId_version2()
    
    # Display the editable table
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    # Initialize the session state if not already initialized
    if 'edited_rows' not in st.session_state:
        st.session_state['edited_rows'] = {}

    # Update the session state with changes from data_editor
    st.session_state['edited_rows'] = edited_df.to_dict('index')
    
    # Find the changed rows by comparing session state with the original data
    changes = {}
    for index, row in edited_df.iterrows():
        if not row.equals(df.loc[index]):
            changes[index] = row.to_dict()

    if changes:
        st.write("Changes detected:")
        st.write(changes)
        
        # Extract the row indices of the changes
        changed_rows = list(changes.keys())
        
        # Extract the modified data as a dictionary
        ground_true = changes
        
        # Display the changed rows
        st.write("Changed rows data:")
        st.write(ground_true)
        #  el new grung truth wa el id wa mrn ahomat @omar
        # Get the IDs of the changed rows
        new_id_values = df.loc[changed_rows, 'id'] 
        st.write("IDs of changed rows:")
        st.write(new_id_values.tolist())
        new_MRN_values = df.loc[changed_rows, 'MRN']
        st.write("MRN of changed rows:")
        st.write(new_MRN_values.tolist())
        new_ground_truth_values = df.loc[changed_rows, 'ground_truth']
        st.write("ground_truth:")
        st.write(new_id_values.tolist())

    else:
        st.write("No changes detected.")


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


