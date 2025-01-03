import streamlit as st
from nearest_hospital import nearest_hospital_page
from specific_hospital import specific_hospital_page 
def home_page():
    
    
    # Buttons for navigation
    nearest_hospital_button = st.button("Connect to Nearest Hospital")
    specific_hospital_button = st.button("Connect to Specific Hospital")
    
    # Set the page navigation flag based on the button clicked
    if nearest_hospital_button:
        
        nearest_hospital_page()
    
    elif specific_hospital_button:
       specific_hospital_page()