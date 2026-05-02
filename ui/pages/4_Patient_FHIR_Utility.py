import streamlit as st

from auth_guard import require_login

st.title("Patient FHIR Utility")
st.write("Use this utility page to manage imported patient data stored in session state.")

token = require_login()

if "imported_patients" not in st.session_state:
    st.session_state["imported_patients"] = {}

st.write("### Imported patient files currently stored in session")
if st.session_state["imported_patients"]:
    for key in st.session_state["imported_patients"]:
        st.write(f"- {key}")
else:
    st.info("No imported patient files are currently stored.")

if st.button("Clear imported patient data"):
    removed_keys = list(st.session_state["imported_patients"].keys())
    st.session_state["imported_patients"].clear()

    if removed_keys:
        st.success("Cleared imported patient data.")
        st.write("### Removed keys")
        for key in removed_keys:
            st.write(f"- {key}")
    else:
        st.info("There was nothing to clear.")
