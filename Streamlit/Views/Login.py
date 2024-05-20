import streamlit as st
from Components.authComponents import AuthComponents
from Authentication.Authenticator import AuthExceptions
from PIL import Image

def app(authComponents):
    col1, col2= st.columns(2)
    with col1:

        # image = Image.open('sunrise.jpg')
        image_url_0 = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/logo.jpg"

        st.image(image_url_0)   
    # Title for your radio button section
    with col2:
        # st.title('Select Your Role')
        # role = st.radio("Select Your Role", options=["Doctor", "Data Analyst","Admin"],index=None,horizontal=True)
        # Radio button widget
        role = st.radio(
            "Select your role:",
            ('Physician', 'Data Analyst', 'Admin'),horizontal=True
        )

        try:
            authComponents.login(role=role)
        except AuthExceptions as e:
            st.error(e)

        if st.session_state['is_logged_in']:
            st.write(f'Welcome *{st.session_state["role"]}*')
            st.title('Some content')
        else:
            st.write(' ')

