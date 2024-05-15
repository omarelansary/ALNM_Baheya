import streamlit as st
from streamlit_option_menu import option_menu
from Components.authComponents import AuthComponents
from Authentication.Authenticator import AuthExceptions
import Views.AdminDashboard, Views.AdminPatientsView
import Views.AnalystDashboard, Views.AnalystReview
import Views.DoctorDashboard, Views.DoctorPatients, Views.DoctorRiskAssesment
import  Views.Home, Views.Login
def main():
    # Perform login if not logged in
    authComponents=AuthComponents()
    app=None
    if st.session_state['is_logged_in']:
        if st.session_state['role']=='Doctor':
            app = option_menu(
            menu_title='Welcome Dr. Omar',
            options=['Home', 'Dashboard', 'Risk','My Patients','Logout'],
            icons=['house-fill', 'graph-up','exclamation-triangle-fill', 'heart-fill','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color":"white", "font-size": "23px"},
                "nav-link": {"color":"white", "font-size": "20px", "text-align":"left","margin":"0px"},
                "nav-link-selected": {"background-color": "#02ab21"},}
            )
        elif st.session_state['role']=='Data Analyst': 
            app = option_menu(
            menu_title='Welcome Analyst. Ahmed',
            options=['Home', 'Analysis', 'Review','Logout'],
            icons=['house-fill', 'bar-chart-line','binoculars','door-open'],
            menu_icon=['person-fill'],
            default_index=0,
            orientation='horizontal',
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color":"white", "font-size": "23px"},
                "nav-link": {"color":"white", "font-size": "20px", "text-align":"left","margin":"0px"},
                "nav-link-selected": {"background-color": "#02ab21"},}
            )
        elif st.session_state['role']=='Admin': 
            app = option_menu(
            menu_title='Welcome Admin. Hassan',
            options=['Home', 'Panel', 'Risk','All Patients','Analysis', 'Review','Logout'],
            icons=['house-fill', 'graph-up','exclamation-triangle-fill', 'heart-fill','bar-chart-line','binoculars','door-open'],
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
    if app=='Analysis':
       Views.AnalystDashboard.app()
    if app=='Review':
       Views.AnalystReview.app()               
    if app== 'Dashboard':
        Views.DoctorDashboard.app()    
    if app== 'Risk':
        Views.DoctorRiskAssesment.app()
    if app=='My Patients':
        Views.DoctorPatients.app()    
    if app== 'Logout':
        authComponents.logout()    



if __name__ == "__main__":
    main()