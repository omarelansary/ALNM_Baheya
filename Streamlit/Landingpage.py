import streamlit as st

import Views.HeadDoctorDashboard
st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
from Components.authComponents import AuthComponents
from Authentication.Authenticator import AuthExceptions
import Views.AdminDashboard, Views.AdminPatientsView
import Views.AdminAddAnalyst, Views.AdminAddDoctor, Views.AdminAddHeadDoctor
import Views.AnalystDashboard, Views.AnalystReview, Views.AnalystDashboard, Views.AnalystCorrelationGraphs
import Views.DoctorDashboard, Views.DoctorPatients, Views.DoctorRiskAssesment
import Views.DoctorGantChart
import  Views.Home, Views.Login
def main():
    # Perform login if not logged in
    authComponents=AuthComponents()
    app=None
    userAuthData=authComponents.check_cookie_session()
    #st.session_state['is_logged_in']
    if userAuthData or st.session_state['is_logged_in']:
        userAuthData=authComponents.check_cookie_session()
        if userAuthData['role']=='Physician':
            app = option_menu(
            menu_title="Welcome Dr. " + str(userAuthData['username']),
            options=['Home', 'Follow Up', 'Patients Table','Dashboard', 'Data Entry','Logout'],
            icons=['house-fill', 'bar-chart-steps','person','graph-up','file-earmark-medical', 'door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color":"white", "font-size": "23px"},
                "nav-link": {"color":"white", "font-size": "20px", "text-align":"left","margin":"0px"},
                "nav-link-selected": {"background-color": "#02ab21"},}
            )
        elif userAuthData['role']=='Data Analyst': 
            app = option_menu(
            menu_title='Welcome Analyst, ' + str(userAuthData['username']),
            options=['Home', 'Analysis', 'Correlations', 'Review','Logout'],
            icons=['house-fill', 'bar-chart-line','clipboard2-pulse-fill','binoculars','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color":"white", "font-size": "23px"},
                "nav-link": {"color":"white", "font-size": "20px", "text-align":"left","margin":"0px"},
                "nav-link-selected": {"background-color": "#02ab21"},}
            )
        elif userAuthData['role']=='Admin': 
            app = option_menu(
            menu_title='Welcome Admin, '+ str(userAuthData['username']),
            options=['Home', 'Panel', 'All Patients','Analysis', 'Correlations', 'Review', 'Add Head Doctor','Add Analyst','Logout'],
            icons=['house-fill', 'graph-up', 'people','bar-chart-line','clipboard2-pulse-fill','binoculars','person-plus','person-plus-fill','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color":"white", "font-size": "23px"},
                "nav-link": {"color":"white", "font-size": "20px", "text-align":"left","margin":"0px"},
                "nav-link-selected": {"background-color": "#02ab21"},}
            )
        elif userAuthData['role']=='Head Doctor':
            app = option_menu(
            menu_title='Welcome Head Dr. '+ str(userAuthData['username']),
            options=['Home', 'All Patients','Patients Table','Dashboard','Head Dashboard', 'Add Doctor','Logout'],
            icons=['house-fill', 'people','person','graph-up','clipboard2-pulse','person-plus','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color":"white", "font-size": "23px"},
                "nav-link": {"color":"white", "font-size": "20px", "text-align":"left","margin":"0px"},
                "nav-link-selected": {"background-color": "#02ab21"},}
            )            
    else:    
        app = option_menu(
          menu_title=None,
          options=['Home', 'Login'],
          icons=['house-fill', 'box-arrow-in-right'],
          default_index=0,
          orientation='horizontal',
          styles={
            "container": {"padding": "5!important", "background-color": "black"},
            "icon": {"color":"white", "font-size": "23px"},
            "nav-link": {"color":"white", "font-size": "20px", "text-align":"left","margin":"0px"},
            "nav-link-selected": {"background-color": "#02ab21"},}
        )

    if app== 'Home':
        Views.Home.app()
    if app== 'Login':
        Views.Login.app(authComponents)
    if app== 'Panel':
       Views.AdminDashboard.app()
    if app== 'All Patients':
       Views.AdminPatientsView.app() 
    if app=='Add Doctor':
        Views.AdminAddDoctor.app() 
    if app=='Add Analyst':
       Views.AdminAddAnalyst.app()
    if app=='Add Head Doctor':
       Views.AdminAddHeadDoctor.app()             
    if app=='Analysis':
       Views.AnalystDashboard.app()
    if app=='Review':
       Views.AnalystReview.app() 
    if app=='Correlations':
       Views.AnalystCorrelationGraphs.app()                  
    if app== 'Dashboard':
        Views.DoctorDashboard.app()    
    if app== 'Data Entry':
        Views.DoctorRiskAssesment.app(userAuthData)
    if app=='Patients Table':
        Views.DoctorPatients.app(userAuthData)    
    if app=='Follow Up':
        Views.DoctorGantChart.app() 
    if app=='Head Dashboard':
        Views.HeadDoctorDashboard.app()
    if app== 'Logout':
        authComponents.logout()    



if __name__ == "__main__":
    main()