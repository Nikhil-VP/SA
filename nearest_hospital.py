import streamlit as st
from pymongo import MongoClient
from utils import display_map
from video_call import video_chat_component, create_room

# MongoDB Connection
uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
client = MongoClient(uri)
db = client["PatientData"]  # Database name
collection = db["patients"]  # Collection name

def nearest_hospital_page():
    # Create two columns: one for the video conference and one for patient details
    col1, col2 = st.columns([3, 1])

    with col1:
        # Generate a unique room ID if not already in session state
        if 'room_id' not in st.session_state:
            st.session_state.room_id = create_room()

        # Display room ID for sharing
        st.info(f"Room ID: {st.session_state.room_id}")
        
        # Initialize video chat component
        video_chat_component(st.session_state.room_id)

    with col2:
        st.subheader("Patient Details")
        
        # Input field to search for a patient using unique ID
        patient_id = st.text_input("Enter Patient ID", placeholder="Enter unique patient ID")
        
        # Search button
        if st.button("Search"):
            # Query the database for patient details using Patient ID
            patient = collection.find_one({"UHID": patient_id})
            
            if patient:
                # Display retrieved patient details
                st.write(f"**Patient Name:** {patient.get('name', 'N/A')}")
                st.write(f"**Medical History:** {patient.get('medical_history', 'N/A')}")
                st.write(f"**Critical Point:** {patient.get('critical_point', 'N/A')}")
                st.write(f"**Allergies:** {patient.get('allergies', 'N/A')}")
            else:
                st.error("Patient not found. Please check the ID and try again.")
    
    # Map Display
    st.subheader("Nearby Hospitals")
    display_map()
