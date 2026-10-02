import streamlit as st
from services.eligibility import evaluate_scheme
from services.rejection_verifier import verify_rejection
from services.verifier import final_verify
from utils.citations import format_citation
from utils.helpers import load_scheme_by_name
from models.schemas import ActionPlan

def render_verification_view():
    st.markdown("<h2 style='margin-bottom: 0.5rem;'>Let's check the published criteria</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--muted-text); margin-bottom: 3rem; font-size: 1.1rem; max-width: 800px; line-height: 1.6;'>"
                "NyayaPath compares the information you confirmed against the structured scheme criteria available in its knowledge base."
                "</p>", unsafe_allow_html=True)

    if st.button("← Back to Review", type="secondary"):
        st.session_state.current_page = "REVIEW"
        st.rerun()

    st.markdown("<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 2rem 0;'>", unsafe_allow_html=True)

    # 1. Preconditions
    if not st.session_state.get('facts_confirmed', False):
        st.error("You must confirm the case facts in the Review step before proceeding.")
        return
        
    scheme_name = st.session_state.get('selected_scheme')
    if not scheme_name or scheme_name == "None (Scheme needs confirmation)":
        st.error("You must select a supported scheme in the Review step.")
        return

    facts = st.session_state.get('case_facts')
    if not facts:
        st.error("No confirmed facts available.")
        return

    # 2. Run / Cache Analysis
    if 'eligibility_results' not in st.session_state or st.session_state.get('_last_scheme_verified') != scheme_name:
        with st.spinner("Checking published rules..."):
            try:
                scheme = load_scheme_by_name(scheme_name)
                
                # Deterministic logic
                eligibility_results = evaluate_scheme(scheme.eligibility_criteria, facts)
                rejection_result = verify_rejection(facts, scheme.eligibility_criteria)
                
                verification_result = final_verify(scheme, eligibility_results, rejection_result, plan=None)
                
                # Cache results
                st.session_state.eligibility_results = eligibility_results
                st.session_state.rejection_result = rejection_result
                st.session_state.verification_result = verification_result
                st.session_state.verified_scheme = scheme
                st.session_state._last_scheme_verified = scheme_name
                
            except Exception as e:
                st.error(f"Failed to load or verify scheme data: {e}")
                return

    # 3. Retrieve Cached Results
    results = st.session_state.eligibility_results
    scheme = st.session_state.verified_scheme
    rejection = st.session_state.rejection_result
    final_verif = st.session_state.verification_result

    # 4. Overall Summary
    met_count = sum(1 for r in results if r.status == 'MET')
    not_met_count = sum(1 for r in results if r.status == 'NOT_MET')
    uncertain_count = sum(1 for r in results if r.status == 'UNCERTAIN')
    
    summary_parts = []
    if met_count > 0: summary_parts.append(f"{met_count} criteria met")
    if not_met_count > 0: summary_parts.append(f"{not_met_count} criteria not met")
    if uncertain_count > 0: summary_parts.append(f"{uncertain_count} needs verification")
    
    st.markdown(f"**{' · '.join(summary_parts)}**")
    
    if not_met_count > 0:
        st.markdown("<p style='color: var(--error-color);'>At least one published criterion is not satisfied based on the confirmed information.</p>", unsafe_allow_html=True)
    elif uncertain_count > 0:
        st.markdown("<p style='color: var(--warning-color);'>Some criteria could not be verified with the available information.</p>", unsafe_allow_html=True)
    elif met_count > 0:
        st.markdown("<p style='color: var(--success-color);'>All currently evaluated criteria are satisfied based on the confirmed information.</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-top: 2rem;'>ELIGIBILITY</h3>", unsafe_allow_html=True)

    # 5. Criterion Results & Show Me Why
    for res in results:
        # Find corresponding rule
        rule = next((r for r in scheme.eligibility_criteria if r.criterion_id == res.criterion_id), None)
        if not rule: continue
        
        # Display state icon and color
        color = "var(--success-color)" if res.status == 'MET' else "var(--error-color)" if res.status == 'NOT_MET' else "var(--warning-color)"
        icon = "✓" if res.status == 'MET' else "✕" if res.status == 'NOT_MET' else "?"
        
        st.markdown(f"**{rule.name}**")
        st.markdown(f"<span style='color: {color}; font-weight: bold;'>{icon} {res.status}</span>", unsafe_allow_html=True)
        
        # Friendly representation of the rule evaluation
        fact_val = facts.applicant_facts.get(rule.field, 'Missing')
        st.markdown(f"<span style='font-size: 0.9rem; color: var(--muted-text);'>{fact_val} {rule.operator} {rule.value}</span>", unsafe_allow_html=True)
        
        with st.expander("Show Me Why"):
            st.markdown("**What we checked:**")
            st.write(f"The confirmed applicant fact for `{rule.field}`: {fact_val}")
            
            st.markdown("**Published rule:**")
            st.write(rule.description)
            
            # Find official source metadata
            source_meta = next((s for s in scheme.official_sources if s.source_id == rule.source_id), None)
            
            if source_meta:
                st.markdown("**Source:**")
                st.write(f"{source_meta.title}")
                
                st.markdown("**Academic year:**")
                st.write(source_meta.applicable_year)
                
                st.markdown("**Source status:**")
                status_color = "var(--warning-color)" if "historical" in str(source_meta.source_status).lower() else "var(--success-color)"
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{source_meta.source_status.upper()}</span>", unsafe_allow_html=True)
                
                if "historical" in str(source_meta.source_status).lower():
                    st.markdown("**Current-year applicability:**")
                    st.write("Uncertain")
                    
                st.markdown("**Source location:**")
                loc = []
                if rule.source_section: loc.append(f"Section: {rule.source_section}")
                if rule.source_page: loc.append(f"Page: {rule.source_page}")
                if loc:
                    st.write(" | ".join(loc))
                else:
                    st.write("Source location not available")
            else:
                st.write("Source information missing.")

        st.markdown("<hr style='border: 0; border-top: 1px solid var(--background-alt); margin: 1rem 0;'>", unsafe_allow_html=True)

    # 6. Rejection Conflict
    if rejection.status == "POTENTIAL_CONFLICT":
        st.markdown("<h3 style='color: var(--warning-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-top: 2rem;'>⚠ POTENTIAL CONFLICT</h3>", unsafe_allow_html=True)
        st.warning("The stated rejection reason appears inconsistent with the published criterion. Available source information may not agree. NyayaPath has not treated either version as definitive.")
        
        with st.expander("Show Me Why"):
            st.markdown("**Stated Rejection Reason:**")
            st.write(rejection.stated_reason)
            st.markdown("**Result:**")
            st.write(rejection.explanation)
            
    # 7. Final Verification
    st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-top: 2rem;'>VERIFICATION STATUS</h3>", unsafe_allow_html=True)
    
    if final_verif.status == "PASS":
        st.success("All conclusions are source-backed and deterministic.")
    elif final_verif.status == "UNSUPPORTED":
        st.error("NyayaPath could not establish a valid source for some conclusions.")
        for msg in final_verif.unsupported_claims:
            st.write(f"- {msg}")
    elif final_verif.status == "UNCERTAIN":
        st.warning("Some information could not be confirmed.")
        st.write(final_verif.explanation)
    else:
        st.info(final_verif.status)
        st.write(final_verif.explanation)

    st.markdown("<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 3rem 0;'>", unsafe_allow_html=True)
    if st.button("Continue to Evidence", type="primary"):
        st.session_state.current_page = "EVIDENCE"
        st.rerun()

