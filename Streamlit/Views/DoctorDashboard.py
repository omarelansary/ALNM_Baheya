import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
from math import pi
import numpy as np
import altair as alt

awamacolor=["#c8387d" , "#ec6989","#169DA6","#b4f8ed"]
text_color = '#2C3E50'  # Customize text color as needed

def count_yes_no_in_column(df, column_title):
    try:
        counts = df[column_title].value_counts()
        yes_count = counts.get("Yes", 0)
        no_count = counts.get("No", 0)
        return yes_count, no_count
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
def count_postive_negative_in_column(df, column_title):
    try:
        counts = df[column_title].value_counts()
        positive_count = counts.get("Positive", 0)
        negative_count = counts.get("Negative", 0)
        return positive_count, negative_count
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
        awamacolor=["#c8387d" , "#ec6989","#169DA6"]
        # Create radar chart
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Average',
            line=dict(color=awamacolor[0])
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
        bars = plt.bar(categories, values, color=awamacolor)

        # Add title and labels
        plt.title(chart_title)
        plt.xlabel(x_title)
        plt.ylabel(y_title)

        # Apply custom colors to bars
        for i, bar in enumerate(bars):
            bar.set_color(colors[i % len(awamacolor)])

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
    ax.hist(df[col_name].dropna(), bins=30, edgecolor='k', color=awamacolor[0])
    ax.set_xlabel(col_name)
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram')
    st.pyplot(fig)
