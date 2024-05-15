import streamlit as st
from Components.authComponents import AuthComponents
from Authentication.Authenticator import AuthExceptions

def app(authComponents):
    # Title for your radio button section
    st.title('Select Your Role')

    # Radio button widget
    role = st.radio(
        "Choose your role:",
        ('Doctor', 'Data Analyst', 'Admin')
    )


    try:
        authComponents.login(role=role)
    except AuthExceptions as e:
        st.error(e)

    if st.session_state['is_logged_in']==True:
        st.write('Welcome *Doctor*')
        st.title('Some content')
    else:
        st.write('Please login')  