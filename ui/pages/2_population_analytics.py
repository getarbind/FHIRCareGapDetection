import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys
from datetime import date, datetime

from auth_guard import require_login

# Allow imports from project root
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.service.care_gap_service import evaluate_patient_gaps

st.title("Population Analytics")
st.write("View overall trends in care gaps and risk tiers across the patient population.")

token = require_login()

# Get imported patients from session
patients = st.session_state.get("imported_patients", {})

if not patients:
    st.warning("No patients imported yet. Please upload FHIR patient files first.")
    st.stop()

# Function to calculate age
def calculate_age(birth_date: str):
    if not birth_date:
        return None
    try:
        parsed = datetime.fromisoformat(birth_date).date()
    except ValueError:
        return None
    today = date.today()
    return today.year - parsed.year - ((today.month, today.day) < (parsed.month, parsed.day))

# Function to format patient name nicely
def format_name(patient):
    if not patient.get("name"):
        return "Unknown"
    name_parts = patient["name"][0].get("prefix", []) + \
                 patient["name"][0].get("given", []) + \
                 [patient["name"][0].get("family", "")]
    return " ".join([p for p in name_parts if p]).strip()

# Run rule engine on each patient
results = []
for key, data in patients.items():
    patient = data.get("entry", [{}])[0].get("resource") if data.get("resourceType") == "Bundle" else data
    if not patient or patient.get("resourceType") != "Patient":
        continue

    age = calculate_age(patient.get("birthDate"))

    rule_patient = dict(patient)
    rule_patient["age"] = age or 0
    rule_patient["gender"] = patient.get("gender", "").lower()
    rule_patient.setdefault("conditions", [])
    rule_patient.setdefault("observations", {})
    rule_patient.setdefault("medications", {"active_classes": []})
    rule_patient.setdefault("immunizations", {})
    rule_patient.setdefault("encounters", {})

    result = evaluate_patient_gaps(rule_patient)

    results.append({
        "Patient Key": key,
        "Name": format_name(patient),
        "Risk Tier": result.get("risk_tier", "Unknown"),
        "Total Score": result.get("total_score", 0),
        "Gap Count": result.get("gap_count", 0),
        "Gaps": [g.get("name", "Unknown") for g in result.get("gaps", [])]
    })

if not results:
    st.warning("No valid patients found for analytics.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(results)

# Key Metrics 
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Patients", len(df))
with col2:
    st.metric("Patients With Care Gaps", (df["Gap Count"] > 0).sum())
with col3:
    st.metric("High Risk Patients", (df["Risk Tier"] == "High").sum())

# Risk Tier Distribution
st.subheader("Risk Tier Distribution")
risk_counts = df["Risk Tier"].value_counts().reset_index()
risk_counts.columns = ["Risk Tier", "Count"]

fig_risk = px.pie(
    risk_counts,
    names="Risk Tier",
    values="Count",
    title="Patient Risk Tier Distribution",
    color="Risk Tier",
    color_discrete_map={"Low": "green", "Moderate": "orange", "High": "red"}
)
st.plotly_chart(fig_risk, use_container_width=True)

# Care Gaps Frequency 
st.subheader("Care Gaps by Type")
all_gaps = [gap for sublist in df["Gaps"] for gap in sublist]

if all_gaps:
    gap_df = pd.DataFrame(all_gaps, columns=["Care Gap"])
    gap_counts = gap_df.value_counts().reset_index(name="Patients Missing").sort_values("Patients Missing", ascending=False)

    fig_gap = px.bar(
        gap_counts,
        x="Care Gap",
        y="Patients Missing",
        title="Patients Missing Recommended Care"
    )
    st.plotly_chart(fig_gap, use_container_width=True)
else:
    st.info("No care gaps detected across patients.")

# Patient Table 
st.subheader("Patients and Care Gap Summary")
st.dataframe(df[["Name", "Risk Tier", "Gap Count", "Total Score"]], use_container_width=True)

# Top 5 Highest Risk Patients
st.subheader("Top 5 Highest Risk Patients")
df_top5 = df.sort_values(by="Total Score", ascending=False).head(5)

fig_top5 = px.bar(
    df_top5,
    x="Name",
    y="Total Score",
    color="Risk Tier",
    color_discrete_map={"High": "red", "Moderate": "orange", "Low": "green"},
    title="Top 5 Highest Risk Patients"
)
st.plotly_chart(fig_top5, use_container_width=True)