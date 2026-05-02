import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

ROLE_LABELS = {
    "patient":   "Patient",
    "clinician": "Clinician",
    "admin":     "Admin",
    "analyst":   "Analyst",
}

st.markdown(
    """
    <div style="text-align:center; padding: 48px 0 24px 0;">
        <h1 style="color:#0B3D91; font-size:2.2rem; margin-bottom:0.4rem;">
            FHIR Care Gap Detection
        </h1>
        <p style="color:#4B5D6B; font-size:1rem;">
            Sign in to access the dashboard and manage patient care gaps.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("### Log In")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log In", use_container_width=True, type="primary"):
        if not username or not password:
            st.warning("Please fill in both fields.")
        else:
            try:
                resp = requests.post(
                    f"{API_URL}/auth/login",
                    data={"username": username, "password": password},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state["token"] = data["access_token"]
                    st.session_state["username"] = data["username"]
                    st.session_state["full_name"] = data.get("full_name", "")
                    st.session_state["role"] = data.get("role", "patient")
                    st.rerun()
                elif resp.status_code == 401:
                    st.error("Incorrect username or password.")
                else:
                    try:
                        detail = resp.json().get("detail", "Unknown error")
                    except Exception:
                        detail = resp.text or f"HTTP {resp.status_code}"
                    st.error(f"Login failed: {detail}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")

with right_col:
    st.markdown("### Create Account")
    reg_full_name = st.text_input("Full Name", key="reg_full_name")
    reg_email     = st.text_input("Email",     key="reg_email")
    reg_username  = st.text_input("Username",  key="reg_username")
    reg_role = st.selectbox(
        "I am a...",
        options=["patient", "clinician", "admin", "analyst"],
        format_func=lambda r: ROLE_LABELS[r],
        key="reg_role",
    )
    reg_password  = st.text_input("Password",         type="password", key="reg_password")
    reg_password2 = st.text_input("Confirm Password", type="password", key="reg_password2")
    if st.button("Create Account", use_container_width=True):
        if not all([reg_full_name, reg_email, reg_username, reg_password, reg_password2]):
            st.warning("Please fill in all fields.")
        elif reg_password != reg_password2:
            st.error("Passwords do not match.")
        elif len(reg_password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            try:
                resp = requests.post(
                    f"{API_URL}/auth/register",
                    json={
                        "username": reg_username,
                        "email":    reg_email,
                        "password": reg_password,
                        "full_name": reg_full_name,
                        "role":     reg_role,
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state["token"]     = data["access_token"]
                    st.session_state["username"]  = data["username"]
                    st.session_state["full_name"] = data.get("full_name", "")
                    st.session_state["role"]      = data.get("role", "patient")
                    st.rerun()
                else:
                    try:
                        detail = resp.json().get("detail", "Unknown error")
                    except Exception:
                        detail = resp.text or f"HTTP {resp.status_code}"
                    st.error(f"Registration failed: {detail}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
