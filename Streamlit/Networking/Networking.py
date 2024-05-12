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
            