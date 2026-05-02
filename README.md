# FHIRCareGapDetection
FHIR-Based Care Gap Detection

**CS-6440, Introduction to Health Informatics — Georgia Tech**

A full-stack application for importing FHIR patient bundles, evaluating care gaps against configurable rules, and visualizing population-level health trends. The system consists of a **FastAPI backend** (authentication, database, REST API) and a **Streamlit frontend** (interactive dashboard).

## Architecture

```
FHIRCareGapDetection/
├── app/
│   ├── api/main.py          # FHIR evaluation API (patients, care gap scoring)
│   ├── main.py              # Auth + database API (register, login, JWT, CRUD)
│   ├── auth.py              # JWT token creation/verification, bcrypt password hashing
│   ├── config/
│   │   ├── care_gap_rules.json  # Care gap rule definitions
│   │   └── rule.json            # Risk tier thresholds
│   ├── db/                  # SQLAlchemy models, CRUD helpers, database session
│   ├── models/              # Pydantic patient model
│   ├── rule_engine/         # Rule loader and rule engine evaluator
│   ├── service/             # Care gap service, patient service
│   └── utils/               # Data utilities
├── ui/
│   ├── care_gap_app.py              # Landing page with login/register
│   ├── auth_guard.py                # Page-level auth guard helper
│   └── pages/
│       ├── 1_patient_dashboard.py       # Individual patient care gap review
│       ├── 2_population_analytics.py    # Population-level analytics
│       ├── 3_Import_Patient_FHIR_file.py  # Upload local FHIR JSON bundles
│       ├── 4_Fetch_Patient_From_FHIR_Server.py  # Fetch patients from live FHIR server
│       └── 4_Patient_FHIR_Utility.py    # Session state management utility
├── fhir_bundles/            # Sample FHIR patient bundles (patient1–9.json)
├── run.py                   # Uvicorn entry point for the backend
├── care_gap.db              # SQLite database (auto-created on first run)
└── requirements.txt
```

## Features

- **User authentication** — register and log in with JWT tokens (8-hour sessions); roles: `patient`, `clinician`, `admin`, `analyst`
- **Protected pages** — all dashboard pages require a valid login via `auth_guard.py`
- **Import FHIR files** — upload local `.json` FHIR bundles and store them in session state
- **Fetch from FHIR server** — query a live FHIR server (default: HAPI R4) by Patient ID or by name search; import results directly into the session
- **Patient dashboard** — view demographics, care gap details, risk tier, total score, and gap count for any imported patient
- **Population analytics** — compare care gap trends and risk tiers across the loaded dataset
- **Care gap rule engine** — rules defined in `app/config/care_gap_rules.json`; risk tiers configured in `app/config/rule.json`
- **REST API** — protected endpoints for patients (`/patients`, `/patients/{id}`) and care gaps (`/care-gaps`, `/patients/{id}/care-gaps`)
- **SQLite persistence** — `User`, `Patient`, and `CareGap` tables managed via SQLAlchemy; database file auto-created at `care_gap.db`
- **9 sample FHIR bundles** in `fhir_bundles/` for immediate testing

## Installation

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the app

The application requires **both** the FastAPI backend and the Streamlit frontend to be running.

### 1. Start the FastAPI backend

```bash
python run.py
```

The backend starts at `http://localhost:8000`. Interactive API docs are available at `http://localhost:8000/docs`.

### 2. Start the Streamlit frontend

Open a second terminal (with the same virtual environment activated):

```bash
streamlit run ui/care_gap_app.py
```

The UI opens at `http://localhost:8501`.

## App pages

| Page | File | Description |
|------|------|-------------|
| Landing / Auth | `ui/care_gap_app.py` | App overview, login, and account registration |
| Patient Dashboard | `ui/pages/1_patient_dashboard.py` | Per-patient care gaps, risk tier, demographics |
| Population Analytics | `ui/pages/2_population_analytics.py` | Cohort-level trends and gap comparisons |
| Import FHIR File | `ui/pages/3_Import_Patient_FHIR_file.py` | Upload local FHIR JSON bundles |
| Fetch from FHIR Server | `ui/pages/4_Fetch_Patient_From_FHIR_Server.py` | Query a live FHIR server by ID or name |
| FHIR Utility | `ui/pages/4_Patient_FHIR_Utility.py` | View and clear session-stored patient data |

## Usage

1. Start the backend (`python run.py`) and frontend (`streamlit run ui/care_gap_app.py`).
2. On the landing page, **create an account** or **log in** with an existing one.
3. Use **Import FHIR File** to upload a `.json` bundle (samples are in `fhir_bundles/`), or use **Fetch from FHIR Server** to pull a patient from a live FHIR endpoint.
4. Open **Patient Care Gap Dashboard**, select a patient from the dropdown, and review the extracted summary and evaluated care gaps.
5. Visit **Population Analytics** to explore trends across all imported patients.
6. Use **FHIR Utility** to inspect or clear patients currently stored in session state.

## API endpoints

All patient and care gap endpoints require a bearer token obtained from `/auth/login`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Log in and receive a JWT token |
| `GET` | `/auth/me` | Get the current user's profile |
| `GET` | `/patients` | List all patients in the database |
| `GET` | `/patients/{id}` | Get a single patient |
| `GET` | `/care-gaps` | List all care gaps |
| `GET` | `/patients/{id}/care-gaps` | Get care gaps for a specific patient |

## Notes

- Imported patients are stored in Streamlit session state and keyed by filename (local import) or FHIR resource ID (server fetch). Re-importing the same key overwrites the existing entry.
- The care gap evaluator reads rules from `app/config/care_gap_rules.json` and risk tier thresholds from `app/config/rule.json`.
- The SQLite database (`care_gap.db`) is created automatically on first backend startup.
- The default FHIR server URL for live fetch is `https://hapi.fhir.org/baseR4`; it can be changed in the UI.
