import streamlit as st
import datetime
from Authentication.Authenticator import Authenticator
from Components.cookieHandler import CookieHandler
class AuthComponents:
    
    def __init__(self): 
        self.cookie_handler = CookieHandler('user_auth_token')
        if 'initialized' not in st.session_state:
            st.session_state['initialized'] = False      
            self.set_user_session_state(is_logged_in=False)
            
    def set_user_session_state(self, is_logged_in=None, role=None, fname=None, lname=None, token=None, token_expiry_date=None):
        # Initialize only once per session if not already done
        if st.session_state['initialized']== False:
            # Set all values, initializing them to None if not provided
            st.session_state['is_logged_in'] = is_logged_in
            st.session_state['role'] = role
            st.session_state['fname'] = fname
            st.session_state['lname'] = lname
            st.session_state['token'] = token
            st.session_state['token_expiry_date'] = token_expiry_date
            st.session_state['initialized']= True
        else:
            # Update only if values are provided
            if is_logged_in is not None:
                st.session_state['is_logged_in'] = is_logged_in
                st.rerun()
            if role is not None:
                st.session_state['role'] = role
            if fname is not None:
                st.session_state['fname'] = fname
            if lname is not None:
                st.session_state['lname'] = lname
            if token is not None:
                st.session_state['token'] = token
            if token_expiry_date is not None:
                st.session_state['token_expiry_date'] = token_expiry_date
 



    def login(self, role):
        if not st.session_state.get('is_logged_in'):
            if not self.check_cookie_session():
                # Initialize the authenticator
                authenticator = Authenticator()

                st.title(f"{role.capitalize()} Portal")

                if 'form_mode' not in st.session_state:
                    st.session_state['form_mode'] = 'Login'

                form_mode = st.session_state['form_mode']

                if form_mode == "Login":
                    with st.form("login_form"):
                        st.subheader("Login to your account")

                        # Form inputs
                        email = st.text_input("Email")
                        password = st.text_input("Password", type="password")

                        # Create columns to center the submit button
                        col1, col2, col3 = st.columns([2, 4, 2])
                        with col2:
                            submit_button = st.form_submit_button("Login", use_container_width=True)

                        # Process form submission
                        if submit_button:
                            response = authenticator.login(role, email, password)
                            if 'token' in response:
                                st.success("Login successful!")
                                st.session_state['is_logged_in'] = True
                                st.session_state['token'] = response.get('token')
                                st.session_state['role'] = role
                                self.set_user_session_state(is_logged_in=True, token_expiry_date=datetime.datetime.now() + datetime.timedelta(seconds=30))
                                self.cookie_handler().set_cookie(st.session_state['token'], datetime.datetime.now() + datetime.timedelta(days=30))
                            else:
                                st.session_state['is_logged_in'] = False
                                st.error("Login failed! Please check your email and password.")
                                st.write(response.get("details", "No additional information available."))

                    # Buttons to switch form mode
                    if st.button('Forgot Password'):
                        st.session_state['form_mode'] = 'Forgot Password'

                elif form_mode == "Forgot Password":
                    with st.form("forgot_password_form"):
                        st.subheader("Reset your password")

                        # Form inputs
                        email = st.text_input("Email")
                        new_password = st.text_input("New Password", type="password")
                        confirm_password = st.text_input("Confirm Password", type="password")

                        # Create columns to center the submit button
                        col1, col2, col3 = st.columns([2,4, 2])
                        with col2:
                            submit_button = st.form_submit_button("Reset Password", use_container_width=True)

                        # Process form submission
                        if submit_button:
                            if new_password != confirm_password:
                                st.error("Passwords do not match! Please try again.")
                            else:
                                response = authenticator.reset_password(email, new_password)
                                if response.get('status') == 'success':
                                    st.success("Password reset successful! You can now log in with your new password.")
                                else:
                                    st.error("Password reset failed! Please try again.")
                                    st.write(response.get("details", "No additional information available."))

                    # Buttons to switch form mode
                    if st.button('Login'):
                        st.session_state['form_mode'] = 'Login'
        else:
            st.write("You are already logged in.")
            st.write(f"Role: {st.session_state['role']}")
            st.write(f"Token: {st.session_state['token']}")
    # Dummy methods for the example
   

    def check_cookie_session(self):
        # Check if token and expiry date exist and are valid
        if ('token' in st.session_state and st.session_state['token'] != None)  and ('token_expiry_date' in st.session_state and st.session_state['token_expiry_date'] != None):
            st.write('Time')
            st.write(datetime.datetime.now() < st.session_state['token_expiry_date'])
            if datetime.datetime.now() < st.session_state['token_expiry_date']:
                # Token is valid and not expired
                st.session_state['is_logged_in'] = False
                return 1
            else:
                # Token is expired
                st.session_state['token'] = None
                st.session_state['token_expiry_date'] = None
                st.session_state['is_logged_in'] = True
                return 0
        else:
            # Token or expiry date does not exist
            st.write('')
            return 0

    def logout(self):
        self.set_user_session_state(is_logged_in=False)

                                              