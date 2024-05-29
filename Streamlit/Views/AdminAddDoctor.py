import streamlit as st
import pandas as pd
from Networking.Networking import Networking
import Components.vaildation
from ourData.cache import LocalCache
from streamlit_modal import Modal

def app():
    st.title('Add Physician')
    # Function to add user to the system
    Cache = LocalCache()

    new_physician_fname = st.text_input("First Name")
    new_physician_lname = st.text_input("Last Name")
    new_physician_email = st.text_input("Email")
    new_physician_password = st.text_input("Password", type="password")
    add_button = st.button("Add Physician")

    if add_button:
        missing_fields = []
        if not new_physician_fname:
            missing_fields.append("First Name")
        if not new_physician_lname:
            missing_fields.append("Last Name")
        if not new_physician_email:
            missing_fields.append("Email")
        if not new_physician_password:
            missing_fields.append("Password") 
        if missing_fields:
            st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            if not Components.vaildation.validate_username(new_physician_fname):
                st.warning("Invalid first name.")
            elif not Components.vaildation.validate_username(new_physician_lname):
                st.warning("Invalid last name.")    
            elif not Components.vaildation.validate_email(new_physician_email):
                st.warning("Invalid email format.")
            else:
                validation_result = Components.vaildation.validate_password(new_physician_password)
                st.write("Validation result:", validation_result)  # Print validation result
                if validation_result == "VALID":
                    Components.vaildation.signup("Physician",new_physician_fname, new_physician_lname, new_physician_email,new_physician_password)
                    new_user = ('Physician', new_physician_fname, new_physician_lname, new_physician_email, new_physician_password)
                    # Add user to session state
                    physicians = st.session_state.get('physicians', [])
                    physicians.append(new_user)
                    st.session_state.physicians = physicians
                elif validation_result == "INVALID_FORMAT":
                    st.warning("Password must contain at least one uppercase letter, one number, and one special character.")
                elif validation_result == "TOO_SHORT":
                    st.warning("Password must be at least 7 characters long.")
                st.write("Password:", new_physician_password)   

    st.subheader('View Physicians')
    physicians = Cache.get_doctors_for_admins()

    if not physicians.empty:
        df = physicians
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
                                <h1 style="color: green; font-size: 28px; font-family: 'Open Sans', sans-serif;">Are you sure you want to delete the selected Physicians?</h1>
                                </div>
                                """,
                                unsafe_allow_html=True
                        )
                        if st.button("Confirm"):
                                # Remove the selected physicians
                                for index in sorted(selected_indices, reverse=True):
                                 physicians.pop(index)
                                st.session_state.physicians = physicians
                                st.rerun()  # Refresh the app to reflect changes

    else:
        st.write("No Physicians added yet.")

