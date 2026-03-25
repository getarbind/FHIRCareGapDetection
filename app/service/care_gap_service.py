from app.rule_engine.rule_loader import load_rules
from app.rule_engine.rule_engine import evaluate_rules

rules = load_rules()

def evaluate_patient_gaps(patient):

    return evaluate_rules(patient, rules)