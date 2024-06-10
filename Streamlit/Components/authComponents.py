import streamlit as st
import datetime
from Authentication.Authenticator import Authenticator
from Components.cookieHandler import CookieHandler
from streamlit_cookies_controller import CookieController
import time

class AuthComponents:
    
    def __init__(self): 
        self.cookie_handler = CookieHandler()
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
    '''
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

                        # CAPTCHA
                        captcha_key, captcha_image_url = authenticator.refresh_captcha()  # Assuming you have a method to refresh CAPTCHA
                        
                        # Get the URL of the CAPTCHA image
                        # Base URL
                        print("captcha URL:\n",captcha_image_url)
                        st.image(base_url + captcha_image_url, use_column_width=False, width=200)
                        captcha_response = st.text_input("Enter CAPTCHA")
                        # Create columns to center the submit button
                        col1, col2, col3 = st.columns([2, 4, 2])
                        with col2:
                            submit_button = st.form_submit_button("Login", use_container_width=True)

                        # Process form submission
                        if submit_button:
                            response = authenticator.login(role, email, password, captcha_key, captcha_response)
                            if 'token' in response:
                                st.success("Login successful!")
                                token=response.get('token')
                                username=response.get('firstName') + ' ' + response.get('lastName')
                                self.set_user_session_state(is_logged_in=True,role=st.session_state['role'], token=st.session_state['token'])
                                self.cookie_handler.set_cookie(token,username=username,role=role,id=response.get('id'))
                            else:
                                st.session_state['is_logged_in'] = False
                                st.error("Login failed! Please check your email, password, and CAPTCHA.")
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
                                response = authenticator.reset_password(role, email, new_password)
                                if response['success']:
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

    '''
    
    def login(self, role):
        if not st.session_state.get('is_logged_in'):
            if not self.check_cookie_session():
                # Initialize the authenticator
                authenticator = Authenticator()

                st.title(f"{role.capitalize()} Portal")

                if 'form_mode' not in st.session_state:
                    st.session_state['form_mode'] = 'Login'

                # Refresh CAPTCHA only if it's not already in session state
                if 'captcha_key' not in st.session_state or 'captcha_image_url' not in st.session_state:
                    st.session_state['captcha_key'], st.session_state['captcha_image_url'] = authenticator.refresh_captcha()

                form_mode = st.session_state['form_mode']

                if form_mode == "Login":
                    with st.form("login_form"):
                        st.subheader("Login to your account")

                        # Form inputs
                        email = st.text_input("Email")
                        password = st.text_input("Password", type="password")
                       
                        # CAPTCHA
                        captcha_image_url = st.session_state['captcha_image_url']
                        print("captcha URL:\n", captcha_image_url)
                        st.image("http://127.0.0.1:8000" + captcha_image_url, use_column_width=False, width=200)
                        captcha_response = st.text_input("Enter the Letters You See Above:")


                        # Create columns to center the submit button
                        col1, col2, col3 = st.columns([2, 4, 2])
                        with col2:
                            submit_button = st.form_submit_button("Login", use_container_width=True)
                        
                        print("captcha_key:\n",st.session_state['captcha_key'])
                        print("captcha_response:\n",captcha_response)
                        

                        # Process form submission
                        if submit_button:
                            response = authenticator.login(role, email, password, st.session_state['captcha_key'], captcha_response)
                            time.sleep(10)  # Sleep for 10 seconds
                            if 'token' in response:
                                st.success("Login successful!")
                                token=response.get('token')
                                username=response.get('firstName') + ' ' + response.get('lastName')
                                self.set_user_session_state(is_logged_in=True,role=st.session_state['role'], token=st.session_state['token'])
                                self.cookie_handler.set_cookie(token,username=username,role=role,id=response.get('id'))
                            else:
                                st.session_state['is_logged_in'] = False
                                st.error("Login failed! Please check your email and password.")
                                st.write(response.get("details", "No additional information available."))
                                # Refresh CAPTCHA on failed login
                                st.session_state['captcha_key'], st.session_state['captcha_image_url'] = authenticator.refresh_captcha()
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
                                response = authenticator.reset_password(role, email, new_password)
                                if response['success']:
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
        if (self.cookie_handler.get_cookie()):
            return self.cookie_handler.check_token_in_config(self.cookie_handler.get_cookie())
        else:
            return 0
    def logout(self):
        self.cookie_handler.del_cookies()
        self.set_user_session_state(is_logged_in=False)

                                              