import streamlit as st
import pandas as pd
from Networking.Networking import Networking
import Components.vaildation

def app():
    st.title('Add Physician')
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
         if not Components.vaildation.validate_username(new_doctor_fname):
          st.warning("aloo.")
         elif not Components.vaildation.validate_username(new_doctor_lname):
          st.warning("aloo.")    
         elif not Components.vaildation.validate_email(new_doctor_email):
          st.warning("Invalid email format.")
         else:
            validation_result = Components.vaildation.validate_password(new_doctor_password)
            st.write("Validation result:", validation_result)  # Print validation result
            if validation_result == "VALID":
                        Components.vaildation.signup(new_doctor_fname, new_doctor_lname, new_doctor_email)
                        new_user = Network.post_signup('Doctor',new_doctor_fname,new_doctor_lname, new_doctor_email,new_doctor_password)
                        st.success("Physician added successfully!")
                        # Display added user
                        st.write(new_user)# DH EL VIRABLE EL FIH HGT EL USER @OMAR
                        # Add user to session state
                        doctor = st.session_state.get('doctor', [])
                        doctor.append(new_user)
                        st.session_state.doctor = doctor
            elif validation_result == "INVALID_FORMAT":
                        st.warning("Password must contain at least one uppercase letter, one number, and one special character.")
            elif validation_result == "TOO_SHORT":
                        st.warning("Password must be at least 7 characters long.")
         st.write("Password:", new_doctor_password)   
    st.subheader('View Physicians')
    df = Network.get_users_table('Physician')
    if df:
        st.write(df)
    else:
        st.write("No Physicians added yet.")

