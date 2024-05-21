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

# st.set_page_config(
#     page_title="Risk Assessment",
#     layout="wide",  # Set layout to wide mode
#     initial_sidebar_state="collapsed",  # Collapse the sidebar initially
# )

def app():
    st.write('ALL Your Patients')
    Network = Networking()
    cacheInMemory = LocalCache()
    st.title("My patients")
    
    # Load the data
    df = cacheInMemory.get_assessment_byDocId_version2()
    st.dataframe(df)
    # Initialize the session state if not already initialized
    if 'edit_mode' not in st.session_state:
        st.session_state['edit_mode'] = False
    if 'selected_mrn' not in st.session_state:
        st.session_state['selected_mrn'] = None

    # Select MRN before enabling editing
    st.write("Select MRN to edit ground_truth:")
    selected_mrn = st.selectbox(
        "Select MRN",
        df['MRN'].unique()
    )
    st.write(f"Editing ground_truth for MRN: {selected_mrn}")

    # Create an "Edit" button to enable editing
    if st.button("Edit"):
        st.session_state['edit_mode'] = True

    if st.session_state['edit_mode']:
        # Make only the ground_truth column editable for the selected MRN
        edited_df = df.copy()
        mask = edited_df['MRN'] == selected_mrn
        st.write("Selected Row:")
        st.write(edited_df[mask])
        
        # Allow the user to select the new ground truth value from a dropdown menu
        new_ground_truth = st.selectbox("Select New Ground Truth", ["0", "1"])

        # Update the ground_truth column with the new value
        edited_df.loc[mask, 'ground_truth'] = new_ground_truth
        # Display the entire row corresponding to the selected MRN

    else:
        edited_df = df.copy()

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
        # Extract the row indices of the changes
        if st.button("Save New Ground truth"):
            changed_rows = list(changes.keys())
            
            # Extract the IDs, MRNs, and new ground_truth values from the changed rows
            new_id_values = df.loc[changed_rows, 'id']
            new_MRN_values = df.loc[changed_rows, 'MRN']
            new_ground_truth_values = [changes[index]['ground_truth'] for index in changed_rows]

            # Create a DataFrame with the extracted values
            omr_change = pd.DataFrame({
                'id': new_id_values,
                'MRN': new_MRN_values,
                'ground_truth': new_ground_truth_values
            })

            # Display the new DataFrame
            st.write("Done")

    else:
        st.write("No changes detected.")

# Run the app













# Call the app function to run the Streamlit app


    # col1, col2 = st.columns(2)

    columns = df.columns.tolist()
    # Drop the 'id' column
    # df = df.drop(columns=['id','MRN'])

    columns = df.columns.tolist()

    # Display DataFrame
    col1, col2 = st.columns(2)

    with col1:
        plot_list = ['Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 'Histogram']
        plot_type = st.selectbox('Select the type of plot', options=plot_list)
        x_axis = st.selectbox('Select the X-axis', options=columns + ["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns + ["None"])

        # # Assuming columns contains the list of column names from your dataset
        # columns = ['age', 'tumor_size', 'bmi', 'ki67', 'column1', 'column2']  # example columns

        # # Dropdown menu for selecting plot type
        # plot_list = ['Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 'Histogram']
        # plot_type = st.selectbox('Select the type of plot', options=plot_list)

        # # Conditional options for x_axis and y_axis based on selected plot type
        # if plot_type == 'Count Plot':
        #     x_axis = st.selectbox('Select the X-axis', options=columns)
        #     y_axis = None
        # elif plot_type == 'Scatter Plot':
        #     numeric_columns = ['age', 'tumor_size', 'bmi', 'ki67']
        #     x_axis = st.selectbox('Select the X-axis', options=numeric_columns)
        #     y_axis = st.selectbox('Select the Y-axis', options=numeric_columns)
        # elif plot_type == 'Histogram':
        #     numeric_columns = ['age', 'tumor_size', 'bmi', 'ki67']
        #     x_axis = st.selectbox('Select the X-axis', options=numeric_columns)
        #     y_axis = None
        # else:
        #     x_axis = st.selectbox('Select the X-axis', options=columns + ["None"])
        #     y_axis = st.selectbox('Select the Y-axis', options=columns + ["None"])

        # # Output selected options for debugging purposes
        # st.write('Selected plot type:', plot_type)
        # st.write('Selected X-axis:', x_axis)
        # if y_axis:
        #     st.write('Selected Y-axis:', y_axis)
 

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


