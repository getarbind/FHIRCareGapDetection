import streamlit as st

from auth_guard import require_login

require_login()

full_name = st.session_state.get("full_name") or st.session_state.get("username", "")

st.markdown(
    f"""
    <div style="padding: 32px 36px; border-radius: 18px;
                background: linear-gradient(135deg, #E9F3FF 0%, #F7FAFF 100%);
                margin-bottom: 1.5rem;">
        <h1 style="color:#0B3D91; margin-bottom:0.25rem;">
            FHIR Care Gap Detection Dashboard
        </h1>
        <p style="color:#34495E; font-size:1.05rem; max-width:860px; line-height:1.7; margin:0;">
            Welcome back, <strong>{full_name}</strong>! Analyze patient FHIR bundles, surface overdue
            care opportunities, and monitor population-level health gaps. This dashboard helps care teams
            and analysts quickly identify patients who may need follow-up screenings, preventive services,
            or chronic care interventions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Salient features ───────────────────────────────────────
st.markdown("## What This App Offers")

col1, col2, col3 = st.columns(3)

card_style = (
    "background:#FFFFFF; padding:22px; border-radius:14px; "
    "box-shadow:0 2px 10px rgba(0,0,0,0.06); height:100%;"
)

with col1:
    st.markdown(
        f"""
        <div style="{card_style}">
            <h3 style="color:#0B3D91; margin-bottom:0.5rem;">🩺 Patient-Focused Analysis</h3>
            <p style="color:#4B5D6B; margin:0; line-height:1.6;">
                Instantly review care gaps, risk tiers, and patient demographics in one place.
                Evaluate individual FHIR bundles against configurable clinical rules to identify
                overdue screenings, missing vaccinations, and chronic care deficiencies.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style="{card_style}">
            <h3 style="color:#0B3D91; margin-bottom:0.5rem;">📊 Population Insights</h3>
            <p style="color:#4B5D6B; margin:0; line-height:1.6;">
                Aggregate trends across your patient cohort. Visualize risk tier distributions,
                most common care gaps, and the top high-risk patients — enabling data-driven
                prioritization for care improvement programs.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div style="{card_style}">
            <h3 style="color:#0B3D91; margin-bottom:0.5rem;">⚡ Actionable Output</h3>
            <p style="color:#4B5D6B; margin:0; line-height:1.6;">
                Every detected gap includes a severity rating, clinical guideline reference, and
                descriptive message — giving care coordinators the context they need to act quickly
                without leaving the dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Key capabilities ───────────────────────────────────────
st.markdown("## Key Capabilities")

cap_col1, cap_col2 = st.columns(2)

with cap_col1:
    st.markdown(
        """
        - **Import FHIR Files** — upload local `.json` FHIR bundles and run the rule engine instantly
        - **Live FHIR Server Fetch** — query any FHIR R4 server by Patient ID or name search
        - **Care Gap Rule Engine** — 28 configurable rules covering preventive care, chronic disease management, and screenings
        - **Risk Tier Scoring** — patients are scored Low / Moderate / High based on accumulated gap severity
        """
    )

with cap_col2:
    st.markdown(
        """
        - **Population Analytics** — pie charts, bar charts, and ranked patient tables across your cohort
        - **Role-Based Access** — patient, clinician, admin, and analyst roles with JWT authentication
        - **Persistent Storage** — SQLite backend stores patients and care gaps via a FastAPI REST API
        - **Session Management** — review and clear imported patient data at any time from the Utility page
        """
    )

st.markdown("---")

# ── Getting started ────────────────────────────────────────
st.markdown("## How to Get Started")

step_col1, step_col2, step_col3 = st.columns(3)

with step_col1:
    st.markdown(
        """
        <div style="background:#F0FFF4; border:1px solid #C6F6D5; border-radius:12px; padding:18px;">
            <h4 style="color:#276749; margin-bottom:0.4rem;">Step 1 — Load Patients</h4>
            <p style="color:#4A5568; margin:0; font-size:0.95rem;">
                Use <strong>Import FHIR File</strong> to upload a local JSON bundle, or
                use <strong>Fetch from FHIR Server</strong> to pull directly from an R4 endpoint.
                Sample bundles are included in <code>fhir_bundles/</code>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_col2:
    st.markdown(
        """
        <div style="background:#EBF8FF; border:1px solid #BEE3F8; border-radius:12px; padding:18px;">
            <h4 style="color:#2B6CB0; margin-bottom:0.4rem;">Step 2 — Review Care Gaps</h4>
            <p style="color:#4A5568; margin:0; font-size:0.95rem;">
                Open <strong>Patient Dashboard</strong>, select a patient from the dropdown, and
                review their demographics, risk tier, total score, and each detected care gap
                with severity and guideline details.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_col3:
    st.markdown(
        """
        <div style="background:#FFF5F5; border:1px solid #FED7D7; border-radius:12px; padding:18px;">
            <h4 style="color:#9B2335; margin-bottom:0.4rem;">Step 3 — Explore Population</h4>
            <p style="color:#4A5568; margin:0; font-size:0.95rem;">
                Visit <strong>Population Analytics</strong> to see cohort-level trends — risk tier
                distribution, most frequent gaps, and the top 5 highest-risk patients ranked by
                total score.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
