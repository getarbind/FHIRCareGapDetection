from fastapi import FastAPI, HTTPException
from app.service.patient_service import get_patient, list_patients
from app.service.care_gap_service import evaluate_patient_gaps
from pydantic import BaseModel
from typing import Any

app = FastAPI(title="Care Gap Detection API")


@app.get("/")
def hello():
    return {"message": "Care Gap Detection API running"}


@app.get("/patients")
def get_all_patients():
    """List all available patients."""
    patients = list_patients()
    return {"patients": patients, "count": len(patients)}


@app.get("/patient/{patient_id}")
def get_patient_data(patient_id: int):
    """
    Return patient info plus all evaluated care gaps and risk tier.

    Response shape:
    {
        "patient": { id, name, age, gender, conditions, ... },
        "care_gaps": {
            "gaps": [ { rule_id, name, category, severity, message, guideline }, ... ],
            "risk_tier": "Low" | "Moderate" | "High",
            "total_score": int,
            "gap_count": int
        }
    }
    """
    patient = get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    care_gaps = evaluate_patient_gaps(patient)

    return {
        "patient": patient,
        "care_gaps": care_gaps,
    }


@app.post("/evaluate")
def evaluate_arbitrary_patient(patient: dict[str, Any]):
    """
    Evaluate care gaps for an arbitrary patient dict.
    Used by the FHIR import page to run rules against a parsed FHIR bundle.
    """
    care_gaps = evaluate_patient_gaps(patient)
    return care_gaps
