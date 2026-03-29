# FHIRCareGapDetection
FHIR-Based Care Gap Detection

**CS-6440, Introduction to Health Informatics — Georgia Tech**

A Streamlit-based dashboard for importing FHIR patient bundles, reviewing patient summaries, and evaluating care gaps against configured rules.

## Features
- Landing page with app overview and navigation guidance
- Import FHIR patient bundles into session state
- Store imported patient data by filename key and overwrite on re-import
- Patient dashboard selects from imported patients and displays extracted demographics
- Care gap evaluation via `app.service.care_gap_service.evaluate_patient_gaps`
- Shows risk tier, total score, gap count, and detailed gap messages
- Sample FHIR bundles available in `fhir_bundles/`

## Installation
1. Create a Python environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the app
Start the Streamlit app from the repository root:
```bash
streamlit run ui/care_gap_app.py
```

## App pages
- `ui/care_gap_app.py` – landing page with application overview
- `ui/pages/1_patient_dashboard.py` – patient dashboard using imported patient data
- `ui/pages/2_population_analytics.py` – population analytics page
- `ui/pages/3_Import_Patient_FHIR_file.py` – upload and store FHIR patient JSON files

## Usage
1. Open the app in your browser after starting Streamlit.
2. Use **Import Patient FHIR Files** to upload `.json` bundle files.
3. The uploaded files are stored in session state under `imported_patients`.
4. Open **Patient Care Gap Dashboard** and select a patient from the dropdown.
5. Review the extracted patient summary and the evaluated care gaps.

## Notes
- Imported patients are keyed by filename without extension.
- Re-importing a file with the same name overwrites the existing session entry.
- The care gap evaluator uses rule definitions from `app/config/care_gap_rules.json` and risk tiers from `app/config/rule.json`.


