import os
import streamlit.components.v1 as components

_RELEASE = False  # Set to False for development

if not _RELEASE:
    _component_func = components.declare_component(
        "video_chat",
        url="http://localhost:3000",  # Default port for React development server
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    _component_func = components.declare_component("video_chat", path=build_dir)

def video_chat(room_id, key=None):
    """Create a video chat component instance."""
    return _component_func(room_id=room_id, key=key)

if not _RELEASE:
    import streamlit as st
    
    # Test the component
    st.subheader("Component test")
    room_id = "test-room"
    video_chat(room_id=room_id) 