import streamlit as st
import requests

API_URL = "http://localhost:8000"  

st.title("Patient Care Gap Dashboard")
st.write("Select a patient to view their summary, detected care gaps, and risk tier.")

# Patient selection
patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)

if st.button("Check Care Gaps"):

    # Call backend API
    try:
        response = requests.get(f"{API_URL}/patient/{patient_id}")
        data = response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.stop()

    # Check if patient data exists
    if "patient" not in data:
        st.error("Patient not found.")
        st.stop()

    # Two-column layout
    col1, col2 = st.columns(2)

    # Left column: Patient Info
    with col1:
        st.subheader("Patient Info")
        patient = data["patient"]
        st.write(f"**Name:** {patient.get('name', 'N/A')}")
        st.write(f"**Age:** {patient.get('age', 'N/A')}")
        st.write(f"**Gender:** {patient.get('gender', 'N/A')}")
        conditions = patient.get("conditions", [])
        st.write(f"**Conditions:** {', '.join(conditions) if conditions else 'None'}")

    # Right column: Care Gaps
    with col2:
        st.subheader("Detected Care Gaps")
        care_gaps = data.get("care_gaps", [])
        if care_gaps:
            for gap in care_gaps:
                st.warning(gap)
        else:
            st.success("No care gaps detected")


    st.subheader("Risk Tier")
    risk = data.get("risk_tier", "Unknown")
    if risk.lower() == "high":
        st.error(risk)
    elif risk.lower() == "moderate":
        st.warning(risk)
    else:
        st.success(risk)