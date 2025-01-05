import streamlit as st
from utils import check_for_call, update_call_status
from patient_data import collection  # Import MongoDB collection
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

def home_page():
    # Connect to MongoDB
    uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.PatientData
    calls_collection = db.calls

    # Fetch recent call information
    call_info = calls_collection.find_one({"status": "active"}, sort=[("timestamp", -1)])  # Get the most recent active call

    # Initialize session state
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = None
    if 'search_clicked' not in st.session_state:
        st.session_state.search_clicked = False

    # Display Connect Button
    if call_info:
        
        # Ensure jitsi_url is available
        jitsi_url = call_info.get('jitsi_url', None)
        if jitsi_url:
            if st.button("Connect"):
                # Update call status to active
                update_call_status(call_info['_id'], "active")
                
                # Create two columns for video and patient data
                    # Video conference implementation
                st.markdown(
                        f'<iframe src="{jitsi_url}" width="100%" height="800em" allow="microphone; camera" style="border:0;"></iframe>',
                        unsafe_allow_html=True
                    )
                st.info("You are now connected to the call.")
                
                
        else:
            st.error("No video conference URL available.")
    else:
        st.warning("No calls available right now.")
