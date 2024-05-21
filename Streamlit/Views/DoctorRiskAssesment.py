import streamlit as st
from Networking.Networking import Networking
import pandas as pd
from ourData.cache import LocalCache
from streamlit_modal import Modal

# st.set_page_config(
#         page_title="Risk Assessment",
#         layout="wide" # Set layout to wide mode
#         # Collapse the sidebar initially
#     )


def app():
        Network=Networking()
        cacheInMemory=LocalCache()

        st.title("Risk Assessment :clipboard:")
        with st.form("Risk Assessment"):
            col_Numerical, col_Categorical1, col_YesorNo = st.columns(3)

            # DM selection
            with col_Numerical:
            # Numerical inputs
                st.subheader("Numerical Inputs :abacus:")
                patient_MRN = st.number_input("Patient MRN", value=0, min_value=0, format="%d")
                patient_first_bmi = st.number_input("First BMI", value=None, min_value=0.0,max_value=100.0, format="%.2f")
                patient_age = st.number_input("Age", value=None, min_value=0, max_value=150, format="%d")
                patient_size_cm = st.number_input("size cm", value=None, min_value=0.0,max_value=20.0,format="%.2f")
                patient_ki67 = st.number_input("KI67", value=None, min_value=0, max_value=100, format="%d")
            with col_Categorical1:
            # Categorical inputs
                st.subheader("Categorical Inputs:page_facing_up: ")
                col_11, col_22 = st.columns(2)
                with col_11:
                    patient_family_history = st.selectbox("Family History", options=["Yes - BC","Yes - both","Yes - other cancers", "No","Unrecorded"],index=None, placeholder="Select family history...")
                    patient_other=st.text_input("Other")
                    patient_unilateral_bilateral = st.selectbox("Unilateral Bilateral", options=["Unilateral", "Bilateral","Unrecorded"],index=None, placeholder="Select unilateral or bilateral...")
                    patient_laterality = st.selectbox("Laterality", options=["Left", "Right", "Bilateral","Unrecorded"],index=None, placeholder="Select laterality...")
                    patient_menopausal_state = st.selectbox("Menopausal State", options=["Post-M", "Pre-M", "Unrecorded"],index=None, placeholder="Select menopausal state...")
                with col_22:

                    # st.subheader("Categorical Inputs Part 2 ")
                    patient_n = st.selectbox("N", options=["N0", "N1","N2","N3", "Nx","Urecorded"],index=None, placeholder="Select N...")
                    patient_t = st.selectbox("T", options=["T1", "T2", "T3","T4","Tis","To","Urecorded"], index=None,placeholder="Select T...")
                    patient_grade = st.selectbox("Grade", options=["I", "II","III"],index=None, placeholder="Select grade...") 
                    patient_tumor_type=st.text_input("Tumor Type")
                    patient_site=st.text_input("Site")

                    # patient_tumor_type = st.selectbox("Tumor Type", options=["Invasive duct carcinoma (NST)","Invasive Lobular carcinoma NOS ","Ductal carcinoma in situ, DCIS", "Invasive tubular/cribriform carcinoma","Mixed Tumor", "Other"], index=None,placeholder="Select tumor type...")
                    # patient_site = st.selectbox("Site", options=["Upper outer quadrant","Upper inner quadrant","Lower outer quadrant", "Lower inner quadrant","Para areolar", "Other"],index=None, placeholder="Select site...")
    
            with col_YesorNo:
                st.subheader("Yes :heavy_check_mark: or No :heavy_multiplication_x: Inputs")
                vte_choice = st.radio("VTE", options=["Yes", "No"],index=None,horizontal=True)
                vte_result = vte_choice.split()[0] if vte_choice else "Not selected"
                Hormonal_Contraception_choice = st.radio("Hormonal Contraception", options=["Yes", "No"],index=None, horizontal=True)
                Hormonal_Contraception_result = Hormonal_Contraception_choice.split()[0] if Hormonal_Contraception_choice else "Not selected"
                # dm_choice = st.radio("DM", options=["Yes", "No"],index=None, horizontal=True)
                # dm_result = dm_choice.split()[0] if dm_choice else "Not selected"
                # htn_choice = st.radio("HTN", options=["Yes", "No"],index=None,horizontal=True)   
                # htn_result = htn_choice.split()[0] if htn_choice else "Not selected"

                # cvd_choice = st.radio("CVD", options=["Yes", "No"],index=None,horizontal=True)    
                # cvd_result = cvd_choice.split()[0] if cvd_choice else "Not selected"
                lymphovascular_invasion_choice = st.radio("Lymphovascular Invasion", options=["Yes", "No"],index=None,horizontal=True)
                lymphovascular_invasion_result = lymphovascular_invasion_choice.split()[0] if lymphovascular_invasion_choice else "Not selected"
            # with col_PositiveAndNegative:    
                st.subheader("Positive :heavy_plus_sign: or Negative :heavy_minus_sign: Inputs")
                er_choice = st.radio("ER", options=["Positive", "Negative"],index=None,horizontal=True)
                er_result = er_choice.split()[0] if er_choice else "Not selected"
                pr_choice = st.radio("PR", options=["Positive", "Negative"],index=None,horizontal=True)   
                pr_result = pr_choice.split()[0] if pr_choice else "Not selected"
                her2_choice = st.radio("HER2", options=["Positive", "Negative","Equivocal"],index=None,horizontal=True)   
                her2_result = her2_choice.split()[0] if her2_choice else "Not selected"
            col1, col2, col3 = st.columns([2, 4, 2])
            with col2:
                submit_button = st.form_submit_button("Submit", use_container_width=True)    

            # Process form submission
            if submit_button:
                # Check for missing fields
                missing_fields = []
                if patient_first_bmi == 0.0:
                    missing_fields.append("First BMI")
                if patient_age == 0:
                    missing_fields.append("Age")
                if patient_size_cm == 0.0:
                    missing_fields.append("Size (cm)")
                if patient_ki67 == 0.0:
                    missing_fields.append("KI67")
                if not patient_other:
                    missing_fields.append("Other")    
                if not patient_family_history:
                    missing_fields.append("Family History")
                if not patient_menopausal_state:
                    missing_fields.append("Menopausal State")
                if not patient_t:
                    missing_fields.append("T")
                if not patient_n:
                    missing_fields.append("N")
                if not patient_laterality:
                    missing_fields.append("Laterality")
                if not patient_unilateral_bilateral:
                    missing_fields.append("Unilateral Bilateral")
                if not patient_site:
                    missing_fields.append("Site")
                if not patient_tumor_type:
                    missing_fields.append("Tumor Type")
                if not patient_grade:
                    missing_fields.append("Grade")
                if not Hormonal_Contraception_choice:
                    missing_fields.append("Hormonal Contraception")    
                # if not dm_choice:
                #     missing_fields.append("DM")
                # if not htn_choice:
                #     missing_fields.append("HTN")
                if not vte_choice:
                    missing_fields.append("VTE")
                # if not cvd_choice:
                #     missing_fields.append("CVD")
                if not lymphovascular_invasion_choice:
                    missing_fields.append("Lymphovascular Invasion")
                if not er_choice:
                    missing_fields.append("ER")
                if not pr_choice:
                    missing_fields.append("PR")
                if not her2_choice:
                    missing_fields.append("HER2")
                if missing_fields:
                    st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
                else:
                    # Display results
                    st.subheader("Risk Assessment Results")
                    st.write("Numerical Inputs:")
                    st.write(f"- Patient MRN: {patient_MRN}")
                    st.write(f"- First BMI: {patient_first_bmi}")
                    st.write(f"- Age: {patient_age}")
                    st.write(f"- Size (cm): {patient_size_cm}")
                    st.write(f"- KI67: {patient_ki67}")

                    st.write("Categorical Inputs:")
                    st.write(f"- Family History: {patient_family_history}")
                    st.write(f"- Menopausal State: {patient_menopausal_state}")
                    st.write(f"- T: {patient_t}")
                    st.write(f"- N: {patient_n}")
                    st.write(f"- Laterality: {patient_laterality}")
                    st.write(f"- Unilateral Bilateral: {patient_unilateral_bilateral}")
                    st.write(f"- Site: {patient_site}")
                    st.write(f"- Tumor Type: {patient_tumor_type}")
                    st.write(f"- Grade: {patient_grade}")

                    st.write("Yes or No Inputs:")
                    # st.write(f"- DM: {dm_result}")
                    # st.write(f"- HTN: {htn_result}")
                    st.write(f"- VTE: {vte_result}")
                    # st.write(f"- CVD: {cvd_result}")
                    st.write(f"- Lymphovascular Invasion: {lymphovascular_invasion_result}")
                    st.write(f"- ER: {er_result}")
                    st.write(f"- PR: {pr_result}")
                    st.write(f"- HER2: {her2_result}")
                    patient_data = {
                                        "MRN": int(patient_MRN),
                                        "patient_first_bmi": float(patient_first_bmi),
                                        "patient_age": int(patient_age),
                                        "patient_size_cm": float(patient_size_cm),
                                        "patient_ki67": float(patient_ki67),
                                        "Others:":str(patient_other),
                                        "patient_family_history": str(patient_family_history),
                                        "patient_menopausal_state": str(patient_menopausal_state),
                                        "patient_t": str(patient_t),
                                        "patient_n": str(patient_n),
                                        "patient_laterality": str(patient_laterality),
                                        "patient_unilateral_bilateral": str(patient_unilateral_bilateral),
                                        "patient_site": str(patient_site),
                                        "patient_tumor_type": str(patient_tumor_type),
                                        "patient_grade": str(patient_grade),
                                        "Hormonal_Contraception":str(Hormonal_Contraception_result),
                                        # "dm_result": str(dm_choice),
                                        # "htn_result": str(htn_choice),
                                        "vte_result": str(vte_choice),
                                        # "cvd_result": str(cvd_choice),
                                        "lymphovascular_invasion_result": str(lymphovascular_invasion_choice),
                                        "er_result": str(er_choice),
                                        "pr_result": str(pr_choice),
                                        "her2_result": str(her2_choice)                                    }
                    st.write(Network.post_make_assesment(18,int(patient_MRN),patient_data))      
        # el mfrood @@ omar trg3 el risk assement result hnh fy variable asmo case
        modal = Modal("Risk Assessment Result", key="result-modal", padding=10, max_width=430)

        # Button to open the modal
        

        # Generate a random value for 'case'
        case = 0

        # Check if modal is open
        if modal.is_open():
            # Content inside the modal based on the value of 'case'
            with modal.container():
                if case == 0:
                    content = """
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                            <h1 style="color: red; font-size: 28px; font-family: 'Open Sans', sans-serif;">No</h1>
                            <h2 style="font-size: 16px; font-family: 'Open Sans', sans-serif;">Patient will not have metastasis</h2>
                        </div>
                    """
                else:
                    content = """
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                            <h1 style="color: green; font-size: 28px; font-family: 'Open Sans', sans-serif;">Yes</h1>
                            <h2 style="font-size: 16px; font-family: 'Open Sans', sans-serif;">Patient might have metastasis</h2>
                        </div>
                    """
                st.markdown(content, unsafe_allow_html=True)

                # Set the height of the modal dynamically
                st.markdown(
                    f"<style>.streamlit-modal .element-container{{height: auto}}</style>",
                    unsafe_allow_html=True
                )                   
                    
        # if st.button("Get Assesment by Doc Id"):
        #     # st.write(Network.get_assesment_byDocId(18))

        #     response = Network.get_assesment_byDocId(20)
        #     all_data = []

        #     # Iterate through each assessment
        #     for assessment in response['assessments']:
        #         # Convert medical_info dictionary directly to Series
        #         assessment_data = pd.Series(assessment['medical_info'])
        #         # Add other scalar values directly to the Series
        #         assessment_data['prediction'] = assessment['prediction']
        #         # Assuming status_message is not in your data. If it is, uncomment the next line
        #         # assessment_data['status_message'] = assessment['status_message']
        #         assessment_data['ground_truth'] = assessment['ground_truth']
        #         assessment_data['creation_date'] = assessment['creation_date']
        #         # Append the Series to the list
        #         all_data.append(assessment_data)

        #     # Convert the list of Series to a DataFrame
        #     full_data_frame = pd.DataFrame(all_data)

        #     #convert dataframe to bytes                     
        #     cacheInMemory.save_assesment_byDocId(full_data_frame.to_json())
            
        #     result=cacheInMemory.get_assessment_byDocId().decode('utf-8')
        #     retrieved_dataframe = pd.read_json(result)
         

        #     st.write(retrieved_dataframe)
            
        # #TODO:Uncomment later @omarelansary

        # # if st.button("Getter"):
        # #     st.write(pd.read_json(cacheInMemory.get_assessment_byDocId().decode('utf-8')))

        # #TODO:Comment later @omarelansary
        # #@mohra

        # if st.button("Getter"):
        #     st.write(cacheInMemory.get_assessment_byDocId_version2())

        #     # st.table(cache.get_data(1))
            


css="""
    <style>
        [data-testid="stForm"] {
            background: White;
        }
    </style>
    """
st.write(css, unsafe_allow_html=True)
