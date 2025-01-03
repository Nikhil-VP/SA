import streamlit as st
from utils import display_map

def nearest_hospital_page():
    # Create two columns: one for the video conference and one for the patient details
    col1, col2 = st.columns([3, 1])  # 3 for video (larger width), 1 for patient details (smaller width)
    
    with col1:
        # Video Conference Placeholder (for demonstration, using a Jitsi Meet link)
        
        
        # Embed Jitsi Meet or another video conferencing platform
        jitsi_url = "https://meet.jit.si/BalancedCropsAccessNor"  # Replace with your own meeting room URL
        
        # Embed the video conference in an iframe to fill the screen
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
