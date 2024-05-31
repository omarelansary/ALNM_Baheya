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
import Views.FiltringPatientsCases
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
            menu_title="Welcome MD. " + str(userAuthData['username']),
            options=['Home', 'Dashboard', 'Follow Up', 'Patients Filters','Patients Table', 'Patient Management','Logout'],
            icons=['house', 'pie-chart', 'bar-chart-steps', 'funnel','file-spreadsheet','file-earmark-medical', 'door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"width": "100%"},
                "icon": {"color":"black", "font-size": "23px"},
                "nav-link": {"color":"black", "font-size": "20px", "text-align":"left" },
                "nav-link-selected": {"background-color": "#ff9cbc"},}
            )
        elif userAuthData['role']=='Data Analyst': 
            app = option_menu(
            menu_title='Welcome Analyst, ' + str(userAuthData['username']),
            options=['Home', 'Analysis', 'Correlations', 'Review','Logout'],
            icons=['house', 'bar-chart-line','graph-up','binoculars','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"width": "100%"},
                "icon": {"color":"black", "font-size": "23px"},
                "nav-link": {"color":"black", "font-size": "20px", "text-align":"left" },
                "nav-link-selected": {"background-color": "#ff9cbc"},}
            )
        elif userAuthData['role']=='Admin': 
            app = option_menu(
            menu_title='Welcome Admin, '+ str(userAuthData['username']),
            options=['Home', 'Panel', 'Add Head Physician','Add Analyst','Logout'],
            icons=['house', 'layout-sidebar', 'person-plus','person-rolodex','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"width": "100%"},
                "icon": {"color":"black", "font-size": "23px"},
                "nav-link": {"color":"black", "font-size": "20px", "text-align":"left" },
                "nav-link-selected": {"background-color": "#ff9cbc"},}
            )
        elif userAuthData['role']=='Head Doctor':
            app = option_menu(
            menu_title='Welcome Head MD. '+ str(userAuthData['username']),
            options=['Home','Dashboard','Head Dashboard', 'Patients Filters','Patients Table', 'Add Physician','Logout'],
            icons=['house','pie-chart','clipboard2-pulse', 'funnel','file-spreadsheet','person-plus','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"width": "100%"},
                "icon": {"color":"black", "font-size": "23px"},
                "nav-link": {"color":"black", "font-size": "20px", "text-align":"left" },
                "nav-link-selected": {"background-color": "#ff9cbc"},}
            )            
    else:    
        app = option_menu(
          menu_title=None,
          options=['Home', 'Login'],
          icons=['house', 'box-arrow-in-right'],
          default_index=0,
          orientation='horizontal',
          styles={
            "container": {"width": "100%"},
            "icon": {"color":"black", "font-size": "23px"},
            "nav-link": {"color":"black", "font-size": "20px", "text-align":"left" },
            "nav-link-selected": {"background-color": "#ff9cbc"},}
        )

    if app== 'Home':
        Views.Home.app()
    if app== 'Login':
        Views.Login.app(authComponents)
    if app== 'Panel':
       Views.AdminDashboard.app()
    if app== 'All Patients':
       Views.AdminPatientsView.app() 
    if app=='Add Physician':
        Views.AdminAddDoctor.app() 
    if app=='Add Analyst':
       Views.AdminAddAnalyst.app()
    if app=='Add Head Physician':
       Views.AdminAddHeadDoctor.app()             
    if app=='Analysis':
       Views.AnalystDashboard.app()
    if app=='Review':
       Views.AnalystReview.app() 
    if app=='Correlations':
       Views.AnalystCorrelationGraphs.app()                  
    if app== 'Dashboard':
        Views.DoctorDashboard.app()    
    if app== 'Patient Management':
        Views.DoctorRiskAssesment.app(userAuthData)
    if app=='Patients Table':
        Views.DoctorPatients.app(userAuthData)
    if app=='Patients Filters':
        Views.FiltringPatientsCases.app(userAuthData)        
    if app=='Follow Up':
        Views.DoctorGantChart.app() 
    if app=='Head Dashboard':
        Views.HeadDoctorDashboard.app()
    if app== 'Logout':
        authComponents.logout()    



if __name__ == "__main__":
    main()