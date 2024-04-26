import streamlit as st

def main():
    st.set_page_config(
        page_title="Risk Assessment",
        layout="wide",  # Set layout to wide mode
        initial_sidebar_state="collapsed",  # Collapse the sidebar initially
    )
    st.title("Risk Assessment")
    with st.form("Risk Assessment"):
        col_Numerical, col_Categorical, col_YesorNo = st.columns(3)

        # DM selection
        with col_Numerical:
        # Numerical inputs
            st.subheader("Numerical Inputs")
            patient_first_bmi = st.number_input("First BMI", value=0.0, min_value=0.0)
            patient_age = st.number_input("Age", value=0, min_value=0)
            patient_size_cm = st.number_input("size cm", value=0.0, min_value=0.0)
            patient_ki67 = st.number_input("KI67", value=0.0, min_value=0.0)
        with col_Categorical:
        # Categorical inputs
            st.subheader("Categorical Inputs")

            patient_family_history = st.selectbox("Family History", options=["Yes - BC","Yes - both","Yes - other cancers", "No","Unrecorded"],index=None, placeholder="Select family history...")
            patient_menopausal_state = st.selectbox("Menopausal State", options=["Post-M", "Pre-M", "Unrecorded"],index=None, placeholder="Select menopausal state...")
            patient_t = st.selectbox("T", options=["T1", "T2", "T3","T4","Tis"], index=None,placeholder="Select T...")
            patient_n = st.selectbox("N", options=["N0", "N1","N2", "Nx"],index=None, placeholder="Select N...")
            patient_laterality = st.selectbox("Laterality", options=["Left", "Right", "Bilateral"],index=None, placeholder="Select laterality...")
            patient_unilateral_bilateral = st.selectbox("Unilateral Bilateral", options=["Unilateral", "Bilateral"],index=None, placeholder="Select unilateral or bilateral...")
            patient_site = st.selectbox("Site", options=["Upper outer quadrant","Upper inner quadrant","Lower outer quadrant", "Lower inner quadrant","Para areolar", "Other"],index=None, placeholder="Select site...")
            patient_tumor_type = st.selectbox("Tumor Type", options=["Invasive duct carcinoma (NST)","Invasive Lobular carcinoma NOS ","Ductal carcinoma in situ, DCIS", "Invasive tubular/cribriform carcinoma","Mixed Tumor", "Other"], index=None,placeholder="Select tumor type...")
            patient_grade = st.selectbox("Grade", options=["I", "II","III"],index=None, placeholder="Select grade...")
        with col_YesorNo:
            st.subheader("Yes or No Inputs")
            dm_choice = st.radio("DM", options=["Yes", "No"],index=None, horizontal=True)
            dm_result = dm_choice.split()[0] if dm_choice else "Not selected"
            htn_choice = st.radio("HTN", options=["Yes", "No"],index=None,horizontal=True)   
            htn_result = htn_choice.split()[0] if htn_choice else "Not selected"
            vte_choice = st.radio("VTE", options=["Yes", "No"],index=None,horizontal=True)
            vte_result = vte_choice.split()[0] if vte_choice else "Not selected"
            cvd_choice = st.radio("CVD", options=["Yes", "No"],index=None,horizontal=True)    
            cvd_result = cvd_choice.split()[0] if cvd_choice else "Not selected"
            lymphovascular_invasion_choice = st.radio("Lymphovascular Invasion", options=["Yes", "No"],index=None,horizontal=True)
            lymphovascular_invasion_result = lymphovascular_invasion_choice.split()[0] if lymphovascular_invasion_choice else "Not selected"
            st.subheader("Positive or No Negative")
            er_choice = st.radio("ER", options=["Positive", "Negative"],index=None,horizontal=True)
            er_result = er_choice.split()[0] if er_choice else "Not selected"
            pr_choice = st.radio("PR", options=["Positive", "Negative"],index=None,horizontal=True)   
            pr_result = pr_choice.split()[0] if pr_choice else "Not selected"
            her2_choice = st.radio("HER2", options=["Positive", "Negative","Equivocal"],index=None,horizontal=True)   
            her2_result = her2_choice.split()[0] if her2_choice else "Not selected"
        submit_button = st.form_submit_button("Submit")

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
            if not dm_choice:
                missing_fields.append("DM")
            if not htn_choice:
                missing_fields.append("HTN")
            if not vte_choice:
                missing_fields.append("VTE")
            if not cvd_choice:
                missing_fields.append("CVD")
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
                st.write(f"- DM: {dm_choice}")
                st.write(f"- HTN: {htn_choice}")
                st.write(f"- VTE: {vte_choice}")
                st.write(f"- CVD: {cvd_choice}")
                st.write(f"- Lymphovascular Invasion: {lymphovascular_invasion_choice}")
                st.write(f"- ER: {er_choice}")
                st.write(f"- PR: {pr_choice}")
                st.write(f"- HER2: {her2_choice}")
    css="""
<style>
    [data-testid="stForm"] {
        background: White;
    }
</style>
"""
    st.write(css, unsafe_allow_html=True)
if __name__ == '__main__':
    main()    
        # st.subheader("Your Inputs:")
        # st.write("patient_first_bMI:", patient_first_bMI)
        # st.write("patient_age:", patient_age)
        # st.write("patient_size_cm:", patient_size_cm)
        # st.write("patient_ki67:", patient_ki67)
        # st.write("family history:", patient_family_history)
        # st.write("Menopausal state :", patient_menopausal_state)
        # st.write("patient T :", patient_t)
        # st.write("patient N :", patient_n)
        # st.write("Laterality :", patient_laterality)
        # st.write("Unilateral Bilateral :", patient_unilateral_bilateral)
        # st.write("Site :", patient_site)
        # st.write("HER2 Result:", patient_her2)
        # st.write("patient_tumor_type :", patient_tumor_type)
        # st.write("Grade :", patient_grade)
        # st.write("DM Result:", dm_result)
        # st.write("HTN Result:", htn_result)
        # st.write("VTE Result:", vte_result)
        # st.write("CVD Result:", cvd_result)
        # st.write("Lymphovascular invasion Result:", lymphovascular_invasion_result)
        # st.write("ER Result:", er_result)
        # st.write("PR Result:", pr_result)
        # agree = st.checkbox('I agree')
        # if agree:
        #     st.write('Great!'))
