import streamlit as st
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils import display_map  # Assuming this function is for displaying maps

def history_page():
    st.title("Patient History")

    # MongoDB Connection
    uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        st.success("Pinged your deployment. You successfully connected to MongoDB!")

        # Choose the database and collection
        db = client["hospital_db"]  # Replace with your database name
        collection = db["patients"]  # Replace with your collection name

        # Fetch all patient history data
        patients = collection.find()
        
        # Create a DataFrame from the MongoDB data
        history_data = pd.DataFrame(list(patients))

        # If the DataFrame is empty, show a message
        if history_data.empty:
            st.warning("No patient history data found.")
        else:
            # Display the patient history data in a table
            st.subheader("Past Records")
            st.dataframe(history_data, use_container_width=True)

    except Exception as e:
        st.error(f"Error occurred: {e}")

    finally:
        # Close the connection to MongoDB
        client.close()

    # Map Display
    st.subheader("Map of Hospitals")
    display_map()  # Assuming display_map() is already implemented in your utils file
