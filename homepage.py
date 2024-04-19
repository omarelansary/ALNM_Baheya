import streamlit as st
import pandas as pd
from helper_functions import divide_by_two  # Importing the function from helper_functions.py

def main():
    st.title("Preschool Enrollment Form")

    # Form inputs
    with st.form("preschool_form"):
        st.subheader("Child Information")
        child_name = st.text_input("Child's Name")
        child_age = st.number_input("Child's Age", min_value=0, max_value=6, step=1)

        st.subheader("Parent/Guardian Information")
        parent_name = st.text_input("Parent/Guardian's Name")
        parent_email = st.text_input("Parent/Guardian's Email")
        parent_phone = st.text_input("Parent/Guardian's Phone Number")

        st.subheader("Additional Information")
        any_medical_conditions = st.checkbox("Does your child have any medical conditions?")
        if any_medical_conditions:
            medical_conditions = st.text_area("Please specify the medical conditions")

        agreed_to_terms = st.checkbox("I agree to the terms and conditions")

        # Submission button
        submit_button = st.form_submit_button("Submit")

        # Process form submission
        if submit_button:
            if agreed_to_terms:
                info = {
                    "Child's Name": child_name,
                    "Child's Age": child_age,
                    "Parent/Guardian's Name": parent_name,
                    "Parent/Guardian's Email": parent_email,
                    "Parent/Guardian's Phone Number": parent_phone,
                    "Medical Conditions": medical_conditions if any_medical_conditions else None,
                    "Agreed to Terms": agreed_to_terms
                }
                
                # Store data in a DataFrame
                df = pd.DataFrame([info])

                # Display user-submitted data
                st.subheader("You have submitted the following information:")
                st.write(df)
                st.subheader("Age devided by 2 is:")
                st.write(divide_by_two(child_age))
                
                
            else:
                st.warning("Please agree to the terms and conditions.")

if __name__ == "__main__":
    main()

