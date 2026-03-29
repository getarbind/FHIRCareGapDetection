from datetime import date
from typing import Any


def _patient_has_condition(patient: dict, required: list[str]) -> bool:
    """Return True if the patient has ANY of the listed conditions."""
    patient_conditions = set(patient.get("conditions", []))
    return bool(patient_conditions.intersection(required))


def _patient_meets_criteria(patient: dict, criteria: dict) -> bool:
    age = patient.get("age", 0)
    gender = patient.get("gender", "").lower()
    age_min = criteria.get("age_min", 0)
    age_max = criteria.get("age_max", 999)
    required_gender = criteria.get("gender", "").lower()

    if age < age_min or age > age_max:
        return False
    if required_gender and gender != required_gender:
        return False
    return True


def _check_observation(patient: dict, rule: dict) -> bool:
    """
    Returns True (gap triggered) if the observation check fails.
    check_type: "recency" — observation is missing or too old
    check_type: "value_threshold" — most recent value exceeds a threshold
    """
    loinc = rule.get("observation_loinc")
    if not loinc:
        return False

    observations = patient.get("observations", {})
    obs = observations.get(loinc)
    evaluation = rule.get("evaluation", {})
    check_type = evaluation.get("check_type")

    if check_type == "recency":
        max_days = evaluation.get("max_days_since_last", 365)
        if obs is None:
            return True  
        return obs.get("days_ago", 9999) > max_days

    if check_type == "value_threshold":
        if obs is None:
            return False 
        value = obs.get("value")
        threshold = evaluation.get("threshold_value")
        operator = evaluation.get("operator", ">=")

        # Handle blood pressure panels (dict value)
        if isinstance(value, dict):
            systolic_thresh = evaluation.get("threshold_value_systolic")
            diastolic_thresh = evaluation.get("threshold_value_diastolic")
            if systolic_thresh and diastolic_thresh:
                s = value.get("systolic", 0)
                d = value.get("diastolic", 0)
                return s >= systolic_thresh or d >= diastolic_thresh
            return False

        if threshold is None:
            return False

        if operator == ">=":
            return value >= threshold
        if operator == ">":
            return value > threshold
        if operator == "<=":
            return value <= threshold
        if operator == "<":
            return value < threshold

    return False


def _check_medication(patient: dict, rule: dict) -> bool:
    """Returns True (gap triggered) if required medication is absent."""
    evaluation = rule.get("evaluation", {})
    check_type = evaluation.get("check_type")
    active_classes = set(patient.get("medications", {}).get("active_classes", []))

    if check_type == "active_medication":
        med_class = rule.get("medication_class")
        if isinstance(med_class, list):
            return not bool(active_classes.intersection(med_class))
        return med_class not in active_classes

    if check_type == "active_medication_any":
        med_class = rule.get("medication_class", [])
        if isinstance(med_class, str):
            med_class = [med_class]
        return not bool(active_classes.intersection(med_class))

    return False


def _check_immunization(patient: dict, rule: dict) -> bool:
    """Returns True (gap triggered) if required vaccine is absent or overdue."""
    evaluation = rule.get("evaluation", {})
    check_type = evaluation.get("check_type")
    immunizations = patient.get("immunizations", {})

    # Normalize CVX codes to list
    raw_cvx = rule.get("vaccine_code_cvx", [])
    if isinstance(raw_cvx, str):
        cvx_codes = [raw_cvx]
    else:
        cvx_codes = list(raw_cvx)

    # Find if any matching vaccine record exists
    matching_record = None
    for code in cvx_codes:
        if code in immunizations:
            matching_record = immunizations[code]
            break

    if check_type == "ever_received":
        return matching_record is None

    if check_type == "recency":
        max_days = evaluation.get("max_days_since_last", 365)
        if matching_record is None:
            return True
        return matching_record.get("last_days_ago", 9999) > max_days

    if check_type == "series_complete":
        required_doses = evaluation.get("required_doses", 1)
        if matching_record is None:
            return True
        return matching_record.get("doses", 0) < required_doses

    return False


def _check_encounter(patient: dict, rule: dict) -> bool:
    """Returns True (gap triggered) if wellness/preventive encounter is overdue."""
    evaluation = rule.get("evaluation", {})
    max_days = evaluation.get("max_days_since_last", 365)
    encounters = patient.get("encounters", {})
    wellness = encounters.get("wellness_visit")
    if wellness is None:
        return True
    return wellness.get("days_ago", 9999) > max_days


def evaluate_rule(patient: dict, rule: dict) -> bool:
    """
    Returns True if this rule's gap is triggered for this patient.
    Returns False if the patient is not eligible for this rule, or passes the check.
    """
    if not rule.get("active", True):
        return False

    # --- Condition eligibility ---
    conditions_all = rule.get("condition_required", [])
    conditions_any = rule.get("condition_required_any", [])

    if conditions_all:
        # Patient must have at least one of the listed conditions
        if not _patient_has_condition(patient, conditions_all):
            return False

    if conditions_any:
        if not _patient_has_condition(patient, conditions_any):
            return False

    # --- Patient demographic criteria ---
    criteria = rule.get("patient_criteria", {})
    if criteria and not _patient_meets_criteria(patient, criteria):
        return False

    # --- Dispatch to the correct check ---
    fhir_resource = rule.get("fhir_resource", "")

    if fhir_resource == "Observation":
        return _check_observation(patient, rule)

    if fhir_resource == "MedicationRequest":
        return _check_medication(patient, rule)

    if fhir_resource == "Immunization":
        return _check_immunization(patient, rule)

    if fhir_resource == "Encounter":
        return _check_encounter(patient, rule)

    return False


def evaluate_rules(patient: dict, rules: list[dict]) -> list[dict]:
    """
    Evaluate all rules against a patient.
    Returns a list of triggered gap dicts with rule metadata included.
    """
    gaps = []
    for rule in rules:
        try:
            if evaluate_rule(patient, rule):
                gaps.append({
                    "rule_id": rule.get("rule_id"),
                    "name": rule.get("name"),
                    "category": rule.get("category"),
                    "severity": rule.get("severity"),
                    "severity_weight": rule.get("severity_weight", 1),
                    "message": rule.get("gap_message"),
                    "guideline": rule.get("clinical_guideline"),
                })
        except Exception as e:
            print(f"[RuleEngine] Error evaluating rule {rule.get('rule_id')}: {e}")
    return gaps