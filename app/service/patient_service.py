def get_patient(patient_id: int):
    # Mock patient data (later replaced with FHIR API or database)
    return {
        "id": patient_id,
        "name": "John Doe",
        "last_physical_days": 400,
        "flu_vaccine": False,
        "diabetic": True,
        "hba1c_days": 200
    }