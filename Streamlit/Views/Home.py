import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def app():
    # CSS to inject contained in a string
    css = """
    <style>
        .home-header {
            font-size: 28px;
            font-weight: bold;
            color: #e91e63;
            border-bottom: 3px solid #e91e63;
            padding-bottom: 10px;
            margin-top: 20px;
        }
        .home-content {
            font-size: 16px;
            color: #212121;
            margin-top: 10px;
            line-height: 1.6;
        }
        .home-section {
            margin-bottom: 40px;
        }
        .subheader {
            color: #f06292;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            border-left: 5px solid #f06292;
            padding-left: 10px;
        }
        .subsubheader {
            color: #ff80ab;
            font-size: 20px;
            font-weight: bold;
            margin-top: 15px;
            border-left: 3px solid #ff80ab;
            padding-left: 8px;
        }
        .content {
            font-size: 16px;
            margin-top: 10px;
            color: #212121;
            line-height: 1.6;
        }
        .content ul {
            margin-left: 20px;
        }
    </style>
    """

    # Inject CSS with Markdown
    st.markdown(css, unsafe_allow_html=True)

    st.markdown('<div class="home-header">💡 Our Project</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-content">
    Our objective is to develop AI software that takes structured data from radiology reports,
    clinical data, and pathological data to predict whether patients have experienced lymph node
    metastasis, to improve the preoperative diagnosis of axillary lymph node (ALN) metastasis
    in breast cancer patients.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="subheader">📋 Methodology</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="content">
    <b>1. Data Collection</b>: Data from radiology reports, clinical data, and pathological data are collected.<br>
    - Example of clinical data: gender, age, body mass index (BMI), history of surgery, and tumour location.<br>
    <b>2. Data Pre-processing</b>: Processing the obtained data.<br>
    <b>3. Feature Extraction</b>: Selecting the effective features based on correlation measures.<br>
    <b>4. Training, Testing, and Validating the model</b>.<br>
    <b>5. Make Prediction</b>: Using the model to make predictions.<br>
    <b>6. Evaluation of Model</b>: Using metrics like accuracy and F1 scores.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-header">📘 About This Site</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-content">
    This website is dedicated to raising awareness about metastatic breast cancer.
    Here, you will find educational content, general statistics, ongoing awareness campaigns,
    and answers to frequently asked questions. Our goal is to provide reliable information and support
    to those affected by metastatic breast cancer.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-header">🌟 Featured Content</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-content">
    - <b>Educational Content</b>: Learn about the causes, symptoms, and treatment options for metastatic breast cancer.<br>
    - <b>General Statistics</b>: Explore the latest statistics and data on metastatic breast cancer.<br>
    - <b>Awareness Campaigns</b>: Join us in our ongoing efforts to raise awareness and support research.<br>
    - <b>Frequently Asked Questions</b>: Find answers to common questions about metastatic breast cancer.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-header">🙌 Get Involved</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-content">
    Join us in our mission to spread awareness about metastatic breast cancer.
    Participate in our campaigns, share your story, or sign up for our newsletter to stay updated on the latest news and events.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-header">🎗️ Join Our Awareness Campaign</div>', unsafe_allow_html=True)
    image_url = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/DALL%C2%B7E%202024-05-19%2020.22.33%20-%20A%20visually%20appealing%20homepage%20for%20a%20cancer%20awareness%20website%20focusing%20on%20metastatic%20breast%20cancer.%20The%20design%20should%20include%20a%20warm%20and%20welcoming%20feel.ong.webp"
    st.image(image_url, caption='Join Our Awareness Campaign')

    st.markdown('<div class="home-header">📰 Latest News</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-content">
    Stay updated with the latest news and developments in the field of metastatic breast cancer. Our news section features recent research findings, new treatment options, and updates on awareness campaigns.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-header">💡 Support Resources</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-content">
    Access a variety of support resources, including counseling services, support groups, and educational materials. These resources are designed to help patients and their families navigate the challenges of living with metastatic breast cancer.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-header">📞 Contact Us</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-content">
    Have questions or need more information? Contact us through our website, email, or phone. We are here to provide you with the support and information you need.
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.title("Menu")

    # Define dictionary to map emoji labels to their corresponding sections
    options = {
        "📚 Educational Content": "educational",
        "📊 General Statistics": "statistics",
        "🎗️ Awareness Campaigns": "campaigns",
        "💬 Frequently Asked Questions": "Frequently Asked Questions"
    }

    # Sidebar buttons with emojis
    if st.sidebar.button("📚 Educational Content"):
        set_session_state(options, "educational")
    if st.sidebar.button("📊 General Statistics"):
        set_session_state(options, "statistics")
    if st.sidebar.button("🎗️ Awareness Campaigns"):
        set_session_state(options, "campaigns")
    if st.sidebar.button("💬 Frequently Asked Questions"):
        set_session_state(options, "Frequently Asked Questions")

    if "educational" in st.session_state:
        # CSS to inject contained in a string
        css = """
        <style>
            .header {
                color: #e91e63;
                font-size: 28px;
                font-weight: bold;
                margin-top: 20px;
                border-bottom: 3px solid #e91e63;
                padding-bottom: 10px;
            }
            .subheader {
                color: #f06292;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                border-left: 5px solid #f06292;
                padding-left: 10px;
            }
            .subsubheader {
                color: #ff80ab;
                font-size: 20px;
                font-weight: bold;
                margin-top: 15px;
                border-left: 3px solid #ff80ab;
                padding-left: 8px;
            }
            .content {
                font-size: 16px;
                margin-top: 10px;
                color: #212121;
                line-height: 1.6;
            }
            .content ul {
                margin-left: 20px;
            }
        </style>
        """

        # Inject CSS with Markdown
        st.markdown(css, unsafe_allow_html=True)

        st.markdown('<div class="header">📘 Educational Content</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">🧠 Intro about Metastatic Breast Cancer</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Metastatic breast cancer, often referred to as stage IV or advanced breast cancer, is a formidable adversary in the realm of oncology. This aggressive form of cancer occurs when breast cancer cells spread beyond the breast and nearby lymph nodes to other organs in the body, such as the bones, lungs, liver, or brain. Unlike localized breast cancer, where the disease is confined to the breast or nearby lymph nodes, metastatic breast cancer poses significant challenges in terms of diagnosis, treatment, and management. Despite advancements in medical science, metastatic breast cancer remains incurable, emphasizing the critical need for ongoing research, improved treatment modalities, and enhanced support systems for those living with this chronic condition.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subheader">🩺 Sentinel Lymph Node Biopsy (SLNB) in Breast Cancer</div>', unsafe_allow_html=True)
        st.markdown('<div class="subsubheader">🔍 Why is SLNB performed?</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">SLNB helps in determining the stage of breast cancer and aids in treatment planning. It helps in avoiding the removal of unnecessary lymph nodes, reducing the risk of complications such as lymphedema.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">📝 Procedure</div>', unsafe_allow_html=True)
        st.markdown('<div class="content"><ul><li>Preoperative preparation: The patient may receive anesthesia before the procedure.</li><li>Injection of tracer: A tracer material, often a radioactive substance or blue dye, is injected into the area around the tumor.</li><li>Mapping of sentinel lymph nodes: The tracer material travels through the lymphatic channels to the sentinel lymph node(s), which are then identified by the surgeon.</li><li>Biopsy: The surgeon removes the identified sentinel lymph node(s) for examination under a microscope.</li></ul></div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">⚠️ Risks and complications</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Although SLNB is generally safe, there are some risks, including infection, bleeding, and lymphedema. It is important to discuss the benefits and risks of SLNB with your healthcare provider.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subheader">🌐 What is metastatic breast cancer (MBC)?</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">MBC (also called stage IV or advanced breast cancer) is breast cancer that has spread beyond the breast to other organs in the body (most often the bones, lungs, liver, or brain). Both women and men can be diagnosed with MBC.</div>', unsafe_allow_html=True)

        # Adding more information specific to Egypt
        st.markdown('<div class="subheader">🇪🇬 Breast Cancer Awareness and Treatment in Egypt</div>', unsafe_allow_html=True)
        st.markdown('<div class="subsubheader">🏥 Awareness Campaigns</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">In Egypt, numerous awareness campaigns are organized annually to educate the public about breast cancer, its early detection, and the importance of regular screenings. The Egyptian Ministry of Health, along with various NGOs and medical institutions, plays a significant role in these initiatives.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">🔬 Research and Treatment Facilities</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Egypt is home to several specialized cancer treatment centers, such as the National Cancer Institute (NCI) in Cairo, which offers comprehensive care for breast cancer patients, including advanced diagnostic tools, treatment options, and research programs.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">📈 Statistics</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">According to the latest statistics, breast cancer is the most common cancer among women in Egypt. Efforts to improve early detection and treatment have led to better outcomes for many patients. However, ongoing education and support are crucial to further reduce mortality rates.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">🤝 Support Groups</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Support groups and counseling services are available to help patients and their families cope with the emotional and psychological impact of breast cancer. These groups provide a platform for sharing experiences and gaining strength from others who are facing similar challenges.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">💡 Early Detection and Screening</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Early detection of breast cancer significantly improves the chances of successful treatment. In Egypt, there are numerous facilities that offer mammograms and other screening services. Women are encouraged to undergo regular screenings, especially if they have a family history of breast cancer.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">🌍 Community Outreach Programs</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Various community outreach programs are conducted in rural and urban areas to raise awareness about breast cancer. These programs include educational workshops, free screening camps, and distribution of informational materials to educate women about the importance of early detection and self-examinations.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">🎗️ Notable Organizations</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Several notable organizations in Egypt are dedicated to the fight against breast cancer. These include the Breast Cancer Foundation of Egypt (BCFE) and Baheya Foundation, which provide support, education, and treatment to breast cancer patients. They also engage in extensive research and advocacy efforts.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">🚑 Treatment Options in Egypt</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">In Egypt, treatment options for breast cancer include surgery, chemotherapy, radiation therapy, and hormone therapy. Advanced treatment facilities and specialized oncologists are available in major cities like Cairo and Alexandria, providing patients with access to comprehensive cancer care.</div>', unsafe_allow_html=True)

        st.markdown('<div class="subsubheader">💬 Personal Stories</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Personal stories from breast cancer survivors in Egypt are shared through various platforms to inspire and provide hope to those currently battling the disease. These stories highlight the importance of early detection, support networks, and perseverance in overcoming challenges.</div>', unsafe_allow_html=True)

    if "statistics" in st.session_state:
        css = """
        <style>
            .home-header {
                font-size: 28px;
                font-weight: bold;
                color: #e91e63;
                border-bottom: 3px solid #e91e63;
                padding-bottom: 10px;
                margin-top: 20px;
            }
            .home-content {
                font-size: 16px;
                color: #212121;
                margin-top: 10px;
                line-height: 1.6;
            }
            .home-section {
                margin-bottom: 40px;
            }
            .subheader {
                color: #f06292;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                border-left: 5px solid #f06292;
                padding-left: 10px;
            }
            .subsubheader {
                color: #ff80ab;
                font-size: 20px;
                font-weight: bold;
                margin-top: 15px;
                border-left: 3px solid #ff80ab;
                padding-left: 8px;
            }
            .content {
                font-size: 16px;
                margin-top: 10px;
                color: #212121;
                line-height: 1.6;
            }
            .content ul {
                margin-left: 20px;
            }
        </style>
        """

        # Inject CSS with Markdown
        st.markdown(css, unsafe_allow_html=True)

        st.markdown('<div class="home-header">📊 SLNB Statistics</div>', unsafe_allow_html=True)

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

        st.markdown('<div class="subheader">📅 SLNB Procedures by Year</div>', unsafe_allow_html=True)
        fig_pie = px.pie(slnb_df, values='SLNB Procedures', names='Year', title='SLNB Procedures by Year')
        fig_pie.update_layout(width=500, height=500)
        st.plotly_chart(fig_pie)

        # Define the percentages
        initial_metastatic_percentage = 8  # 6-10% of new cases
        future_metastatic_percentage = 25  # 20-30% of all cases
        survival_percentage = 15  # Survival rate for at least five years after diagnosis with MBC

        # Create pie charts
        fig1, ax1 = plt.subplots(figsize=(3, 3))
        ax1.pie([initial_metastatic_percentage, 100 - initial_metastatic_percentage],
                labels=["Initially Stage IV or Metastatic", "Other Stages"],
                autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])
        ax1.axis('equal')

        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.pie([future_metastatic_percentage, 100 - future_metastatic_percentage],
                labels=["Estimated Future Metastatic", "Non-Metastatic"],
                autopct='%1.1f%%', startangle=90, colors=['orange', 'lightgreen'])
        ax2.axis('equal')

        fig3, ax3 = plt.subplots(figsize=(4, 4))
        ax3.pie([survival_percentage, 100 - survival_percentage],
                labels=["Survival Rate (>5 years)", "Non-Survival Rate"],
                autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightgreen'],
                textprops={'fontsize': 12})
        ax3.axis('equal')

        # Display the charts using Streamlit
        st.markdown('<div class="subheader">📈 Proportion of New Breast Cancer Cases</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Proportion of new breast cancer cases that are initially Stage IV or metastatic:</div>', unsafe_allow_html=True)
        st.pyplot(fig1)

        st.markdown('<div class="subheader">📉 Estimated Future Metastatic Cases</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Estimated percentage of all breast cancer cases that will become metastatic:</div>', unsafe_allow_html=True)
        st.pyplot(fig2)

        st.markdown('<div class="subheader">🔍 Survival Rate for MBC Patients</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Survival rate for at least five years after diagnosis with MBC:</div>', unsafe_allow_html=True)
        st.pyplot(fig3)

    if "campaigns" in st.session_state:
        css = """
        <style>
            .home-header {
                font-size: 28px;
                font-weight: bold;
                color: #e91e63;
                border-bottom: 3px solid #e91e63;
                padding-bottom: 10px;
                margin-top: 20px;
            }
            .home-content {
                font-size: 16px;
                color: #212121;
                margin-top: 10px;
                line-height: 1.6;
            }
            .home-section {
                margin-bottom: 40px;
            }
            .subheader {
                color: #f06292;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                border-left: 5px solid #f06292;
                padding-left: 10px;
            }
            .subsubheader {
                color: #ff80ab;
                font-size: 20px;
                font-weight: bold;
                margin-top: 15px;
                border-left: 3px solid #ff80ab;
                padding-left: 8px;
            }
            .content {
                font-size: 16px;
                margin-top: 10px;
                color: #212121;
                line-height: 1.6;
            }
            .content ul {
                margin-left: 20px;
            }
        </style>
        """

        # Inject CSS with Markdown
        st.markdown(css, unsafe_allow_html=True)

        st.markdown('<div class="home-header">🎗️ Awareness Campaigns</div>', unsafe_allow_html=True)

        st.markdown('<div class="subheader">1. لكل نجاح حكاية وأنتي بداية الحكاية</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="content">
        Join us in our mission to spread awareness about breast cancer and the importance of early detection. Our campaign "لكل نجاح حكاية وأنتي بداية الحكاية" focuses on empowering women to take proactive steps in their health journey. 
        </div>
        """, unsafe_allow_html=True)
        image_url_0 = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/baheya1.jpeg"
        st.image(image_url_0, caption='Join Our Awareness Campaign')

        st.markdown('<div class="subheader">2. سعادتنا مش هتكتمل غير بيكي.. خليكي وسطنا</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="content">
        Our campaign "سعادتنا مش هتكتمل غير بيكي.. خليكي وسطنا" highlights the vital role women play in our lives and communities. This initiative aims to encourage women to prioritize their health by participating in regular screenings and supporting each other in the fight against breast cancer.
        </div>
        """, unsafe_allow_html=True)
        image_url_1 = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/baheya2.jpeg"
        st.image(image_url_1, caption='Join Our Awareness Campaign')

        st.markdown('<div class="subheader">3. متنسيش نفسك واعلمي الكشف المبكر</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="content">
        Our campaign "متنسيش نفسك واعلمي الكشف المبكر" emphasizes the importance of regular check-ups and early detection. Early detection can save lives by identifying breast cancer at a more treatable stage.
        </div>
        """, unsafe_allow_html=True)
        image_url_2 = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/baheya 3.jpeg"
        st.image(image_url_2, caption='Join Our Awareness Campaign')
    if "Frequently Asked Questions" in st.session_state:
                
            # CSS to inject contained in a string
        css = """
        <style>
            .home-header {
                font-size: 28px;
                font-weight: bold;
                color: #e91e63;
                border-bottom: 3px solid #e91e63;
                padding-bottom: 10px;
                margin-top: 20px;
            }
            .home-content {
                font-size: 16px;
                color: #212121;
                margin-top: 10px;
                line-height: 1.6;
            }
            .home-section {
                margin-bottom: 40px;
            }
            .subheader {
                color: #f06292;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                border-left: 5px solid #f06292;
                padding-left: 10px;
            }
            .subsubheader {
                color: #ff80ab;
                font-size: 20px;
                font-weight: bold;
                margin-top: 15px;
                border-left: 3px solid #ff80ab;
                padding-left: 8px;
            }
            .content {
                font-size: 16px;
                margin-top: 10px;
                color: #212121;
                line-height: 1.6;
            }
            .content ul {
                margin-left: 20px;
            }
            .faq-header {
                font-size: 28px;
                font-weight: bold;
                color: #e91e63;
                border-bottom: 3px solid #e91e63;
                padding-bottom: 10px;
                margin-top: 20px;
            }
            .faq-content {
                font-size: 16px;
                color: #212121;
                margin-top: 10px;
                line-height: 1.6;
            }
            .faq-question {
                font-size: 20px;
                font-weight: bold;
                color: #f06292;
                margin-top: 15px;
                border-left: 3px solid #f06292;
                padding-left: 10px;
            }
            .expander-label::after {
                content: "Show";
                color: #f06292;
            }
        </style>
        """

        # Inject CSS with Markdown
        st.markdown(css, unsafe_allow_html=True)

        st.markdown('<div class="home-header">💬 Frequently Asked Questions</div>', unsafe_allow_html=True)

        # Define the FAQ list
        faq_list = {
            "🧠 What are signs and symptoms of MBC?": [
                "• Severe and persistent headache",
                "• Bone pain and fracture",
                "• Shortness of breath",
                "• Abdominal bloating, pain, or swelling",
                "• Constant nausea, vomiting, or weight loss",
                "• Numbness or weakness anywhere in your body and confusion",
                "• Loss of appetite",
                "• Vision problems (blurry vision, double vision, loss of vision)",
                "• Loss of balance"
            ],
            "🏥 Seeking Physicians Help": [
                "If you notice any of the above symptoms, it's crucial to seek medical attention promptly. Physicians can provide an accurate diagnosis and recommend appropriate treatment options."
            ],
            "💊 Common Treatment Options": [
                "Treatment options for metastatic breast cancer may include systemic therapies such as chemotherapy, hormonal therapy, targeted therapy, and immunotherapy. Treatment plans are personalized based on the individual's specific condition and medical history."
            ],
            "📅 How often should I get screened for breast cancer?": [
                "It is recommended that women begin annual mammograms at age 40. However, women with a family history of breast cancer or other risk factors may need to start earlier. Always consult with your healthcare provider to determine the best screening schedule for you."
            ],
            "🧬 What are the risk factors for breast cancer?": [
                "• Gender: Women are much more likely than men to develop breast cancer.",
                "• Age: The risk of breast cancer increases as you age.",
                "• Family history: A family history of breast cancer increases your risk.",
                "• Genetic mutations: Inherited mutations in genes such as BRCA1 and BRCA2.",
                "• Personal health history: Having had breast cancer or certain non-cancerous breast diseases.",
                "• Lifestyle factors: Obesity, alcohol consumption, and lack of physical activity."
            ],
            "🏋️‍♀️ Can lifestyle changes reduce the risk of breast cancer?": [
                "Yes, lifestyle changes can help reduce the risk of breast cancer. These include maintaining a healthy weight, staying physically active, eating a healthy diet, limiting alcohol consumption, avoiding smoking, and considering the risks of hormone replacement therapy."
            ],
            "📖 What should I know about genetic testing for breast cancer?": [
                "Genetic testing can identify mutations in genes such as BRCA1 and BRCA2, which increase the risk of breast and ovarian cancers. It is recommended for those with a family history of these cancers. Consult with a genetic counselor to understand the benefits, risks, and implications of genetic testing."
            ],
            "🔬 What is Sentinel Lymph Node Biopsy (SLNB)?": [
                "SLNB is a surgical procedure used to determine if cancer has spread beyond the breast to nearby lymph nodes. It involves removing one or a few sentinel lymph nodes to check for cancer cells."
            ],
            "❓ Why is SLNB performed?": [
                "SLNB helps in determining the stage of breast cancer and aids in treatment planning. It helps in avoiding the removal of unnecessary lymph nodes, reducing the risk of complications such as lymphedema."
            ],
            "⚙️ What is the procedure for SLNB?": [
                "<b>1. Preoperative preparation</b>: The patient may receive anesthesia before the procedure.",
                "<b>2. Injection of tracer</b>: A tracer material, often a radioactive substance or blue dye, is injected into the area around the tumor.",
                "<b>3. Mapping of sentinel lymph nodes</b>: The tracer material travels through the lymphatic channels to the sentinel lymph node(s), which are then identified by the surgeon.",
                "<b>4. Biopsy</b>: The surgeon removes the identified sentinel lymph node(s) for examination under a microscope."
            ],
            "⚠️ What are the risks and complications of SLNB?": [
                "Although SLNB is generally safe, there are some risks, including infection, bleeding, and lymphedema. It is important to discuss the benefits and risks of SLNB with your healthcare provider."
            ],
            "🩺 How do I prepare for SLNB?": [
                "Before SLNB, you may be asked to stop certain medications, avoid eating or drinking for a specified period, and arrange for someone to drive you home after the procedure. Follow your surgeon's preoperative instructions carefully."
            ]
        }

        # Display FAQs with headers and expandable answers with custom styling
        for question, answers in faq_list.items():
            st.markdown(f'<div class="faq-question">{question}</div>', unsafe_allow_html=True)
            with st.expander("Show"):
                for answer in answers:
                    st.markdown(f'<div class="faq-content">{answer}</div>', unsafe_allow_html=True)
def set_session_state(options, selected_option):
    # Reset session state
    for option in options.values():
        st.session_state.pop(option, None)
    # Set selected option in session state
    st.session_state[selected_option] = True

# Call the app function to run the app
if __name__ == "__main__":
    app()
