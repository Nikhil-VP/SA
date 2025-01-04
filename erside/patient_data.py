import streamlit as st
from pymongo import MongoClient
import uuid
from datetime import datetime

# MongoDB URI
uri = "mongodb+srv://DTL:1234@patientdata.xxxos.mongodb.net/?retryWrites=true&w=majority&appName=Patientdata"

# Connect to MongoDB
client = MongoClient(uri)
db = client["PatientData"]  # Database name
collection = db["patients"]  # Collection name

def generate_uhid():
    # Generate a timestamp-based prefix (YYYYMMDD)
    timestamp = datetime.now().strftime('%Y%m%d')
    # Generate a random 4-character string
    random_suffix = str(uuid.uuid4())[:4]
    # Combine them to create a UHID (e.g., "20240319-8f3a")
    return f"{timestamp}-{random_suffix}"

def patient_data_page():
    st.title("Patient Data")
    
    # Options for viewing or filling patient data
    choice = st.radio("Choose an option:", ["View Patient Data", "Fill Patient Data"])
    
    if choice == "View Patient Data":
        st.subheader("View Patient Data")
        search_option = st.radio("Search by:", ["UHID", "Patient Name"])
        
        if search_option == "UHID":
            search_uhid = st.text_input("Enter UHID", placeholder="e.g., 20240319-8f3a")
            if st.button("Search"):
                # Query the database for patient data using UHID
                patient = collection.find_one({"UHID": search_uhid})
                if patient:
                    st.markdown("### Patient Details")
                    st.write(f"**UHID**: {patient['UHID']}")
                    st.write(f"**Name**: {patient['name']}")
                    st.write(f"**Medical History**: {patient['medical_history']}")
                    st.write(f"**Critical Point**: {patient['critical_point']}")
                    st.write(f"**Allergies**: {patient['allergies']}")
                else:
                    st.error("Patient not found.")
        
        else:  # Search by Patient Name
            search_name = st.text_input("Search Patient Name", placeholder="Enter patient name")
            if st.button("Search"):
                # Query the database for patient data using name
                patient = collection.find_one({"name": search_name})
                if patient:
                    st.markdown("### Patient Details")
                    st.write(f"**UHID**: {patient['UHID']}")
                    st.write(f"**Name**: {patient['name']}")
                    st.write(f"**Medical History**: {patient['medical_history']}")
                    st.write(f"**Critical Point**: {patient['critical_point']}")
                    st.write(f"**Allergies**: {patient['allergies']}")
                else:
                    st.error("Patient not found.")
    
    elif choice == "Fill Patient Data":
        st.subheader("Fill Patient Data")
        
        name = st.text_input("Patient Name", placeholder="Enter name")
        medical_history = st.text_area("Medical History", placeholder="Enter medical history")
        critical_point = st.text_area("Critical Point", placeholder="Enter critical point")
        allergies = st.text_area("Allergies", placeholder="Enter allergies")
        identity = generate_uhid()  # Generate UHID automatically
        
        # Display the generated UHID
        st.text(f"Generated UHID: {identity}")
        
        if st.button("Submit"):
            # Insert data into the MongoDB collection
            if name and medical_history and critical_point and allergies:
                patient_data = {
                    "UHID": identity,
                    "name": name,
                    "medical_history": medical_history,
                    "critical_point": critical_point,
                    "allergies": allergies
                }
                collection.insert_one(patient_data)
                st.success("Patient data has been saved successfully!")
            else:
                st.error("Please fill in all fields before submitting.")
