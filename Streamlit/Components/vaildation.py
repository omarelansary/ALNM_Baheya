import streamlit as st
import re
def signup(fname,lname, email):
    username = f"{fname} {lname}"
    # Here you can implement your signup logic, like saving the user to a database
    st.success(f"Signup successful! Username: {username}, Email: {email}")
    # Email validation function
def validate_email(email):
        # Regular expression to check if email is in valid format
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return True
        else:
            return False

    # Password validation function
def validate_password(password):
        # Regular expression to check if password contains at least one uppercase letter, one number, and one special character
        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|<>?])[A-Za-z\d!@#$%^&*()_+{}|<>?]{3,}$", password):
            return "INVALID_FORMAT"  # Return error code for invalid format

        if len(password) < 7:
            return "TOO_SHORT"  # Return error code for password too short

        return "VALID"  # Password is valid
def validate_username(username):
  # Regular expression to check if username contains only alphabetic characters
    if re.match(r"^[a-zA-Z]+$", username):
        return True
    else:
        return False
