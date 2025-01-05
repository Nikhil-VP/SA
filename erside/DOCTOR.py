import streamlit as st
from pymongo import MongoClient
import home
import call_history
import patient_data

# MongoDB URI
uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
# Connect to MongoDB
client = MongoClient(uri)
db = client["PatientData"]  # Database name
collection = db["patients"]
st.set_page_config(page_title="Hospital ER Doctor", layout="wide")

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

# Initialize session state for search results
if "patient_details" not in st.session_state:
    st.session_state.patient_details = None

st.sidebar.subheader("View patient data")
search = st.sidebar.radio("Search by data:", ["UHID", "Patient Name"])

if search == "UHID":
    search1_uhid = st.sidebar.text_input("Enter UHIDs", placeholder="e.g., 20240319-8f3a")
    if st.sidebar.button("Search in database"):
        # Query the database for patient data using UHID
        patient = collection.find_one({"UHID": search1_uhid})
        if patient:
            st.session_state.patient_details = {
                "UHID": patient['UHID'],
                "Name": patient['name'],
                "Medical History": patient['medical_history'],
                "Critical Point": patient['critical_point'],
                "Allergies": patient['allergies']
            }
        else:
            st.session_state.patient_details = None
            st.sidebar.error("Patient not found.")

else:  # Search by Patient Name
    search1_name = st.sidebar.text_input("Search Patient Names", placeholder="Enter patient name")
    if st.sidebar.button("Search in database"):
        # Query the database for patient data using name
        patient = collection.find_one({"name": search1_name})
        if patient:
            st.session_state.patient_details = {
                "UHID": patient['UHID'],
                "Name": patient['name'],
                "Medical History": patient['medical_history'],
                "Critical Point": patient['critical_point'],
                "Allergies": patient['allergies']
            }
        else:
            st.session_state.patient_details = None
            st.sidebar.error("Patient not found.")

# Display patient details if available
if st.session_state.patient_details:
    st.sidebar.markdown("### Patient Details")
    for key, value in st.session_state.patient_details.items():
        st.sidebar.write(f"**{key}**: {value}")

# Render the selected page
if st.session_state.active_page == "Home":
    home.home_page()
elif st.session_state.active_page == "Call History":
    call_history.call_history_page()
elif st.session_state.active_page == "Patient Data":
    patient_data.patient_data_page()
