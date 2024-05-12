import jwt
from datetime import datetime, timedelta
import extra_streamlit_components as stx
import streamlit as st
import secrets
class CookieHandler:
    def __init__(self, cookie_name):
        self.cookie_name = cookie_name
        self.cookie_key = secrets.token_urlsafe(32)  
        self.cookie_manager = stx.CookieManager()

    def get_cookie(self):
        token = self.cookie_manager.get(self.cookie_name)
        if token:
            try:
                # This assumes the JWT 'exp' claim is properly set and will automatically check for expiration.
                return jwt.decode(token, self.cookie_key, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                # If the token is expired, delete the cookie.
                self.delete_cookie()
            except jwt.DecodeError:
                # If the token is malformed, delete the cookie.
                self.delete_cookie()
        return token  # Return None if there's no token or if any exception occurs.

    def set_cookie(self, token, expiry):
        encoded_token = jwt.encode({'token': token, 'exp': expiry}, self.cookie_key, algorithm="HS256")
        self.cookie_manager.set(self.cookie_name, encoded_token, path='http://localhost:8501', expires_at=expiry)


    def delete_cookie(self):
        self.cookie_manager.delete(self.cookie_name)
