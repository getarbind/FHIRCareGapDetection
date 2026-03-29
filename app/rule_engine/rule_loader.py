import json
from pathlib import Path


def load_rules(rules_path: str = "app/config/care_gap_rules.json") -> list[dict]:
    """
    Load rules from care_gap_rules.json.
    Returns only the list of rule objects (not the full metadata/codes sections).
    Only returns rules where active == True.
    """
    path = Path(rules_path)
    with open(path) as f:
        data = json.load(f)

    all_rules = data.get("rules", [])
    active_rules = [r for r in all_rules if r.get("active", True)]
    print(f"[RuleLoader] Loaded {len(active_rules)} active rules from {path}")
    return active_rules


def load_risk_tiers(rules_path: str = "app/config/care_gap_rules.json") -> dict:
    """Load the risk tier threshold configuration."""
    path = Path(rules_path)
    with open(path) as f:
        data = json.load(f)
    return data.get("risk_tier_thresholds", {}).get("tiers", {})
