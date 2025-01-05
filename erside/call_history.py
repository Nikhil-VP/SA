import streamlit as st
import pandas as pd
from pymongo import MongoClient

def call_history_page():
    st.title("Call History")
    
    # Connect to MongoDB
    uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
    client = MongoClient(uri)
    db = client.PatientData
    calls_collection = db.calls

    # Fetch call history data from MongoDB
    call_history_data = pd.DataFrame(list(calls_collection.find()))
    st.dataframe(call_history_data, use_container_width=True)