def horizontal_bar_chart(chart_title, x_title, y_title, data, categorical_column):
    try:
        # Grouping data by the categorical column and counting occurrences
        grouped_data = data[categorical_column].value_counts()

        # Ensure there are enough colors for the bars
        colors = awamacolor * (len(grouped_data) // len(awamacolor) + 1)
        colors = colors[:len(grouped_data)]

        # Plotting horizontal bar chart
        fig = go.Figure(go.Bar(y=grouped_data.index, x=grouped_data.values, orientation='h', marker=dict(color=colors)))

        # Update layout with title
        fig.update_layout(
            title=chart_title,
            xaxis=dict(title=x_title),
            yaxis=dict(title=y_title),
            font=dict(color=text_color)  # Set text color
        )

        # Displaying the chart
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
   
def missing_data_bar_chart(data):
    colors = ['#cc8562', '#c08497', '#3a4440']
    # Calculate missing values for each column
    missing_values = data.isnull().sum()
    
    # Plotting horizontal bar chart
    fig, ax = plt.subplots()
    ax.barh(missing_values.index, missing_values.values, color=awamacolor)
    
    # Customizing labels and title
    ax.set_xlabel('Number of Missing Values')
    ax.set_ylabel('Columns')
    ax.set_title('Missing Data per Column')
    
    # Displaying the plot in Streamlit
    st.pyplot(fig)     
def plot_histogram(chart_title, x_title, y_title, data, col_name):
    try:
        # Check if the column exists in the DataFrame
        if col_name not in data.columns:
            st.error(f"Column '{col_name}' does not exist in the DataFrame.")
            return
        
        # Check if the column is numerical
        if not pd.api.types.is_numeric_dtype(data[col_name]):
            st.error(f"Column '{col_name}' is not a numerical column.")
            return
        
        # Plotting the histogram
        fig = go.Figure(go.Histogram(x=data[col_name], marker=dict(color='#169DA6')))
        
        # Update layout with title
        fig.update_layout(
            title=chart_title,
            xaxis=dict(title=x_title),
            yaxis=dict(title=y_title)
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        print(f"An error occurred: {e}")

def draw_bar_chart(chart_title, x_title, y_title, categories, values):
    try:
        # Define colors from the palette
        colors = ['#b7dbda', '#b7bfbe', '#d7c8e9']
        colors = ['#d8e2dc', '#9d8189', '#ffe5d9']
        colors = ['#cc8562', '#c08497', '#3a4440']
        
        # Create the bar chart
        fig = go.Figure(go.Bar(x=categories, y=values, marker=dict(color=awamacolor)))

        # Update layout with title
        fig.update_layout(
            title=chart_title,
            xaxis=dict(title=x_title),
            yaxis=dict(title=y_title),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        print(f"An error occurred: {e}")
def count_tumor_sites(df):
    # Count occurrences of each tumor site
    tumor_site_counts = df['Site'].value_counts().reset_index()
    tumor_site_counts.columns = ['site', 'cases']
    return tumor_site_counts
def app():
    st.title("Physician Dashboard")
    
    file_path = "cairouniversity_march_known_nooutliers (1).xlsx"

    try:
        df = pd.read_excel(file_path)
        
        col11, col22 = st.columns([3, 1])
        
        with col11:
            col1a, col2a = st.columns(2)
            with col1a:
                horizontal_bar_chart("Grade Distribution", "Count", "Grade", df, "Grade")
            with col2a:
                horizontal_bar_chart("Family History Distribution", "Count", "Family History", df, "family_history")

        st.header("Bar Charts:")
        
        categories1 = ["Post-M", "Pre-M", "Unrecorded"]
        counts1 = count_responses_in_column(df, "Menopausal_state", categories1)
        
        categories2 = ["Unilateral", "Bilateral"]
        counts2 = count_responses_in_column(df, "Unilateral_Bilateral", categories2)
        
        categories3 = ["Yes - BC", "Yes - both", "Yes - other cancers", "No", "Unrecorded"]
        counts3 = count_responses_in_column(df, "family_history", categories3)
        
        categories4 = ["N0", "N1", "N2", "Nx"]
        counts4 = count_responses_in_column(df, "N", categories4)
        
        categories5 = ["T1", "T2", "T3", "T4", "Tis"]
        counts5 = count_responses_in_column(df, "T", categories5)
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            draw_bar_chart("Menopausal State Distribution", "Menopausal State", "Count", categories1, counts1)

        with col2:
            draw_bar_chart("Unilateral Bilateral Distribution", "Unilateral Bilateral", "Count", categories2, counts2)

        with col3:
            draw_bar_chart("T Distribution","t", "Count", categories5, counts5)
            # draw_bar_chart("Family History Distribution", "Family History", "Count", categories3, counts3)

        with col4:
            draw_bar_chart("N Distribution","N", "Count", categories4, counts4)
        st.header("Histograms:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            plot_histogram("First BMI State Distribution", "First BMI", "Frequency", df, "First_BMI")

        with col2:
            plot_histogram("Age Distribution", "Age", "Frequency", df, "Age")

        with col3:
            plot_histogram("Tumor Size Distribution", "Tumor Size (cm)", "Frequency", df, "size_cm")

        with col4:
            plot_histogram("KI67 Distribution", "KI67", "Frequency", df, "KI67")
        st.header("Pie Charts")
        pie_col1, pie_col2, pie_col3, pie_col4 = st.columns(4)
        custom_colors = ['#ffcad4', '#3a4440']
        awamacolorpeichart=[ "#ec6989","#169DA6"]  
        awamacolorpeichart3aks=[ "#c8387d" ,"#b4f8ed"]

        with pie_col1:
            column_title = "Lymphovascular_Invasion"
            labels = ['No', 'Yes']
            yes_count, no_count = count_yes_no_in_column(df, column_title)
            values = [no_count, yes_count]
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=awamacolorpeichart))])
            ig.update_layout(
                title='Lymphovascular Yes/No Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
        
        with pie_col2:
            column_title = "VTE"
            labels = ['No', 'Yes']
            yes_count, no_count = count_yes_no_in_column(df, column_title)
            values = [no_count, yes_count]
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=awamacolorpeichart))])
            ig.update_layout(
                title=f'{column_title} Yes/No Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
        
        with pie_col3:
            column_title = "PR"
            labels = ['Negative', 'Positive']
            positive_count, negtive_count = count_postive_negative_in_column(df, column_title)
            values = [positive_count, negtive_count]
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=awamacolorpeichart))])
            ig.update_layout(
                title=f'{column_title} Positive/Negative Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
        
        with pie_col4:
            column_title = "ER"
            labels = ['Negative', 'Positive']
            positive_count, negtive_count = count_postive_negative_in_column(df, column_title)
            values = [positive_count, negtive_count]
            ig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=awamacolorpeichart))])
            ig.update_layout(
                title=f'{column_title} Positive/Negative Distribution',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(ig, use_container_width=True)
        ###############
        with col22:    
            # Display dataframe
            st.header("Tumor Location")
            st.write(" ")
            df_site = count_tumor_sites(df)
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
                                format="%d",  # Display integer format
                                min_value=0,
                                max_value=max(df_site['cases']),  # Max value for progress bar
                            )}
                        )

        ############
    except Exception as e:
        st.error(f"An error occurred: {e}")

