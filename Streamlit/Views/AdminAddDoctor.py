import streamlit as st
import pandas as pd
from Networking.Networking import Networking

def app():
    st.title('Add Doctor')
    # Function to add user to the system
    Network = Networking()
    new_doctor_fname = st.text_input("First Name")
    new_doctor_lname = st.text_input("Last Name")
    new_doctor_email = st.text_input("Email")
    new_doctor_password = st.text_input("Password",type="password")
    add_button = st.button("Add Doctor")
    if add_button:
        missing_fields = []
        if not new_doctor_fname:
                missing_fields.append("First Name")
        if not new_doctor_lname:
                missing_fields.append("Last Name")
        if not new_doctor_email:
                missing_fields.append("Email")
        if not new_doctor_password:
                missing_fields.append("password") 
        if missing_fields:
                st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            new_user = Network.post_signup('Doctor',new_doctor_fname,new_doctor_lname, new_doctor_email,new_doctor_password)
            st.success("Doctor added successfully!")
            # Display added user
            st.write(new_user)# DH EL VIRABLE EL FIH HGT EL USER @OMAR
            # Add user to session state
            doctor = st.session_state.get('doctor', [])
            doctor.append(new_user)
            st.session_state.doctor = doctor
    st.subheader('View Doctors')
    df = Network.get_table('Doctor')
    if df:
        st.write(df)
    else:
        st.write("No Doctors added yet.")

