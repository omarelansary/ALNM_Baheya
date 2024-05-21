# import streamlit as st
# import pandas as pd
# from Networking.Networking import Networking
# import Components.vaildation

# def app():
#     st.title('Add Analyst')
#     # Function to add user to the system
#     Network = Networking()
#     new_analyst_fname = st.text_input("First Name")
#     new_analyst_lname = st.text_input("Last Name")
#     new_analyst_email = st.text_input("Email")
#     new_analyst_password = st.text_input("Password",type="password")
#     add_button = st.button("Add Analyst")
#     if add_button:
#         missing_fields = []
#         if not new_analyst_fname:
#                 missing_fields.append("First Name")
#         if not new_analyst_lname:
#                 missing_fields.append("Last Name")
#         if not new_analyst_email:
#                 missing_fields.append("Email")
#         if not new_analyst_password:
#                 missing_fields.append("password") 
#         if missing_fields:
#                 st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
#         else:
#             new_user = Network.post_signup('Data Analyst',new_analyst_fname,new_analyst_lname, new_analyst_email,new_analyst_password)
#             st.success("DataAnalyst added successfully!")
#             st.write("New Analyst Information:")
#             st.write(f"First Name: {new_user.get('first_name', 'N/A')}")
#             st.write(f"Last Name: {new_user.get('last_name', 'N/A')}")
#             st.write(f"Email: {new_user.get('email', 'N/A')}")
#             st.write(f"Role: {new_user.get('role', 'N/A')}")
            
#             # Display added user
#             st.write(new_user)# DH EL VIRABLE EL FIH HGT EL USER @OMAR
#             # Add user to session state
#             analysts = st.session_state.get('analysts', [])
#             analysts.append(new_user)
#             st.session_state.analysts = analysts
#     st.subheader('View Analysts')
#     #analysts = st.session_state.get('analysts', [])
#     df = Network.get_table('Data Analyst')
#     if df:
#         st.write(df)
#     else:
#         st.write("No Analysts added yet.")
import streamlit as st
import re
from Networking.Networking import Networking
import Components.vaildation


def app():
    st.title('Add Analyst')
    # Function to add user to the system
    Network = Networking()
    new_analyst_fname = st.text_input("First Name")
    new_analyst_lname = st.text_input("Last Name")
    new_analyst_email = st.text_input("Email")
    new_analyst_password = st.text_input("Password", type="password")
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
            if not Components.vaildation.validate_username(new_analyst_fname):
                st.warning("aloo.")
            elif not Components.vaildation.validate_username(new_analyst_lname):
                st.warning("aloo.")    
            elif not Components.vaildation.validate_email(new_analyst_email):
                st.warning("Invalid email format.")
            else:
                validation_result = Components.vaildation.validate_password(new_analyst_password)
                st.write("Validation result:", validation_result)  # Print validation result
                if validation_result == "VALID":
                    Components.vaildation.signup(new_analyst_fname, new_analyst_lname, new_analyst_email)
                    new_user = Network.post_signup('Data Analyst', new_analyst_fname, new_analyst_lname, new_analyst_email, new_analyst_password)
                    st.success("DataAnalyst added successfully!")
                    # Display added user
                    st.write(new_user)  # DH EL VIRABLE EL FIH HGT EL USER @OMAR
                    # Add user to session state
                    analysts = st.session_state.get('analysts', [])
                    analysts.append(new_user)
                    st.session_state.analysts = analysts
                elif validation_result == "INVALID_FORMAT":
                    st.warning("Password must contain at least one uppercase letter, one number, and one special character.")
                elif validation_result == "TOO_SHORT":
                    st.warning("Password must be at least 7 characters long.")
                st.write("Password:", new_analyst_password)

    st.subheader('View Analysts')
    # analysts = st.session_state.get('analysts', [])
    df = Network.get_users_table('Data Analyst')
    if df:
        st.write(df)
    else:
        st.write("No Analysts added yet.")
