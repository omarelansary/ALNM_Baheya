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
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data
            else:
                st.error(data['message'])
                #raise Exception(data.get('message'))
        else:
            raise Exception(f"HTTP Error: {response.json()['message']}")
        
    def post_delete_assesment(self,selectedMRN):
        patient_data = {"MRN": selectedMRN}
        response = requests.post('http://127.0.0.1:8000/api/doctors/deleteAssessment', json=patient_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data
            else:
                st.error(data.get('message'))
                #raise Exception(data.get('message'))
        else:
            raise Exception(f"HTTP Error: {response.status_code}")  
        
    def post_setGroundTruth(self, doctor_id, selected_MRN, ground_truth):
        payload = {
        "doctor_id": int(doctor_id),
        "MRN": int(selected_MRN),    
        "ground_truth": int(ground_truth)
        }
        response = requests.post('http://127.0.0.1:8000/api/doctors/setGroundTruth' , json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data
            else:
                st.error(data.get('message'))
        else:
            raise Exception(f"HTTP Error: {response.status_code}")  

    def post_updateAssessmentToReviewed(self, selected_MRN):
        payload = {
        "MRN": selected_MRN,    
        }
        response = requests.post('http://127.0.0.1:8000/api/dataScientists/updateAssessmentToReviewed' , json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data
            else:
                st.error(data.get('message'))
        else:
            raise Exception(f"HTTP Error: {response.status_code}")   
          
    def get_assessment_byDocId(self, doctor_id):
        payload = {"doctor_id": doctor_id}
        response = requests.get('http://127.0.0.1:8000/api/doctors/getAssessmentsByDocId', json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['assessments']
            else:
                st.error(data.get('message'))
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    def get_allAssessment_byStatus(self, status):
        payload = {"status": int(status)}
        response = requests.post('http://127.0.0.1:8000/api/dataScientists/getAllAssessmentsByStatus', json=payload)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['assessments']
            else:
                st.error(data.get('message'))
        else:
            raise Exception(f"HTTP Error: {response.json()}")    
    
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
        if role == "Physician":
            response = requests.post('http://127.0.0.1:8000/api/admins/signUp', json=payload)
        elif role == "Data Analyst":
            response = requests.post('http://127.0.0.1:8000/api/admins/signUpDataScientists', json=payload)
        elif role == "Head Doctor":
            response = requests.post('http://127.0.0.1:8000/api/admins/signUpHeadDoctor', json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data
            else:
                raise Exception(data.get('message', 'Signup failed'))
        else:
            response.raise_for_status()  # Raise an HTTPError for bad responses
    
    def get_users_table(self,role):
        response=None
        if role=="Physician":
            response = requests.get('http://127.0.0.1:8000/api/admins/getDoctors')
        if role=="Data Analyst":
            response = requests.get('http://127.0.0.1:8000/api/admins/getDataScientists')
        if role == "Head Doctor":
            response = requests.get('http://127.0.0.1:8000/api/headDoctors/getHeadDoctors')         
        if response.status_code == 200:
            if response.json()['success']:     
                return response.json()
            else:
                raise Exception(response.json()['message'])
        else:
            raise Exception('Response status is: ' + str(response.status_code))    
        
    
    #==========================NEW===========================@Mona
    def get_dashBoardData_forAnalysts(self):
        response = requests.get('http://127.0.0.1:8000/api/dataScientists/getDashboardData')
        if response.json()['success']:    
            return response.json()
        else:
            return response.json()['message']
    #==========================================================


