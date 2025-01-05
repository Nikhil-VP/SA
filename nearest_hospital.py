import streamlit as st
from utils import display_map
import uuid
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

def nearest_hospital_page():
    # Create two columns: one for the video conference and one for the patient details
    col1, col2 = st.columns([3, 1])  # 3 for video (larger width), 1 for patient details (smaller width)
    
    with col1:
        # Video Conference Placeholder
        meeting_id = str(uuid.uuid4())[:8]
        jitsi_url = f"https://meet.jit.si/{meeting_id}"
        
        # Connect to MongoDB
        uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client.PatientData
        calls_collection = db.calls
        
        # Store call information
        call_data = {
            "meeting_id": meeting_id,
            "jitsi_url": jitsi_url,
            "timestamp": datetime.now(),
            "status": "active"
        }
        calls_collection.insert_one(call_data)
        
        # Embed the video conference
        st.markdown(
            f'<iframe src="{jitsi_url}" width="100%" height="800em" allow="microphone; camera" style="border:0;"></iframe>',
            unsafe_allow_html=True
        )
    
    with col2:
        # Patient Details Section (on the right side)
        st.subheader("Patient Details")
        st.text_area("Patient Name")
        st.text_area("Medical History")
        st.text_area("Critical Point")
        st.text_area("Allergies")
    
    # Map Display below the video and patient details
    st.subheader("Nearby Hospitals")
    display_map()
