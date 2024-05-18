import streamlit as st
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
import pandas as pd
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

def count_yes_no_in_column(df, column_title):
    try:
        counts = df[column_title].value_counts()
        yes_count = counts.get("Yes", 0)
        no_count = counts.get("No", 0)
        return yes_count, no_count
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def count_responses_in_column(df, column_title, categories):
    try:
        counts = df[column_title].value_counts()
        counts_array = [counts.get(category, 0) for category in categories]
        return counts_array
    except Exception as e:
        print(f"An error occurred: {e}")
        return [None] * len(categories)

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

def draw_bar_chart(chart_title, x_title, y_title, categories, values):
    try:
        # Define colors from the palette
        colors = ['#b7dbda', '#b7bfbe', '#d7c8e9']
        colors = ['#d8e2dc', '#9d8189', '#ffe5d9']
        # colors = ['#ed5894', '#fffae3', '#f7af9d']
        colors = ['#cc8562', '#c08497', '#3a4440']
        
        # Create the bar chart
        plt.figure(figsize=(8, 6))
        bars = plt.bar(categories, values, color=colors)

        # Add title and labels
        plt.title(chart_title)
        plt.xlabel(x_title)
        plt.ylabel(y_title)

        # Apply custom colors to bars
        for i, bar in enumerate(bars):
            bar.set_color(colors[i % len(colors)])

        # Save the plot as an image
        plt.savefig('bar_chart.png')

        # Show the saved image
        plt.close()  # Close the plot to release resources

        # Display the saved image using Streamlit
        st.image('bar_chart.png')

    except Exception as e:
        print(f"An error occurred: {e}")


def draw_pareto_chart(df, column_to_analyze):
    try:
        fig, ax = plt.subplots(figsize=(4, 2))

        # Count frequencies
        freq = df[column_to_analyze].value_counts()

        # Calculate cumulative frequencies
        cumulative_freq = freq.cumsum()

        # Calculate percentage
        percentage = (freq / freq.sum()) * 100

        # Calculate cumulative percentage
        cumulative_percentage = (cumulative_freq / cumulative_freq.max()) * 100

        # Plot Pareto chart
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.bar(freq.index.astype(str), freq, color='#cc8562')  # First color
        ax2.plot(freq.index.astype(str), cumulative_percentage, color='#c08497', marker='o')  # Third color
        ax1.set_xlabel('Categories')
        ax1.set_ylabel('Frequency', color='#cc8562')  # First color
        ax2.set_ylabel('Cumulative Percentage', color='#c08497')  # Third color
        plt.title('Pareto Chart for {}'.format(column_to_analyze))
        
        # Rotate x-axis labels
        for tick in ax1.get_xticklabels():
            tick.set_rotation(90)

        # Display the plot
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
def plot_histogram(df, col_name):
    # Check if the column exists in the DataFrame
    if col_name not in df.columns:
        st.error(f"Column '{col_name}' does not exist in the DataFrame.")
        return
    
    # Check if the column is numerical
    if not pd.api.types.is_numeric_dtype(df[col_name]):
        st.error(f"Column '{col_name}' is not a numerical column.")
        return
    
    # Plotting the histogram
    st.write(f"Histogram for column: {col_name}")
    colors = ['#cc8562', '#c08497', '#3a4440']
    fig, ax = plt.subplots()
    ax.hist(df[col_name].dropna(), bins=30, edgecolor='k', color=colors[0])
    ax.set_xlabel(col_name)
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram')
    st.pyplot(fig)
def horizontal_bar_chart(data, categorical_column):
    # Grouping data by the categorical column and counting occurrences
    grouped_data = data[categorical_column].value_counts()
    colors = ['#cc8562', '#c08497', '#3a4440']
    # Plotting horizontal bar chart
    fig, ax = plt.subplots()
    ax.barh(grouped_data.index, grouped_data.values,color=colors)
    
    # Customizing labels and title
    ax.set_xlabel('Count')
    ax.set_ylabel(categorical_column)
    ax.set_title('Horizontal Bar Chart')
    
    # Displaying the plot in Streamlit
    st.pyplot(fig)     
def missing_data_bar_chart(data):
    colors = ['#cc8562', '#c08497', '#3a4440']
    # Calculate missing values for each column
    missing_values = data.isnull().sum()
    
    # Plotting horizontal bar chart
    fig, ax = plt.subplots()
    ax.barh(missing_values.index, missing_values.values, color=colors)
    
    # Customizing labels and title
    ax.set_xlabel('Number of Missing Values')
    ax.set_ylabel('Columns')
    ax.set_title('Missing Data per Column')
    
    # Displaying the plot in Streamlit
    st.pyplot(fig)     
def plot_histogram(df, col_name):
    # Check if the column exists in the DataFrame
    if col_name not in df.columns:
        st.error(f"Column '{col_name}' does not exist in the DataFrame.")
        return
    
    # Check if the column is numerical
    if not pd.api.types.is_numeric_dtype(df[col_name]):
        st.error(f"Column '{col_name}' is not a numerical column.")
        return
    colors = ['#cc8562', '#c08497', '#3a4440']
    # Plotting the histogram
    st.write(f"Histogram for column: {col_name}")
    fig, ax = plt.subplots()
    ax.hist(df[col_name].dropna(), bins=30, edgecolor='k',color=colors[1])
    ax.set_xlabel(col_name)
    ax.set_ylabel('Frequency')
    st.pyplot(fig)    
