import streamlit as st
import textwrap

def render_progress(current_step=1):
    steps = [
        "Intake",
        "Fact Review",
        "Verification",
        "Evidence",
        "Action Plan",
        "Case File"
    ]
    
    html = '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3rem; position: relative; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; padding: 0 20px;">'
    html += '<div style="position: absolute; top: 15px; left: 40px; right: 40px; height: 1px; background-color: #999; z-index: 0;"></div>'
    for i, step in enumerate(steps, 1):
        bg_color = "#4b5563" if i == current_step else "#fff"
        text_color = "#fff" if i == current_step else "#4b5563"
        border = "1px solid #4b5563" if i != current_step else "1px solid #4b5563"
        label_color = "#333" if i == current_step else "#666"
        
        step_html = f'''<div style="display: flex; flex-direction: column; align-items: center; z-index: 1;">
<div style="width: 30px; height: 30px; border-radius: 50%; background-color: {bg_color}; color: {text_color}; border: {border}; display: flex; align-items: center; justify-content: center; font-size: 14px; margin-bottom: 8px;">
{i}
</div>
<div style="font-size: 1.1rem; color: {label_color}; white-space: nowrap;">{step}</div>
</div>'''
        html += step_html
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)
