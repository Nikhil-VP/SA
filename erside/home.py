import streamlit as st
from utils import check_for_call

def home_page():
    st.title("Home")

    # Display Connect Button
    call_available = check_for_call()  # Simulated call check
    if call_available:
        st.success("You have an incoming call!")
        if st.button("Connect"):
            st.info("You are now connected to the call.")
    else:
        st.warning("No calls available right now.")
