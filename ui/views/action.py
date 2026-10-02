import streamlit as st
from services.action_planner import plan_action
from services.verifier import final_verify

def render_action_view():
    st.markdown("<h2 style='margin-bottom: 0.5rem;'>Here's what you can do next</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--muted-text); margin-bottom: 3rem; font-size: 1.1rem; max-width: 800px; line-height: 1.6;'>"
                "NyayaPath only shows routes that can be supported by the available scheme information."
                "</p>", unsafe_allow_html=True)

    # 1. Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Evidence", type="secondary"):
            st.session_state.current_page = "EVIDENCE"
            st.rerun()

    st.markdown("<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 2rem 0;'>", unsafe_allow_html=True)

    # 2. Preconditions
    if not st.session_state.get('facts_confirmed', False):
        st.error("You must confirm the case facts in the Review step before proceeding.")
        return
        
    scheme = st.session_state.get('verified_scheme')
    if not scheme:
        st.error("You must complete the verification step first.")
        return

    eligibility = st.session_state.get('eligibility_results')
    rejection = st.session_state.get('rejection_result')
    evidence = st.session_state.get('evidence_results')

    if not eligibility or not rejection or not evidence:
        st.error("Missing verification or evidence results.")
        return

    # 3. Process/Cache Action Plan
    if 'action_plan' not in st.session_state:
        st.session_state.action_plan = plan_action(scheme, eligibility, rejection, evidence)
        # 4. Rerun Final Verifier with real Action Plan
        st.session_state.verification_result = final_verify(scheme, eligibility, rejection, plan=st.session_state.action_plan)

    plan = st.session_state.action_plan

    # 5. Display Main Action
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>NEXT ACTION</h3>", unsafe_allow_html=True)
    
    if plan.action_route == "NO_VERIFIED_ROUTE":
        st.error("No supported route could be established from the available scheme information.")
    elif plan.action_route == "UNCERTAIN":
        st.warning("NyayaPath could not verify a reliable next step from the available information.")
    else:
        st.markdown(f"<h2 style='color: var(--success-color);'>{plan.action_route.upper()}</h2>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render details
    st.markdown("**Why**")
    st.write(plan.reason)

    if plan.action_route not in ["NO_VERIFIED_ROUTE", "UNCERTAIN"]:
        st.markdown("**Authority**")
        st.write(plan.authority if plan.authority else "Not specified in scheme")

        st.markdown("**Deadline**")
        if not plan.deadline:
            st.markdown("<span style='color: var(--warning-color);'>Not verified</span>", unsafe_allow_html=True)
            st.markdown("<span style='font-size: 0.85rem; color: var(--muted-text);'>Deadline could not be verified from the available official information.</span>", unsafe_allow_html=True)
        else:
            st.write(plan.deadline)

        # Historical source warning heuristic
        # If the scheme source itself is historical, the action plan drawn from it might be historical
        is_historical = any("historical" in str(s.source_status).lower() for s in scheme.official_sources)
        if is_historical:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Source status:** <span style='color: var(--warning-color); font-weight: bold;'>HISTORICAL</span>", unsafe_allow_html=True)
            st.markdown("**Current-year applicability:** Uncertain", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Evidence needed**")
        if plan.missing_evidence:
            st.write("Evidence still needed:")
            for e in plan.missing_evidence:
                st.write(f"- {e.name}")
        else:
            st.write("All required evidence appears to be available.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Immediate next step**")
    if plan.missing_evidence and plan.action_route not in ["NO_VERIFIED_ROUTE", "UNCERTAIN"]:
        st.write("Collect the missing evidence before submitting.")
    st.write(plan.immediate_next_action)

    st.markdown("<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 3rem 0;'>", unsafe_allow_html=True)
    if st.button("Continue to Case File", type="primary"):
        st.session_state.current_page = "CASE_FILE"
        st.rerun()

