import os
import streamlit as st
from services.document_generator import generate_appeal

def render_case_file_view():
    st.markdown("<h2 style='margin-bottom: 0.5rem;'>NyayaPath Case File</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--muted-text); margin-bottom: 3rem; font-size: 1.1rem; max-width: 800px; line-height: 1.6;'>"
                "A complete summary of your verified case."
                "</p>", unsafe_allow_html=True)

    # Preconditions
    facts = st.session_state.get('case_facts')
    scheme = st.session_state.get('verified_scheme')
    eligibility = st.session_state.get('eligibility_results')
    rejection = st.session_state.get('rejection_result')
    verification = st.session_state.get('verification_result')
    evidence = st.session_state.get('evidence_results')
    plan = st.session_state.action_plan

    if not st.session_state.get('facts_confirmed', False) or not all([facts, scheme, eligibility, rejection, verification, evidence, plan]):
        st.error("You must complete all previous steps before viewing the Case File.")
        if st.button("← Back to Action Plan", type="secondary"):
            st.session_state.current_page = "ACTION"
            st.rerun()
        return

    # Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Action Plan", type="secondary"):
            st.session_state.current_page = "ACTION"
            st.rerun()

    st.markdown(f"<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 2rem 0;'>", unsafe_allow_html=True)

    ref_id = facts.reference_id if facts.reference_id else "Not provided"
    st.markdown(f"**Case #{ref_id}**")
    st.markdown(f"<p style='font-size: 0.85rem; color: var(--muted-text);'>NyayaPath provides civic support based on available published information. It does not provide legal representation or guarantee an outcome.</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. NEXT ACTION (Visual Priority 1)
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>NEXT ACTION</h3>", unsafe_allow_html=True)
    
    if plan.action_route == "NO_VERIFIED_ROUTE":
        st.error("No supported route could be established from the available scheme information.")
    elif plan.action_route == "UNCERTAIN":
        st.warning("NyayaPath could not verify a reliable next step from the available information.")
    else:
        st.markdown(f"<h2 style='color: var(--success-color);'>{plan.action_route.upper()}</h2>", unsafe_allow_html=True)
        st.write(plan.immediate_next_action)
        
        st.markdown("**Authority:** " + (plan.authority if plan.authority else "Not specified"))
        st.markdown("**Deadline:** " + (plan.deadline if plan.deadline else "<span style='color: var(--warning-color);'>Not verified</span>"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. TRUST STATUS (Visual Priority 2)
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>TRUST STATUS</h3>", unsafe_allow_html=True)
    
    if verification.status == "PASS":
        st.markdown("<h3 style='color: var(--success-color); margin:0;'>PASS</h3>", unsafe_allow_html=True)
    elif verification.status == "UNCERTAIN":
        st.markdown("<h3 style='color: var(--warning-color); margin:0;'>UNCERTAIN</h3>", unsafe_allow_html=True)
    elif verification.status == "UNSUPPORTED":
        st.markdown("<h3 style='color: var(--error-color); margin:0;'>UNSUPPORTED</h3>", unsafe_allow_html=True)
    elif verification.status == "POTENTIAL_CONFLICT":
        st.markdown("<h3 style='color: var(--warning-color); margin:0;'>POTENTIAL CONFLICT</h3>", unsafe_allow_html=True)
        
    st.write(verification.explanation)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. WHAT WE FOUND (Visual Priority 3)
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>WHAT WE FOUND</h3>", unsafe_allow_html=True)
    
    met_count = sum(1 for r in eligibility if r.status == 'MET')
    not_met_count = sum(1 for r in eligibility if r.status == 'NOT_MET')
    uncertain_count = sum(1 for r in eligibility if r.status == 'UNCERTAIN')
    
    st.markdown(f"<span style='color: var(--success-color);'>✓ {met_count} criteria met</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: var(--error-color);'>✕ {not_met_count} criteria not met</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: var(--warning-color);'>? {uncertain_count} criteria needs verification</span>", unsafe_allow_html=True)
    
    with st.expander("Show Detailed Verification"):
        for res in eligibility:
            rule = next((r for r in scheme.eligibility_criteria if r.criterion_id == res.criterion_id), None)
            if not rule: continue
            color = "var(--success-color)" if res.status == 'MET' else "var(--error-color)" if res.status == 'NOT_MET' else "var(--warning-color)"
            icon = "✓" if res.status == 'MET' else "✕" if res.status == 'NOT_MET' else "?"
            st.markdown(f"**{rule.name}**")
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{icon} {res.status}</span>", unsafe_allow_html=True)
            st.write(rule.description)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. EVIDENCE (Visual Priority 4)
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>EVIDENCE</h3>", unsafe_allow_html=True)
    for item in evidence:
        if item.status == 'AVAILABLE':
            st.markdown(f"<span style='color: var(--success-color); font-weight: bold;'>✓ {item.name}</span> - Available", unsafe_allow_html=True)
        elif item.status == 'MISSING':
            st.markdown(f"<span style='color: var(--error-color); font-weight: bold;'>○ {item.name}</span> - Missing", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color: var(--warning-color); font-weight: bold;'>? {item.name}</span> - Needs verification", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. WHAT HAPPENED (Visual Priority 5)
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>WHAT HAPPENED</h3>", unsafe_allow_html=True)
    st.markdown("**Application Rejected**")
    if facts.rejection_reason:
        st.write(f"The application was reported as rejected because the stated rejection reason was: {facts.rejection_reason}")
    else:
        st.write("Rejection reason was not available in the confirmed information.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. DOCUMENT
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>DOCUMENT</h3>", unsafe_allow_html=True)
    
    can_generate = True
    if plan.action_route in ["NO_VERIFIED_ROUTE", "UNCERTAIN"]:
        can_generate = False
    if verification.status == "UNSUPPORTED":
        can_generate = False
        
    if can_generate:
        if st.button("Generate Appeal Document", type="primary"):
            with st.spinner("Generating controlled document..."):
                try:
                    out_path = os.path.join(os.getcwd(), "generated_appeal.docx")
                    template_path = os.path.join(os.getcwd(), "templates", "appeal_template.docx")
                    generated_path = generate_appeal(facts, plan, template_path, out_path)
                    
                    with open(generated_path, "rb") as file:
                        btn = st.download_button(
                            label="Download document",
                            data=file,
                            file_name="nyayapath_appeal.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    st.success("Appeal document ready.")
                except Exception as e:
                    st.error("We couldn't generate the document safely. Your case information has not been changed.")
    else:
        st.warning("NyayaPath cannot safely generate this document from the available verified information.")

    st.markdown("<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 3rem 0;'>", unsafe_allow_html=True)
    
    if st.button("Start New Case", type="secondary"):
        for key in ['uploaded_file_name', 'extracted_text', 'case_facts', 'facts_confirmed', 'selected_scheme', 'eligibility_results', 'rejection_result', 'verification_result', 'evidence_results', 'action_plan', 'document_generated']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.extraction_status = 'FILE_SELECTED'
        st.session_state.current_page = "INTAKE"
        st.rerun()
