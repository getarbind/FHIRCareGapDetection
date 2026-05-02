import streamlit as st
import requests
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional

from auth_guard import require_login

UI_DIR   = Path(__file__).resolve().parents[1]
ROOT_DIR = Path(__file__).resolve().parents[2]
for p in (str(UI_DIR), str(ROOT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from config import API_URL
from app.service.care_gap_service import evaluate_patient_gaps

st.title("Patient Care Gap Dashboard")
st.write("Select a patient to view their summary, detected care gaps, and risk tier.")

token = require_login()

imported_patients = st.session_state.get("imported_patients", {})
selected_patient = None

if imported_patients:
    selected_patient = st.selectbox(
        "Select imported patient",
        [""] + list(imported_patients.keys()),
        format_func=lambda x: "Choose imported patient" if x == "" else x,
    )
else:
    st.warning("No imported patients found. Upload a FHIR patient file from the Import page first.")

if selected_patient:
    data = imported_patients[selected_patient]
    patient = data.get("entry", [{}])[0].get("resource") if data.get("resourceType") == "Bundle" else data

    if not patient or patient.get("resourceType") != "Patient":
        st.error("Imported file does not contain a Patient resource.")
    else:
        st.success(f"Loaded patient: {selected_patient}")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Patient Info")
            name = "N/A"
            if patient.get("name"):
                name_parts = []
                name_parts.extend(patient["name"][0].get("prefix", []))
                name_parts.extend(patient["name"][0].get("given", []))
                if patient["name"][0].get("family"):
                    name_parts.append(patient["name"][0]["family"])
                name = " ".join(name_parts).strip() or "N/A"

            birth_date = patient.get("birthDate", "N/A")
            age = None
            if birth_date != "N/A":
                try:
                    parsed = datetime.fromisoformat(birth_date).date()
                    today = date.today()
                    age = today.year - parsed.year - ((today.month, today.day) < (parsed.month, parsed.day))
                except ValueError:
                    age = None

            st.write(f"**Name:** {name}")
            st.write(f"**Birth date:** {birth_date}")
            st.write(f"**Age:** {age if age is not None else 'N/A'}")
            st.write(f"**Gender:** {patient.get('gender', 'N/A').title()}")
            tele = [item.get("value") for item in patient.get("telecom", []) if item.get("value")]
            st.write(f"**Contact:** {', '.join(tele) if tele else 'N/A'}")

        with col2:
            st.subheader("Summary")
            address = patient.get("address", [{}])[0]
            address_text = ", ".join(
                [part for part in [address.get("line", [None])[0], address.get("city"), address.get("state"), address.get("postalCode"), address.get("country")]
                 if part]
            )
            st.write(f"**Address:** {address_text or 'N/A'}")
            st.write(f"**Marital status:** {patient.get('maritalStatus', {}).get('text', 'N/A')}")
            st.write(f"**Language:** {patient.get('communication', [{}])[0].get('language', {}).get('text', 'N/A')}")
            st.write(f"**Resource type:** {patient.get('resourceType', 'N/A')}")

        st.markdown("---")

        rule_patient = dict(patient)
        rule_patient["age"] = age or 0
        rule_patient["gender"] = patient.get("gender", "").lower()
        rule_patient.setdefault("conditions", [])
        rule_patient.setdefault("observations", {})
        rule_patient.setdefault("medications", {"active_classes": []})
        rule_patient.setdefault("immunizations", {})
        rule_patient.setdefault("encounters", {})

        care_gaps_result = evaluate_patient_gaps(rule_patient)

        st.subheader("Care Gap Evaluation")
        st.write(f"**Risk tier:** {care_gaps_result.get('risk_tier', 'Unknown')}")
        st.write(f"**Total score:** {care_gaps_result.get('total_score', 0)}")
        st.write(f"**Gap count:** {care_gaps_result.get('gap_count', 0)}")

        gaps = care_gaps_result.get("gaps", [])
        if gaps:
            for gap in gaps:
                st.warning(f"{gap.get('name', 'Unknown gap')} - {gap.get('message', '')} (Severity: {gap.get('severity', 'N/A')})")
        else:
            st.success("No care gaps detected")

        #st.subheader("Raw Imported JSON")
        #st.json(data)
