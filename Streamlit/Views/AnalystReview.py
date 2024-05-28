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

def app():
    st.title('ALL Patients with Setted Ground Truth')
    temp=None
 
    # Instantiate cache object
    Network = Networking()
    cacheInMemory = LocalCache()
    df = cacheInMemory.get_assessment_byDocId_version2()
    
     # Display the dataframe
     
    # Display the dataframe
    st.dataframe(df)

    # Initialize session state for reviewed patients and selected row
    if 'reviewed_patients' not in st.session_state:
        st.session_state.reviewed_patients = pd.DataFrame()
    if 'selected_row' not in st.session_state:
        st.session_state.selected_row = pd.DataFrame()

    # Input box to enter the MRN of the patient
    mrn_input = st.text_input("Enter MRN of the Patient:")

    # Button to review the selected row
    if st.button("Review"):
        if mrn_input.isdigit():
            mrn_input = int(mrn_input)
            if mrn_input in df['MRN'].values:
                st.session_state.selected_row = df[df['MRN'] == mrn_input]
                st.write("Selected Row Displayed Horizontally:")
                st.table(st.session_state.selected_row)
            else:
                st.error("MRN not found. Please enter a valid MRN.")
        else:
            st.error("Invalid input. Please enter a numeric MRN.")

    # Reviewed button to confirm review
    if not st.session_state.selected_row.empty:
        if st.button("Reviewed", key="reviewed_button"):
            st.success("Reviewed button clicked successfully")
            st.session_state.reviewed_patients = pd.concat([st.session_state.reviewed_patients, st.session_state.selected_row])
            st.session_state.selected_row = pd.DataFrame()  # Clear the selected row after reviewing

    # Display reviewed patients
    if st.session_state.reviewed_patients.empty:
        st.write("No reviewed patients yet.")
    else:
        st.write("Reviewed Patients")
        st.table(st.session_state.reviewed_patients)