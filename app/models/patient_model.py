"""
Patient data model.

This defines the normalized patient structure that the rule engine operates on.
"""

from dataclasses import dataclass, field


@dataclass
class ObservationRecord:
    """A single lab result or clinical measurement."""
    value: float | dict      # float for most labs; dict for BP panels: {"systolic": 140, "diastolic": 90}
    days_ago: int            # How many days since this observation was recorded
    unit: str = ""


@dataclass
class ImmunizationRecord:
    """Vaccination history for a given CVX code."""
    doses: int               # Total doses received
    last_days_ago: int       # Days since the most recent dose


@dataclass
class EncounterRecord:
    """A clinical encounter (e.g. wellness visit)."""
    days_ago: int


@dataclass
class PatientRecord:
    """
    Normalized patient record consumed by the rule engine.

    observations: keyed by LOINC code (e.g. "4548-4" for HbA1c)
    immunizations: keyed by CVX code (e.g. "141" for flu shot)
    encounters: keyed by type (e.g. "wellness_visit")
    medications.active_classes: list of medication class names from care_gap_rules.json
                                (e.g. ["statins", "ace_inhibitors"])
    conditions: list of condition keys from care_gap_rules.json
                (e.g. ["diabetes_type2", "hypertension"])
    """
    id: int
    name: str
    age: int
    gender: str                                              # "male" | "female"
    conditions: list[str] = field(default_factory=list)
    observations: dict[str, ObservationRecord] = field(default_factory=dict)
    medications: dict = field(default_factory=lambda: {"active_classes": []})
    immunizations: dict[str, ImmunizationRecord] = field(default_factory=dict)
    encounters: dict[str, EncounterRecord] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to a plain dict the rule engine can evaluate."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "conditions": self.conditions,
            "observations": {
                loinc: {"value": obs.value, "days_ago": obs.days_ago, "unit": obs.unit}
                for loinc, obs in self.observations.items()
            },
            "medications": self.medications,
            "immunizations": {
                cvx: {"doses": imm.doses, "last_days_ago": imm.last_days_ago}
                for cvx, imm in self.immunizations.items()
            },
            "encounters": {
                enc_type: {"days_ago": enc.days_ago}
                for enc_type, enc in self.encounters.items()
            },
        }
