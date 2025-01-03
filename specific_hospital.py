import streamlit as st
from utils import display_map

def specific_hospital_page():
    st.title("Specific Hospital")
    
    # Input fields for hospital and doctor search
    st.text_input("Type hospital name", placeholder="Search for a hospital")
    st.text_input("Type doctor name", placeholder="Search for a doctor")
    
    # Patient Details
    st.subheader("Patient Details")
    st.text_area("Patient Name")
    st.text_area("Medical History")
    st.text_area("Critical Point")
    st.text_area("Diagnosis")
    
    # Map Display
    st.subheader("Map of Hospitals")
    display_map()
