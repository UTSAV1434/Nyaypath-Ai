import streamlit as st

def render_status(status_type, explanation=""):
    """
    Renders a status badge and optional explanation according to NyayaPath design tokens.
    status_type: VERIFIED, UNCERTAIN, POTENTIAL CONFLICT, NOT MET, MET
    """
    icon_map = {
        "VERIFIED": "✓",
        "MET": "✓",
        "UNCERTAIN": "?",
        "POTENTIAL CONFLICT": "⚠",
        "NOT MET": "✕"
    }
    
    bg_map = {
        "VERIFIED": "#E8F5E9",
        "MET": "#E8F5E9",
        "UNCERTAIN": "#FFF8E1",
        "POTENTIAL CONFLICT": "#FFEBEE",
        "NOT MET": "#F5F5F5"
    }
    
    color_map = {
        "VERIFIED": "var(--success-color)",
        "MET": "var(--success-color)",
        "UNCERTAIN": "var(--warning-color)",
        "POTENTIAL CONFLICT": "var(--conflict-color)",
        "NOT MET": "var(--muted-text)"
    }
    
    st_type = status_type.upper()
    icon = icon_map.get(st_type, "")
    bg = bg_map.get(st_type, "#F5F5F5")
    color = color_map.get(st_type, "var(--muted-text)")
    
    html = f"""
    <div style="display: flex; align-items: flex-start; margin: 0.5rem 0;">
        <div style="display: inline-flex; align-items: center; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; background-color: {bg}; color: {color};">
            <span style="margin-right: 6px; font-size: 0.9rem;">{icon}</span> {status_type}
        </div>
        <div style="margin-left: 1rem; color: var(--text-color); font-size: 0.9rem; line-height: 1.5; padding-top: 0.1rem;">
            {explanation}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
