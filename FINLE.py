import streamlit as st
from home import home_page
from nearest_hospital import nearest_hospital_page
from history import history_page
from specific_hospital import specific_hospital_page
from utils import display_map
from pymongo import MongoClient
# MongoDB URI
uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
# Connect to MongoDB
client = MongoClient(uri)
db = client["PatientData"]  # Database name
collection = db["patients"]
# ----------------- Main App -----------------
st.set_page_config(page_title="Hospital Navigation App", layout="wide")
st.title("Hospital Navigation System")

# Sidebar for Navigation using Buttons
home_button = st.sidebar.button("Home")
navigate_button = st.sidebar.button("Navigation")
history_button = st.sidebar.button("History")
language = st.sidebar.selectbox("Select Language", ["English", "Hindi", "Spanish", "French"])

# Display a message based on the selected language
if language == "English":
    st.write("Welcome to the Hospital Navigation system in english")
elif language == "Hindi":
    st.write("अस्पताल नेविगेशन सिस्टम में आपका स्वागत है।")
elif language == "Spanish":
    st.write("Bienvenido al sistema de navegación hospitalaria en español.")
elif language == "French":
    st.write("Bienvenue dans le système de navigation hospitalière en français.")


# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "home"


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



# Page Selection Logic based on buttons clicked
if home_button:
    st.session_state.page = 'home'
elif navigate_button:
    st.session_state.page = 'navigate'
elif history_button:
    st.session_state.page = 'history'

# Display content based on selected page
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'navigate':
    display_map()
elif st.session_state.page == 'history':
    history_page()

# Footer
st.markdown("---")
