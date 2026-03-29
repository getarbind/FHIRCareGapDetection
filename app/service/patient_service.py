"""
Patient service — returns mock patient records for development/testing.

Each patient is a realistic clinical scenario designed to exercise different rules.
"""

from app.models.patient_model import PatientRecord, ObservationRecord, ImmunizationRecord, EncounterRecord


MOCK_PATIENTS: dict[int, PatientRecord] = {

    # Patient 1 — Diabetic with multiple gaps (should be High risk)
    1: PatientRecord(
        id=1,
        name="John Doe",
        age=55,
        gender="male",
        conditions=["diabetes_type2", "hypertension", "hyperlipidemia"],
        observations={
            "4548-4":  ObservationRecord(value=9.4, days_ago=210, unit="%"),       # HbA1c — overdue AND poor control
            "55284-4": ObservationRecord(value={"systolic": 148, "diastolic": 94}, days_ago=90),  # BP — uncontrolled
            "2093-3":  ObservationRecord(value=220.0, days_ago=400, unit="mg/dL"), # Cholesterol — overdue
        },
        medications={
            "active_classes": ["metformin"]   # Missing statin, ACE/ARB
        },
        immunizations={
            "141": ImmunizationRecord(doses=1, last_days_ago=400),  # Flu — overdue
        },
        encounters={
            "wellness_visit": EncounterRecord(days_ago=400),  # Annual physical — overdue
        }
    ),

    # Patient 2 — Well-managed diabetic (should be Low risk)
    2: PatientRecord(
        id=2,
        name="Maria Garcia",
        age=62,
        gender="female",
        conditions=["diabetes_type2"],
        observations={
            "4548-4":  ObservationRecord(value=6.8, days_ago=90, unit="%"),        # HbA1c — recent and controlled
            "9318-7":  ObservationRecord(value=15.0, days_ago=60, unit="mg/g"),    # UACR — recent
            "33914-3": ObservationRecord(value=68.0, days_ago=100, unit="mL/min"), # eGFR — recent
            "67797-5": ObservationRecord(value=1.0, days_ago=200),                 # Eye exam
            "29544-4": ObservationRecord(value=1.0, days_ago=200),                 # Foot exam
            "2093-3":  ObservationRecord(value=180.0, days_ago=150, unit="mg/dL"),
        },
        medications={
            "active_classes": ["metformin", "statins"]
        },
        immunizations={
            "141": ImmunizationRecord(doses=1, last_days_ago=200),  # Flu — current
        },
        encounters={
            "wellness_visit": EncounterRecord(days_ago=200),
        }
    ),

    # Patient 3 — Heart failure with missing beta-blocker (should be High risk)
    3: PatientRecord(
        id=3,
        name="Robert Kim",
        age=70,
        gender="male",
        conditions=["heart_failure", "coronary_artery_disease", "hypertension"],
        observations={
            "55284-4": ObservationRecord(value={"systolic": 152, "diastolic": 96}, days_ago=200),
            "2093-3":  ObservationRecord(value=210.0, days_ago=300, unit="mg/dL"),
        },
        medications={
            "active_classes": ["statins"]  # Missing beta-blocker, ACE/ARB
        },
        immunizations={
            "141": ImmunizationRecord(doses=1, last_days_ago=100),
            "215": ImmunizationRecord(doses=1, last_days_ago=500),  # Pneumococcal — done
            "187": ImmunizationRecord(doses=2, last_days_ago=200),  # Shingrix complete
        },
        encounters={
            "wellness_visit": EncounterRecord(days_ago=300),
        }
    ),

    # Patient 4 — Preventive care gaps only (female, age 45)
    4: PatientRecord(
        id=4,
        name="Susan Lee",
        age=45,
        gender="female",
        conditions=[],  # No chronic conditions
        observations={
            "39156-5": ObservationRecord(value=31.5, days_ago=400, unit="kg/m2"),  # BMI > 30 — obesity
        },
        medications={"active_classes": []},
        immunizations={
            "141": ImmunizationRecord(doses=1, last_days_ago=180),
        },
        encounters={
            "wellness_visit": EncounterRecord(days_ago=500),  # Overdue
        }
    ),
}


def get_patient(patient_id: int) -> dict:
    """
    Return a patient record as a plain dict.
    Falls back to a simple unknown patient if ID not found in mock data.
    """
    patient = MOCK_PATIENTS.get(patient_id)
    if patient:
        return patient.to_dict()

    # Fallback for unknown IDs during testing
    return {
        "id": patient_id,
        "name": f"Test Patient #{patient_id}",
        "age": 40,
        "gender": "male",
        "conditions": [],
        "observations": {},
        "medications": {"active_classes": []},
        "immunizations": {},
        "encounters": {},
    }


def list_patients(*args) -> list[dict]:
    """Return all mock patients as a list of plain dicts."""
    return [p.to_dict() for p in MOCK_PATIENTS.values()]
