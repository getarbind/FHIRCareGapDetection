def evaluate_rules(patient, rules):

    gaps = []

    for rule in rules:

        try:
            if eval(rule["condition"], {}, patient):
                gaps.append(rule["message"])

        except Exception as e:
            print(f"Rule error: {e}")

    return gaps