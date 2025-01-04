import streamlit as st
import pandas as pd

def call_history_page():
    st.title("Call History")
    
    # Placeholder for call history data
    call_history_data = pd.DataFrame({
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "Patient Name": ["John Doe", "Jane Smith", "Michael Brown"],
        "Diagnosis": ["Fever", "Back Pain", "Headache"],
        "Duration (min)": [15, 20, 10]
    })
    st.dataframe(call_history_data, use_container_width=True)
