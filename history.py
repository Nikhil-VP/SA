import streamlit as st
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils import display_map  # Assuming this function is for displaying maps


def history_page():
    st.title("Call History")
    
    # Connect to MongoDB
    uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
    client = MongoClient(uri)
    db = client.PatientData
    calls_collection = db.calls

    # Fetch call history data from MongoDB
    call_history_data = pd.DataFrame(list(calls_collection.find()))
    st.dataframe(call_history_data, use_container_width=True)
    # Map Display
st.subheader("Map of Hospitals")
display_map()  # Assuming display_map() is already implemented in your utils file
