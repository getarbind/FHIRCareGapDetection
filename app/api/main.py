from fastapi import FastAPI
from app.services.patient_service import get_patient
from app.services.care_gap_service import evaluate_patient_gaps

app = FastAPI(title="Care Gap Detection API")

@app.get("/")
def hello():
    return {"message": "Care Gap Detection API running"}

@app.get("/patient/{patient_id}")
def get_patient_data(patient_id: int):
    patient = get_patient(patient_id)
    gaps = evaluate_patient_gaps(patient)

    return {
        "patient": patient,
        "care_gaps": gaps
    }