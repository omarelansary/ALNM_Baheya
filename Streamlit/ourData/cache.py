import redis
import pandas as pd
from pandas import json_normalize
#NEW
from Networking.Networking import Networking
assessments_json_data = {
    "success": True,
    "assessments": [
        {
            "id": 4,
            "MRN": 123,
            "status": 1,
            "status_message": "Filled",
            "prediction": 1,
            "ground_truth": 1,
            "creation_date": "2024-05-12",
            "medical_info": {
                "MRN": 123,
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
                "lymphovascular_invasion_result": "Positive"
            }
            
        },
        {
            "id": 8,
            "MRN": 122,
            "status": 1,
            "status_message": "Filled",
            "prediction": 1,
            "ground_truth": 0,
            "creation_date": "2024-05-11",
            "medical_info": {
                "MRN": 122,
                "dm_result": "NO",
                "er_result": "Negative",
                "patient_n": "N2",
                "patient_t": "T3",
                "pr_result": "Negative",
                "cvd_result": "Yes",
                "htn_result": "No",
                "vte_result": "No",
                "her2_result": "Negative",
                "patient_age": 50,
                "patient_ki67": 25.5,
                "patient_site": "Lower inner quadrant",
                "patient_grade": "III",
                "patient_size_cm": 160.5,
                "patient_first_bmi": 23.5,
                "patient_laterality": "Right",
                "patient_tumor_type": "Invasive lobular carcinoma",
                "patient_family_history": "No",
                "patient_menopausal_state": "Post-M",
                "patient_unilateral_bilateral": "Unilateral",
                "lymphovascular_invasion_result": "Negative"
            }
        },
        {
            "id": 5,
            "MRN": 142,
            "status": 1,
            "status_message": "Filled",
            "prediction": 0,
            "ground_truth": 1,
            "creation_date": "2024-05-11",
            "medical_info": {
                "MRN": 142,
                "dm_result": "Yes",
                "er_result": "Positive",
                "patient_n": "N3",
                "patient_t": "T1",
                "pr_result": "Positive",
                "cvd_result": "No",
                "htn_result": "Yes",
                "vte_result": "No",
                "her2_result": "Positive",
                "patient_age": 45,
                "patient_ki67": 20.5,
                "patient_site": "Central",
                "patient_grade": "I",
                "patient_size_cm": 170.5,
                "patient_first_bmi": 24.5,
                "patient_laterality": "Left",
                "patient_tumor_type": "Mucinous carcinoma",
                "patient_family_history": "Yes - BC",
                "patient_menopausal_state": "Pre-M",
                "patient_unilateral_bilateral": "Bilateral",
                "lymphovascular_invasion_result": "Positive"
            }
        }
    ]
}
Network=Networking()
class LocalCache:
    def __init__(self):
        # Initialize the Redis connection using default settings
        self.redisobj = redis.Redis(host='localhost', port=6379, db=0)

    '''Nerbotha b2a b networking :
    ya3ny lma user ye3mel sign up asagel l id l7ad l session ma tekhlas'''
    def save_id(self,id):
        self.redisobj.set("docId", id)

    def get_id(self):
        return self.redisobj.get("docId")

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

        #@Mona
        '''doc_id=self.get_id()
        patientsDataFrame=Network.get_assesment_byDocId(doc_id)
        return patientsDataFrame'''

        
    
    def get_assessment_byDocId_version2(self):
        # Normalize the JSON data and create a DataFrame
       # df = json_normalize(assesssments_json_data['assessments'][''])
        return self.dataframeTest()
    #=========================================ADMIN===============================================
    #=============================NEW=========================
    def get_doctors_for_admins(self):
        data_json=Network.get_table('Doctor')
        # Convert the dictionary to a DataFrame
        # Convert the dictionary to a DataFrame
        doctors_df = pd.DataFrame(data_json["doctors"])       
        return doctors_df
        
    #=========================================================
    #=============================NEW=========================@Mona
    def get_dataAnalysts_for_admins(self):
        data_json=Network.get_table('Data Analyst')
        # Convert the dictionary to a DataFrame
        # Convert the dictionary to a DataFrame
        doctors_df = pd.DataFrame(data_json["dataScientists"])
        
        return doctors_df
        
    #=========================================================
    def get_dashBoardData_forAnalysts(self):
        data_json=Network.get_dashBoardData_forAnalysts()
        doctors_df = pd.DataFrame(data_json["data"])
        return doctors_df

    #======================DATA ANALYSTS===================================
    #==========================NEW====================@Mona

    #======================================================
    def extract_and_exclude_assessment_info(self, assessment, exclude_keys):
        assessment_filtered = {key: value for key, value in assessment.items() if key not in exclude_keys}
        return assessment_filtered

    def dataframeTest(self):
        # Extract assessments and medical_info into separate lists
        assessments = []
        medical_infos = []
        exclude_keys = ["id", "status","MRN"]
        for assessment in assessments_json_data["assessments"]:
            medical_info = assessment["medical_info"]
            medical_infos.append(medical_info)
            assessment_filtered = self.extract_and_exclude_assessment_info(assessment, exclude_keys)
            assessments.append(assessment_filtered)
            print(assessment_filtered)


        # Convert to DataFrames
        df_assessments = pd.DataFrame(assessments)
        df_medical_info = pd.DataFrame(medical_infos)

        # Concatenate DataFrames side by side
        df_combined = pd.concat([df_medical_info, df_assessments], axis=1)
        return df_combined
        # Display DataFrame as HTML table
        # html_table = df_combined.to_html()
    
