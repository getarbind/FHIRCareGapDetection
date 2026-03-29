from app.rule_engine.rule_loader import load_rules, load_risk_tiers
from app.rule_engine.rule_engine import evaluate_rules

_rules = load_rules()
_risk_tiers = load_risk_tiers()


def _compute_risk_tier(gaps: list[dict]) -> str:
    """
    Sum the severity_weight of all triggered gaps.
    Map the total score to a risk tier per the thresholds in care_gap_rules.json.
    """
    total_score = sum(g.get("severity_weight", 1) for g in gaps)

    for tier_name, bounds in _risk_tiers.items():
        if bounds["min_score"] <= total_score <= bounds["max_score"]:
            return tier_name

    return "Unknown"


def evaluate_patient_gaps(patient: dict) -> dict:
    """
    Evaluate all care gap rules for a patient.
    Returns a dict with:
      - gaps: list of triggered gap dicts
      - risk_tier: "Low" | "Moderate" | "High"
      - total_score: numeric weighted score
      - gap_count: total number of gaps
    """
    gaps = evaluate_rules(patient, _rules)
    risk_tier = _compute_risk_tier(gaps)
    total_score = sum(g.get("severity_weight", 1) for g in gaps)

    return {
        "gaps": gaps,
        "risk_tier": risk_tier,
        "total_score": total_score,
        "gap_count": len(gaps),
    }
