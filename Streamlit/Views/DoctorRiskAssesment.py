import streamlit as st
import pandas as pd
from pandas import json_normalize
from Networking.Networking import Networking
import pandas as pd
from ourData.cache import LocalCache
from streamlit_modal import Modal
from streamlit_modal import Modal

# Example JSON data

def default_form(userAuthData):
        Network = Networking()
        cacheInMemory = LocalCache()
        patient_data=None
        predectionResult=None
        predectionPercentage=None
        # with st.form("Breast Cancer Metastasis Risk Prediction"):
        predection_modal = Modal("Breast Cancer Metastasis Risk Prediction Result", key="result-modal", padding=10, max_width=430)
        col_Numerical, col_Categorical1, col_YesorNo = st.columns(3)

        # Numerical inputs
        with col_Numerical:
            st.subheader(":abacus: Numerical Inputs ")
            patient_MRN = st.number_input("Patient MRN", value=0, min_value=0, format="%d")
            patient_first_bmi = st.number_input("First BMI", value=0.00, min_value=0.0, max_value=100.0, format="%.2f")
            patient_age = st.number_input("Age", value=0, min_value=0, max_value=150, format="%d")
            patient_size_cm = st.number_input("Size cm", value=0.00, min_value=0.0, max_value=20.0, format="%.2f")
            patient_ki67 = st.number_input("KI67", value=0, min_value=0, max_value=100, format="%d")

        # Categorical inputs
        with col_Categorical1:
            st.subheader(":page_facing_up: Categorical Inputs ")
            col_11, col_22 = st.columns(2)
            with col_11:
                patient_family_history = st.selectbox("Family History", options=["Yes - BC", "Yes - both", "Yes - other cancers", "No", "Unrecorded"], index=None, placeholder="Select family history...")
                patient_other = st.text_input("Other")
                patient_unilateral_bilateral = st.selectbox("Unilateral Bilateral", options=["Unilateral", "Bilateral", "Unrecorded"], index=None, placeholder="Select unilateral or bilateral...")
                patient_laterality = st.selectbox("Laterality", options=["Left", "Right", "Bilateral", "Unrecorded"], index=None, placeholder="Select laterality...")
                patient_menopausal_state = st.selectbox("Menopausal State", options=["Post-M", "Pre-M", "Unrecorded"], index=None, placeholder="Select menopausal state...")
            with col_22:
                patient_n = st.selectbox("N", options=["N0", "N1", "N2", "N3", "Nx", "Unrecorded"], index=None, placeholder="Select N...")
                patient_t = st.selectbox("T", options=["T1", "T2", "T3", "T4", "Tis", "To", "Unrecorded"], index=None, placeholder="Select T...")
                patient_grade = st.selectbox("Grade", options=["I", "II", "III", "Unrecorded"], index=None, placeholder="Select grade...")
                patient_tumor_type = st.text_input("Tumor Type")
                patient_site = st.text_input("Site")

        # Yes or No inputs
        with col_YesorNo:
            st.subheader("Yes :heavy_check_mark: or No :heavy_multiplication_x: Inputs")
            vte_choice = st.radio("VTE", options=["Yes", "No"], index=None, horizontal=True)
            Hormonal_Contraception_choice = st.radio("Hormonal Contraception", options=["Yes", "No"], index=None, horizontal=True)
            lymphovascular_invasion_choice = st.radio("Lymphovascular Invasion", options=["Yes", "No"], index=None, horizontal=True)
            st.subheader("Positive :heavy_plus_sign: or Negative :heavy_minus_sign: Inputs")
            er_choice = st.radio("ER", options=["Positive", "Negative"], index=None, horizontal=True)
            pr_choice = st.radio("PR", options=["Positive", "Negative"], index=None, horizontal=True)
            her2_choice = st.radio("HER2", options=["Positive", "Negative", "Equivocal"], index=None, horizontal=True)

        col111, col222 = st.columns([2,2])
        with col111:
            save_button = st.button("Save", use_container_width=True)
        with col222:
            predict_button = st.button("Predict", use_container_width=True) 
        # Process form submission
        if save_button:
            if patient_MRN == 0:
                st.error("Please enter Patient MRN.")
            else:
                # Check for missing or unrecorded fields and default them to "Unrecorded" if necessary
                patient_data = {
                    "MRN": int(patient_MRN),
                    "patient_first_bmi": float(patient_first_bmi) if patient_first_bmi is not None and patient_first_bmi != 0.0 else "Unrecorded",
                    "patient_age": int(patient_age) if patient_age is not None and patient_age != 0 else "Unrecorded",
                    "patient_size_cm": float(patient_size_cm) if patient_size_cm is not None and patient_size_cm != 0.0 else "Unrecorded",
                    "patient_ki67": float(patient_ki67) if patient_ki67 is not None and patient_ki67 != 0 else "Unrecorded",
                    "Others": patient_other if patient_other else "Unrecorded",
                    "patient_family_history": patient_family_history if patient_family_history != "Unrecorded" else "Unrecorded",
                    "patient_menopausal_state": patient_menopausal_state if patient_menopausal_state != "Unrecorded" else "Unrecorded",
                    "patient_t": patient_t if patient_t != "Unrecorded" else "Unrecorded",
                    "patient_n": patient_n if patient_n != "Unrecorded" else "Unrecorded",
                    "patient_laterality": patient_laterality if patient_laterality != "Unrecorded" else "Unrecorded",
                    "patient_unilateral_bilateral": patient_unilateral_bilateral if patient_unilateral_bilateral != "Unrecorded" else "Unrecorded",
                    "patient_site": patient_site if patient_site else "Unrecorded",
                    "patient_tumor_type": patient_tumor_type if patient_tumor_type else "Unrecorded",
                    "patient_grade": patient_grade if patient_grade != "Unrecorded" else "Unrecorded",
                    "Hormonal_Contraception": Hormonal_Contraception_choice if Hormonal_Contraception_choice else "Unrecorded",
                    "vte_result": vte_choice if vte_choice else "Unrecorded",
                    "lymphovascular_invasion_result": lymphovascular_invasion_choice if lymphovascular_invasion_choice else "Unrecorded",
                    "er_result": er_choice if er_choice else "Unrecorded",
                    "pr_result": pr_choice if pr_choice else "Unrecorded",
                    "her2_result": her2_choice if her2_choice else "Unrecorded"
                }

                try:
                    assessment_result = Network.post_make_assesment(userAuthData['id'], int(patient_MRN), patient_data)
                    if assessment_result:
                        st.success('Saved Successfully')
                except Exception as e:
                    st.error(f"An error occurred: {e}")   
                # Check for the number of unrecorded fields
                
                    # st.write(Network.post_make_assesment(18, int(patient_MRN), patient_data))
        if predict_button:
            missing_or_unrecorded_fields = []

            if patient_MRN == 0:
                st.error("Please enter Patient MRN.")
            else:
                # Check for missing or unrecorded fields and default them to "Unrecorded" if necessary
                patient_data = {
                    "MRN": int(patient_MRN),
                    "patient_first_bmi": float(patient_first_bmi) if patient_first_bmi is not None and patient_first_bmi != 0.0 else "Unrecorded",
                    "patient_age": int(patient_age) if patient_age is not None and patient_age != 0 else "Unrecorded",
                    "patient_size_cm": float(patient_size_cm) if patient_size_cm is not None and patient_size_cm != 0.0 else "Unrecorded",
                    "patient_ki67": float(patient_ki67) if patient_ki67 is not None and patient_ki67 != 0 else "Unrecorded",
                    "Others": patient_other if patient_other else "Unrecorded",
                    "patient_family_history": patient_family_history if patient_family_history != "Unrecorded" else "Unrecorded",
                    "patient_menopausal_state": patient_menopausal_state if patient_menopausal_state != "Unrecorded" else "Unrecorded",
                    "patient_t": patient_t if patient_t != "Unrecorded" else "Unrecorded",
                    "patient_n": patient_n if patient_n != "Unrecorded" else "Unrecorded",
                    "patient_laterality": patient_laterality if patient_laterality != "Unrecorded" else "Unrecorded",
                    "patient_unilateral_bilateral": patient_unilateral_bilateral if patient_unilateral_bilateral != "Unrecorded" else "Unrecorded",
                    "patient_site": patient_site if patient_site else "Unrecorded",
                    "patient_tumor_type": patient_tumor_type if patient_tumor_type else "Unrecorded",
                    "patient_grade": patient_grade if patient_grade != "Unrecorded" else "Unrecorded",
                    "Hormonal_Contraception": Hormonal_Contraception_choice if Hormonal_Contraception_choice else "Unrecorded",
                    "vte_result": vte_choice if vte_choice else "Unrecorded",
                    "lymphovascular_invasion_result": lymphovascular_invasion_choice if lymphovascular_invasion_choice else "Unrecorded",
                    "er_result": er_choice if er_choice else "Unrecorded",
                    "pr_result": pr_choice if pr_choice else "Unrecorded",
                    "her2_result": her2_choice if her2_choice else "Unrecorded"
                }

                # Check for the number of unrecorded fields
                unrecorded_count = sum(value == "Unrecorded" for value in patient_data.values())
                if unrecorded_count > 5:
                    st.error(f"Please fill in the following fields or reduce 'Unrecorded' selections: {', '.join([k for k, v in patient_data.items() if v == 'Unrecorded'])}")
                else:
                    # Display results
                    st.subheader("Breast Cancer Metastasis Risk Prediction Results")
                    for key, value in patient_data.items():
                        st.write(f"- {key.replace('_', ' ').title()}: {value}")
                        
                    # Make API call and handle the result
                    try:
                        assessment_result = Network.post_make_assesment(userAuthData['id'], int(patient_MRN), patient_data)
                        if assessment_result:
                            predection_modal.open()
                            predectionResult=assessment_result['prediction']          # Check if modal is open
                            predectionPercentage=assessment_result['predictionProbability']
                    except Exception as e:
                        st.error(f"An error occurred: {e}")   

        if predection_modal.is_open():
            # Content inside the modal based on the value of 'predectionResult'
            with predection_modal.container():
                if predectionResult == 0:
                    content = f"""
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                            <h1 style="color: green; font-size: 28px; font-family: 'Open Sans', sans-serif;">Patient is Unlikley to Have Metastasis</h1>
                        </div>
                    """
                else:
                    content = f"""
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                            <h1 style="color: red; font-size: 28px; font-family: 'Open Sans', sans-serif;">Patient may Have Metastasis</h1>
                        </div>
                    """
                st.markdown(content, unsafe_allow_html=True)

                    # Set the height of the modal dynamically
                st.markdown(
                        f"<style>.streamlit-modal .element-container{{height: auto}}</style>",
                        unsafe_allow_html=True
                    )
       



