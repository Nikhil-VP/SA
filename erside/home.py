import streamlit as st
from utils import check_for_call, update_call_status
from patient_data import collection  # Import MongoDB collection

def home_page():
    st.title("Home")
    
    # Initialize session state
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = None
    if 'search_clicked' not in st.session_state:
        st.session_state.search_clicked = False

    # Display Connect Button
    call_info = check_for_call()  # Now returns call document instead of just boolean
    if call_info:
        st.success(f"You have an incoming call scheduled for {call_info['scheduled_time'].strftime('%H:%M')}")
        if st.button("Connect"):
            # Update call status to active
            update_call_status(call_info['_id'], "active")
            
            # Create two columns for video and patient data
            col1, col2 = st.columns([3, 1])  # Changed from 2:1 to 3:1 ratio for more video space
            
            with col1:
                # Video conference implementation
                jitsi_url = "https://meet.jit.si/BalancedCropsAccessNor"
                st.markdown(
                    f'<iframe src="{jitsi_url}" width="150%" height="800em" allow="microphone; camera" style="border:0;"></iframe>',
                    unsafe_allow_html=True
                )
                st.info("You are now connected to the call.")
            
            with col2:
                st.subheader("Patient Details")
                # Add search functionality
                search_option = st.radio("Search by:", ["UHID", "Patient Name"])
                
                def search_patient():
                    st.session_state.search_clicked = True

                if search_option == "UHID":
                    search_uhid = st.text_input("Enter UHID", placeholder="e.g., 20240319-8f3a", key="uhid_input")
                    st.button("Search Patient", on_click=search_patient)
                    
                    if st.session_state.search_clicked and search_uhid:
                        patient = collection.find_one({"UHID": search_uhid})
                        st.session_state.patient_data = patient
                
                else:  # Search by Patient Name
                    search_name = st.text_input("Search Patient Name", placeholder="Enter patient name", key="name_input")
                    st.button("Search Patient", on_click=search_patient)
                    
                    if st.session_state.search_clicked and search_name:
                        patient = collection.find_one({"name": search_name})
                        st.session_state.patient_data = patient

                # Display patient data if available
                if st.session_state.patient_data:
                    patient = st.session_state.patient_data
                    st.write(f"**UHID**: {patient['UHID']}")
                    st.write(f"**Name**: {patient['name']}")
                    st.write(f"**Medical History**: {patient['medical_history']}")
                    st.write(f"**Critical Point**: {patient['critical_point']}")
                    st.write(f"**Allergies**: {patient['allergies']}")
                elif st.session_state.search_clicked:
                    st.error("Patient not found.")
    else:
        st.warning("No calls available right now.")
