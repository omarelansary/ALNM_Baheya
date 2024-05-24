import jwt
from datetime import datetime, timedelta
import extra_streamlit_components as stx
import streamlit as st
from streamlit_cookies_controller import CookieController
import yaml
import os
import time
class CookieHandler:
    def __init__(self):
        self.cookie_name='userToken'
        self.config_path='..\\Streamlit\\Components\\config.yaml'
        self.token=None
        self.controller = CookieController('userToken')
        
    def load_yaml(self):
        """ Load a YAML file from the given path, returning an empty dictionary if the file doesn't exist or is empty. """
        if os.path.exists(self.config_path) and os.path.getsize(self.config_path) > 0:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file) or {}
        return {}
    
    def get_cookie(self):
        try:
            self.token=self.controller.get(self.cookie_name)
            return self.token
        except:
            st.error('Can not get token')
            
    def append_to_yaml(self,new_user):
        """ Append new data to an existing YAML file. """
        # Load the existing data
        data = self.load_yaml()
        # Update the data with new_data
        data.update(new_user)
        # Save the updated data back to the file
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(data, file, default_flow_style=False)
    
    def check_token_in_config(self, token):
        """ Check if a given token exists in the configuration file. """
        config = self.load_yaml()
        if token in config:

            return config[token]
        else:
            return False
        
    def set_cookie(self, token,username,role,id):
            # JavaScript code to set and read a cookie, correctly embedding the Python variable
        js_code_set_cookies = f"""
        <script>
        // Function to set a cookie
        function setCookie(name, value, days) {{
            var expires = "";
            if (days) {{
                var date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }}
            document.cookie = name + "=" + (value || "")  + expires + "; path=/";
        }}
        // Set a sample cookie
        setCookie('userToken', '{token}', 7);  // Set a cookie that expires in 7 days
        setTimeout(function() {{
            parent.window.location.reload();
        }}, 3);
        </script>
        """
        st.components.v1.html(js_code_set_cookies, height=0)
        new_user = {
            token:
                {'username': username ,
                 'role': role, 
                 'id':id
                }
        }
        self.append_to_yaml(new_user)
        #st.rerun()

    def del_cookies(self):
        #self.controller.remove('userToken')    
        js_code_delete_cookie = f"""
        <script>
        function deleteCookie(name) {{
            document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
        }}
        deleteCookie('userToken');
        setTimeout(function() {{
            parent.window.location.reload();
        }}, 1);
        </script>
        """
        st.components.v1.html(js_code_delete_cookie, height=0)    
