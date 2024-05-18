import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
def app():
    st.write('Home')
    st.title("SLNB Cancer Awareness WebSite")
    st.sidebar.title("Menu")

    # Define dictionary to map emoji labels to their corresponding sections
    options = {
        "🏠 Home": "home",
        "📚 Educational Content": "educational",
        "📊 General Statistics": "statistics",
        "🎗️ Awareness Campaigns": "campaigns",
        "💬 Frequently Asked Questions": "Frequently Asked Questions"
    }

    # Sidebar buttons with emojis
    if st.sidebar.button("🏠 Home"):
        set_session_state(options, "home")
    if st.sidebar.button("📚 Educational Content"):
        set_session_state(options, "educational")
    if st.sidebar.button("📊 General Statistics"):
        set_session_state(options, "statistics")
    if st.sidebar.button("🎗️ Awareness Campaigns"):
        set_session_state(options, "campaigns")
    if st.sidebar.button("💬 Frequently Asked Questions"):
        set_session_state(options, "Frequently Asked Questions")

    # Display content based on selected option
    if "home" in st.session_state:
        st.write("Welcome to the Metastatic Breast Cancer Awareness App!")
        st.write("Use the sidebar to navigate to different sections.")

    if "educational" in st.session_state:
        st.header("Educational Content")
        st.write("### Sentinel Lymph Node Biopsy (SLNB) in Breast Cancer")
        st.write("Sentinel Lymph Node Biopsy (SLNB) is a surgical procedure used to determine if cancer has spread beyond the breast to nearby lymph nodes. During SLNB, the surgeon identifies and removes the sentinel lymph node(s), which are the first lymph nodes to which cancer cells are likely to spread from the primary tumor.")
        st.write("#### Why is SLNB performed?")
        st.write("SLNB helps in determining the stage of breast cancer and aids in treatment planning. It helps in avoiding the removal of unnecessary lymph nodes, reducing the risk of complications such as lymphedema.")
        st.write("#### Procedure")
        st.write("1. Preoperative preparation: The patient may receive anesthesia before the procedure.")
        st.write("2. Injection of tracer: A tracer material, often a radioactive substance or blue dye, is injected into the area around the tumor.")
        st.write("3. Mapping of sentinel lymph nodes: The tracer material travels through the lymphatic channels to the sentinel lymph node(s), which are then identified by the surgeon.")
        st.write("4. Biopsy: The surgeon removes the identified sentinel lymph node(s) for examination under a microscope.")
        st.write("#### Risks and complications")
        st.write("Although SLNB is generally safe, there are some risks, including infection, bleeding, and lymphedema. It is important to discuss the benefits and risks of SLNB with your healthcare provider.")
        st.write("### What is metastatic breast cancer (MBC)?")
        st.write("MBC (also called stage IV or advanced breast cancer) is breast cancer that has spread beyond the breast to other organs in the body (most often the bones, lungs, liver or brain). Both women and men can be diagnosed with MBC.")

    if "statistics" in st.session_state:
        st.header("SLNB Statistics")

        # Sample statistical data for SLNB
        slnb_data = {
            'Year': [2015, 2016, 2017, 2018, 2019],
            'SLNB Procedures': [5000, 5200, 5400, 5600, 5800],
            'Positive SLNB Cases': [800, 820, 850, 870, 890]
        }
        slnb_df = pd.DataFrame(slnb_data)

        # Visualize SLNB statistics
        fig = px.line(slnb_df, x='Year', y=['SLNB Procedures', 'Positive SLNB Cases'], 
                      title='Trends in Sentinel Lymph Node Biopsy (SLNB) Procedures and Positive Cases')
        st.plotly_chart(fig)

        # Pie chart for SLNB procedures
        st.subheader("SLNB Procedures by Year")
        fig_pie = px.pie(slnb_df, values='SLNB Procedures', names='Year', title='SLNB Procedures by Year')
        st.plotly_chart(fig_pie)
        # Define the percentages
        initial_metastatic_percentage = 8  # 6-10% of new cases
        future_metastatic_percentage = 25  # 20-30% of all cases
        survival_percentage = 15  # Survival rate for at least five years after diagnosis with MBC
        

