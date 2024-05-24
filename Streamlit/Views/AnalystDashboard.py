import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import altair as alt
from ourData.cache import LocalCache

def make_donut(input_response, input_text,color):
    chart_color = color
    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
    
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    return plot_bg + plot + text


Cache=LocalCache()

def app():
    st.title('Analyst DashBoard')
        # Load your data
    
    AUC=79
    accurcy=83
    macro=80
    micro=83
    weighted=80
    image_url_PCA_Analysis = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/PCA_Analysis.png"
    image_url_Mean_ROC_AUC_Curve2 = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/Mean_ROC_AUC_Curve2.png"
    image_url_Mean_ROC_AUC_Curve1 = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/Mean_ROC_AUC_Curve1.png"
    image_url_HMAP_NEW= "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/HMAP_NEW.png"
    image_url_confusion_matrix_last = "https://raw.githubusercontent.com/omarelansary/ALNM_Baheya/develop/Streamlit/Images/confusion_matrix_last.png"

    # st.image(image_url_HMAP_NEW)
    color = ['#E74C3C', '#781F16']
    donut_chart_Accuracy = make_donut(accurcy, 'Accuracy',color)
    donut_chart_weighted = make_donut(weighted, 'Outbound Migration',color)
    donut_chart_Macro = make_donut(macro, 'Accuracy',color)
    donut_chart_Micro = make_donut(micro, 'Outbound Migration',color)
    donut_chart_Auc = make_donut(AUC, 'Accuracy',color)
    st.markdown('Machine learning')
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.write('Accuracy')
        st.altair_chart(donut_chart_Accuracy)
    with col2:
        st.write('F1 Micro')
        st.altair_chart(donut_chart_Micro)
    with col3:
        st.write('F1 weighted')
        st.altair_chart(donut_chart_weighted)
    with col4:
        st.write('F1 Macro')
        st.altair_chart(donut_chart_Macro)
    with col5:
        st.write('Auc Score')
        st.altair_chart(donut_chart_Auc) 
    col11,col22=st.columns(2)  
    with col11:    
        st.image(image_url_Mean_ROC_AUC_Curve1)
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)

        st.image(image_url_PCA_Analysis)                 
        
    with col22:    
        st.image(image_url_Mean_ROC_AUC_Curve2) 
        st.image(image_url_confusion_matrix_last) 
    
    st.image(image_url_HMAP_NEW)
    
   