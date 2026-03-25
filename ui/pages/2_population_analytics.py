import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Population Analytics")
st.write("View overall trends in care gaps and risk tiers across the patient population.")


st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Patients", 150)

with col2:
    st.metric("Patients with Overdue HbA1c", 20)

with col3:
    st.metric("High Risk Patients", 5)


# an example chart to showcase what care gaps are missing with associated number of patients
st.subheader("Care Gaps by Type")

care_gap_data = pd.DataFrame({
    "Care Gap": [
        "HbA1c Test",
        "Statin Therapy",
        "Annual Physical",
        "Flu Vaccine"
    ],
    "Patients Missing": [20, 10, 5, 15]
})

fig = px.bar(
    care_gap_data,
    x="Care Gap",
    y="Patients Missing",
    color="Patients Missing",
    color_continuous_scale="Reds",
    title="Patients Missing Recommended Care"
)

st.plotly_chart(fig, use_container_width=True)


# Example risk tiers to showcase
st.subheader("Risk Tier Distribution")

risk_data = pd.DataFrame({
    "Risk Tier": ["Low", "Moderate", "High"],
    "Count": [100, 45, 5]
})

fig2 = px.pie(
    risk_data,
    names="Risk Tier",
    values="Count",
    title="Patient Risk Tier Distribution",
    color="Risk Tier",
    color_discrete_map={
        "Low": "green",
        "Moderate": "orange",
        "High": "red"
    }
)

st.plotly_chart(fig2, use_container_width=True)

# example patient table to showcase the graphs
st.subheader("Sample Patients with Care Gaps")

patients_data = pd.DataFrame({
    "Patient ID": [1, 2, 3, 4, 5],
    "Name": ["Alice Smith", "Bob Johnson", "Charlie Lee", "Dana Patel", "Evan Kim"],
    "Risk Tier": ["High", "Moderate", "Low", "Low", "Moderate"],
    "Missing HbA1c": ["Yes", "Yes", "No", "No", "Yes"]
})

st.dataframe(patients_data, use_container_width=True)

