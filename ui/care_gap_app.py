import streamlit as st

st.title("FHIR Care Gap Detection Dashboard")

st.write("""
Welcome! This app helps identify missing or overdue care for chronic disease patients.
Select a patient to view their summary, care gaps, and risk tier.
Use the tabs on the left to explore analyze patients, population analytics and other features.
""")


st.subheader("Get Started")
st.write("Go to the **Patient Dashboard** tab to select a patient and check care gaps.")
st.write("Go to **Population Analytics** to see overall statistics and charts.")