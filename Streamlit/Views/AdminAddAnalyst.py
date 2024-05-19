import streamlit as st
import pandas as pd
from Networking.Networking import Networking

def app():
    st.title('Add Analyst')
    # Function to add user to the system
    Network = Networking()
    new_analyst_fname = st.text_input("First Name")
    new_analyst_lname = st.text_input("Last Name")
    new_analyst_email = st.text_input("Email")
    new_analyst_password = st.text_input("Password",type="password")
    add_button = st.button("Add Analyst")
    if add_button:
        missing_fields = []
        if not new_analyst_fname:
                missing_fields.append("First Name")
        if not new_analyst_lname:
                missing_fields.append("Last Name")
        if not new_analyst_email:
                missing_fields.append("Email")
        if not new_analyst_password:
                missing_fields.append("password") 
        if missing_fields:
                st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            new_user = Network.post_signup('Data Analyst',new_analyst_fname,new_analyst_lname, new_analyst_email,new_analyst_password)
            st.success("DataAnalyst added successfully!")
            # Display added user
            st.write(new_user)# DH EL VIRABLE EL FIH HGT EL USER @OMAR
            # Add user to session state
            analysts = st.session_state.get('analysts', [])
            analysts.append(new_user)
            st.session_state.analysts = analysts
    st.subheader('View Analysts')
    #analysts = st.session_state.get('analysts', [])
    df = Network.get_table('Data Analyst')
    if df:
        st.write(df)
    else:
        st.write("No Analysts added yet.")

