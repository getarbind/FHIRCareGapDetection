import streamlit as st


def require_login():
    """Call this at the top of any page that requires authentication."""
    if not st.session_state.get("token"):
        st.rerun()  # navigation controller will redirect to login page
    return st.session_state["token"]
