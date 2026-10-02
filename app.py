import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from ui.styles import apply_design_system
from ui.components.header import render_header
from ui.components.progress import render_progress
from ui.views.intake import render_intake_view
from ui.views.review import render_review_view
from ui.views.verification import render_verification_view
from ui.views.evidence import render_evidence_view
from ui.views.action import render_action_view
from ui.views.case_file import render_case_file_view

# Initialize Streamlit config
st.set_page_config(
    page_title="NyayaPath",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply global design system
apply_design_system()

# Initialize global routing state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "INTAKE"

# Mapping pages to integer steps for progress
page_to_step = {
    "INTAKE": 1,
    "REVIEW": 2,
    "VERIFY": 3,
    "EVIDENCE": 4,
    "ACTION": 5,
    "CASE_FILE": 6
}

current_step = page_to_step.get(st.session_state.current_page, 1)

# Render Header and Progress
page_titles = {
    "INTAKE": "Case Intake",
    "REVIEW": "Fact Review",
    "VERIFY": "Verification",
    "EVIDENCE": "Evidence",
    "ACTION": "Action Plan",
    "CASE_FILE": "Case File"
}
render_header(page_titles.get(st.session_state.current_page, ""))
render_progress(current_step=current_step)

# Orchestrate the views
if st.session_state.current_page == "INTAKE":
    render_intake_view()
elif st.session_state.current_page == "REVIEW":
    render_review_view()
elif st.session_state.current_page == "VERIFY":
    render_verification_view()
elif st.session_state.current_page == "EVIDENCE":
    render_evidence_view()
elif st.session_state.current_page == "ACTION":
    render_action_view()
elif st.session_state.current_page == "CASE_FILE":
    render_case_file_view()
