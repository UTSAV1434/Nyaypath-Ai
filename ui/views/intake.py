import streamlit as st
import tempfile
import os
from services.pdf_parser import extract_text_from_pdf

def render_intake_view():
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 1.8rem; margin-top: 0; margin-bottom: 0.5rem;'>Upload Rejection Notice</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #444; font-size: 1.2rem; margin-bottom: 1.5rem;'>Start by uploading the rejection notice you received from the government scheme.</p>", unsafe_allow_html=True)
    
    # Initialize session state for file upload tracking
    if 'intake_state' not in st.session_state:
        st.session_state.intake_state = 'EMPTY'
        
    if st.session_state.intake_state == 'EMPTY':
        uploaded_file = st.file_uploader("Upload Rejection Notice", type=["pdf"], label_visibility="collapsed")
        
        st.markdown("""
        <hr style="border: 0; border-top: 1px solid #ddd; margin-bottom: 1.5rem; margin-top: 1.5rem;">
        <div style="display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 2rem;">
            <div style="font-size: 1.5rem; color: #333; border: 1px solid #333; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 16px;">i</div>
            <div style="font-size: 1.1rem; color: #444; line-height: 1.4;">We will securely extract key facts from your notice using AI and check your eligibility against scheme rules and guidelines.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # We must process the actual PDF using our deterministic backend service.
            with st.spinner("Processing document..."):
                # Write uploaded bytes to a temp file for the parser
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    extracted_text = extract_text_from_pdf(tmp_path)
                    
                    if extracted_text.startswith("ERROR: Unable to extract text"):
                        if "Scanned/image PDFs are not supported" in extracted_text:
                            st.session_state.intake_state = 'UNSUPPORTED'
                        else:
                            st.session_state.intake_state = 'ERROR'
                        st.session_state.extracted_text = None
                    else:
                        st.session_state.intake_state = 'SUCCESS'
                        st.session_state.extracted_text = extracted_text
                        st.session_state.uploaded_file_name = uploaded_file.name
                        st.session_state.intake_status = 'EXTRACTION_SUCCESS'
                except Exception as e:
                    st.session_state.intake_state = 'ERROR'
                    st.session_state.extracted_text = None
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
            st.rerun()
            
        st.button("Analyze Notice →", type="primary", use_container_width=True)

    elif st.session_state.intake_state == 'UNSUPPORTED':
        st.error("NyayaPath couldn't extract readable text from this PDF.\\n\\n"
                 "This MVP supports digital PDFs, but not scanned/image-only documents.\\n\\n"
                 "Try uploading a text-based PDF.")
        if st.button("Try another file", type="secondary"):
            st.session_state.intake_state = 'EMPTY'
            st.rerun()

    elif st.session_state.intake_state == 'ERROR':
        st.error("The uploaded file could not be read or is corrupted. Please try uploading a valid PDF document.")
        if st.button("Try another file", type="secondary"):
            st.session_state.intake_state = 'EMPTY'
            st.rerun()

    elif st.session_state.intake_state == 'SUCCESS':
        st.success(f"Document '{st.session_state.get('uploaded_file_name', '')}' successfully uploaded and processed.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Analyze Notice →", type="primary"):
                st.session_state.current_page = "REVIEW"
                st.rerun()
        with col2:
            if st.button("Upload different file", type="secondary"):
                st.session_state.intake_state = 'EMPTY'
                # Clear existing session data for intake
                keys_to_clear = ['extracted_text', 'uploaded_file_name', 'intake_status', 
                                 'case_facts', 'extraction_status', 'facts_confirmed', 'selected_scheme']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)
