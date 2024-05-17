import streamlit as st
import datetime
from Authentication.Authenticator import Authenticator
from Components.cookieHandler import CookieHandler
class AuthComponents:
    
    def __init__(self): 
        self.cookie_handler = CookieHandler('user_auth_token')
        if 'initialized' not in st.session_state:
            st.session_state['initialized'] = False      
            # self.set_user_session_state(is_logged_in=True)
            self.set_user_session_state(is_logged_in=True, role="Admin")
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
 
       


    def login(self,role):
        if st.session_state['is_logged_in'] == False:
            #if self.cookie_handler.get_cookie()==None:
            if not self.check_cookie_session():
                # Initialize the authenticator
                authenticator = Authenticator()
                st.title(f"{role.capitalize()} Login")
                with st.form("login"):
                    st.subheader("Please enter your credentials")

                    # Form inputs
                    email = st.text_input("Email")
                    password = st.text_input("Enter a password", type="password")

                    # Submission button
                    submit_button = st.form_submit_button("Submit")

                    # Process form submission
                    if submit_button:
                        response = authenticator.login(role, email, password)
                        if 'token' in response:
                            st.success("Login successful!")
                            st.session_state['is_logged_in']=True
                            st.session_state['token'] = response.get('token')
                            st.session_state['role'] = role
                            st.write(st.session_state['token'])
                            st.write(st.session_state['role']) 
                            self.set_user_session_state(is_logged_in= True, token_expiry_date=datetime.datetime.now()+datetime.timedelta(seconds=30))
                            self.cookie_handler.set_cookie(st.session_state['token'], datetime.datetime.now() + datetime.timedelta(days=30))
                        else:
                            st.session_state['is_logged_in']=False
                            st.error("Login failed!")
                            st.write(response.get("details", "No additional information available."))      
        else:
            st.write(self.cookie_handler.get_cookie())                         

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
            st.write('I AM HERE')
            return 0

    def logout(self):
        self.set_user_session_state(is_logged_in=False)

                                              