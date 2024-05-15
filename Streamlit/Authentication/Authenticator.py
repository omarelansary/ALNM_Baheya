import requests
import streamlit as st

class AuthExceptions(Exception):
    """
    Exceptions raised for the Login widget.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str, response=None,):
        self.message = message
        self.response=response
        super().__init__(self.message)


class Authenticator:
    def __init__(self, api_url='http://127.0.0.1:8000/api'):
        self.api_url = api_url
    
    def login(self, role, email, password):
        """Send login request to API and return the response."""
        payload = {
            "email": email,
            "password": password
        }
        response = ''
        # Adjust the URLs as necessary
        if role == "Doctor":
            response = requests.post('http://127.0.0.1:8000/api/doctors/login', json=payload)
        elif role == "Data Scientist":
            response = requests.post('http://127.0.0.1:8000/api/doctors/login', json=payload)  # TODO: Update this URL?
        elif role == "Admin":
            response = requests.post('http://127.0.0.1:8000/api/admins/login', json=payload)
            
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise AuthExceptions(f"Failed to login in for {role} authenticate", response=response.status_code)