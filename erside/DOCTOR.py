import streamlit as st
from pymongo import MongoClient
import home
import call_history
import patient_data


# MongoDB URI
uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"

# Sidebar Buttons for Navigation
st.sidebar.title("Navigation")

# Use session state to manage the active page
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# Sidebar Buttons
if st.sidebar.button("Home"):
    st.session_state.active_page = "Home"

if st.sidebar.button("Call History"):
    st.session_state.active_page = "Call History"

if st.sidebar.button("Patient Data"):
    st.session_state.active_page = "Patient Data"

# Render the selected page
if st.session_state.active_page == "Home":
    home.home_page()
elif st.session_state.active_page == "Call History":
    call_history.call_history_page()
elif st.session_state.active_page == "Patient Data":
    patient_data.patient_data_page()