# Create pie chart for initially metastatic cases
        fig1, ax1 = plt.subplots()
        ax1.pie([initial_metastatic_percentage, 100 - initial_metastatic_percentage],
        labels=["Initially Stage IV or Metastatic", "Other Stages"],
        autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])
        ax1.axis('equal')

# Create pie chart for estimated future metastatic cases
        fig2, ax2 = plt.subplots()
        ax2.pie([future_metastatic_percentage, 100 - future_metastatic_percentage],
        labels=["Estimated Future Metastatic", "Non-Metastatic"],
        autopct='%1.1f%%', startangle=90, colors=['orange', 'lightgreen'])
        ax2.axis('equal')

# Create pie chart for survival rate for MBC patients
        fig3, ax3 = plt.subplots()
        ax3.pie([survival_percentage, 100 - survival_percentage],
        labels=["Survival Rate (>5 years)", "Non-Survival Rate"],
        autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightgreen'])
        ax3.axis('equal')

# Display the charts using Streamlit
        st.write("Proportion of new breast cancer cases that are initially Stage IV or metastatic:")
        st.pyplot(fig1)

        st.write("Estimated percentage of all breast cancer cases that will become metastatic:")
        st.pyplot(fig2)

        st.write("Survival rate for at least five years after diagnosis with MBC:")
        st.pyplot(fig3)
   
    if "campaigns" in st.session_state:
        st.header("Awareness Campaigns")

        # Include visualizations and informative content for awareness campaigns
        st.subheader("1. Breast Cancer Infographics")
        st.write("Create visually appealing infographics highlighting key statistics about breast cancer incidence, mortality rates, and survival rates. Include information about the benefits of early detection and the role of screening tests like mammograms.")
        st.image("C:/Users/BOOTCAMP/Desktop/signup/c.jpg", use_column_width=True)

        st.subheader("2. Breast Cancer Risk Factors Visualization")
        st.write("Present visualizations that illustrate common risk factors associated with breast cancer, such as age, family history, genetic mutations (BRCA1 and BRCA2), hormone replacement therapy, alcohol consumption, and obesity. This can help users understand their risk profile and take preventive measures accordingly.")
        st.image("C:/Users/BOOTCAMP/Desktop/signup/n.jpg", use_column_width=True)

        st.subheader("3. Breast Cancer Prevention Tips")
        st.write("Provide visual guides on lifestyle changes and preventive measures that can reduce the risk of breast cancer, such as maintaining a healthy diet, exercising regularly, limiting alcohol intake, avoiding smoking, and conducting regular breast self-exams.")
        st.image("breast_cancer_prevention_tips.jpg", use_column_width=True)

    if "Frequently Asked Questions" in st.session_state:
        st.header("Frequently Asked Questions")
        st.write("### What are signs and symptoms of MBC?") 
        st.write("• Sever and persistent headache")
        st.write("• Bone pain and fracture")
        st.write("• Shortness of breath")
        st.write("• abdominal bloating, pain, or swelling")
        st.write("• constant nausea, vomiting, or weight loss")
        st.write("• numbness or weakness anywhere in your body and confusion")
        st.write("• loss of appetite")
        st.write("• vision problems (blurry vision, double vision, loss of vision)")
        st.write("• loss of balance")
        st.write("### How is MBC found?")
        st.write("If breast cancer is found in the lymph nodes, tests are done to check for metastasis. If symptoms suchas shortness of breath, chronic cough, weight loss or bone pain occur, they may be signs of MBC. Tests are then needed to confirm or rule out metastases.")
        st.write("The three main tests are")
        st.write("• A blood test to check for spread to the liver or bones")
        st.write("• Bone scans to test for spread to the bone")
        st.write("• X-ray/CT scans to test for spread to the chest, abdomen and liver")


def set_session_state(options, selected_option):
    # Reset session state
    for option in options.values():
        st.session_state.pop(option, None)
    # Set selected option in session state
    st.session_state[selected_option] = True
