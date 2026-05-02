import streamlit as st

st.set_page_config(
    page_title="FHIR Care Gap Detection",
    page_icon="🩺",
    layout="wide",
)

ROLE_LABELS = {
    "patient":   "Patient",
    "clinician": "Clinician",
    "admin":     "Admin",
    "analyst":   "Analyst",
}

if not st.session_state.get("token"):
    # Not logged in — show only the login page, hide the sidebar entirely
    pg = st.navigation(
        [st.Page("pages/login.py", title="Login", icon="🔐")],
        position="hidden",
    )
else:
    # Logged in — show user info + logout in sidebar, then all app pages
    with st.sidebar:
        full_name = st.session_state.get("full_name") or st.session_state.get("username", "")
        role_key  = st.session_state.get("role", "patient")
        st.markdown(f"**{full_name}**")
        st.caption(ROLE_LABELS.get(role_key, role_key.capitalize()))
        st.markdown("---")
        if st.button("Log Out", use_container_width=True):
            for key in ["token", "username", "full_name", "role"]:
                st.session_state.pop(key, None)
            st.rerun()

    pg = st.navigation([
        st.Page("pages/0_home.py",                           title="Home",                   icon="🏠"),
        st.Page("pages/1_patient_dashboard.py",              title="Patient Dashboard",      icon="🩺"),
        st.Page("pages/2_population_analytics.py",           title="Population Analytics",   icon="📊"),
        st.Page("pages/3_Import_Patient_FHIR_file.py",       title="Import FHIR File",       icon="📁"),
        st.Page("pages/4_Fetch_Patient_From_FHIR_Server.py", title="Fetch from FHIR Server", icon="🌐"),
        st.Page("pages/4_Patient_FHIR_Utility.py",           title="FHIR Utility",           icon="🔧"),
    ])

pg.run()