def app():
    st.write('Doctor DashBoard')
    st.title("Dashboard")
    
    file_path = "ourData/cairouniversity_march_known_nooutliers.xlsx"
    file_site_path="ourData/mohraData.xlsx"

    try:
        df = pd.read_excel(file_path)
        df_site = pd.read_excel(file_site_path)
        
        col11,col22=st.columns([3, 1])    
        # Arrange charts in rows
        with col11:
            
            col1a,col2a=st.columns(2)
            # st.header('Radar Plot Generator')
            # radar_plot(df, "First_BMI", "size_cm" , "Age") 
            with col1a:
             st.header('Grade Distribution')   
             horizontal_bar_chart(df, "Grade") 
            with col2a:
                st.header('family history Distribution')
                horizontal_bar_chart(df, "family_history")
            # missing_data_bar_chart(df)
            # st.header("Pareto Chart")
            # st.write("This is the Pareto chart:")
            # # Call the function to draw Pareto chart
            # draw_pareto_chart(df, "Tumor_Type")  # Change "First_BMI" to any column you want to analyze
        st.header("Bar Charts and Pie Charts")
        st.write("These are the bar charts and pie charts:")
        
        # Draw bar charts and pie charts
        categories1 = ["Post-M", "Pre-M", "Unrecorded"]
        counts1 = count_responses_in_column(df, "Menopausal_state", categories1)
        
        categories2 = ["Unilateral", "Bilateral"]
        counts2 = count_responses_in_column(df, "Unilateral_Bilateral", categories2)
        
        categories3 = ["Yes - BC","Yes - both","Yes - other cancers", "No","Unrecorded"]
        counts3 = count_responses_in_column(df, "family_history", categories3)
        
        categories4 = ["N0", "N1", "N2", "Nx"]
        counts4 = count_responses_in_column(df, "N", categories4)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Menopausal State Distribution")
            draw_bar_chart("Menopausal State Distribution", "Menopausal State", "Count", categories1, counts1)
            st.subheader("First BMI State Distribution")
            plot_histogram(df, "First_BMI")
        with col2:
            st.subheader("Unilateral Bilateral Distribution")
            draw_bar_chart("Unilateral Bilateral Distribution", "Unilateral Bilateral", "Count", categories2, counts2)
            st.subheader("Age Distribution")
            plot_histogram(df, "Age")
        
        with col3:
            st.subheader("T Distribution")
            st.subheader(" ")
            draw_bar_chart("T", "T", "Count", categories3, counts3)
            st.subheader("Tumer size Distribution")
            plot_histogram(df, "size_cm")
        
        with col4:
            st.subheader("N Distribution")
            st.subheader(" ")
            draw_bar_chart("N Distribution", "N", "Count", categories4, counts4)
            st.subheader("KI67 Distribution")
            plot_histogram(df, "KI67")
        
        # Display pie charts in a row
        st.header("Pie Charts")
        st.write("These are the pie charts:")
        pie_col1, pie_col2, pie_col3, pie_col4 = st.columns(4)
        custom_colors = ['#ffcad4', '#3a4440']
        # Pie chart for CVD
        with pie_col1:
            column_title = "CVD"
            labels = ['No', 'Yes']
            yes_count, no_count = count_yes_no_in_column(df, column_title)
            values = [no_count, yes_count]
            # custom_colors = ['#b7dbda', '#b7bfbe']
            # Create the Pie chart with custom colors
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=custom_colors))])
            # Update layout and display the chart
            ig.update_layout(
                title=f'{column_title} Yes/No Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
                        
        # Pie chart for DM
        with pie_col2:
            column_title = "DM"
            labels = ['No', 'Yes']
            yes_count, no_count = count_yes_no_in_column(df, column_title)
            values = [no_count, yes_count]
            # custom_colors = ['#ffe5d8', '#9e8189']
            # Create the Pie chart with custom colors
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=custom_colors))])
            # Update layout and display the chart
            ig.update_layout(
                title=f'{column_title} Yes/No Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
        
        # Pie chart for HTN
        with pie_col3:
            column_title = "HTN"
            labels = ['No', 'Yes']
            yes_count, no_count = count_yes_no_in_column(df, column_title)
            values = [no_count, yes_count]
            # custom_colors = ['#b7dbda', '#b7bfbe']
            # Create the Pie chart with custom colors
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=custom_colors))])
            # Update layout and display the chart
            ig.update_layout(
                title=f'{column_title} Yes/No Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
        # Pie chart for VTE
        with pie_col4:
            column_title = "VTE"
            labels = ['No', 'Yes']
            yes_count, no_count = count_yes_no_in_column(df, column_title)
            values = [no_count, yes_count]
            # custom_colors = ['#b7dbda', '#b7bfbe']
            # Create the Pie chart with custom colors
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=custom_colors))])
            # Update layout and display the chart
            ig.update_layout(
                title=f'{column_title} Yes/No Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
        with col22:    
            # Display dataframe
            st.header("Tumer Location")
            st.write(" ")
            st.dataframe(df_site,
                        column_order=("site", "cases"),
                        hide_index=True,
                        width=None,
                        column_config={
                            "site": st.column_config.TextColumn(
                                "site",
                            ),
                            "cases": st.column_config.ProgressColumn(
                                "cases",
                                format="%f",
                                min_value=0,
                                max_value=max(df_site.cases),
                            )}
                        )
              
    except Exception as e:
        st.error(f"An error occurred: {e}")
