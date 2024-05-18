import streamlit as st
import pandas as pd
def add_user(username, email, password):
    # Here you would typically add the user to your database or perform some backend operation
    # For this example, let's just return the user details
    return {"Username": username, "Email": email, "password": password}

def app():
    st.title('Add Doctor')
# Function to add user to the system
    new_doctor_username = st.text_input("Username")
    new_doctor_email = st.text_input("Email")
    new_doctor_password = st.text_input("Password",type="password")
    add_button = st.button("Add doctor")
    if add_button:
        missing_fields = []
        if not new_doctor_username:
                missing_fields.append("Username")
        if not new_doctor_email:
                missing_fields.append("Email")
        if not new_doctor_password:
                missing_fields.append("password") 
        if missing_fields:
                st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            new_user = add_user(new_doctor_username, new_doctor_email,new_doctor_password)
            st.success("User added successfully!")
            # Display added user
            st.write(new_user)# DH EL VIRABLE EL FIH HGT EL USER @OMAR
            # Add user to session state
            doctors = st.session_state.get('doctors', [])
            doctors.append(new_user)
            st.session_state.doctors = doctors
    st.subheader('View Doctors')
    doctors = st.session_state.get('doctors', [])
    if doctors:
        df = pd.DataFrame(doctors)
        st.write(df)
    else:
        st.write("No doctors added yet.")

