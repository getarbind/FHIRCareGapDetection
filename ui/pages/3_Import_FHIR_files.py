import streamlit as st
import json

st.title("Import FHIR Files")

st.write("Upload a FHIR JSON file to view its content.")

uploaded_file = st.file_uploader("Upload FHIR JSON file", type=["json"])

if uploaded_file is not None:
    try:
        # Read JSON file
        data = json.load(uploaded_file)

        st.success("FHIR file uploaded successfully!")

        # Show JSON data
        st.subheader("FHIR Data Preview")
        st.json(data)

    except Exception as e:
        st.error(f"Error reading file: {e}")