def editing_form(df, selected_mrn, userAuthData):
        Network = Networking()
        selected_row = df[df["MRN"] == selected_mrn].iloc[0]
        form_key = f"form_{selected_mrn}"
        modal = Modal("Confirm Deletion", key="confirm_deletion")
        edited_patient_data=None
        predectionResult=None
        predection_modal = Modal("Breast Cancer Metastasis Risk Prediction Result", key="result-modal", padding=10, max_width=430)

        col_Numerical, col_Categorical1, col_YesorNo = st.columns(3)
        with col_Numerical:
            st.subheader(":abacus: Numerical Inputs ")
            patient_MRN = st.number_input("Patient MRN", value=selected_row["MRN"], min_value=0, format="%d", disabled=True)
            patient_first_bmi = st.number_input("First BMI", value=float(selected_row['patient_first_bmi']) if selected_row['patient_first_bmi'] not in ["", None] else None, min_value=0.0, max_value=100.0, format="%.2f")
            patient_age = st.number_input("Age", value=int(selected_row["patient_age"]) if selected_row['patient_age'] not in ["", None] else None , min_value=0, max_value=150, format="%d")
            patient_size_cm = st.number_input("Size cm", value=float(selected_row["patient_size_cm"]) if selected_row['patient_size_cm'] not in ["", None] else None, min_value=0.0, max_value=2000.0, format="%.2f")
            patient_ki67 = st.number_input("KI67", value=int(selected_row["patient_ki67"]) if selected_row['patient_ki67'] not in ["", None] else None)
        with col_Categorical1:
            st.subheader(":page_facing_up: Categorical Inputs ")
            col_11, col_22 = st.columns(2)
            with col_11:
                familyHistoryOptions=["Yes - BC", "Yes - both", "Yes - other cancers", "No", "Unrecorded"]
                patient_family_history = st.selectbox("Family History", options=familyHistoryOptions, index=next((i for i, option in enumerate(familyHistoryOptions) if option == selected_row['patient_family_history']), None), placeholder="Select family history...")
                patient_other = st.text_input("Other",value=selected_row["Others"] if selected_row["Others"] else None)
                patient_unilateral_bilateral = st.selectbox("Unilateral Bilateral", options=["Unilateral", "Bilateral", "Unrecorded"], index=next((i for i, option in enumerate(["Unilateral", "Bilateral", "Unrecorded"]) if option == selected_row["patient_unilateral_bilateral"]), None), placeholder="Select unilateral or bilateral...")
                patient_laterality = st.selectbox("Laterality", options=["Left", "Right", "Bilateral", "Unrecorded"], index=next((i for i, option in enumerate(["Left", "Right", "Bilateral", "Unrecorded"]) if option == selected_row["patient_laterality"]), None), placeholder="Select laterality...")
                patient_menopausal_state = st.selectbox("Menopausal State", options=["Post-M", "Pre-M", "Unrecorded"], index=next((i for i, option in enumerate(["Post-M", "Pre-M", "Unrecorded"]) if option == selected_row["patient_menopausal_state"]), None), placeholder="Select menopausal state...")
            with col_22:
                patient_n = st.selectbox("N", options=["N0", "N1", "N2", "N3", "Nx", "Unrecorded"], index=next((i for i, option in enumerate(["N0", "N1", "N2", "N3", "Nx", "Unrecorded"]) if option == selected_row["patient_n"]), None), placeholder="Select N...")
                patient_t = st.selectbox("T", options=["T1", "T2", "T3", "T4", "Tis", "To", "Unrecorded"], index=next((i for i, option in enumerate(["T1", "T2", "T3", "T4", "Tis", "To", "Unrecorded"]) if option == selected_row["patient_t"]), None), placeholder="Select T...")
                patient_grade = st.selectbox("Grade", options=["I", "II", "III", "Unrecorded"], index=next((i for i, option in enumerate(["I", "II", "III", "Unrecorded"]) if option == selected_row["patient_grade"]), None), placeholder="Select grade...")
                patient_tumor_type = st.text_input("Tumor Type", value=selected_row["patient_tumor_type"] if selected_row["patient_tumor_type"] else None)
                patient_site = st.text_input("Site", value=selected_row["patient_site"] if selected_row["patient_site"] else None)
        with col_YesorNo:
            st.subheader("Yes :heavy_check_mark: or No :heavy_multiplication_x: Inputs")
            vte_choice = st.radio("VTE", options=["Yes", "No"], index=0 if selected_row["vte_result"] == "Yes" else 1 if selected_row["vte_result"] == "No" else None, horizontal=True)
            Hormonal_Contraception_choice = st.radio("Hormonal Contraception", options=["Yes", "No"],index=0 if selected_row["Hormonal_Contraception"] == "Yes" else 1 if selected_row["Hormonal_Contraception"] == "No" else None, horizontal=True)
            lymphovascular_invasion_choice = st.radio("Lymphovascular Invasion", options=["Yes", "No"], index=0 if selected_row["lymphovascular_invasion_result"] == "Yes" else 1 if selected_row["lymphovascular_invasion_result"] == "No" else None, horizontal=True)
            st.subheader("Positive :heavy_plus_sign: or Negative :heavy_minus_sign: Inputs")
            er_choice = st.radio("ER", options=["Positive", "Negative"], index=0 if selected_row["er_result"] == "Positive" else 1 if selected_row["er_result"] == "Negative" else None, horizontal=True)
            pr_choice = st.radio("PR", options=["Positive", "Negative"], index=0 if selected_row["pr_result"] == "Positive" else 1 if selected_row["pr_result"] == "Negative" else None, horizontal=True)
            her2_choice = st.radio("HER2", options=["Positive", "Negative", "Equivocal"], index=0 if selected_row["her2_result"] == "Positive" else (1 if selected_row["her2_result"] == "Negative" else 2 if selected_row["her2_result"] == "Equivocal" else None), horizontal=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            saveEdits_button = st.button("Save Edits", use_container_width=True)
        with col2:
            predict_button = st.button("Predict", use_container_width=True)    
        with col3:
            delete_button = st.button("Delete", use_container_width=True)

        if saveEdits_button:
            edited_patient_data = {
                "MRN": int(patient_MRN),
                "patient_first_bmi": float(patient_first_bmi) if patient_first_bmi is not None and patient_first_bmi != 0.0 else "Unrecorded",
                "patient_age": int(patient_age) if patient_age is not None and patient_age != 0 else "Unrecorded",
                "patient_size_cm": float(patient_size_cm) if patient_size_cm is not None and patient_size_cm != 0.0 else "Unrecorded",
                "patient_ki67": float(patient_ki67) if patient_ki67 is not None and patient_ki67 != 0 else "Unrecorded",
                "Others": patient_other if patient_other else "Unrecorded",
                "patient_family_history": patient_family_history if patient_family_history != "Unrecorded" else "Unrecorded",
                "patient_menopausal_state": patient_menopausal_state if patient_menopausal_state != "Unrecorded" else "Unrecorded",
                "patient_t": patient_t if patient_t != "Unrecorded" else "Unrecorded",
                "patient_n": patient_n if patient_n != "Unrecorded" else "Unrecorded",
                "patient_laterality": patient_laterality if patient_laterality != "Unrecorded" else "Unrecorded",
                "patient_unilateral_bilateral": patient_unilateral_bilateral if patient_unilateral_bilateral != "Unrecorded" else "Unrecorded",
                "patient_site": patient_site if patient_site else "Unrecorded",
                "patient_tumor_type": patient_tumor_type if patient_tumor_type else "Unrecorded",
                "patient_grade": patient_grade if patient_grade != "Unrecorded" else "Unrecorded",
                "Hormonal_Contraception": Hormonal_Contraception_choice if Hormonal_Contraception_choice else "Unrecorded",
                "vte_result": vte_choice if vte_choice else "Unrecorded",
                "lymphovascular_invasion_result": lymphovascular_invasion_choice if lymphovascular_invasion_choice else "Unrecorded",
                "er_result": er_choice if er_choice else "Unrecorded",
                "pr_result": pr_choice if pr_choice else "Unrecorded",
                "her2_result": her2_choice if her2_choice else "Unrecorded"
            }
            try:
                assessment_result = Network.post_make_assesment(userAuthData['id'], int(selected_mrn), edited_patient_data)
                if assessment_result:
                    st.success('Saved Successfully')
            except Exception as e:
                st.error(f"An error occurred: {e}")   

        if delete_button:
            modal.open()

            if modal.is_open():
                with modal.container():
                    st.markdown(
                        """
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                            <h1 style="color: green; font-size: 28px; font-family: 'Open Sans', sans-serif;">Are you sure you want to delete the selected data?</h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button("Confirm"):
                        # Logic to delete the selected data
                        df.drop(df[df["MRN"] == selected_mrn].index, inplace=True)
                        modal.close()
            try:
                deleteResponseResult =Network.post_delete_assesment(selected_mrn)
                if deleteResponseResult:
                    st.success('Deleted Successfully') 
            except Exception as e:
                st.error(f"An error occurred: {e}")   

  
        
        if predict_button:
            missing_or_unrecorded_fields = []

            if patient_MRN == 0:
                st.error("Please enter Patient MRN.")
            else:
                # Check for missing or unrecorded fields and default them to "Unrecorded" if necessary
                edited_patient_data = {
                "MRN": int(patient_MRN),
                "patient_first_bmi": float(patient_first_bmi) if patient_first_bmi is not None and patient_first_bmi != 0.0 else "Unrecorded",
                "patient_age": int(patient_age) if patient_age is not None and patient_age != 0 else "Unrecorded",
                "patient_size_cm": float(patient_size_cm) if patient_size_cm is not None and patient_size_cm != 0.0 else "Unrecorded",
                "patient_ki67": float(patient_ki67) if patient_ki67 is not None and patient_ki67 != 0 else "Unrecorded",
                "Others": patient_other if patient_other else "Unrecorded",
                "patient_family_history": patient_family_history if patient_family_history != "Unrecorded" else "Unrecorded",
                "patient_menopausal_state": patient_menopausal_state if patient_menopausal_state != "Unrecorded" else "Unrecorded",
                "patient_t": patient_t if patient_t != "Unrecorded" else "Unrecorded",
                "patient_n": patient_n if patient_n != "Unrecorded" else "Unrecorded",
                "patient_laterality": patient_laterality if patient_laterality != "Unrecorded" else "Unrecorded",
                "patient_unilateral_bilateral": patient_unilateral_bilateral if patient_unilateral_bilateral != "Unrecorded" else "Unrecorded",
                "patient_site": patient_site if patient_site else "Unrecorded",
                "patient_tumor_type": patient_tumor_type if patient_tumor_type else "Unrecorded",
                "patient_grade": patient_grade if patient_grade != "Unrecorded" else "Unrecorded",
                "Hormonal_Contraception": Hormonal_Contraception_choice if Hormonal_Contraception_choice else "Unrecorded",
                "vte_result": vte_choice if vte_choice else "Unrecorded",
                "lymphovascular_invasion_result": lymphovascular_invasion_choice if lymphovascular_invasion_choice else "Unrecorded",
                "er_result": er_choice if er_choice else "Unrecorded",
                "pr_result": pr_choice if pr_choice else "Unrecorded",
                "her2_result": her2_choice if her2_choice else "Unrecorded"
                }

                # Check for the number of unrecorded fields
                unrecorded_count = sum(value == "Unrecorded" for value in edited_patient_data.values())
                if unrecorded_count > 5:
                    st.error(f"Please fill in the following fields or reduce 'Unrecorded' selections: {', '.join([k for k, v in edited_patient_data.items() if v == 'Unrecorded'])}")
                else:
                    # Display results
                    st.subheader("Breast Cancer Metastasis Risk Prediction Results")
                    for key, value in edited_patient_data.items():
                        st.write(f"- {key.replace('_', ' ').title()}: {value}")
                        
                    # Make API call and handle the result
                    try:
                        assessment_result = Network.post_make_assesment(userAuthData['id'], int(patient_MRN), edited_patient_data)
                        if assessment_result:
                            predection_modal.open()
                            predectionResult=assessment_result['prediction']          # Check if modal is open
                            #predectionPercentage=assessment_result['predictionProbability']
                    except Exception as e:
                        st.error(f"An error occurred: {e}")   

        if predection_modal.is_open():
            # Content inside the modal based on the value of 'predectionResult'
            with predection_modal.container():
                if predectionResult == 0:
                    content = f"""
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                            <h1 style="color: green; font-size: 28px; font-family: 'Open Sans', sans-serif;">Patient is Unlikley to Have Metastasis</h1>
                        </div>
                    """
                else:
                    content = f"""
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                            <h1 style="color: red; font-size: 28px; font-family: 'Open Sans', sans-serif;">Patient may Have Metastasis</h1>
                        </div>
                    """
                st.markdown(content, unsafe_allow_html=True)

                    # Set the height of the modal dynamically
                st.markdown(
                        f"<style>.streamlit-modal .element-container{{height: auto}}</style>",
                        unsafe_allow_html=True
                    )
       


def app(userAuthData):
    Network = Networking()
    cacheInMemory = LocalCache()
    Cache = LocalCache()
    df = Cache.get_assessment_byDocId(userAuthData['id'])
    st.sidebar.title("Breast Cancer Metastasis Risk Prediction")
    menu_options = ["Enter New Patient", "Add Biopsy Result", "Choose Patient to(edite,pridect or delete)"]
    choice = st.sidebar.selectbox("Select an option", menu_options)
    if choice == "Enter New Patient":
        st.title(":clipboard: Breast Cancer Metastasis Risk Prediction ")

        default_form(userAuthData)
        # pass
    elif choice == "Add Biopsy Result":
        ###################
        Network = Networking()
        Cache = LocalCache()
        st.title(f"{userAuthData['username']} patients")
        df=Cache.get_assessment_byDocId(userAuthData['id'])
        st.write(df)
        # Initialize the session state if not already initialized
        if 'edit_mode' not in st.session_state:
            st.session_state['edit_mode'] = False
        if 'selected_mrn' not in st.session_state:
            st.session_state['selected_mrn'] = None
        if df.empty:
            st.write('Nothing to set')
        else:    
            # Select MRN before enabling editing
            st.write("Select Patient's MRN to add Biopsy Result:")
            selected_mrn = st.selectbox(
                "Select MRN",
                df['MRN'].unique()
            )
            st.session_state['selected_mrn'] = selected_mrn
            # st.write(f"Editing ground_truth for MRN: {selected_mrn}")
            if selected_mrn:
                    st.write(f"Add Biopsy Result for Patient with this MRN: {selected_mrn}")
                    # Enable edit mode if MRN is selected
                    st.session_state['edit_mode'] = True
            # Create an "Edit" button to enable editing

            if st.session_state['edit_mode']:
                # Make only the ground_truth column editable for the selected MRN
                edited_df = df.copy()
                mask = edited_df['MRN'] == selected_mrn
                st.write("Selected Row:")
                st.write(edited_df[mask])
                
                # Allow the user to select the new ground truth value from a dropdown menu
                new_ground_truth = st.selectbox("Select Biopsy Result", ["0", "1"])

                # Update the ground_truth column with the new value
                edited_df.loc[mask, 'ground_truth'] = new_ground_truth
                # Display the entire row corresponding to the selected MRN

            else:
                edited_df = df.copy()

            # Initialize the session state if not already initialized
            if 'edited_rows' not in st.session_state:
                st.session_state['edited_rows'] = {}

            # Update the session state with changes from data_editor
            st.session_state['edited_rows'] = edited_df.to_dict('index')
            
            # Find the changed rows by comparing session state with the original data
            changes = {}
            for index, row in edited_df.iterrows():
                if not row.equals(df.loc[index]):
                    changes[index] = row.to_dict()

            if changes:
                # Extract the row indices of the changes
                if st.button("Save Biopsy Result"):
                    changed_rows = list(changes.keys())
                    
                    # Extract the IDs, MRNs, and new ground_truth values from the changed rows
                    new_MRN_values = df.loc[changed_rows, 'MRN']
                    new_ground_truth_values = [changes[index]['ground_truth'] for index in changed_rows]

                    # Create a DataFrame with the extracted values
                    omr_change = pd.DataFrame({
                        'MRN': new_MRN_values,
                        'ground_truth': new_ground_truth_values
                    })
                    mrn = new_MRN_values.iloc[0] if not new_MRN_values.empty else "N/A"
                    new_ground_truth = new_ground_truth_values[0] if new_ground_truth_values else "N/A"
                    message = f"You have Added Biopsy Result with Value {new_ground_truth} for MRN {mrn}"
                    # Display the new DataFrame
                    modal = Modal("Added Biopsy Result", key="result-modal", padding=10, max_width=430)

                # Button to open the modal
                    


                    # Check if modal is open
                    if modal.is_open():
                        # Content inside the modal based on the value of 'case'
                        with modal.container():
                        
                            content = """
                                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                                    <h1 style="color: green; font-size: 28px; font-family: 'Open Sans', sans-serif;">{message}</h1>
                                </div>
                            """
                            
                            st.markdown(content, unsafe_allow_html=True)

                            # Set the height of the modal dynamically
                            st.markdown(
                                f"<style>.streamlit-modal .element-container{{height: auto}}</style>",
                                unsafe_allow_html=True
                            )             

            else:
                st.write("No changes detected.")

    # Run the app

        ##########################
    elif choice == "Choose Patient to(edite,pridect or delete)":
        st.title(":clipboard: Breast Cancer Metastasis Risk Prediction ")
        if not df.empty:
            mrn_list = df["MRN"].unique().tolist()
            selected_mrn = st.sidebar.selectbox("Select Patient MRN", mrn_list)
            editing_form(df, selected_mrn, userAuthData)
        else:
            st.write('No patients added yet') 


