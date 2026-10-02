import streamlit as st
from services.evidence_checker import check_evidence

def render_evidence_view():
    st.markdown("<h2 style='margin-bottom: 0.5rem;'>What you have — and what's missing</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--muted-text); margin-bottom: 3rem; font-size: 1.1rem; max-width: 800px; line-height: 1.6;'>"
                "Review the evidence required for this case and see what still needs to be provided."
                "</p>", unsafe_allow_html=True)

    # 1. Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Verify", type="secondary"):
            st.session_state.current_page = "VERIFY"
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

    facts = st.session_state.get('case_facts')
    if not facts:
        st.error("No confirmed facts available.")
        return

    # 3. Process/Cache Evidence Results
    if 'evidence_results' not in st.session_state:
        st.session_state.evidence_results = check_evidence(facts, scheme)

    evidence_results = st.session_state.evidence_results

    # 4. Render Evidence Checklist
    for item in evidence_results:
        req = next((r for r in scheme.required_documents if r.document_id == item.id), None)
        if not req: continue
        
        # Display state icon and color
        if item.status == 'AVAILABLE':
            color = "var(--success-color)"
            icon = "✓"
            status_text = "Available"
        elif item.status == 'MISSING':
            color = "var(--error-color)"
            icon = "○"
            status_text = "Missing"
        else:
            color = "var(--warning-color)"
            icon = "?"
            status_text = "Needs verification"
            
        st.markdown(f"**{item.name}**")
        st.markdown(f"<span style='color: {color}; font-weight: bold; font-size: 1.2rem;'>{icon}</span> <span style='color: var(--text-color); font-weight: 500;'>{status_text}</span>", unsafe_allow_html=True)
        
        # Condition logic
        if req.mandatory:
            st.markdown("<span style='font-size: 0.85rem; color: var(--error-color);'>Required</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='font-size: 0.85rem; color: var(--muted-text);'>May be required</span>", unsafe_allow_html=True)
            
        if getattr(req, "condition", None):
            st.markdown(f"<span style='font-size: 0.85rem; color: var(--muted-text);'>Condition: {req.condition}</span>", unsafe_allow_html=True)

        # Show Why Expander
        with st.expander("Show Why"):
            st.markdown("**Why it matters:**")
            st.write(req.purpose)
            
            source_meta = next((s for s in scheme.official_sources if s.source_id == item.source_id), None)
            
            if source_meta:
                st.markdown("**Source:**")
                st.write(source_meta.title)
                
                st.markdown("**Academic year:**")
                st.write(source_meta.applicable_year)
                
                st.markdown("**Source status:**")
                status_color = "var(--warning-color)" if "historical" in str(source_meta.source_status).lower() else "var(--success-color)"
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{source_meta.source_status.upper()}</span>", unsafe_allow_html=True)
                
                st.markdown("**Source location:**")
                loc = []
                if getattr(req, "source_section", None): loc.append(f"Section: {req.source_section}")
                if getattr(req, "source_page", None): loc.append(f"Page: {req.source_page}")
                if loc:
                    st.write(" | ".join(loc))
                else:
                    st.write("Source location not available")
            else:
                st.write("Source details unavailable.")

        st.markdown("<hr style='border: 0; border-top: 1px solid var(--background-alt); margin: 1rem 0;'>", unsafe_allow_html=True)

    # 5. Continue to Action Plan
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue to Action Plan", type="primary"):
        st.session_state.current_page = "ACTION"
        st.rerun()

