import streamlit as st
import pandas as pd
from Networking.Networking import Networking
import Components.vaildation
from ourData.cache import LocalCache
from streamlit_modal import Modal

def app():
    st.title('Add Head Doctor')
    # Function to add user to the system
    Cache = LocalCache()

    new_headDoctor_fname = st.text_input("First Name")
    new_headDoctor_lname = st.text_input("Last Name")
    new_headDoctor_email = st.text_input("Email")
    new_headDoctor_password = st.text_input("Password", type="password")
    add_button = st.button("Add Head Doctor")

    if add_button:
        missing_fields = []
        if not new_headDoctor_fname:
            missing_fields.append("First Name")
        if not new_headDoctor_lname:
            missing_fields.append("Last Name")
        if not new_headDoctor_email:
            missing_fields.append("Email")
        if not new_headDoctor_password:
            missing_fields.append("Password") 
        if missing_fields:
            st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            if not Components.vaildation.validate_username(new_headDoctor_fname):
                st.warning("Invalid first name.")
            elif not Components.vaildation.validate_username(new_headDoctor_lname):
                st.warning("Invalid last name.")    
            elif not Components.vaildation.validate_email(new_headDoctor_email):
                st.warning("Invalid email format.")
            else:
                validation_result = Components.vaildation.validate_password(new_headDoctor_password)
                st.write("Validation result:", validation_result)  # Print validation result
                if validation_result == "VALID":
                    Components.vaildation.signup("Head Doctor",new_headDoctor_fname, new_headDoctor_lname, new_headDoctor_email,new_headDoctor_password)
                    new_user = ('Head Doctor', new_headDoctor_fname, new_headDoctor_lname, new_headDoctor_email, new_headDoctor_password)
                    # Add user to session state
                    headDoctors = st.session_state.get('headDoctors', [])
                    headDoctors.append(new_user)
                    st.session_state.headDoctors = headDoctors
                elif validation_result == "INVALID_FORMAT":
                    st.warning("Password must contain at least one uppercase letter, one number, and one special character.")
                elif validation_result == "TOO_SHORT":
                    st.warning("Password must be at least 7 characters long.")
                st.write("Password:", new_headDoctor_password)   

    st.subheader('View Head Doctors')
    headDoctors = Cache.get_headDoctors_for_admins()
    if not headDoctors.empty:
        df = headDoctors
        selected_indices = []

        col1, col2, col3, col4, col5 = st.columns([0.1, 0.2, 0.25, 0.25, 0.2])
        with col1:
            st.write("")
        with col2:
            st.write("ID")
        with col3:
            st.write("First Name")
        with col4:
            st.write("Last Name")
        with col5:
            st.write("Email")


        # Display the table with checkboxes
        for i, row in df.iterrows():
            col1, col2, col3, col4, col5= st.columns([0.1, 0.2, 0.25, 0.25, 0.2])
            with col1:
                if st.checkbox("", key=f"select_{i}"):
                    selected_indices.append(i)
            with col2:
                st.write(row['id'])
            with col3:
                st.write(row['firstName'])
            with col4:
                st.write(row['lastName'])
            with col5:
                st.write(row['email'])

        modal = Modal("Confirm Deletion", key="confirm_deletion")

        if selected_indices:
           open_modal = st.button("Delete Selected Data Scientists")
           if open_modal:
        # Open the modal when the delete button is clicked
        # modal = Modal("Confirm Deletion", key="confirm_deletion")
                 modal.open()
           if modal.is_open():
                    with modal.container():
                        st.markdown(
                                """
                                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                                <h1 style="color: green; font-size: 28px; font-family: 'Open Sans', sans-serif;">Are you sure you want to delete the selected headDoctors?</h1>
                                </div>
                                """,
                                unsafe_allow_html=True
                        )
                        if st.button("Confirm"):
                                # Remove the selected headDoctors
                                for index in sorted(selected_indices, reverse=True):
                                 headDoctors.pop(index)
                                st.session_state.headDoctors = headDoctors
                                st.rerun()  # Refresh the app to reflect changes

    else:
        st.write("No Head Doctors added yet.")

