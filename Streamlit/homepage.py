import streamlit as st
from Components.authComponents import AuthComponents
from Authentication.Authenticator import AuthExceptions
def main():
    # Display debugging information
    #   st.write('is_logged_in' in st.session_state)
    # Perform login if not logged in
    authComponents=AuthComponents()
    try:
        authComponents.login(role="Doctor")
    except AuthExceptions as e:
        st.error(e)

    if st.session_state['is_logged_in']==True:
        st.write('Welcome *Doctor*')
        st.title('Some content')
    else:
        st.write('Please login')  

    st.write(st.session_state['is_logged_in'])
    st.write(st.session_state['token'])
    # if st.session_state['page']== 'logged_out' :
    #     authComponents.login(role="Doctor")
    #     st.session_state['page'] == 'loged in'
    #     # Check again if login was successful to display welcome message
    # else:
    #     st.write(f"Welcome {st.session_state['role']}! You are logged in.")
    #     if st.button('Logout'):
    #         # Clear the login session state
    #         st.session_state['is_logged_in'] = False
    #         if 'token' in st.session_state:
    #             del st.session_state['token']  # Clean up session token
    #         if 'role' in st.session_state:
    #             del st.session_state['role']
    #         st.experimental_rerun()  # Force a rerun to refresh the state



if __name__ == "__main__":
    main()