import streamlit as st

st.set_page_config(
    page_title="FHIR Care Gap Detection",
    page_icon="🩺",
    layout="wide",
)

st.markdown(
    """
    <div style="padding: 30px; border-radius: 18px; background: linear-gradient(135deg, #E9F3FF 0%, #F7FAFF 100%);">
        <h1 style="color: #0B3D91; margin-bottom: 0.15rem;">FHIR Care Gap Detection Dashboard</h1>
        <p style="color: #34495E; font-size: 1.05rem; max-width: 880px; line-height: 1.6;">
            Analyze patient FHIR bundles, surface overdue care opportunities, and monitor population-level health gaps.
            This dashboard is designed to help care teams and analysts quickly identify patients who may need follow-up screenings,
            preventive services, or chronic care interventions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown("### What you can do")
st.markdown(
    """
    - **Import FHIR Files** to load patient bundles and preview structured patient data.
    - **Patient Dashboard** to review individual care gaps, demographics, and encounter summaries.
    - **Population Analytics** to compare trends, risk tiers, and care gap counts across your dataset.
    """
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div style='background:#FFFFFF; padding:18px; border-radius:14px; box-shadow:0 2px 10px rgba(0,0,0,0.05);'>
        <h3 style='margin-bottom:0.5rem; color:#0B3D91;'>Patient-focused</h3>
        <p style='margin:0; color:#4B5D6B;'>Quickly review care gaps, risk factors, and patient demographics in one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div style='background:#FFFFFF; padding:18px; border-radius:14px; box-shadow:0 2px 10px rgba(0,0,0,0.05);'>
        <h3 style='margin-bottom:0.5rem; color:#0B3D91;'>Population insights</h3>
        <p style='margin:0; color:#4B5D6B;'>Discover patterns and trends across your patients to prioritize care improvement.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div style='background:#FFFFFF; padding:18px; border-radius:14px; box-shadow:0 2px 10px rgba(0,0,0,0.05);'>
        <h3 style='margin-bottom:0.5rem; color:#0B3D91;'>Actionable output</h3>
        <p style='margin:0; color:#4B5D6B;'>Use extracted patient data and care gap details to accelerate follow-up planning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

st.subheader("How to get started")
st.write(
    "1. Upload a FHIR JSON file from the Import page.\n"
    "2. Inspect the extracted patient summary and care gap details.\n"
    "3. Explore the Population Analytics tab for cohort insights and risk patterns."
)
