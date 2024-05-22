import requests
import streamlit as st




class Networking():
    def __init__(self, api_url='http://127.0.0.1:8000/api'):
        self.api_url = api_url

    def post_make_assesment(self,doctor_id,mrn,data):

        patient_data = { "doctor_id": doctor_id,
                        "MRN": mrn,
                        "medical_info":data }
        response = requests.post('http://127.0.0.1:8000/api/doctors/makeAssessment', json=patient_data)
            
        if response.json()['success']:
            data = response.json()
            return response.json()
        else:
            return response.json()['message']
        
    def get_assesment_byDocId(self,doctor_id):
        payload = { "doctor_id": doctor_id}
        response = requests.get('http://127.0.0.1:8000/api/doctors/getAssessmentsByDocId', json=payload)
        if response.json()['success']:
            return response.json()
        else:
            return response.json()['message']
    
    def post_signup(self,role,fname,lname,email,password):
        """Send login request to API and return the response."""
        payload = {
            "firstName":fname,
            "lastName": lname,
            "email": email,
            "password": password
        }
        response = ''
        # Adjust the URLs as necessary
        if role == "Doctor":
            response = requests.post('http://127.0.0.1:8000/api/admins/signUp', json=payload)
        elif role == "Data Analyst":
            response = requests.post('http://127.0.0.1:8000/api/admins/signUpDataScientists', json=payload)
            
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise KeyError ##TODO: Change it ya Omar
    
    def get_users_table(self,role):
        response=None
        if role=="Physician":
            response = requests.get('http://127.0.0.1:8000/api/admins/getDoctors')
        if role=="Data Analyst":
            response = requests.get('http://127.0.0.1:8000/api/admins/getDataScientists')
        if response.json()['success']:     
            return response.json()
        else:
            return response.json()['message']
        
    def get_table(self,role):
        response=None
        if role=="Doctor":
            response = requests.get('http://127.0.0.1:8000/api/admins/getDoctors')
        if role=="Data Analyst":
            response = requests.get('http://127.0.0.1:8000/api/admins/getDataScientists')
        if response.json()['success']:    
            return response.json()
        else:
            return response.json()['message']
    
    #==========================NEW===========================@Mona
    def get_dashBoardData_forAnalysts(self):
        response = requests.get('http://127.0.0.1:8000/api/dataScientists/getDashboardData')
        if response.json()['success']:    
            return response.json()
        else:
            return response.json()['message']
    #==========================================================


