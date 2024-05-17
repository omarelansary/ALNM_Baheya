import streamlit as st
import pandas as pd
def add_user(username, email, password):
    # Here you would typically add the user to your database or perform some backend operation
    # For this example, let's just return the user details
    return {"Username": username, "Email": email, "password": password}

def app():
    st.title('Add Analyst')
# Function to add user to the system
    new_analyst_username = st.text_input("Username")
    new_analyst_email = st.text_input("Email")
    new_analyst_password = st.text_input("Password",type="password")
    add_button = st.button("Add Analyst")
    if add_button:
        missing_fields = []
        if not new_analyst_username:
                missing_fields.append("Username")
        if not new_analyst_email:
                missing_fields.append("Email")
        if not new_analyst_password:
                missing_fields.append("password") 
        if missing_fields:
                st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            new_user = add_user(new_analyst_username, new_analyst_email,new_analyst_password)
            st.success("User added successfully!")
            # Display added user
            st.write(new_user)# DH EL VIRABLE EL FIH HGT EL USER @OMAR
            # Add user to session state
            analysts = st.session_state.get('analysts', [])
            analysts.append(new_user)
            st.session_state.analysts = analysts
    st.subheader('View Analysts')
    analysts = st.session_state.get('analysts', [])
    if analysts:
        df = pd.DataFrame(analysts)
        st.write(df)
    else:
        st.write("No analysts added yet.")

