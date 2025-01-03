import streamlit as st
from home import home_page
from nearest_hospital import nearest_hospital_page
from history import history_page
from specific_hospital import specific_hospital_page
from utils import display_map

# ----------------- Main App -----------------
st.set_page_config(page_title="Hospital Navigation App", layout="wide")
st.title("Hospital Navigation System")

# Sidebar for Navigation using Buttons
home_button = st.sidebar.button("Home")
navigate_button = st.sidebar.button("Navigation")
history_button = st.sidebar.button("History")
language = st.sidebar.selectbox("Select Language", ["English", "Hindi", "Spanish", "French"])

# Display a message based on the selected language
if language == "English":
    st.write("Welcome to the Hospital Navigation system in english")
elif language == "Hindi":
    st.write("अस्पताल नेविगेशन सिस्टम में आपका स्वागत है।")
elif language == "Spanish":
    st.write("Bienvenido al sistema de navegación hospitalaria en español.")
elif language == "French":
    st.write("Bienvenue dans le système de navigation hospitalière en français.")


# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "home"



# Page Selection Logic based on buttons clicked
if home_button:
    st.session_state.page = 'home'
elif navigate_button:
    st.session_state.page = 'navigate'
elif history_button:
    st.session_state.page = 'history'

# Display content based on selected page
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'navigate':
    display_map()
elif st.session_state.page == 'history':
    history_page()

# Footer
st.markdown("---")
