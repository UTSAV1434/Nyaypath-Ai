import streamlit as st

def apply_design_system():
    # Insert custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
        
        /* Base tokens */
        :root {
            --bg-color: #ffffff;
            --surface-color: #ffffff;
            --ink-color: #333333;
            --accent-color: #4b5563;
            --text-color: #333333;
            --muted-text: #666666;
            --border-color: #333333;
        }

        /* Overall App Background & Text */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Patrick Hand', cursive !important;
        }
        
        /* Apply font everywhere */
        html, body, [class*="css"], [class*="st-"], h1, h2, h3, h4, p, div, span, button, input {
            font-family: 'Patrick Hand', cursive !important;
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: var(--ink-color) !important;
            font-weight: normal !important;
        }

        /* Buttons */
        .stButton>button[kind="primary"] {
            background-color: var(--accent-color) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            font-size: 1.4rem !important;
            width: 100%;
            transition: all 0.2s ease;
        }
        
        .stButton>button[kind="secondary"] {
            background-color: transparent !important;
            color: var(--ink-color) !important;
            border: 1px solid var(--ink-color) !important;
            border-radius: 6px !important;
            padding: 0.4rem 1.2rem !important;
            font-size: 1.1rem !important;
        }

        /* Uploader custom styling */
        [data-testid="stFileUploader"] {
            background-color: var(--surface-color);
            border: 2px dashed #888;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
        }
        
        [data-testid="stFileUploader"] section {
            padding: 0;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Container styling to match the card */
        .main-card {
            border: 1px solid #333;
            border-radius: 8px;
            padding: 2rem;
            background: #fff;
            max-width: 800px;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)
