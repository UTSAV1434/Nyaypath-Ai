import streamlit as st

def render_header(context_text=""):
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
        <h1 style="font-size: 3rem; color: #333; margin: 0; font-weight: normal; display: flex; align-items: center; justify-content: center; gap: 10px;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M3 10l9-7 9 7"/><path d="M7 10v6a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-6"/><path d="M5 21h14"/></svg> 
            NyayaPath
        </h1>
        <p style="color: #666; font-size: 1.2rem; margin: 0; margin-top: 0.2rem;">
            Your AI Copilot for Welfare Appeals
        </p>
    </div>
    """, unsafe_allow_html=True)
