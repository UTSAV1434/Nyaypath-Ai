import streamlit as st
import traceback
from services.extraction import extract_case_facts

def render_review_view():
    st.markdown("<h2 style='margin-bottom: 0.5rem;'>Here's what we understood</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--muted-text); margin-bottom: 3rem; font-size: 1.1rem; max-width: 800px; line-height: 1.6;'>"
                "Review these details before we check the rules. Correct anything that looks wrong."
                "</p>", unsafe_allow_html=True)

    # Allow returning to Intake
    if st.button("← Back to Intake", type="secondary"):
        st.session_state.current_page = "INTAKE"
        st.rerun()

    st.markdown("<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 2rem 0;'>", unsafe_allow_html=True)

    if 'extracted_text' not in st.session_state or not st.session_state.extracted_text:
        st.error("No extracted text found. Please return to Intake and upload a document.")
        return

    # Initialize extraction state
    if 'extraction_status' not in st.session_state:
        st.session_state.extraction_status = 'EXTRACTION_PENDING'

    if st.session_state.extraction_status == 'EXTRACTION_PENDING':
        with st.spinner("Extracting structured facts..."):
            try:
                # Call Gemini ONLY once
                facts = extract_case_facts(user_description="", pdf_text=st.session_state.extracted_text)
                
                # Check if facts object is essentially empty (extraction failure fallback)
                if not facts.applicant_facts and not facts.stated_rejection_reason and not facts.reference_id:
                    st.session_state.extraction_status = 'EXTRACTION_ERROR'
                else:
                    st.session_state.case_facts = facts
                    st.session_state.extraction_status = 'REVIEW_REQUIRED'
                    st.session_state.facts_confirmed = False
                    
                    # Store original facts for "changed" state tracking
                    st.session_state.original_applicant_facts = facts.applicant_facts.copy() if facts.applicant_facts else {}
                    st.session_state.original_rejection_reason = facts.stated_rejection_reason
                    st.session_state.original_reference_id = facts.reference_id
                    
                    # Scheme Detection heuristic
                    detected_scheme = None
                    text_lower = st.session_state.extracted_text.lower()
                    if "pm-usp" in text_lower or "csss" in text_lower or "central sector scheme of scholarship" in text_lower:
                        detected_scheme = "PM-USP CSSS"
                    elif "top class education for sc" in text_lower or "top class sc" in text_lower:
                        detected_scheme = "Top Class Education for SC Students"
                    
                    st.session_state.selected_scheme = detected_scheme
            except Exception as e:
                st.session_state.extraction_status = 'EXTRACTION_ERROR'

        st.rerun()

    if st.session_state.extraction_status == 'EXTRACTION_ERROR':
        st.error("We couldn't reliably structure the information from this notice.")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Retry extraction", type="primary"):
                st.session_state.extraction_status = 'EXTRACTION_PENDING'
                st.rerun()
        with col2:
            if st.button("Return to intake", type="secondary"):
                st.session_state.current_page = "INTAKE"
                st.rerun()
        return

    if st.session_state.extraction_status in ['REVIEW_REQUIRED', 'FACTS_CONFIRMED']:
        facts = st.session_state.case_facts
        
        # Helper to render a field
        def render_field(label, key, current_val, original_val, is_applicant_fact=True):
            st.markdown(f"**{label}**")
            
            # Show original provenance if available
            provenance = "From uploaded notice" if original_val is not None else "Not found in the notice"
            st.markdown(f"<span style='font-size: 0.85rem; color: var(--muted-text);'>{provenance}</span>", unsafe_allow_html=True)
            
            # Determine type from current_val or original_val
            val_type = type(current_val) if current_val is not None else type(original_val) if original_val is not None else str
            
            parsed_val = None
            if val_type == bool:
                # Use selectbox for explicit True/False/Missing
                options = ["True", "False", "Not Found"]
                default_idx = 0 if current_val is True else 1 if current_val is False else 2
                new_str = st.selectbox("Edit boolean", options, index=default_idx, key=f"input_{key}", label_visibility="collapsed")
                if new_str == "True": parsed_val = True
                elif new_str == "False": parsed_val = False
                else: parsed_val = None
            elif val_type == int or val_type == float:
                # Use number input, but we need to handle None. Streamlit's number_input requires a value.
                # If we want to allow None, we can use a text_input and explicitly cast it.
                display_val = str(current_val) if current_val is not None else ""
                new_str = st.text_input("Edit number", value=display_val, key=f"input_{key}", label_visibility="collapsed", placeholder="Add numeric value")
                new_str = new_str.strip()
                if new_str == "":
                    parsed_val = None
                else:
                    try:
                        parsed_val = float(new_str) if '.' in new_str else int(new_str)
                    except ValueError:
                        # Revert or keep as string if malformed, but wait: prompt says "do not silently coerce questionable text".
                        # We will just preserve the string, the backend will return UNCERTAIN.
                        parsed_val = new_str
            else:
                display_val = str(current_val) if current_val is not None else ""
                new_str = st.text_input("Edit text", value=display_val, key=f"input_{key}", label_visibility="collapsed", placeholder="Add text value")
                parsed_val = new_str.strip() if new_str.strip() != "" else None

            if parsed_val != current_val:
                if is_applicant_fact:
                    facts.applicant_facts[key] = parsed_val
                elif key == 'stated_rejection_reason':
                    facts.stated_rejection_reason = parsed_val
                elif key == 'reference_id':
                    facts.reference_id = parsed_val
                elif key == 'selected_scheme':
                    st.session_state.selected_scheme = parsed_val

                st.session_state.facts_confirmed = False
                st.session_state.extraction_status = 'REVIEW_REQUIRED'
                # Invalidate downstream state
                for key in ['evidence_results', 'action_plan', 'verification_result', 'eligibility_results', 'rejection_result']:
                    if key in st.session_state:
                        del st.session_state[key]

            # Changed indicator
            if parsed_val != original_val and (parsed_val is not None or original_val is not None):
                st.markdown(f"<span style='font-size: 0.85rem; color: var(--warning-color);'>Changed</span>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;'>CASE</h3>", unsafe_allow_html=True)
        
        # Scheme selection
        st.markdown("**Scheme**")
        scheme_options = ["None (Scheme needs confirmation)", "PM-USP CSSS", "Top Class Education for SC Students"]
        current_scheme = st.session_state.get('selected_scheme')
        
        # Determine display index
        if not current_scheme:
            selected_idx = 0
            st.warning("Scheme needs confirmation")
        else:
            selected_idx = scheme_options.index(current_scheme) if current_scheme in scheme_options else 0
            if st.session_state.extraction_status != 'FACTS_CONFIRMED' and current_scheme in ["PM-USP CSSS", "Top Class Education for SC Students"]:
                st.info("Suggested scheme from extraction. Please confirm.")
            
        new_scheme_sel = st.selectbox("Select Scheme", scheme_options, index=selected_idx, label_visibility="collapsed")
        new_scheme = new_scheme_sel if new_scheme_sel != "None (Scheme needs confirmation)" else None
        
        if new_scheme != current_scheme:
            st.session_state.selected_scheme = new_scheme
            st.session_state.facts_confirmed = False
            st.session_state.extraction_status = 'REVIEW_REQUIRED'
            for key in ['evidence_results', 'action_plan', 'verification_result', 'eligibility_results', 'rejection_result']:
                if key in st.session_state:
                    del st.session_state[key]
        st.markdown("<br>", unsafe_allow_html=True)

        render_field("Application/reference ID", "reference_id", facts.reference_id, st.session_state.original_reference_id, is_applicant_fact=False)
        render_field("Rejection reason", "stated_rejection_reason", facts.stated_rejection_reason, st.session_state.original_rejection_reason, is_applicant_fact=False)

        # Applicant Facts categorization
        academic_keys = ['class_xii_percentile', 'education_level', 'course', 'course_type', 'course_mode', 'institution', 'is_beyond_class_12']
        financial_keys = ['income', 'family_income']
        
        st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-top: 1rem;'>ACADEMIC</h3>", unsafe_allow_html=True)
        for k in academic_keys:
            val = facts.applicant_facts.get(k)
            orig_val = st.session_state.original_applicant_facts.get(k)
            # Display if it was in the extracted facts or if we explicitly want to show the field
            if k in facts.applicant_facts or k in st.session_state.original_applicant_facts:
                render_field(k.replace('_', ' ').capitalize(), k, val, orig_val)

        st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-top: 1rem;'>FINANCIAL</h3>", unsafe_allow_html=True)
        for k in financial_keys:
            if k in facts.applicant_facts or k in st.session_state.original_applicant_facts:
                val = facts.applicant_facts.get(k)
                orig_val = st.session_state.original_applicant_facts.get(k)
                render_field(k.replace('_', ' ').capitalize(), k, val, orig_val)

        st.markdown("<h3 style='color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-top: 1rem;'>OTHER FACTS</h3>", unsafe_allow_html=True)
        for k, val in facts.applicant_facts.items():
            if k not in academic_keys and k not in financial_keys:
                orig_val = st.session_state.original_applicant_facts.get(k)
                render_field(k.replace('_', ' ').capitalize(), k, val, orig_val)

        st.markdown("<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 3rem 0;'>", unsafe_allow_html=True)

        if st.session_state.facts_confirmed:
            st.success("Facts confirmed.")
            if st.button("Continue to Verification", type="primary"):
                st.session_state.current_page = "VERIFY"
                st.rerun()
        else:
            if st.button("Confirm information", type="primary"):
                st.session_state.facts_confirmed = True
                st.session_state.extraction_status = 'FACTS_CONFIRMED'
                st.rerun()
            st.markdown("<p style='font-size: 0.85rem; color: var(--muted-text); margin-top: 0.5rem;'>NyayaPath will use these confirmed details to check the published scheme criteria.</p>", unsafe_allow_html=True)

