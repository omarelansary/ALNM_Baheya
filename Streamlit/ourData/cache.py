import redis
import pandas as pd
from pandas import json_normalize

assesssments_json_data={
    "success": True,
    "assessments": [
        {
            "id": 4,
            "MRN": 123,
            "status": 1,
            "prediction": 1,
            "ground_truth": 1,
            "creation_date": "2024-05-12",
            "medical_info": {
                "MRN": 123,
                "dm_result": "Positive",
                "er_result": "Negative",
                "patient_n": "N1",
                "patient_t": "T2",
                "pr_result": "Positive",
                "cvd_result": "Negative",
                "htn_result": "Negative",
                "vte_result": "Positive",
                "her2_result": "Negative",
                "patient_age": 40,
                "patient_ki67": 30.5,
                "patient_site": "Upper outer quadrant",
                "patient_grade": "II",
                "patient_size_cm": 165.5,
                "patient_first_bmi": 22.5,
                "patient_laterality": "Left",
                "patient_tumor_type": "Invasive duct carcinoma (NST)",
                "patient_family_history": "Yes - BC",
                "patient_menopausal_state": "Pre-M",
                "patient_unilateral_bilateral": "Unilateral",
                "lymphovascular_invasion_result": "Positive"
            },
            "status_message": "Filled"
        },
        {
            "id": 8,
            "MRN": 122,
            "status": 1,
            "prediction": 1,
            "ground_truth": 0,
            "creation_date": "2024-05-11",
            "medical_info": {
                "MRN": 122,
                "dm_result": "Positive",
                "er_result": "Negative",
                "patient_n": "N1",
                "patient_t": "T2",
                "pr_result": "Positive",
                "cvd_result": "Negative",
                "htn_result": "Negative",
                "vte_result": "Positive",
                "her2_result": "Negative",
                "patient_age": 40,
                "patient_ki67": 30.5,
                "patient_site": "Upper outer quadrant",
                "patient_grade": "II",
                "patient_size_cm": 165.5,
                "patient_first_bmi": 21.5,
                "patient_laterality": "Left",
                "patient_tumor_type": "Invasive duct carcinoma (NST)",
                "patient_family_history": "Yes - BC",
                "patient_menopausal_state": "Pre-M",
                "patient_unilateral_bilateral": "Unilateral",
                "lymphovascular_invasion_result": "Positive"
            },
            "status_message": "Filled"
        },
        {
            "id": 5,
            "MRN": 142,
            "status": 1,
            "prediction": 1,
            "ground_truth": 1,
            "creation_date": "2024-05-11",
            "medical_info": {
                "MRN": 142,
                "dm_result": "Yes",
                "er_result": "Negative",
                "patient_n": "N1",
                "patient_t": "T2",
                "pr_result": "Positive",
                "cvd_result": "No",
                "htn_result": "No",
                "vte_result": "Yes",
                "her2_result": "Negative",
                "patient_age": 40,
                "patient_ki67": 30.5,
                "patient_site": "Upper outer quadrant",
                "patient_grade": "II",
                "patient_size_cm": 165.5,
                "patient_first_bmi": 22.5,
                "patient_laterality": "Left",
                "patient_tumor_type": "Invasive duct carcinoma (NST)",
                "patient_family_history": "Yes - BC",
                "patient_menopausal_state": "Pre-M",
                "patient_unilateral_bilateral": "Unilateral",
                "lymphovascular_invasion_result": "Yes"
            },
            "status_message": "Filled"
        }
    ]
}

class LocalCache:
    def __init__(self):
        # Initialize the Redis connection using default settings
        self.redisobj = redis.Redis(host='localhost', port=6379, db=0)

    def save_assesment_byDocId(self, dataFrame):
        # Save assessment data to Redis
        self.redisobj.set("assessment_data", dataFrame)

    # def get_assessment_byDocId(self,dataFrame):
    #     # Retrieve assessment data from Redis
    #     return self.redisobj.get("assessment_data")
    
    def get_assessment_byDocId(self):
        # Retrieve assessment data from Redis
        # print(self.redisobj.get("assessment_data"))
        return self.redisobj.get("assessment_data")
    
    def get_assessment_byDocId_version2(self):
        # Normalize the JSON data and create a DataFrame
        df = json_normalize(assesssments_json_data['assessments'])
        return df
    
