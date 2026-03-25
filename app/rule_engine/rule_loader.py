import json
from pathlib import Path

def load_rules():

    rules_path = Path("app/config/rules.json")

    with open(rules_path) as f:
        rules = json.load(f)

    return rules